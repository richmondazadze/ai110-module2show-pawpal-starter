from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, time


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str  # e.g., "daily", "weekly"
    priority: str  # "low", "medium", "high"
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True

    def is_due_today(self) -> bool:
        # Simple check: assume daily tasks are due
        return self.frequency == "daily" and not self.completed

    def get_priority_score(self) -> int:
        return {"low": 1, "medium": 2, "high": 3}[self.priority]


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        return [t for t in self.tasks if not t.completed]

    def get_info(self) -> str:
        return f"{self.name} is a {self.age}-year-old {self.species}."


class Owner:
    def __init__(self, name: str, available_time_minutes: int):
        self.name = name
        self.available_time_minutes = available_time_minutes
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)
        pet.owner = self  # Assuming we add owner to Pet, but since Pet is dataclass, need to adjust

    def get_all_tasks(self) -> List[Task]:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_pending_tasks(self) -> List[Task]:
        return [t for t in self.get_all_tasks() if not t.completed]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_daily_plan(self) -> List[Task]:
        pending_tasks = self.owner.get_pending_tasks()
        # Sort by priority (high first), then by duration
        sorted_tasks = sorted(pending_tasks, key=lambda t: (-t.get_priority_score(), t.duration_minutes))
        # Fit into available time
        plan = []
        time_used = 0
        for task in sorted_tasks:
            if time_used + task.duration_minutes <= self.owner.available_time_minutes:
                plan.append(task)
                time_used += task.duration_minutes
        return plan

    def explain_plan(self, plan: List[Task]) -> str:
        if not plan:
            return "No tasks scheduled today."
        explanation = "Today's plan:\n"
        for task in plan:
            explanation += f"- {task.description} ({task.duration_minutes} min, priority: {task.priority})\n"
        remaining = self.owner.available_time_minutes - sum(t.duration_minutes for t in plan)
        explanation += f"Total time used: {sum(t.duration_minutes for t in plan)} min. Remaining time: {remaining} min."
        return explanation
