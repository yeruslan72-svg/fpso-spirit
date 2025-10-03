import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
import random

# =========================
# REAL FPSO CONFIGURATION
# =========================
class FPSOConfig:
    """Конфигурация реального FPSO"""
    
    # Насосное отделение
    CARGO_PUMPS = {
        'CargoPump_A': {'location': 'Pump Room', 'type': 'Vertical Centrifugal', 'power': 800},
        'CargoPump_B': {'location': 'Pump Room', 'type': 'Vertical Centrifugal', 'power': 800},
        'CargoPump_C': {'location': 'Pump Room', 'type': 'Vertical Centrifugal', 'power': 800},
    }
    
    BALLAST_PUMPS = {
        'BallastPump_Port': {'location': 'Pump Room', 'type': 'Vertical Centrifugal', 'power': 400},
        'BallastPump_Stbd': {'location': 'Pump Room', 'type': 'Vertical Centrifugal', 'power': 400},
    }
    
    FIRE_PUMPS = {
        'FirePump_1': {'location': 'Pump Room', 'type': 'Vertical Centrifugal', 'power': 300},
        'FirePump_2': {'location': 'Pump Room', 'type': 'Vertical Centrifugal', 'power': 300},
    }
    
    # Дизель-генераторы
    DIESEL_GENERATORS = {
        'DG1_Caterpillar': {'location': 'Second Deck', 'power': 4500, 'fuel': 'MDO'},
        'DG2_Caterpillar': {'location': 'Second Deck', 'power': 4500, 'fuel': 'MDO'},
    }
    
    # Танковая система
    CARGO_TANKS = {f'Cargo_Tank_{i}': {'capacity': 15000, 'product': 'Crude Oil'} for i in range(1, 7)}
    SLOP_TANKS = {
        'Slop_Tank_Port': {'capacity': 500, 'purpose': 'Drainage Collection'},
        'Slop_Tank_Stbd': {'capacity': 500, 'purpose': 'Drainage Collection'},
    }
    
    BALLAST_TANKS = {
        **{f'Ballast_Port_{i}': {'capacity': 800} for i in range(1, 7)},
        **{f'Ballast_Stbd_{i}': {'capacity': 800} for i in range(1, 7)},
        'Forepeak_Tank': {'capacity': 300}
    }
    
    FLOW_METERS = {
        'FlowMeter_Import': {'location': 'Turret Input', 'type': 'Yokogawa', 'range': '0-5000 m³/h'},
        'FlowMeter_Export': {'location': 'Export Line', 'type': 'Yokogawa', 'range': '0-5000 m³/h'},
    }

