# app.py
import time
import random
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# =========================
# FPSO CONFIG (описание)
# =========================
class FPSOConfig:
    CARGO_PUMPS = {
        'CargoPump_A': {'power': 800},
        'CargoPump_B': {'power': 800},
        'CargoPump_C': {'power': 800},
    }
    BALLAST_PUMPS = {
        'BallastPump_Port': {'power': 400},
        'BallastPump_Stbd': {'power': 400},
    }

# =========================
# DATA GENERATOR
# =========================
def generate_realistic_fpso_data(cycle: int, pump_status=None, faults=None, auto_fault_prob=0.0):
    """Генерация данных для одного цикла.
       pump_status: dict с булевыми значениями для каждого cargo pump
       faults: dict флагов неисправностей, которые действуют в текущем цикле
       auto_fault_prob: вероятность автогенерации случайной неисправности (0..1)
    """
    if pump_status is None:
        pump_status = {"CargoPump_A": True, "CargoPump_B": True, "CargoPump_C": False}
    if faults is None:
        faults = {}

    # Возможна автоматическая случайная инъекция неисправности
    if auto_fault_prob > 0 and random.random() < auto_fault_prob:
        # случайно выбираем одно из устройств и ставим флаг в faults (локально)
        choice = random.choice(["CargoPump_A_failure", "DG1_overheat", "IGS_low_pressure"])
        faults = {**faults, choice: True}

    time_factor = cycle * 0.12
    degradation = min(2.5, cycle * 0.0025)

    # Определяем режимы (loading/exporting/idle)
    is_loading = (cycle % 200) < 100
    is_exporting = (cycle % 200) > 150

    data = {}
    data['cycle'] = cycle
    data['operation_mode'] = 'LOADING' if is_loading else 'EXPORTING' if is_exporting else 'IDLE'

    # Import / Export flows (import работает при loading, export при exporting)
    data['import_flow_rate'] = 2500 + np.random.normal(0, 200) if is_loading else 0
    # export_flow_rate = сумма активных насосов (только в режиме EXPORTING)
    for pump_key in ["CargoPump_A", "CargoPump_B", "CargoPump_C"]:
        if pump_status.get(pump_key, False) and is_exporting:
            flow = 800 + np.random.normal(0, 40)
            vib = 1.8 + np.random.normal(0, 0.4) + degradation * 0.3
            temp = 75 + np.random.normal(0, 5) + degradation * 8
        else:
            flow = 0
            vib = 0.3 + np.random.normal(0, 0.1)
            temp = 40 + np.random.normal(0, 2)

        data[f"{pump_key}_flow"] = max(0, flow)
        data[f"{pump_key}_vib"] = round(float(vib), 3)
        data[f"{pump_key}_temp"] = round(float(temp), 1)

    data['export_flow_rate'] = sum([data[f"{p}_flow"] for p in ["CargoPump_A", "CargoPump_B", "CargoPump_C"]])

    # Ballast pumps & tank levels
    data['BallastPump_Port_flow'] = 300 + np.random.normal(0, 30)
    data['BallastPump_Stbd_flow'] = 300 + np.random.normal(0, 30)
    for i in range(1, 7):
        data[f'Ballast_Port_{i}_level'] = round(60 + np.random.normal(0, 6), 2)
        data[f'Ballast_Stbd_{i}_level'] = round(58 + np.random.normal(0, 6), 2)
    data['Forepeak_Tank_level'] = round(65 + np.random.normal(0, 4), 2)

    # Diesel Generators
    data['DG1_power'] = max(0, 3500 + np.random.normal(0, 200))
    data['DG2_power'] = max(0, 3200 + np.random.normal(0, 250))
    data['DG1_temp'] = 85 + np.random.normal(0, 5) + degradation * 6
    data['DG2_temp'] = 83 + np.random.normal(0, 6) + degradation * 5
    data['DG1_vib'] = 1.4 + np.random.normal(0, 0.3) + degradation * 0.2
    data['DG2_vib'] = 1.5 + np.random.normal(0, 0.4) + degradation * 0.3
    data['DG1_fuel_rate'] = 280 + np.random.normal(0, 15)
    data['DG2_fuel_rate'] = 270 + np.random.normal(0, 20)

    # Boiler & heating system
    data['Boiler_pressure'] = 8.5 + np.random.normal(0, 0.3)
    data['Boiler_temp'] = 125 + np.random.normal(0, 8)
    data['cargo_heating_temp'] = 42 + np.random.normal(0, 2)

    # IGS
    data['IGS_generator_temp'] = 70 + np.random.normal(0, 4)
    data['IGS_main_pressure'] = 0.16 + np.random.normal(0, 0.02)
    data['IGS_flow_rate'] = 1200 + np.random.normal(0, 80)
    data['IGS_O2_content'] = 2.1 + np.random.normal(0, 0.3)

    # Cargo tanks
    for i in range(1, 7):
        data[f'Cargo_Tank_{i}_level'] = round(80 + np.random.normal(0, 5), 2)
        data[f'Cargo_Tank_{i}_temp'] = round(40 + np.random.normal(0, 3), 2)

    # Hull / structural
    data['heel_angle'] = round(0.2 + np.sin(time_factor) * 0.8 + np.random.normal(0, 0.02), 3)
    data['trim_angle'] = round(0.3 + np.cos(time_factor) * 0.6 + np.random.normal(0, 0.02), 3)
    data['hull_stress'] = round(22 + abs(np.sin(time_factor)) * 15 + degradation * 5 + np.random.normal(0, 1.5), 3)
    data['bending_moment'] = round(1100 + np.random.normal(0, 80), 2)
    data['shear_force'] = round(750 + np.random.normal(0, 60), 2)

    # Totals (кумулятивные)
    data['total_cargo_loaded'] = min(90000, cycle * 45)
    data['total_cargo_exported'] = min(85000, max(0, cycle - 150) * 40)

    # Fault injection overrides
    if faults.get("CargoPump_A_failure"):
        data['CargoPump_A_flow'] = 0
        data['CargoPump_A_vib'] = 5.0
        data['CargoPump_A_temp'] = 120
    if faults.get("CargoPump_B_failure"):
        data['CargoPump_B_flow'] = 0
        data['CargoPump_B_vib'] = 5.0
        data['CargoPump_B_temp'] = 120
    if faults.get("DG1_overheat"):
        data['DG1_temp'] += 30
        data['DG1_power'] *= 0.5
    if faults.get("DG2_overheat"):
        data['DG2_temp'] += 30
        data['DG2_power'] *= 0.5
    if faults.get("IGS_low_pressure"):
        data['IGS_main_pressure'] = 0.05
        data['IGS_flow_rate'] *= 0.5

    return data

