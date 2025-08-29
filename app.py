import streamlit as st
import pandas as pd

# Load results
result_df = pd.read_csv("result.csv")

# Make sure UniqueID is string for comparison
result_df["UniqueID"] = result_df["UniqueID"].astype(str)

# Add AllotmentStatus column if not already present
if "AllotmentStatus" not in result_df.columns:
    result_df["AllotmentStatus"] = result_df["CollegeID"].apply(
        lambda x: "Allotted" if x != "No College Available" else "Not Allotted"
    )

# Custom CSS for better visibility
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #2E86C1;
        margin-bottom: 30px;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        border-left: 8px solid #28a745;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        border-left: 8px solid #dc3545;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        border-left: 8px solid #ffc107;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown('<div class="title">🎓 College Allotment Validation Portal</div>', unsafe_allow_html=True)

# Input
uid = st.text_input("🔑 Enter your UniqueID:")

if st.button("🔍 Validate Allotment"):
    uid = uid.strip()  # remove spaces
    student = result_df[result_df["UniqueID"] == uid]

    if student.empty:
        st.markdown('<div class="error-box">❌ Student ID not found.</div>', unsafe_allow_html=True)

    elif student.iloc[0]["AllotmentStatus"] == "Allotted":
        st.markdown(
            f"""
            <div class="success-box">
                ✅ Congratulations <b>{student.iloc[0]['Name']}</b>!<br><br>
                You are allotted <b>{student.iloc[0]['Institution']}</b><br>
                (Preference: {int(student.iloc[0]['PrefNumber'])})
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.markdown('<div class="warning-box">⚠️ Sorry, you have not been allotted any college try in next Phase .</div>', unsafe_allow_html=True)