# =========================
# ENHANCED DATA GENERATOR
# =========================
def generate_realistic_fpso_data(cycle: int, pump_status=None, faults=None):
    if pump_status is None:
        pump_status = {"CargoPump_A": True, "CargoPump_B": True, "CargoPump_C": False}
    if faults is None:
        faults = {}

    # Базовые параметры
    time_factor = cycle * 0.1
    degradation = min(2.0, cycle * 0.002)
    
    # Симуляция режима
    is_loading = (cycle % 200) < 100
    is_exporting = not is_loading and (cycle % 200) > 150
    
    data = {
        'operation_mode': 'LOADING' if is_loading else 'EXPORTING' if is_exporting else 'IDLE',
        'cycle_duration': cycle,
        'import_flow_rate': 2500 + np.random.normal(0, 200) if is_loading else 0,
        'export_flow_rate': 0,  # скорректируем ниже
        'total_cargo_loaded': min(90000, cycle * 45),
        'total_cargo_exported': min(85000, max(0, cycle - 150) * 40),
    }
    
    # === ГРУЗОВЫЕ НАСОСЫ ===
    for pump in ["A", "B", "C"]:
        if pump_status[f"CargoPump_{pump}"]:
            data[f"CargoPump_{pump}_flow"] = 800 + np.random.normal(0, 50) if is_exporting else 0
            data[f"CargoPump_{pump}_vib"] = 1.8 + np.random.normal(0, 0.4) + degradation * 0.3
            data[f"CargoPump_{pump}_temp"] = 75 + np.random.normal(0, 5) + degradation * 8
        else:
            data[f"CargoPump_{pump}_flow"] = 0
            data[f"CargoPump_{pump}_vib"] = 0.3 + np.random.normal(0, 0.1)
            data[f"CargoPump_{pump}_temp"] = 40 + np.random.normal(0, 2)
    
    data['export_flow_rate'] = sum(data[f"CargoPump_{p}_flow"] for p in ["A", "B", "C"])
    
    # === Балластные насосы ===
    data['BallastPump_Port_flow'] = 300 + np.random.normal(0, 30)
    data['BallastPump_Stbd_flow'] = 300 + np.random.normal(0, 30)
    data['BallastPump_Port_vib'] = 1.2 + np.random.normal(0, 0.2)
    data['BallastPump_Stbd_vib'] = 1.3 + np.random.normal(0, 0.3)
    data['BallastPump_Port_temp'] = 65 + np.random.normal(0, 4)
    data['BallastPump_Stbd_temp'] = 66 + np.random.normal(0, 5)
    
    # === Дизель-генераторы ===
    data['DG1_power'] = 3500 + np.random.normal(0, 200)
    data['DG2_power'] = 3200 + np.random.normal(0, 250)
    data['DG1_vib'] = 1.4 + np.random.normal(0, 0.3) + degradation * 0.2
    data['DG2_vib'] = 1.5 + np.random.normal(0, 0.4) + degradation * 0.3
    data['DG1_temp'] = 85 + np.random.normal(0, 5) + degradation * 6
    data['DG2_temp'] = 83 + np.random.normal(0, 6) + degradation * 5
    
    # === Корпус ===
    data['heel_angle'] = 0.2 + np.sin(time_factor) * 0.8
    data['trim_angle'] = 0.3 + np.cos(time_factor) * 0.6
    data['hull_stress'] = 22 + abs(np.sin(time_factor)) * 15 + degradation * 5
    data['bending_moment'] = 1100 + np.random.normal(0, 80)
    data['shear_force'] = 750 + np.random.normal(0, 60)
    
    # === Fault Injection ===
    if faults.get("CargoPump_A_failure"):
        data['CargoPump_A_flow'] = 0
        data['CargoPump_A_vib'] = 5.0
        data['CargoPump_A_temp'] = 120
    if faults.get("DG1_overheat"):
        data['DG1_temp'] += 30
        data['DG1_power'] *= 0.5
    if faults.get("IGS_low_pressure"):
        data['IGS_main_pressure'] = 0.05
    
    return data

# =========================
# VISUALIZATIONS
# =========================
def create_operations_dashboard(data):
    fig = go.Figure()
    fig.add_trace(go.Indicator(mode="number", value=data['import_flow_rate'], title={"text": "Import Flow (m³/h)"}))
    fig.add_trace(go.Indicator(mode="number", value=data['export_flow_rate'], title={"text": "Export Flow (m³/h)"}))
    return fig

def create_pump_room_monitoring(data):
    pumps = ['CargoPump_A', 'CargoPump_B', 'CargoPump_C']
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Vibration',
        x=pumps,
        y=[data[f'{p}_vib'] for p in pumps],
        marker_color=['red' if data[f'{p}_vib'] > 2.5 else 'orange' if data[f'{p}_vib'] > 1.8 else 'green' for p in pumps],
        text=[f"{data[f'{p}_vib']:.1f}" for p in pumps],
        textposition='auto'
    ))
    fig.add_trace(go.Scatter(
        name='Temperature',
        x=pumps,
        y=[data[f'{p}_temp'] for p in pumps],
        mode='lines+markers',
        line=dict(color='orange')
    ))
    fig.update_layout(title="Pump Room Monitoring", height=400)
    return fig