# =========================
# PLOT HELPERS
# =========================
def create_operations_dashboard(data):
    fig = go.Figure()
    # import & export as indicators
    fig.add_trace(go.Indicator(mode="number", value=data['import_flow_rate'],
                               title={"text": "Import Flow (m³/h)"},
                               domain={'x': [0, 0.45], 'y': [0.55, 1]}))
    fig.add_trace(go.Indicator(mode="number", value=data['export_flow_rate'],
                               title={"text": "Export Flow (m³/h)"},
                               domain={'x': [0.55, 1], 'y': [0.55, 1]}))
    # totals
    fig.add_trace(go.Indicator(mode="number", value=data['total_cargo_loaded'],
                               title={"text": "Total Loaded (m³)"},
                               domain={'x': [0, 0.3], 'y': [0, 0.45]},
                               number={'valueformat': ",.0f"}))
    fig.add_trace(go.Indicator(mode="number", value=data['total_cargo_exported'],
                               title={"text": "Total Exported (m³)"},
                               domain={'x': [0.35, 0.65], 'y': [0, 0.45]},
                               number={'valueformat': ",.0f"}))
    fig.add_trace(go.Indicator(mode="number", value=max(0, data['total_cargo_loaded'] - data['total_cargo_exported']),
                               title={"text": "Current Cargo (m³)"},
                               domain={'x': [0.7, 1], 'y': [0, 0.45]},
                               number={'valueformat': ",.0f"}))

    fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10), title="Cargo Operations Overview")
    return fig

def create_pump_room_monitoring(data):
    pumps = ['CargoPump_A', 'CargoPump_B', 'CargoPump_C']
    vib_vals = [data[f'{p}_vib'] for p in pumps]
    temp_vals = [data[f'{p}_temp'] for p in pumps]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Vibration (mm/s)',
        x=pumps,
        y=vib_vals,
        text=[f"{v:.2f}" for v in vib_vals],
        textposition='auto',
        marker_color=[('red' if v > 2.5 else 'orange' if v > 1.8 else 'green') for v in vib_vals]
    ))
    fig.add_trace(go.Scatter(
        name='Temperature (°C)',
        x=pumps,
        y=temp_vals,
        mode='lines+markers+text',
        text=[f"{t:.0f}°C" for t in temp_vals],
        textposition='top center',
        yaxis='y2'
    ))
    fig.update_layout(title="Pump Room: Vibration & Temperature", height=380,
                      yaxis=dict(title="Vibration (mm/s)"),
                      yaxis2=dict(title="Temperature (°C)", overlaying='y', side='right'))
    return fig

