import streamlit as st
import pandas as pd
import datetime
import os
global workout_log
# Load the structured workout plan
def load_workout_plan():
    # Define the structured workout plan including muscle groups, exercises, and default reps/sets
    structured_workout_data = [
        ["Day 1: Chest & Back", "Barbell Bench Press", 4, 12, "90 sec"],
        ["Day 1: Chest & Back", "Pull Ups / Lat Pulldown", 5, 8, "90 sec"],
        ["Day 1: Chest & Back", "Incline Dumbbell Press", 4, 10, "90 sec"],
        ["Day 1: Chest & Back", "Bent-Over Row", 4, 10, "90 sec"],
        ["Day 1: Chest & Back", "Dumbbell Pullover", 4, 8, "90 sec"],
        ["Day 1: Chest & Back", "Dips", 4, 8, "90 sec"],
        ["Day 1: Chest & Back", "Seated Cable Row", 4, 8, "90 sec"],
        ["Day 2: Quad & Hamstrings", "Squat", 4, 12, "90 sec"],
        ["Day 2: Quad & Hamstrings", "Romanian Deadlift", 4, 10, "90 sec"],
        ["Day 2: Quad & Hamstrings", "Leg Extension", 4, 10, "90 sec"],
        ["Day 2: Quad & Hamstrings", "Leg Curls", 4, 10, "90 sec"],
        ["Day 2: Quad & Hamstrings", "Calf Raise", 6, 6, "90 sec"],
        ["Day 4: Deltoid & Arms", "Military Press (OHP)", 4, 12, "90 sec"],
        ["Day 4: Deltoid & Arms", "Side Lateral Raise", 4, 12, "90 sec"],
        ["Day 4: Deltoid & Arms", "Front Raise with Barbell", 4, 12, "90 sec"],
        ["Day 4: Deltoid & Arms", "Face Pulls", 4, 12, "90 sec"],
        ["Day 4: Deltoid & Arms", "Rear Delt Flys", 3, 12, "90 sec"],
        ["Day 4: Deltoid & Arms", "Barbell Curls", 4, 10, "90 sec"],
        ["Day 4: Deltoid & Arms", "Skull Crusher", 4, 10, "90 sec"],
        ["Day 5: Hamstrings & Quads", "Sumo Deadlift", 4, 12, "90 sec"],
        ["Day 5: Hamstrings & Quads", "Leg Curl", 5, 6, "90 sec"],
        ["Day 5: Hamstrings & Quads", "Front Squat", 4, 12, "90 sec"],
        ["Day 5: Hamstrings & Quads", "Romanian Deadlift", 4, 8, "90 sec"],
        ["Day 5: Hamstrings & Quads", "Leg Press", 4, 12, "90 sec"],
        ["Day 5: Hamstrings & Quads", "Hyperextensions", 3, 12, "90 sec"],
        ["Day 5: Hamstrings & Quads", "Calf Press in Leg Machine", 4, 15, "90 sec"],
        ["Day 6: Chest & Arms", "Dumbbell Bench Press", 4, 12, "90 sec"],
        ["Day 6: Chest & Arms", "Dumbbell Fly", 4, 10, "90 sec"],
        ["Day 6: Chest & Arms", "Side Lateral Raise", 3, 12, "90 sec"],
        ["Day 6: Chest & Arms", "Biceps Curls with EZ-Bar", 4, 10, "90 sec"],
        ["Day 6: Chest & Arms", "Triceps Cable Push Downs", 4, 10, "120 sec"]
    ]

    # Convert to DataFrame
    df_structured = pd.DataFrame(structured_workout_data, columns=["Muscle Group", "Exercise", "Sets", "Reps", "Rest Time"])

    # Define the correct weekly progressions for focus exercises
    corrected_focus_progression = {
        "Barbell Bench Press": [[4, 12], [4, 10], [4, 6], [4, 6], [5, 8], [5, 8], [5, 5], [5, 5], [6, 5], [6, 5], [6, 3], [6, 3]],
        "Squat": [[4, 12], [4, 10], [4, 6], [4, 6], [5, 12], [5, 8], [5, 5], [5, 5], [6, 5], [6, 5], [6, 3], [6, 3]],
        "Military Press (OHP)": [[4, 12], [4, 10], [4, 6], [4, 6], [5, 12], [5, 8], [5, 5], [5, 5], [6, 5], [6, 5], [6, 3], [6, 3]],
        "Sumo Deadlift": [[4, 12], [4, 10], [4, 6], [4, 6], [5, 12], [5, 8], [5, 5], [5, 5], [6, 5], [6, 5], [6, 3], [6, 3]],
        "Dumbbell Bench Press": [[4, 12], [4, 10], [4, 6], [4, 6], [5, 8], [5, 8], [5, 5], [5, 5], [5, 5], [5, 5], [5, 5], [5, 5]]
    }

    # Generate the 12-week plan including dynamic focus exercise progression
    workout_data = []
    for week in range(1, 13):
        for _, row in df_structured.iterrows():
            exercise = row["Exercise"]
            if exercise in corrected_focus_progression:
                sets, reps = corrected_focus_progression[exercise][week - 1]  # Adjust for focus exercises
            else:
                sets, reps = row["Sets"], row["Reps"]  # Keep default for non-focus exercises

            workout_data.append([row["Muscle Group"], exercise, sets, reps, row["Rest Time"], f"Week {week}", "", "", ""])

    # Convert the structured data into a DataFrame
    df_final = pd.DataFrame(workout_data, columns=["Muscle Group", "Exercise", "Sets", "Reps", "Rest Time", "Week", "ORM", "Reality Sets/Reps", "Notes"])

    return df_final

