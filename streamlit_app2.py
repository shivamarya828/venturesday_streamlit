# streamlit_app.py
import streamlit as st
import sqlite3
import pandas as pd

# Initialize SQLite database
conn = sqlite3.connect("feedback2.db")
cursor = conn.cursor()

# # Drop the table if it exists
# cursor.execute("DROP TABLE IF EXISTS feedback2")

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    company TEXT,
    relevance TEXT,
    innovation TEXT,
    maturity TEXT,
    presentation TEXT,
    follow_up TEXT,
    comments TEXT
)
""")
conn.commit()

# App title
st.title("COE Ventures Day – Leader Evaluation Form")
st.write("Please complete this form after each session to help us evaluate the featured ventures and improve future events.")

# Question: Attended Sessions
attended_sessions = st.multiselect(
    "Which all companies' sessions did you attend?",
    ["RegScale", "With Accend", "Tellius"]
)

if attended_sessions:
    # Feedback form for each selected company
    with st.form("feedback_form"):
        name = st.text_input("Please add your name:")

        feedback_data = []
        for company in attended_sessions:
            st.write(f"### Feedback for {company}")

            # Question 1
            q1 = st.radio(
                f"1. Relevance to Our Business Needs for {company}: How well does the company’s solution align with our strategic priorities or operational challenges?",
                ["1 – Not Relevant", "2 – Slightly Relevant", "3 – Moderately Relevant", "4 – Highly Relevant", "5 – Extremely Relevant"],
                key=f"relevance_{company}"
            )

            # Question 2
            q2 = st.radio(
                f"2. Innovation and Differentiation for {company}: How innovative or differentiated is the company’s offering compared to existing market solutions?",
                ["1 – Not Innovative", "2 – Slightly Innovative", "3 – Moderately Innovative", "4 – Very Innovative", "5 – Breakthrough Innovation"],
                key=f"innovation_{company}"
            )

            # Question 3
            q3 = st.radio(
                f"3. Product Maturity & Scalability for {company}: Is the product/solution ready for enterprise adoption, and can it scale with our needs?",
                ["1 – Early Stage / Not Ready", "2 – Needs Development", "3 – Somewhat Ready", "4 – Ready", "5 – Fully Enterprise-Ready"],
                key=f"maturity_{company}"
            )

            # Question 4
            q4 = st.radio(
                f"4. Presentation Quality for {company}: Clarity, delivery, and ability to answer questions.",
                ["1 – Poor", "2 – Fair", "3 – Good", "4 – Very Good", "5 – Excellent"],
                key=f"presentation_{company}"
            )

            # Question 5
            q5 = st.radio(
                f"5. Potential for Follow-Up or Pilot for {company}: Would you recommend further exploration or a pilot engagement?",
                ["Yes", "Maybe / Needs Further Review", "No"],
                key=f"follow_up_{company}"
            )

            # Additional comments
            comments = st.text_area(
                f"6. Additional Comments on {company} (Optional):",
                key=f"comments_{company}"
            )

            # Collect feedback for this company
            feedback_data.append((name, company, q1, q2, q3, q4, q5, comments))

        # Submit button
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            # Insert feedback into SQLite database
            for feedback in feedback_data:
                cursor.execute("""
                INSERT INTO feedback2 (name, company, relevance, innovation, maturity, presentation, follow_up, comments)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, feedback)
            conn.commit()
            st.success("Thank you for your feedback!")

# Password-protected section for viewing feedback
st.write("---")
password = st.text_input("Enter password to view submitted feedback:", type="password")
if password == "00000000":  # Replace with your secure password
    st.write("### Submitted Feedback")
    feedback_df = pd.read_sql_query("SELECT * FROM feedback2", conn)
    st.dataframe(feedback_df)

    # Download feedback as CSV
    csv = feedback_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Feedback as CSV",
        data=csv,
        file_name="feedback.csv",
        mime="text/csv",
    )
elif password:
    st.error("Incorrect password. Access denied.")
