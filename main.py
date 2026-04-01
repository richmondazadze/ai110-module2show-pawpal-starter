from paypal_system import Owner, Pet, Task, Scheduler

# Create an Owner
owner = Owner(name="Jordan", available_time_minutes=120)  # 2 hours

# Create Pets
pet1 = Pet(name="Mochi", species="dog", age=3)
pet2 = Pet(name="Whiskers", species="cat", age=2)

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create Tasks
task1 = Task(description="Morning walk", duration_minutes=30, frequency="daily", priority="high")
task2 = Task(description="Feed breakfast", duration_minutes=10, frequency="daily", priority="medium")
task3 = Task(description="Playtime", duration_minutes=20, frequency="daily", priority="low")
task4 = Task(description="Evening grooming", duration_minutes=15, frequency="daily", priority="medium")

# Add tasks to pets
pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)
pet2.add_task(task4)

# Create Scheduler
scheduler = Scheduler(owner)

# Get daily plan
plan = scheduler.get_daily_plan()

# Print Today's Schedule
print("Today's Schedule:")
if plan:
    for task in plan:
        print(f"- {task.description} ({task.duration_minutes} min, priority: {task.priority})")
    total_time = sum(t.duration_minutes for t in plan)
    print(f"Total time: {total_time} min out of {owner.available_time_minutes} min available.")
else:
    print("No tasks scheduled.")