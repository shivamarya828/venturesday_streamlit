# streamlit_app.py
import streamlit as st
import sqlite3
import pandas as pd

# Initialize SQLite database
conn = sqlite3.connect("feedback.db")
cursor = conn.cursor()

# # Drop the table if it exists
# cursor.execute("DROP TABLE IF EXISTS feedback")

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
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
st.title("COE Ventures Day – Leader Feedback Form")
st.write("Please complete this form after each session to help us evaluate the featured ventures and improve future events.")

# Feedback form
with st.form("feedback_form"):
    # Question: Name
    name = st.text_input("Please add your name:")

    # Question 1
    q1 = st.radio(
        "1. Relevance to Our Business Needs: How well does the company’s solution align with our strategic priorities or operational challenges?",
        ["1 – Not Relevant", "2 – Slightly Relevant", "3 – Moderately Relevant", "4 – Highly Relevant", "5 – Extremely Relevant"],
    )

    # Question 2
    q2 = st.radio(
        "2. Innovation and Differentiation: How innovative or differentiated is the company’s offering compared to existing market solutions?",
        ["1 – Not Innovative", "2 – Slightly Innovative", "3 – Moderately Innovative", "4 – Very Innovative", "5 – Breakthrough Innovation"],
    )

    # Question 3
    q3 = st.radio(
        "3. Product Maturity & Scalability: Is the product/solution ready for enterprise adoption, and can it scale with our needs?",
        ["1 – Early Stage / Not Ready", "2 – Needs Development", "3 – Somewhat Ready", "4 – Ready", "5 – Fully Enterprise-Ready"],
    )

    # Question 4
    q4 = st.radio(
        "4. Presentation Quality: Clarity, delivery, and ability to answer questions.",
        ["1 – Poor", "2 – Fair", "3 – Good", "4 – Very Good", "5 – Excellent"],
    )

    # Question 5
    q5 = st.radio(
        "5. Potential for Follow-Up or Pilot: Would you recommend further exploration or a pilot engagement?",
        ["Yes", "Maybe / Needs Further Review", "No"],
    )

    # Additional comments
    comments = st.text_area("6. Additional Comments on the Company or Solution (Optional):")

    # Submit button
    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        # Insert feedback into SQLite database
        cursor.execute("""
        INSERT INTO feedback (name, relevance, innovation, maturity, presentation, follow_up, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, q1, q2, q3, q4, q5, comments))
        conn.commit()
        st.success("Thank you for your feedback!")

# Password-protected section for viewing feedback
st.write("---")
password = st.text_input("Enter password to view submitted feedback:", type="password")
if password == "00000000":  # Replace with your secure password
    st.write("### Submitted Feedback")
    feedback_df = pd.read_sql_query("SELECT * FROM feedback", conn)
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
