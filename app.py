import streamlit as st
import pandas as pd
import datetime
import os
import matplotlib.pyplot as plt
import re
from io import BytesIO
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from google.oauth2.service_account import Credentials
import threading

# Google Drive API setup using Streamlit Secrets
SCOPES = ['https://www.googleapis.com/auth/drive.file']
FILE_NAME = 'workout_log2.csv'

# Load credentials from Streamlit secrets
SERVICE_ACCOUNT_INFO = st.secrets["gcp_service_account"]
global workout_log
# Load the structured workout plan
def format_df_history(df):
    try:
        df['Set'] = df.apply(lambda x: str(x['Sets'])+"/"+str(x["Target Sets"]), axis=1)                                      
        df['Rep'] = df.apply(lambda x: str(x['Reps'])+"/"+str(x["Target Reps"]), axis=1)
        df = df[['Week', 'ORM',  'Set', 'Rep', 'Weights','Completed','Date', 'Notes']]
    except:
        pass
    return df

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

    return df_final

# Authenticate and create Drive service
def authenticate_google_drive():
    creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def get_file_id(service, filename):
    results = service.files().list(q=f"name='{filename}'", fields="files(id, name)").execute()
    items = results.get('files', [])
    return items[0]['id'] if items else None

def load_workout_log(service):
    file_id = get_file_id(service, FILE_NAME)
    if file_id:
        request = service.files().get_media(fileId=file_id)
        fh = BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.seek(0)
        return pd.read_csv(fh)
    else:
        return pd.DataFrame(columns=["Date", "Week", "Day Of Week", "Exercise", "Completed", "Sets", "Reps", "Weights", "ORM", "Notes", "Timestamp", "Target Sets", "Target Reps"])

def save_workout_log(service, df, to_drive=True):
    df.to_csv(FILE_NAME, index=False)
    file_id = get_file_id(service, FILE_NAME)
    if to_drive:
        def upload_to_drive():
            media = MediaFileUpload(FILE_NAME, mimetype='text/csv')
            if file_id:
                service.files().update(fileId=file_id, media_body=media).execute()
            else:
                file_metadata = {'name': FILE_NAME}
                service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        threading.Thread(target=upload_to_drive).start()


# Authenticate and load data
service = authenticate_google_drive()
if st.button("Reload Workout Log From Drive"):
    workout_log = load_workout_log(service)
    st.success("Reloaded workout log from Google Drive successfully!")
    st.rerun()
if not os.path.exists(FILE_NAME):
    workout_log = load_workout_log(service)
    workout_log.to_csv(FILE_NAME, index=False)
else:
    workout_log = pd.read_csv(FILE_NAME)


st.title("12-Week Workout Tracker")

# Load workout data
df_workout = load_workout_plan()

# Identify completion status for days
completed_days_per_week = workout_log.groupby("Week")["Day Of Week"].nunique()

# Identify all days per week
total_days_per_week = df_workout.groupby("Week")["Day Of Week"].nunique()
# Identify completed weeks where all exercises are done
completed_weeks = []
for week in total_days_per_week.index:
    days_of_week = df_workout[df_workout["Week"] == week]["Day Of Week"].unique()
    all_exercises_done = all(
        set(df_workout[(df_workout["Week"] == week) & (df_workout["Day Of Week"] == day)]["Exercise"].unique()) ==
        set(workout_log[(workout_log["Week"] == week) & (workout_log["Day Of Week"] == day)]["Exercise"].unique())
        for day in days_of_week
    )
    if all_exercises_done:
        completed_weeks.append(week)

# Generate week options
all_weeks = df_workout["Week"].unique()
week_options = [
    f"{week} ✅" if week in completed_weeks else week 
    for week in all_weeks
]

# Auto-select first incomplete week
default_week = next((week for week in all_weeks if week not in completed_weeks), all_weeks[0])
selected_week = st.selectbox("Select Week", week_options, index=list(all_weeks).index(default_week))
selected_week = selected_week.replace(" ✅", "").replace(" ❌", "")
# Identify completed days for the selected week
days_of_week = df_workout[df_workout["Week"] == selected_week]["Day Of Week"].unique()
logged_days = []