log_file = "workout_log.csv"
if os.path.exists(log_file):
    workout_log = pd.read_csv(log_file)
else:
    workout_log = pd.DataFrame(columns=["Date", "Week", "Muscle Group", "Exercise", "Completed"])

def save_workout_log():
    workout_log.to_csv(log_file, index=False)

st.title("12-Week Workout Tracker")

# Load workout data
df_workout = load_workout_plan()

# Identify completed weeks
completed_weeks = workout_log.groupby("Week")["Muscle Group"].nunique()
full_weeks = completed_weeks[completed_weeks == df_workout["Muscle Group"].nunique()].index

# Select available weeks
available_weeks = [w for w in df_workout["Week"].unique() if w not in full_weeks]
selected_week = st.selectbox("Select Week", available_weeks)

# Identify completed muscle groups for the selected week
logged_muscle_groups = workout_log.loc[workout_log["Week"] == selected_week, "Muscle Group"].unique()
muscle_groups = df_workout["Muscle Group"].unique()
logged_exercises_in_week = workout_log.loc[workout_log["Week"] == selected_week, "Exercise"].unique()
full_muscle_groups = [mg for mg in muscle_groups if all(ex in logged_exercises_in_week for ex in df_workout[df_workout["Muscle Group"] == mg]["Exercise"].unique())]
available_muscle_groups = [mg for mg in muscle_groups if mg not in full_muscle_groups]
selected_muscle_group = st.selectbox("Select Muscle Group", available_muscle_groups)

# Identify completed exercises
logged_exercises = workout_log.loc[(workout_log["Week"] == selected_week) & (workout_log["Muscle Group"] == selected_muscle_group), "Exercise"].unique()
df_week = df_workout[(df_workout["Week"] == selected_week) & (df_workout["Muscle Group"] == selected_muscle_group)]
unlogged_exercises = [ex for ex in df_week["Exercise"].unique() if ex not in logged_exercises]

if unlogged_exercises:
    selected_exercise = st.selectbox("Select Exercise", unlogged_exercises)
    exercise_details = df_week[df_week["Exercise"] == selected_exercise].iloc[0]
    st.write(f"**Target Sets:** {exercise_details['Sets']}, **Target Reps:** {exercise_details['Reps']}, **Rest Time:** {exercise_details['Rest Time']}")
    workout_date = st.date_input("Workout Date", datetime.date.today())
    completed_sets = st.number_input("Completed Sets", min_value=0, max_value=10, step=1,  value=0)
    completed_reps = st.text_input("Completed Reps (e.g., 10,10,8,6)")
    orm = st.number_input("One Rep Max (ORM)", min_value=0, step=1, value=0)
    notes = st.text_area("Notes")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if st.button("Log Workout", key="log_workout"):
        new_entry = pd.DataFrame({
            "Date": [workout_date],
            "Week": [selected_week],
            "Muscle Group": [selected_muscle_group],
            "Exercise": [selected_exercise],
            "Completed Sets": [completed_sets],
            "Completed Reps": [completed_reps],
            "Completed": [True if completed_sets > 0 else False],
            "ORM": [orm],
            "Notes": [notes],
            "Timestamp": [timestamp],
            "Target Sets": [exercise_details["Sets"]],
            "Target Reps": [exercise_details["Reps"]]
        })
        
        workout_log = pd.concat([workout_log, new_entry], ignore_index=True)
        save_workout_log()
        st.success("Workout logged successfully!")
        
        # Update the unlogged exercises list
        logged_exercises = workout_log.loc[(workout_log["Week"] == selected_week) & (workout_log["Muscle Group"] == selected_muscle_group), "Exercise"].unique()
        unlogged_exercises = [ex for ex in df_week["Exercise"].unique() if ex not in logged_exercises]
        if len(unlogged_exercises) > 0:
            
            selected_exercise = unlogged_exercises[0]
            st.rerun()
        else:
            st.success("You have completed all exercises for this muscle group today!")
    
    # If all exercises of the muscle group are done, mark it as finished
    remaining_exercises = df_week["Exercise"].unique()
    if all(ex in logged_exercises for ex in remaining_exercises):
        st.success("You finished your workout day!")
        st.balloons()
        
else:
    st.success("You have completed all exercises for this muscle group!")
    # Show the summary of the completed exercises
st.subheader("Today Exercises")
completed_exercises = workout_log.loc[(workout_log["Week"] == selected_week) & (workout_log["Muscle Group"] == selected_muscle_group)]
if completed_exercises.empty:
    st.write("No exercises logged yet.")
else:
    st.dataframe(completed_exercises[["Exercise", "Completed Sets", "Completed Reps", "ORM", "Notes", "Completed"]])


if st.button("Show Completed Days in Week"):
    completed_days = workout_log.loc[(workout_log["Week"] == selected_week) & (workout_log["Muscle Group"].isin(full_muscle_groups))][["Muscle Group", "Exercise", "Completed Sets", "Completed Reps", "ORM", "Notes", "Completed"]]
    st.dataframe(completed_days)
# st.subheader("Workout History")
# st.dataframe(workout_log)
