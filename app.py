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
if 'emergency_stop' not in st.session_state:
    st.session_state.emergency_stop = False
if 'system_data' not in st.session_state:
    st.session_state.system_data = {}
if 'risk_level' not in st.session_state:
    st.session_state.risk_level = "LOW"
if 'cycle_count' not in st.session_state:
    st.session_state.cycle_count = 0
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

def generate_sensor_data():
    """Generate realistic sensor data"""
    return {
        'trim_angle': max(0.1, 0.5 + np.random.normal(0, 0.3)),
        'heel_angle': max(0.1, 0.3 + np.random.normal(0, 0.2)),
        'ballast_pressure': max(0.5, 3.2 + np.random.normal(0, 0.5)),
        'ballast_pump_temp': max(20, 72 + np.random.normal(0, 4)),
        'fire_pressure': max(1.0, 7.5 + np.random.normal(0, 0.8)),
        'fire_pump_temp': max(20, 78 + np.random.normal(0, 5)),
        'cargo_temp_1': max(10, 42 + np.random.normal(0, 3)),
        'cargo_temp_2': max(10, 43 + np.random.normal(0, 3)),
        'cargo_temp_3': max(10, 41 + np.random.normal(0, 3)),
        'heating_pump_temp': max(20, 85 + np.random.normal(0, 6))
    }

def calculate_risk_level(data):
    """Calculate risk level based on sensor data"""
    if not data:
        return "LOW"
    
    risk_score = 0
    
    # Ballast system checks
    if abs(data['trim_angle']) > 2.0:
        risk_score += 30
    elif abs(data['trim_angle']) > 1.0:
        risk_score += 15
        
    if abs(data['heel_angle']) > 1.5:
        risk_score += 25
    elif abs(data['heel_angle']) > 0.5:
        risk_score += 12
        
    if data['ballast_pressure'] < 2.0:
        risk_score += 40
    elif data['ballast_pressure'] < 2.5:
        risk_score += 20
        
    if data['ballast_pump_temp'] > 100:
        risk_score += 35
    elif data['ballast_pump_temp'] > 85:
        risk_score += 18
        
    # Fire system checks
    if data['fire_pressure'] < 4.0:
        risk_score += 45
    elif data['fire_pressure'] < 6.0:
        risk_score += 22
        
    if data['fire_pump_temp'] > 105:
        risk_score += 30
    elif data['fire_pump_temp'] > 90:
        risk_score += 15
        
    # Cargo system checks
    avg_cargo_temp = np.mean([data['cargo_temp_1'], data['cargo_temp_2'], data['cargo_temp_3']])
    if avg_cargo_temp > 55 or avg_cargo_temp < 30:
        risk_score += 20
        
    if data['heating_pump_temp'] > 100:
        risk_score += 25
    elif data['heating_pump_temp'] > 90:
        risk_score += 12
    
    # Determine risk level
    if risk_score >= 80:
        return "CRITICAL"
    elif risk_score >= 50:
        return "HIGH"
    elif risk_score >= 25:
        return "MEDIUM"
    else:
        return "LOW"

def display_ballast_monitoring():
    """Ballast System Monitoring Interface"""
    st.subheader("⚖️ Ballast System & Stability Monitoring")
    
    if not st.session_state.system_data:
        st.info("📊 Monitoring not active. Click 'Start Monitoring' to begin.")
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
        status = "READY" if fire_pressure > 6.0 and fire_pump_temp < 90 else "CHECK"
        color = "✅" if status == "READY" else "⚠️"
        st.metric("Deluge System", f"{color} {status}")
            
    with col4:
        status = "ACTIVE" if fire_pressure > 5.0 else "STANDBY"
        color = "✅" if status == "ACTIVE" else "🟡"
        st.metric("Foam System", f"{color} {status}")

