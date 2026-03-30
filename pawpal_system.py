from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Task:
    description: str
    duration: int           # in minutes
    frequency: str          # e.g. "daily", "weekly", "as needed"
    priority: int = 1       # 1 = high, 2 = medium, 3 = low
    status: str = "pending" # "pending" or "completed"

    def mark_complete(self):
        self.status = "completed"

    def reset(self):
        self.status = "pending"

    def is_complete(self) -> bool:
        return self.status == "completed"


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task: Task):
        if task in self.tasks:
            self.tasks.remove(task)

    def get_pending_tasks(self) -> List[Task]:
        return [t for t in self.tasks if not t.is_complete()]

    def get_completed_tasks(self) -> List[Task]:
        return [t for t in self.tasks if t.is_complete()]


class Owner:
    def __init__(self, name: str, availability: int = 60, preferences: dict = None):
        self.name = name
        self.availability = availability    # minutes available today
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> List[Task]:
        """Returns every task across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_all_pending_tasks(self) -> List[Task]:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_pending_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner, plan_date: date = None):
        self.owner = owner
        self.plan_date = plan_date or date.today()
        self.scheduled_tasks: List[Task] = []

    def generate_plan(self) -> List[Task]:
        """Sort pending tasks by priority and fit them within available time."""
        pending = self.owner.get_all_pending_tasks()
        pending.sort(key=lambda t: (t.priority, -t.duration))

        scheduled = []
        time_remaining = self.owner.availability
        for task in pending:
            if task.duration <= time_remaining:
                scheduled.append(task)
                time_remaining -= task.duration

        self.scheduled_tasks = scheduled
        return scheduled

    def display_plan(self) -> str:
        lines = [f"Daily plan for {self.plan_date} — {self.owner.name}"]
        lines.append(f"Available time: {self.owner.availability} minutes\n")
        for task in self.scheduled_tasks:
            lines.append(f"- {task.description} ({task.duration} min, {task.frequency}) [{task.status}]")
        if not self.scheduled_tasks:
            lines.append("No tasks scheduled.")
        return "\n".join(lines)

    def explain_plan(self) -> str:
        return (
            "Tasks were selected in priority order. "
            "Only pending tasks were considered. "
            "Tasks were added until the owner's available time ran out."
        )

    def mark_task_complete(self, task: Task):
        task.mark_complete()
