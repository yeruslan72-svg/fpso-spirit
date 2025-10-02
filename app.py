import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
import random
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="FPSO Spirit - AVCS + Thermal DNA",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# SESSION STATE INIT
# =========================
if "system_data" not in st.session_state:
    st.session_state.system_data = {}
if "monitoring_active" not in st.session_state:
    st.session_state.monitoring_active = False
if "emergency_stop" not in st.session_state:
    st.session_state.emergency_stop = False
if "cycle_count" not in st.session_state:
    st.session_state.cycle_count = 0
if "historical_data" not in st.session_state:
    st.session_state.historical_data = []
if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()
if "prevented_incidents" not in st.session_state:
    st.session_state.prevented_incidents = 0
if "cost_savings" not in st.session_state:
    st.session_state.cost_savings = 0

# AI Model
if "ai_model" not in st.session_state:
    np.random.seed(42)
    normal_data = np.random.normal(0, 1, (1000, 20))
    st.session_state.ai_model = IsolationForest(contamination=0.08, random_state=42)
    st.session_state.ai_model.fit(normal_data)


# =========================
# DATA GENERATOR
# =========================
def generate_sensor_data(cycle: int):
    degradation = min(1.0, cycle * 0.001)

    data = {
        # Hull
        "heel_angle": 0.3 + np.random.normal(0, 0.2) + degradation * 0.3,
        "trim_angle": 0.4 + np.random.normal(0, 0.2) + degradation * 0.2,
        "hull_stress": 25 + np.sin(cycle * 0.1) * 10 + degradation * 15,
        "bending_moment": 1200 + np.random.normal(0, 100) + degradation * 120,
        "shear_force": 800 + np.random.normal(0, 80) + degradation * 100,

        # Equipment vibration (mm/s)
        "DG1_vib": 1.5 + np.random.normal(0, 0.3) + degradation * 0.6,
        "DG2_vib": 1.6 + np.random.normal(0, 0.4) + degradation * 0.7,
        "Pump1_vib": 2.0 + np.random.normal(0, 0.5) + degradation * 0.8,
        "Pump2_vib": 1.8 + np.random.normal(0, 0.5) + degradation * 0.7,
        "Pump3_vib": 2.1 + np.random.normal(0, 0.5) + degradation * 0.9,
        "BallastP_vib": 1.7 + np.random.normal(0, 0.3) + degradation * 0.5,
        "BallastS_vib": 1.6 + np.random.normal(0, 0.3) + degradation * 0.6,
        "Boiler_vib": 0.8 + np.random.normal(0, 0.2),
        "IG_vib": 0.5 + np.random.normal(0, 0.1),

        # Equipment temperature (°C)
        "DG1_temp": 85 + np.random.normal(0, 5) + degradation * 10,
        "DG2_temp": 82 + np.random.normal(0, 6) + degradation * 8,
        "Pump1_temp": 88 + np.random.normal(0, 7) + degradation * 12,
        "Pump2_temp": 86 + np.random.normal(0, 6) + degradation * 11,
        "Pump3_temp": 87 + np.random.normal(0, 7) + degradation * 12,
        "Boiler_temp": 120 + np.random.normal(0, 10),
        "IG_temp": 60 + np.random.normal(0, 5),

        # Cargo tanks
        **{f"Cargo_{i}": 42 + np.random.normal(0, 2) for i in range(1, 7)},

        # Ballast tanks (Port + Starboard)
        **{f"BallastP_{i}": 55 + np.random.normal(0, 5) for i in range(1, 7)},
        **{f"BallastS_{i}": 55 + np.random.normal(0, 5) for i in range(1, 7)},

        # Slop & Forepeak
        "SlopP": 40 + np.random.normal(0, 3),
        "SlopS": 41 + np.random.normal(0, 3),
        "Forepeak": 60 + np.random.normal(0, 5),
    }

    # AI detection
    try:
        features = [
            data["hull_stress"], data["heel_angle"], data["DG1_vib"], data["Pump1_vib"],
            data["DG1_temp"], data["Pump1_temp"], data["Cargo_1"]
        ]
        ai_prediction = st.session_state.ai_model.predict([features])[0]
        data["ai_anomaly"] = ai_prediction
        if ai_prediction == -1:
            data["ai_action"] = "PREEMPTIVE DAMPING"
            if random.random() < 0.3:
                st.session_state.prevented_incidents += 1
                st.session_state.cost_savings += 200000
        else:
            data["ai_action"] = "MONITORING"
    except:
        data["ai_anomaly"] = 1
        data["ai_action"] = "MONITORING"

    return data


