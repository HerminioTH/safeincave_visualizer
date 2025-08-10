import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")


def read_mesh_on(file):
	if "mesh_on" not in st.session_state:
		html_content = file.read().decode("utf-8", errors="ignore")
		html_content.replace(
			"</head>",
		    "<style>html,body{background:#0d1117 !important;}</style></head>"
		)
		st.session_state["mesh_on"] = {
			"data" : html_content,
			"name" : file.name
		}

def read_mesh_off(file):
	if "mesh_off" not in st.session_state:
		st.session_state["mesh_off"] = {
			"data" : file.read().decode("utf-8", errors="ignore"),
			"name" : file.name
		}

def read_cavern_displacements(file):
	if "cavern_displacements" not in st.session_state:
		st.session_state["cavern_displacements"] = {
			"data" : pd.read_csv(file, index_col=0),
			"name" : file.name
		}

def read_subsidence(file):
	if "subsidence" not in st.session_state:
		st.session_state["subsidence"] = {
			"data" : pd.read_csv(file, index_col=0),
			"name" : file.name
		}

def read_stress_path(file):
	if "stress_path" not in st.session_state:
		st.session_state["stress_path"] = {
			"data" : pd.read_csv(file, index_col=0),
			"name" : file.name
		}

def read_convergence(file):
	if "convergence" not in st.session_state:
		st.session_state["convergence"] = {
			"data" : pd.read_csv(file, index_col=0),
			"name" : file.name
		}

def read_gas_pressure(file):
	if "gas_pressure" not in st.session_state:
		st.session_state["gas_pressure"] = {
			"data" : pd.read_csv(file, index_col=0),
			"name" : file.name
		}



def upload_all_at_once():
	uploaded_files = st.file_uploader("Upload results files", type=["html", "csv"], accept_multiple_files=True)
	if uploaded_files is not None:
		for file in uploaded_files:
			print(file.name)
			if file.name == "mesh_on.html":
				read_mesh_on(file)
			elif file.name == "mesh_off.html":
				read_mesh_off(file)
			elif file.name == "cavern_displacements.csv":
				read_cavern_displacements(file)
			elif file.name == "subsidence.csv":
				read_subsidence(file)
			elif file.name == "stress_path.csv":
				read_stress_path(file)
			elif file.name == "convergence.csv":
				read_convergence(file)
			elif file.name == "gas_pressure.csv":
				read_gas_pressure(file)
			else:
				st.warning(f"File {file.name} is will be ignored.", icon="⚠️")


def check_uploaded_files():
	if "mesh_on" in st.session_state:
		st.session_state["uploaded_files_complete"] = True
	else:
		st.session_state["uploaded_files_complete"] = False


st.title("Upload results files")

upload_all_at_once()

# upload_mesh()
# upload_displacement()
check_uploaded_files()