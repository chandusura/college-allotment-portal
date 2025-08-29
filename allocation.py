import pandas as pd

# ------------------------
# Load Data
# ------------------------
students = pd.read_csv("data/students.csv")  
# Columns: UniqueID, Name, Gender, Caste, Rank

preferences = pd.read_csv("data/preference.csv")  
# Columns: CollegeID, PrefNumber, UniqueID

seats = pd.read_csv("data/seat.csv")  
# Columns: CollegeID, Institution, Total Seats, Total Admitted, Orphan Quota, PHC Quota, SC, SC-CC, ST, BC, Minority, OC

# ------------------------
# Admission Simulation
# ------------------------
# Sort students by Rank (ascending → best rank first)
students = students.sort_values(by="Rank")

# Create seat availability dictionary
seat_availability = {}
for _, row in seats.iterrows():
    seat_availability[row["CollegeID"]] = {
        "SC": row["SC"],
        "SC-CC": row["SC-CC"],
        "ST": row["ST"],
        "BC": row["BC"],
        "Minority": row["Minority"],
        "OC": row["OC"]
    }

results = []

# Process each student
for _, student in students.iterrows():
    uid = student["UniqueID"]
    caste = student["Caste"]
    gender = student["Gender"]
    name = student["Name"]
    rank = student["Rank"]

    # Get student’s preferences sorted by PrefNumber
    student_prefs = preferences[preferences["UniqueID"] == uid].sort_values(by="PrefNumber")

    allotted_college = None
    used_pref = None

    for _, pref in student_prefs.iterrows():
        college_id = pref["CollegeID"]
        pref_no = int(pref["PrefNumber"])  # ensure integer

        if college_id in seat_availability and caste in seat_availability[college_id]:
            if seat_availability[college_id][caste] > 0:
                # Allot seat
                seat_availability[college_id][caste] -= 1
                allotted_college = college_id
                used_pref = pref_no
                break

    if allotted_college:
        institution = seats.loc[seats["CollegeID"] == allotted_college, "Institution"].values[0]
        results.append([uid, name, gender, caste, rank, allotted_college, institution, used_pref])
    else:
        results.append([uid, name, gender, caste, rank, "No College Available", "N/A", None])

# ------------------------
# Save Results
# ------------------------
result_df = pd.DataFrame(
    results,
    columns=["UniqueID", "Name", "Gender", "Caste", "Rank", "CollegeID", "Institution", "PrefNumber"]
)
result_df["PrefNumber"] = result_df["PrefNumber"].astype("Int64")  # keeps NaN as <NA>
result_df.to_csv("result.csv", index=False)

print("✅ Admission process completed. Results saved to result.csv")
