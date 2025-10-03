import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
import random

# =========================
# REAL FPSO CONFIGURATION
# =========================
class FPSOConfig:
    """Конфигурация реального FPSO на основе вашего описания"""
    
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
    
    # Flow meters (Yokogawa)
    FLOW_METERS = {
        'FlowMeter_Import': {'location': 'Turret Input', 'type': 'Yokogawa', 'range': '0-5000 m³/h'},
        'FlowMeter_Export': {'location': 'Export Line', 'type': 'Yokogawa', 'range': '0-5000 m³/h'},
    }

# =========================
# ENHANCED DATA GENERATOR
# =========================
def generate_realistic_fpso_data(cycle: int):
    """Генерация данных для реального FPSO процесса"""
    
    # Базовые параметры
    time_factor = cycle * 0.1
    degradation = min(2.0, cycle * 0.002)
    
    # Симуляция операционных циклов
    is_loading = (cycle % 200) < 100  # Чередование погрузки/отгрузки
    is_exporting = not is_loading and (cycle % 200) > 150
    
    data = {
        # === ОПЕРАЦИОННЫЕ ПАРАМЕТРЫ ===
        'operation_mode': 'LOADING' if is_loading else 'EXPORTING' if is_exporting else 'IDLE',
        'cycle_duration': cycle,
        
        # === ПОГРУЗКА/ОТГРУЗКА ===
        'import_flow_rate': 2500 + np.random.normal(0, 200) if is_loading else 0,
        'export_flow_rate': 2800 + np.random.normal(0, 300) if is_exporting else 0,
        'total_cargo_loaded': min(90000, cycle * 45),  # кумулятивная загрузка
        'total_cargo_exported': min(85000, max(0, cycle - 150) * 40),
        
        # === ГРУЗОВЫЕ НАСОСЫ ===
        'CargoPump_A_flow': 800 + np.random.normal(0, 50) if is_exporting else 0,
        'CargoPump_B_flow': 800 + np.random.normal(0, 50) if is_exporting else 0, 
        'CargoPump_C_flow': 800 + np.random.normal(0, 50) if is_exporting else 0,
        'CargoPump_A_vib': 1.8 + np.random.normal(0, 0.4) + degradation * 0.3,
        'CargoPump_B_vib': 1.7 + np.random.normal(0, 0.3) + degradation * 0.4,
        'CargoPump_C_vib': 1.9 + np.random.normal(0, 0.5) + degradation * 0.5,
        'CargoPump_A_temp': 75 + np.random.normal(0, 5) + degradation * 8,
        'CargoPump_B_temp': 74 + np.random.normal(0, 6) + degradation * 7,
        'CargoPump_C_temp': 76 + np.random.normal(0, 7) + degradation * 9,
        
        # === БАЛЛАСТНЫЕ НАСОСЫ ===
        'BallastPump_Port_flow': 300 + np.random.normal(0, 30),
        'BallastPump_Stbd_flow': 300 + np.random.normal(0, 30),
        'BallastPump_Port_vib': 1.2 + np.random.normal(0, 0.2),
        'BallastPump_Stbd_vib': 1.3 + np.random.normal(0, 0.3),
        'BallastPump_Port_temp': 65 + np.random.normal(0, 4),
        'BallastPump_Stbd_temp': 66 + np.random.normal(0, 5),
        
        # === ПОЖАРНЫЕ НАСОСЫ ===
        'FirePump_1_pressure': 7.5 + np.random.normal(0, 0.5),
        'FirePump_2_pressure': 7.3 + np.random.normal(0, 0.6),
        'FirePump_1_temp': 60 + np.random.normal(0, 3),
        'FirePump_2_temp': 61 + np.random.normal(0, 4),
        
        # === ДИЗЕЛЬ-ГЕНЕРАТОРЫ ===
        'DG1_power': 3500 + np.random.normal(0, 200),
        'DG2_power': 3200 + np.random.normal(0, 250),
        'DG1_vib': 1.4 + np.random.normal(0, 0.3) + degradation * 0.2,
        'DG2_vib': 1.5 + np.random.normal(0, 0.4) + degradation * 0.3,
        'DG1_temp': 85 + np.random.normal(0, 5) + degradation * 6,
        'DG2_temp': 83 + np.random.normal(0, 6) + degradation * 5,
        'DG1_fuel_rate': 280 + np.random.normal(0, 15),
        'DG2_fuel_rate': 270 + np.random.normal(0, 20),
        
        # === КОТЕЛ И ТЕПЛООБМЕН ===
        'Boiler_pressure': 8.5 + np.random.normal(0, 0.3),
        'Boiler_temp': 125 + np.random.normal(0, 8),
        'cargo_heating_temp': 42 + np.random.normal(0, 2),  # температура подогрева груза
        
        # === IGS СИСТЕМА ===
        'IGS_generator_temp': 70 + np.random.normal(0, 4),
        'IGS_main_pressure': 0.16 + np.random.normal(0, 0.02),
        'IGS_flow_rate': 1200 + np.random.normal(0, 80),
        'IGS_O2_content': 2.1 + np.random.normal(0, 0.3),
        
        # === ТАНКОВАЯ СИСТЕМА ===
        **{f'Cargo_Tank_{i}_level': 80 + np.random.normal(0, 5) for i in range(1, 7)},
        **{f'Cargo_Tank_{i}_temp': 40 + np.random.normal(0, 3) for i in range(1, 7)},
        **{f'Ballast_Port_{i}_level': 60 + np.random.normal(0, 8) for i in range(1, 7)},
        **{f'Ballast_Stbd_{i}_level': 58 + np.random.normal(0, 7) for i in range(1, 7)},
        'Forepeak_Tank_level': 65 + np.random.normal(0, 4),
        'Slop_Tank_Port_level': 45 + np.random.normal(0, 6),
        'Slop_Tank_Stbd_level': 48 + np.random.normal(0, 5),
        
        # === СТРУКТУРНЫЕ ПАРАМЕТРЫ ===
        'heel_angle': 0.2 + np.sin(time_factor) * 0.8,
        'trim_angle': 0.3 + np.cos(time_factor) * 0.6,
        'hull_stress': 22 + abs(np.sin(time_factor)) * 15 + degradation * 5,
        'bending_moment': 1100 + np.random.normal(0, 80),
        'shear_force': 750 + np.random.normal(0, 60),
    }
    
    # Корректировки на основе операционного режима
    if is_loading:
        # Увеличиваем уровни грузовых танков при погрузке
        for i in range(1, 7):
            data[f'Cargo_Tank_{i}_level'] = min(95, data[f'Cargo_Tank_{i}_level'] + 0.5)
            
    elif is_exporting:
        # Уменьшаем уровни при отгрузке (кроме танка 6)
        for i in range(1, 6):
            data[f'Cargo_Tank_{i}_level'] = max(10, data[f'Cargo_Tank_{i}_level'] - 0.8)
    
    # AI анализ для предиктивного обслуживания
    try:
        features = [
            data['CargoPump_A_vib'], data['CargoPump_A_temp'], data['DG1_vib'], data['DG1_temp'],
            data['hull_stress'], data['heel_angle'], data['IGS_O2_content']
        ]
        ai_prediction = st.session_state.ai_model.predict([features])[0]
        data['ai_anomaly'] = ai_prediction
        data['ai_confidence'] = abs(st.session_state.ai_model.decision_function([features])[0])
        
        if ai_prediction == -1 and data['ai_confidence'] > 0.6:
            data['ai_action'] = "PREEMPTIVE_MAINTENANCE"
            if random.random() < 0.4:  # 40% шанс предотвращения инцидента
                st.session_state.prevented_incidents += 1
                st.session_state.cost_savings += 350000  # Высокая стоимость инцидентов на FPSO
        else:
            data['ai_action'] = "OPERATIONAL"
            
    except Exception as e:
        data['ai_anomaly'] = 1
        data['ai_action'] = "SYSTEM_ERROR"
    
    return data

