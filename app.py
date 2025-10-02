# FPSO Spirit - COMPLETE SYSTEM with Hull Visualization
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import IsolationForest

# Page Configuration
st.set_page_config(
    page_title="FPSO Spirit",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize ALL session states
session_states = {
    'monitoring_active': False,
    'emergency_stop': False,
    'system_data': {},
    'risk_level': "LOW",
    'cycle_count': 0,
    'last_update': datetime.now(),
    'historical_data': [],
    'prevented_incidents': 0,
    'cost_savings': 0,
    'simulation_start': datetime.now()
}

for key, default_value in session_states.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# Initialize AI model
if 'ai_model' not in st.session_state:
    np.random.seed(42)
    normal_data = np.random.normal(0, 1, (1000, 15))
    st.session_state.ai_model = IsolationForest(contamination=0.1, random_state=42)
    st.session_state.ai_model.fit(normal_data)

def generate_complete_sensor_data():
    """Generate data for ALL systems including hull parameters"""
    cycle = st.session_state.cycle_count
    degradation = min(1.0, cycle * 0.001)
    
    # Simulate hull stresses based on operations
    wave_effect = np.sin(cycle * 0.1) * 5  # Wave-induced stress
    cargo_effect = np.random.normal(0, 3)   # Cargo loading effect
    degradation_effect = degradation * 10
    
    data = {
        # === HULL & STRUCTURAL PARAMETERS ===
        'trim_angle': 0.5 + np.random.normal(0, 0.3) + degradation * 0.3,
        'heel_angle': 0.3 + np.random.normal(0, 0.2) + degradation * 0.2,
        'draft_forward': 18.5 + np.random.normal(0, 0.2),
        'draft_aft': 18.2 + np.random.normal(0, 0.2),
        'hull_stress': 25 + wave_effect + cargo_effect + degradation_effect,
        'bending_moment': 1200 + np.random.normal(0, 100) + degradation * 150,
        'shear_force': 800 + np.random.normal(0, 80) + degradation * 100,
        'hogging_sagging': np.sin(cycle * 0.05) * 50,  # Hogging/sagging moment
        
        # === VIBRATION with degradation ===
        'vib_dg1_de': 1.2 + np.random.normal(0, 0.3) + degradation * 0.5,
        'vib_dg2_de': 1.5 + np.random.normal(0, 0.4) + degradation * 0.6,
        'vib_cargo_pump': 2.1 + np.random.normal(0, 0.5) + degradation * 0.8,
        'vib_ballast_pump': 1.8 + np.random.normal(0, 0.4) + degradation * 0.7,
        
        # === TEMPERATURE with degradation ===
        'dg1_temp': 85 + np.random.normal(0, 5) + degradation * 10,
        'dg2_temp': 82 + np.random.normal(0, 6) + degradation * 8,
        'cargo_pump_temp': 88 + np.random.normal(0, 7) + degradation * 12,
        
        # === CARGO SYSTEM ===
        'cargo_temp_1': 42 + np.random.normal(0, 2),
        'cargo_temp_2': 43 + np.random.normal(0, 2),
        'cargo_temp_3': 41 + np.random.normal(0, 2),
        'cargo_temp_4': 44 + np.random.normal(0, 2),
        'cargo_temp_5': 42.5 + np.random.normal(0, 2),
        'cargo_temp_6': 43.5 + np.random.normal(0, 2),
        
        # === BALLAST SYSTEM ===
        'ballast_port_1_level': 60 + np.random.normal(0, 8),
        'ballast_port_2_level': 55 + np.random.normal(0, 8),
        'ballast_stbd_1_level': 61 + np.random.normal(0, 8),
        'ballast_stbd_2_level': 56 + np.random.normal(0, 8),
        'ballast_forepeak_level': 70 + np.random.normal(0, 5),
        
        # === IGS SYSTEM ===
        'igs_o2_tank1': 2.0 + np.random.normal(0, 0.3),
        'igs_pressure': 0.15 + np.random.normal(0, 0.02),
        
        # === MR DAMPERS ===
        'damper_dg1_force': 1000,
        'damper_dg2_force': 1000,
    }
    
    # Apply heel effect to ballast tanks
    heel_effect = data['heel_angle'] * 2
    data['ballast_port_1_level'] = max(0, min(100, data['ballast_port_1_level'] - heel_effect))
    data['ballast_stbd_1_level'] = max(0, min(100, data['ballast_stbd_1_level'] + heel_effect))
    
    # Adaptive damper control
    for equipment in ['dg1', 'dg2']:
        vib_key = f'vib_{equipment}_de'
        damper_key = f'damper_{equipment}_force'
        if data[vib_key] > 3.0:
            data[damper_key] = 4000
        elif data[vib_key] > 2.0:
            data[damper_key] = 2000
    
    # AI anomaly detection
    try:
        features = [data['hull_stress'], data['heel_angle'], 
                   data['vib_dg1_de'], data['dg1_temp']]
        ai_prediction = st.session_state.ai_model.predict([features])[0]
        data['ai_anomaly'] = ai_prediction
        data['ai_confidence'] = abs(st.session_state.ai_model.decision_function([features])[0])
        
        if ai_prediction == -1:
            data['ai_action'] = "PREEMPTIVE_DAMPING"
            if np.random.random() < 0.3:  # 30% chance this prevented an incident
                st.session_state.prevented_incidents += 1
                st.session_state.cost_savings += 250000
        else:
            data['ai_action'] = "MONITORING"
    except:
        data['ai_anomaly'] = 1
        data['ai_action'] = "MONITORING"
    
    return data

def create_hull_visualization(data):
    """Create 3D hull visualization with stress and deformation"""
    if not data:
        return go.Figure()
    
    # Create hull geometry points
    length = 100  # meters
    width = 20    # meters
    height = 10   # meters
    
    # Hull vertices
    x = np.array([0, length, length, 0, 0, length, length, 0])
    y = np.array([0, 0, width, width, 0, 0, width, width]) 
    z = np.array([0, 0, 0, 0, height, height, height, height])
    
    # Apply heel and trim transformations
    heel_rad = np.radians(data['heel_angle'])
    trim_rad = np.radians(data['trim_angle'])
    
    # Heel rotation (around x-axis)
    y_heel = y * np.cos(heel_rad) - z * np.sin(heel_rad)
    z_heel = y * np.sin(heel_rad) + z * np.cos(heel_rad)
    
    # Trim rotation (around y-axis)
    x_trim = x * np.cos(trim_rad) - z_heel * np.sin(trim_rad)
    z_final = x * np.sin(trim_rad) + z_heel * np.cos(trim_rad)
    
    fig = go.Figure()
    
    # Hull mesh
    fig.add_trace(go.Mesh3d(
        x=x_trim, y=y_heel, z=z_final,
        color='lightblue',
        opacity=0.7,
        name="Hull Structure",
        showscale=False
    ))
    
    # Stress points with color coding
    stress_points = [
        [25, 10, 5], [75, 10, 5],  # Mid-ship (high stress)
        [10, 5, 8], [90, 5, 8],    # Bow/stern areas
        [50, 2, 6], [50, 18, 6],   # Port/starboard sides
    ]
    
    for i, point in enumerate(stress_points):
        # Calculate stress at this point
        base_stress = data['hull_stress']
        location_factor = 1.0 + (i * 0.2)  # Different locations have different stress
        point_stress = base_stress * location_factor + np.random.normal(0, 3)
        
        # Color based on stress level
        if point_stress > 45:
            color = 'red'
            size = 12
        elif point_stress > 35:
            color = 'orange' 
            size = 9
        else:
            color = 'green'
            size = 6
            
        fig.add_trace(go.Scatter3d(
            x=[point[0]], y=[point[1]], z=[point[2]],
            mode='markers',
            marker=dict(size=size, color=color),
            name=f"Stress: {point_stress:.0f}%",
            text=f"Stress: {point_stress:.0f}%",
            hovertemplate="<b>Hull Stress Point</b><br>Stress: %{text}<br>Location: %{x:.0f}m, %{y:.0f}m<extra></extra>"
        ))
    
    # Add waterline based on draft
    waterline_z = -data['draft_forward'] * 0.5  # Scale for visualization
    waterline_points = 20
    waterline_x = np.linspace(0, length, waterline_points)
    waterline_y = np.linspace(0, width, waterline_points)
    xx, yy = np.meshgrid(waterline_x, waterline_y)
    zz = np.full_like(xx, waterline_z)
    
    fig.add_trace(go.Surface(
        x=xx, y=yy, z=zz,
        colorscale='Blues',
        opacity=0.3,
        showscale=False,
        name="Waterline"
    ))
    
    fig.update_layout(
        title={
            'text': f"FPSO Hull - 3D Structural Analysis<br>Heel: {data['heel_angle']:.1f}° | Trim: {data['trim_angle']:.1f}° | Stress: {data['hull_stress']:.0f}%",
            'x': 0.5,
            'xanchor': 'center'
        },
        scene=dict(
            xaxis_title="Length (m)",
            yaxis_title="Width (m)",
            zaxis_title="Height (m)",
            aspectmode='data',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
        ),
        height=500,
        margin=dict(l=0, r=0, b=0, t=50)
    )
    
    return fig

def create_hull_stress_analysis(data):
    """Create 2D stress analysis chart"""
    if not data:
        return go.Figure()
    
    fig = go.Figure()
    
    # Structural loads
    loads = {
        'Bending Moment': data['bending_moment'],
        'Shear Force': data['shear_force'],
        'Hull Stress': data['hull_stress'],
        'Hogging/Sagging': data.get('hogging_sagging', 0)
    }
    
    colors = []
    for load, value in loads.items():
        if load == 'Bending Moment':
            if value > 1600: colors.append('red')
            elif value > 1400: colors.append('orange')
            else: colors.append('green')
        elif load == 'Shear Force':
            if value > 1200: colors.append('red')
            elif value > 1000: colors.append('orange')
            else: colors.append('green')
        else:  # Stress
            if value > 45: colors.append('red')
            elif value > 35: colors.append('orange')
            else: colors.append('green')
    
    fig.add_trace(go.Bar(
        x=list(loads.keys()),
        y=list(loads.values()),
        marker_color=colors,
        text=[f"{v:.0f}" for v in loads.values()],
        textposition='auto',
    ))
    
    # Add critical limits
    fig.add_hline(y=1600, line_dash="dash", line_color="red", annotation_text="Bending Critical")
    fig.add_hline(y=1400, line_dash="dot", line_color="orange", annotation_text="Bending Warning")
    fig.add_hline(y=1200, line_dash="dash", line_color="red", annotation_text="Shear Critical")
    fig.add_hline(y=1000, line_dash="dot", line_color="orange", annotation_text="Shear Warning")
    fig.add_hline(y=45, line_dash="dash", line_color="red", annotation_text="Stress Critical")
    fig.add_hline(y=35, line_dash="dot", line_color="orange", annotation_text="Stress Warning")
    
    fig.update_layout(
        title="Hull Structural Load Analysis",
        xaxis_title="Load Types",
        yaxis_title="Load Value",
        height=300
    )
    
    return fig

def create_tank_temperature_chart(data):
    """Create cargo tank temperature visualization"""
    if not data:
        return go.Figure()
    
    tank_temps = {
        'Tank 1': data['cargo_temp_1'],
        'Tank 2': data['cargo_temp_2'],
        'Tank 3': data['cargo_temp_3'], 
        'Tank 4': data['cargo_temp_4'],
        'Tank 5': data['cargo_temp_5'],
        'Tank 6': data['cargo_temp_6']
    }
    
    colors = ['red' if temp > 50 else 'orange' if temp > 45 else 'green' 
              for temp in tank_temps.values()]
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(tank_temps.keys()),
            y=list(tank_temps.values()),
            marker_color=colors,
            text=[f"{temp:.1f}°C" for temp in tank_temps.values()],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Cargo Tank Temperatures",
        xaxis_title="Tanks",
        yaxis_title="Temperature (°C)",
        height=300
    )
    
    fig.add_hline(y=55, line_dash="dash", line_color="red", annotation_text="Critical")
    fig.add_hline(y=45, line_dash="dot", line_color="orange", annotation_text="Warning")
    
    return fig

