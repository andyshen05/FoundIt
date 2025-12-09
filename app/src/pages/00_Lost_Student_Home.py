import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, Student {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Submit Missing Item Report', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Missing_Item.py')

if st.button('View All Found Items in Storage', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/14_Item_Catalogue.py')

if st.button('Report a Malicious User', 
            type='primary',
            use_container_width=True):
  st.switch_page('pages/02_Item_Catalogue.py')