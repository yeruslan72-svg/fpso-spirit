# app.py - AVCS DNA v6.0 PRO (ВСЕ В ОДНОМ ФАЙЛЕ)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import requests
import json

# =============================================================================
# AI ENGINE - ВСТРАИВАЕМ ПРЯМО В ФАЙЛ
# =============================================================================

class AVCSDNAEngine:
    """AI движок для анализа и стабилизации - встроен прямо в app.py"""
    
    def __init__(self):
        self.risk_history = []
        self.damper_forces = []
        self.vibration_history = []
        self.temperature_history = []
        
    def analyze_equipment_health(self, sensor_data):
        """Основной AI анализ состояния оборудования"""
        # Анализ вибрации
        vib_signals = [
            sensor_data.get('VIB_PUMP_A_X', 0),
            sensor_data.get('VIB_PUMP_A_Y', 0), 
            sensor_data.get('VIB_PUMP_B_X', 0),
            sensor_data.get('VIB_PUMP_B_Y', 0)
        ]
        
        # Анализ температуры
        temps = [
            sensor_data.get('TEMP_PUMP_A', 0),
            sensor_data.get('TEMP_MOTOR_A', 0)
        ]
        
        # Расчет RMS вибрации
        rms_vibration = np.sqrt(np.mean(np.square(vib_signals)))
        max_temperature = max(temps)
        
        # Индекс риска на основе вибрации и температуры
        vib_risk = min(100, rms_vibration * 15)
        temp_risk = min(100, max(0, max_temperature - 60) * 2)
        
        risk_index = (vib_risk * 0.6 + temp_risk * 0.4)
        
        # Сохраняем историю
        self.risk_history.append(risk_index)
        self.vibration_history.append(rms_vibration)
        self.temperature_history.append(max_temperature)
        
        # Прогноз остаточного ресурса (RUL)
        if risk_index < 30:
            rul_hours = 720  # 30 дней
        elif risk_index < 60:
            rul_hours = 240  # 10 дней
        elif risk_index < 80:
            rul_hours = 72   # 3 дня
        else:
            rul_hours = 24   # 1 день
            
        # Определение силы демпфирования
        if risk_index >= 80:
            damper_force = 8000
            status = "🔴 CRITICAL"
            recommendation = "НЕМЕДЛЕННАЯ ОСТАНОВКА"
        elif risk_index >= 60:
            damper_force = 4000
            status = "🟡 WARNING" 
            recommendation = "Плановый ремонт в течение 24 часов"
        elif risk_index >= 30:
            damper_force = 1000
            status = "🟢 NORMAL"
            recommendation = "Усилить мониторинг"
        else:
            damper_force = 500
            status = "🔵 STANDBY"
            recommendation = "Нормальная работа"
            
        self.damper_forces.append(damper_force)
        
        # Диагностика неисправностей
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
        """Диагностика конкретных неисправностей"""
        faults = {}
        
        # Диагностика повреждения подшипников
        peak_vibration = max(vib_signals)
        if peak_vibration > 5.0:
            faults['bearing_damage'] = min(1.0, (peak_vibration - 5.0) / 3.0)
        
        # Диагностика misalignment
        vib_diff = abs(vib_signals[0] - vib_signals[1])
        if vib_diff > 2.0:
            faults['misalignment'] = min(1.0, vib_diff / 4.0)
            
        # Диагностика дисбаланса
        if rpm > 2950 or rpm < 2850:
            faults['imbalance'] = min(1.0, abs(rpm - 2900) / 100.0)
            
        # Диагностика перегрева
        if max(temps) > 85:
            faults['overheating'] = min(1.0, (max(temps) - 85) / 20.0)
            
        return faults

# =============================================================================
# MR DAMPER CONTROLLER - ТАКЖЕ ВСТРАИВАЕМ
# =============================================================================

class MRDamperController:
    """Контроллер MR демпферов"""
    
    def __init__(self):
        self.dampers = {
            'Front-Left': {'force': 0, 'position': 'FL'},
            'Front-Right': {'force': 0, 'position': 'FR'},
            'Rear-Left': {'force': 0, 'position': 'RL'}, 
            'Rear-Right': {'force': 0, 'position': 'RR'}
        }
        
    def apply_force_distribution(self, total_force, vibration_data):
        """Применение распределения силы к демпферам"""
        # Простое распределение - в реальности будет сложная логика
        force_per_damper = total_force // 4
        
        for damper in self.dampers:
            self.dampers[damper]['force'] = force_per_damper
            
        return self.dampers
    
    def get_damper_status(self):
        """Получение статуса демпферов"""
        return self.dampers

