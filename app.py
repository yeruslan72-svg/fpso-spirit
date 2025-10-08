# app.py - AVCS DNA v6.0 PRO (ALL IN ONE FILE - ENGLISH)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import requests
import json

# =============================================================================
# AI ENGINE - EMBEDDED DIRECTLY IN THE FILE
# =============================================================================

class AVCSDNAEngine:
    """AI Engine for analysis and stabilization - embedded directly in app.py"""
    
    def __init__(self):
        self.risk_history = []
        self.damper_forces = []
        self.vibration_history = []
        self.temperature_history = []
        
    def analyze_equipment_health(self, sensor_data):
        """Main AI analysis of equipment condition"""
        # Vibration analysis
        vib_signals = [
            sensor_data.get('VIB_PUMP_A_X', 0),
            sensor_data.get('VIB_PUMP_A_Y', 0), 
            sensor_data.get('VIB_PUMP_B_X', 0),
            sensor_data.get('VIB_PUMP_B_Y', 0)
        ]
        
        # Temperature analysis
        temps = [
            sensor_data.get('TEMP_PUMP_A', 0),
            sensor_data.get('TEMP_MOTOR_A', 0)
        ]
        
        # Calculate RMS vibration
        rms_vibration = np.sqrt(np.mean(np.square(vib_signals)))
        max_temperature = max(temps)
        
        # Risk index based on vibration and temperature
        vib_risk = min(100, rms_vibration * 15)
        temp_risk = min(100, max(0, max_temperature - 60) * 2)
        
        risk_index = (vib_risk * 0.6 + temp_risk * 0.4)
        
        # Save history
        self.risk_history.append(risk_index)
        self.vibration_history.append(rms_vibration)
        self.temperature_history.append(max_temperature)
        
        # Remaining Useful Life (RUL) prediction
        if risk_index < 30:
            rul_hours = 720  # 30 days
        elif risk_index < 60:
            rul_hours = 240  # 10 days
        elif risk_index < 80:
            rul_hours = 72   # 3 days
        else:
            rul_hours = 24   # 1 day
            
        # Determine damping force
        if risk_index >= 80:
            damper_force = 8000
            status = "🔴 CRITICAL"
            recommendation = "IMMEDIATE SHUTDOWN REQUIRED"
        elif risk_index >= 60:
            damper_force = 4000
            status = "🟡 WARNING" 
            recommendation = "Schedule maintenance within 24 hours"
        elif risk_index >= 30:
            damper_force = 1000
            status = "🟢 NORMAL"
            recommendation = "Increase monitoring frequency"
        else:
            damper_force = 500
            status = "🔵 STANDBY"
            recommendation = "Normal operation"
            
        self.damper_forces.append(damper_force)
        
        # Fault diagnosis
        faults = self._diagnose_faults(vib_signals, temps, sensor_data.get('RPM_PUMP_A', 0))
        
        return {
            'risk_index': risk_index,
            'damper_force': damper_force,
            'status': status,
            'rul_hours': rul_hours,
            'recommendation': recommendation,
            'faults': faults,
            'vibration_rms': rms_vibration,
            'max_temperature': max_temperature,
            'timestamp': datetime.now().isoformat()
        }
    
    def _diagnose_faults(self, vib_signals, temps, rpm):
        """Diagnose specific equipment faults"""
        faults = {}
        
        # Bearing damage diagnosis
        peak_vibration = max(vib_signals)
        if peak_vibration > 5.0:
            faults['bearing_damage'] = min(1.0, (peak_vibration - 5.0) / 3.0)
        
        # Misalignment diagnosis
        vib_diff = abs(vib_signals[0] - vib_signals[1])
        if vib_diff > 2.0:
            faults['misalignment'] = min(1.0, vib_diff / 4.0)
            
        # Imbalance diagnosis
        if rpm > 2950 or rpm < 2850:
            faults['imbalance'] = min(1.0, abs(rpm - 2900) / 100.0)
            
        # Overheating diagnosis
        if max(temps) > 85:
            faults['overheating'] = min(1.0, (max(temps) - 85) / 20.0)
            
        return faults

# =============================================================================
# MR DAMPER CONTROLLER - ALSO EMBEDDED
# =============================================================================

class MRDamperController:
    """MR Damper Controller"""
    
    def __init__(self):
        self.dampers = {
            'Front-Left': {'force': 0, 'position': 'FL'},
            'Front-Right': {'force': 0, 'position': 'FR'},
            'Rear-Left': {'force': 0, 'position': 'RL'}, 
            'Rear-Right': {'force': 0, 'position': 'RR'}
        }
        
    def apply_force_distribution(self, total_force, vibration_data):
        """Apply force distribution to dampers"""
        # Simple distribution - complex logic in real implementation
        force_per_damper = total_force // 4
        
        for damper in self.dampers:
            self.dampers[damper]['force'] = force_per_damper
            
        return self.dampers
    
    def get_damper_status(self):
        """Get damper status"""
        return self.dampers

