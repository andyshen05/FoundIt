import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Found Item Directory")

# API endpoint
API_URL = "http://web-api:4000/foundit/found_item_inventory"

# Create filter columns
col1, col2, col3 = st.columns(3)

# Get unique values for filters from the API
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        items = response.json()

        # Extract unique values for filters
        items = sorted(list(set(item["Item"] for item in items)))
        locations = sorted(list(set(item["Location_Found"] for item in items)))
        dates = sorted(list(set(item["Date_Found"] for item in items)))

        # Create filters
        with col1:
            selected_item = st.selectbox("Filter by Item", ["All"] + items)

        with col2:
            selected_location = st.selectbox("Filter by Location", ["All"] + locations)

        with col3:
            selected_date = st.selectbox(
                "Filter by Date",
                ["All"] + [str(date) for date in dates],
            )

        # Build query parameters
        params = {}
        if selected_item != "All":
            params["item"] = selected_item
        if selected_location != "All":
            params["locations"] = selected_location
        if selected_date != "All":
            params["dates"] = selected_date

        # Get filtered data
        filtered_response = requests.get(API_URL, params=params)
        if filtered_response.status_code == 200:
            filtered_items = filtered_response.json()

            # Display results count
            st.write(f"Found {len(filtered_items)} Items")

            # Create expandable rows for each item
            for item in filtered_items:
                with st.expander(f"{item['Name']} ({item['Location']})"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Basic Information**")
                        st.write(f"**Item:** {item['Item']}")
                        st.write(f"**Location Found:** {item['Location_Found']}")
                        st.write(f"**Date Found:** {item['Date_Found']}")

                    with col2:
                        st.write("**Contact Information**")
                        st.write(f"**Email:** [{item['Email']}]")
                        st.write(f"**Phone Number:** [{item['Phone']}]")

    else:
        st.error("Failed to fetch item data from the API")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to the API: {str(e)}")
    st.info("Please ensure the API server is running on http://web-api:4000")