for day in days_of_week:
    exercises = df_workout[(df_workout["Week"] == selected_week) & (df_workout["Day Of Week"] == day)]["Exercise"].unique()
    logged_exercises = workout_log.loc[(workout_log["Week"] == selected_week) & (workout_log["Day Of Week"] == day), "Exercise"].unique()
    if set(exercises) == set(logged_exercises):
        logged_days.append(day)

# Mark days as 'Done'
day_options = [
    f"{day} ✅" if day in logged_days else day 
    for day in days_of_week
]

default_day = next((day for day in days_of_week if day not in logged_days), days_of_week[0])
selected_day = st.selectbox("Select Day Of Week", day_options, index=list(days_of_week).index(default_day))
selected_day = selected_day.replace(" ✅", "").replace(" ❌", "")
# Select Exercise
exercises = df_workout[(df_workout["Week"] == selected_week) & (df_workout["Day Of Week"] == selected_day)]["Exercise"].unique()
logged_exercises = workout_log.loc[(workout_log["Week"] == selected_week) & (workout_log["Day Of Week"] == selected_day), "Exercise"].unique()
logged_exercises_df = workout_log.loc[(workout_log["Week"] == selected_week) & (workout_log["Day Of Week"] == selected_day)]
exercise_options = [
    # f"{ex} ✅" if ex in logged_exercises else ex 
    # for ex in exercises
]
for ex in exercises:
    if ex in logged_exercises_df["Exercise"].values:
        ex_df = logged_exercises_df[logged_exercises_df["Exercise"] == ex]
        completed = ex_df["Completed"].values[0]
        if completed:
            exercise_options.append(f"{ex} ✅")
        else:
            exercise_options.append(f"{ex} ❌")
    else:
        exercise_options.append(ex)

# Auto-select first incomplete exercise
default_exercise = next((ex for ex in exercises if ex not in logged_exercises), exercises[0])
selected_exercise = st.selectbox("Select Exercise", exercise_options, index=list(exercises).index(default_exercise))
selected_exercise = selected_exercise.replace(" ✅", "").replace(" ❌", "")

is_completed = selected_exercise in logged_exercises

# If all exercises are done, show summary
# if len(logged_exercises) == len(exercises):
#     # st.success(f"All exercises for {selected_day} are completed!")
#     st.write("Summary:")
#     st.dataframe(workout_log[(workout_log["Week"] == selected_week) & (workout_log["Day Of Week"] == selected_day)])

