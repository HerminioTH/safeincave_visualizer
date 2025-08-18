import streamlit as st
import os

st.set_page_config(
    page_title="SafeInCave Docs",
    page_icon=os.path.join("assets", "logo.png"),
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items=None,
)
st._config.set_option("theme.base", "dark")

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





pg = st.navigation(
	{
		"Info": [about_page],
		# "Visualizer": [upload_page, dashboard1_page]
		"Visualizer": [dashboard1_page]
	}
)

st.logo(os.path.join("assets", "logo_safeincave.png"))
st.sidebar.text("Something here.")

pg.run()