from paypal_system import Owner, Pet, Task, Scheduler

# Create an Owner
owner = Owner(name="Jordan", available_time_minutes=120)  # 2 hours

# Create Pets
pet1 = Pet(name="Mochi", species="dog", age=3)
pet2 = Pet(name="Whiskers", species="cat", age=2)

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create Tasks with times (out of order)
task1 = Task(description="Morning walk", duration_minutes=30, frequency="daily", priority="high", start_time="08:00")
task2 = Task(description="Feed breakfast", duration_minutes=10, frequency="daily", priority="medium", start_time="07:00")
task3 = Task(description="Playtime", duration_minutes=20, frequency="daily", priority="low", start_time="10:00")
task4 = Task(description="Evening grooming", duration_minutes=15, frequency="daily", priority="medium", start_time="08:00")  # Conflict with walk

# Add tasks to pets
pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)
pet2.add_task(task4)

# Create Scheduler
scheduler = Scheduler(owner)

# Test sorting by time
all_tasks = owner.get_all_tasks()
sorted_tasks = scheduler.sort_tasks_by_time(all_tasks)
print("Tasks sorted by time:")
for task in sorted_tasks:
    print(f"- {task.description} at {task.start_time}")

# Test filtering by status
pending_tasks = scheduler.filter_tasks_by_status(all_tasks, completed=False)
print(f"\nPending tasks: {len(pending_tasks)}")

# Test filtering by pet
mochi_tasks = owner.filter_tasks_by_pet("Mochi")
print(f"Mochi's tasks: {[t.description for t in mochi_tasks]}")

# Test conflict detection
conflicts = scheduler.detect_conflicts(all_tasks)
if conflicts:
    print("\nConflicts detected:")
    for warning in conflicts:
        print(f"- {warning}")
else:
    print("\nNo conflicts detected.")

# Get daily plan
plan = scheduler.get_daily_plan()

# Print Today's Schedule
print("\nToday's Schedule:")
if plan:
    for task in plan:
        print(f"- {task.description} ({task.duration_minutes} min, priority: {task.priority})")
    total_time = sum(t.duration_minutes for t in plan)
    print(f"Total time: {total_time} min out of {owner.available_time_minutes} min available.")
else:
    print("No tasks scheduled.")

# Test recurring: mark a task complete
task2.mark_complete()
print(f"\nAfter marking '{task2.description}' complete, it is still due today: {task2.is_due_today()}")