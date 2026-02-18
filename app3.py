import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import json
import os
import numpy as np

# --- КОНФИГУРАЦИЯ ЦВЕТОВ ---
DARK_BLUE = "#001F3F"
ACCENT_BLUE = "#0072FF"
LIGHT_BG = "#F1F5F9"
GRAY_TEXT = "#64748B"

# 1. Настройка страницы
st.set_page_config(
    page_title="Исследование Каспийского моря", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap');

    /* Глобальные настройки шрифта и базового размера */
    html, body, [class*="st-"], div, p, span {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.05rem; /* Увеличили базовый текст */
    }

    .stApp { background-color: #F8FAFC; }
    
    /* Заголовок страницы */
    .main-title {
        color: #001f3f; text-align: center; font-size: 3rem !important;
        margin-bottom: 25px; font-weight: 900; text-transform: uppercase;
    }

    /* Официальный текст (курсив в рамке) */
    .official-text {
        font-size: 1.2rem !important; 
        color: #475569;
        line-height: 1.6; 
        border-left: 5px solid #0072FF;
        padding-left: 20px; 
        margin-bottom: 25px; 
        font-style: italic;
    }

    /* Текст в блоке Сеть (3 станции и т.д.) */
    .network-text { 
        font-size: 1.3rem !important; 
        line-height: 1.8; 
        color: #1E293B; 
    }
    .network-text b { color: #0072FF; font-size: 1.1em; }

    /* Заголовки секций в белых рамках */
    .section-header-text {
        color: #003366; font-weight: 800; font-size: 1.5rem !important; margin: 0;
    }

    /* Текст "Критическое снижение" и цифра под ним */
    .status-badge {
        display: inline-block; padding: 8px 16px; border-radius: 20px;
        font-weight: 800; font-size: 1rem !important; background: #FFEBEE;
        color: #D32F2F; border: 1px solid #FFCDD2;
    }
    
    .dynamic-level-text {
        font-size: 2rem !important; color: #D32F2F; font-weight: 900; margin: 15px 0;
    }

    /* Подзаголовки и описания под графиками */
    .promo-bold {
        font-size: 1.4rem !important; font-weight: 700; color: #1E293B; margin-bottom: 12px;
    }
    .promo-sub {
        font-size: 1.15rem !important; color: #475569; line-height: 1.5; margin-bottom: 25px;
    }

    /* Контейнер для плашек прогноза (горизонтальный) */
    .forecast-row {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        gap: 20px !important;
        width: 100% !important;
        margin: 25px 0 !important;
    }


    .forecast-card {
        flex: 1 !important;
        border-radius: 20px !important;
        padding: 35px 20px !important;
        text-align: center !important;
        color: white !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
    }

    .fc-year { font-size: 1.1rem !important; opacity: 0.8; margin-bottom: 10px; text-transform: uppercase; font-weight: 600; }
    .fc-value { font-size: 2.6rem !important; font-weight: 900; margin-bottom: 8px; white-space: nowrap; }
    .fc-unit { font-size: 0.6em; margin-left: 5px; }
    .fc-desc { font-size: 1.1rem !important; opacity: 0.95; }
    
    /* Исправление кнопок */
    div.stButton > button p {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- СОЗДАНИЕ ВКЛАДОК (7+1 согласно списку) ---
tabs = st.tabs([
    "📊 Мониторинг", 
    "🌤️ Прогноз погоды", 
    "🌾 Агрометеорологические прогнозы", 
    "💧 Гидрологические прогнозы", 
    "🌊 Водные ресурсы", 
    "🌊 Каспийское море", 
    "🇰🇿 Климат", 
    "🏭 Экология городов"
])

# --- Твой основной контент по Каспию идет во вкладку №5 (индекс 5) ---
with tabs[5]:
    st.markdown('<h1 class="main-title">🌊 Исследование Каспийского моря</h1>', unsafe_allow_html=True)
    # ВСЕ СТРОКИ НИЖЕ ДОЛЖНЫ ИМЕТЬ ОТСТУП (4 ПРОБЕЛА)
    
    
    if 'selected_param' not in st.session_state:
        st.session_state.selected_param = "Уровень"

    months = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
    units = {"Уровень моря": "м БС", "Температура воздуха": "°C", "Температура воды": "°C","Соленость": "‰", "Лед": "см", "Ветер": "м/с", "Волнение": "м"}

    seasonal_data = {
        "Уровень моря": [-29.40, -29.38, -29.35, -29.20, -29.10, -29.15, -29.25, -29.35, -29.40, -29.42, -29.45, -29.48],
        "Температура воздуха": [2, 1, 4, 11, 18, 24, 27, 26, 20, 13, 7, 3],
        "Температура воды": [2, 1, 4, 11, 18, 24, 27, 26, 30, 13, 7, 3],
        "Соленость": [12.5, 12.6, 12.4, 11.8, 11.2, 11.5, 11.9, 12.2, 12.4, 12.5, 12.5, 12.6],
        "Лед": [25, 35, 15, 0, 0, 0, 0, 0, 0, 0, 5, 18],
        "Ветер": [6, 7, 8, 6, 5, 4, 4, 5, 6, 7, 8, 7],
        "Волнение": [1.2, 1.5, 1.8, 1.1, 0.7, 0.6, 0.5, 0.8, 1.2, 1.5, 1.9, 1.4]
    }

    # ПОЛНЫЕ ДАННЫЕ ДЛЯ ГРАФИКА
    raw_data = {
        "Год": list(range(1921, 2026)),
        "КчКМ": [-26.19,-26.31,-26.36,-26.38,-26.46,-26.38,-26.17,-25.99,-25.93,-26.05,-26.17,-26.12,-26.14,-26.32,-26.57,-26.77,-26.97,-27.28,-27.54,-27.73,-27.77,-27.68,-27.68,-27.73,-27.88,-27.80,-27.70,-27.68,-27.79,-27.91,-28.09,-28.06,-28.12,-28.23,-28.33,-28.40,-28.32,-28.18,-28.16,-28.21,-28.37,-28.48,-28.44,-28.35,-28.38,-28.24,-28.30,-28.42,-28.49,-28.37,-28.41,-28.45,-28.53,-28.54,-28.66,-28.89,-28.97,-28.88,-28.61,-28.43,-28.24,-28.15,-28.07,-28.10,-27.97,-27.90,-27.83,-27.75,-27.82,-27.68,-27.26,-27.14,-26.91,-26.70,-26.59,-26.81,-27.05,-27.07,-27.07,-27.18,-27.20,-27.20,-27.11,-27.00,-26.98,-27.06,-27.08,-27.17,-27.21,-27.31,-27.50,-27.56,-27.61,-27.70,-27.92,-27.97,-27.94,-28.10,-28.29,-28.30,-28.50,-28.72,-29.02,-29.20,-29.35],
        "КМ": [-26.28,-26.39,-26.44,-26.47,-26.56,-26.47,-26.27,-26.10,-25.93,-26.06,-26.19,-26.11,-26.12,-26.33,-26.54,-26.77,-26.99,-27.31,-27.61,-27.78,-27.85,-27.77,-27.75,-27.78,-27.96,-27.90,-27.78,-27.75,-27.83,-28.01,-28.16,-28.16,-28.26,-28.27,-28.36,-28.41,-28.33,-28.20,-28.17,-28.23,-28.41,-28.51,-28.44,-28.37,-28.43,-28.27,-28.34,-28.46,-28.47,-28.35,-28.42,-28.51,-28.56,-28.59,-28.69,-28.92,-29.00,-28.94,-28.60,-28.48,-28.32,-28.25,-28.08,-28.04,-27.95,-27.87,-27.76,-27.57,-27.57,-27.52,-27.15,-26.99,-26.95,-26.75,-26.61,-26.78,-26.98,-27.00,-27.02,-27.07,-27.17,-27.14,-27.09,-27.00,-26.91,-27.04,-27.06,-27.12,-27.15,-27.25,-27.50,-27.56,-27.61,-27.73,-27.98,-27.99,-27.98,-27.98,-28.20,-28.24,-28.42,-28.66,-28.86,-29.05,None]

    }
    history_df = pd.DataFrame(raw_data)


# 4. КОНТЕНТ

    t_col1, t_col2, t_col3 = st.columns([0.9, 1, 1.2])

    with t_col1:
        st.markdown('<div class="white-label-header"><p class="section-header-text">📡 Сеть</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="official-text">РГП «Казгидромет» осуществляет непрерывный гидрометеорологический и экологический мониторинг казахстанского сектора Каспийского моря.</div>', unsafe_allow_html=True)
        st.markdown("""<div class="network-text">🚢 <b>10</b> морских станций<br>🌦️ <b>28</b> метеостанций<br>💧 <b>4</b> гидропоста<br>🧪 <b>50</b> точек качества</div>""", unsafe_allow_html=True)

    with t_col2:
        st.markdown('<div class="white-label-header"><p class="section-header-text">🔎 Параметры</p></div>', unsafe_allow_html=True)
        
        # Приписка про 2025 год
        st.markdown('<div style="color: #64748B; font-size: 0.9rem; margin-bottom: 10px; font-weight: 600;">📅 Оперативные данные за 2025 г.</div>', unsafe_allow_html=True)
        
        p_c1, p_c2 = st.columns(2)
        
        # Добавили "Темп. воды" в список
        params = [
            ("🌊", "Уровень моря"), 
            ("🌡️", "Температура воздуха"), 
            ("💧", "Температура воды"), # Новый параметр
            ("🧪", "Соленость"), 
            ("❄️", "Лед"), 
            ("🌬️", "Ветер"), 
            ("〰️", "Волнение")
        ]
        
        for i, (emoji, name) in enumerate(params):
            with [p_c1, p_c2][i % 2]:
                if st.button(f"{emoji} {name}", key=f"top_{name}", use_container_width=True):
                    st.session_state.selected_param = name

    with t_col3:
        # Используем .get(), чтобы не вылетала ошибка, если ключ не найден
        current_unit = units.get(st.session_state.selected_param, "")
        
        st.markdown(f'<div class="white-label-header"><p class="section-header-text">📊 Сезонный ход ({current_unit})</p></div>', unsafe_allow_html=True)
        
        fig_s = go.Figure()
        
        # Берем данные из словаря по выбранному ключу
        display_data = seasonal_data.get(st.session_state.selected_param, [0]*12)
        
        fig_s.add_trace(go.Scatter(
            x=months, y=display_data,
            mode='lines+markers', 
            line=dict(color='#0072FF', width=3, shape='spline'),
            marker=dict(size=8, color='white', line=dict(color='#0072FF', width=2)),
            name=st.session_state.selected_param
        ))
        
        fig_s.update_layout(
            height=250, 
            margin=dict(l=10, r=10, t=30, b=10), 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified"
        )
        fig_s.update_xaxes(showgrid=False, tickfont=dict(size=12, color='#64748B'))
        fig_s.update_yaxes(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(size=12, color='#64748B'))
        
        st.plotly_chart(fig_s, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<hr style='margin: 30px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # --- НИЖНИЙ БЛОК ---
    b_col1, b_col2 = st.columns([1.8, 1])

    with b_col1:
        st.markdown('<div class="white-label-header"><p class="section-header-text">📉 Динамика уровня Каспийского моря</p></div>', unsafe_allow_html=True) 
        
        st.markdown('<div class="promo-bold">Уровень Каспийского моря подвержен значительным колебаниям</div>', unsafe_allow_html=True)
        st.markdown('<div class="promo-sub">В 2025 г. уровень моря в его казахстанской части достиг отметки минус 29,35 м БС. Это один из самых низких показателей за последние 100 лет в казахстанской части Каспийского моря.</div>', unsafe_allow_html=True)


        # ТЕПЕРЬ ГРАФИК ВНУТРИ КОЛОНКИ (ПРАВИЛЬНЫЙ ОТСТУП)
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Scatter(
            x=history_df["Год"], y=history_df["КчКМ"],
            name="Казахстанская часть (КчКМ)",
            line=dict(color='#0072FF', width=3),
            hovertemplate="Год: %{x}<br>Уровень: %{y} м БС<extra></extra>"
        ))
        fig_hist.add_trace(go.Scatter(
            x=history_df["Год"], y=history_df["КМ"],
            name="Общий уровень (КМ)",
            line=dict(color='#94A3B8', width=2, dash='dash'),
            hovertemplate="Год: %{x}<br>Уровень: %{y} м БС<extra></extra>"
        ))
        fig_hist.update_layout(
            height=400, margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified"
        )
        fig_hist.update_xaxes(showgrid=False, linecolor='#E2E8F0', range=[1920, 2026])
        fig_hist.update_yaxes(showgrid=True, gridcolor='#E2E8F0', linecolor='#E2E8F0', zeroline=False)
        st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})

    # --- БЛОК: НАУЧНЫЙ КОНТЕКСТ (ЦИКЛИЧНОСТЬ) ---
    with b_col1: # Размещаем под графиком динамики
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🔍 Почему уровень моря постоянно меняется? (Научный контекст)"):
            st.markdown("""
                <div style="padding: 10px; line-height: 1.6; color: #334155;">
                    Каспийское море — это замкнутый водоем, его уровень работает как <b> климатический индикатор</b>. 
                    Исторически выделяются три ключевые фазы в новейшей истории:
                </div>
            """, unsafe_allow_html=True)
            
            c_phase1, c_phase2, c_phase3 = st.columns(3)
            
            with c_phase1:
                st.markdown("""
                    <div style="border-left: 3px solid #64748B; padding-left: 15px;">
                        <span style="color: #64748B; font-weight: 800;">1930 — 1977</span><br>
                        <b>Резкое падение</b><br>
                        <span style="font-size: 0.9rem;">Обусловлено активным строительством ГЭС на Волге и длительным периодом засухи.</span>
                    </div>
                """, unsafe_allow_html=True)
                
            with c_phase2:
                st.markdown("""
                    <div style="border-left: 3px solid #0072FF; padding-left: 15px;">
                        <span style="color: #0072FF; font-weight: 800;">1978 — 1995</span><br>
                        <b>Аномальный подъем</b><br>
                        <span style="font-size: 0.9rem;">Внезапное увеличение стока рек и изменение атмосферной циркуляции. Уровень вырос на 2.5 метра.</span>
                    </div>
                """, unsafe_allow_html=True)
                
            with c_phase3:
                st.markdown("""
                    <div style="border-left: 3px solid #D32F2F; padding-left: 15px;">
                        <span style="color: #D32F2F; font-weight: 800;">2005 — н.в.</span><br>
                        <b>Текущий спад</b><br>
                        <span style="font-size: 0.9rem;">Снижение притока и рост испарения из-за глобального потепления. Фаза, требующая адаптации.</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background: #F8FAFC; border-radius: 10px; padding: 15px; margin-top: 20px; border: 1px dashed #CBD5E1; font-size: 0.95rem;">
                    <b>💡 Мнение ученых:</b> Каспий живет циклами. Нынешнее состояние — это вызов для экономики, но с точки зрения геологии море неоднократно проходило через подобные и даже более глубокие минимумы.
                </div>
            """, unsafe_allow_html=True)

    # --- КОНЕЦ БЛОКА ЦИКЛИЧНОСТИ ---

    with b_col2:
        # 1. Заголовок (внутри колонки)
        st.markdown('<div class="white-label-header"><p class="section-header-text">⏳ Исторические минимумы и максимумы</p></div>', unsafe_allow_html=True)
        
        # 2. Колонки для плашек
        r1_c1, r1_c2 = st.columns(2)
        r2_c1, r2_c2 = st.columns(2)
        
        history_cards = [
            {"year": "1903", "val": "-25,74 м", "col": r1_c1, "label": "Максимум"},
            {"year": "1977", "val": "-29,01 м", "col": r1_c2, "label": "Минимум XX в."},
            {"year": "1995", "val": "-26,62 м", "col": r2_c1, "label": "Пик подъема"},
            {"year": "2024", "val": "-29,05 м", "col": r2_c2, "label": "Текущий спад"},
        ]

        for card in history_cards:
            with card["col"]:
                st.markdown(f"""
                    <div style="background: white; padding: 15px; border-radius: 15px; border: 1px solid #E2E8F0; margin-bottom: 10px; text-align: center;">
                        <p style="margin: 0; color: #64748B; font-size: 0.8rem; font-weight: 600;">{card['year']} год</p>
                        <p style="margin: 5px 0; color: #1E293B; font-size: 1.2rem; font-weight: 800;">{card['val']}</p>
                        <p style="margin: 0; color: #94A3B8; font-size: 0.7rem;">{card['label']}</p>
                    </div>
                """, unsafe_allow_html=True)

        # 3. ПЕРВЫЙ БЛОК: ИЗМЕНЕНИЕ АКВАТОРИИ
        st.markdown("""
            <div style="background: #F0F9FF; padding: 20px; border-radius: 20px; border: 1px solid #BAE6FD; margin-top: 15px; font-family: 'Montserrat', sans-serif;">
                <p style="margin: 0 0 15px 0; color: #0369A1; font-weight: 800; font-size: 0.9rem; text-align: center; text-transform: uppercase;">
                    Изменение акватории (2006 — 2024)
                </p>
                <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 10px;">
                    <div style="text-align: center;">
                        <p style="margin: 0; color: #64748B; font-size: 0.7rem;">2006 г.</p>
                        <p style="margin: 0; color: #0C4A6E; font-size: 1.1rem; font-weight: 800;">392.3 <span style="font-size: 0.6rem;">тыс. км²</span></p>
                    </div>
                    <div style="flex-grow: 1; position: relative; margin: 0 15px; text-align: center;">
                        <div style="height: 2px; background: #0EA5E9; width: 100%;"></div>
                        <div style="position: absolute; right: -2px; top: -5px; width: 10px; height: 10px; border-top: 2px solid #0EA5E9; border-right: 2px solid #0EA5E9; transform: rotate(45deg);"></div>
                        <span style="background: #0EA5E9; color: white; padding: 1px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: 800; position: relative; top: -20px;">
                            -36.6 тыс. км²
                        </span>
                    </div>
                    <div style="text-align: center;">
                        <p style="margin: 0; color: #0369A1; font-size: 0.7rem; font-weight: 700;">2024 г.</p>
                        <p style="margin: 0; color: #0369A1; font-size: 1.1rem; font-weight: 800;">355.7 <span style="font-size: 0.6rem;">тыс. км²</span></p>
                    </div>
                </div>
                <p style="margin: 0; text-align: center; color: #0C4A6E; font-size: 0.85rem; line-height: 1.4;">
                    За этот период Каспий потерял объем воды, равный <b>47.6 км³</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # 4. ВТОРОЙ БЛОК: КРИТИЧЕСКИЙ ПОРОГ (-34 см)
        st.markdown("""
            <div style="background: #FFF5F5; padding: 20px; border-radius: 20px; border: 1px solid #FECACA; margin-top: 15px; font-family: 'Montserrat', sans-serif; box-shadow: 0 4px 15px rgba(211, 47, 47, 0.05);">
                <p style="margin: 0 0 15px 0; color: #D32F2F; font-weight: 800; font-size: 0.9rem; text-align: center; text-transform: uppercase;">
                    Превышение критического порога
                </p>
                <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 10px;">
                    <div style="text-align: center;">
                        <p style="margin: 0; color: #64748B; font-size: 0.7rem;">РЕКОРД 1977 г.</p>
                        <p style="margin: 0; color: #475569; font-size: 1.2rem; font-weight: 700;">-29.01 м</p>
                    </div>
                    <div style="flex-grow: 1; position: relative; margin: 0 15px; text-align: center;">
                        <div style="height: 2px; background: #D32F2F; width: 100%;"></div>
                        <div style="position: absolute; right: -2px; top: -5px; width: 10px; height: 10px; border-top: 2px solid #D32F2F; border-right: 2px solid #D32F2F; transform: rotate(45deg);"></div>
                        <span style="background: #D32F2F; color: white; padding: 2px 10px; border-radius: 10px; font-size: 0.9rem; font-weight: 900; position: relative; top: -22px; display: inline-block;">
                            ⬇ -34 см
                        </span>
                    </div>
                    <div style="text-align: center;">
                        <p style="margin: 0; color: #D32F2F; font-size: 0.7rem; font-weight: 800;">ФАКТ 2025 г.</p>
                        <p style="margin: 0; color: #D32F2F; font-size: 1.5rem; font-weight: 900;">-29.35 м</p>
                    </div>
                </div>
                <p style="margin: 0; text-align: center; color: #334155; font-size: 0.85rem; line-height: 1.4;">
                    Уровень моря опустился ниже самого низкого значения XX века.
                </p>
            </div>
        """, unsafe_allow_html=True)



    # --- ОБЩИЙ БЛОК: ОСНОВНЫЕ ФАКТОРЫ ---
    st.markdown("<hr style='margin: 40px 0; opacity: 0.1;'>", unsafe_allow_html=True)
    st.markdown('<div class="white-label-header"><p class="section-header-text">🔍 Основные факторы, влияющие на изменение уровня</p></div>', unsafe_allow_html=True)

    # Общий подзаголовок на всю ширину (тот самый текст)
    st.markdown("""
        <div style="margin-bottom: 30px; text-align: center;">
            <p style="font-style: italic; color: #64748B; font-size: 1.1rem; max-width: 800px; margin: 0 auto;">
                Изменения элементов водного баланса, обусловленные антропогенным воздействием и природными циклами.
            </p>
        </div>
    """, unsafe_allow_html=True)

    f_col1, f_col2 = st.columns(2)

    # --- ЛЕВЫЙ БЛОК: РЕЧНОЙ СТОК ---
    with f_col1:
        st.markdown('<div class="promo-bold">🌊 Речной сток и вклад Волги</div>', unsafe_allow_html=True)
        # Фиксируем высоту контейнера описания (80px), чтобы плашки ниже начались на одном уровне
        st.markdown("""
            <div style="height: 80px;">
                <p class="promo-sub" style="font-style: italic; border-left: 4px solid #0072FF; padding-left: 15px; margin: 0;">
                    Волга обеспечивает около 80% всего речного притока. Критические минимумы стока напрямую коррелируют с падением уровня моря.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
    # Данные распределены по двум категориям: Бассейн (все реки) и Волга
        river_stats = [
            # ПЕРВЫЙ РЯД: Все реки
            {"val": "210,2", "lbl": "Мин. сток всех рек<br>(1973 г.), км³", "bg": "#475569"},
            {"val": "290,3", "lbl": "Средний сток<br>всех рек, км³", "bg": "#334155"},
            {"val": "393,4", "lbl": "Макс. сток всех рек<br>(1990 г.), км³", "bg": "#1E293B"},
            # ВТОРОЙ РЯД: Волга
            {"val": "166,0", "lbl": "Мин. сток Волги<br>(1975 г.), км³", "bg": "#337AB7"},
            {"val": "236,2", "lbl": "Средний сток<br>Волги, км³", "bg": "#2A6091"},
            {"val": "333,2", "lbl": "Макс. сток Волги<br>(1994 г.), км³", "bg": "#1D4E77"}
        ]

        # Стили для анимации плашек (если еще не добавлены ранее)
        st.markdown("""
        <style>
            .river-card {
                transition: all 0.3s ease !important;
            }
            .river-card:hover {
                transform: scale(1.03);
                box-shadow: 0 10px 15px rgba(0,0,0,0.1) !important;
                filter: brightness(1.1);
            }
        </style>
        """, unsafe_allow_html=True)

        # Рендерим первый ряд (Все реки)
        r_row1 = st.columns(3)
        for i in range(3):
            with r_row1[i]:
                st.markdown(f"""
                    <div class="river-card" style="background: {river_stats[i]['bg']}; padding: 15px; border-radius: 20px; text-align: center; 
                                min-height: 140px; display: flex; flex-direction: column; justify-content: center; 
                                box-shadow: 0 4px 6px rgba(0,0,0,0.05); color: white; margin-bottom: 10px;">
                        <div style="font-size: 1.5rem; font-weight: 900; font-family: 'Exo 2', sans-serif;">{river_stats[i]['val']}</div>
                        <div style="font-size: 0.7rem; margin-top: 8px; opacity: 0.9; font-weight: 600; text-transform: uppercase; line-height: 1.2;">{river_stats[i]['lbl']}</div>
                    </div>
                """, unsafe_allow_html=True)

        # Рендерим второй ряд (Волга)
        r_row2 = st.columns(3)
        for i in range(3, 6):
            with r_row2[i-3]:
                st.markdown(f"""
                    <div class="river-card" style="background: {river_stats[i]['bg']}; padding: 15px; border-radius: 20px; text-align: center; 
                                min-height: 140px; display: flex; flex-direction: column; justify-content: center; 
                                box-shadow: 0 4px 6px rgba(0,0,0,0.05); color: white; margin-bottom: 20px;">
                        <div style="font-size: 1.5rem; font-weight: 900; font-family: 'Exo 2', sans-serif;">{river_stats[i]['val']}</div>
                        <div style="font-size: 0.7rem; margin-top: 8px; opacity: 0.9; font-weight: 600; text-transform: uppercase; line-height: 1.2;">{river_stats[i]['lbl']}</div>
                    </div>
                """, unsafe_allow_html=True)

        # Данные для графика (оставляем как были)
        river_data = {
            "Год": [1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
            "Бассейн": [247.5, 215.7, 219.7, 232.5, 254.0, 315.1, 340.0, 293.1, 307.6, 259.2, 349.8, 384.0, 347.4, 274.0, 299.6, 279.9, 294.9, 318.6, 259.6, 341.3, 255.6, 350.7, 360.1, 278.0, 255.0, 268.9, 282.6, 327.2, 276.6, 266.2, 334.1, 229.3, 269.8, 268.8, 313.7, 268.9, 263.9, 210.2, 312.0, 207.1, 223.3, 223.3, 319.4, 364.6, 286.1, 350.1, 270.3, 274.4, 273.3, 335.9, 333.7, 329.8, 297.7, 268.1, 393.4, 369.8, 302.9, 348.4, 392.2, 324.9, 250.8, 276.67, 320.7, 320.9, 293.24, 306.73, 306.7, 294.78, 310.41, 334.8, 241.42, 319.81, 266.55, 266.9, 248.9, 223.2, 266.8, 297.0, 249.6, 216.5, 304.6, 313.2, 280.5, 279.0, 305.1, 236.6, 239.2, 214.2],
            "Волга": [None, None, 181.8, 174.2, 190.3, 232.1, 262.5, 238.7, 233.8, 202.0, 256.5, 306.6, None, 217.9, 222.8, 217.4, 217.4, 251.6, 214.9, 272.1, 210.2, None, 275.3, 212.8, 206.2, 229.1, 233.6, 260.1, 213.6, 211.9, 275.5, 180.0, 209.4, 212.2, 258.3, 221.6, 201.5, None, 238.4, 166.0, 187.1, 195.3, 273.5, 303.5, 252.6, 288.1, 218.8, 225.6, 224.3, 282.5, 288.7, 273.2, 225.4, 221.5, 308.3, 302.6, 239.4, 275.6, 333.2, 273.6, 176.0, 236.2, 277.0, 283.3, 241.5, 272.3, 254.2, 244.1, 255.3, 279.9, 201.8, 275.8, 229.5, 228.6, 196.6, 189.0, 229.6, 257.3, 212.2, 181.6, 261.2, 272.1, 244.9, 205.2, 279.9, 208.3, 211.6, 207.0]
        }

        fig_river = go.Figure()
        fig_river.add_trace(go.Scatter(x=river_data["Год"], y=river_data["Бассейн"], name="Сток всех рек", mode='lines', line=dict(color='#94A3B8', width=1.5, dash='dot')))
        fig_river.add_trace(go.Scatter(x=river_data["Год"], y=river_data["Волга"], name="Сток Волги", mode='lines', line=dict(color='#0072FF', width=3)))

        fig_river.update_layout(
            height=300, margin=dict(l=10,r=10,t=20,b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", y=-0.3, xanchor="center", x=0.5),
            yaxis_title="км³/год", xaxis_title="год"
        )
        st.plotly_chart(fig_river, use_container_width=True, config={'displayModeBar': False})

    # --- ПРАВЫЙ БЛОК: КЛИМАТ ---
    with f_col2:
        st.markdown('<div class="promo-bold">🌡️ Изменения климата</div>', unsafe_allow_html=True)
        # Те же 80px высоты для выравнивания
        st.markdown("""
            <div style="height: 80px;">
                <p class="promo-sub" style="font-style: italic; border-left: 4px solid #CC661D; padding-left: 15px; margin: 0;">
                    Рост температуры воздуха и испарения с поверхности моря относительно базового периода 1991-2020 гг.
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        
        speed_data = [
            {"label": "Земной шар", "val": "0,19°C", "bg": "#FFF1C1", "text": "#003366"},
            {"label": "Казахстан", "val": "0,36°C", "bg": "#FFE082", "text": "#003366"},
            {"label": "Каспийский регион", "val": "0,51°C", "bg": "#CC661D", "text": "#FFFFFF"} # Белый текст для темного фона
        ]

        for i, col in enumerate([c1, c2, c3]):
            with col:
                st.markdown(f"""
                    <div style="background: {speed_data[i]['bg']}; padding: 15px; border-radius: 20px; text-align: center; min-height: 160px; 
                                display: flex; flex-direction: column; justify-content: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                        <div style="color: {'red' if i < 2 else 'white'}; font-size: 1.6rem; font-weight: 900; font-family: 'Exo 2', sans-serif; line-height: 1;">{speed_data[i]['val']}</div>
                        <div style="color: {'#475569' if i < 2 else 'white'}; font-size: 0.75rem; margin: 8px 0; opacity: 0.8;">каждые 10 лет</div>
                        <div style="color: {speed_data[i]['text']}; font-size: 0.9rem; font-weight: 700; line-height: 1.1;">{speed_data[i]['label']}</div>
                    </div>
                """, unsafe_allow_html=True)

        
        # --- КОНЕЦ ПЛАШЕК ---

        # Данные для графика аномалий
        climate_years = [1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
        avg_anomaly = [-2.3, -1.1, -1.3, 0.1, -1.5, 0.0, -1.7, 0.0, -1.4, -1.5, -0.7, -1.9, -0.8, 0.1, -0.4, -0.2, -1.0, -2.3, -1.6, 0.9, -0.8, -0.7, -0.5, 0.5, 0.3, 0.2, -0.1, -0.8, 1.0, 0.6, -0.2, 0.7, -0.4, -0.1, 1.1, -0.8, -0.1, 0.8, -0.1, 0.5, 0.7, 0.6, 0.2, 0.8, 0.9, 1.4, 1.2, 1.7, 1.2, 1.4]
        min_anomaly = [-2.5, -1.6, -1.5, -0.2, -1.8, -0.5, -2.0, -0.8, -1.9, -1.9, -1.1, -2.6, -1.1, -0.2, -0.7, -0.4, -1.2, -2.5, -2.4, 0.4, -1.2, -1.1, -1.0, 0.3, 0.1, 0.0, -0.4, -1.1, 0.8, 0.2, -0.6, 0.5, -0.7, -0.4, 0.9, -1.1, -0.3, 0.6, -0.6, 0.1, 0.3, 0.3, -0.4, 0.4, 0.5, 0.9, 0.7, 1.2, 0.5, 0.8]
        max_anomaly = [-2.0, -0.7, -1.1, 0.3, -1.2, 0.5, -1.5, 0.6, -1.1, -1.1, -0.4, -1.2, -0.6, 0.4, 0.0, 0.3, -0.7, -1.9, -1.2, 1.4, -0.4, -0.4, -0.2, 0.8, 0.6, 0.4, 0.1, -0.3, 1.3, 1.0, 0.0, 0.8, -0.2, 0.1, 1.5, -0.6, 0.3, 1.2, 0.3, 0.6, 1.0, 0.9, 0.7, 1.1, 1.6, 2.0, 1.5, 2.3, 1.4, 2.1]
        sea_level = [-28.45, -28.53, -28.54, -28.66, -28.89, -28.97, -28.88, -28.61, -28.43, -28.24, -28.15, -28.07, -28.10, -27.97, -27.90, -27.83, -27.75, -27.82, -27.68, -27.26, -27.14, -26.91, -26.70, -26.59, -26.81, -27.05, -27.07, -27.07, -27.18, -27.20, -27.20, -27.11, -27.00, -26.98, -27.06, -27.08, -27.17, -27.21, -27.31, -27.50, -27.56, -27.61, -27.70, -27.92, -27.97, -27.94, -28.10, -28.29, -29.05, -29.35]

        fig_climate = go.Figure()
        
        # Слой с разбросом
        fig_climate.add_trace(go.Scatter(x=climate_years+climate_years[::-1], y=max_anomaly+min_anomaly[::-1], fill='toself', fillcolor='rgba(200, 200, 200, 0.3)', line=dict(color='rgba(255,255,255,0)'), name='Разброс станций'))
        
        # Линии данных
        fig_climate.add_trace(go.Scatter(x=climate_years, y=avg_anomaly, name="Аномалия T°C", line=dict(color='#D32F2F', width=2.5)))
        fig_climate.add_trace(go.Scatter(x=climate_years, y=sea_level, name="Уровень моря", line=dict(color='#003366', width=2), yaxis="y2"))

        # --- ЛИНИЯ ТЕКУЩЕГО МОМЕНТА ---
        fig_climate.add_vline(x=2025, line_width=2, line_dash="dash", line_color="#D32F2F")

        # --- АННОТАЦИИ ---
        
        # 1. Минимум 1977
        fig_climate.add_annotation(
            x=1977, y=-29.01, yref="y2",
            text="<b>-29.01 м</b><br>(1977 г.)",
            showarrow=True, arrowhead=2, ax=0, ay=40, bgcolor="white"
        )

        # 2. Пик 1995
        fig_climate.add_annotation(
            x=1995, y=-26.62, yref="y2",
            text="<b>-26.62 м</b><br>(1995 г.)",
            showarrow=True, arrowhead=2, ax=0, ay=-40, bgcolor="white"
        )

        # 3. Текущая точка 2025
        fig_climate.add_annotation(
            x=2025, y=-29.35, yref="y2",
            text="<b>СЕЙЧАС</b><br>-29.35 м",
            showarrow=True, arrowhead=2, arrowcolor="red",
            ax=-50, ay=0, bgcolor="#FFEBEE", bordercolor="red"
        )

        fig_climate.update_layout(
            height=380, margin=dict(l=10,r=10,t=20,b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", y=-0.3, xanchor="center", x=0.5),
            yaxis=dict(title="Аномалия воздуха, °C", range=[-3, 3]),
            yaxis2=dict(title="Уровень моря, м БС", overlaying="y", side="right", range=[-30, -25], showgrid=False)
        )
        
        st.plotly_chart(fig_climate, use_container_width=True, config={'displayModeBar': False})

    # --- БЛОК: ГЛОБАЛЬНЫЕ ПОСЛЕДСТВИЯ ---
    st.markdown("<hr style='margin: 40px 0; opacity: 0.1;'>", unsafe_allow_html=True)
    st.markdown('<div class="white-label-header"><p class="section-header-text">⚠️ Комплексное влияние на регион</p></div>', unsafe_allow_html=True)

    # 1. Добавляем CSS стили для анимации
    st.markdown("""
    <style>
        .impact-card {
            transition: all 0.3s ease-in-out !important;
            cursor: default;
            border: 1px solid rgba(0,0,0,0.05);
        }
        
        .impact-card:hover {
            transform: translateY(-5px) scale(1.02); /* Увеличение и подъем */
            box-shadow: 0 12px 20px rgba(0,0,0,0.1) !important; /* Свечение/Тень */
            filter: brightness(1.02); /* Легкое осветление */
            border: 1px solid rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

    impact_items = [
        {
            "icon": "🚢", "title": "Логистика", 
            "desc": "<b>Снижение перевозок:</b> Падение глубин в портах Актау и Курык требует дноуглубления и ограничивает тоннаж судов.",
            "bg": "#E0F2FE", "text": "#0369A1"
        },
        {
            "icon": "💧", "title": "Гидрология", 
            "desc": "<b>Обмеление протоков:</b> Нарушение водообмена в дельтах, дефицит пресной воды в прибрежных поселках.",
            "bg": "#DBEAFE", "text": "#1E40AF"
        },
        {
            "icon": "🐟", "title": "Биоресурсы", 
            "desc": "<b>Сокращение нерестилищ:</b> Исчезновение мелководных зон размножения осетровых и ценных видов рыб.",
            "bg": "#DCFCE7", "text": "#166534"
        },
        {
            "icon": "❄️", "title": "Климат", 
            "desc": "<b>Ледовый покров:</b> Сокращение площади льда меняет критические условия жизни каспийского тюленя.",
            "bg": "#F1F5F9", "text": "#475569"
        },
        {
            "icon": "🗺️", "title": "География", 
            "desc": "<b>Береговая линия:</b> Смещение границы воды на километры делает причалы и порты неэффективными.",
            "bg": "#FEF9C3", "text": "#854D0E"
        },
        {
            "icon": "🌿", "title": "Экосистемы", 
            "desc": "<b>Флора и фауна:</b> Деградация уникальной растительности и прибрежных водно-болотных угодий.",
            "bg": "#F0FDF4", "text": "#166534"
        }
    ]

    # Создаем сетку 3 колонки x 2 ряда
    for i in range(0, len(impact_items), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(impact_items):
                item = impact_items[i + j]
                with cols[j]:
                    # Добавляем класс impact-card в div
                    st.markdown(f"""
                        <div class="impact-card" style="
                            background: {item['bg']}; 
                            padding: 25px; 
                            border-radius: 20px; 
                            min-height: 220px; 
                            margin-bottom: 20px;
                            display: flex; 
                            flex-direction: column;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
                        ">
                            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                <span style="font-size: 2rem; margin-right: 15px;">{item['icon']}</span>
                                <span style="color: {item['text']}; font-weight: 800; font-size: 1.2rem; text-transform: uppercase;">{item['title']}</span>
                            </div>
                            <div style="color: #334155; font-size: 0.95rem; line-height: 1.5;">
                                {item['desc']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    # --- КОНЕЦ БЛОКА ---


    # --- БЛОК: ПРОГНОЗЫ И ПРОДУКЦИЯ С ЭФФЕКТОМ НАЖАТИЯ ---
    st.markdown("<hr style='margin: 40px 0; opacity: 0.1;'>", unsafe_allow_html=True)
    st.markdown('<div class="white-label-header"><p class="section-header-text">🔮 Прогнозы и информационная продукция</p></div>', unsafe_allow_html=True)

    # Расширенные стили для анимации плашек
    st.markdown("""
    <style>
        /* Контейнер карточки прогноза */
        .interactive-card {
            padding: 25px;
            border-radius: 15px;
            color: white;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); /* Плавный переход */
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            min-height: 280px;
            display: flex;
            flex-direction: column;
            user-select: none; /* Чтобы текст не выделялся при частом нажатии */
        }

        /* Эффект при наведении курсора */
        .interactive-card:hover {
            transform: translateY(-8px); /* Приподнимаем */
            box-shadow: 0 12px 20px rgba(0,0,0,0.2); /* Усиливаем тень */
        }

        /* Эффект при клике (нажатии) */
        .interactive-card:active {
            transform: translateY(-2px); /* Слегка опускаем обратно */
            box-shadow: 0 2px 4px rgba(0,0,0,0.2); /* Ослабляем тень */
            filter: brightness(0.9); /* Слегка затемняем */
        }

        .forecast-title-large {
            font-family: 'Exo 2', sans-serif;
            font-weight: 800;
            font-size: 1.4em;
            text-transform: uppercase;
            margin-bottom: 15px;
            letter-spacing: 1px;
        }

        .forecast-text-large {
            font-size: 1.1em;
            line-height: 1.4;
            opacity: 0.95;
        }
    </style>
    """, unsafe_allow_html=True)

    m_col1, m_col2 = st.columns([1.6, 1.4])

    with m_col1:
        st.markdown('<div class="promo-bold" style="font-size: 1.5em; margin-bottom:20px;">🛠️ Методы прогнозирования</div>', unsafe_allow_html=True)
        
        p1, p2, p3 = st.columns(3)
        forecast_items = [
            {"title": "УРОВЕНЬ", "desc": "Модели <b>WRF</b> & <b>Mike21</b>", "bg": "linear-gradient(135deg, #1D4E77 0%, #2A6091 100%)"},
            {"title": "ВОЛНЕНИЕ", "desc": "Модели <b>WRF</b> & <b>SWAN</b>", "bg": "linear-gradient(135deg, #337AB7 0%, #4A90E2 100%)"},
            {"title": "ЛЕД", "desc": "Статистический метод расчета", "bg": "linear-gradient(135deg, #A3C8E7 0%, #CDE4F7 100%)"}
        ]

        for i, col in enumerate([p1, p2, p3]):
            with col:
                st.markdown(f"""
                    <div class="interactive-card" style="background: {forecast_items[i]['bg']};">
                        <div class="forecast-title-large">{forecast_items[i]['title']}</div>
                        <p class="forecast-text-large">{forecast_items[i]['desc']}</p>
                    </div>
                """, unsafe_allow_html=True)

    with m_col2:
        st.markdown('<div class="promo-bold" style="font-size: 1.5em; margin-bottom:20px;">📄 Выпускаемая продукция</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #FAFAFA; padding: 30px; border-radius: 15px; border: 1px solid #E0E0E0; min-height: 280px;">
            <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                <div style="flex: 1; min-width: 220px;">
                    <div style="margin-bottom:18px;"><span style="font-size:1.15em; font-weight:700;">📅 Бюллетень по морю</span><br><span style="color:#0072FF; font-weight:600;">Еженедельно (пт)</span></div>
                    <div style="margin-bottom:18px;"><span style="font-size:1.15em; font-weight:700;">🌊 Бюллетень волнения</span><br><span style="color:#0072FF; font-weight:600;">Еженедельно (пт)</span></div>
                    <div style="margin-bottom:18px;"><span style="font-size:1.15em; font-weight:700;">❄️ Обзор льда</span><br><span style="color:#0072FF; font-weight:600;">Еженедельно (вт)</span></div>
                </div>
                <div style="flex: 1; min-width: 220px;">
                    <div style="margin-bottom:18px;"><span style="font-size:1.15em; font-weight:700;">🌀 Сгонно-нагонные</span><br><span style="color:#0072FF; font-weight:600;">Раз в месяц</span></div>
                    <div style="margin-bottom:18px;"><span style="font-size:1.15em; font-weight:700;">📈 Прогноз условий</span><br><span style="color:#0072FF; font-weight:600;">2 раза в неделю</span></div>
                    <div style="margin-bottom:18px;"><span style="font-size:1.15em; font-weight:700;">📁 Водный кадастр</span><br><span style="color:#0072FF; font-weight:600;">Ежегодно</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    # --- БЛОК: ДОЛГОСРОЧНЫЙ ПРОГНОЗ ---
    st.markdown("<hr style='margin: 40px 0; opacity: 0.1;'>", unsafe_allow_html=True)
    st.markdown('<div class="white-label-header"><p class="section-header-text">🔭 Долгосрочная оценка изменений</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="promo-sub" style="margin-bottom: 25px; font-size: 1.1em !important;">'
                'РГП «Казгидромет» проводятся исследования по долгосрочной оценке изменения уровня и параметров волнения.'
                '</div>', unsafe_allow_html=True)

    # Стили для интерактива (если они еще не объявлены выше)
    st.markdown("""
    <style>
        .long-term-card {
            padding: 30px;
            border-radius: 20px;
            color: white;
            transition: all 0.3s ease;
            cursor: pointer;
            min-height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        }
        .long-term-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        }
        .long-term-card:active {
            transform: translateY(-2px);
        }
        .lt-title {
            font-family: 'Exo 2', sans-serif;
            font-weight: 800;
            font-size: 1.6em;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        .lt-desc {
            font-size: 1.15em;
            opacity: 0.9;
            line-height: 1.4;
        }
    </style>
    """, unsafe_allow_html=True)

    lt_col1, lt_col2 = st.columns(2)

    with lt_col1:
        st.markdown("""
            <div class="long-term-card" style="background: linear-gradient(135deg, #003366 0%, #00509E 100%);">
                <div class="lt-title">🌊 Долгосрочный уровень</div>
                <div class="lt-desc">
                    Анализ вековых колебаний и расчет сценариев изменения уровня моря до конца XXI века на основе глобальных климатических моделей.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with lt_col2:
        st.markdown("""
            <div class="long-term-card" style="background: linear-gradient(135deg, #337AB7 0%, #5BC0DE 100%);">
                <div class="lt-title">🌬️ Режим волнения</div>
                <div class="lt-desc">
                    Оценка будущих изменений ветрового волнения и штормовой активности в казахстанском секторе Каспийского моря.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        
    # --- ОБНОВЛЕННЫЙ БЛОК: ДОЛГОСРОЧНЫЙ ПРОГНОЗ С SSP ---
    st.markdown("<br>", unsafe_allow_html=True)
    lt_plot_col1, lt_plot_col2 = st.columns([1.6, 1.4])

    with lt_plot_col1:
        st.markdown('<div class="promo-bold" style="font-size: 1.3em; margin-bottom: 10px;">📉 Прогноз уровня моря до 2050 г. (RCP & SSP)</div>', unsafe_allow_html=True)
        
        # Расширенные данные прогноза
        data = {
            "Год": list(range(2006, 2051)),
            "Факт": [-27.04, -27.07, -27.13, -27.15, -27.25, -27.50, -27.57, -27.61, -27.74, -27.98, -27.99, -27.99, -28.03, -28.21, -28.24, -28.43, -28.67, -28.87, -29.18] + [None]*26,
            "RCP4.5": [None]*18 + [-29.18, -29.16, -29.39, -29.64, -29.77, -29.88, -29.81, -29.94, -30.01, -30.09, -30.34, -30.56, -30.78, -30.87, -30.82, -30.95, -30.95, -31.08, -31.26, -31.52, -31.72, -31.89, -32.03, -32.16, -32.07, -32.17, -32.42],
            "RCP8.5": [None]*18 + [-29.18, -29.37, -29.37, -29.43, -29.62, -29.76, -29.95, -30.16, -30.43, -30.51, -30.47, -30.67, -30.92, -31.17, -31.38, -31.54, -31.78, -32.02, -32.22, -32.36, -32.60, -32.77, -33.03, -33.26, -33.51, -33.74, -33.99],
            "SSP1-2.6": [None]*18 + [-29.18, -29.33, -29.52, -29.65, -29.76, -29.88, -30.05, -30.22, -30.41, -30.53, -30.67, -30.81, -30.91, -31.01, -31.12, -31.24, -31.33, -31.53, -31.62, -31.75, -31.88, -31.94, -32.01, -32.18, -32.34, -32.49, -32.67],
            "SSP5-8.5": [None]*18 + [-28.87, -28.64, -28.58, -28.58, -28.74, -28.92, -28.94, -29.02, -29.05, -29.21, -29.34, -29.51, -29.65, -29.79, -29.81, -29.88, -30.00, -30.13, -30.20, -30.21, -30.32, -30.51, -30.63, -30.74, -30.90, -30.99, -31.13, -31.38]
        }
        
        fig_lt = go.Figure()

        # Историческая линия (сплошная жирная)
        fig_lt.add_trace(go.Scatter(x=data["Год"], y=data["Факт"], name="<b>Факт (измерения)</b>", line=dict(color="#1e293b", width=4)))
        
        # Сценарии RCP (предыдущее поколение моделей)
        fig_lt.add_trace(go.Scatter(x=data["Год"], y=data["RCP4.5"], name="RCP 4.5 (умер.)", line=dict(color="#337AB7", width=2.5, dash='dash')))
        fig_lt.add_trace(go.Scatter(x=data["Год"], y=data["RCP8.5"], name="RCP 8.5 (экстр.)", line=dict(color="#D32F2F", width=2.5, dash='dash')))
        
        # Сценарии SSP (новое поколение моделей)
        fig_lt.add_trace(go.Scatter(x=data["Год"], y=data["SSP1-2.6"], name="SSP1-2.6 ('Зеленый')", line=dict(color="#2E7D32", width=2.5, dash='dot')))
        fig_lt.add_trace(go.Scatter(x=data["Год"], y=data["SSP5-8.5"], name="SSP5-8.5 (Инерц.)", line=dict(color="#FF8F00", width=2.5, dash='dot')))

        fig_lt.update_layout(
            height=450, margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified",
            legend=dict(orientation="h", y=-0.25, xanchor="center", x=0.5, font=dict(size=10)),
            yaxis=dict(title="м БС", gridcolor='#E2E8F0', range=[-35, -26]),
            xaxis=dict(showgrid=False, dtick=5)
        )
        
        # Линия раздела (начало прогноза)
        fig_lt.add_vline(x=2024, line_width=1, line_dash="solid", line_color="#94a3b8")
        
        st.plotly_chart(fig_lt, use_container_width=True, config={'displayModeBar': False})

    with lt_plot_col2:
        # Здесь остается ваша карта/заглушка по волнению
        st.markdown('<div class="promo-bold" style="font-size: 1.3em; margin-bottom: 10px;">🌊 Карта изменений волнения</div>', unsafe_allow_html=True)
        st.markdown("""
            <div style="background: #f1f5f9; border: 2px dashed #cbd5e1; border-radius: 15px; height: 450px; display: flex; align-items: center; justify-content: center; flex-direction: column; color: #64748b;">
                <span style="font-size: 4em; margin-bottom: 10px;">🗺️</span>
                <p style="font-size: 1.1em; font-weight: 500;">Место для визуализации волнения</p>
            </div>
        """, unsafe_allow_html=True)


    # --- БЛОК: ПРОГНОЗЫ И БУДУЩЕЕ ---
    st.markdown("<hr style='margin: 40px 0; opacity: 0.1;'>", unsafe_allow_html=True)
    st.markdown('<div class="white-label-header"><p class="section-header-text">🔮 Будущее Каспия: Сценарии до 2100 года</p></div>', unsafe_allow_html=True)

    # Описание прогнозов
    st.markdown("""
        <div style="margin-bottom: 30px; color: #475569; line-height: 1.6;">
            Согласно международным климатическим моделям (CMIP6), уровень Каспийского моря продолжит снижаться под влиянием глобального потепления. 
            Ниже представлены три научно обоснованных сценария изменения уровня к концу столетия:
        </div>
    """, unsafe_allow_html=True)

    # Горизонтальные плашки прогноза
    f_col1, f_col2, f_col3 = st.columns(3)

    with f_col1:
        st.markdown("""
            <div class="forecast-card" style="background: linear-gradient(135deg, #34D399 0%, #059669 100%);">
                <div class="fc-year">Оптимистичный (SSP1-2.6)</div>
                <div class="fc-value">-9<span class="fc-unit">метров</span></div>
                <div class="fc-desc">Стабилизация климата и сохранение текущего притока рек.</div>
            </div>
        """, unsafe_allow_html=True)

    with f_col2:
        st.markdown("""
            <div class="forecast-card" style="background: linear-gradient(135deg, #FBBF24 0%, #D97706 100%);">
                <div class="fc-year">Умеренный (SSP2-4.5)</div>
                <div class="fc-value">-14<span class="fc-unit">метров</span></div>
                <div class="fc-desc">Продолжение потепления и частичное обмеление северной части.</div>
            </div>
        """, unsafe_allow_html=True)

    with f_col3:
        st.markdown("""
            <div class="forecast-card" style="background: linear-gradient(135deg, #F87171 0%, #DC2626 100%);">
                <div class="fc-year">Пессимистичный (SSP5-8.5)</div>
                <div class="fc-value">-18<span class="fc-unit">метров</span></div>
                <div class="fc-desc">Критическое испарение и полная трансформация экосистемы.</div>
            </div>
        """, unsafe_allow_html=True)

    # --- БЛОК: ПОСЛЕДСТВИЯ И ВЫЗОВЫ ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="promo-bold" style="text-align: center;">🚨 Ключевые риски при снижении уровня</div>', unsafe_allow_html=True)

    risk_c1, risk_c2, risk_c3, risk_c4 = st.columns(4)

    risks = [
        {"icon": "🚢", "title": "Транспорт", "text": "Ограничение работы портов и судоходных каналов."},
        {"icon": "🐟", "title": "Биоресурсы", "text": "Уничтожение мест нереста осетровых рыб."},
        {"icon": "🏙️", "title": "Инфраструктура", "text": "Нарушение работы водозаборов прибрежных городов."},
        {"icon": "🌫️", "title": "Экология", "text": "Пыльные бури с обнаженного дна (солончаки)."}
    ]

    for i, col in enumerate([risk_c1, risk_c2, risk_c3, risk_c4]):
        with col:
            st.markdown(f"""
                <div style="text-align: center; padding: 20px; background: white; border-radius: 15px; border: 1px solid #E2E8F0; min-height: 200px;">
                    <div style="font-size: 3rem; margin-bottom: 10px;">{risks[i]['icon']}</div>
                    <div style="font-weight: 800; color: #1E293B; margin-bottom: 5px;">{risks[i]['title']}</div>
                    <div style="font-size: 0.85rem; color: #64748B;">{risks[i]['text']}</div>
                </div>
            """, unsafe_allow_html=True)



    # --- ФИНАЛЬНЫЙ ПОДВАЛ (FOOTER) ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background: #001f3f; padding: 40px; border-radius: 30px 30px 0 0; color: white; text-align: center;">
            <h2 style="font-weight: 900; margin-bottom: 10px;">СОХРАНИМ КАСПИЙ ВМЕСТЕ</h2>
            <p style="opacity: 0.8; font-size: 1.1rem; max-width: 700px; margin: 0 auto 25px auto;">
                Мониторинг Казгидромета — это основа для принятия государственных решений по адаптации к изменениям климата.
            </p>
            <div style="display: flex; justify-content: center; gap: 30px; font-weight: 600;">
                <span>🌐 www.kazhydromet.kz</span>
                <span>📧 caspian@meteo.kz</span>
                <span>📞 +7 (7172) 79-83-94</span>
            </div>
            <hr style="opacity: 0.2; margin: 25px 0;">
            <p style="font-size: 0.8rem; opacity: 0.5;">© 2025 РГП «Казгидромет». Все данные защищены.</p>
        </div>
    """, unsafe_allow_html=True)



with tabs[0]:
    # 1. СТИЛИЗАЦИЯ
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;600;800&family=Orbitron:wght@400;700;900&family=Inter:wght@400;600&display=swap');

        .main-title-promo {
            font-family: 'Orbitron', sans-serif;
            background: linear-gradient(90deg, #001f3f, #004A99, #0072FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            font-weight: 900;
            font-size: 3.5em;
            text-transform: uppercase;
            margin-bottom: 10px;
            letter-spacing: 2px;
        }

        .promo-subtitle {
            text-align: center;
            font-family: 'Exo 2', sans-serif;
            color: #546e7a;
            font-size: 1.2em;
            margin-bottom: 40px;
            font-weight: 400;
        }

        /* Карточка с эффектом стекла */
        .monitor-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 24px;
            padding: 25px;
            min-height: 380px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 10px 30px rgba(0, 74, 153, 0.08);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 1px solid #e3f2fd;
        }

        .monitor-card:hover {
            transform: translateY(-12px);
            box-shadow: 0 20px 40px rgba(0, 74, 153, 0.15);
        }

        .card-header-text {
            font-family: 'Exo 2', sans-serif;
            color: #003366;
            font-weight: 800;
            font-size: 1.4em;
            margin-bottom: 15px;
            border-bottom: 2px solid #0072FF;
            padding-bottom: 10px;
        }

        .stat-val {
            font-family: 'JetBrains Mono', monospace;
            color: #0072FF;
            font-weight: 800;
            font-size: 1.2em;
        }

        /* Баннер Казгидромет */
        .kaz-banner {
            background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
            padding: 30px;
            border-radius: 20px;
            border-left: 8px solid #004a99;
            margin-bottom: 35px;
            position: relative;
            overflow: hidden;
        }

        .kaz-banner::after {
            content: "KAZHYDROMET";
            position: absolute;
            right: -20px;
            bottom: -10px;
            font-family: 'Orbitron', sans-serif;
            font-size: 4em;
            color: rgba(0, 74, 153, 0.03);
            font-weight: 900;
        }

        .param-card {
            background: white;
            border-radius: 15px;
            padding: 12px;
            text-align: center;
            border: 1px solid #eceff1;
            transition: all 0.3s ease;
        }
        .param-card:hover {
            background: #004A99;
            color: white !important;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. HEADER
    st.markdown('<h1 class="main-title-promo">РГП «КАЗГИДРОМЕТ»</h1>', unsafe_allow_html=True)
    st.markdown('<p class="promo-subtitle">Национальная гидрометеорологическая служба Казахстана с 1922 года</p>', unsafe_allow_html=True)

    # 3. ГЛАВНЫЙ ИНФО-БАННЕР
    st.markdown("""
        <div class="kaz-banner">
            <h3 style="color: #004a99; margin-top:0;">🌍 Глобальный мониторинг — Национальная безопасность</h3>
            <p style="font-size: 1.1em; color: #334e68; max-width: 85%;">
                «Казгидромет» — фундамент экологической и гидрометеорологической стабильности Казахстана. 
                Вековой опыт и примененяя данные наблюдательной сети, <b>мы создаем точные аналитические продукты для стратегических отраслей</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 4. МЕТРИКИ МАСШТАБА
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("История и опыт", "100+ лет наблюдений", "мониторинг 24/7")
    m2.metric("География", "17 филиалов", "100% охват страны")
    m3.metric("Команда", "3160", "Экспертов в штате")
    m4.metric("Мировой стандарт", "ВМО (WMO)", "с 1993 года")

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. КАРТОЧКИ НАПРАВЛЕНИЙ
    col1, col2, col3, col4 = st.columns(4)
    
    sections = [
        {
            "title": "🌡️ Метеорология",
            "total": "351 Станция",
            "desc": "Глобальный обмен данными с ВМО. Аэрологическое зондирование атмосферы и актинометрия.",
            "items": ["225 Традиционных", "126 Автоматических", "9 Аэрологических"]
        },
        {
            "title": "💧 Гидрология",
            "total": "442 Поста",
            "desc": "Мониторинг трансграничных рек (Урал, Иртыш, Или) и Каспийского моря.",
            "items": ["394 Речных поста", "38 Озерных", "10 Морских станций"]
        },
        {
            "title": "🌾 Агрометео",
            "total": "226 Пунктов",
            "desc": "Обеспечение продовольственной безопасности: прогнозы урожайности и влагозапасов почвы.",
            "items": ["129 На станциях", "97 Постов", "50 Автоматических"]
        },
        {
            "title": "🌱 Экология",
            "total": "175 Постов",
            "desc": "Контроль качества воздуха, почв и радиационного фона во всех регионах РК.",
            "items": ["131 Автоматических", "44 Ручных", "15 Лабораторий"]
        }
    ]

    cols = [col1, col2, col3, col4]
    for i, sec in enumerate(sections):
        with cols[i]:
            items_list = "".join([f'<li style="margin-bottom:5px;"><span class="stat-val">{item.split()[0]}</span> {" ".join(item.split()[1:])}</li>' for item in sec["items"]])
            st.markdown(f"""
                <div class="monitor-card">
                    <div class="card-header-text">{sec['title']}</div>
                    <p style="font-size: 0.9em; color: #455a64; margin-bottom: 15px;">{sec['desc']}</p>
                    <p style="font-weight:700; color:#004A99;">Мощность сети: {sec['total']}</p>
                    <ul style="list-style:none; padding-left:0; font-size:0.95em;">
                        {items_list}
                    </ul>
                </div>
            """, unsafe_allow_html=True)

# 6. ИНТЕРАКТИВНЫЕ ПАРАМЕТРЫ МОНИТОРИНГА
st.markdown("""
    <div style="text-align:center; margin: 30px 0 15px 0;">
        <h3 style="color: #003366; font-family: 'Exo 2'; font-weight: 700;">Наблюдаемые параметры</h3>
        <p style="color: #546e7a; font-size: 0.9em;">Нажмите на карточку, чтобы увидеть процесс мониторинга</p>
    </div>
""", unsafe_allow_html=True)

# Описываем контент для каждого параметра
# Можно указать путь к локальному видео, картинке или YouTube
params_content = {
    "Темп.": {"video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "desc": "Измерение температуры в психометрической будке"},
    "Осадки": {"image": "https://via.placeholder.com/800x450?text=Осадкомер+Третьякова", "desc": "Работа с осадкомером Третьякова"},
    "Ветер": {"video": "https://example.com/wind.mp4", "desc": "Анеморумбометр в действии"},
    "Снег": {"image": "snow.png", "desc": "Снегомерная съемка в степи"},
    "Уровень": {"desc": "Автоматический гидрологический пост"},
    "Расход": {"desc": "Измерение расхода воды вертушкой"},
    "Т. воды": {"desc": "Термический режим рек"},
    "Воздух": {"desc": "Экологический мониторинг атмосферы"},
    "Гамма": {"desc": "Радиационный мониторинг"}
}

params = [
    {"icon": "🌡️", "label": "Темп."},
    {"icon": "🌧️", "label": "Осадки"},    
    {"icon": "🌬️", "label": "Ветер"},
    {"icon": "❄️", "label": "Снег"},
    {"icon": "🌊", "label": "Уровень"},
    {"icon": "📊", "label": "Расход"},   
    {"icon": "🌡️💧", "label": "Т. воды"},
    {"icon": "🧪", "label": "Воздух"},
    {"icon": "☢️", "label": "Гамма"}
]

# Создаем 9 колонок
cols = st.columns(len(params))

# Инициализируем переменную в session_state, чтобы помнить, что выбрали
if "selected_param" not in st.session_state:
    st.session_state.selected_param = None

for i, p in enumerate(params):
    with cols[i]:
        # Стилизуем кнопку так, чтобы она была похожа на карточку
        # В Streamlit кнопка всегда возвращает True при нажатии
        if st.button(f"{p['icon']}\n{p['label']}", key=f"btn_{p['label']}", use_container_width=True):
            st.session_state.selected_param = p['label']

# --- БЛОК ОТОБРАЖЕНИЯ КОНТЕНТА ---
if st.session_state.selected_param:
    param_key = st.session_state.selected_param
    content = params_content.get(param_key, {"desc": "Описание скоро появится..."})
    
    st.markdown("---")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader(f"🎥 Мониторинг: {param_key}")
        # Если есть видео — показываем плеер
        if "video" in content:
            st.video(content["video"])
        # Если есть фото — показываем фото
        elif "image" in content:
            # st.image(content["image"])
            st.info("Здесь будет фото инструментария") # Заглушка
        else:
            st.warning("Медиа-материалы загружаются...")
            
    with c2:
        st.write("### Описание процесса")
        st.write(content["desc"])
        if st.button("Закрыть ✖️"):
            st.session_state.selected_param = None
            st.rerun()                

    # 7. МЕТЕОРОЛОГИЧЕСКИЙ МОНИТОРИНГ
    st.markdown("""
        <div style="text-align:center; margin: 40px 0 20px 0;">
            <h3 style="color: #003366; font-family: 'Exo 2'; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
                Метеорологический мониторинг
            </h3>
            <p style="color: #546e7a; font-size: 1em;">Высокотехнологичная сеть глобального сбора данных об атмосфере</p>
        </div>
    """, unsafe_allow_html=True)

    # Используем 3 колонки для основных типов мониторинга
    met_col1, met_col2, met_col3 = st.columns(3)

    with met_col1:
        st.markdown("""
            <div style="background: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #004A99; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #004A99; margin-top: 0;">📡 Традиционные наблюдения</h4>
                <p style="font-size: 0.9em; color: #455a64;">Вертикальное сканирование атмосферы для авиации и долгосрочных прогнозов.</p>
                <ul style="font-size: 0.85em; color: #1f2937; padding-left: 15px;">
                    <li><b>9 аэрологических станций</b> (выпуск радиозондов)</li>
                    <li>Метеорологические радары (ДМРЛ)</li>
                    <li>Спутниковый прием данных NOAA, EUMETSAT</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with met_col2:
        st.markdown("""
            <div style="background: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #0288d1; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #0288d1; margin-top: 0;">☀️ Специальные измерения</h4>
                <p style="font-size: 0.9em; color: #455a64;">Уникальные наблюдения за энергией солнца и испарением.</p>
                <ul style="font-size: 0.85em; color: #1f2937; padding-left: 15px;">
                    <li><b>Актинометрия:</b> прямая и рассеянная радиация</li>
                    <li><b>Озонометрия:</b> контроль озонового слоя</li>
                    <li>Теплобалансовые наблюдения на ключевых станциях</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with met_col3:
        st.markdown("""
            <div style="background: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #4fc3f7; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #03a9f4; margin-top: 0;">🤖 Автоматизация (АМС)</h4>
                <p style="font-size: 0.9em; color: #455a64;">Переход на цифровой сбор данных без участия человека.</p>
                <ul style="font-size: 0.85em; color: #1f2937; padding-left: 15px;">
                    <li><b>126 автоматических станций</b> (Real-time)</li>
                    <li>Датчики видимости и облачности</li>
                    <li>Гололедные станки и датчики промерзания почвы</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
# 7.1 HIGHLIGHTS (Ключевые показатели метеосети)
    st.markdown("""
        <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 30px;">
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #004A99; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">🌍</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">347</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Метеостанций в сети</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #0288d1; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">📡</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">100%</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Цифровая передача</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #03a9f4; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">⏱️</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">3 часа</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Интервал синоптических сроков</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #4fc3f7; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">🛰️</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">WMO</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Глобальный обмен данными</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    
    st.markdown("<br>", unsafe_allow_html=True) 

    # --- 7.2 ИНТЕРАКТИВНАЯ КАРТА (РАЗМЕСТИТЬ ПОСЛЕ ХАЙЛАЙТОВ) ---

    # --- ИНТЕРАКТИВНАЯ КАРТА (OSM ВАРИАНТ) ---

    st.markdown("""
        <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; margin-top: 20px;">
            <h4 style="color: #0d47a1; text-align: center; margin: 0; font-family: 'Exo 2';">
                🗺️ Интерактивная сеть мониторинга (OpenStreetMap)
            </h4>
        </div>
    """, unsafe_allow_html=True)

    # 1. Используем публичную ссылку на границы областей Казахстана
    # Это надежный GeoJSON, который заменит отсутствующий .shp
    GEOJSON_URL = "https://raw.githubusercontent.com/datasets/geo-boundaries-world/master/countries/KAZ/provinces.geojson"

    # 2. Подготовка данных для регионов
    # (Названия регионов в этом GeoJSON обычно на латинице/английском)
    regions = [
        'Almaty', 'Akmola', 'Aktobe', 'Atyrau', 'West Kazakhstan', 'Zhambyl', 
        'Karagandy', 'Kostanay', 'Kyzylorda', 'Mangystau', 'South Kazakhstan', 
        'Pavlodar', 'North Kazakhstan', 'East Kazakhstan', 'Almaty City', 'Astana'
    ]

    df_osm = pd.DataFrame({
        'Region': regions,
        'МС_Колво': [28, 25, 22, 15, 19, 20, 30, 24, 18, 12, 25, 21, 23, 26, 5, 4],
        'Статус': ['Активно' for _ in regions]
    })

    # 3. Отрисовка карты Mapbox (использует OSM стиль)
    fig_osm = px.choropleth_mapbox(
        df_osm, 
        geojson=GEOJSON_URL, 
        locations='Region', 
        featureidkey="properties.name", # Ключ в этом конкретном GeoJSON
        color='МС_Колво',
        color_continuous_scale="Viridis",
        mapbox_style="open-street-map", # СТИЛЬ OPEN STREET MAP
        zoom=3.5, 
        center={"lat": 48.0196, "lon": 66.9237},
        opacity=0.5,
        hover_name='Region',
        labels={'МС_Колво': 'Кол-во МС'}
    )

    fig_osm.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        height=600,
        showlegend=False
    )

    st.plotly_chart(fig_osm, use_container_width=True)

    st.info("💡 Эта карта работает на данных OpenStreetMap. Границы областей загружены из глобального репозитория.")

    # 8. ГИДРОЛОГИЧЕСКИЙ МОНИТОРИНГ
    st.markdown("""
        <div style="text-align:center; margin: 40px 0 20px 0;">
            <h3 style="color: #003366; font-family: 'Exo 2'; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
                Гидрологичексий мониторинг
            </h3>
            <p style="color: #546e7a; font-size: 1em;">Высокотехнологичная сеть глобального сбора данных об атмосфере</p>
        </div>
    """, unsafe_allow_html=True)

    # Используем 3 колонки для основных типов мониторинга
    met_col1, met_col2, met_col3 = st.columns(3)

    with met_col1:
        st.markdown("""
            <div style="background: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #004A99; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #004A99; margin-top: 0;">📡 Традиционные наблюдения</h4>
                <p style="font-size: 0.9em; color: #455a64;">Вертикальное сканирование атмосферы для авиации и долгосрочных прогнозов.</p>
                <ul style="font-size: 0.85em; color: #1f2937; padding-left: 15px;">
                    <li><b>9 аэрологических станций</b> (выпуск радиозондов)</li>
                    <li>Метеорологические радары (ДМРЛ)</li>
                    <li>Спутниковый прием данных NOAA, EUMETSAT</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with met_col2:
        st.markdown("""
            <div style="background: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #0288d1; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #0288d1; margin-top: 0;">☀️ Специальные измерения</h4>
                <p style="font-size: 0.9em; color: #455a64;">Уникальные наблюдения за энергией солнца и испарением.</p>
                <ul style="font-size: 0.85em; color: #1f2937; padding-left: 15px;">
                    <li><b>Актинометрия:</b> прямая и рассеянная радиация</li>
                    <li><b>Озонометрия:</b> контроль озонового слоя</li>
                    <li>Теплобалансовые наблюдения на ключевых станциях</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with met_col3:
        st.markdown("""
            <div style="background: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #4fc3f7; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #03a9f4; margin-top: 0;">🤖 Автоматизация (АМС)</h4>
                <p style="font-size: 0.9em; color: #455a64;">Переход на цифровой сбор данных без участия человека.</p>
                <ul style="font-size: 0.85em; color: #1f2937; padding-left: 15px;">
                    <li><b>126 автоматических станций</b> (Real-time)</li>
                    <li>Датчики видимости и облачности</li>
                    <li>Гололедные станки и датчики промерзания почвы</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
# 7.1 HIGHLIGHTS (Ключевые показатели метеосети)
    st.markdown("""
        <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 30px;">
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #004A99; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">🌍</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">347</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Метеостанций в сети</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #0288d1; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">📡</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">100%</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Цифровая передача</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #03a9f4; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">⏱️</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">3 часа</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Интервал синоптических сроков</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #4fc3f7; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">🛰️</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">WMO</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Глобальный обмен данными</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True) 
    
        # 9. АГРОМЕТЕОРОЛОГИЧЕСКИЙ МОНИТОРИНГ
    st.markdown("""
        <div style="text-align:center; margin: 40px 0 20px 0;">
            <h3 style="color: #003366; font-family: 'Exo 2'; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
                Агрометеорологический мониторинг
            </h3>
            <p style="color: #546e7a; font-size: 1em;">Высокотехнологичная сеть глобального сбора данных об атмосфере</p>
        </div>
    """, unsafe_allow_html=True)

    # Используем 3 колонки для основных типов мониторинга
    met_col1, met_col2, met_col3 = st.columns(3)

    with met_col1:
        st.markdown("""
            <div style="background: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #004A99; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #004A99; margin-top: 0;">📡 Традиционные наблюдения</h4>
                <p style="font-size: 0.9em; color: #455a64;">Вертикальное сканирование атмосферы для авиации и долгосрочных прогнозов.</p>
                <ul style="font-size: 0.85em; color: #1f2937; padding-left: 15px;">
                    <li><b>9 аэрологических станций</b> (выпуск радиозондов)</li>
                    <li>Метеорологические радары (ДМРЛ)</li>
                    <li>Спутниковый прием данных NOAA, EUMETSAT</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with met_col2:
        st.markdown("""
            <div style="background: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #0288d1; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #0288d1; margin-top: 0;">☀️ Специальные измерения</h4>
                <p style="font-size: 0.9em; color: #455a64;">Уникальные наблюдения за энергией солнца и испарением.</p>
                <ul style="font-size: 0.85em; color: #1f2937; padding-left: 15px;">
                    <li><b>Актинометрия:</b> прямая и рассеянная радиация</li>
                    <li><b>Озонометрия:</b> контроль озонового слоя</li>
                    <li>Теплобалансовые наблюдения на ключевых станциях</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with met_col3:
        st.markdown("""
            <div style="background: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #4fc3f7; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #03a9f4; margin-top: 0;">🤖 Автоматизация (АМС)</h4>
                <p style="font-size: 0.9em; color: #455a64;">Переход на цифровой сбор данных без участия человека.</p>
                <ul style="font-size: 0.85em; color: #1f2937; padding-left: 15px;">
                    <li><b>126 автоматических станций</b> (Real-time)</li>
                    <li>Датчики видимости и облачности</li>
                    <li>Гололедные станки и датчики промерзания почвы</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
# 7.1 HIGHLIGHTS (Ключевые показатели метеосети)
    st.markdown("""
        <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 30px;">
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #004A99; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">🌍</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">347</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Метеостанций в сети</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #0288d1; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">📡</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">100%</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Цифровая передача</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #03a9f4; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">⏱️</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">3 часа</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Интервал синоптических сроков</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #4fc3f7; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">🛰️</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">WMO</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Глобальный обмен данными</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    
    st.markdown("<br>", unsafe_allow_html=True) 

        # 10. ЭКОЛОГИЧЕСКИЙ МОНИТОРИНГ
    st.markdown("""
        <div style="text-align:center; margin: 40px 0 20px 0;">
            <h3 style="color: #003366; font-family: 'Exo 2'; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
                Экологический мониторинг
            </h3>
            <p style="color: #546e7a; font-size: 1em;">Высокотехнологичная сеть глобального сбора данных об атмосфере</p>
        </div>
    """, unsafe_allow_html=True)

    # Используем 3 колонки для основных типов мониторинга
    met_col1, met_col2, met_col3 = st.columns(3)

    with met_col1:
        st.markdown("""
            <div style="background: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #004A99; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #004A99; margin-top: 0;">📡 Традиционные наблюдения</h4>
                <p style="font-size: 0.9em; color: #455a64;">Вертикальное сканирование атмосферы для авиации и долгосрочных прогнозов.</p>
                <ul style="font-size: 0.85em; color: #1f2937; padding-left: 15px;">
                    <li><b>9 аэрологических станций</b> (выпуск радиозондов)</li>
                    <li>Метеорологические радары (ДМРЛ)</li>
                    <li>Спутниковый прием данных NOAA, EUMETSAT</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with met_col2:
        st.markdown("""
            <div style="background: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #0288d1; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #0288d1; margin-top: 0;">☀️ Специальные измерения</h4>
                <p style="font-size: 0.9em; color: #455a64;">Уникальные наблюдения за энергией солнца и испарением.</p>
                <ul style="font-size: 0.85em; color: #1f2937; padding-left: 15px;">
                    <li><b>Актинометрия:</b> прямая и рассеянная радиация</li>
                    <li><b>Озонометрия:</b> контроль озонового слоя</li>
                    <li>Теплобалансовые наблюдения на ключевых станциях</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with met_col3:
        st.markdown("""
            <div style="background: #ffffff; padding: 20px; border-radius: 15px; border-top: 4px solid #4fc3f7; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #03a9f4; margin-top: 0;">🤖 Автоматизация (АМС)</h4>
                <p style="font-size: 0.9em; color: #455a64;">Переход на цифровой сбор данных без участия человека.</p>
                <ul style="font-size: 0.85em; color: #1f2937; padding-left: 15px;">
                    <li><b>126 автоматических станций</b> (Real-time)</li>
                    <li>Датчики видимости и облачности</li>
                    <li>Гололедные станки и датчики промерзания почвы</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
# 7.1 HIGHLIGHTS (Ключевые показатели метеосети)
    st.markdown("""
        <div style="display: flex; justify-content: space-between; gap: 15px; margin-bottom: 30px;">
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #004A99; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">🌍</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">347</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Метеостанций в сети</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #0288d1; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">📡</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">100%</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Цифровая передача</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #03a9f4; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">⏱️</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">3 часа</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Интервал синоптических сроков</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: #f8f9fa; border-left: 5px solid #4fc3f7; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5em;">🛰️</span>
                    <div>
                        <div style="font-size: 1.2em; font-weight: 800; color: #003366;">WMO</div>
                        <div style="font-size: 0.75em; color: #546e7a; text-transform: uppercase; letter-spacing: 0.5px;">Глобальный обмен данными</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    
    st.markdown("<br>", unsafe_allow_html=True) 


    # 7. РЕГЛАМЕНТЫ (TABS)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Научно-методологическая база")
    
    rt1, rt2, rt3 = st.tabs(["💧 Водный мониторинг", "🌬️ Воздушный бассейн", "🛰️ Технологии"])
    
    with rt1:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("""
                **Гидрологическая безопасность:**
                * Ежедневный замер уровня в 08:00 и 20:00.
                * Оповещение о штормовых нагонах на Каспии.
                * Прогнозы весеннего половодья.
            """)
        with c2:
            st.info("🌊 Каспийское море контролируется 50 точками наблюдения, включая автоматические морские станции.")

    with rt2:
        st.markdown("""
            **Экологический щит:**
            * Мониторинг 30 основных загрязнителей (PM2.5, NO2, SO2).
            * Прогнозы НМУ (неблагоприятных метеоусловий) для городов.
            * Интерактивная карта качества воздуха в приложении *AirKZ*.
        """)
        chart_data = pd.DataFrame(np.random.randn(20, 1), columns=['AQI Index'])
        st.line_chart(chart_data, height=120)

    with rt3:
        st.success("🚀 Казгидромет использует прогностическую модель **WRF (Weather Research and Forecasting)** для сверхкраткосрочных и среднесрочных прогнозов с детализацией до 4 км.")

    # FOOTER
    st.markdown("""
        <div style="background: #003366; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-top: 30px;">
            <p style="margin:0;">👉 Перейдите во вкладку <b>«Каспийское море»</b> для детального анализа морской среды</p>
        </div>
    """, unsafe_allow_html=True)
    
    
with tabs[1]:
    st.title("Прогноз погоды")

with tabs[2]:
    st.title("Агрометеорологические прогнозы")

with tabs[3]:
    st.title("Гидрологические прогнозы")

with tabs[4]:
    st.title("Водные ресурсы")

with tabs[6]:
    st.title("Климат Казахстана и городов")



with tabs[7]:
    st.title("Экология городов")


   
st.markdown('<div style="text-align: center; margin-top: 40px; color: #94A3B8;">РГП «Казгидромет» | 2026</div>', unsafe_allow_html=True)