def create_ballast_monitoring(data):
    # средние уровни порт/стбд
    port_levels = [data[f'Ballast_Port_{i}_level'] for i in range(1, 7)]
    stbd_levels = [data[f'Ballast_Stbd_{i}_level'] for i in range(1, 7)]
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Port ballast levels', x=[f'P{i}' for i in range(1,7)], y=port_levels))
    fig.add_trace(go.Bar(name='Stbd ballast levels', x=[f'S{i}' for i in range(1,7)], y=stbd_levels))
    fig.update_layout(barmode='group', title="Ballast Tank Levels (%)", height=350)
    return fig

def create_hull_monitoring(history):
    if not history:
        return go.Figure()
    cycles = [d['cycle'] for d in history]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cycles, y=[d['heel_angle'] for d in history], mode='lines', name='Heel Angle (°)'))
    fig.add_trace(go.Scatter(x=cycles, y=[d['trim_angle'] for d in history], mode='lines', name='Trim Angle (°)'))
    fig.add_trace(go.Scatter(x=cycles, y=[d['hull_stress'] for d in history], mode='lines', name='Hull Stress'))
    fig.add_trace(go.Scatter(x=cycles, y=[d['bending_moment'] for d in history], mode='lines', name='Bending Moment'))
    fig.add_trace(go.Scatter(x=cycles, y=[d['shear_force'] for d in history], mode='lines', name='Shear Force'))
    fig.update_layout(title="Hull Stability & Structural Monitoring", xaxis_title="Cycle", height=420)
    return fig