# =========================
# REAL-TIME VISUALIZATIONS
# =========================
def create_operations_dashboard(data):
    """Дашборд операций погрузки/отгрузки"""
    fig = go.Figure()
    
    # Flow rates
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=data['import_flow_rate'],
        title={'text': "Import Flow Rate"},
        domain={'x': [0, 0.45], 'y': [0.5, 1]},
        gauge={'axis': {'range': [0, 5000]},
               'bar': {'color': "green"},
               'steps': [{'range': [0, 4000], 'color': "lightgray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 4500}}
    ))
    
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=data['export_flow_rate'],
        title={'text': "Export Flow Rate"},
        domain={'x': [0.55, 1], 'y': [0.5, 1]},
        gauge={'axis': {'range': [0, 5000]},
               'bar': {'color': "blue"},
               'steps': [{'range': [0, 4000], 'color': "lightgray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 4500}}
    ))
    
    # Cargo totals
    fig.add_trace(go.Indicator(
        mode="number",
        value=data['total_cargo_loaded'],
        title={'text': "Total Loaded (m³)"},
        domain={'x': [0, 0.3], 'y': [0, 0.4]},
        number={'valueformat': ",.0f"}
    ))
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=data['total_cargo_exported'],
        title={'text': "Total Exported (m³)"},
        domain={'x': [0.35, 0.65], 'y': [0, 0.4]},
        number={'valueformat': ",.0f"}
    ))
    
    fig.add_trace(go.Indicator(
        mode="number",
        value=data['total_cargo_loaded'] - data['total_cargo_exported'],
        title={'text': "Current Cargo (m³)"},
        domain={'x': [0.7, 1], 'y': [0, 0.4]},
        number={'valueformat': ",.0f"}
    ))
    
    fig.update_layout(height=300, title="Cargo Operations Dashboard")
    return fig