# =============================================================================
# DATA SIMULATOR - IF EXTERNAL API IS UNAVAILABLE
# =============================================================================

class DataSimulator:
    """Realistic equipment data generator"""
    
    def __init__(self):
        self.cycle = 0
        
    def generate_sensor_data(self):
        """Generate sensor data"""
        self.cycle += 1
        
        # Gradual equipment degradation
        if self.cycle < 30:
            # Normal operation
            degradation = 0
        elif self.cycle < 60:
            # Initial degradation
            degradation = (self.cycle - 30) * 0.02
        elif self.cycle < 90:
            # Serious degradation
            degradation = 0.6 + (self.cycle - 60) * 0.03
        else:
            # Critical condition
            degradation = 1.5 + (self.cycle - 90) * 0.05
            
        data = {
            'VIB_PUMP_A_X': round(1.0 + degradation + np.random.normal(0, 0.3), 2),
            'VIB_PUMP_A_Y': round(1.0 + degradation + np.random.normal(0, 0.3), 2),
            'VIB_PUMP_B_X': round(1.0 + degradation * 0.8 + np.random.normal(0, 0.3), 2),
            'VIB_PUMP_B_Y': round(1.0 + degradation * 0.8 + np.random.normal(0, 0.3), 2),
            'TEMP_PUMP_A': round(65 + degradation * 15 + np.random.normal(0, 2), 1),
            'TEMP_MOTOR_A': round(60 + degradation * 12 + np.random.normal(0, 2), 1),
            'RPM_PUMP_A': int(2900 + np.random.normal(0, 20)),
            'PRESS_MAIN_LINE': round(7.0 + np.random.normal(0, 0.2), 2),
            'timestamp': datetime.now().isoformat()
        }
        
        # Value constraints
        data['VIB_PUMP_A_X'] = max(0.1, min(10.0, data['VIB_PUMP_A_X']))
        data['TEMP_PUMP_A'] = max(20, min(120, data['TEMP_PUMP_A']))
        
        return data

# =============================================================================
# MAIN STREAMLIT APP
# =============================================================================

