import streamlit as st
from user_auth import create_user_table, add_user, validate_user
from app.divorce_model import predict_divorce

# Create the user table when the app starts
create_user_table()

# Streamlit UI
st.title(" THANI CAN ")
st.markdown("### Predict the future of your relationship based on key factors")

# Streamlit session state for managing login status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Sidebar navigation
sidebar = st.sidebar.selectbox("Choose an option", ["Home", "Predict Relationship Future", "Login", "Sign Up"])

# Home page
if sidebar == "Home":
    st.write("Welcome to the **Relationship in Future Prediction** app! 🚀")
    st.write("Provide details about your relationship to predict how it may evolve in the future.")
    st.write("This model uses machine learning and factors like communication, financial stability, mental health, etc., to make a prediction.")

# Login page
elif sidebar == "Login":
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if validate_user(email, password):
            st.session_state['logged_in'] = True
            st.session_state['email'] = email  # Store the logged-in email
            st.success("Logged in successfully!")
        else:
            st.error("Invalid email or password. Please try again.")

# Sign-up page
elif sidebar == "Sign Up":
    st.subheader("Create a New Account")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password == confirm_password:
            success = add_user(username, email, password)
            if success:
                st.success("Account created successfully! Please log in.")
            else:
                st.error("Email or username already exists. Please try a different one.")
        else:
            st.error("Passwords do not match.")

# Prediction page (only for logged-in users)
elif sidebar == "Predict Relationship Future":
    if not st.session_state['logged_in']:
        st.warning("You need to log in to access this page.")
        st.stop()

    st.subheader("Provide Your Relationship Details")

    # Collecting input data based on the selected relationship type
    relationship_type = st.selectbox("Relationship Type", ["Married", "Unmarried", "Friendship"])

    years_married = st.number_input("Years in Relationship", min_value=0, max_value=50, step=1)
    communication_score = st.slider("Communication Score", 1.0, 5.0, step=0.1)
    shared_activities = st.slider("Shared Activities Score", 1.0, 5.0, step=0.1)
    financial_stability = st.slider("Financial Stability Score", 1.0, 5.0, step=0.1)
    conflict_resolution = st.slider("Conflict Resolution Score", 1.0, 5.0, step=0.1)
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    children_count = st.number_input("Children Count", min_value=0, max_value=5, step=1)
    education_level = st.selectbox("Education Level", ["High School", "College", "Graduate"])
    job_satisfaction = st.slider("Job Satisfaction", 1.0, 5.0, step=0.1)
    mental_health = st.slider("Mental Health Status", 1.0, 5.0, step=0.1)
    conflict_history = st.radio("Conflict History", ["No", "Yes"])
    stress_levels = st.slider("Stress Levels", 1.0, 5.0, step=0.1)

    # Map user input to model input
    data = {
        'years_married': years_married if relationship_type == "Married" else 0,  # Married only
        'communication_score': communication_score,
        'shared_activities': shared_activities,
        'financial_stability': financial_stability,
        'conflict_resolution': conflict_resolution,
        'age': age,
        'children_count': children_count if relationship_type == "Married" else 0,  # Only relevant for married relationships
        'education_level': 1 if education_level == "High School" else (2 if education_level == "College" else 3),
        'job_satisfaction': job_satisfaction,
        'mental_health': mental_health,
        'conflict_history': 1 if conflict_history == "Yes" else 0,
        'stress_levels': stress_levels
    }
    
    if st.button("Predict"):
        result, suggestions = predict_divorce(data, relationship_type)  # Pass relationship_type to the model
        st.subheader(f"Prediction: {result}")
        st.markdown(suggestions)  # Display relationship improvement suggestions
