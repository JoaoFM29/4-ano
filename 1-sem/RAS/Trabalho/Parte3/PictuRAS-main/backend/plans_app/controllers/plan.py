from typing import Optional, List
from models.plan import Plan


def list_plans() -> List[Plan]:
    return Plan.objects()


def find_by_id(plan_id: str) -> Optional[Plan]:
    return Plan.objects.get(id=plan_id)


def insert_plan(plan: Plan) -> Optional[Plan]:
    plan.save()
    return plan


def update_plan(plan_id: str, plan: dict) -> Optional[Plan]:
    old_plan = Plan.objects.get(id=plan_id)
    old_plan.update(**plan)
    return Plan.objects.get(id=plan_id)


def delete_plan(plan_id: str) -> Optional[Plan]:
    plan = Plan.objects.get(id=plan_id)
    plan.delete()
    return plan