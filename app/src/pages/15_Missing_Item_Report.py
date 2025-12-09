import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Create New Lost Item Report")

# Initialize session state for modal
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_report_name" not in st.session_state:
    st.session_state.success_report_name = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if "form_key_counter" not in st.session_state:
    st.session_state.form_key_counter = 0

# Define the success dialog function
@st.dialog("Success")
def show_success_dialog(item_name):
    st.markdown(f"### {item_name} has been successfully added to the system!")
    
    # Create two buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Return to Found Item Catalogue", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_report_name = ""
            st.switch_page("pages/14_Item_Catalogue.py")
    
    with col2:
        if st.button("Create Another Report", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_report_name = ""
            st.session_state.reset_form = True
            st.rerun()

# Handle form reset
if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

# API endpoint
API_URL = "http://web-api:4000/foundit/lost_item_report"

# Create a form for NGO details with dynamic key to force reset
with st.form(f"add_report_{st.session_state.form_key_counter}"):
    st.subheader("Missing Item Reports")

    # Required fields
    name = st.text_input("Item Name *")
    location = st.text_input("Location Lost *")
    # founding_year = st.number_input(
        # "Founding Year *", min_value=1800, max_value=2024, value=2024
    # )
    date = st.text_input("Date Lost *")

    # Form submission button
    submitted = st.form_submit_button("Submit Report")

    if submitted:
        # Validate required fields
        if not all([name, location, date]):
            st.error("Please fill in all required fields marked with *")
        else:
            # Prepare the data for API
            item_data = {
                "Name": name,
                "Location Lost": location,
                "Date Lost": date
            }

            try:
                # Send POST request to API
                response = requests.post(API_URL, json=item_data)

                if response.status_code == 201:
                    # Store item report and show modal
                    st.session_state.show_success_modal = True
                    st.session_state.success_report_name = name
                    st.rerun()
                else:
                    st.error(
                        f"Failed to create Report: {response.json().get('error', 'Unknown error')}"
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

# Show success modal if NGO was added successfully
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_report_name)

# Add a button to return to the NGO Directory
if st.button("Return to Found Item Catalogue"):
    st.switch_page("pages/14_Item_Catalogue.py")
