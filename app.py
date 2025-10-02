# FPSO Spirit - Digital Soul of Floating Production
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="FPSO Spirit",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# System Configuration
class FPSOIndustrialConfig:
    """FPSO System Configuration"""
    
    # BALLAST SYSTEM
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
    
    # FIRE FIGHTING SYSTEM
    FIRE_SYSTEM = {
        'FIRE_PUMP_VIB': 'Fire Pump - Vibration',
        'FIRE_PUMP_TEMP': 'Fire Pump - Temperature',
        'FIRE_MAIN_PRESSURE': 'Fire Main Pressure',
        'DELUG_SYSTEM_STATUS': 'Deluge System Status',
        'FOAM_SYSTEM_STATUS': 'Foam System Status',
        'WATER_MIST_STATUS': 'Water Mist System Status',
        'FIRE_DETECTOR_CARGO': 'Fire Detector - Cargo Area',
        'FIRE_DETECTOR_ENGINE': 'Fire Detector - Engine Room',
        'FIRE_DETECTOR_ACCOMM': 'Fire Detector - Accommodation'
    }
    
    # CARGO TANK HEATING
    CARGO_HEATING_SYSTEM = {
        'HEATING_PUMP_VIB': 'Heating Pump - Vibration',
        'HEATING_PUMP_TEMP': 'Heating Pump - Temperature',
        'HEATER_TEMP_IN': 'Heater Temperature - Inlet',
        'HEATER_TEMP_OUT': 'Heater Temperature - Outlet',
        'CARGO_TEMP_1': 'Cargo Temperature - Tank 1',
        'CARGO_TEMP_2': 'Cargo Temperature - Tank 2',
        'CARGO_TEMP_3': 'Cargo Temperature - Tank 3',
        'HEATING_COIL_TEMP': 'Heating Coil Temperature',
        'THERMAL_OIL_TEMP': 'Thermal Oil Temperature',
        'HEATING_FLOW_RATE': 'Heating Flow Rate'
    }

class BallastSystemMonitor:
    """Ballast System Monitor"""
    
    def __init__(self):
        self.stability_limits = {
            'trim_angle': {'normal': 1.0, 'warning': 2.0, 'critical': 3.0},
            'heel_angle': {'normal': 0.5, 'warning': 1.5, 'critical': 2.5},
            'draft_difference': {'normal': 0.3, 'warning': 0.8, 'critical': 1.5},
            'ballast_pump_temp': {'normal': 70, 'warning': 85, 'critical': 100}
        }
    
    def check_stability(self, sensor_data):
        """Check FPSO stability"""
        stability_risk = 0
        
        if abs(sensor_data['trim_angle']) > self.stability_limits['trim_angle']['critical']:
            stability_risk += 80
        elif abs(sensor_data['trim_angle']) > self.stability_limits['trim_angle']['warning']:
            stability_risk += 30
            
        if abs(sensor_data['heel_angle']) > self.stability_limits['heel_angle']['critical']:
            stability_risk += 70
        elif abs(sensor_data['heel_angle']) > self.stability_limits['heel_angle']['warning']:
            stability_risk += 25
            
        draft_diff = abs(sensor_data['draft_fwd'] - sensor_data['draft_aft'])
        if draft_diff > self.stability_limits['draft_difference']['critical']:
            stability_risk += 60
            
        return min(100, stability_risk)

class CargoHeatingMonitor:
    """Cargo Heating System Monitor"""
    
    def __init__(self):
        self.cargo_params = {
            'viscosity_temp': 45,
            'max_cargo_temp': 60,
            'min_cargo_temp': 35
        }
    
    def optimize_heating(self, sensor_data):
        """Optimize cargo heating"""
        cargo_temp = np.mean([sensor_data['cargo_temp_1'], sensor_data['cargo_temp_2'], sensor_data['cargo_temp_3']])
        
        if cargo_temp < self.cargo_params['min_cargo_temp']:
            return "INCREASE_HEATING", f"Cargo temp {cargo_temp:.1f}C below minimum"
        elif cargo_temp > self.cargo_params['max_cargo_temp']:
            return "DECREASE_HEATING", f"Cargo temp {cargo_temp:.1f}C above maximum"
        elif abs(cargo_temp - self.cargo_params['viscosity_temp']) < 2:
            return "MAINTAIN", f"Optimal cargo temp {cargo_temp:.1f}C"
        else:
            return "ADJUST", f"Cargo temp {cargo_temp:.1f}C - adjust to {self.cargo_params['viscosity_temp']}C"

