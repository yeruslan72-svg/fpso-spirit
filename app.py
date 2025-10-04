# app.py - СУПЕР-ОПТИМИЗИРОВАННАЯ ВЕРСИЯ
import streamlit as st
import time
from datetime import datetime

class FPSSimple:
    def __init__(self):
        self.project_name = "FPSO SPIRIT"
        self.version = "1.0"
        
        if 'systems' not in st.session_state:
            self._init_simple_systems()
    
    def _init_simple_systems(self):
        """Только самые базовые системы"""
        st.session_state.systems = {
            'cargo_tanks': {
                'TANK_1': {'volume': 12000, 'capacity': 15000, 'valve': False},
                'TANK_2': {'volume': 12000, 'capacity': 15000, 'valve': False},
                'TANK_3': {'volume': 12000, 'capacity': 15000, 'valve': False},
            },
            'pumps': {
                'PUMP_1': {'running': False, 'flow': 0},
                'PUMP_2': {'running': False, 'flow': 0},
            },
            'esd_level': 0,
            'total_cargo': 36000
        }
        st.session_state.last_update = datetime.now()
    
    def run(self):
        st.set_page_config(
            page_title="FPSO Simulator",
            page_icon="⚓",
            layout="wide"
        )
        
        st.title("⚓ FPSO SPIRIT - CCR Simulator")
        st.caption("Ultra-Light Version - Optimized for Streamlit Cloud")
        
        # Простая навигация
        tab1, tab2, tab3 = st.tabs(["🏠 ГЛАВНАЯ", "🛢️ ГРУЗ", "🚨 БЕЗОПАСНОСТЬ"])
        
        with tab1:
            self._main_dashboard()
        with tab2:
            self._cargo_operations()
        with tab3:
            self._safety_panel()
    
    def _main_dashboard(self):
        """Упрощенная главная панель"""
        systems = st.session_state.systems
        
        st.header("🎛️ ЦЕНТРАЛЬНЫЙ ЩИТ")
        
        # Статусы
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ESD", f"Уровень {systems['esd_level']}")
        with col2:
            st.metric("Груз", f"{systems['total_cargo']:,.0f} m³")
        with col3:
            active_pumps = sum(1 for p in systems['pumps'].values() if p['running'])
            st.metric("Насосы", f"{active_pumps}/2")
        
        # Быстрые действия
        st.subheader("🚀 БЫСТРЫЕ ДЕЙСТВИЯ")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📤 НАЧАТЬ ОТГРУЗКУ", use_container_width=True):
                st.success("Открыты клапаны TANK_1, TANK_2. Запустите насосы.")
        with col2:
            if st.button("📥 НАЧАТЬ ПОГРУЗКУ", use_container_width=True):
                st.info("Подготовка к погрузке...")
        with col3:
            if st.button("🔄 ОБНОВИТЬ", use_container_width=True):
                st.rerun()
    
    def _cargo_operations(self):
        """Упрощенное управление грузом"""
        systems = st.session_state.systems
        
        st.header("🛢️ ГРУЗОВЫЕ ОПЕРАЦИИ")
        
        # Управление танками
        st.subheader("🎛️ КЛАПАНЫ ТАНКОВ")
        for tank_name, tank_data in systems['cargo_tanks'].items():
            col1, col2 = st.columns([2, 1])
            with col1:
                new_valve = st.checkbox(
                    f"{tank_name} ({tank_data['volume']:,.0f}/{tank_data['capacity']:,.0f} m³)",
                    value=tank_data['valve'],
                    key=f"valve_{tank_name}"
                )
                if new_valve != tank_data['valve']:
                    systems['cargo_tanks'][tank_name]['valve'] = new_valve
                    st.rerun()
            with col2:
                percentage = (tank_data['volume'] / tank_data['capacity']) * 100
                st.progress(percentage / 100)
        
        # Управление насосами
        st.subheader("⚙️ НАСОСЫ")
        for pump_name, pump_data in systems['pumps'].items():
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button(
                    f"{'⏹️ ОСТАНОВИТЬ' if pump_data['running'] else '▶️ ЗАПУСТИТЬ'} {pump_name}",
                    use_container_width=True,
                    key=f"pump_{pump_name}"
                ):
                    systems['pumps'][pump_name]['running'] = not pump_data['running']
                    systems['pumps'][pump_name]['flow'] = 800 if not pump_data['running'] else 0
                    st.rerun()
            with col2:
                st.write(f"Расход: {pump_data['flow']} m³/h")
    
    def _safety_panel(self):
        """Упрощенная панель безопасности"""
        systems = st.session_state.systems
        
        st.header("🚨 СИСТЕМА БЕЗОПАСНОСТИ")
        
        # ESD управление
        st.subheader("🛑 АВАРИЙНЫЙ ОСТАНОВ")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🟡 ESD-1", use_container_width=True, disabled=systems['esd_level'] >= 1):
                systems['esd_level'] = 1
                st.rerun()
        with col2:
            if st.button("🟠 ESD-2", use_container_width=True, disabled=systems['esd_level'] >= 2):
                systems['esd_level'] = 2
                st.rerun()
        with col3:
            if st.button("🔴 ESD-3", use_container_width=True, disabled=systems['esd_level'] >= 3):
                systems['esd_level'] = 3
                st.rerun()
        
        # Сброс ESD
        if systems['esd_level'] > 0:
            if st.button("🔄 СБРОС ESD", use_container_width=True):
                systems['esd_level'] = 0
                st.success("ESD сброшена!")
                st.rerun()
        
        # Предупреждения
        st.subheader("⚠️ ПРЕДУПРЕЖДЕНИЯ")
        for tank_name, tank_data in systems['cargo_tanks'].items():
            percentage = (tank_data['volume'] / tank_data['capacity']) * 100
            if percentage > 95:
                st.error(f"🔴 ПЕРЕПОЛНЕНИЕ {tank_name}: {percentage:.1f}%")
            elif percentage > 85:
                st.warning(f"🟡 ВЫСОКИЙ УРОВЕНЬ {tank_name}: {percentage:.1f}%")
        
        if all(tank['volume'] / tank['capacity'] < 0.8 for tank in systems['cargo_tanks'].values()):
            st.success("✅ ВСЕ СИСТЕМЫ В НОРМЕ")

if __name__ == "__main__":
    simulator = FPSSimple()
    simulator.run()
