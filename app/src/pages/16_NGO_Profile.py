import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Item Report")

# Get ITEM ID from session state
item_id = st.session_state.get("selected_item_id")

if item_id is None:
    st.error("No Item selected")
    st.button(
        "Return to Item Catalogue",
        on_click=lambda: st.switch_page("pages/14_NGO_Directory.py"),
    )
else:
    # API endpoint
    API_URL = f"http://web-api:4000/ngo/ngos/{item_id}"

    try:
        # Fetch Item details
        response = requests.get(API_URL)

        if response.status_code == 200:
            item = response.json()

            # Display basic information
            st.header(item["Name"])

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Basic Information")
                st.write(f"**Item:** {item['Country']}")
                st.write(f"**Location Found:** {item['Location_Found']}")
                st.write(f"**Date Found:** {item['Date_Found']}")
                st.write(f"**Description:** {item['Description']}")

            with col2:
                st.write("**Contact Information**")
                st.write(f"**Email:** [{item['Email']}]")
                st.write(f"**Phone Number:** [{item['Phone']}]")

        elif response.status_code == 404:
            st.error("Item not found")
        else:
            st.error(
                f"Error fetching item data: {response.json().get('error', 'Unknown error')}"
            )

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        st.info("Please ensure the API server is running")

# Add a button to return to the Item Catalogue
if st.button("Return to Item Catalogue"):
    # Clear the selected Item ID from session state
    if "selected_item_id" in st.session_state:
        del st.session_state["selected_item_id"]
    st.switch_page("pages/14_NGO_Directory.py")
