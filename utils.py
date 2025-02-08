import pandas as pd
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
    df_structured = pd.DataFrame(structured_workout_data, columns=["Day Of Week", "Exercise", "Sets", "Reps", "Rest Time"])

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

            workout_data.append([row["Day Of Week"], exercise, sets, reps, row["Rest Time"], f"Week {week}", "", "", ""])

    # Convert the structured data into a DataFrame
    df_final = pd.DataFrame(workout_data, columns=["Day Of Week", "Exercise", "Sets", "Reps", "Rest Time", "Week", "ORM", "Reality Sets/Reps", "Notes"])
    # df_final.to_csv("workout_plan.csv", index=False)
    return df_final