if not is_completed:
    df_week = df_workout[(df_workout["Week"] == selected_week) & (df_workout["Day Of Week"] == selected_day)]
    st.write(f"**Selected Exercise:** {selected_exercise}")
    exercise_details = df_week[df_week["Exercise"] == selected_exercise].iloc[0]
    st.write(f"**Target Sets:** {exercise_details['Sets']}, **Target Reps:** {exercise_details['Reps']}, **Rest Time:** {exercise_details['Rest Time']}")
    # Add a link to search for the selected exercise on Google
    query = selected_exercise + " body building guide"
    search_query = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    st.markdown(f"[Search for {selected_exercise} on Google]({search_query})")
    # Exercise History
    st.subheader("Exercise History")
    df_exercise_history = workout_log[workout_log["Exercise"] == selected_exercise]
    df_exercise_history = format_df_history(df_exercise_history)
    st.dataframe(df_exercise_history)
    last_orm = df_exercise_history['ORM'].iloc[-1] if not df_exercise_history.empty else 0
    
    workout_date = st.date_input("Workout Date", datetime.date.today())
    # completed_sets = st.number_input("Sets - Target: " + str(exercise_details['Sets']), min_value=0, step=1)
    weights = st.text_input("Weights (comma separated) - Last ORM: " + str(last_orm))
    reps = st.text_input("Reps (comma separated) - Target: " + str(exercise_details['Reps']) + " Reps x " + str(exercise_details['Sets']) + " Sets, Finished by default.")
    # Clean the reps and weights text, keep only float numbers and commas
    completed_reps = [float(x) for x in re.findall(r'\d+\.?\d*', reps)]
    auto_input_rep = False
    if not completed_reps:
        completed_reps = [int(exercise_details['Reps'])] * exercise_details['Sets']
        reps = ",".join([str(x) for x in completed_reps])
        auto_input_rep = True
    completed_weights = [float(x) for x in re.findall(r'\d+\.?\d*', weights)]
    notes = st.text_area("Notes")
    completed_sets = 0
    # Clean the reps and weights text, keep only float numbers and commas
    if completed_weights:
        max_weight = max(completed_weights)
        completed_sets = len(completed_reps)
        if not auto_input_rep:
            st.write(f"Completed Sets: {completed_sets}/{exercise_details['Sets']}")
        orm = max_weight
        # max_reps = completed_reps[completed_weights.index(max_weight)]
        # if max_reps > 1:
        #     orm = max_weight
        # else:
        #     orm = round(max_weight * (1 + max_reps / 30), 2)
    else:
        orm = 0

    st.write(f"Calculated One Rep Max (ORM): {orm}")
    # orm = st.number_input("One Rep Max (ORM)", min_value=0.0, step=0.1)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("Log Exercise", disabled=is_completed):
        new_entry = pd.DataFrame({
            "Date": [workout_date],
            "Week": [selected_week],
            "Day Of Week": [selected_day],
            "Exercise": [selected_exercise],
            "Sets": [completed_sets],
            "Reps": [reps],
            "Weights": [weights],
            "Completed": [True if completed_sets > 0 else False],
            "ORM": [orm],
            "Notes": [notes],
            "Timestamp": [timestamp],
            "Target Sets": [df_workout.loc[df_workout["Exercise"] == selected_exercise, "Sets"].values[0]],
            "Target Reps": [df_workout.loc[df_workout["Exercise"] == selected_exercise, "Reps"].values[0]]
        })
        workout_log = pd.concat([workout_log, new_entry], ignore_index=True)
        save_workout_log(service, workout_log)
        st.success(f"Logged {selected_exercise} successfully!")
        st.rerun()

elif is_completed:
    # Find in logged exercises that if selected_exercise is completed
    selected_exercise_data = workout_log[(workout_log["Week"] == selected_week) & (workout_log["Day Of Week"] == selected_day) & (workout_log["Exercise"] == selected_exercise)]
    
    if not selected_exercise_data.empty:
        if selected_exercise_data["Completed"].values[0]:
            st.success(f"You have completed {selected_exercise} for {selected_day}!")
        else:
            st.warning(f"You have skipped {selected_exercise} for {selected_day}!")
    else:
        pass
    st.subheader(f"{selected_week} - {selected_day}'s Workout")
    completed_wordkout_df = workout_log[(workout_log["Week"] == selected_week) & (workout_log["Day Of Week"] == selected_day)]
    st.dataframe(completed_wordkout_df[[ "Exercise",'ORM', 'Sets', 'Reps', 'Weights','Completed','Date', 'Notes']])
    st.subheader(f"{selected_exercise} History")
    df_exercise_history = workout_log[workout_log["Exercise"] == selected_exercise]
    df_exercise_history = format_df_history(df_exercise_history)
    st.dataframe(df_exercise_history)
    st.subheader(f"{selected_exercise} ORM Chart")
    plt.figure(figsize=(12, 6))
    plt.plot(df_exercise_history["Week"], df_exercise_history["ORM"], marker='o')
    plt.xlabel("Week")
    plt.ylabel("One Rep Max (ORM)")
    plt.title(f"{selected_exercise} One Rep Max (ORM) Progression")
    plt.xticks(rotation=45)
    st.pyplot(plt)
    
if st.button(f"Show {selected_week} Summary"):
    st.subheader(f"{selected_week} Summary")
    st.dataframe(workout_log[workout_log["Week"] == selected_week][["Exercise",'ORM', 'Sets', 'Reps', 'Weights','Completed','Date', 'Notes', 'Day Of Week']])


