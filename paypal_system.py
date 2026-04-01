from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str  # e.g., "daily", "weekly"
    priority: str  # "low", "medium", "high"
    start_time: Optional[str] = None  # e.g., "08:00"
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True
        # Note: Recurring logic handled separately (e.g., in scheduler)

    def is_due_today(self) -> bool:
        return self.frequency == "daily" and not self.completed

    def get_priority_score(self) -> int:
        return {"low": 1, "medium": 2, "high": 3}[self.priority]

    def get_end_time(self) -> Optional[str]:
        if not self.start_time:
            return None
        start = datetime.strptime(self.start_time, "%H:%M")
        end = start + timedelta(minutes=self.duration_minutes)
        return end.strftime("%H:%M")


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

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        return [t for t in self.tasks if t.completed == completed]

    def get_info(self) -> str:
        return f"{self.name} is a {self.age}-year-old {self.species}."

    def mark_task_complete(self, task: Task) -> None:
        if task in self.tasks:
            task.completed = True
            if task.frequency == "daily":
                new_task = Task(
                    description=task.description,
                    duration_minutes=task.duration_minutes,
                    frequency=task.frequency,
                    priority=task.priority,
                    start_time=task.start_time,
                    completed=False
                )
                self.tasks.append(new_task)


class Owner:
    def __init__(self, name: str, available_time_minutes: int):
        self.name = name
        self.available_time_minutes = available_time_minutes
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_pending_tasks(self) -> List[Task]:
        return [t for t in self.get_all_tasks() if not t.completed]

    def filter_tasks_by_pet(self, pet_name: str) -> List[Task]:
        pet = next((p for p in self.pets if p.name == pet_name), None)
        return pet.tasks if pet else []


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        # Sort by start_time (HH:MM format)
        return sorted(tasks, key=lambda t: t.start_time or "23:59")

    def filter_tasks_by_status(self, tasks: List[Task], completed: bool) -> List[Task]:
        return [t for t in tasks if t.completed == completed]

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        warnings = []
        for i, task1 in enumerate(tasks):
            if not task1.start_time:
                continue
            for task2 in tasks[i+1:]:
                if not task2.start_time:
                    continue
                if self.times_overlap(task1, task2):
                    warnings.append(f"Conflict: {task1.description} and {task2.description} overlap.")
        return warnings

    def times_overlap(self, task1: Task, task2: Task) -> bool:
        if not task1.start_time or not task2.start_time:
            return False
        start1 = datetime.strptime(task1.start_time, "%H:%M")
        end1 = start1 + timedelta(minutes=task1.duration_minutes)
        start2 = datetime.strptime(task2.start_time, "%H:%M")
        end2 = start2 + timedelta(minutes=task2.duration_minutes)
        return max(start1, start2) < min(end1, end2)

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
