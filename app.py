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

    if st.button("Add Task"):
        pet = next(p for p in owner.pets if p.name == selected_pet)
        new_task = Task(description=task_description, duration_minutes=duration, frequency=frequency, priority=priority)
        pet.add_task(new_task)
        st.success(f"Added task to {pet.name}: {new_task.description}")
else:
    st.info("Add a pet first to add tasks.")

st.divider()

st.subheader("Current Tasks")
all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("All Tasks:")
    for task in all_tasks:
        status = "✅ Completed" if task.completed else "⏳ Pending"
        st.write(f"- {task.description} ({task.duration_minutes} min, {task.priority}, {task.frequency}) - {status}")
else:
    st.info("No tasks added yet.")

st.divider()

st.subheader("Generate Daily Schedule")
if st.button("Generate Schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.get_daily_plan()
    explanation = scheduler.explain_plan(plan)
    st.write("### Today's Schedule")
    st.code(explanation)
