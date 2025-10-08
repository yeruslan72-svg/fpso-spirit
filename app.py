# app.py - AVCS DNA v6.0 Complete System
import streamlit as st
import asyncio
import json
import aiohttp
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from core.ai_engine import AVCSDNAEngine
from core.stabilizer import MRDamperController

# Инициализация системы
@st.cache_resource
def get_avcs_system():
    return AVCSDNAEngine(), MRDamperController()

async def websocket_listener(ai_engine, damper_controller):
    """Прослушивание WebSocket и обработка данных"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect('ws://localhost:8081/ws/data') as ws:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        sensor_data = json.loads(msg.data)
                        
                        # Обработка AI
                        analysis_result = await ai_engine.process_realtime_data(sensor_data)
                        
                        if analysis_result:
                            # Управление демпферами
                            await damper_controller.apply_force_profile(
                                analysis_result['damper_force'], 
                                sensor_data
                            )
                            
                            # Обновление интерфейса
                            update_dashboard(analysis_result, damper_controller)
                            
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break
                        
    except Exception as e:
        st.error(f"Ошибка подключения: {e}")

def update_dashboard(analysis, damper_controller):
    """Обновление Streamlit дашборда"""
    
    # Основные метрики
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_color = "🟢" if analysis['risk_index'] < 50 else "🟡" if analysis['risk_index'] < 80 else "🔴"
        st.metric("🎯 Индекс риска", f"{analysis['risk_index']}/100", delta=risk_color)
    
    with col2:
        rul_color = "🟢" if analysis['rul_hours'] > 168 else "🟡" if analysis['rul_hours'] > 72 else "🔴"
        st.metric("⏳ RUL", f"{analysis['rul_hours']} ч", delta=rul_color)
    
    with col3:
        st.metric("🔧 Сила демпферов", f"{analysis['damper_force']} N")
    
    with col4:
        status_color = {"STANDBY": "🟢", "NORMAL": "🟡", "WARNING": "🟠", "CRITICAL": "🔴"}
        st.metric("📊 Статус", analysis['system_status'], delta=status_color.get(analysis['system_status'], "⚪"))
    
    # Визуализация демпферов
    st.subheader("🔧 Управление MR-Демпферами")
    damper_status = damper_controller.get_damper_status()
    
    damper_cols = st.columns(4)
    for i, (damper_id, status) in enumerate(damper_status.items()):
        with damper_cols[i]:
            force = status['force']
            if force >= 4000:
                st.error(f"🔴 {status['position']}\n{force} N")
            elif force >= 1000:
                st.warning(f"🟡 {status['position']}\n{force} N") 
            else:
                st.success(f"🟢 {status['position']}\n{force} N")
    
    # График риска
    st.subheader("📈 Динамика индекса риска")
    if hasattr(ai_engine, 'risk_history') and ai_engine.risk_history:
        risk_df = pd.DataFrame({
            'Индекс риска': ai_engine.risk_history,
            'Критический порог': [80] * len(ai_engine.risk_history),
            'Предупреждение': [50] * len(ai_engine.risk_history)
        })
        st.line_chart(risk_df)

# Основной интерфейс Streamlit
def main():
    st.set_page_config(page_title="AVCS DNA v6.0 PRO", layout="wide")
    st.title("🏭 AVCS DNA v6.0 PRO - AI система стабилизации")
    
    ai_engine, damper_controller = get_avcs_system()
    
    # Запуск системы
    if st.button("🚀 Запуск системы AVCS DNA"):
        with st.spinner("Запуск AI системы..."):
            asyncio.run(websocket_listener(ai_engine, damper_controller))
    
    # Статус системы
    st.sidebar.header("🔧 Статус системы")
    st.sidebar.info("AVCS DNA AI Core активен")
    st.sidebar.info("Демпферы LORD RD-8040 подключены")
    st.sidebar.info("WebSocket данные поступают")

if __name__ == "__main__":
    main()
    
