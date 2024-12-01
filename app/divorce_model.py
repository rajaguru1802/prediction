import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt

# Updated prediction function with relationship type consideration
def predict_divorce(data, relationship_type):
    """
    Predicts the future of the relationship based on machine learning and relationship type.
    Provides relationship improvement suggestions based on divorce risk and relationship type.
    """

    feature_names = ['years_married', 'communication_score', 'shared_activities', 'financial_stability', 
                     'conflict_resolution', 'age', 'children_count', 'education_level', 'job_satisfaction', 'mental_health', 
                     'conflict_history', 'stress_levels']

    # Convert the inputs into a numpy array
    input_data = np.array([data[feature] for feature in feature_names]).reshape(1, -1)

    # Example synthetic data (for demonstration purposes)
    synthetic_data = pd.DataFrame({
        'years_married': np.random.randint(0, 30, 100),
        'communication_score': np.random.uniform(1, 5, 100),
        'shared_activities': np.random.uniform(1, 5, 100),
        'financial_stability': np.random.uniform(1, 5, 100),
        'conflict_resolution': np.random.uniform(1, 5, 100),
        'age': np.random.randint(18, 60, 100),
        'children_count': np.random.randint(0, 5, 100),
        'education_level': np.random.randint(1, 4, 100),
        'job_satisfaction': np.random.uniform(1, 5, 100),
        'mental_health': np.random.uniform(1, 5, 100),
        'conflict_history': np.random.randint(0, 2, 100),  # 0: No, 1: Yes
        'stress_levels': np.random.uniform(1, 5, 100)
    })

    target = np.random.choice([0, 1], size=100)  # 0: Low Risk, 1: High Risk

    # Train a RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(synthetic_data, target)

    # Make predictions
    prediction = clf.predict(input_data)

    # Feature importance visualization
    perm_importance = permutation_importance(clf, synthetic_data, target, n_repeats=10, random_state=42)
    sorted_idx = perm_importance.importances_mean.argsort()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(range(len(sorted_idx)), perm_importance.importances_mean[sorted_idx], align='center')
    ax.set_yticks(range(len(sorted_idx)))
    ax.set_yticklabels(np.array(feature_names)[sorted_idx])
    ax.set_xlabel("Feature Importance")
    ax.set_title("Feature Importance - Relationship Prediction Model")
    st.pyplot(fig)

    # Relationship improvement suggestions
    suggestions = ""
    if prediction[0] == 1:
        suggestions = """
        **High Risk**: Based on your inputs, the model predicts a high risk of relationship failure. 
        Here are some suggestions to improve your relationship:
        
        - **Improve Communication**: Make time for open, honest conversations with your partner.
        - **Seek Professional Help**: Consider couples counseling to work through unresolved issues.
        - **Spend More Quality Time Together**: Plan activities you both enjoy to strengthen your bond.
        - **Manage Conflict Effectively**: Learn healthy conflict resolution strategies.
        - **Focus on Mental Health**: Address individual stress or mental health issues that could affect your relationship.
        """
    else:
        suggestions = """
        **Low Risk**: Your relationship appears to be in a healthy state based on your inputs. Here are some tips to continue nurturing it:
        
        - **Continue Building Communication**: Keep nurturing open and honest conversations.
        - **Make Time for Each Other**: Continue planning activities you both enjoy to stay connected.
        - **Strengthen Conflict Resolution Skills**: Keep practicing healthy ways of resolving conflicts.
        - **Maintain Work-Life Balance**: Continue to prioritize both work and personal time to reduce stress.
        - **Support Mental Well-Being**: Continue supporting each other’s mental and emotional health.
        """

    # Specific relationship-type suggestions
    if relationship_type == "Friendship":
        suggestions += """
        **For Friendship Relationships**: Consider the following to maintain a strong friendship:
        
        - **Open Communication**: Be honest and open with each other.
        - **Trust and Respect**: Build a foundation of mutual respect and trust.
        - **Support Each Other**: Be there for each other during tough times.
        """

    return "High Risk" if prediction[0] == 1 else "Low Risk", suggestions
