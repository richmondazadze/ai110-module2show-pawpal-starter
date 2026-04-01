import pytest
from paypal_system import Task, Pet, Owner, Scheduler


class TestTaskCompletion:
    """Test Task completion behavior."""
    
    def test_mark_complete_changes_status(self):
        """Verify that calling mark_complete() changes the task's completed status."""
        # Arrange
        task = Task(
            description="Morning walk",
            duration_minutes=30,
            frequency="daily",
            priority="high",
            completed=False
        )
        
        # Assert initial state is False
        assert task.completed is False
        
        # Act
        task.mark_complete()
        
        # Assert state is now True
        assert task.completed is True


class TestTaskAddition:
    """Test Task addition to Pet."""
    
    def test_adding_task_increases_pet_task_count(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        # Arrange
        pet = Pet(name="Mochi", species="dog", age=3)
        task1 = Task(
            description="Morning walk",
            duration_minutes=30,
            frequency="daily",
            priority="high"
        )
        task2 = Task(
            description="Feed breakfast",
            duration_minutes=10,
            frequency="daily",
            priority="medium"
        )
        
        # Assert initial task count is 0
        assert len(pet.tasks) == 0
        
        # Act - Add first task
        pet.add_task(task1)
        
        # Assert task count increased to 1
        assert len(pet.tasks) == 1
        
        # Act - Add second task
        pet.add_task(task2)
        
        # Assert task count increased to 2
        assert len(pet.tasks) == 2


class TestScheduling:
    """Additional tests for scheduling logic (bonus)."""
    
    def test_scheduler_respects_available_time(self):
        """Verify that scheduler respects owner's available time constraint."""
        # Arrange
        owner = Owner(name="Jordan", available_time_minutes=50)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        
        # Create tasks that exceed available time
        task1 = Task(
            description="Morning walk",
            duration_minutes=30,
            frequency="daily",
            priority="high"
        )
        task2 = Task(
            description="Playtime",
            duration_minutes=30,
            frequency="daily",
            priority="low"
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act
        scheduler = Scheduler(owner)
        plan = scheduler.get_daily_plan()
        
        # Assert only high priority task fits within available time
        assert len(plan) == 1
        assert plan[0].description == "Morning walk"
    
    def test_scheduler_sorts_by_priority(self):
        """Verify that scheduler sorts tasks by priority (high first)."""
        # Arrange
        owner = Owner(name="Jordan", available_time_minutes=100)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        
        # Create tasks with different priorities (add in mixed order)
        task_low = Task(
            description="Playtime",
            duration_minutes=20,
            frequency="daily",
            priority="low"
        )
        task_high = Task(
            description="Morning walk",
            duration_minutes=30,
            frequency="daily",
            priority="high"
        )
        task_medium = Task(
            description="Feed",
            duration_minutes=10,
            frequency="daily",
            priority="medium"
        )
        
        pet.add_task(task_low)
        pet.add_task(task_high)
        pet.add_task(task_medium)
        
        # Act
        scheduler = Scheduler(owner)
        plan = scheduler.get_daily_plan()
        
        # Assert tasks are ordered by priority: high, medium, low
        assert plan[0].priority == "high"
        assert plan[1].priority == "medium"
        assert plan[2].priority == "low"
