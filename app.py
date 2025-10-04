# app.py - FPSO SPIRIT Simulator v1.0
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ------------------------------
# Инициализация систем
# ------------------------------
if 'systems' not in st.session_state:
    st.session_state.systems = {
        'cargo_tanks': {
            f'TANK_{i+1}': {'level': np.random.randint(50, 95), 'valve_open': False, 'temperature': 45.0 + i, 'pressure': 0.02 + 0.01*i} for i in range(6)
        },
        'ballast_tanks': {
            'BALLAST_1P': {'volume': 2000, 'capacity': 5000},
            'BALLAST_1S': {'volume': 3000, 'capacity': 5000},
            'BALLAST_2P': {'volume': 1500, 'capacity': 5000},
            'BALLAST_2S': {'volume': 3500, 'capacity': 5000},
            'BALLAST_F': {'volume': 1200, 'capacity': 3000},
            'BALLAST_A': {'volume': 1800, 'capacity': 3000},
        },
        'cargo_pumps': {
            'CARGO_PUMP_1': {'running': False, 'flow': 0, 'vibration': 2.0},
            'CARGO_PUMP_2': {'running': False, 'flow': 0, 'vibration': 1.8},
            'STRIPPING_PUMP': {'running': False, 'flow': 0, 'vibration': 1.2},
        },
        'dg_generators': {
            f'DG_{i+1}': {'running': False, 'power_output': 0, 'vibration': 1.5} for i in range(2)
        },
        'vessel_status': {'heel': 2.5, 'trim': 0.8, 'draft_fore': 18.2, 'draft_aft': 19.0},
        'safety_systems': {'esd_level': 0, 'igs_pressure': 0.8, 'igs_o2': 2.5, 'fire_alarms': [], 'gas_alarms': []},
        'boiler': {'running': False, 'steam_pressure': 8.2, 'water_level': 85, 'temperature': 285, 'fuel_pressure': 4.5},
        'operations': {'total_cargo': 0, 'export_flow': 0, 'operational_mode': 'NORMAL'},
        'last_update': datetime.now()
    }

# ------------------------------
# Вычисление суммарного груза
# ------------------------------
st.session_state.systems['operations']['total_cargo'] = sum(
    tank['level'] for tank in st.session_state.systems['cargo_tanks'].values()
)

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="FPSO SPIRIT Simulator", layout="wide")

st.title("⚓ FPSO SPIRIT - Simulator")

# ------------------------------
# Таблицы Cargo и Ballast
# ------------------------------
st.header("🛢 Cargo Tanks")
cols = st.columns(3)
for i, (tank_name, tank_data) in enumerate(st.session_state.systems['cargo_tanks'].items()):
    with cols[i % 3]:
        st.metric(tank_name, f"{tank_data['level']}%")
        valve_status = "OPEN" if tank_data['valve_open'] else "CLOSED"
        if st.button(f"{tank_name} Valve: {valve_status}", key=f"valve_{tank_name}"):
            tank_data['valve_open'] = not tank_data['valve_open']
            st.experimental_rerun()

st.header("🌊 Ballast Tanks")
cols = st.columns(3)
for i, (tank_name, tank_data) in enumerate(st.session_state.systems['ballast_tanks'].items()):
    with cols[i % 3]:
        level_percent = (tank_data['volume'] / tank_data['capacity']) * 100
        st.metric(tank_name, f"{level_percent:.1f}% ({tank_data['volume']}/{tank_data['capacity']} m³)")
        if st.button(f"Fill {tank_name}", key=f"fill_{tank_name}"):
            tank_data['volume'] = min(tank_data['capacity'], tank_data['volume'] + 500)
            st.experimental_rerun()
        if st.button(f"Drain {tank_name}", key=f"drain_{tank_name}"):
            tank_data['volume'] = max(0, tank_data['volume'] - 500)
            st.experimental_rerun()

# ------------------------------
# Pump Control
# ------------------------------
st.header("⚙ Cargo Pumps")
cols = st.columns(3)
for i, (pump_name, pump_data) in enumerate(st.session_state.systems['cargo_pumps'].items()):
    with cols[i % 3]:
        status = "RUNNING" if pump_data['running'] else "STOPPED"
        st.metric(pump_name, status)
        if st.button(f"Toggle {pump_name}", key=f"pump_{pump_name}"):
            pump_data['running'] = not pump_data['running']
            pump_data['flow'] = 800 if pump_data['running'] else 0
            st.experimental_rerun()

# ------------------------------
# DG Generators
# ------------------------------
st.header("⚡ DG Generators")
cols = st.columns(2)
for i, (dg_name, dg_data) in enumerate(st.session_state.systems['dg_generators'].items()):
    with cols[i % 2]:
        status = "RUNNING" if dg_data['running'] else "STOPPED"
        st.metric(dg_name, status)
        if st.button(f"Toggle {dg_name}", key=f"dg_{dg_name}"):
            dg_data['running'] = not dg_data['running']
            st.experimental_rerun()

# ------------------------------
# IGS & Boiler
# ------------------------------
st.header("💨 IGS System")
igs = st.session_state.systems['safety_systems']
st.metric("IGS Pressure", f"{igs['igs_pressure']} bar")
st.metric("O2 Content", f"{igs['igs_o2']}%")
st.slider("Set IGS Pressure", 0.0, 2.0, igs['igs_pressure'], 0.1, key="igs_slider")

st.header("🔥 Boiler")
boiler = st.session_state.systems['boiler']
status = "RUNNING" if boiler['running'] else "STOPPED"
st.metric("Boiler Status", status)
if st.button("Toggle Boiler"):
    boiler['running'] = not boiler['running']
    st.experimental_rerun()

# ------------------------------
# Vessel Stability
# ------------------------------
st.header("⚓ Vessel Stability")
vessel = st.session_state.systems['vessel_status']
fig = go.Figure()
fig.add_trace(go.Bar(
    x=list(st.session_state.systems['cargo_tanks'].keys()),
    y=[t['level'] for t in st.session_state.systems['cargo_tanks'].values()],
    name="Cargo Level (%)"
))
fig.add_trace(go.Bar(
    x=list(st.session_state.systems['ballast_tanks'].keys()),
    y=[(t['volume']/t['capacity']*100) for t in st.session_state.systems['ballast_tanks'].values()],
    name="Ballast Level (%)"
))
fig.update_layout(barmode='group', title="Tank Levels")
st.plotly_chart(fig, use_container_width=True)
