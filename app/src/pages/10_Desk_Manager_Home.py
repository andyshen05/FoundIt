import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Desk Manager, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Item Catalogue', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/14_Item_Catalogue.py')

if st.button('View Lost Item Reports', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Lost_Item_Reports.py')

if st.button('View User Contact Information', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/16_User_Database.py')
  