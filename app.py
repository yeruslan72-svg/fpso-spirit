# app.py - ОПТИМИЗИРОВАННАЯ ВЕРСИЯ
import streamlit as st
import time
from datetime import datetime
import numpy as np

class FPSOSpiritLite:
    def __init__(self):
        self.project_name = "FPSO SPIRIT LITE"
        self.version = "4.0"
        self.update_interval = 10  # 10 секунд вместо 2
        self.simple_mode = True
        
        if 'systems' not in st.session_state:
            self._initialize_lightweight_systems()
    
    def _initialize_lightweight_systems(self):
        """Инициализация только основных систем"""
        from core.system_state_lite import SystemStateLite
        from modules.cargo_system_lite import CargoSystemLite
        from modules.ballast_system_lite import BallastSystemLite
        from modules.esd_system_lite import ESDSystemLite
        
        st.session_state.systems = {
            'system_state': SystemStateLite(),
            'cargo': CargoSystemLite(),
            'ballast': BallastSystemLite(),
            'esd': ESDSystemLite(),
        }
        st.session_state.last_update = datetime.now()
        st.session_state.auto_refresh = False
    
    def run_optimized(self):
        # Минималистичная конфигурация
        st.set_page_config(
            page_title="FPSO SPIRIT - CCR Simulator",
            page_icon="⚓",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Минимальный CSS
        st.markdown("""
        <style>
        .main-title { text-align: center; color: #1E90FF; font-size: 2rem; margin-bottom: 0; }
        .metric-card { border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin: 5px 0; }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f'<h1 class="main-title">⚓ FPSO SPIRIT LITE</h1>', unsafe_allow_html=True)
        st.caption(f"Optimized for Streamlit • v{self.version}")
        
        # УПРАВЛЕНИЕ ОБНОВЛЕНИЕМ
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info("🔧 **Режим оптимизации**: Упрощенные расчеты для стабильной работы")
        with col2:
            if st.button("🔄 Обновить вручную", use_container_width=True):
                st.rerun()
        
        # Автообновление только если включено (по умолчанию выключено)
        auto_refresh = st.checkbox("Автообновление (каждые 10 сек)", value=False)
        if auto_refresh and time.time() - st.session_state.last_update.timestamp() > self.update_interval:
            self._update_systems_lightweight()
            st.session_state.last_update = datetime.now()
            st.rerun()
        
        # ОСНОВНЫЕ ВКЛАДКИ
        tab1, tab2, tab3, tab4 = st.tabs([
            "🏠 ГЛАВНЫЙ ЩИТ", 
            "🛢️ ГРУЗОВЫЕ ОПЕР.",
            "🌊 БАЛЛАСТ", 
            "🚨 БЕЗОПАСНОСТЬ"
        ])
        
        with tab1:
            self._render_main_dashboard_lite()
        with tab2:
            self._render_cargo_lite()
        with tab3:
            self._render_ballast_lite()
        with tab4:
            self._render_safety_lite()
    
    def _update_systems_lightweight(self):
        """Упрощенное обновление систем"""
        try:
            systems = st.session_state.systems
            
            # Только базовые расчеты
            systems['cargo'].calculate_flows_simple()
            systems['ballast'].calculate_ballast_simple(systems['system_state'])
            systems['esd'].check_critical_triggers(systems)
            
        except Exception as e:
            st.error(f"Ошибка обновления: {str(e)}")
    
    def _render_main_dashboard_lite(self):
        """Упрощенный главный щит"""
        systems = st.session_state.systems
        
        st.header("🎛️ ЦЕНТРАЛЬНЫЙ ЩИТ")
        
        # КРИТИЧЕСКИЕ СТАТУСЫ
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # ESD статус
            esd_active = any([systems['esd'].esd_level_1, systems['esd'].esd_level_2])
            st.metric("ESD", "🔴 АКТИВ" if esd_active else "🟢 НОРМА")
            
        with col2:
            # Переполнение танков
            overflow = any(tank.volume_percentage > 95 for tank in systems['cargo'].tanks.values())
            st.metric("ТАНКИ", "🔴 ПЕРЕПОЛН." if overflow else "🟢 НОРМА")
            
        with col3:
            # Крен
            heel_status = "🔴 ОПАСНО" if abs(systems['system_state'].heel) > 8 else "🟡 ВНИМАНИЕ" if abs(systems['system_state'].heel) > 5 else "🟢 НОРМА"
            st.metric("КРЕН", heel_status)
            
        with col4:
            # Общий груз
            st.metric("ГРУЗ", f"{systems['cargo'].total_cargo_onboard:,.0f} m³")
        
        # БЫСТРЫЕ ОПЕРАЦИИ
        st.subheader("🚀 БЫСТРЫЕ ДЕЙСТВИЯ")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("📤 НАЧАТЬ ОТГРУЗКУ", use_container_width=True):
                st.info("Отгрузка: 1. Откройте клапаны 2. Запустите насосы")
                
        with col2:
            if st.button("📥 НАЧАТЬ ПОГРУЗКУ", use_container_width=True):
                st.info("Погрузка: 1. Подготовьте танки 2. Откройте клапаны")
                
        with col3:
            if st.button("🌊 КОРРЕКТИРОВАТЬ БАЛЛАСТ", use_container_width=True):
                st.info("Балласт: Выберите танки для коррекции крена")
                
        with col4:
            if st.button("🚨 ESD-1", use_container_width=True):
                systems['esd'].activate_esd(1, "Ручная активация", "Оператор")
                st.rerun()
                
        with col5:
            if st.button("📊 СОСТОЯНИЕ СИСТЕМ", use_container_width=True):
                st.json({
                    "cargo_flow": systems['cargo'].export_flow_m3h,
                    "ballast_heel": systems['system_state'].heel,
                    "esd_status": systems['esd'].esd_level_1,
                    "tank_levels": {name: tank.volume_percentage for name, tank in systems['cargo'].tanks.items()}
                })
    
    def _render_cargo_lite(self):
        """Упрощенная панель грузовых операций"""
        systems = st.session_state.systems
        
        st.header("🛢️ ГРУЗОВЫЕ ОПЕРАЦИИ")
        
        # Основные метрики
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Экспорт", f"{systems['cargo'].export_flow_m3h:.1f} m³/h")
        with col2:
            st.metric("Всего груза", f"{systems['cargo'].total_cargo_onboard:,.0f} m³")
        with col3:
            active_pumps = sum(1 for pump in systems['cargo'].pumps.values() if pump.is_running)
            st.metric("Активные насосы", active_pumps)
        
        # УПРАВЛЕНИЕ КЛАПАНАМИ - ТОЛЬКО ОСНОВНЫЕ
        st.subheader("🎛️ ОСНОВНЫЕ КЛАПАНЫ")
        
        # Грузовые танки
        st.write("**Грузовые танки:**")
        cols = st.columns(6)
        tank_names = ["TANK_1", "TANK_2", "TANK_3", "TANK_4", "TANK_5", "TANK_6"]
        
        for i, tank_name in enumerate(tank_names):
            with cols[i]:
                valve_state = systems['cargo'].valves.get(f"V-{tank_name}", False)
                new_state = st.checkbox(tank_name, value=valve_state, key=f"valve_{tank_name}")
                if new_state != valve_state:
                    systems['cargo'].valves[f"V-{tank_name}"] = new_state
                    st.rerun()
                
                # Простой индикатор уровня
                tank = systems['cargo'].tanks[tank_name]
                level_color = "red" if tank.volume_percentage > 95 else "orange" if tank.volume_percentage > 85 else "green"
                st.markdown(f"<span style='color:{level_color}'>{tank.volume_percentage:.1f}%</span>", 
                           unsafe_allow_html=True)
        
        # СИСТЕМНЫЕ КЛАПАНЫ
        st.write("**Системные клапаны:**")
        sys_cols = st.columns(4)
        system_valves = ["V-EXPORT", "V-CROSSOVER", "V-SLOP1", "V-SLOP2"]
        
        for i, valve_name in enumerate(system_valves):
            with sys_cols[i]:
                valve_state = systems['cargo'].valves.get(valve_name, False)
                new_state = st.checkbox(valve_name, value=valve_state, key=f"sys_{valve_name}")
                if new_state != valve_state:
                    systems['cargo'].valves[valve_name] = new_state
                    st.rerun()
        
        # УПРАВЛЕНИЕ НАСОСАМИ
        st.subheader("⚙️ НАСОСЫ")
        pump_cols = st.columns(3)
        
        for i, (pump_name, pump) in enumerate(systems['cargo'].pumps.items()):
            with pump_cols[i]:
                if st.button(f"{'⏹️' if pump.is_running else '▶️'} {pump_name}", 
                           use_container_width=True):
                    if pump.is_running:
                        pump.stop()
                    else:
                        pump.start()
                    st.rerun()
                
                st.caption(f"Расход: {pump.current_flow_m3h:.0f} m³/h")
    
    def _render_ballast_lite(self):
        """Упрощенная панель балласта"""
        systems = st.session_state.systems
        
        st.header("🌊 БАЛЛАСТ И ОСАДКА")
        
        # ПАРАМЕТРЫ
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Крен", f"{systems['system_state'].heel:.1f}°")
        with col2:
            st.metric("Дифферент", f"{systems['system_state'].trim:.1f}°")
        with col3:
            st.metric("Осадка", f"{systems['system_state'].draft_mean:.2f} м")
        
        # ПРОСТОЕ УПРАВЛЕНИЕ БАЛЛАСТОМ
        st.subheader("💧 БЫСТРАЯ КОРРЕКЦИЯ")
        
        # Автокоррекция
        auto_correct = st.checkbox("🤖 АВТОКОРРЕКЦИЯ КРЕНА", 
                                 value=systems['ballast'].auto_heel_correction)
        if auto_correct != systems['ballast'].auto_heel_correction:
            systems['ballast'].auto_heel_correction = auto_correct
            st.rerun()
        
        # Ручная коррекция
        st.write("**Коррекция крена:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⬅️ УВЕЛИЧИТЬ БАЛЛАСТ ЛЕВЫЙ БОРТ", use_container_width=True):
                # Упрощенная логика коррекции
                systems['ballast'].tanks["BALLAST_1P"].current_volume_m3 += 500
                systems['ballast'].tanks["BALLAST_2P"].current_volume_m3 += 500
                st.rerun()
                
        with col2:
            if st.button("➡️ УВЕЛИЧИТЬ БАЛЛАСТ ПРАВЫЙ БОРТ", use_container_width=True):
                systems['ballast'].tanks["BALLAST_1S"].current_volume_m3 += 500
                systems['ballast'].tanks["BALLAST_2S"].current_volume_m3 += 500
                st.rerun()
        
        # СТАТУС БАЛЛАСТНЫХ ТАНКОВ
        st.subheader("📊 БАЛЛАСТНЫЕ ТАНКИ")
        
        ballast_tanks = ["BALLAST_1P", "BALLAST_1S", "BALLAST_2P", "BALLAST_2S"]
        cols = st.columns(4)
        
        for i, tank_name in enumerate(ballast_tanks):
            with cols[i]:
                tank = systems['ballast'].tanks[tank_name]
                st.write(f"**{tank_name}**")
                st.progress(tank.volume_percentage / 100)
                st.write(f"{tank.current_volume_m3:.0f} m³")
    
    def _render_safety_lite(self):
        """Упрощенная панель безопасности"""
        systems = st.session_state.systems
        
        st.header("🚨 СИСТЕМЫ БЕЗОПАСНОСТИ")
        
        # ESD СИСТЕМА
        st.subheader("🛑 АВАРИЙНЫЙ ОСТАНОВ")
        
        esd = systems['esd']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🟡 ESD-1", use_container_width=True, disabled=esd.esd_level_1):
                esd.activate_esd(1, "Ручная активация", "Оператор")
                st.rerun()
            st.caption("Остановка грузовых операций")
            
        with col2:
            if st.button("🟠 ESD-2", use_container_width=True, disabled=esd.esd_level_2):
                esd.activate_esd(2, "Ручная активация", "Оператор")
                st.rerun()
            st.caption("Остановка платформы")
            
        with col3:
            if st.button("🔴 ESD-3", use_container_width=True, disabled=esd.esd_level_3):
                esd.activate_esd(3, "Ручная активация", "Оператор")
                st.rerun()
            st.caption("Полный аварийный останов")
        
        # СБРОС ESD
        if any([esd.esd_level_1, esd.esd_level_2, esd.esd_level_3]):
            if st.button("🔄 СБРОС ESD", use_container_width=True):
                esd.reset_esd()
                st.success("ESD сброшена!")
                st.rerun()
        
        # ПРЕДУПРЕЖДЕНИЯ
        st.subheader("⚠️ АКТИВНЫЕ ПРЕДУПРЕЖДЕНИЯ")
        
        warnings = []
        
        # Проверка переполнения
        for tank_name, tank in systems['cargo'].tanks.items():
            if tank.volume_percentage > 95:
                warnings.append(f"🔴 ПЕРЕПОЛНЕНИЕ {tank_name}: {tank.volume_percentage:.1f}%")
            elif tank.volume_percentage > 85:
                warnings.append(f"🟡 ВЫСОКИЙ УРОВЕНЬ {tank_name}: {tank.volume_percentage:.1f}%")
        
        # Проверка крена
        if abs(systems['system_state'].heel) > 8:
            warnings.append(f"🔴 ОПАСНЫЙ КРЕН: {systems['system_state'].heel:.1f}°")
        elif abs(systems['system_state'].heel) > 5:
            warnings.append(f"🟡 БОЛЬШОЙ КРЕН: {systems['system_state'].heel:.1f}°")
        
        # Отображение предупреждений
        if warnings:
            for warning in warnings:
                if "🔴" in warning:
                    st.error(warning)
                else:
                    st.warning(warning)
        else:
            st.success("✅ КРИТИЧЕСКИХ ПРЕДУПРЕЖДЕНИЙ НЕТ")

if __name__ == "__main__":
    simulator = FPSOSpiritLite()
    simulator.run_optimized()
