# app.py - INTERACTIVE FPSO SIMULATOR
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

st.set_page_config(page_title="FPSO Simulator", layout="wide")

# -------------------------
# Initialize systems state
# -------------------------
if 'systems' not in st.session_state:
    st.session_state.systems = {
        # Cargo Tanks
        'cargo_tanks': {f'TANK_{i+1}': {'level': np.random.randint(50, 95), 'valve_open': False, 'temperature': 45+np.random.rand()*5} for i in range(6)},
        'slop_tanks': {f'SLOP_{i+1}': {'level': np.random.randint(30, 80), 'valve_open': False} for i in range(2)},
        # Ballast Tanks
        'ballast_tanks': {f'BALLAST_{i+1}': {'volume': np.random.randint(1000, 4000), 'capacity': 5000, 'valve_open': False} for i in range(6)},
        # Pumps
        'cargo_pumps': {f'CARGO_PUMP_{i+1}': {'running': False, 'flow':0, 'vibration': np.random.rand()*2, 'temperature': 60+np.random.rand()*5} for i in range(2)},
        'stripping_pump': {'running': False, 'flow':0, 'vibration':1.2, 'temperature':55},
        # Ballast Pumps
        'ballast_pumps': {f'BALLAST_PUMP_{i+1}': {'running': False, 'flow':0, 'vibration': np.random.rand()*2} for i in range(2)},
        # DG and Boiler
        'DG': {'running': False, 'load': 0},
        'Boiler': {'running': False, 'pressure': 8.0, 'temperature': 280, 'water_level': 80},
        'IGS': {'running': False, 'pressure': 0.8, 'O2': 2.5},
        # Vessel Status
        'vessel': {'heel': 2.0, 'trim': 0.5, 'draft_fore':18.0, 'draft_aft':19.0, 'wind_dir': 45, 'wind_speed': 8.0},
        # Operations
        'total_cargo': sum([tank['level'] for tank in [{'level': v['level']} for v in [{'level':v['level']} for v in st.session_state.systems['cargo_tanks'].values()]]] ),
        'alerts': []
    }
    st.session_state.last_update = datetime.now()

# -------------------------
# Utility Functions
# -------------------------
def toggle_valve(system, tank):
    st.session_state.systems[system][tank]['valve_open'] = not st.session_state.systems[system][tank]['valve_open']

def toggle_pump(pump_name, pump_type='cargo_pumps'):
    pump = st.session_state.systems[pump_type][pump_name]
    pump['running'] = not pump['running']
    pump['flow'] = 800 if pump['running'] else 0

def toggle_boiler():
    st.session_state.systems['Boiler']['running'] = not st.session_state.systems['Boiler']['running']

def toggle_DG():
    st.session_state.systems['DG']['running'] = not st.session_state.systems['DG']['running']
    st.session_state.systems['DG']['load'] = 50 if st.session_state.systems['DG']['running'] else 0

def toggle_IGS():
    st.session_state.systems['IGS']['running'] = not st.session_state.systems['IGS']['running']

def vessel_alerts():
    alerts = []
    heel = st.session_state.systems['vessel']['heel']
    if abs(heel) > 5:
        alerts.append(f"⚠️ Heel is high: {heel}°")
    return alerts

# -------------------------
# Layout
# -------------------------
st.title("⚓ FPSO INTERACTIVE SIMULATOR")

tabs = st.tabs(["Dashboard","Cargo & Pumps","Ballast & Stability","Power & Utilities","Safety & Alerts"])

# -------------------------
# Dashboard
# -------------------------
with tabs[0]:
    st.header("📊 Vessel Status")
    v = st.session_state.systems['vessel']
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Heel (°)", v['heel'])
    col2.metric("Trim (°)", v['trim'])
    col3.metric("Draft Fore (m)", v['draft_fore'])
    col4.metric("Draft Aft (m)", v['draft_aft'])
    
    # Wind / Orientation
    st.subheader("🌬️ Wind & Heading")
    st.write(f"Wind Speed: {v['wind_speed']} m/s, Direction: {v['wind_dir']}°")
    
    # Alerts
    alerts = vessel_alerts()
    if alerts:
        for a in alerts:
            st.warning(a)