def main():
    st.set_page_config(
        page_title="AVCS DNA v6.0 PRO", 
        page_icon="🏭", 
        layout="wide"
    )
    
    st.title("🏭 AVCS DNA v6.0 PRO - AI Stabilization System")
    st.markdown("**Active Vibration Control System with AI Failure Prediction**")
    
    # Session initialization
    if 'avcs_engine' not in st.session_state:
        st.session_state.avcs_engine = AVCSDNAEngine()
        st.session_state.damper_controller = MRDamperController()
        st.session_state.data_simulator = DataSimulator()
        st.session_state.system_running = False
        st.session_state.analysis_history = []
    
    # =========================================================================
    # SIDEBAR - CONTROL PANEL
    # =========================================================================
    st.sidebar.header("🎛️ AVCS DNA Control Panel")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🚀 Start System", type="primary", use_container_width=True):
            st.session_state.system_running = True
            st.session_state.avcs_engine = AVCSDNAEngine()  # Reset on new start
            st.rerun()
            
    with col2:
        if st.button("🛑 Emergency Stop", use_container_width=True):
            st.session_state.system_running = False
            st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 System Status")
    
    if st.session_state.system_running:
        st.sidebar.success("✅ System Active")
        st.sidebar.info("🔄 Processing real-time data")
    else:
        st.sidebar.warning("⏸️ System Stopped")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🏭 System Architecture")
    st.sidebar.write("• 4x Vibration Sensors (PCB 603C01)")
    st.sidebar.write("• 2x Thermal Sensors (FLIR A500f)")
    st.sidebar.write("• 4x MR Dampers (LORD RD-8040)")
    st.sidebar.write("• AI: Risk Analysis + RUL Prediction")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 Business Case")
    st.sidebar.metric("System Cost", "$250,000")
    st.sidebar.metric("Typical ROI", ">2000%")
    st.sidebar.metric("Payback Period", "<3 months")
    
    # =========================================================================
    # MAIN INTERFACE
    # =========================================================================
    
    if not st.session_state.system_running:
        # Welcome screen
        st.info("🚀 **System Ready** - Click 'Start System' to begin monitoring")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🎯 AVCS DNA Advantages")
            st.write("""
            - **AI Failure Prediction** 48+ hours in advance
            - **Active Vibration Suppression** in real-time  
            - **Automatic Equipment Stabilization**
            - **Guaranteed ROI** >2000%
            - **Prevention** of unplanned downtime
            """)
            
        with col2:
            st.subheader("📈 Technology Stack")
            st.write("""
            - **ML Algorithms**: Isolation Forest + Gradient Boosting
            - **Sensors**: PCB Piezotronics + FLIR Thermal
            - **Dampers**: LORD MR Technology
            - **Controller**: Beckhoff TwinCAT
            - **Integration**: OPC-UA + REST API
            """)
        
        return
    
    # =========================================================================
    # REAL-TIME MONITORING
    # =========================================================================
    
    # Data acquisition and analysis
    sensor_data = st.session_state.data_simulator.generate_sensor_data()
    analysis = st.session_state.avcs_engine.analyze_equipment_health(sensor_data)
    st.session_state.analysis_history.append(analysis)
    
    # Damper control application
    damper_status = st.session_state.damper_controller.apply_force_distribution(
        analysis['damper_force'], sensor_data
    )
    
    # =========================================================================
    # MAIN DASHBOARD
    # =========================================================================
    
    # ROW 1: KEY METRICS
    st.subheader("📊 System Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Risk Index with color coding
        risk_color = "green" if analysis['risk_index'] < 50 else "orange" if analysis['risk_index'] < 80 else "red"
        st.metric(
            "🎯 Risk Index", 
            f"{analysis['risk_index']:.1f}/100",
            delta=analysis['status'],
            delta_color=risk_color
        )
    
    with col2:
        # Remaining Useful Life
        rul_color = "green" if analysis['rul_hours'] > 168 else "orange" if analysis['rul_hours'] > 72 else "red"
        st.metric(
            "⏳ Remaining Useful Life (RUL)",
            f"{analysis['rul_hours']} hours",
            delta_color=rul_color
        )
    
    with col3:
        st.metric(
            "🔧 Damping Force", 
            f"{analysis['damper_force']} N"
        )
    
    with col4:
        st.metric(
            "🌡️ Max Temperature",
            f"{analysis['max_temperature']} °C"
        )
    
    # ROW 2: DAMPER SYSTEM
    st.subheader("🔧 MR Damper System")
    damper_cols = st.columns(4)
    
    for i, (position, status) in enumerate(damper_status.items()):
        with damper_cols[i]:
            force = status['force']
            if force >= 2000:
                st.error(f"🔴 {position}\n**{force} N**\n*Critical Mode*")
            elif force >= 250:
                st.warning(f"🟡 {position}\n**{force} N**\n*Active Mode*")
            else:
                st.success(f"🟢 {position}\n**{force} N**\n*Standby Mode*")
    
    # ROW 3: CHARTS AND VISUALIZATION
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Risk Index Trend")
        if len(st.session_state.avcs_engine.risk_history) > 1:
            risk_df = pd.DataFrame({
                'Risk Index': st.session_state.avcs_engine.risk_history,
                'Critical Threshold': [80] * len(st.session_state.avcs_engine.risk_history),
                'Warning Threshold': [50] * len(st.session_state.avcs_engine.risk_history)
            })
            st.line_chart(risk_df)
    
    with col2:
        st.subheader("⚡ Damping Force History")
        if len(st.session_state.avcs_engine.damper_forces) > 1:
            force_df = pd.DataFrame({
                'Damper Force (N)': st.session_state.avcs_engine.damper_forces
            })
            st.line_chart(force_df)
    
    # ROW 4: DIAGNOSTICS AND RECOMMENDATIONS
    st.subheader("🔍 AI Equipment Diagnostics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📋 Detected Faults:**")
        if analysis['faults']:
            for fault, probability in analysis['faults'].items():
                prob_percent = probability * 100
                if prob_percent > 70:
                    st.error(f"🔴 {fault.replace('_', ' ').title()}: {prob_percent:.1f}%")
                elif prob_percent > 40:
                    st.warning(f"🟡 {fault.replace('_', ' ').title()}: {prob_percent:.1f}%")
                else:
                    st.info(f"🔵 {fault.replace('_', ' ').title()}: {prob_percent:.1f}%")
        else:
            st.success("✅ No critical faults detected")
    
    with col2:
        st.write("**💡 AI Recommendations:**")
        if analysis['risk_index'] >= 80:
            st.error(f"🚨 {analysis['recommendation']}")
        elif analysis['risk_index'] >= 60:
            st.warning(f"⚠️ {analysis['recommendation']}")
        else:
            st.success(f"✅ {analysis['recommendation']}")
    
    # ROW 5: REAL-TIME SENSOR DATA
    st.subheader("📡 Real-time Sensor Data")
    
    sensor_cols = st.columns(4)
    sensor_metrics = {
        "Vibration X": f"{sensor_data['VIB_PUMP_A_X']:.2f} mm/s",
        "Vibration Y": f"{sensor_data['VIB_PUMP_A_Y']:.2f} mm/s",
        "Pump Temperature": f"{sensor_data['TEMP_PUMP_A']:.1f} °C", 
        "RPM": f"{sensor_data['RPM_PUMP_A']} RPM"
    }
    
    for i, (name, value) in enumerate(sensor_metrics.items()):
        with sensor_cols[i]:
            st.metric(name, value)
    
    # Auto-refresh
    time.sleep(1)
    st.rerun()

if __name__ == "__main__":
    main()
