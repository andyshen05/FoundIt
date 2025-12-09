import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("User Information")

# API endpoint
API_URL = "http://web-api:4000/foundit/user"

# Create filter columns
col1, col2, col3 = st.columns(3)

# Get unique values for filters from the API
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        users = response.json()

        # Extract unique values for filters
        status = sorted(list(set(user["accStatus"] for user in users)))

        # Create filters
        with col1:
            selected_status = st.selectbox("Filter by Status", ["All"] + status)

        # Build query parameters
        params = {}
        if selected_status != "All":
            params["accStatus"] = selected_status

        # Get filtered data
        filtered_response = requests.get(API_URL, params=params)
        if filtered_response.status_code == 200:
            filtered_items = filtered_response.json()

            # Display results count
            st.write(f"Found {len(filtered_items)} Users")

            # Create expandable rows for each item
            for item in filtered_items:
                with st.expander(f"{item['name']} ({item['email']})"):
                    col1 = st.columns(1)

                    with col1:
                        st.write("**Contact Information**")
                        st.write(f"**Name:** [{item['nane']}]")
                        st.write(f"**Email:** [{item['email']}]")
                        st.write(f"**Phone Number:** [{item['phoneNumber']}]")
                        st.write(f"**Status:** [{item['accStatus']}]")

    else:
        st.error("Failed to fetch item data from the API")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
