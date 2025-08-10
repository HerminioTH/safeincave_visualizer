import streamlit as st
import os

st.set_page_config(
    page_title="SafeInCave Docs",
    page_icon=os.path.join("assets", "logo.png"),
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items=None,
)
st._config.set_option("theme.base", "light")

about_page = st.Page(
	page="views/about.py",
	title="About",
	icon=":material/info_i:",
	default=True
)

upload_page = st.Page(
	page="views/upload.py",
	title="Upload files",
	icon=":material/upload:",
)

dashboard1_page = st.Page(
	page="views/dashboard_1.py",
	title="View results",
	icon=":material/bid_landscape:",
)


# st.markdown(
#     """
#     <style>
#         /* Target the navigation menu text */
#         [data-testid="stNavigation"] {
#             color: red !important;  /* Change to your desired color */
#         }
        
#         /* Optional: Change hover/focus colors */
#         [data-testid="stNavigation"] button:hover,
#         [data-testid="stNavigation"] button:focus {
#             color: darkred !important;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown("""
# <style>
# /* All nav link text */
# div[data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"] span {
#   color: #1f6feb !important;
# }

# /* Section headers like "Info", "Visualizer" */
# div[data-testid="stSidebarNav"] button span,
# div[data-testid="stSidebarNav"] button p,
# div[data-testid="stSidebarNav"] li > div > span {
#   color: #1f6feb !important;
# }

# /* Optional: hover/focus on headers */
# div[data-testid="stSidebarNav"] button:hover span,
# div[data-testid="stSidebarNav"] button:focus span {
#   color: #d29922 !important;
# }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("""
# <style>
# /* Recolor everything inside the sidebar navigation area */
# div[data-testid="stSidebarNav"] * { 
#   color: #2B2B2B !important; 
# }
# </style>
# """, unsafe_allow_html=True)

pg = st.navigation(
	{
		"Info": [about_page],
		"Visualizer": [upload_page, dashboard1_page]
	}
)

st.logo(os.path.join("assets", "logo_safeincave.png"))
st.sidebar.text("Something here.")

pg.run()