import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import os
import sys
# sys.path.append(os.path.join("..", "libs"))
sys.path.append(os.path.join("libs"))



hour = 60*60
day = 24*hour
MPa = 1e6

def show_geometry():
	col11.subheader(f"Geometry view")
	col1_11, col2_12 = col11.columns([1,4])
	radio_value = col1_11.radio("Mesh:", ["on","off"], index=1, horizontal=False)
	mesh_state = f"mesh_{radio_value}"
	if mesh_state not in st.session_state:
		col11.warning(f"Upload {mesh_state}.html file.")
	else:
		with col2_12:
			st.components.v1.html(st.session_state[mesh_state]["data"], height=400, width=350, scrolling=True)
	# col11.write("Something in here.")

def plot_subsidence():
	col32.subheader(f"Subsidence")
	if "subsidence" not in st.session_state:
		col32.warning("Upload subsidence.csv file.")
	else:
		df = st.session_state["subsidence"]["data"]
		uz = df["Subsidence"].values
		uz = uz - uz[0]
		time_list = df["Time"].values
		time_id = st.session_state["Time"]["index"]
		current_time = time_list[time_id]

		fig_subs = px.line()
		fig_subs.add_scatter(x=time_list/day, y=uz*100, mode="lines", line=dict(color="#5abcff"), showlegend=False)
		fig_subs.update_layout(xaxis_title="Time (days)", yaxis_title="Subsidence (cm)")

		marker_props = dict(color='white', size=8, symbol='0', line=dict(width=2, color='black'))
		df_scatter = pd.DataFrame({"x": [current_time/day], "y": [uz[time_id]*100]})
		fig_subs.add_scatter(x=df_scatter["x"], y=df_scatter["y"], mode="markers", line=dict(color='white'), marker=marker_props, showlegend=False)

		col32.plotly_chart(fig_subs, theme="streamlit", use_container_width=True)

def plot_convergence():
	col33.subheader(f"Cavern convergence")
	if "convergence" not in st.session_state:
		col33.warning("Upload convergence.csv file.")
	else:
		df = st.session_state["convergence"]["data"]
		volumes = df["Volume"].values
		time_list = df["Time"].values
		time_id = st.session_state["Time"]["index"]
		current_time = time_list[time_id]

		fig_conv = px.line()
		fig_conv.add_scatter(x=time_list/day, y=volumes, mode="lines", line=dict(color="#5abcff"), showlegend=False)
		fig_conv.update_layout(xaxis_title="Time (days)", yaxis_title="Volumetric loss (%)")

		time_id = st.session_state["Time"]["index"]
		marker_props = dict(color='white', size=8, symbol='0', line=dict(width=2, color='black'))
		df_scatter = pd.DataFrame({"x": [current_time/day], "y": [volumes[time_id]]})
		fig_conv.add_scatter(x=df_scatter["x"], y=df_scatter["y"], mode="markers", line=dict(color='white'), marker=marker_props, showlegend=False)

		col33.plotly_chart(fig_conv, theme="streamlit", use_container_width=True)

def plot_gas_pressure():
	col31.subheader(f"Gas pressure")
	if "gas_pressure" not in st.session_state:
		col31.warning("Upload gas_pressure.csv file.")
	else:
		df = st.session_state["gas_pressure"]["data"]
		p_gas = -df["Pressure"].values
		time_list = df["Time"].values
		time_global = st.session_state["Time"]["data"]
		time_id = st.session_state["Time"]["index"]

		current_p = -np.interp(time_global[time_id], df.Time.values, df.Pressure.values)
		current_time = np.interp(time_global[time_id], df.Time.values, df.Time.values)

		fig_conv = px.line()
		fig_conv.add_scatter(x=time_list/day, y=p_gas/MPa, mode="lines", line=dict(color="#FF57AE"), showlegend=False)
		fig_conv.update_layout(xaxis_title="Time (days)", yaxis_title="Volumetric loss (%)")

		time_id = st.session_state["Time"]["index"]
		marker_props = dict(color='white', size=8, symbol='0', line=dict(width=2, color='black'))
		df_scatter = pd.DataFrame({"x": [current_time/day], "y": [current_p/MPa]})
		fig_conv.add_scatter(x=df_scatter["x"], y=df_scatter["y"], mode="markers", line=dict(color='white'), marker=marker_props, showlegend=False)

		col31.plotly_chart(fig_conv, theme="streamlit", use_container_width=True)



def create_slider():
	col21.markdown("**Select time:**")
	time_list = st.session_state["Time"]["data"]
	time_value = col22.slider("Time", time_list[0], time_list[-1], time_list[0], label_visibility="collapsed")
	diff = abs(time_list - time_value)
	idx = diff.argmin()
	st.session_state["Time"]["index"] = idx
	col23.write(f"Current time: {round(time_list[idx]/day, 2)} day(s)")

