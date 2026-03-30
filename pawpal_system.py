from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
    name: str
    species: str
    age: int
    care_needs: dict = field(default_factory=dict)  # e.g. {"feeding": "2x/day", "walk": "30min"}

    def get_care_needs(self):
        pass

    def update_info(self, **kwargs):
        pass


@dataclass
class Task:
    task_type: str          # "walk", "feed", "meds", etc.
    pet: Pet = None
    duration: int = 0       # in minutes
    priority: int = 1       # 1 = high, 2 = medium, 3 = low
    status: str = "pending" # "pending" or "completed"

    def mark_complete(self):
        pass

    def update(self, **kwargs):
        pass


@dataclass
class DailyPlan:
    date: str
    tasks: List[Task] = field(default_factory=list)
    available_time: int = 60  # in minutes

    def generate_plan(self):
        pass

    def display_plan(self):
        pass

    def explain_plan(self):
        pass


class User:
    def __init__(self, name: str, availability: int = 60, preferences: dict = None):
        self.name = name
        self.availability = availability          # minutes available today
        self.preferences = preferences or {}

    def log_in(self):
        pass

    def log_out(self):
        pass
