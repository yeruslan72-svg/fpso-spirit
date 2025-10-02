# FPSO Spirit - Digital Soul of Floating Production
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# Page Configuration
st.set_page_config(
    page_title="FPSO Spirit",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'monitoring_active' not in st.session_state:
    st.session_state.monitoring_active = False
if 'system_data' not in st.session_state:
    st.session_state.system_data = {}
if 'risk_level' not in st.session_state:
    st.session_state.risk_level = "LOW"

# System Configuration
class FPSOIndustrialConfig:
    """FPSO System Configuration"""
    
    BALLAST_SYSTEM = {
        'BALLAST_PUMP_VIB': 'Ballast Pump - Vibration',
        'BALLAST_PUMP_TEMP': 'Ballast Pump - Temperature',
        'BALLAST_VALVE_POSITION': 'Ballast Valve Position',
        'BALLAST_TANK_LEVEL': 'Ballast Tank Level',
        'BALLAST_FLOW_RATE': 'Ballast Flow Rate',
        'BALLAST_PRESSURE': 'Ballast System Pressure',
        'TRIM_ANGLE': 'Vessel Trim Angle',
        'HEEL_ANGLE': 'Vessel Heel Angle',
        'DRAFT_FWD': 'Forward Draft',
        'DRAFT_AFT': 'Aft Draft'
    }

class BallastSystemMonitor:
    """Ballast System Monitor"""
    
    def __init__(self):
        self.stability_limits = {
            'trim_angle': {'normal': 1.0, 'warning': 2.0, 'critical': 3.0},
            'heel_angle': {'normal': 0.5, 'warning': 1.5, 'critical': 2.5},
        }

def generate_sensor_data():
    """Generate realistic sensor data"""
    return {
        'trim_angle': 0.5 + np.random.normal(0, 0.2),
        'heel_angle': 0.3 + np.random.normal(0, 0.1),
        'ballast_pressure': 3.2 + np.random.normal(0, 0.3),
        'ballast_pump_temp': 72 + np.random.normal(0, 2),
        'fire_pressure': 7.5 + np.random.normal(0, 0.5),
        'fire_pump_temp': 78 + np.random.normal(0, 3),
        'cargo_temp_1': 42 + np.random.normal(0, 1),
        'cargo_temp_2': 43 + np.random.normal(0, 1),
        'cargo_temp_3': 41 + np.random.normal(0, 1),
        'heating_pump_temp': 85 + np.random.normal(0, 2)
    }

def simulate_monitoring_cycle():
    """Simulate one monitoring cycle"""
    if st.session_state.monitoring_active:
        # Generate new data
        st.session_state.system_data = generate_sensor_data()
        
        # Calculate risk level based on sensor data
        risk_score = 0
        data = st.session_state.system_data
        
        if abs(data['trim_angle']) > 2.0:
            risk_score += 30
        if abs(data['heel_angle']) > 1.0:
            risk_score += 25
        if data['ballast_pressure'] < 2.5:
            risk_score += 20
        if data['fire_pressure'] < 6.0:
            risk_score += 25
            
        # Determine risk level
        if risk_score > 50:
            st.session_state.risk_level = "HIGH"
        elif risk_score > 25:
            st.session_state.risk_level = "MEDIUM"
        else:
            st.session_state.risk_level = "LOW"

def display_ballast_monitoring():
    """Ballast System Monitoring Interface"""
    st.subheader("⚖️ Ballast System & Stability Monitoring")
    
    if not st.session_state.system_data:
        st.info("Monitoring not active. Click 'Start Monitoring' to begin.")
        return
    
    data = st.session_state.system_data
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        trim_angle = data['trim_angle']
        if abs(trim_angle) > 2.0:
            st.error(f"🚨 Trim Angle\n{trim_angle:.1f}°")
        elif abs(trim_angle) > 1.0:
            st.warning(f"⚠️ Trim Angle\n{trim_angle:.1f}°")
        else:
            st.success(f"✅ Trim Angle\n{trim_angle:.1f}°")
            
    with col2:
        heel_angle = data['heel_angle']
        if abs(heel_angle) > 1.5:
            st.error(f"🚨 Heel Angle\n{heel_angle:.1f}°")
        elif abs(heel_angle) > 0.5:
            st.warning(f"⚠️ Heel Angle\n{heel_angle:.1f}°")
        else:
            st.success(f"✅ Heel Angle\n{heel_angle:.1f}°")
            
    with col3:
        ballast_pressure = data['ballast_pressure']
        if ballast_pressure < 2.0:
            st.error(f"🚨 Pressure\n{ballast_pressure:.1f} bar")
        elif ballast_pressure < 2.5:
            st.warning(f"⚠️ Pressure\n{ballast_pressure:.1f} bar")
        else:
            st.success(f"✅ Pressure\n{ballast_pressure:.1f} bar")
            
    with col4:
        ballast_pump_temp = data['ballast_pump_temp']
        if ballast_pump_temp > 100:
            st.error(f"🚨 Pump Temp\n{ballast_pump_temp:.1f}°C")
        elif ballast_pump_temp > 85:
            st.warning(f"⚠️ Pump Temp\n{ballast_pump_temp:.1f}°C")
        else:
            st.success(f"✅ Pump Temp\n{ballast_pump_temp:.1f}°C")

def display_fire_system_monitoring():
    """Fire System Monitoring Interface"""
    st.subheader("🔥 Fire Fighting System Monitoring")
    
    if not st.session_state.system_data:
        return
    
    data = st.session_state.system_data
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fire_pressure = data['fire_pressure']
        if fire_pressure < 4.0:
            st.error(f"🚨 Fire Main\n{fire_pressure:.1f} bar")
        elif fire_pressure < 6.0:
            st.warning(f"⚠️ Fire Main\n{fire_pressure:.1f} bar")
        else:
            st.success(f"✅ Fire Main\n{fire_pressure:.1f} bar")
            
    with col2:
        fire_pump_temp = data['fire_pump_temp']
        if fire_pump_temp > 105:
            st.error(f"🚨 Fire Pump\n{fire_pump_temp:.1f}°C")
        elif fire_pump_temp > 90:
            st.warning(f"⚠️ Fire Pump\n{fire_pump_temp:.1f}°C")
        else:
            st.success(f"✅ Fire Pump\n{fire_pump_temp:.1f}°C")
            
    with col3:
        status = "READY" if fire_pressure > 6.0 else "CHECK"
        st.success(f"✅ Deluge System\n{status}")
            
    with col4:
        status = "READY" if fire_pump_temp < 90 else "STANDBY"
        st.warning(f"⚠️ Foam System\n{status}")

def display_cargo_heating_monitoring():
    """Cargo Heating Monitoring Interface"""
    st.subheader("🌡️ Cargo Tank Heating System")
    
    if not st.session_state.system_data:
        return
    
    data = st.session_state.system_data
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cargo_temp_1 = data['cargo_temp_1']
        st.metric("Tank 1 Temperature", f"{cargo_temp_1:.1f}°C", f"{np.random.choice(['+', '-'])}{np.random.uniform(0.1, 0.5):.1f}")
        
    with col2:
        cargo_temp_2 = data['cargo_temp_2']
        st.metric("Tank 2 Temperature", f"{cargo_temp_2:.1f}°C", f"{np.random.choice(['+', '-'])}{np.random.uniform(0.1, 0.5):.1f}")
        
    with col3:
        cargo_temp_3 = data['cargo_temp_3']
        st.metric("Tank 3 Temperature", f"{cargo_temp_3:.1f}°C", f"{np.random.choice(['+', '-'])}{np.random.uniform(0.1, 0.5):.1f}")
        
    with col4:
        heating_pump_temp = data['heating_pump_temp']
        if heating_pump_temp > 100:
            st.error(f"🚨 Heating Pump\n{heating_pump_temp:.1f}°C")
        elif heating_pump_temp > 90:
            st.warning(f"⚠️ Heating Pump\n{heating_pump_temp:.1f}°C")
        else:
            st.success(f"✅ Heating Pump\n{heating_pump_temp:.1f}°C")

# Main Application
def main():
    # Main Title
    st.title("🌊 FPSO Spirit - Digital Soul of Floating Production")
    st.markdown("### *Where Engineering Meets Consciousness*")

    # Simulate monitoring cycle
    simulate_monitoring_cycle()

    # System Status
    if st.session_state.monitoring_active:
        st.success("🚀 FPSO Spirit - ACTIVE MONITORING")
        # Auto-refresh
        time.sleep(2)
        st.rerun()
    else:
        st.info("🟡 FPSO Spirit - READY FOR ACTIVATION")

    # Dashboard Columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        status = "ACTIVE" if st.session_state.monitoring_active else "STANDBY"
        color = "🟢" if st.session_state.monitoring_active else "🟡"
        st.metric("System Status", f"{color} {status}")
        
    with col2:
        risk_color = "🔴" if st.session_state.risk_level == "HIGH" else "🟡" if st.session_state.risk_level == "MEDIUM" else "🟢"
        st.metric("Risk Level", f"{risk_color} {st.session_state.risk_level}")

    with col3:
        systems = "6/8" if st.session_state.monitoring_active else "0/8"
        st.metric("Systems Active", systems)

    with col4:
        if st.session_state.monitoring_active:
            st.metric("Data Cycles", f"#{np.random.randint(1, 100)}")
        else:
            st.metric("Data Cycles", "0")

    # System Overview
    st.subheader("🎯 System Consciousness States")

    systems = {
        "Ballast System": {"state": "MINDFUL", "awareness": 96},
        "IGS System": {"state": "VIGILANT", "awareness": 98}, 
        "Fire System": {"state": "ALERT", "awareness": 95},
        "Power System": {"state": "BALANCED", "awareness": 92},
        "Production": {"state": "FLOWING", "awareness": 94},
        "Cargo Heating": {"state": "TEMPERATE", "awareness": 91}
    }

    for system, data in systems.items():
        st.progress(data["awareness"]/100, f"{system}: {data['state']} ({data['awareness']}%)")

    # Systems Monitoring
    display_ballast_monitoring()
    display_fire_system_monitoring()
    display_cargo_heating_monitoring()

    # Footer
    st.markdown("---")
    st.caption(f"FPSO Spirit v1.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Breathing consciousness into steel")

    # Sidebar
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        if not st.session_state.monitoring_active:
            if st.button("⚡ Start Monitoring", type="primary", use_container_width=True):
                st.session_state.monitoring_active = True
                st.session_state.system_data = generate_sensor_data()
                st.rerun()
        else:
            if st.button("🛑 Stop Monitoring", type="secondary", use_container_width=True):
                st.session_state.monitoring_active = False
                st.rerun()
        
        st.markdown("---")
        st.subheader("System Info")
        st.write(f"**Status:** {'ACTIVE' if st.session_state.monitoring_active else 'STANDBY'}")
        st.write(f"**Risk Level:** {st.session_state.risk_level}")
        st.write(f"**Last Update:** {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