def display_ballast_monitoring():
    """Ballast System Monitoring Interface"""
    st.subheader("⚖️ Ballast System & Stability Monitoring")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        trim_angle = 0.8
        if abs(trim_angle) > 2.0:
            st.error(f"🚨 Trim Angle\n{trim_angle}deg")
        elif abs(trim_angle) > 1.0:
            st.warning(f"⚠️ Trim Angle\n{trim_angle}deg")
        else:
            st.success(f"✅ Trim Angle\n{trim_angle}deg")
            
    with col2:
        heel_angle = 0.3
        if abs(heel_angle) > 1.5:
            st.error(f"🚨 Heel Angle\n{heel_angle}deg")
        elif abs(heel_angle) > 0.5:
            st.warning(f"⚠️ Heel Angle\n{heel_angle}deg")
        else:
            st.success(f"✅ Heel Angle\n{heel_angle}deg")
            
    with col3:
        ballast_pressure = 3.2
        if ballast_pressure < 2.0:
            st.error(f"🚨 Ballast Pressure\n{ballast_pressure} bar")
        elif ballast_pressure < 2.5:
            st.warning(f"⚠️ Ballast Pressure\n{ballast_pressure} bar")
        else:
            st.success(f"✅ Ballast Pressure\n{ballast_pressure} bar")
            
    with col4:
        ballast_pump_temp = 72
        if ballast_pump_temp > 100:
            st.error(f"🚨 Pump Temp\n{ballast_pump_temp}C")
        elif ballast_pump_temp > 85:
            st.warning(f"⚠️ Pump Temp\n{ballast_pump_temp}C")
        else:
            st.success(f"✅ Pump Temp\n{ballast_pump_temp}C")

def display_fire_system_monitoring():
    """Fire System Monitoring Interface"""
    st.subheader("🔥 Fire Fighting System Monitoring")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fire_pressure = 7.8
        if fire_pressure < 4.0:
            st.error(f"🚨 Fire Main\n{fire_pressure} bar")
        elif fire_pressure < 6.0:
            st.warning(f"⚠️ Fire Main\n{fire_pressure} bar")
        else:
            st.success(f"✅ Fire Main\n{fire_pressure} bar")
            
    with col2:
        fire_pump_temp = 78
        if fire_pump_temp > 105:
            st.error(f"🚨 Fire Pump\n{fire_pump_temp}C")
        elif fire_pump_temp > 90:
            st.warning(f"⚠️ Fire Pump\n{fire_pump_temp}C")
        else:
            st.success(f"✅ Fire Pump\n{fire_pump_temp}C")
            
    with col3:
        deluge_status = "READY"
        st.success(f"✅ Deluge System\n{deluge_status}")
            
    with col4:
        foam_system = "STANDBY"
        st.warning(f"⚠️ Foam System\n{foam_system}")

def display_cargo_heating_monitoring():
    """Cargo Heating Monitoring Interface"""
    st.subheader("🌡️ Cargo Tank Heating System")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cargo_temp_1 = 42.5
        st.metric("Tank 1 Temperature", f"{cargo_temp_1}C", "0.5")
        
    with col2:
        cargo_temp_2 = 43.2
        st.metric("Tank 2 Temperature", f"{cargo_temp_2}C", "0.3")
        
    with col3:
        cargo_temp_3 = 41.8  
        st.metric("Tank 3 Temperature", f"{cargo_temp_3}C", "-0.2")
        
    with col4:
        heating_pump_temp = 85
        if heating_pump_temp > 100:
            st.error(f"🚨 Heating Pump\n{heating_pump_temp}C")
        elif heating_pump_temp > 90:
            st.warning(f"⚠️ Heating Pump\n{heating_pump_temp}C")
        else:
            st.success(f"✅ Heating Pump\n{heating_pump_temp}C")

# Main Application
def main():
    # Main Title
    st.title("🌊 FPSO Spirit - Digital Soul of Floating Production")
    st.markdown("### *Where Engineering Meets Consciousness*")

    # System Status
    st.success("🚀 FPSO Spirit System Initialized Successfully!")
    st.info("The digital soul of your FPSO is awakening...")

    # Dashboard Columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Spirit Health", "98%", "2%")
        
    with col2:
        st.metric("Consciousness Level", "AWAKENING")

    with col3:
        st.metric("Systems Integrated", "6/8")

    with col4:
        st.metric("Operational Time", "0 days")

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
        st.button("⚡ Start Monitoring", type="primary")
        st.button("🛑 Emergency Stop")
        
        st.markdown("---")
        st.subheader("System Info")
        st.write("**Status:** Initializing")
        st.write("**Version:** 1.0.0")
        st.write("**Last Update:** Just now")

if __name__ == "__main__":
    main()
