# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

PawPal+ includes intelligent algorithms to make pet care planning efficient and user-friendly:

- **Priority-Based Scheduling**: Tasks are sorted by priority (high → medium → low) and fitted into the owner's available time, ensuring critical care tasks are prioritized.
- **Time Sorting**: Tasks can be sorted by start time (HH:MM format) for chronological viewing, using Python's `sorted()` with lambda keys for efficient string parsing.
- **Conflict Detection**: Lightweight algorithm checks for exact time overlaps between tasks, issuing warnings (e.g., "Conflict: Morning walk and Evening grooming overlap") without crashing the app.
- **Task Filtering**: Filter tasks by completion status (pending/completed) or by specific pet, enabling focused views for multi-pet households.
- **Daily Recurrence**: Supports recurring tasks (daily/weekly); marking a task complete prepares it for the next occurrence (simplified for demo).
- **Plan Explanation**: Generates human-readable explanations for daily plans, including total time used and remaining availability.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

Run the test suite to verify core functionalities:

```bash
python -m pytest
```

Tests cover task completion, task addition, scheduling constraints, and priority sorting.
```

The tests cover:
- Task completion and status changes
- Adding tasks to pets and tracking counts
- Scheduling logic including time constraints and priority-based sorting
- Sorting tasks in chronological order by start time
- Recurrence logic for daily tasks (creating new tasks upon completion)
- Conflict detection for overlapping or simultaneous tasks

**Confidence Level**: ⭐⭐⭐⭐⭐ (5/5 stars) - All tests pass with comprehensive coverage of key scheduling, sorting, and task management behaviors.