def create_vibration_dashboard(data):
    """Create vibration and damper monitoring"""
    if not data:
        return go.Figure()
    
    fig = go.Figure()
    
    equipment = ['DG1', 'DG2', 'Cargo Pump', 'Ballast Pump']
    vibrations = [data['vib_dg1_de'], data['vib_dg2_de'], 
                 data['vib_cargo_pump'], data['vib_ballast_pump']]
    damper_forces = [data['damper_dg1_force'], data['damper_dg2_force'], 1000, 1000]
    
    fig.add_trace(go.Bar(
        name='Vibration (mm/s)',
        x=equipment,
        y=vibrations,
        marker_color=['red' if v > 3.0 else 'orange' if v > 2.0 else 'green' for v in vibrations],
        text=[f"{v:.1f} mm/s" for v in vibrations],
        textposition='auto',
    ))
    
    fig.add_trace(go.Scatter(
        name='Damper Force (N)',
        x=equipment[:2],  # Only for DG1 and DG2
        y=damper_forces[:2],
        mode='lines+markers+text',
        line=dict(color='blue', width=3),
        marker=dict(size=10),
        text=[f"{f} N" for f in damper_forces[:2]],
        textposition='top center',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Vibration Monitoring & MR Damper Control",
        xaxis_title="Equipment",
        yaxis_title="Vibration (mm/s)",
        yaxis2=dict(
            title="Damper Force (N)",
            overlaying='y',
            side='right'
        ),
        height=350
    )
    
    fig.add_hline(y=4.0, line_dash="dash", line_color="red", annotation_text="Critical")
    fig.add_hline(y=2.0, line_dash="dot", line_color="orange", annotation_text="Warning")
    
    return fig

# Main Application
def main():
    st.title("🌊 FPSO Spirit - Complete Hull & Systems Monitoring")
    st.markdown("### *3D Hull Visualization + AVCS DNA + Thermal DNA*")

    # Auto-refresh
    if st.session_state.monitoring_active and not st.session_state.emergency_stop:
        current_time = datetime.now()
        time_diff = (current_time - st.session_state.last_update).total_seconds()
        
        if time_diff >= 3:
            st.session_state.system_data = generate_complete_sensor_data()
            st.session_state.cycle_count += 1
            st.session_state.last_update = current_time
            
            if len(st.session_state.historical_data) > 50:
                st.session_state.historical_data.pop(0)
            st.session_state.historical_data.append(st.session_state.system_data.copy())
            
            st.rerun()

    # System Status
    if st.session_state.emergency_stop:
        st.error("🚨 EMERGENCY STOP - ALL SYSTEMS HALTED")
    elif st.session_state.monitoring_active:
        data = st.session_state.system_data
        ai_status = data.get('ai_action', 'MONITORING')
        st.success(f"🚀 ACTIVE MONITORING - Cycle #{st.session_state.cycle_count}")
        st.info(f"AI Status: {ai_status} | Prevented Incidents: {st.session_state.prevented_incidents}")
    else:
        st.info("🟡 SYSTEM READY - Click Start to Begin 3D Monitoring")

    # 3D HULL VISUALIZATION
    st.subheader("🚢 FPSO Hull - 3D Structural Analysis")
    if st.session_state.system_data:
        hull_fig = create_hull_visualization(st.session_state.system_data)
        st.plotly_chart(hull_fig, use_container_width=True)
    else:
        st.info("Start monitoring to see 3D hull visualization")

    # Systems Dashboards
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.system_data:
            stress_fig = create_hull_stress_analysis(st.session_state.system_data)
            st.plotly_chart(stress_fig, use_container_width=True)
    
    with col2:
        if st.session_state.system_data:
            temp_fig = create_tank_temperature_chart(st.session_state.system_data)
            st.plotly_chart(temp_fig, use_container_width=True)

    # Vibration & Dampers
    st.subheader("🎯 Vibration Control & MR Dampers")
    if st.session_state.system_data:
        vib_fig = create_vibration_dashboard(st.session_state.system_data)
        st.plotly_chart(vib_fig, use_container_width=True)

    # Current Parameters
    if st.session_state.system_data:
        st.subheader("📊 Real-time Parameters")
        data = st.session_state.system_data
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Heel Angle", f"{data['heel_angle']:.1f}°")
            st.metric("Trim Angle", f"{data['trim_angle']:.1f}°")
            
        with col2:
            st.metric("Hull Stress", f"{data['hull_stress']:.0f}%")
            st.metric("Bending Moment", f"{data['bending_moment']:.0f} kN·m")
            
        with col3:
            st.metric("DG1 Vibration", f"{data['vib_dg1_de']:.1f} mm/s")
            st.metric("DG1 Temperature", f"{data['dg1_temp']:.0f}°C")
            
        with col4:
            st.metric("AI Detection", data.get('ai_action', 'MONITORING'))
            st.metric("Cost Savings", f"${st.session_state.cost_savings:,}")

    # Control Panel
    with st.sidebar:
        st.header("🎛️ Complete System Control")
        
        if st.session_state.emergency_stop:
            st.error("🚨 EMERGENCY STOP")
            if st.button("✅ Reset System", type="primary", use_container_width=True):
                st.session_state.emergency_stop = False
                st.rerun()
        else:
            col1, col2 = st.columns(2)
            with col1:
                if not st.session_state.monitoring_active:
                    if st.button("⚡ Start All", type="primary", use_container_width=True):
                        st.session_state.monitoring_active = True
                        st.session_state.simulation_start = datetime.now()
                        st.rerun()
                else:
                    if st.button("⏸️ Stop", type="secondary", use_container_width=True):
                        st.session_state.monitoring_active = False
                        st.rerun()
            with col2:
                if st.button("🛑 E-Stop", type="secondary", use_container_width=True):
                    st.session_state.emergency_stop = True
                    st.session_state.monitoring_active = False
                    st.rerun()

        st.markdown("---")
        st.subheader("System Status")
        st.write("✅ **3D Hull Monitoring**")
        st.write("✅ **Structural Analysis**")
        st.write("✅ **Vibration Control**")
        st.write("✅ **Thermal DNA**")
        st.write("✅ **AI Predictive**")
        st.write(f"**Uptime:** {((datetime.now() - st.session_state.simulation_start).total_seconds() / 3600):.1f}h")

if __name__ == "__main__":
    main()