# -------------------------
# Cargo & Pumps
# -------------------------
with tabs[1]:
    st.header("🛢️ Cargo Tanks")
    for tank_name, tank in st.session_state.systems['cargo_tanks'].items():
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            st.write(f"**{tank_name}** Level: {tank['level']}% Temp: {tank['temperature']}°C")
        with col2:
            if st.button(f"{'OPEN' if not tank['valve_open'] else 'CLOSE'} Valve", key=f"valve_{tank_name}"):
                toggle_valve('cargo_tanks', tank_name)
        with col3:
            tank['level'] = st.slider("Level", 0, 100, tank['level'], key=f"level_{tank_name}")

    st.header("⚙️ Cargo Pumps")
    for pump_name, pump in st.session_state.systems['cargo_pumps'].items():
        col1, col2 = st.columns([2,1])
        with col1:
            st.write(f"**{pump_name}** Status: {'RUNNING' if pump['running'] else 'STOPPED'} Flow: {pump['flow']} m³/h Vib: {pump['vibration']:.2f} mm/s Temp: {pump['temperature']:.1f}°C")
        with col2:
            if st.button(f"{'STOP' if pump['running'] else 'START'}", key=f"pump_{pump_name}"):
                toggle_pump(pump_name)

# -------------------------
# Ballast & Stability
# -------------------------
with tabs[2]:
    st.header("🌊 Ballast Tanks")
    for tank_name, tank in st.session_state.systems['ballast_tanks'].items():
        col1, col2 = st.columns([3,1])
        with col1:
            st.write(f"**{tank_name}** Volume: {tank['volume']}/{tank['capacity']} m³ ({tank['volume']/tank['capacity']*100:.1f}%)")
        with col2:
            if st.button(f"💧/🚰", key=f"ballast_{tank_name}"):
                tank['volume'] += 500
                if tank['volume']>tank['capacity']: tank['volume']=tank['capacity']

    st.subheader("⚖️ Stability Chart")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[-10,10,10,-10,-10], y=[0,0,5,5,0], fill='toself', fillcolor='lightgray'))
    heel = st.session_state.systems['vessel']['heel']
    water_y = [2+heel*0.2,2-heel*0.2]
    fig.add_trace(go.Scatter(x=[-10,10], y=water_y, line=dict(color='blue', width=3)))
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Power & Utilities
# -------------------------
with tabs[3]:
    st.header("⚡ Generators & Utilities")
    DG = st.session_state.systems['DG']
    Boiler = st.session_state.systems['Boiler']
    IGS = st.session_state.systems['IGS']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("DG Status", "RUNNING" if DG['running'] else "STOPPED")
        if st.button("Toggle DG"):
            toggle_DG()
        st.metric("Load (%)", DG['load'])
    with col2:
        st.metric("Boiler Status", "RUNNING" if Boiler['running'] else "STOPPED")
        if st.button("Toggle Boiler"):
            toggle_boiler()
        st.metric("Pressure (bar)", Boiler['pressure'])
        st.metric("Temperature (°C)", Boiler['temperature'])
    with col3:
        st.metric("IGS Status", "RUNNING" if IGS['running'] else "STOPPED")
        if st.button("Toggle IGS"):
            toggle_IGS()
        st.metric("Pressure (bar)", IGS['pressure'])
        st.metric("O2 (%)", IGS['O2'])

# -------------------------
# Safety & Alerts
# -------------------------
with tabs[4]:
    st.header("🚨 Safety Alerts")
    if st.session_state.systems['alerts']:
        for alert in st.session_state.systems['alerts']:
            st.warning(alert)
    else:
        st.success("All systems normal.")

