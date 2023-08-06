from __future__ import annotations

import asyncio
import json
import time
from functools import singledispatch
from typing import Any, Dict, Optional, Tuple, Union

import strangeworks as sw
from braket.annealing.problem import Problem
from braket.circuits import Circuit
from braket.circuits.serialization import IRType
from braket.ir.openqasm import Program as OpenQasmProgram
from braket.schema_common import BraketSchemaBase
from braket.tasks.annealing_quantum_task_result import AnnealingQuantumTaskResult
from braket.tasks.gate_model_quantum_task_result import GateModelQuantumTaskResult
from braket.tasks.quantum_task import QuantumTask
from strangeworks.core.client.resource import Resource
from strangeworks_core.errors.error import StrangeworksError
from strangeworks_core.types.job import Job, Status


# create a new class that inherits from QuantumTask and implement the abstract methods
class StrangeworksQuantumTask(QuantumTask):
    def __init__(self, job: Job, *args, **kwargs):
        self.job: Job = job

    @property
    def id(self) -> str:
        return self.job.slug

    def cancel(self) -> None:
        # todo: this will complain about typing. need to update strangeworks-python
        resource: Resource = self.job.resource
        if not self.job.external_identifier:
            raise StrangeworksError(
                "Job has not been submitted to the cloud yet. Missing external_identifier."  # noqa: E501
            )

        cancel_url = f"{resource.proxy_url()}/jobs/{self.job.external_identifier}"
        # todo: stgrangeworks-python is rest_client an optional thing. i dont think it should be # noqa: E501
        # this is something we should discuss
        sw.client.rest_client.delete(url=cancel_url)

    def state(self) -> str:
        resource: Resource = self.job.resource
        if not self.job.external_identifier:
            raise StrangeworksError(
                "Job has not been submitted to the cloud yet. Missing external_identifier."  # noqa: E501
            )

        res = sw.execute(resource, None, f"jobs/{self.job.external_identifier}")
        self.job = StrangeworksQuantumTask._transform_dict_to_job(res)
        if not self.job.resource:
            self.job.resource = resource

        if not self.job.remote_status:
            raise StrangeworksError("Job has no remote_status")
        return self.job.remote_status

    def result(self) -> Union[GateModelQuantumTaskResult, AnnealingQuantumTaskResult]:
        resource: Resource = self.job.resource
        if not self.job.external_identifier:
            raise StrangeworksError(
                "Job has not been submitted to the cloud yet. Missing external_identifier."  # noqa: E501
            )
        # loop until complete
        # then we can ask the platform for jobs ?
        # put this in a loop and the condition is the job.state is "COMPLETED"
        # then we can return the result
        while self.job.status not in {
            Status.COMPLETED,
            Status.FAILED,
            Status.CANCELLED,
        }:
            res = sw.execute(resource, None, f"jobs/{self.job.external_identifier}")
            self.job = StrangeworksQuantumTask._transform_dict_to_job(res)
            if not self.job.resource:
                self.job.resource = resource
            time.sleep(2.5)

        if self.job.status != Status.COMPLETED:
            raise StrangeworksError("Job did not complete successfully")
        # sw.jobs will return type errors until it updates their type hints
        # todo: update strangeworks-python job type hints
        # todo: at this point in time, sw.jobs returns a different type than sw.execute
        jobs = sw.jobs(slug=self.job.slug)
        if not jobs:
            raise StrangeworksError(
                "Job not found. Something went wrong with the strangeworks platform."
            )
        if len(jobs) != 1:
            raise StrangeworksError(
                "Multiple jobs found. Something went wrong with the strangeworks platform."  # noqa: E501
            )
        job: Job = jobs[0]
        if not job.files:
            raise StrangeworksError("Job has no files. Something went wrong.")
        files = list(
            filter(lambda f: f.file_name == "job_results_braket.json", job.files)
        )
        if len(files) != 1:
            raise StrangeworksError("Job has multiple files. Something went wrong.")

        file = files[0]
        if not file.url:
            raise StrangeworksError("Job file has no url. Something went wrong.")
        # why does this say it returns a list of files?
        # did it not just download the file?
        # is the contents not some dictionary?
        # todo probably have to update this in strangeworks-python
        contents = sw.download_job_files([file.url])
        if len(contents) != 1:
            raise StrangeworksError("Unable to download result file.")
        bsh = BraketSchemaBase.parse_raw_schema(json.dumps(contents[0]))
        task_result = GateModelQuantumTaskResult.from_object(bsh)
        return task_result

    def async_result(self) -> asyncio.Task:
        raise NotImplementedError

    def metadata(self, use_cached_value: bool = False) -> Dict[str, Any]:
        raise NotImplementedError

    @staticmethod
    def from_strangeworks_slug(slug: str) -> StrangeworksQuantumTask:
        # todo: at this point in time, sw.jobs returns a different type than sw.execute
        jobs = sw.jobs(slug=slug)
        if not jobs:
            raise StrangeworksError("No jobs found for slug")
        if len(jobs) != 1:
            raise StrangeworksError("Multiple jobs found for slug")
        job = jobs[0]
        return StrangeworksQuantumTask(job)

    @staticmethod
    def create(
        device_name: str,
        task_specification: Union[Circuit, Problem, OpenQasmProgram],
        shots: int,
        device_parameters: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None,
        *args,
        **kwargs,
    ) -> StrangeworksQuantumTask:
        # this is one way to allow the caller to specify a resource
        # but for now we can just get the first resource available.
        resource = kwargs.get("resource", None)
        if not resource:
            resources = sw.resources()
            if not resources:
                raise StrangeworksError("No strangeworks resources found")
            resource = next(
                rsc for rsc in resources if rsc.product.slug == "amazon-braket"
            )
            if not resource:
                raise StrangeworksError("No strangeworks amazon-braket resources found")

        circuit_type, circuit = _sw_task_specification(task_specification)
        payload = {
            "circuit_type": circuit_type,
            "circuit": circuit,
            "aws_device_name": device_name,
            "device_parameters": device_parameters if device_parameters else {},
            "shots": shots,
        }

        res = sw.execute(resource, payload, "jobs")
        sw_job = StrangeworksQuantumTask._transform_dict_to_job(res)
        if not sw_job.resource:
            sw_job.resource = resource
        # todo: can i use sw to create tags ?
        return StrangeworksQuantumTask(sw_job)

    # create a method that transforms the dict into a job
    # first it must convert the json keys from snake_case to camelCase
    # then it must create a job from the dict
    @staticmethod
    def _transform_dict_to_job(d: Dict[str, Any]) -> Job:
        # todo: this is unfortunate. dont like that we need to do this.
        def to_camel_case(snake_str):
            components = snake_str.split("_")
            # We capitalize the first letter of each component except the first one
            # with the 'title' method and join them together.
            return components[0] + "".join(x.title() for x in components[1:])

        remix = {to_camel_case(key): value for key, value in d.items()}
        return Job.from_dict(remix)


@singledispatch
def _sw_task_specification(
    task_specification: Union[Circuit, Problem, OpenQasmProgram]
) -> Tuple[str, str]:
    raise NotImplementedError


# register a function for each type
@_sw_task_specification.register
def _sw_task_specification_circuit(task_specification: Circuit) -> Tuple[str, str]:
    return "qasm", task_specification.to_ir(ir_type=IRType.OPENQASM).json()


@_sw_task_specification.register
def _sw_task_specification_problem(task_specification: Problem) -> Tuple[str, str]:
    raise NotImplementedError


@_sw_task_specification.register
def _sw_task_specification_openqasm(
    task_specification: OpenQasmProgram,
) -> Tuple[str, str]:
    return "qasm", task_specification.json()
