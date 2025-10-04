# app.py - FPSO SPIRIT FULL SIMULATOR
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime

# ----------------------
# Initialization
# ----------------------
if 'systems' not in st.session_state:
    st.session_state.systems = {
        'cargo_tanks': {
            'TANK_1': {'volume': 12000, 'capacity': 15000, 'valve_open': False, 'level': 80.0},
            'TANK_2': {'volume': 13500, 'capacity': 15000, 'valve_open': False, 'level': 90.0},
            'TANK_3': {'volume': 9000, 'capacity': 15000, 'valve_open': False, 'level': 60.0},
            'TANK_4': {'volume': 14250, 'capacity': 15000, 'valve_open': False, 'level': 95.0},
            'TANK_5': {'volume': 7500, 'capacity': 15000, 'valve_open': False, 'level': 50.0},
            'TANK_6': {'volume': 11250, 'capacity': 15000, 'valve_open': False, 'level': 75.0},
        },
        'cargo_pumps': {
            'CARGO_PUMP_1': {'running': False, 'flow': 0},
            'CARGO_PUMP_2': {'running': False, 'flow': 0},
            'STRIPPING_PUMP': {'running': False, 'flow': 0},
        },
        'ballast_tanks': {
            'BALLAST_1P': {'volume': 2000, 'capacity': 5000},
            'BALLAST_1S': {'volume': 3000, 'capacity': 5000},
            'BALLAST_2P': {'volume': 1500, 'capacity': 5000},
            'BALLAST_2S': {'volume': 3500, 'capacity': 5000},
            'BALLAST_F': {'volume': 1200, 'capacity': 3000},
            'BALLAST_A': {'volume': 1800, 'capacity': 3000},
        },
        'vessel_status': {
            'heel': 2.5, 'trim': 0.8, 'draft_fore': 18.2, 'draft_aft': 19.0,
        },
        'safety_systems': {
            'esd_level': 0, 'igs_pressure': 0.8, 'igs_o2': 2.5,
        },
        'operations': {
            'total_cargo': sum([tank['level'] for tank in st.session_state.systems['cargo_tanks'].values()]) if 'systems' in st.session_state else 0,
            'weather': {'wind_speed': 8.5, 'wind_dir': 45}
        }
    }
    st.session_state['last_update'] = datetime.now()


# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(
    page_title="FPSO SPIRIT - Simulator",
    layout="wide"
)

st.title("⚓ FPSO SPIRIT Simulator - Full CCR")


# ----------------------
# FUNCTIONS
# ----------------------
def update_cargo_total():
    st.session_state.systems['operations']['total_cargo'] = sum(
        [tank['level'] for tank in st.session_state.systems['cargo_tanks'].values()]
    )


def toggle_valve(tank_name):
    st.session_state.systems['cargo_tanks'][tank_name]['valve_open'] = not st.session_state.systems['cargo_tanks'][tank_name]['valve_open']
    st.session_state['last_update'] = datetime.now()


def toggle_pump(pump_name):
    pump = st.session_state.systems['cargo_pumps'][pump_name]
    pump['running'] = not pump['running']
    pump['flow'] = 800 if pump['running'] else 0
    st.session_state['last_update'] = datetime.now()


def ballast_in(tank_name):
    tank = st.session_state.systems['ballast_tanks'][tank_name]
    tank['volume'] = min(tank['capacity'], tank['volume'] + 500)
    st.session_state['last_update'] = datetime.now()


def ballast_out(tank_name):
    tank = st.session_state.systems['ballast_tanks'][tank_name]
    tank['volume'] = max(0, tank['volume'] - 500)
    st.session_state['last_update'] = datetime.now()


def activate_esd(level):
    st.session_state.systems['safety_systems']['esd_level'] = level
    # Stop all pumps
    for pump in st.session_state.systems['cargo_pumps'].values():
        pump['running'] = False
        pump['flow'] = 0
    st.session_state['last_update'] = datetime.now()


# ----------------------
# DASHBOARD - TABS
# ----------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Dashboard", "Cargo System", "Ballast & Stability", "Power & Utilities", "Safety Systems"
])

# ----------------------
# DASHBOARD TAB
# ----------------------
with tab1:
    st.subheader("Vessel Overview")
    vs = st.session_state.systems['vessel_status']
    st.metric("Heel", f"{vs['heel']}°")
    st.metric("Trim", f"{vs['trim']}°")
    st.metric("Draft Fore", f"{vs['draft_fore']} m")
    st.metric("Draft Aft", f"{vs['draft_aft']} m")

# ----------------------
# CARGO TAB
# ----------------------
with tab2:
    st.subheader("Cargo Tanks & Pumps")
    for tank_name, tank_data in st.session_state.systems['cargo_tanks'].items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{tank_name}** - Level: {tank_data['level']}%")
        with col2:
            valve_status = "OPEN" if tank_data['valve_open'] else "CLOSED"
            if st.button(f"{valve_status}", key=f"valve_{tank_name}"):
                toggle_valve(tank_name)

    st.subheader("Cargo Pumps")
    for pump_name in st.session_state.systems['cargo_pumps'].keys():
        col1, col2 = st.columns([3, 1])
        with col1:
            pump = st.session_state.systems['cargo_pumps'][pump_name]
            st.write(f"**{pump_name}** - Flow: {pump['flow']} m³/h - Status: {'RUNNING' if pump['running'] else 'STOPPED'}")
        with col2:
            if st.button("Toggle", key=f"pump_{pump_name}"):
                toggle_pump(pump_name)
    update_cargo_total()
    st.metric("Total Cargo Level", f"{st.session_state.systems['operations']['total_cargo']}%")

# ----------------------
# BALLAST TAB
# ----------------------
with tab3:
    st.subheader("Ballast Tanks")
    for tank_name, tank_data in st.session_state.systems['ballast_tanks'].items():
        level_percent = (tank_data['volume'] / tank_data['capacity']) * 100
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{tank_name}** - {level_percent:.1f}% ({tank_data['volume']}/{tank_data['capacity']} m³)")
        with col2:
            if st.button("💧 IN", key=f"in_{tank_name}"):
                ballast_in(tank_name)
        with col3:
            if st.button("🚰 OUT", key=f"out_{tank_name}"):
                ballast_out(tank_name)

# ----------------------
# POWER & UTILITIES TAB
# ----------------------
with tab4:
    st.subheader("Boiler & IGS")
    igs = st.session_state.systems['safety_systems']
    st.metric("IGS Pressure", f"{igs['igs_pressure']} bar")
    st.metric("IGS O2 Content", f"{igs['igs_o2']}%")
    if st.button("Start Boiler"):
        st.success("Boiler started!")

# ----------------------
# SAFETY TAB
# ----------------------
with tab5:
    st.subheader("ESD System")
    for i, level in enumerate([1, 2, 3], start=1):
        if st.button(f"Activate ESD Level {level}", key=f"esd_{level}"):
            activate_esd(level)
    st.metric("Current ESD Level", f"{st.session_state.systems['safety_systems']['esd_level']}")
