import streamlit as st
import pandas as pd

# Set up the Streamlit app title
st.title("for Data Entry:")

# Define function to append data to Excel file
def append_to_excel(data, file_name):
    # Load existing Excel file or create new file if it doesn't exist
    try:
        df = pd.read_excel(file_name)
    except:
        df = pd.DataFrame()
    
    # Append data to Excel file
    
    df = df.append(data, ignore_index=True)
    df.to_excel(file_name, index=False)

# Create Streamlit form to collect input data
with st.form("append_data_form"):
    # Create form fields for input data
    proj_title = st.text_input("Project Title")
    required_skills = st.text_input("Required Skills")
    difficulty = st.text_input("Difficulty level")
    proj_type = st.text_input("Project Type")
    proj_domain = st.text_input("Project Domain")
    proj_desc = st.text_input("Project Desription")
    company_name=st.text_input("company name")
    company_contact=st.text_input("Contact no.")

    # Create button to submit form data
    submit_button = st.form_submit_button(label="Append Data")

# Define data to be appended to Excel file
data = {"Project_title": proj_title, "Required_Skills": required_skills, "Difficulty_level": difficulty, "Project_type":proj_type,"Project_domain":proj_domain,"Description":proj_desc,"Company_name":company_name,"Contact":company_contact}

# Append data to Excel file when form is submitted
if submit_button:
    file_name = "Proj_list.xlsx"  # Change this to your desired file name
    append_to_excel(data, file_name)
    st.success("Data appended successfully!")