def display_cargo_heating_monitoring():
    """Cargo Heating Monitoring Interface"""
    st.subheader("🌡️ Cargo Tank Heating System")
    
    if not st.session_state.system_data:
        return
    
    data = st.session_state.system_data
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cargo_temp_1 = data['cargo_temp_1']
        trend = np.random.choice(['+', '-']) + f"{np.random.uniform(0.1, 0.8):.1f}"
        st.metric("Tank 1", f"{cargo_temp_1:.1f}°C", trend)
        
    with col2:
        cargo_temp_2 = data['cargo_temp_2']
        trend = np.random.choice(['+', '-']) + f"{np.random.uniform(0.1, 0.8):.1f}"
        st.metric("Tank 2", f"{cargo_temp_2:.1f}°C", trend)
        
    with col3:
        cargo_temp_3 = data['cargo_temp_3']
        trend = np.random.choice(['+', '-']) + f"{np.random.uniform(0.1, 0.8):.1f}"
        st.metric("Tank 3", f"{cargo_temp_3:.1f}°C", trend)
        
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

    # Auto-refresh logic (only if not in emergency stop)
    if st.session_state.monitoring_active and not st.session_state.emergency_stop:
        current_time = datetime.now()
        time_diff = (current_time - st.session_state.last_update).total_seconds()
        
        # Update data every 3 seconds
        if time_diff >= 3:
            st.session_state.system_data = generate_sensor_data()
            st.session_state.risk_level = calculate_risk_level(st.session_state.system_data)
            st.session_state.cycle_count += 1
            st.session_state.last_update = current_time
            
            # Use Streamlit's built-in auto-refresh
            st.rerun()

    # System Status with Emergency Stop indicator
    if st.session_state.emergency_stop:
        st.error("🚨🚨🚨 EMERGENCY STOP ACTIVATED - ALL SYSTEMS HALTED 🚨🚨🚨")
        st.warning("⚠️ Acknowledge emergency stop to resume operations")
        
    elif st.session_state.monitoring_active:
        st.success(f"🚀 LIVE MONITORING - Cycle #{st.session_state.cycle_count}")
        
        # Animation indicator
        with st.empty():
            animation_frames = ["🌊", "🌀", "⚡", "✨"]
            current_frame = animation_frames[st.session_state.cycle_count % len(animation_frames)]
            st.markdown(f"### {current_frame} **REAL-TIME DATA STREAMING** {current_frame}")
            
        # Next update countdown
        next_update = 3 - (datetime.now() - st.session_state.last_update).total_seconds()
        st.info(f"🔄 Next update in: {max(0, int(next_update))} seconds")
        
    else:
        st.info("🟡 SYSTEM READY - Click 'Start Monitoring' to begin live data streaming")

    # Dashboard Columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.session_state.emergency_stop:
            st.error("🚨 EMERGENCY STOP")
        else:
            status = "ACTIVE" if st.session_state.monitoring_active else "STANDBY"
            color = "🟢" if st.session_state.monitoring_active else "🟡"
            st.metric("System Status", f"{color} {status}")
        
    with col2:
        risk_color = {
            "CRITICAL": "🔴",
            "HIGH": "🟠", 
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }.get(st.session_state.risk_level, "🟢")
        st.metric("Risk Level", f"{risk_color} {st.session_state.risk_level}")

    with col3:
        if st.session_state.emergency_stop:
            st.error("SYSTEMS OFFLINE")
        else:
            systems = "6/8" if st.session_state.monitoring_active else "0/8"
            st.metric("Active Systems", systems)

    with col4:
        st.metric("Data Cycles", st.session_state.cycle_count)

    # System Overview with animated progress bars (only if not emergency stop)
    st.subheader("🎯 System Consciousness States")

    if st.session_state.emergency_stop:
        st.error("🔴 ALL SYSTEMS OFFLINE - EMERGENCY STOP ACTIVE")
        for system in ["Ballast System", "IGS System", "Fire System", "Power System", "Production", "Cargo Heating"]:
            st.progress(0, f"{system}: OFFLINE (0%)")
    else:
        base_awareness = {
            "Ballast System": 96,
            "IGS System": 98, 
            "Fire System": 95,
            "Power System": 92,
            "Production": 94,
            "Cargo Heating": 91
        }

        # Adjust awareness based on risk level and add animation
        risk_modifier = {
            "CRITICAL": -20,
            "HIGH": -10,
            "MEDIUM": -5,
            "LOW": 0
        }.get(st.session_state.risk_level, 0)

        # Add subtle animation to awareness values
        animation_offset = np.sin(st.session_state.cycle_count * 0.5) * 2 if st.session_state.monitoring_active else 0

        for system, awareness in base_awareness.items():
            adjusted_awareness = max(50, min(100, awareness + risk_modifier + animation_offset))
            state = "ALERT" if risk_modifier < -5 else "NORMAL"
            
            # Animated progress bar
            progress_html = f"""
            <div style="background: #262730; padding: 10px; border-radius: 10px; margin: 5px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>{system}</span>
                    <span>{state} ({adjusted_awareness:.0f}%)</span>
                </div>
                <div style="background: #1E88E5; height: 20px; border-radius: 10px; width: {adjusted_awareness}%; 
                         transition: width 0.5s ease-in-out; animation: pulse 2s infinite;">
                </div>
            </div>
            <style>
            @keyframes pulse {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.7; }}
                100% {{ opacity: 1; }}
            }}
            </style>
            """
            st.markdown(progress_html, unsafe_allow_html=True)

    # Systems Monitoring (only if not emergency stop)
    if not st.session_state.emergency_stop:
        display_ballast_monitoring()
        display_fire_system_monitoring()
        display_cargo_heating_monitoring()

        # Manual refresh option
        if st.session_state.monitoring_active:
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🔄 Force Update", type="secondary"):
                    st.session_state.system_data = generate_sensor_data()
                    st.session_state.risk_level = calculate_risk_level(st.session_state.system_data)
                    st.session_state.cycle_count += 1
                    st.session_state.last_update = datetime.now()
                    st.rerun()

    # Footer
    st.markdown("---")
    st.caption(f"FPSO Spirit v1.3 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Breathing consciousness into steel")

    # Sidebar with Emergency Stop
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        if st.session_state.emergency_stop:
            # Emergency Stop Active - Show acknowledge button
            st.error("🚨 EMERGENCY STOP ACTIVE")
            if st.button("✅ Acknowledge & Reset", type="primary", use_container_width=True):
                st.session_state.emergency_stop = False
                st.session_state.monitoring_active = False
                st.rerun()
                
        else:
            # Normal operation
            col1, col2 = st.columns(2)
            
            with col1:
                if not st.session_state.monitoring_active:
                    if st.button("⚡ Start", type="primary", use_container_width=True):
                        st.session_state.monitoring_active = True
                        st.session_state.system_data = generate_sensor_data()
                        st.session_state.risk_level = calculate_risk_level(st.session_state.system_data)
                        st.session_state.cycle_count = 1
                        st.session_state.last_update = datetime.now()
                        st.rerun()
                else:
                    if st.button("⏸️ Stop", type="secondary", use_container_width=True):
                        st.session_state.monitoring_active = False
                        st.rerun()
            
            with col2:
                if st.button("🛑 E-Stop", type="secondary", use_container_width=True, 
                           help="Immediate system shutdown"):
                    st.session_state.emergency_stop = True
                    st.session_state.monitoring_active = False
                    st.rerun()
        
        st.markdown("---")
        st.subheader("System Status")
        
        if st.session_state.emergency_stop:
            st.error("**Status:** EMERGENCY STOP")
            st.error("**All Systems:** OFFLINE")
        else:
            st.write(f"**Monitoring:** {'🟢 ACTIVE' if st.session_state.monitoring_active else '🟡 STANDBY'}")
            st.write(f"**Risk Level:** {st.session_state.risk_level}")
        
        st.write(f"**Cycles:** {st.session_state.cycle_count}")
        st.write(f"**Last Update:** {st.session_state.last_update.strftime('%H:%M:%S')}")
        
        st.markdown("---")
        st.subheader("Quick Actions")
        
        if not st.session_state.emergency_stop:
            if st.button("🎲 Simulate Data", use_container_width=True):
                st.session_state.system_data = generate_sensor_data()
                st.session_state.risk_level = calculate_risk_level(st.session_state.system_data)
                if st.session_state.monitoring_active:
                    st.session_state.cycle_count += 1
                st.rerun()

if __name__ == "__main__":
    main()