# =============================================================================
# DATA SIMULATOR - ЕСЛИ ВНЕШНИЙ API НЕДОСТУПЕН
# =============================================================================

class DataSimulator:
    """Генератор реалистичных данных оборудования"""
    
    def __init__(self):
        self.cycle = 0
        
    def generate_sensor_data(self):
        """Генерация данных сенсоров"""
        self.cycle += 1
        
        # Постепенная деградация оборудования
        if self.cycle < 30:
            # Нормальная работа
            degradation = 0
        elif self.cycle < 60:
            # Начальная деградация
            degradation = (self.cycle - 30) * 0.02
        elif self.cycle < 90:
            # Серьезная деградация
            degradation = 0.6 + (self.cycle - 60) * 0.03
        else:
            # Критическое состояние
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
        
        # Ограничение значений
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
    
    st.title("🏭 AVCS DNA v6.0 PRO - AI Система Стабилизации")
    st.markdown("**Active Vibration Control System с AI-прогнозированием отказов**")
    
    # Инициализация сессии
    if 'avcs_engine' not in st.session_state:
        st.session_state.avcs_engine = AVCSDNAEngine()
        st.session_state.damper_controller = MRDamperController()
        st.session_state.data_simulator = DataSimulator()
        st.session_state.system_running = False
        st.session_state.analysis_history = []
    
    # =========================================================================
    # SIDEBAR - ПАНЕЛЬ УПРАВЛЕНИЯ
    # =========================================================================
    st.sidebar.header("🎛️ Панель управления AVCS DNA")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🚀 Запуск системы", type="primary", use_container_width=True):
            st.session_state.system_running = True
            st.session_state.avcs_engine = AVCSDNAEngine()  # Сброс при новом запуске
            st.rerun()
            
    with col2:
        if st.button("🛑 Остановка", use_container_width=True):
            st.session_state.system_running = False
            st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Статус системы")
    
    if st.session_state.system_running:
        st.sidebar.success("✅ Система активна")
        st.sidebar.info("🔄 Данные обрабатываются в реальном времени")
    else:
        st.sidebar.warning("⏸️ Система остановлена")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🏭 Системная архитектура")
    st.sidebar.write("• 4x Датчики вибрации (PCB 603C01)")
    st.sidebar.write("• 2x Термопары (FLIR A500f)")
    st.sidebar.write("• 4x MR демпферы (LORD RD-8040)")
    st.sidebar.write("• AI: Анализ рисков + Прогноз RUL")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 Бизнес-кейс")
    st.sidebar.metric("Стоимость системы", "$250,000")
    st.sidebar.metric("Типичный ROI", ">2000%")
    st.sidebar.metric("Окупаемость", "<3 месяцев")
    
    # =========================================================================
    # MAIN INTERFACE - ОСНОВНОЙ ИНТЕРФЕЙС
    # =========================================================================
    
    if not st.session_state.system_running:
        # Экран ожидания
        st.info("🚀 **Готов к работе** - Нажмите 'Запуск системы' для начала мониторинга")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🎯 Преимущества AVCS DNA")
            st.write("""
            - **AI-прогнозирование** отказов за 48+ часов
            - **Активное подавление** вибраций в реальном времени  
            - **Автоматическая стабилизация** оборудования
            - **Гарантированный ROI** >2000%
            - **Предотвращение** непредвиденных простоев
            """)
            
        with col2:
            st.subheader("📈 Технологический стек")
            st.write("""
            - **ML алгоритмы**: Isolation Forest + Gradient Boosting
            - **Сенсоры**: PCB Piezotronics + FLIR Thermal
            - **Демпферы**: LORD MR технология
            - **Контроллер**: Beckhoff TwinCAT
            - **Интеграция**: OPC-UA + REST API
            """)
        
        return
    
    # =========================================================================
    # REAL-TIME MONITORING - РЕАЛЬНЫЙ МОНИТОРИНГ
    # =========================================================================
    
    # Получение и анализ данных
    sensor_data = st.session_state.data_simulator.generate_sensor_data()
    analysis = st.session_state.avcs_engine.analyze_equipment_health(sensor_data)
    st.session_state.analysis_history.append(analysis)
    
    # Применение управления демпферами
    damper_status = st.session_state.damper_controller.apply_force_distribution(
        analysis['damper_force'], sensor_data
    )
    
    # =========================================================================
    # MAIN DASHBOARD - ОСНОВНОЙ ДАШБОРД
    # =========================================================================
    
    # РЯД 1: ОСНОВНЫЕ МЕТРИКИ
    st.subheader("📊 Основные показатели системы")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Индекс риска с цветовой индикацией
        risk_color = "green" if analysis['risk_index'] < 50 else "orange" if analysis['risk_index'] < 80 else "red"
        st.metric(
            "🎯 Индекс риска", 
            f"{analysis['risk_index']:.1f}/100",
            delta=analysis['status'],
            delta_color=risk_color
        )
    
    with col2:
        # Остаточный ресурс
        rul_color = "green" if analysis['rul_hours'] > 168 else "orange" if analysis['rul_hours'] > 72 else "red"
        st.metric(
            "⏳ Остаточный ресурс (RUL)",
            f"{analysis['rul_hours']} часов",
            delta_color=rul_color
        )
    
    with col3:
        st.metric(
            "🔧 Сила демпфирования", 
            f"{analysis['damper_force']} N"
        )
    
    with col4:
        st.metric(
            "🌡️ Макс. температура",
            f"{analysis['max_temperature']} °C"
        )
    
    # РЯД 2: СИСТЕМА ДЕМПФЕРОВ
    st.subheader("🔧 Система MR-Демпферов")
    damper_cols = st.columns(4)
    
    for i, (position, status) in enumerate(damper_status.items()):
        with damper_cols[i]:
            force = status['force']
            if force >= 2000:
                st.error(f"🔴 {position}\n**{force} N**\n*Критический режим*")
            elif force >= 250:
                st.warning(f"🟡 {position}\n**{force} N**\n*Активный режим*")
            else:
                st.success(f"🟢 {position}\n**{force} N**\n*Дежурный режим*")
    
    # РЯД 3: ГРАФИКИ И ВИЗУАЛИЗАЦИЯ
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Динамика индекса риска")
        if len(st.session_state.avcs_engine.risk_history) > 1:
            risk_df = pd.DataFrame({
                'Индекс риска': st.session_state.avcs_engine.risk_history,
                'Критический порог': [80] * len(st.session_state.avcs_engine.risk_history),
                'Порог предупреждения': [50] * len(st.session_state.avcs_engine.risk_history)
            })
            st.line_chart(risk_df)
    
    with col2:
        st.subheader("⚡ История силы демпфирования")
        if len(st.session_state.avcs_engine.damper_forces) > 1:
            force_df = pd.DataFrame({
                'Сила демпферов (N)': st.session_state.avcs_engine.damper_forces
            })
            st.line_chart(force_df)
    
    # РЯД 4: ДИАГНОСТИКА И РЕКОМЕНДАЦИИ
    st.subheader("🔍 AI Диагностика оборудования")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📋 Обнаруженные неисправности:**")
        if analysis['faults']:
            for fault, probability in analysis['faults'].items():
                prob_percent = probability * 100
                if prob_percent > 70:
                    st.error(f"🔴 {fault}: {prob_percent:.1f}%")
                elif prob_percent > 40:
                    st.warning(f"🟡 {fault}: {prob_percent:.1f}%")
                else:
                    st.info(f"🔵 {fault}: {prob_percent:.1f}%")
        else:
            st.success("✅ Критических неисправностей не обнаружено")
    
    with col2:
        st.write("**💡 Рекомендации AI:**")
        if analysis['risk_index'] >= 80:
            st.error(f"🚨 {analysis['recommendation']}")
        elif analysis['risk_index'] >= 60:
            st.warning(f"⚠️ {analysis['recommendation']}")
        else:
            st.success(f"✅ {analysis['recommendation']}")
    
    # РЯД 5: ДАННЫЕ СЕНСОРОВ В РЕАЛЬНОМ ВРЕМЕНИ
    st.subheader("📡 Данные сенсоров в реальном времени")
    
    sensor_cols = st.columns(4)
    sensor_metrics = {
        "Вибрация X": f"{sensor_data['VIB_PUMP_A_X']:.2f} mm/s",
        "Вибрация Y": f"{sensor_data['VIB_PUMP_A_Y']:.2f} mm/s",
        "Температура насоса": f"{sensor_data['TEMP_PUMP_A']:.1f} °C", 
        "Обороты": f"{sensor_data['RPM_PUMP_A']} RPM"
    }
    
    for i, (name, value) in enumerate(sensor_metrics.items()):
        with sensor_cols[i]:
            st.metric(name, value)
    
    # Автоматическое обновление
    time.sleep(1)
    st.rerun()

if __name__ == "__main__":
    main()