# =========================
# MAIN APP
# =========================
def main():
    st.set_page_config(page_title="FPSO Spirit - Simulator", layout="wide")
    st.title("🌊 FPSO Spirit - Реальный симулятор процессов (step & continuous)")
    st.markdown("**Управление насосами, Fault Injection, Hull Monitoring, Ballast, DG, IGS, Boiler**")

    # --- session state init
    if "cycle_count" not in st.session_state:
        st.session_state.cycle_count = 0
    if "system_data" not in st.session_state:
        st.session_state.system_data = generate_realistic_fpso_data(0)
    if "history" not in st.session_state:
        st.session_state.history = [st.session_state.system_data]
    if "monitoring_active" not in st.session_state:
        st.session_state.monitoring_active = False
    if "stop_requested" not in st.session_state:
        st.session_state.stop_requested = False

    # Sidebar controls
    st.sidebar.header("⚙️ CCR Control Panel")
    st.sidebar.subheader("Cargo Pumps Control (ручной)")
    pump_a_on = st.sidebar.checkbox("Cargo Pump A (A)", value=True)
    pump_b_on = st.sidebar.checkbox("Cargo Pump B (B)", value=True)
    pump_c_on = st.sidebar.checkbox("Cargo Pump C (C) - Standby", value=False)
    pump_status = {"CargoPump_A": pump_a_on, "CargoPump_B": pump_b_on, "CargoPump_C": pump_c_on}

    st.sidebar.markdown("---")
    st.sidebar.subheader("🚨 Fault Injection (вкл. вручную)")
    faults = {
        "CargoPump_A_failure": st.sidebar.checkbox("Failure: Cargo Pump A"),
        "CargoPump_B_failure": st.sidebar.checkbox("Failure: Cargo Pump B"),
        "CargoPump_C_failure": st.sidebar.checkbox("Failure: Cargo Pump C"),
        "DG1_overheat": st.sidebar.checkbox("Overheat: DG1"),
        "DG2_overheat": st.sidebar.checkbox("Overheat: DG2"),
        "IGS_low_pressure": st.sidebar.checkbox("Low Pressure: IGS"),
    }

    st.sidebar.markdown("---")
    st.sidebar.subheader("▶️ Управление мониторингом")
    # step / continuous controls
    step_btn = st.sidebar.button("Step ▶ (один цикл)")
    start_btn = st.sidebar.button("Start Continuous ▶")
    stop_btn = st.sidebar.button("Stop ⏸")
    continuous_steps = st.sidebar.number_input("Steps per run (continuous)", min_value=1, max_value=1000, value=10, step=1)
    interval_seconds = st.sidebar.slider("Interval (seconds)", min_value=0.1, max_value=5.0, value=0.6, step=0.1)
    auto_fault_prob = st.sidebar.slider("Auto fault probability per cycle", min_value=0.0, max_value=0.2, value=0.0, step=0.01)

    # Handle buttons
    if stop_btn:
        st.session_state.monitoring_active = False
        st.session_state.stop_requested = True

    if start_btn:
        st.session_state.monitoring_active = True
        st.session_state.stop_requested = False

    # Placeholders for UI regions (so we can update in loop)
    ops_placeholder = st.empty()
    left_col, right_col = st.columns([2, 1])
    pump_placeholder = left_col.empty()
    ballast_placeholder = left_col.empty()
    power_placeholder = right_col.empty()
    hull_placeholder = st.empty()

    # internal function to update UI instantly
    def update_ui(data, history):
        # Ops
        with ops_placeholder.container():
            st.subheader("📊 Operations Overview")
            fig_ops = create_operations_dashboard(data)
            st.plotly_chart(fig_ops, use_container_width=True)

        # Pump room and ballast (left column)
        with pump_placeholder.container():
            st.subheader("🏭 Pump Room Monitoring")
            fig_pumps = create_pump_room_monitoring(data)
            st.plotly_chart(fig_pumps, use_container_width=True)

        with ballast_placeholder.container():
            st.subheader("🚰 Ballast System")
            fig_ballast = create_ballast_monitoring(data)
            st.plotly_chart(fig_ballast, use_container_width=True)

        # Power / IGS / Boiler (right column)
        with power_placeholder.container():
            st.subheader("⚡ Power / IGS / Boiler")
            cols = st.columns(1)
            # display metrics in compact form
            st.metric("DG1 Power (kW)", f"{data['DG1_power']:.0f}")
            st.metric("DG1 Temp (°C)", f"{data['DG1_temp']:.0f}")
            st.metric("DG2 Power (kW)", f"{data['DG2_power']:.0f}")
            st.metric("DG2 Temp (°C)", f"{data['DG2_temp']:.0f}")
            st.markdown("---")
            st.metric("Boiler Pressure (bar)", f"{data['Boiler_pressure']:.2f}")
            st.metric("Boiler Temp (°C)", f"{data['Boiler_temp']:.0f}")
            st.markdown("---")
            st.metric("IGS Pressure (bar)", f"{data['IGS_main_pressure']:.3f}")
            st.metric("IGS Flow (m³/h)", f"{data['IGS_flow_rate']:.0f}")
            st.metric("IGS O₂ (%)", f"{data['IGS_O2_content']:.2f}")

        # Hull condition (history)
        with hull_placeholder.container():
            st.subheader("⚓ Hull Condition (history)")
            fig_hull = create_hull_monitoring(history)
            st.plotly_chart(fig_hull, use_container_width=True)

    # If user pressed Step — perform one update cycle
    if step_btn:
        st.session_state.cycle_count += 1
        data = generate_realistic_fpso_data(st.session_state.cycle_count, pump_status=pump_status, faults=faults, auto_fault_prob=auto_fault_prob)
        st.session_state.system_data = data
        st.session_state.history.append(data)
        if len(st.session_state.history) > 100:
            st.session_state.history.pop(0)
        update_ui(data, st.session_state.history)

    # If monitoring is active -> perform continuous run for 'continuous_steps'
    if st.session_state.monitoring_active:
        # run a short loop (blocking for the requested steps). Stop button takes effect between iterations.
        for i in range(int(continuous_steps)):
            if st.session_state.stop_requested:
                st.session_state.monitoring_active = False
                break
            st.session_state.cycle_count += 1
            data = generate_realistic_fpso_data(st.session_state.cycle_count, pump_status=pump_status, faults=faults, auto_fault_prob=auto_fault_prob)
            st.session_state.system_data = data
            st.session_state.history.append(data)
            if len(st.session_state.history) > 100:
                st.session_state.history.pop(0)

            update_ui(data, st.session_state.history)

            # небольшой пауз (интервал)
            time.sleep(float(interval_seconds))

        # закончился batch run
        st.session_state.monitoring_active = False

    # При обычном запуске (нет step / continuous) показываем текущие сохранённые данные
    if not step_btn and not st.session_state.monitoring_active:
        update_ui(st.session_state.system_data, st.session_state.history)

    # Информативная панель внизу
    st.markdown("---")
    st.write(f"Cycle: **{st.session_state.cycle_count}** — History length: **{len(st.session_state.history)}**")
    st.write("Примечания: кнопка **Step** выполняет единичный цикл. **Start Continuous** запустит серию циклов (кол-во и интервал выбираются в боковой панели)."
             " Для полной интерактивности используйте короткие значения `Steps per run`.")

if __name__ == "__main__":
    main()