def plot_cavern():
	col12.subheader(f"Cavern shape")
	if "cavern_displacements" not in st.session_state:
		col12.warning("Upload cavern_displacements.csv file.")
	else:
		df = st.session_state["cavern_displacements"]["data"]
		time_list = st.session_state["Time"]["data"]
		time_id = st.session_state["Time"]["index"]

		fig_cavern = px.line()
		# fig_cavern.update_xaxes(range=[0, 80])
		fig_cavern.update_layout(yaxis={"scaleanchor": "x", "scaleratio": 1}, xaxis_title="x (m)", yaxis_title="z (m)")

		mask = (df["Time"] == time_list[0])
		fig_cavern.add_scatter(x=df[mask]["dx"], y=df[mask]["dz"], mode="lines+markers", line=dict(color="#5abcff"), marker=dict(size=10))
		fig_cavern.data[1].name = "Initial shape"

		# mask = (df["Time"] == time_list[-1])
		# fig_cavern.add_scatter(x=df[mask]["dx"], y=df[mask]["dz"], mode="lines", line=dict(color='lightcoral'))
		# fig_cavern.data[2].name = "Final shape"

		mask = (df["Time"] == time_list[time_id])
		fig_cavern.add_scatter(x=df[mask]["dx"], y=df[mask]["dz"], mode="lines", line=dict(color="#FF57AE"))
		fig_cavern.data[2].name = "Current shape"

		# event = col12.plotly_chart(fig_cavern, theme=None, on_select="rerun", selection_mode="points", use_container_width=True)
		event = col12.plotly_chart(fig_cavern, theme="streamlit", on_select="rerun", selection_mode="points", use_container_width=True)

		pt = event.selection["points"]
		if len(pt) > 0:
			x = pt[0]["x"]
			y = 0.0
			z = pt[0]["y"]
			st.session_state["selected_point"] = [x, y, z]
			marker_props = dict(color='red', size=8, symbol='0', line=dict(width=2, color='black'))
			fig_cavern.add_scatter(x=[x], y=[z], mode="markers", line=dict(color='red'), marker=marker_props, showlegend=False)
			fig_cavern.update_layout(clickmode="event+select")
			# with col12:
			# 	st.rerun()
			# col12.plotly_chart(fig_cavern, theme="streamlit", use_container_width=True)
			# col12.plotly_chart(fig_cavern, theme="streamlit", on_select="rerun", selection_mode="points", use_container_width=True)
		# if len(pt) > 0:
		# 	x = pt[0]["x"]
		# 	y = pt[0]["y"]
		# 	marker_props = dict(color='red', size=8, symbol='0', line=dict(width=2, color='black'))
		# 	fig_cavern.add_scatter(x=[x], y=[y], mode="markers", line=dict(color='red'), marker=marker_props, showlegend=False)
			# col12.plotly_chart(fig_cavern, theme="streamlit", on_select="rerun", selection_mode="points", use_container_width=True)

		# print(event)
		# print(event.selection)
		# print(event.selection.get("points"))
		# print(pt)

def plot_stress_path():
	col13.subheader(f"Stress path")
	if "stress_path" not in st.session_state:
		col12.warning("Upload stress_path.csv file.")
	else:
		if "selected_point" in st.session_state:
			xp = st.session_state["selected_point"][0]
			yp = st.session_state["selected_point"][1]
			zp = st.session_state["selected_point"][2]
		else:
			xp, yp, zp = 0, 0, 0

		time_list = st.session_state["Time"]["data"]
		time_id = st.session_state["Time"]["index"]
		time = time_list[time_id]

		df = st.session_state["stress_path"]["data"].copy()
		coords = df[["x", "y", "z"]].values
		d = np.sqrt(  (coords[:,0] - xp)**2
			        + (coords[:,1] - yp)**2
			        + (coords[:,2] - zp)**2 )
		idx_min = d.argmin()
		vertex_id = int(df[df["Time"] == 0.0].iloc[idx_min].iloc[0])

		fig_path = px.line()

		mask1 = (df["ID"] == vertex_id)
		fig_path.add_scatter(x=df["p"][mask1]/MPa, y=df["q"][mask1]/MPa, mode="lines", line=dict(color="#5abcff"), showlegend=False)

		marker_props = dict(color='white', size=8, symbol='0', line=dict(width=2, color='black'))
		mask2 = (df["ID"] == vertex_id) & (df["Time"] == time)
		fig_path.add_scatter(x=df["p"][mask2]/MPa, y=df["q"][mask2]/MPa, mode="markers", line=dict(color='red'), marker=marker_props, showlegend=False)

		fig_path.update_layout(xaxis_title="Mean stress, p (MPa)", yaxis_title="Von Mises stress, q (MPa)")

		col13.plotly_chart(fig_path, theme="streamlit", use_container_width=True)


def load_time():
	if "subsidence" in st.session_state:
		df = st.session_state["subsidence"]["data"]
		time_list = df["Time"].values
		st.session_state["Time"] = {
			"data": time_list,
			"index": 0
		}
	else:
		st.session_state["Time"] = {
			"data": np.arange(10),
			"index": 0
		}


st.set_page_config(layout="wide")
st.title("Results Viewer")

col11, col12, col13 = st.columns([1,1,1])
col21, col22, col23 = st.columns([1,8,2])
col31, col32, col33 = st.columns([1,1,1])


load_time()
create_slider()
show_geometry()
plot_cavern()
plot_subsidence()
plot_stress_path()
plot_convergence()
plot_gas_pressure()
