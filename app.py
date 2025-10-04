# app.py - PREMIUM VERSION WITH WOW EFFECTS
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import time
from datetime import datetime
import numpy as np

class FPSOPremium:
    def __init__(self):
        self.project_name = "FPSO SPIRIT"
        self.version = "3.0"
        
        if 'systems' not in st.session_state:
            self._initialize_premium_systems()
    
    def _initialize_premium_systems(self):
        """Initialize advanced FPSO systems with realistic data"""
        st.session_state.systems = {
            'cargo_tanks': {
                'TANK_1': {'volume': 12000, 'capacity': 15000, 'valve_open': False, 'level': 80.0, 'temperature': 45.0, 'pressure': 0.02},
                'TANK_2': {'volume': 13500, 'capacity': 15000, 'valve_open': False, 'level': 90.0, 'temperature': 42.0, 'pressure': 0.03},
                'TANK_3': {'volume': 9000, 'capacity': 15000, 'valve_open': False, 'level': 60.0, 'temperature': 47.0, 'pressure': 0.01},
                'TANK_4': {'volume': 14250, 'capacity': 15000, 'valve_open': False, 'level': 95.0, 'temperature': 43.0, 'pressure': 0.04},
                'TANK_5': {'volume': 7500, 'capacity': 15000, 'valve_open': False, 'level': 50.0, 'temperature': 46.0, 'pressure': 0.02},
                'TANK_6': {'volume': 11250, 'capacity': 15000, 'valve_open': False, 'level': 75.0, 'temperature': 44.0, 'pressure': 0.03},
            },
            'cargo_pumps': {
                'CARGO_PUMP_1': {'running': False, 'flow': 0, 'status': 'STOPPED', 'vibration': 2.1, 'temperature': 65.0},
                'CARGO_PUMP_2': {'running': False, 'flow': 0, 'status': 'STOPPED', 'vibration': 1.8, 'temperature': 62.0},
                'STRIPPING_PUMP': {'running': False, 'flow': 0, 'status': 'STOPPED', 'vibration': 1.2, 'temperature': 55.0},
            },
            'ballast_tanks': {
                'BALLAST_1P': {'volume': 2000, 'capacity': 5000, 'valve_open': False, 'level': 40.0},
                'BALLAST_1S': {'volume': 3000, 'capacity': 5000, 'valve_open': False, 'level': 60.0},
                'BALLAST_2P': {'volume': 1500, 'capacity': 5000, 'valve_open': False, 'level': 30.0},
                'BALLAST_2S': {'volume': 3500, 'capacity': 5000, 'valve_open': False, 'level': 70.0},
                'BALLAST_F': {'volume': 1200, 'capacity': 3000, 'valve_open': False, 'level': 40.0},
                'BALLAST_A': {'volume': 1800, 'capacity': 3000, 'valve_open': False, 'level': 60.0},
            },
            'vessel_status': {
                'heel': 2.5, 'trim': 0.8, 'draft_fore': 18.2, 'draft_aft': 19.0, 
                'draft_mean': 18.6, 'displacement': 245000, 'gm': 2.1
            },
            'safety_systems': {
                'esd_level': 0, 'igs_pressure': 0.8, 'igs_o2': 2.5, 
                'fire_alarms': [], 'gas_alarms': [], 'overflow_alarms': []
            },
            'operations': {
                'export_flow': 0, 'total_cargo': 67500, 'operational_mode': 'NORMAL',
                'weather': {'wind_speed': 8.5, 'wind_dir': 45, 'wave_height': 2.5}
            }
        }
        st.session_state.last_update = datetime.now()
    
    def run(self):
        # Premium page configuration
        st.set_page_config(
            page_title="FPSO SPIRIT - Professional CCR",
            page_icon="⚓",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Custom CSS for premium look
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
        }
        .status-normal { color: #28a745; font-weight: bold; }
        .status-warning { color: #ffc107; font-weight: bold; }
        .status-critical { color: #dc3545; font-weight: bold; }
        </style>
        """, unsafe_allow_html=True)
        
        # Premium Header
        st.markdown(f"""
        <div class="main-header">
            <h1>⚓ FPSO SPIRIT - Central Control Room</h1>
            <p>Professional Offshore Operations Simulator • Version {self.version}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main Navigation with Icons
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏠 DASHBOARD", 
            "📊 CARGO SYSTEM", 
            "🌊 BALLAST & STABILITY",
            "⚡ POWER & UTILITIES", 
            "🚨 SAFETY SYSTEMS",
            "📈 ANALYTICS"
        ])
        
        with tab1:
            self._premium_dashboard()
        with tab2:
            self._cargo_operations_premium()
        with tab3:
            self._ballast_stability_premium()
        with tab4:
            self._power_utilities_premium()
        with tab5:
            self._safety_systems_premium()
        with tab6:
            self._analytics_dashboard()
    
    def _premium_dashboard(self):
        """Premium Main Dashboard with Visualizations"""
        systems = st.session_state.systems
        
        st.header("🎛️ CENTRAL CONTROL PANEL")
        
        # Real-time Status Overview
        st.subheader("📊 REAL-TIME SYSTEM OVERVIEW")
        
        # Top Metrics Row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            self._create_metric_card("ESD STATUS", 
                                   f"Level {systems['safety_systems']['esd_level']}",
                                   "normal" if systems['safety_systems']['esd_level'] == 0 else "critical")
        with col2:
            self._create_metric_card("TOTAL CARGO", 
                                   f"{systems['operations']['total_cargo']:,.0f} m³",
                                   "normal")
        with col3:
            self._create_metric_card("VESSEL HEEL", 
                                   f"{systems['vessel_status']['heel']:.1f}°",
                                   "warning" if abs(systems['vessel_status']['heel']) > 5 else "normal")
        with col4:
            self._create_metric_card("IGS PRESSURE", 
                                   f"{systems['safety_systems']['igs_pressure']:.1f} bar",
                                   "warning" if systems['safety_systems']['igs_pressure'] < 0.5 else "normal")
        with col5:
            self._create_metric_card("OPERATIONAL MODE", 
                                   systems['operations']['operational_mode'],
                                   "normal")
        
        # Visual System Status
        st.subheader("📈 SYSTEM STATUS VISUALIZATION")
        
        # Create a Plotly visualization for tank levels
        fig = self._create_tank_levels_chart()
        st.plotly_chart(fig, use_container_width=True)
        
        # Quick Operations Panel
        st.subheader("🚀 QUICK OPERATIONS")
        
        op_cols = st.columns(6)
        
        operations = [
            ("📤", "START UNLOADING", "primary"),
            ("📥", "START LOADING", "primary"), 
            ("🌊", "BALLAST OPS", "secondary"),
            ("🔥", "START BOILER", "secondary"),
            ("💨", "START IGS", "secondary"),
            ("🔄", "UPDATE DATA", "secondary")
        ]
        
        for i, (icon, text, color) in enumerate(operations):
            with op_cols[i]:
                if st.button(f"{icon} {text}", use_container_width=True, type=color):
                    st.toast(f"{text} sequence initiated!", icon=icon)
        
        # Emergency Panel
        st.subheader("🚨 EMERGENCY CONTROLS")
        
        emergency_cols = st.columns(4)
        
        with emergency_cols[0]:
            if st.button("🟡 ESD LEVEL 1", use_container_width=True, type="secondary"):
                self._activate_esd(1)
        with emergency_cols[1]:
            if st.button("🟠 ESD LEVEL 2", use_container_width=True, type="secondary"):
                self._activate_esd(2)
        with emergency_cols[2]:
            if st.button("🔴 ESD LEVEL 3", use_container_width=True, type="secondary"):
                self._activate_esd(3)
        with emergency_cols[3]:
            if st.button("🧯 FIRE DRILL", use_container_width=True, type="secondary"):
                self._simulate_fire_drill()
    
    def _cargo_operations_premium(self):
        """Premium Cargo Operations with Visual Diagrams"""
        systems = st.session_state.systems
        
        st.header("🛢️ CARGO HANDLING SYSTEM")
        
        # Cargo System Schematic
        st.subheader("📊 CARGO SYSTEM SCHEMATIC DIAGRAM")
        
        # Create interactive cargo system diagram
        fig = self._create_cargo_system_diagram()
        st.plotly_chart(fig, use_container_width=True)
        
        # Tank Control Panel
        st.subheader("🎛️ TANK CONTROL PANEL")
        
        # Create tank control cards in two rows
        tank_rows = st.columns(2)
        
        with tank_rows[0]:
            for tank_name in ['TANK_1', 'TANK_2', 'TANK_3']:
                self._create_tank_control_card(tank_name, systems['cargo_tanks'][tank_name])
        
        with tank_rows[1]:
            for tank_name in ['TANK_4', 'TANK_5', 'TANK_6']:
                self._create_tank_control_card(tank_name, systems['cargo_tanks'][tank_name])
        
        # Pump Control Panel
        st.subheader("⚙️ PUMP CONTROL CENTER")
        
        pump_cols = st.columns(3)
        
        for i, (pump_name, pump_data) in enumerate(systems['cargo_pumps'].items()):
            with pump_cols[i]:
                self._create_pump_control_card(pump_name, pump_data)
    
    def _ballast_stability_premium(self):
        """Premium Ballast and Stability Control"""
        systems = st.session_state.systems
        
        st.header("🌊 BALLAST & STABILITY MANAGEMENT")
        
        # Stability Visualization
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("⚖️ STABILITY INDICATORS")
            fig = self._create_stability_chart()
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📐 VESSEL PARAMETERS")
            
            params = [
                ("Heel", f"{systems['vessel_status']['heel']:.1f}°"),
                ("Trim", f"{systems['vessel_status']['trim']:.1f}°"),
                ("Draft Fore", f"{systems['vessel_status']['draft_fore']:.1f} m"),
                ("Draft Aft", f"{systems['vessel_status']['draft_aft']:.1f} m"),
                ("GM", f"{systems['vessel_status']['gm']:.1f} m"),
                ("Displacement", f"{systems['vessel_status']['displacement']:,.0f} t")
            ]
            
            for param, value in params:
                st.metric(param, value)
        
        # Ballast Tank Control
        st.subheader("💧 BALLAST TANK CONTROL")
        
        ballast_cols = st.columns(3)
        
        ballast_groups = [
            ['BALLAST_1P', 'BALLAST_1S'],
            ['BALLAST_2P', 'BALLAST_2S'], 
            ['BALLAST_F', 'BALLAST_A']
        ]
        
        for i, tank_group in enumerate(ballast_groups):
            with ballast_cols[i]:
                for tank_name in tank_group:
                    tank_data = systems['ballast_tanks'][tank_name]
                    self._create_ballast_tank_card(tank_name, tank_data)
    
    def _power_utilities_premium(self):
        """Premium Power and Utilities Panel"""
        systems = st.session_state.systems
        
        st.header("⚡ POWER & UTILITIES SYSTEMS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💨 INERT GAS SYSTEM")
            
            # IGS Control Panel
            igs_cols = st.columns(2)
            
            with igs_cols[0]:
                st.metric("IGS Pressure", f"{systems['safety_systems']['igs_pressure']:.1f} bar")
                new_pressure = st.slider("Pressure Setpoint", 0.0, 2.0, systems['safety_systems']['igs_pressure'], 0.1)
                if new_pressure != systems['safety_systems']['igs_pressure']:
                    systems['safety_systems']['igs_pressure'] = new_pressure
            
            with igs_cols[1]:
                st.metric("O2 Content", f"{systems['safety_systems']['igs_o2']:.1f}%")
                st.metric("Blower Status", "🟢 RUNNING")
                st.metric("Scrubber Temp", "45°C")
        
        with col2:
            st.subheader("🔥 BOILER SYSTEM")
            
            boiler_params = [
                ("Steam Pressure", "8.2 bar", "normal"),
                ("Water Level", "85%", "normal"), 
                ("Steam Temperature", "285°C", "normal"),
                ("Fuel Pressure", "4.5 bar", "normal")
            ]
            
            for param, value, status in boiler_params:
                self._create_metric_card(param, value, status)
            
            if st.button("🔥 START BOILER", use_container_width=True):
                st.toast("Boiler start sequence initiated!", icon="🔥")
    
    def _safety_systems_premium(self):
        """Premium Safety Systems Panel"""
        systems = st.session_state.systems
        
        st.header("🚨 SAFETY & EMERGENCY SYSTEMS")
        
        # ESD Control Center
        st.subheader("🛑 EMERGENCY SHUTDOWN SYSTEM")
        
        esd_cols = st.columns(4)
        
        esd_buttons = [
            ("🟡 ESD LEVEL 1", "Stop Cargo Operations", "secondary"),
            ("🟠 ESD LEVEL 2", "Stop All Operations", "secondary"),
            ("🔴 ESD LEVEL 3", "Emergency Shutdown", "secondary"), 
            ("🔄 RESET ESD", "Reset All Systems", "primary")
        ]
        
        for i, (label, tooltip, color) in enumerate(esd_buttons):
            with esd_cols[i]:
                if st.button(label, use_container_width=True, type=color, help=tooltip):
                    if "RESET" in label:
                        systems['safety_systems']['esd_level'] = 0
                        st.success("ESD System Reset!")
                    else:
                        level = 1 if "LEVEL 1" in label else 2 if "LEVEL 2" in label else 3
                        self._activate_esd(level)
        
        # Safety Monitoring
        st.subheader("⚠️ SAFETY MONITORING")
        
        # Create safety status cards
        safety_cols = st.columns(4)
        
        safety_status = [
            ("Fire System", "🟢 ARMED", "normal"),
            ("Gas Detection", "🟢 NORMAL", "normal"),
            ("Tank Levels", "🟡 1 HIGH", "warning"),
            ("IGS System", "🟢 NORMAL", "normal")
        ]
        
        for i, (system, status, level) in enumerate(safety_status):
            with safety_cols[i]:
                self._create_metric_card(system, status, level)
    
    def _analytics_dashboard(self):
        """Premium Analytics Dashboard"""
        st.header("📈 OPERATIONAL ANALYTICS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 CARGO FLOW ANALYTICS")
            
            # Simulate flow data
            time_points = list(range(24))
            flow_data = [max(0, 800 + np.random.normal(0, 100)) for _ in time_points]
            
            fig = px.line(x=time_points, y=flow_data, 
                         labels={'x': 'Time (hours)', 'y': 'Flow Rate (m³/h)'},
                         title="24-Hour Cargo Flow Analysis")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🌡️ EQUIPMENT HEALTH")
            
            equipment_health = {
                'CARGO_PUMP_1': 95,
                'CARGO_PUMP_2': 88,
                'BALLAST_PUMP_1': 92,
                'BALLAST_PUMP_2': 85,
                'IGS_BLOWER': 96,
                'BOILER': 90
            }
            
            for equipment, health in equipment_health.items():
                st.write(f"**{equipment}**")
                st.progress(health/100)
                st.caption(f"Health: {health}%")
    
    # Visualization Methods
    def _create_tank_levels_chart(self):
        """Create beautiful tank levels visualization"""
        systems = st.session_state.systems
        
        tank_names = list(systems['cargo_tanks'].keys())
        levels = [tank['level'] for tank in systems['cargo_tanks'].values()]
        
        colors = ['#28a745' if level < 85 else '#ffc107' if level < 95 else '#dc3545' 
                 for level in levels]
        
        fig = go.Figure(data=[go.Bar(
            x=tank_names,
            y=levels,
            marker_color=colors,
            text=levels,
            texttemplate='%{text:.1f}%',
            textposition='auto',
        )])
        
        fig.update_layout(
            title="CARGO TANK LEVELS MONITORING",
            yaxis_title="Level (%)",
            yaxis_range=[0, 100],
            showlegend=False
        )
        
        return fig
    
    def _create_cargo_system_diagram(self):
        """Create interactive cargo system diagram"""
        # Simplified cargo system visualization
        fig = go.Figure()
        
        # Add tanks as circles
        tank_positions = {
            'TANK_1': (1, 4), 'TANK_2': (2, 4), 'TANK_3': (3, 4),
            'TANK_4': (1, 2), 'TANK_5': (2, 2), 'TANK_6': (3, 2),
        }
        
        for tank_name, (x, y) in tank_positions.items():
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                marker=dict(size=50, color='lightblue'),
                text=tank_name,
                textposition="middle center",
                name=tank_name
            ))
        
        fig.update_layout(
            title="CARGO SYSTEM SCHEMATIC",
            xaxis=dict(visible=False, range=[0, 4]),
            yaxis=dict(visible=False, range=[0, 5]),
            showlegend=False,
            height=400
        )
        
        return fig
    
    def _create_stability_chart(self):
        """Create vessel stability visualization"""
        systems = st.session_state.systems
        
        heel = systems['vessel_status']['heel']
        
        fig = go.Figure()
        
        # Create a simple vessel representation
        fig.add_trace(go.Scatter(
            x=[-10, 10, 10, -10, -10],
            y=[0, 0, 5, 5, 0],
            fill="toself",
            fillcolor="lightgray",
            line=dict(color="darkgray"),
            name="Vessel"
        ))
        
        # Water line with heel effect
        water_x = [-10, 10]
        water_y = [2 + heel * 0.2, 2 - heel * 0.2]
        
        fig.add_trace(go.Scatter(
            x=water_x, y=water_y,
            line=dict(color="blue", width=3),
            name="Water Line"
        ))
        
        fig.update_layout(
            title=f"VESSEL STABILITY - Heel: {heel}°",
            xaxis=dict(visible=False, range=[-15, 15]),
            yaxis=dict(visible=False, range=[-1, 6]),
            showlegend=False,
            height=300
        )
        
        return fig
    
    # Component Creation Methods
    def _create_metric_card(self, title, value, status):
        """Create a beautiful metric card"""
        color_map = {
            "normal": "#28a745",
            "warning": "#ffc107", 
            "critical": "#dc3545"
        }
        
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: {color_map[status]};">
            <h4 style="margin: 0; color: #666; font-size: 0.9rem;">{title}</h4>
            <h2 style="margin: 0; color: {color_map[status]};">{value}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    def _create_tank_control_card(self, tank_name, tank_data):
        """Create interactive tank control card"""
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{tank_name}**")
                
                # Level indicator with color coding
                level = tank_data['level']
                color = "🟢" if level < 85 else "🟡" if level < 95 else "🔴"
                
                st.progress(level/100)
                st.write(f"{color} {level:.1f}%")
                
                # Additional parameters
                st.caption(f"Temp: {tank_data['temperature']}°C")
                st.caption(f"Pressure: {tank_data['pressure']:.3f} bar")
            
            with col2:
                # Valve control
                valve_status = "🔓 OPEN" if tank_data['valve_open'] else "🔒 CLOSED"
                if st.button(valve_status, key=f"valve_{tank_name}"):
                    st.session_state.systems['cargo_tanks'][tank_name]['valve_open'] = not tank_data['valve_open']
                    st.rerun()
                
                # Level adjustment
                new_level = st.slider("Level", 0, 100, int(level), 
                                    key=f"level_{tank_name}")
                if new_level != level:
                    st.session_state.systems['cargo_tanks'][tank_name]['level'] = new_level
                    st.rerun()
    
    def _create_pump_control_card(self, pump_name, pump_data):
        """Create interactive pump control card"""
        with st.container():
            st.write(f"**{pump_name}**")
            
            # Status with color
            status_color = "🟢" if pump_data['running'] else "🔴"
            st.write(f"{status_color} {pump_data['status']}")
            
            # Parameters
            st.metric("Flow Rate", f"{pump_data['flow']} m³/h")
            st.metric("Vibration", f"{pump_data['vibration']} mm/s")
            st.metric("Temperature", f"{pump_data['temperature']}°C")
            
            # Control button
            button_text = "⏹️ STOP" if pump_data['running'] else "▶️ START"
            if st.button(button_text, key=f"pump_{pump_name}", use_container_width=True):
                st.session_state.systems['cargo_pumps'][pump_name]['running'] = not pump_data['running']
                st.session_state.systems['cargo_pumps'][pump_name]['flow'] = 800 if not pump_data['running'] else 0
                st.session_state.systems['cargo_pumps'][pump_name]['status'] = 'RUNNING' if not pump_data['running'] else 'STOPPED'
                st.rerun()
    
    def _create_ballast_tank_card(self, tank_name, tank_data):
        """Create ballast tank control card"""
        with st.container():
            level = (tank_data['volume'] / tank_data['capacity']) * 100
            
            st.write(f"**{tank_name}**")
            st.progress(level/100)
            st.write(f"{tank_data['volume']} / {tank_data['capacity']} m³")
            st.write(f"({level:.1f}%)")
            
            # Control buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"💧", key=f"ballast_in_{tank_name}"):
                    st.session_state.systems['ballast_tanks'][tank_name]['volume'] = min(
                        tank_data['capacity'], tank_data['volume'] + 500
                    )
                    st.rerun()
            with col2:
                if st.button(f"🚰", key=f"ballast_out_{tank_name}"):
                    st.session_state.systems['ballast_tanks'][tank_name]['volume'] = max(
                        0, tank_data['volume'] - 500
                    )
                    st.rerun()
    
    # Operation Methods
    def _activate_esd(self, level):
        """Activate ESD with visual feedback"""
        systems = st.session_state.systems
        systems['safety_systems']['esd_level'] = level
        
        # Stop operations based on ESD level
        if level >= 1:
            for pump in systems['cargo_pumps'].values():
                pump['running'] = False
                pump['flow'] = 0
                pump['status'] = 'STOPPED'
        
        st.toast(f"ESD LEVEL {level} ACTIVATED!", icon="🚨")
    
    def _simulate_fire_drill(self):
        """Simulate fire drill with visual feedback"""
        systems = st.session_state.systems
        systems['safety_systems']['fire_alarms'].append("FIRE DRILL - PUMP ROOM")
        st.toast("FIRE DRILL INITIATED - This is a test", icon="🧯")

if __name__ == "__main__":
    simulator = FPSOPremium()
    simulator.run()
