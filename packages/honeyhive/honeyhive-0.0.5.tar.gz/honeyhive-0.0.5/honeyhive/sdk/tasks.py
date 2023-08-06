from typing import Optional, List
from honeyhive.api.models.tasks import TaskCreationQuery, TaskUpdateQuery, TaskResponse, ListTaskResponse
from honeyhive.api.models.fine_tuned_models import FineTunedModelResponse
from honeyhive.api.models.prompts import PromptResponse
from honeyhive.api.models.datasets import DatasetResponse
from honeyhive.api.models.metrics import MetricResponse
from honeyhive.api.models.utils import DeleteResponse
from honeyhive.sdk.init import honeyhive_client

def get_tasks(
    name: Optional[str] = None,
) -> ListTaskResponse:
    """Get all tasks"""
    client = honeyhive_client()
    return client.get_tasks(name=name)

def get_task(
    task_id: str
) -> TaskResponse:
    """Get a task"""
    client = honeyhive_client()
    return client.get_tasks(name=task_id)

def create_task(
    name: str,
    type: str,
    fine_tuned_models: Optional[List[FineTunedModelResponse]],
    prompts: Optional[List[PromptResponse]],
    datasets: Optional[List[DatasetResponse]],
    metrics: Optional[List[MetricResponse]]
) -> TaskResponse:
    """Create a task"""
    client = honeyhive_client()
    return client.create_task(
        task=TaskCreationQuery(
            name=name,
            type=type,
            fine_tuned_models=fine_tuned_models,
            prompts=prompts,
            datasets=datasets,
            metrics=metrics
        )
    )

def update_task(
    task_id: str,
    name: Optional[str] = None,
    type: Optional[str] = None,
    fine_tuned_models: Optional[List[FineTunedModelResponse]] = None,
    prompts: Optional[List[PromptResponse]] = None,
    datasets: Optional[List[DatasetResponse]] = None,
    metrics: Optional[List[MetricResponse]] = None
) -> TaskResponse:
    """Update a task"""
    client = honeyhive_client()
    return client.update_task(
        task_id=task_id,
        task=TaskUpdateQuery(
            name=name,
            type=type,
            fine_tuned_models=fine_tuned_models,
            prompts=prompts,
            datasets=datasets,
            metrics=metrics
        )
    )

def delete_task(
    task_id: str
) -> DeleteResponse:
    """Delete a task"""
    client = honeyhive_client()
    return client.delete_task(name=task_id)

__all__ = [
    "get_tasks",
    "get_task",
    "create_task",
    "update_task",
    "delete_task"
]