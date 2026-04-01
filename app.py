import streamlit as st
from paypal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Step 2: Manage Application Memory with st.session_state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time_minutes=120)

owner = st.session_state.owner

st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value=owner.name)
available_time = st.number_input("Available time (minutes)", min_value=1, max_value=480, value=owner.available_time_minutes)

if st.button("Update Owner"):
    owner.name = owner_name
    owner.available_time_minutes = available_time
    st.success("Owner updated!")

st.write(f"Current Owner: {owner.name} (Available time: {owner.available_time_minutes} min)")

st.divider()

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi", key="pet_name")
species = st.selectbox("Species", ["dog", "cat", "other"], key="species")
age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, species=species, age=age)
    owner.add_pet(new_pet)
    st.success(f"Added pet: {new_pet.name}")

if owner.pets:
    st.write("Current Pets:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species}, {pet.age} years old)")
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")
if owner.pets:
    selected_pet = st.selectbox("Select Pet", [pet.name for pet in owner.pets])
    task_description = st.text_input("Task description", value="Morning walk")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    frequency = st.selectbox("Frequency", ["daily", "weekly"], index=0)
    start_time = st.text_input("Start time (HH:MM)", value="08:00")

    if st.button("Add Task"):
        pet = next(p for p in owner.pets if p.name == selected_pet)
        new_task = Task(description=task_description, duration_minutes=duration, frequency=frequency, priority=priority, start_time=start_time)
        pet.add_task(new_task)
        st.success(f"Added task '{new_task.description}' to {pet.name} at {start_time}")
else:
    st.info("Add a pet first to add tasks.")

st.divider()

st.subheader("Current Tasks")
all_tasks = owner.get_all_tasks()
if all_tasks:
    # Display sorted by time
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_tasks_by_time(all_tasks)
    
    # Prepare data for table
    task_data = []
    for task in sorted_tasks:
        status = "✅ Completed" if task.completed else "⏳ Pending"
        task_data.append({
            "Pet": next((p.name for p in owner.pets if task in p.tasks), "Unknown"),
            "Description": task.description,
            "Time": task.start_time or "No time",
            "Duration": f"{task.duration_minutes} min",
            "Priority": task.priority,
            "Status": status
        })
    st.table(task_data)
    
    # Conflict detection
    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        st.warning("⚠️ Conflicts Detected:")
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("✅ No conflicts detected.")
else:
    st.info("No tasks added yet.")

st.divider()

st.subheader("Filter Tasks")
if all_tasks:
    col1, col2 = st.columns(2)
    with col1:
        filter_pet = st.selectbox("Filter by Pet", ["All"] + [pet.name for pet in owner.pets])
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
    
    filtered_tasks = all_tasks
    if filter_pet != "All":
        filtered_tasks = owner.filter_tasks_by_pet(filter_pet)
    if filter_status != "All":
        completed = filter_status == "Completed"
        filtered_tasks = scheduler.filter_tasks_by_status(filtered_tasks, completed)
    
    if filtered_tasks:
        st.write(f"Showing {len(filtered_tasks)} task(s):")
        for task in filtered_tasks:
            st.write(f"- {task.description} ({task.start_time or 'No time'}, {task.priority})")
    else:
        st.info("No tasks match the filters.")

st.divider()

st.subheader("Generate Daily Schedule")
if st.button("Generate Schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.get_daily_plan()
    explanation = scheduler.explain_plan(plan)
    st.write("### Today's Schedule")
    st.code(explanation)
    
    # Show plan in table
    if plan:
        plan_data = []
        for task in plan:
            plan_data.append({
                "Task": task.description,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority,
                "Time": task.start_time or "TBD"
            })
        st.table(plan_data)