def create_pump_room_monitoring(data):
    """Мониторинг насосного отделения"""
    pumps = ['CargoPump_A', 'CargoPump_B', 'CargoPump_C', 'BallastPump_Port', 'BallastPump_Stbd']
    
    fig = go.Figure()
    
    # Vibration
    fig.add_trace(go.Bar(
        name='Vibration (mm/s)',
        x=pumps,
        y=[data[f'{p}_vib'] for p in pumps],
        marker_color=['red' if data[f'{p}_vib'] > 2.5 else 'orange' if data[f'{p}_vib'] > 1.8 else 'green' for p in pumps],
        text=[f"{data[f'{p}_vib']:.1f}" for p in pumps],
        textposition='auto',
        yaxis='y'
    ))
    
    # Temperature
    fig.add_trace(go.Scatter(
        name='Temperature (°C)',
        x=pumps,
        y=[data[f'{p}_temp'] for p in pumps],
        mode='lines+markers+text',
        line=dict(color='orange', width=3),
        marker=dict(size=10),
        text=[f"{data[f'{p}_temp']:.0f}°C" for p in pumps],
        textposition='top center',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Pump Room Monitoring - Vibration & Temperature",
        xaxis_title="Pumps",
        yaxis_title="Vibration (mm/s)",
        yaxis2=dict(
            title="Temperature (°C)",
            overlaying='y',
            side='right'
        ),
        height=400
    )
    
    return fig

# =========================
# MAIN APPLICATION
# =========================
def main():
    st.title("🌊 FPSO Spirit - Real-time Process Monitoring")
    st.markdown("**AVCS DNA + Thermal DNA Integrated with Yokogawa DCS**")
    
    # Initialize session state
    if "system_data" not in st.session_state:
        st.session_state.system_data = generate_realistic_fpso_data(0)
    if "monitoring_active" not in st.session_state:
        st.session_state.monitoring_active = False
    if "cycle_count" not in st.session_state:
        st.session_state.cycle_count = 0

    # Control Panel
    st.sidebar.header("⚙️ CCR Control Panel")
    
    if st.sidebar.button("▶️ Start Process Monitoring"):
        st.session_state.monitoring_active = True
        
    if st.sidebar.button("⏸️ Stop Monitoring"):
        st.session_state.monitoring_active = False
        
    # Auto-update when monitoring is active
    if st.session_state.monitoring_active:
        st.session_state.cycle_count += 1
        st.session_state.system_data = generate_realistic_fpso_data(st.session_state.cycle_count)
        st.rerun()
    
    data = st.session_state.system_data
    
    # Operations Overview
    st.subheader("📊 Operations Overview")
    st.plotly_chart(create_operations_dashboard(data), use_container_width=True)
    
    # Equipment Monitoring
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏭 Pump Room Monitoring")
        st.plotly_chart(create_pump_room_monitoring(data), use_container_width=True)
        
    with col2:
        st.subheader("⚡ Power Generation")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("DG1 Power", f"{data['DG1_power']:.0f} kW")
            st.metric("DG1 Temp", f"{data['DG1_temp']:.0f}°C")
        with col_b:
            st.metric("DG2 Power", f"{data['DG2_power']:.0f} kW") 
            st.metric("DG2 Temp", f"{data['DG2_temp']:.0f}°C")
    
    # AI Predictive Maintenance
    st.subheader("🧠 AVCS DNA Predictive Analysis")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_color = "red" if data.get('ai_anomaly') == -1 else "green"
        st.metric("AI Status", data.get('ai_action', 'OPERATIONAL'), delta="Anomaly Detected" if data.get('ai_anomaly') == -1 else "Normal")
    
    with col2:
        st.metric("Prevented Incidents", st.session_state.get('prevented_incidents', 0))
    
    with col3:
        st.metric("Cost Savings", f"${st.session_state.get('cost_savings', 0):,}")

if __name__ == "__main__":
    main()
