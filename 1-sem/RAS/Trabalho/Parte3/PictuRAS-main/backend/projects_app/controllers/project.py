from typing import Optional, List
from models.project import Project


def list_projects() -> List[Project]:
    return Project.objects()


def find_by_id(project_id: str) -> Optional[Project]:
    return Project.objects.get(id=project_id)


def find_user_projects(user_id: str) -> List[Project]:
    return Project.objects.filter(owner=user_id)


def insert_project(project: Project) -> Optional[Project]:
    project.save()
    return project


def update_project(project_id: str, project: dict) -> Optional[Project]:
    old_project = Project.objects.get(id=project_id)
    old_project.update(**project)
    return Project.objects.get(id=project_id)


def delete_project(project_id: str) -> Optional[Project]:
    project = Project.objects.get(id=project_id)
    project.delete()
    return project