# =========================
# VISUALS
# =========================
def hull_visualization(data):
    length, width, height = 100, 20, 15
    x = np.array([0, length, length, 0, 0, length, length, 0])
    y = np.array([0, 0, width, width, 0, 0, width, width])
    z = np.array([0, 0, 0, 0, height, height, height, height])

    heel = np.radians(data["heel_angle"])
    trim = np.radians(data["trim_angle"])
    y_heel = y * np.cos(heel) - z * np.sin(heel)
    z_heel = y * np.sin(heel) + z * np.cos(heel)
    x_trim = x * np.cos(trim) - z_heel * np.sin(trim)
    z_final = x * np.sin(trim) + z_heel * np.cos(trim)

    fig = go.Figure()
    fig.add_trace(go.Mesh3d(
        x=x_trim, y=y_heel, z=z_final,
        color="lightblue", opacity=0.6, name="Hull"
    ))

    fig.update_layout(
        title=f"Hull Stress: {data['hull_stress']:.1f}%",
        scene=dict(aspectmode="data"),
        height=500
    )
    return fig


def equipment_vibration_chart(data, show_dampers=True):
    eq = ["DG1", "DG2", "Pump1", "Pump2", "Pump3", "BallastP", "BallastS", "Boiler", "IG"]
    vibrations = [data[f"{e}_vib"] for e in eq]

    colors = ["red" if v > 3 else "orange" if v > 2 else "green" for v in vibrations]

    fig = go.Figure(go.Bar(
        x=eq, y=vibrations, marker_color=colors,
        text=[f"{v:.1f}" for v in vibrations], textposition="auto"
    ))

    if show_dampers:
        fig.add_hline(y=3, line_dash="dash", line_color="red", annotation_text="Critical")
        fig.add_hline(y=2, line_dash="dot", line_color="orange", annotation_text="Warning")

    fig.update_layout(title="Vibration Monitoring", height=350)
    return fig


def tank_temperature_chart(data):
    cargo = [data[f"Cargo_{i}"] for i in range(1, 7)]
    ballastP = [data[f"BallastP_{i}"] for i in range(1, 7)]
    ballastS = [data[f"BallastS_{i}"] for i in range(1, 6)]
    slop = [data["SlopP"], data["SlopS"], data["Forepeak"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=[f"C{i}" for i in range(1, 7)], y=cargo, name="Cargo Tanks"))
    fig.add_trace(go.Bar(x=[f"P{i}" for i in range(1, 7)], y=ballastP, name="Ballast Port"))
    fig.add_trace(go.Bar(x=[f"S{i}" for i in range(1, 7)], y=ballastS, name="Ballast Stbd"))
    fig.add_trace(go.Bar(x=["SlopP", "SlopS", "Forepeak"], y=slop, name="Special Tanks"))

    fig.update_layout(barmode="group", title="Tank Temperatures / Levels", height=350)
    return fig


# =========================
# MAIN APP
# =========================
def main():
    st.title("🌊 FPSO Spirit – AVCS DNA + Thermal DNA")
    st.markdown("Digital Twin with **Hull, Equipment, Tanks, AI Anomaly Detection**")

    # Sidebar Control
    st.sidebar.header("⚙️ Control Panel")
    speed = st.sidebar.slider("Animation Speed (s)", 0.1, 2.0, 1.0, 0.1)
    dampers = st.sidebar.checkbox("Enable MR Dampers", value=True)
    ai_enable = st.sidebar.checkbox("Enable AI Analysis", value=True)

    if st.sidebar.button("▶️ Start Monitoring"):
        st.session_state.monitoring_active = True
        st.session_state.last_update = datetime.now()
    if st.sidebar.button("⏸️ Stop Monitoring"):
        st.session_state.monitoring_active = False
    if st.sidebar.button("🛑 Emergency Stop"):
        st.session_state.emergency_stop = True
        st.session_state.monitoring_active = False
    if st.sidebar.button("♻️ Reset"):
        for k in ["cycle_count", "historical_data", "prevented_incidents", "cost_savings"]:
            st.session_state[k] = 0
        st.session_state.system_data = {}
        st.session_state.emergency_stop = False
        st.session_state.monitoring_active = False

    # MAIN LOOP
    if st.session_state.monitoring_active and not st.session_state.emergency_stop:
        now = datetime.now()
        if (now - st.session_state.last_update).total_seconds() > speed:
            st.session_state.system_data = generate_sensor_data(st.session_state.cycle_count)
            st.session_state.cycle_count += 1
            st.session_state.last_update = now
            st.session_state.historical_data.append(st.session_state.system_data.copy())
            if len(st.session_state.historical_data) > 100:
                st.session_state.historical_data.pop(0)
            st.rerun()

    # OUTPUT
    if st.session_state.emergency_stop:
        st.error("🚨 EMERGENCY STOP")
        return

    if st.session_state.system_data:
        data = st.session_state.system_data
        tabs = st.tabs(["Hull", "Equipment", "Tanks", "AI Dashboard"])

        with tabs[0]:
            st.plotly_chart(hull_visualization(data), use_container_width=True)

        with tabs[1]:
            st.plotly_chart(equipment_vibration_chart(data, dampers), use_container_width=True)

        with tabs[2]:
            st.plotly_chart(tank_temperature_chart(data), use_container_width=True)

        with tabs[3]:
            st.metric("AI Action", data["ai_action"])
            st.metric("Prevented Incidents", st.session_state.prevented_incidents)
            st.metric("Cost Savings", f"${st.session_state.cost_savings:,}")


if __name__ == "__main__":
    main()