def create_hull_monitoring(history):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=[d['heel_angle'] for d in history], mode="lines", name="Heel Angle"))
    fig.add_trace(go.Scatter(y=[d['trim_angle'] for d in history], mode="lines", name="Trim Angle"))
    fig.add_trace(go.Scatter(y=[d['hull_stress'] for d in history], mode="lines", name="Hull Stress"))
    fig.add_trace(go.Scatter(y=[d['bending_moment'] for d in history], mode="lines", name="Bending Moment"))
    fig.add_trace(go.Scatter(y=[d['shear_force'] for d in history], mode="lines", name="Shear Force"))
    fig.update_layout(title="⚓ Hull Stability & Structural Monitoring", xaxis_title="Cycle", height=400)
    return fig

# =========================
# MAIN APPLICATION
# =========================
def main():
    st.title("🌊 FPSO Spirit - Real-time Process Monitoring")
    st.markdown("**AVCS DNA + Fault Injection + Hull Monitoring**")
    
    if "system_data" not in st.session_state:
        st.session_state.system_data = generate_realistic_fpso_data(0)
    if "monitoring_active" not in st.session_state:
        st.session_state.monitoring_active = False
    if "cycle_count" not in st.session_state:
        st.session_state.cycle_count = 0
    if "history" not in st.session_state:
        st.session_state.history = []
    
    # === Pump Control Panel ===
    st.sidebar.header("⚙️ CCR Control Panel")
    st.sidebar.subheader("Cargo Pumps Control")
    pump_a_on = st.sidebar.checkbox("Cargo Pump A", value=True)
    pump_b_on = st.sidebar.checkbox("Cargo Pump B", value=True)
    pump_c_on = st.sidebar.checkbox("Cargo Pump C (Standby)", value=False)
    
    pump_status = {"CargoPump_A": pump_a_on, "CargoPump_B": pump_b_on, "CargoPump_C": pump_c_on}
    
    # === Fault Injection ===
    st.sidebar.subheader("🚨 Fault Injection")
    faults = {
        "CargoPump_A_failure": st.sidebar.checkbox("Failure: Cargo Pump A"),
        "CargoPump_B_failure": st.sidebar.checkbox("Failure: Cargo Pump B"),
        "CargoPump_C_failure": st.sidebar.checkbox("Failure: Cargo Pump C"),
        "DG1_overheat": st.sidebar.checkbox("Overheat: DG1"),
        "DG2_overheat": st.sidebar.checkbox("Overheat: DG2"),
        "IGS_low_pressure": st.sidebar.checkbox("Low Pressure: IGS"),
    }
    
    if st.sidebar.button("▶️ Start Monitoring"):
        st.session_state.monitoring_active = True
    if st.sidebar.button("⏸️ Stop Monitoring"):
        st.session_state.monitoring_active = False
    
    if st.session_state.monitoring_active:
        st.session_state.cycle_count += 1
        st.session_state.system_data = generate_realistic_fpso_data(
            st.session_state.cycle_count,
            pump_status=pump_status,
            faults=faults
        )
        st.session_state.history.append(st.session_state.system_data)
        if len(st.session_state.history) > 100:
            st.session_state.history.pop(0)
        st.rerun()
    
    data = st.session_state.system_data
    
    # === UI ===
    st.subheader("📊 Operations Overview")
    st.plotly_chart(create_operations_dashboard(data), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏭 Pump Room Monitoring")
        st.plotly_chart(create_pump_room_monitoring(data), use_container_width=True)
    with col2:
        st.subheader("⚡ Power Generation")
        st.metric("DG1 Power", f"{data['DG1_power']:.0f} kW")
        st.metric("DG1 Temp", f"{data['DG1_temp']:.0f}°C")
        st.metric("DG2 Power", f"{data['DG2_power']:.0f} kW")
        st.metric("DG2 Temp", f"{data['DG2_temp']:.0f}°C")
    
    st.subheader("⚓ Hull Condition")
    st.plotly_chart(create_hull_monitoring(st.session_state.history), use_container_width=True)

if __name__ == "__main__":
    main()
