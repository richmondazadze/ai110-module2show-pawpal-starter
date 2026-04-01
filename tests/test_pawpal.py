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


class TestSortingCorrectness:
    """Test that tasks are sorted correctly."""
    
    def test_sort_tasks_by_time_chronological(self):
        """Verify tasks are sorted in chronological order by start_time."""
        # Arrange
        task1 = Task(description="Task1", duration_minutes=10, frequency="daily", priority="high", start_time="09:00")
        task2 = Task(description="Task2", duration_minutes=10, frequency="daily", priority="high", start_time="08:00")
        task3 = Task(description="Task3", duration_minutes=10, frequency="daily", priority="high", start_time=None)
        tasks = [task1, task2, task3]
        owner = Owner(name="Test", available_time_minutes=100)
        scheduler = Scheduler(owner)
        
        # Act
        sorted_tasks = scheduler.sort_tasks_by_time(tasks)
        
        # Assert
        assert sorted_tasks[0].description == "Task2"  # 08:00 first
        assert sorted_tasks[1].description == "Task1"  # 09:00 second
        assert sorted_tasks[2].description == "Task3"  # None last (23:59)


class TestRecurrenceLogic:
    """Test recurrence logic for tasks."""
    
    def test_marking_daily_task_complete_creates_new_task(self):
        """Verify that marking a daily task complete creates a new task for the following day."""
        # Arrange
        pet = Pet(name="Mochi", species="dog", age=3)
        task = Task(description="Morning walk", duration_minutes=30, frequency="daily", priority="high", start_time="08:00")
        pet.add_task(task)
        initial_task_count = len(pet.tasks)
        
        # Act
        pet.mark_task_complete(task)
        
        # Assert
        assert task.completed == True
        assert len(pet.tasks) == initial_task_count + 1
        new_task = pet.tasks[-1]
        assert new_task.description == task.description
        assert new_task.frequency == task.frequency
        assert new_task.completed == False


class TestConflictDetection:
    """Test conflict detection in scheduler."""
    
    def test_scheduler_flags_overlapping_tasks(self):
        """Verify that scheduler flags overlapping tasks."""
        # Arrange
        owner = Owner(name="Test", available_time_minutes=100)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        task1 = Task(description="Task1", duration_minutes=30, frequency="daily", priority="high", start_time="08:00")
        task2 = Task(description="Task2", duration_minutes=30, frequency="daily", priority="high", start_time="08:15")  # overlaps
        pet.add_task(task1)
        pet.add_task(task2)
        scheduler = Scheduler(owner)
        
        # Act
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # Assert
        assert len(conflicts) == 1
        assert "overlap" in conflicts[0]
    
    def test_scheduler_flags_same_start_time(self):
        """Verify that scheduler flags tasks with the same start time."""
        # Arrange
        owner = Owner(name="Test", available_time_minutes=100)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        task1 = Task(description="Task1", duration_minutes=30, frequency="daily", priority="high", start_time="08:00")
        task2 = Task(description="Task2", duration_minutes=30, frequency="daily", priority="high", start_time="08:00")  # same time
        pet.add_task(task1)
        pet.add_task(task2)
        scheduler = Scheduler(owner)
        
        # Act
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # Assert
        assert len(conflicts) == 1
        assert "overlap" in conflicts[0]
    
    def test_scheduler_no_conflict_for_non_overlapping(self):
        """Verify no conflict for non-overlapping tasks."""
        # Arrange
        owner = Owner(name="Test", available_time_minutes=100)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        task1 = Task(description="Task1", duration_minutes=30, frequency="daily", priority="high", start_time="08:00")
        task2 = Task(description="Task2", duration_minutes=30, frequency="daily", priority="high", start_time="09:00")  # no overlap
        pet.add_task(task1)
        pet.add_task(task2)
        scheduler = Scheduler(owner)
        
        # Act
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # Assert
        assert len(conflicts) == 0
