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

# --- ЦЕНТРИРОВАННАЯ ТЕХНОЛОГИЧНАЯ ШАПКА ---
st.markdown(f"""
    <div class="header-wrapper">
        <div class="header-main">
            <div class="glow-line"></div>
            <h1 class="brand-title">KAZHYDROMET</h1>
            <div class="glow-line"></div>
        </div>
        <div class="header-sub">
            <div class="sub-item">NATIONAL HYDROMETEOROLOGICAL SERVICE OF KAZAKHSTAN</div>
            <div class="sub-divider"></div>
            <div class="sub-item">НАЦИОНАЛЬНАЯ ГИДРОМЕТЕОРОЛОГИЧЕСКАЯ СЛУЖБА КАЗАХСТАНА</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Стили вынесены отдельно для надежности отображения
st.markdown(f"""
    <style>
    .header-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 0;
        background-color: #FFFFFF;
        border-radius: 20px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.03);
        border: 1px solid #E2E8F0;
        margin-bottom: 30px;
        width: 100%;
    }}
    
    .header-main {{
        display: flex;
        align-items: center;
        gap: 30px;
        margin-bottom: 15px;
    }}
    
    .glow-line {{
        width: 40px;
        height: 4px;
        background-color: {ACCENT_BLUE};
        border-radius: 10px;
        box-shadow: 0 0 15px {ACCENT_BLUE};
        animation: blink 3s infinite ease-in-out;
    }}
    
    .brand-title {{
        color: {DARK_BLUE} !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 900 !important;
        letter-spacing: 15px !important;
        margin: 0 !important;
        font-size: 3.5rem !important;
        text-transform: uppercase !important;
        line-height: 1 !important;
    }}
    
    .header-sub {{
        display: flex;
        align-items: center;
        gap: 20px;
        color: #64748B;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 3px;
        text-transform: uppercase;
    }}
    
    .sub-divider {{
        width: 1px;
        height: 15px;
        background-color: #CBD5E1;
    }}
    
    @keyframes blink {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.3; }}
        100% {{ opacity: 1; }}
    }}
    
    /* Убираем стандартные отступы Streamlit для чистоты */
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    </style>
""", unsafe_allow_html=True)

# CSS для анимации выносим отдельно, чтобы не ломать f-строку
st.markdown("""
    <style>
    @keyframes pulse_line {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    /* Добавляем анимацию к линии через селектор, если нужно, 
       но пока оставим статично для надежности отображения */
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
    st.markdown('<p class="promo-subtitle">Национальная гидрометеорологическая служба Казахстана с 1922 года</p>', unsafe_allow_html=True)

    # 3. ГЛАВНЫЙ ИНФО-БАННЕР
    st.markdown("""
        <div class="kaz-banner">
            <h3 style="color: #004a99; margin-top:0;">🌍 Глобальный мониторинг — Национальная безопасность</h3>
            <p style="font-size: 1.1em; color: #334e68; max-width: 85%;">
                «Казгидромет» — фундамент гидрометеорологической и экологической стабильности Казахстана. 
                Опираясь на вековой опыт и данные государственной наблюдательной сети, мы создаем высокоточные аналитические продукты для стратегических отраслей экономики</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 4. МЕТРИКИ МАСШТАБА
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("История и опыт", "100+ лет наблюдений", "мониторинг 24/7")
    m2.metric("География", "17 филиалов", "100% охват страны")
    m3.metric("Команда", "3160", "сотрудников в штате")
    m4.metric("Мировой стандарт", "ВМО (WMO)", "с 1993 года")

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. КАРТОЧКИ НАПРАВЛЕНИЙ
    col1, col2, col3, col4 = st.columns(4)
    
    sections = [
        {
            "title": "🌡️ Метеорология",
            "total": "351 Станция",
            "desc": "",
            "items": ["225 Традиционных", "126 Автоматических", "9 Аэрологических", "5 ДМРЛ"]
        },
        {
            "title": "💧 Гидрология",
            "total": "442 Поста",
            "desc": "",
            "items": ["394 Речных поста", "38 Озерных", "10 Морских станций"]
        },
        {
            "title": "🌾 Агрометеорология",
            "total": "226 Пунктов",
            "desc": "",
            "items": ["129 На станциях", "97 Постов", "50 Автоматических"]
        },
        {
            "title": "🌱 Экология",
            "total": "175 Постов",
            "desc": "",
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
                    <p style="font-weight:700; color:#004A99;"> {sec['total']}</p>
                    <ul style="list-style:none; padding-left:0; font-size:0.95em;">
                        {items_list}
                    </ul>
                </div>
            """, unsafe_allow_html=True)

# 6. ИНТЕРАКТИВНЫЕ ПАРАМЕТРЫ МОНИТОРИНГА
    st.markdown(f"""
        <div style="text-align:center; margin: 30px 0 15px 0;">
            <h2 style="color: {DARK_BLUE}; font-family: 'Montserrat'; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;">
                Наблюдаемые параметры
            </h2>
            <p style="color: #546e7a; font-size: 1.1em;">Выберите параметр для детального обзора</p>
        </div>
    """, unsafe_allow_html=True)

    # Словарь контента (без изменений, дополнен всеми ключами)
    params_content = {
        "Темп.": {"video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "desc": "Измерение температуры воздуха в психометрической будке."},
        "Осадки": {"desc": "Использование осадкомера Третьякова и датчиков интенсивности."},
        "Ветер": {"desc": "Определение скорости и направления ветра анеморумбометрами."},
        "Давление": {"desc": "Мониторинг давления прецизионными цифровыми барометрами."},
        "Снег": {"desc": "Снегомерные съемки: определение высоты и плотности покрова."},
        "Облачность": {"desc": "Определение формы, высоты и количества облаков."},
        "Солнечная радиация": {"desc": "Актинометрические наблюдения за солнечной энергией."},
        "Опасные и стихийные явления": {"desc": "Круглосуточный мониторинг шквалов, града и метелей."},
        "Уровень": {"desc": "Автоматизированный мониторинг уровня воды."},
        "Расход": {"desc": "Измерение расхода воды с помощью вертушек и ADCP-профилографов."},
        "Т. воды": {"desc": "Контактное измерение температуры поверхности водоемов."},
        "Воздух": {"desc": "Экологический мониторинг: анализ ПДК загрязняющих веществ."},
        "Гамма": {"desc": "Контроль радиационного фона (мощность гамма-излучения)."}
    }

    params = [
        {"icon": "🌡️", "label": "Темп."}, {"icon": "🌧️", "label": "Осадки"},    
        {"icon": "🌬️", "label": "Ветер"}, {"icon": "⏲️", "label": "Давление"},
        {"icon": "❄️", "label": "Снег"}, {"icon": "☁️", "label": "Облачность"},
        {"icon": "☀️", "label": "Солнечная радиация"}, {"icon": "⚠️", "label": "Опасные и стихийные явления"},
        {"icon": "🌊", "label": "Уровень"}, {"icon": "📉", "label": "Расход"},   
        {"icon": "💧", "label": "Т. воды"}, {"icon": "🧪", "label": "Воздух"},
        {"icon": "☢️", "label": "Гамма"}
    ]

    if "selected_param" not in st.session_state:
        st.session_state.selected_param = None

    # Отрисовка кнопок
    row1 = st.columns(7)
    row2 = st.columns(6)
    
    for i, p in enumerate(params):
        target_col = row1[i] if i < 7 else row2[i-7]
        with target_col:
            # Если параметр уже выбран, подсвечиваем его (опционально через стили, тут упрощенно)
            if st.button(f"{p['icon']}\n{p['label']}", key=f"btn_{p['label']}", use_container_width=True):
                # Если нажали на уже выбранный — закрываем, иначе открываем новый
                if st.session_state.selected_param == p['label']:
                    st.session_state.selected_param = None
                else:
                    st.session_state.selected_param = p['label']
                st.rerun()

    # --- БЛОК ОТОБРАЖЕНИЯ КОНТЕНТА (БЕЗ КНОПКИ ЗАКРЫТЬ) ---
    if st.session_state.selected_param:
        param_key = st.session_state.selected_param
        content = params_content.get(param_key, {"desc": "Информация загружается..."})
        
        # Контейнер с контентом
        st.markdown(f"""
            <div style="background-color: white; padding: 30px; border-radius: 20px; border-top: 4px solid {ACCENT_BLUE}; box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-top: 25px; position: relative;">
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns([1.8, 1])
        
        with c1:
            st.markdown(f"<h3 style='color: {DARK_BLUE}; margin-top: 0;'>🔍 {param_key}</h3>", unsafe_allow_html=True)
            if "video" in content:
                st.video(content["video"])
            else:
                st.info("🎥 Видеоматериалы процесса мониторинга готовятся к публикации.")
                
        with c2:
            st.markdown(f"<h4 style='color: {ACCENT_BLUE};'>Методология</h4>", unsafe_allow_html=True)
            st.write(content["desc"])
            st.caption("Нажмите на иконку параметра еще раз, чтобы скрыть эту панель.")
        
        st.markdown("</div>", unsafe_allow_html=True)         

        # 7. МЕТЕОРОЛОГИЧЕСКИЙ МОНИТОРИНГ
        st.markdown("""
            <div style="text-align:center; margin: 40px 0 20px 0;">
                <h3 style="color: #003366; font-family: 'Exo 2'; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
                    Метеорологический мониторинг
                </h3>
                <p style="color: #546e7a; font-size: 1em;">Единая национальная сеть комплексного мониторинга приземных и высоких слоев атмосферы, интегрированная в глобальную систему обмена данными ВМО</p>
            </div>
        """, unsafe_allow_html=True)

    # 7.1 HIGHLIGHTS (Ключевые показатели метеосети)
        st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; margin-bottom: 30px;">
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #003366; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">🏢</span>
                        <div>
                            <div style="font-size: 1.3em; font-weight: 800; color: #003366; line-height: 1.1;">351</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Метеостанций в сети</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #004A99; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">📲</span>
                        <div>
                            <div style="font-size: 1.3em; font-weight: 800; color: #003366; line-height: 1.1;">100%</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">автоматизированная передача данных</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #0288d1; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">⏱️</span>
                        <div>
                            <div style="font-size: 1.3em; font-weight: 800; color: #003366; line-height: 1.1;">3 часа</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Срок наблюдений</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #03a9f4; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">🌐</span>
                        <div>
                            <div style="font-size: 1.3em; font-weight: 800; color: #003366; line-height: 1.1;">WMO</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Глобальный обмен</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #26c6da; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">🏛️</span>
                        <div>
                            <div style="font-size: 1.3em; font-weight: 800; color: #003366; line-height: 1.1;">19</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Вековых станций</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 180px; background: #ffffff; border-left: 5px solid #4fc3f7; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">📧</span>
                        <div>
                            <div style="font-size: 1.1em; font-weight: 800; color: #003366; line-height: 1.1;">658 800</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Телеграмм/год (МС)</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 180px; background: #ffffff; border-left: 5px solid #81d4fa; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">📡</span>
                        <div>
                            <div style="font-size: 1.1em; font-weight: 800; color: #003366; line-height: 1.1;">1 106 784</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Телеграмм/год (АМС)</div>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        
        st.markdown("<br>", unsafe_allow_html=True) 
        import streamlit as st
        from PIL import Image

        # 1. Словарь с путями к фото
        IMAGE_PATHS = {
            "Метеонаблюдения": r"C:\Users\eltai_a\Desktop\RES\stend\МС.jpeg",
            "Аэрология": r"C:\Users\eltai_a\Desktop\RES\stend\Aerology.jpeg",
            "ДМРЛ": r"C:\Users\eltai_a\Desktop\RES\stend\DMRL.jpeg",
            "Кадастр": r"C:\Users\eltai_a\Desktop\RES\stend\Cadastre.jpeg"
        }

        @st.dialog("Просмотр оборудования", width="large")
        def show_modal(title, img_path):
            try:
                img = Image.open(img_path)
                st.subheader(title)
                st.image(img, use_container_width=True)
            except Exception as e:
                st.error(f"Не удалось загрузить изображение: {e}")

        # 2. Улучшенный CSS с Font Awesome
        st.markdown("""
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            
            <style>
            .hover-card {
                background: #ffffff; 
                padding: 24px; 
                border-radius: 20px; 
                border-top: 5px solid #004A99; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
                height: 500px;
                transition: all 0.3s ease;
                position: relative;
                display: flex;
                flex-direction: column;
            }
            
            .hover-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 15px 30px rgba(0, 74, 153, 0.15);
                border-top: 5px solid #00d2ff;
            }

            /* Дизайн кнопки-иконки */
            div.stButton > button[key*="icon_btn"] {
                border-radius: 12px !important; /* Делаем скругленным квадратом для стиля "Soft UI" */
                width: 45px !important;
                height: 45px !important;
                padding: 0 !important;
                border: none !important;
                background-color: #f0f4f8 !important; /* Светло-голубой фон */
                color: #5d707f !important; /* Серый цвет иконки по умолчанию */
                position: absolute !important;
                top: 20px !important;
                right: 20px !important;
                z-index: 100 !important;
                transition: all 0.3s ease !important;
            }
            
            div.stButton > button[key*="icon_btn"]:hover {
                background-color: #004A99 !important; /* Синий фон при наведении */
                color: #ffffff !important; /* Белая иконка при наведении */
                box-shadow: 0 4px 10px rgba(0, 74, 153, 0.3) !important;
                transform: scale(1.1) rotate(5deg) !important;
            }

            /* Стили для текста внутри кнопки (иконки Font Awesome) */
            div.stButton > button[key*="icon_btn"] p {
                font-size: 1.2em !important;
                font-weight: normal !important;
            }
            </style>
        """, unsafe_allow_html=True)

        met_col1, met_col2, met_col3, met_col4 = st.columns(4)

        # Функция для отрисовки блока (чтобы не дублировать код)
        def draw_block(col, btn_key, title, icon_html, description, list_items, img_key):
            with col:
                # Используем HTML иконку внутри кнопки Streamlit
                if st.button(icon_html, key=btn_key, help=f"Открыть фото: {title}"):
                    show_modal(title, IMAGE_PATHS[img_key])
                
                st.markdown(f"""
                    <div class="hover-card">
                        <h4 style="color: #004A99; margin-top: 5px; padding-right: 45px;">{title}</h4>
                        <p style="font-size: 0.9em; color: #455a64;">{description}</p>
                        <div style="margin-top: 10px; font-weight: bold; color: #004A99;"></div>
                        <ul style="padding-left: 20px; margin-top: 8px; font-size: 0.85em; color: #333; line-height: 1.6;">
                            {"".join([f"<li>{item}</li>" for item in list_items])}
                        </ul>
                    </div>
                """, unsafe_allow_html=True)

        # Отрисовываем 4 блока

        # 1. Метеорологические наблюдения
        draw_block(
            met_col1, 
            "icon_btn_1", 
            "🌡️ Метеорологические наблюдения", 
            "📷", 
            "Системный сбор данных о приземном состоянии атмосферы в единые синхронные сроки (8 раз в сутки).", 
            [
                "<b>Атмосфера:</b> температура, влажность и давление.", 
                "<b>Ветер:</b> скорость, направление и порывы.", 
                "<b>Осадки:</b> интенсивность, тип и снежный покров.",
                "<b>Облачность:</b> количество, форма и высота ВНГО.",
                "<b>Почва:</b> температура на поверхности и глубинах.",
                "<b>Явления:</b> мониторинг ОЯ, СГЯ и гололеда."
            ], 
            "Метеонаблюдения"
        )

        # 2. Аэрология
        draw_block(
            met_col2, 
            "icon_btn_2", 
            "🎈 Аэрология", 
            "📸", 
            "Высотное зондирование атмосферы на 9 станциях РК для глобального прогнозирования.", 
            [
                "<b>Вертикаль:</b> мониторинг состояния до 30 км и выше.", 
                "<b>Зонды:</b> выпуск радиозондов 2 раза в сутки.", 
                "<b>Модели:</b> данные для циклонов и антициклонов.",
                "<b>Безопасность:</b> прогноз ОЯ на разных эшелонах."
            ], 
            "Аэрология"
        )

        # 3. ДМРЛ (Доплеровские метеорологические радиолокаторы)
        draw_block(
            met_col3, 
            "icon_btn_3", 
            "📡 ДМРЛ", 
            "🖼️", 
            "Дистанционное сканирование атмосферы в режиме real-time в радиусе до 250 км.", 
            [
                "<b>Осадки:</b> тип (град/дождь), интенсивность и трек.", 
                "<b>Структура:</b> зоны зарождения гроз и шквалов.", 
                "<b>Доплер:</b> скорость движения воздушных масс.",
                "<b>Оперативность:</b> ежеминутное обновление данных."
            ], 
            "ДМРЛ"
        )

        # 4. Кадастр
        draw_block(
            met_col4, 
            "icon_btn_4", 
            "📖 Кадастр", 
            "📁", 
            "Единая государственная система климатических данных и архивов Казахстана.", 
            [
                "<b>Тренды:</b> долгосрочные изменения климата РК.", 
                "<b>Аномалии:</b> фиксация исторических рекордов.", 
                "<b>Статистика:</b> повторяемость опасных явлений.",
                "<b>Фонд:</b> хранение вековых рядов наблюдений."
            ], 
            "Кадастр"
        )

                   
        # Добавляем отступ и заголовок секции
        st.write("") # Пустая строка
        st.markdown("---") # Горизонтальная линия
        st.subheader("📍 География мониторинга и статистика по регионам")
        st.write("") # Еще немного места

     

    import streamlit as st
    import geopandas as gpd
    import folium
    from streamlit_folium import st_folium
    import os

    # --- ПУТЬ К ФАЙЛУ ---
    SHP_PATH = r"C:\Users\eltai_a\Desktop\RES\stend\kaz 17 obl.shp"

    # 1. СЛОВАРЬ С ДАННЫМИ (Добавлены экстремумы с карты)
    # t_min, t_max, wind, press, rain — порядковые номера с вашей легенды
    kaz_stats = {
        "almaty": {"ru": "г. Алматы", "ms": 19, "ams": 16, "t_min": -38, "t_max": 43, "wind": 3.45, "press": 1012, "rain": 5.82},
        "akmola": {"ru": "Акмолинская область", "ms": 15, "ams": 15, "t_min": -52, "t_max": 42, "wind": 3.48, "press": 1038, "rain": 5.129},
        "aktobe": {"ru": "Актюбинская область", "ms": 17, "ams": 9, "t_min": -47, "t_max": 47, "wind": 3.48, "press": 1048, "rain": 5.74},
        "atyrau": {"ru": "Атырауская область", "ms": 9, "ams": 2, "t_min": -42, "t_max": 46, "wind": 3.34, "press": 1058, "rain": 5.90},
        "east kazakhstan": {"ru": "ВКО и Абай", "ms": 30, "ams": 14, "t_min": -50, "t_max": 45, "wind": 3.45, "press": 1050, "rain": 5.81},
        "zhambyl": {"ru": "Жамбылская область", "ms": 13, "ams": 8, "t_min": -50, "t_max": 48, "wind": 3.49, "press": 1022, "rain": 5.82},
        "west kazakhstan": {"ru": "Западно-Казахстанская область", "ms": 13, "ams": 5, "t_min": -44, "t_max": 45, "wind": 3.34, "press": 1058, "rain": 5.109},
        "karaganda": {"ru": "Карагандинская и Улытау", "ms": 23, "ams": 10, "t_min": -50, "t_max": 45, "wind": 3.40, "press": 1019, "rain": 5.144},
        "kostanay": {"ru": "Костанайская область", "ms": 18, "ams": 2, "t_min": -47, "t_max": 45, "wind": 3.40, "press": 1052, "rain": 5.154},
        "kyzylorda": {"ru": "Кызылординская область", "ms": 9, "ams": 6, "t_min": -40, "t_max": 48, "wind": 3.62, "press": 1047, "rain": 5.111},
        "mangystau": {"ru": "Мангистауская область", "ms": 7, "ams": 10, "t_min": -38, "t_max": 47, "wind": 3.45, "press": 1053, "rain": 5.94},
        "pavlodar": {"ru": "Павлодарская область", "ms": 15, "ams": 4, "t_min": -49, "t_max": 42, "wind": 3.50, "press": 1056, "rain": 5.106},
        "north kazakhstan": {"ru": "Северо-Казахстанская область", "ms": 11, "ams": 5, "t_min": -48, "t_max": 41, "wind": 3.40, "press": 1055, "rain": 5.117},
        "turkistan": {"ru": "Туркестанская область", "ms": 14, "ams": 6, "t_min": -43, "t_max": 51, "wind": 3.52, "press": 1047, "rain": 5.110},
        "astana": {"ru": "г. Астана", "ms": 5, "ams": 5, "t_min": -52, "t_max": 42, "wind": 3.48, "press": 1038, "rain": 5.129},
        "shymkent": {"ru": "г. Шымкент", "ms": 8, "ams": 4, "t_min": -43, "t_max": 51, "wind": 3.52, "press": 1047, "rain": 5.110},
        "almaty oblast": {"ru": "Алматинская и Жетісу", "ms": 12, "ams": 7, "t_min": -44, "t_max": 44, "wind": 3.70, "press": 1012, "rain": 5.82},
    }

    # Функция загрузки
    @st.cache_data
    def load_data(path):
        if not os.path.exists(path): return None
        try:
            gdf = gpd.read_file(path)
            if 'ADMO_EN' in gdf.columns: gdf = gdf[gdf['ADMO_EN'] != 'KAZ']
            name_col = 'ADM1_EN' if 'ADM1_EN' in gdf.columns else gdf.select_dtypes(include=['object']).columns[0]
            
            def get_ru_name(en_name):
                name = str(en_name).strip().lower()
                if name in kaz_stats: return kaz_stats[name]['ru']
                for key, val in kaz_stats.items():
                    if key in name or name in key: return val['ru']
                return en_name

            gdf['RUS_NAME'] = gdf[name_col].apply(get_ru_name)
            return gdf.to_crs(epsg=4326), name_col
        except Exception as e:
            st.error(f"Ошибка загрузки: {e}")
            return None

    # --- ГЛАВНАЯ ЛОГИКА ---
    result = load_data(SHP_PATH)

    if result:
        gdf, name_col = result
        
        # Создаем колонки для интерфейса
        col_map, col_info = st.columns([2, 1])

    with col_map:
        # Обновленный CSS: добавляем text-transform: uppercase для подстраховки
        st.markdown("""
            <style>
                path.leaflet-interactive:focus { outline: none !important; }
                .leaflet-container:focus { outline: none !important; }
                .region-label {
                    font-size: 9pt;
                    font-weight: 800;
                    color: #004A99;
                    text-align: center;
                    text-transform: uppercase; /* Все буквы заглавные */
                    white-space: normal;
                    width: 100px;
                    text-shadow: 0 0 3px white, 0 0 3px white;
                    pointer-events: none;
                }
            </style>
        """, unsafe_allow_html=True)

      

        # Состояния (центр, зум, выбор)
        if 'map_center' not in st.session_state:
            st.session_state.map_center = [48.0, 67.0]
        if 'map_zoom' not in st.session_state:
            st.session_state.map_zoom = 5
        if 'selected_region_id' not in st.session_state:
            st.session_state.selected_region_id = None

        m = folium.Map(
            location=st.session_state.map_center, 
            zoom_start=st.session_state.map_zoom, 
            tiles="cartodbpositron"
        )

        # 2. Основной слой областей
        style_fn = lambda x: {
            'fillColor': '#e3f2fd', 'color': '#004A99', 'weight': 1, 'fillOpacity': 0.4
        }
        
        folium.GeoJson(
            gdf,
            name="Regions",
            style_function=style_fn,
            tooltip=folium.GeoJsonTooltip(fields=['RUS_NAME'], aliases=['Область:'])
        ).add_to(m)


        

        # 4. Слой выделения (если область выбрана)
        if st.session_state.selected_region_id is not None:
            selected_gdf = gdf[gdf[name_col] == st.session_state.selected_region_id]
            folium.GeoJson(
                selected_gdf,
                style_function=lambda x: {
                    'fillColor': '#E67E22', 'color': '#D35400', 'weight': 3, 'fillOpacity': 0.7
                }
            ).add_to(m)

        # Отрисовка
        map_output = st_folium(m, width=700, height=500, key="kaz_map_with_labels")

        # 5. Обработка клика и зума
        if map_output and map_output.get("last_active_drawing"):
            props = map_output["last_active_drawing"]["properties"]
            region_id = props.get(name_col)
            
            if st.session_state.selected_region_id != region_id:
                geometry = map_output["last_active_drawing"]["geometry"]
                # Упрощенное получение центра для зума
                if geometry['type'] in ['Polygon', 'MultiPolygon']:
                    # Берем координаты из свойств объекта streamlit-folium
                    # (или можно вычислить через центроид gdf по ID)
                    target_row = gdf[gdf[name_col] == region_id].iloc[0]
                    center = target_row.geometry.centroid
                    
                    st.session_state.map_center = [center.y, center.x]
                    st.session_state.map_zoom = 6
                    st.session_state.selected_region_id = region_id
                    st.rerun()
                                
        
    with col_info:
            # Общая статистика (всегда отображается)
        total_ms = sum(v['ms'] for v in kaz_stats.values())
        total_ams = sum(v['ams'] for v in kaz_stats.values())
            
        st.markdown(f"""
                <div style="background: #f8f9fa; padding: 15px; border-radius: 12px; border: 1px solid #dee2e6; margin-bottom: 20px;">
                    <h4 style="margin:0; color: #343a40;">Всего по сети РГП:</h4>
                    <p style="margin:5px 0; font-size: 1.1em;">🏢 МС: <b>{total_ms}</b> | 📡 АМС: <b>{total_ams}</b></p>
                </div>
            """, unsafe_allow_html=True)

            # Обработка клика
# --- ВНУТРИ БЛОКА ОБРАБОТКИ КЛИКА ---
        if map_output and map_output.get("last_active_drawing"):
            props = map_output["last_active_drawing"]["properties"]
            raw_name = props.get(name_col)
            # Переводим в нижний регистр для поиска по словарю kaz_stats
            search_name = str(raw_name).strip().lower()
            
            # Поиск данных (ищем совпадение ключа в нижнем регистре)
            found_data = next((val for key, val in kaz_stats.items() if key == search_name or key in search_name or search_name in key), None)

            if found_data:
                # Название области выводим ЗАГЛАВНЫМИ
                st.markdown(f"<h3 style='color: #004A99; margin-bottom: 15px;'>{found_data['ru'].upper()}</h3>", unsafe_allow_html=True)
                
                sub_col1, sub_col2 = st.columns(2)
                with sub_col1:
                    st.markdown(f"""
                        <div style="padding: 12px; border-radius: 10px; border-top: 4px solid #004A99; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.08); height: 160px;">
                            <p style="color: #004A99; font-weight: bold; margin-bottom: 8px; font-size: 0.8em;">СЕТЬ СТАНЦИЙ</p>
                            <p style="margin: 3px 0; font-size: 0.85em;">🏢 МС: <b>{found_data['ms']}</b></p>
                            <p style="margin: 3px 0; font-size: 0.85em;">📡 АМС: <b>{found_data['ams']}</b></p>
                        </div>
                    """, unsafe_allow_html=True)

                with sub_col2:
                    st.markdown(f"""
                        <div style="padding: 12px; border-radius: 10px; border-top: 4px solid #E67E22; background: #fffaf5; box-shadow: 0 2px 8px rgba(0,0,0,0.08); height: 160px;">
                            <p style="color: #E67E22; font-weight: bold; margin-bottom: 8px; font-size: 0.8em;">ЭКСТРЕМУМЫ</p>
                            <div style="font-size: 0.8em; line-height: 1.3;">
                                ❄️ Т.МИН: <b>{found_data['t_min']}°</b><br>
                                🔥 Т.МАКС: <b>{found_data['t_max']}°</b><br>
                                💨 ВЕТЕР: <b>{found_data['wind']} м/с</b><br>
                                🌡️ ДАВЛ: <b>{found_data['press']} гПа</b>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                # Если не нашли, выводим ошибку с тем именем, которое пришло из карты
                st.warning(f"Данные для '{raw_name}' не найдены в базе.")
        else:
            # Если ничего не выбрано — показываем заглушку (этот блок всегда отображен)
            st.info("👈 ВЫБЕРИТЕ ОБЛАСТЬ НА КАРТЕ")


    
# --- БЛОК МЕТЕО-РЕКОРДОВ ---
    st.markdown("""
            <style>
            .record-card {
                background: linear-gradient(135deg, #ffffff 0%, #f0f4f8 100%);
                border-radius: 15px;
                padding: 15px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                border: 1px solid #e0e6ed;
                transition: transform 0.2s;
            }
            .record-card:hover {
                transform: scale(1.02);
            }
            .record-val {
                font-size: 1.8em;
                font-weight: 800;
                margin: 5px 0;
            }
            .record-city {
                font-size: 0.9em;
                color: #546e7a;
                font-weight: 600;
                text-transform: uppercase;
            }
            </style>
    """, unsafe_allow_html=True)

    st.write("### 🏆 Метео-рекорды Казахстана за сегодня")
    st.caption(f"Данные на {pd.Timestamp.now().strftime('%d.%m.%Y %H:%M')} по сети РГП 'Казгидромет'")

    rec_col1, rec_col2, rec_col3 = st.columns(3)

    with rec_col1:
        st.markdown(f"""
                <div class="record-card">
                    <div style="font-size: 2em;">❄️</div>
                    <div class="record-city">Самый холодный</div>
                    <div class="record-val" style="color: #0288d1;">-28°C</div>
                    <div style="font-size: 0.8em; color: #78909c;">ст. Атбасар</div>
                </div>
        """, unsafe_allow_html=True)

    with rec_col2:
        st.markdown(f"""
                <div class="record-card">
                    <div style="font-size: 2em;">☀️</div>
                    <div class="record-city">Самый теплый</div>
                    <div class="record-val" style="color: #f57c00;">+12°C</div>
                    <div style="font-size: 0.8em; color: #78909c;">г. Шымкент</div>
                </div>
        """, unsafe_allow_html=True)

    with rec_col3:
            st.markdown(f"""
                <div class="record-card">
                    <div style="font-size: 2em;">💨</div>
                    <div class="record-city">Сильный ветер</div>
                    <div class="record-val" style="color: #455a64;">35 м/с</div>
                    <div style="font-size: 0.8em; color: #78909c;">ст. Достык (Джунгарские ворота)</div>
                </div>
            """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.express as px
    from datetime import datetime, timedelta

        # --- ГЕНЕРАЦИЯ ДАННЫХ (для демонстрации) ---
        # В реальном проекте здесь будет загрузка вашего лога предупреждений
    def get_heatmap_data():
            end_date = datetime(2026, 2, 20) # Текущая дата по инструкции
            start_date = end_date - timedelta(days=364)
            date_range = pd.date_range(start=start_date, end=end_date)
            
            # Имитируем активность: осенью и весной (сезоны штормов) данных больше
            data = []
            for date in date_range:
                month = date.month
                if month in [3, 4, 10, 11]: # Пиковые месяцы
                    count = np.random.randint(40, 100)
                else:
                    count = np.random.randint(10, 50)
                data.append({"Дата": date, "Предупреждения": count, "День": date.strftime('%a'), "Неделя": date.isocalendar()[1]})
            
            return pd.DataFrame(data)

    df_heat = get_heatmap_data()


    
    
    
        # 7. ГИДРОЛОГИЧЕСКИЙ МОНИТОРИНГ
    st.markdown("""
            <div style="text-align:center; margin: 40px 0 20px 0;">
                <h3 style="color: #003366; font-family: 'Exo 2'; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
                    Гидрологический мониторинг
                </h3>
                <p style="color: #546e7a; font-size: 1em;">Единая государственная система наблюдений за состоянием водных объектов и ведение водного кадастра РК</p>
            </div>
        """, unsafe_allow_html=True)

        # 7.1 HIGHLIGHTS (Убедитесь, что здесь НЕТ лишнего отступа слева)
    st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; margin-bottom: 30px;">
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #003366; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">🏢</span>
                        <div>
                            <div style="font-size: 1.3em; font-weight: 800; color: #003366; line-height: 1.1;">377</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Гидропостов</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #004A99; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">📊</span>
                        <div>
                            <div style="font-size: 1.3em; font-weight: 800; color: #003366; line-height: 1.1;">8</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Бассейнов</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #0288d1; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">🏛️</span>
                        <div>
                            <div style="font-size: 1.3em; font-weight: 800; color: #003366; line-height: 1.1;">24</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Вековых поста</div>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        # --- ДОПОЛНИТЕЛЬНЫЙ АНАЛИТИЧЕСКИЙ БЛОК ---
    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
            st.write("### 🛠️ Техническое оснащение")
            equipment_data = {
                "Тип поста": ["Автоматические (передача онлайн)", "Классические (ручной замер)"],
                "Количество": [170, 207] # Цифры для примера
            }
            fig_donut = go.Figure(data=[go.Pie(labels=equipment_data["Тип поста"], 
                                             values=equipment_data["Количество"], 
                                             hole=.5,
                                             marker_colors=['#003366', '#3498db'])])
            fig_donut.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300, showlegend=False)
            st.plotly_chart(fig_donut, use_container_width=True)
            st.caption("Соотношение автоматизированных и классических гидрологических постов.")

    with col_b:
            st.write("### ⚠️ Оперативный статус (ОЯ/НЯ)")
            # Имитация оперативных данных
            st.error("❗ **Превышение уровней:** Не зафиксировано")
            st.warning("❄️ **Ледовые явления:** Забереги, ледостав на 85% рек")
            st.success("✅ **Связь с постами:** 98.2% постов в сети")
            
            if st.button("Сформировать отчет по ОЯ"):
                st.write("Отчет за последние 24 часа подготовлен...")
        
        # 1. Словарь с путями к фото
    IMAGE_PATHS = {
            "HP": r"C:\Users\eltai_a\Desktop\RES\stend\HP1.jpeg",
            "Auto": r"C:\Users\eltai_a\Desktop\RES\stend\Aerology.jpeg",
            "TDS": r"C:\Users\eltai_a\Desktop\RES\stend\DMRL.jpeg",
            "Cadastre": r"C:\Users\eltai_a\Desktop\RES\stend\Cadastre.jpeg"
    }

        # 2. Создаем колонки
    h_col1, h_col2, h_col3, h_col4 = st.columns(4)

        # 3. Отрисовываем блоки (используем h_col вместо met_col, чтобы не путать с метео)
    draw_block(h_col1, "hydro_btn_1", "🌊 Гидропосты", "📷", 
                   "Комплекс приборов для наблюдений на реках, озерах и каналах.", 
                   ["<b>Уровень:</b> замеры в 08:00 и 20:00", "<b>Температура:</b> воды (ТМ-10)", "<b>Расход:</b> вертушки ИСВП"], "HP")

    draw_block(h_col2, "hydro_btn_2", "📟 Автоматические посты", "📸", 
                   "Системы непрерывного мониторинга и передачи данных.", 
                   ["<b>ADCP:</b> River Ray/M9", "<b>Режим:</b> учащенно в паводки", "<b>Передача:</b> спутник/GSM"], "Auto")

    draw_block(h_col3, "hydro_btn_3", "🏔️ Труднодоступные посты", "🖼️", 
                   "Наблюдения в сложных географических условиях.", 
                   ["<b>Половодье:</b> мониторинг максимумов", "<b>Лед:</b> толщина и высота снега", "<b>ОЯ:</b> штормовые оповещения"], "TDS")

    draw_block(h_col4, "hydro_btn_4", "💧 Водный кадастр", "📁", 
                   "Единая система данных о водных ресурсах Казахстана.", 
                   ["<b>Ежегодники:</b> данные по 8 бассейнам", "<b>Ресурсы:</b> анализ и банк данных", "<b>Справочники:</b> многолетние данные"], "Cadastre")
        
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go

        # --- 1. ПОДГОТОВКА ДАННЫХ (Цифры для примера) ---
    data = {
            "Область": [
                "Абай", "Акмолинская", "Актюбинская", "Алматинская", "Атырауская", 
                "ЗКО", "Жамбылская", "Жетысу", "Карагандинская", "Костанайская", 
                "Кызылординская", "Мангистауская", "Павлодарская", "СКО", "Туркестанская", "Улытау", "ВКО"
            ],
            "Гидропосты": [12, 25, 18, 30, 10, 15, 22, 19, 28, 20, 14, 5, 16, 24, 21, 8, 35],
            "ТД (Техдокументация)": [45, 120, 80, 150, 40, 65, 90, 85, 130, 100, 70, 15, 75, 110, 95, 30, 160]
    }

    df_posts = pd.DataFrame(data)

        # --- 2. ИНТЕРФЕЙС STREAMLIT ---
    st.subheader("📊 Мониторинг гидрологической сети по областям")

        # Фильтр выбора областей (по умолчанию выбраны все)
    selected_regions = st.multiselect(
            "Выберите области для анализа:",
            options=df_posts["Область"].tolist(),
            default=df_posts["Область"].tolist()
    )

    filtered_df = df_posts[df_posts["Область"].isin(selected_regions)]

        # --- 3. ПОСТРОЕНИЕ ИНТЕРАКТИВНОГО ГРАФИКА ---
    fig = go.Figure()

        # Столбцы для Гидропостов
    fig.add_trace(go.Bar(
            x=filtered_df["Область"],
            y=filtered_df["Гидропосты"],
            name="Кол-во гидропостов",
            marker_color='#3498db',
            text=filtered_df["Гидропосты"],
            textposition='auto',
    ))

        # Столбцы для ТД (Техническая документация / Трудозатраты / Данные)
    fig.add_trace(go.Bar(
            x=filtered_df["Область"],
            y=filtered_df["ТД (Техдокументация)"],
            name="Количество ТД",
            marker_color='#2ecc71',
            text=filtered_df["ТД (Техдокументация)"],
            textposition='auto',
    ))

        # Настройка внешнего вида
    fig.update_layout(
            barmode='group', # Группировка столбиков рядом
            xaxis_title="Регионы",
            yaxis_title="Количество",
            legend_title="Показатели",
            hovermode="x unified",
            height=550,
            margin=dict(l=20, r=20, t=40, b=100),
            xaxis={'categoryorder':'total descending'} # Сортировка по убыванию
    )

        # Отображение графика
    st.plotly_chart(fig, use_container_width=True)

        # --- 4. ДОПОЛНИТЕЛЬНАЯ ТАБЛИЦА (СВОДКА) ---
    with st.expander("📋 Посмотреть табличные данные"):
        st.dataframe(filtered_df.sort_values(by="Гидропосты", ascending=False), use_container_width=True)
    
    import streamlit as st
    import pandas as pd

        # --- ДАННЫЕ ДЛЯ РЕТРОСПЕКТИВЫ ---
    HISTORICAL_DATA = {
            "р. Есиль (г. Астана)": {
                "record_level": 912, "record_year": 2017, "current_level": 245, "danger_level": 850,
                "fact": "В 2017 году уровень воды достиг рекордной отметки, что привело к заполнению защитной дамбы."
            },
            "р. Жайык (г. Уральск)": {
                "record_level": 942, "record_year": 1994, "current_level": 320, "danger_level": 850,
                "fact": "Исторический максимум был зафиксирован в середине 90-х. Сейчас уровень в пределах нормы."
            },
            "р. Ертис (г. Усть-Каменогорск)": {
                "record_level": 450, "record_year": 1966, "current_level": 180, "danger_level": 400,
                "fact": "Максимальный уровень регулируется Бухтарминским каскадом ГЭС."
            }
    }

    st.markdown("### 📜 Историческая память рек")
    st.write("Сравните текущее состояние реки с самым масштабным наводнением в истории наблюдений.")

        # Выбор объекта
    river_choice = st.selectbox("Выберите реку для сравнения:", list(HISTORICAL_DATA.keys()))
    data = HISTORICAL_DATA[river_choice]

        # Визуал: Две карточки
    col_hist, col_curr = st.columns(2)

    with col_hist:
        st.markdown(f"""
                <div style="background-color: #f1f3f4; padding: 20px; border-radius: 15px; border-left: 8px solid #607d8b;">
                    <h5 style="margin:0; color: #455a64;">📊 ИСТОРИЧЕСКИЙ ПИК</h5>
                    <h2 style="margin:0; color: #263238;">{data['record_level']} см</h2>
                    <p style="font-weight: bold; color: #78909c;">{data['record_year']} год</p>
                </div>
            """, unsafe_allow_html=True)

    with col_curr:
            # Динамический цвет в зависимости от уровня
            status_color = "#2ecc71" if data['current_level'] < data['danger_level'] else "#e74c3c"
            st.markdown(f"""
                <div style="background-color: #e3f2fd; padding: 20px; border-radius: 15px; border-left: 8px solid {status_color};">
                    <h5 style="margin:0; color: #1565c0;">🌊 ТЕКУЩИЙ УРОВЕНЬ</h5>
                    <h2 style="margin:0; color: #0d47a1;">{data['current_level']} см</h2>
                    <p style="font-weight: bold; color: #1e88e5;">20 февраля 2026 г.</p>
                </div>
            """, unsafe_allow_html=True)

        # Визуальная шкала (Progress Bar как линейка)
    st.write("")
    st.write("**Визуальное сравнение масштаба:**")
    diff_percent = data['current_level'] / data['record_level']
    st.progress(diff_percent, text=f"Текущий уровень составляет {int(diff_percent*100)}% от исторического максимума")

    st.info(f"💡 **Интересный факт:** {data['fact']}")

            
        
# 9. АГРОМЕТЕОРОЛОГИЧЕСКИЙ МОНИТОРИНГ
    st.markdown("""
            <div style="text-align:center; margin: 40px 0 20px 0;">
                <h3 style="color: #1b5e20; font-family: 'Exo 2'; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">
                    Агрометеорологический мониторинг
                </h3>
                <p style="color: #546e7a; font-size: 1.1em;">Комплексный контроль состояния почв и посевов для продовольственной безопасности РК</p>
            </div>
        """, unsafe_allow_html=True)

        # 9.1 HIGHLIGHTS (Обновленная агро-статистика на основе слайда)
    st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; margin-bottom: 30px;">
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #1b5e20; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">🌾</span>
                        <div>
                            <div style="font-size: 1.3em; font-weight: 800; color: #1b5e20; line-height: 1.1;">226</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Пунктов наблюдений</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #2e7d32; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">🧪</span>
                        <div>
                            <div style="font-size: 1.3em; font-weight: 800; color: #1b5e20; line-height: 1.1;">134</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Замеров влажности</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #43a047; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">✅</span>
                        <div>
                            <div style="font-size: 1.3em; font-weight: 800; color: #1b5e20; line-height: 1.1;">78%</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Оправдываемость</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #81c784; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">🤖</span>
                        <div>
                            <div style="font-size: 1.3em; font-weight: 800; color: #1b5e20; line-height: 1.1;">50</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Автопостов (ААП)</div>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 9.2 АНАЛИТИКА И QR-ДОСТУП
    col_qr, col_chart = st.columns([1, 2])

    with col_qr:
        st.markdown("""
                <div style="background: #f1f8e9; padding: 20px; border-radius: 15px; border: 1px dashed #2e7d32; text-align: center;">
                    <h5 style="color: #1b5e20; margin-bottom: 15px;">📲 Приложение AgroData</h5>
                    <img src="https://img.icons8.com/ios/100/2e7d32/qr-code--v1.png" width="100">
                    <p style="font-size: 0.8em; margin-top: 10px; color: #455a64;">Доступ к фактическим данным для фермеров в режиме реального времени</p>
                    <a href="https://agrodata.kazhydromet.kz" target="_blank" style="text-decoration: none;">
                        <button style="background: #2e7d32; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Открыть портал</button>
                    </a>
                </div>
            """, unsafe_allow_html=True)

    with col_chart:
        st.write("### 🌦️ Фенологический мониторинг")
        crop_data = {
                "Состояние посевов": ["Хорошее", "Удовлетворительное", "Плохое"],
                "Процент площади": [65, 25, 10]
             }
        fig_donut = go.Figure(data=[go.Pie(labels=crop_data["Состояние посевов"], 
                                             values=crop_data["Процент площади"], 
                                             hole=.5,
                                             marker_colors=['#2e7d32', '#fbc02d', '#d32f2f'])])
        fig_donut.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=250, showlegend=True)
        st.plotly_chart(fig_donut, use_container_width=True)

    st.divider()

        # --- БЛОКИ С ПОДРОБНОСТЯМИ ---
        # 1. Словарь с путями к фото (Замените на актуальные пути для агро)
    AGRO_IMAGE_PATHS = {
            "Soil": r"C:\Users\eltai_a\Desktop\RES\stend\Soil.jpeg",
            "Phenology": r"C:\Users\eltai_a\Desktop\RES\stend\Pheno.jpeg",
            "AutoAgro": r"C:\Users\eltai_a\Desktop\RES\stend\AutoAgro.jpeg",
            "Yield": r"C:\Users\eltai_a\Desktop\RES\stend\Yield.jpeg"
    }

    a_col1, a_col2, a_col3, a_col4 = st.columns(4)

    draw_block(a_col1, "agro_btn_1", "🌱 Фенология", "🌾", 
                   "Наблюдения за ростом и развитием культурных растений.", 
                   ["<b>Фазы:</b> всходы, кущение, колошение", "<b>Высота:</b> замеры каждые 10 дней", "<b>Густота:</b> стеблестой на 1 м²"], "Phenology")

    draw_block(a_col2, "agro_btn_2", "💧 Влажность почвы", "🧪", 
                   "Определение запасов продуктивной влаги в слое до 1 метра.", 
                   ["<b>Метод:</b> термостатно-весовой", "<b>Глубина:</b> послойно через 10 см", "<b>Сроки:</b> в начале и конце декады"], "Soil")

    draw_block(a_col3, "agro_btn_3", "📡 Агро-автоматизация", "🤖", 
                   "Датчики температуры почвы и влажности в режиме онлайн.", 
                   ["<b>Глубина:</b> до 120 см", "<b>Параметры:</b> электропроводность и T", "<b>Передача:</b> GPRS/LoRaWAN"], "AutoAgro")

    draw_block(a_col4, "agro_btn_4", "📉 Прогнозы", "📈", 
                   "Моделирование урожайности и оптимальных сроков сева.", 
                   ["<b>Урожай:</b> зерновые и масличные", "<b>Засуха:</b> индекс SPEI", "<b>Рекомендации:</b> для фермеров"], "Yield")

        # --- ГРАФИК ПО ОБЛАСТЯМ ---
    st.subheader("🚜 Оснащенность агро-сети по регионам")

    agro_data = {
            "Область": ["Акмолинская", "Костанайская", "СКО", "Алматинская", "Туркестанская", "ВКО", "Павлодарская", "Карагандинская"],
            "Агропосты": [28, 26, 24, 18, 22, 20, 15, 12],
            "Метеостанции": [35, 32, 30, 25, 28, 24, 20, 18]
    }
    df_agro = pd.DataFrame(agro_data)

    fig_agro = go.Figure()
    fig_agro.add_trace(go.Bar(x=df_agro["Область"], y=df_agro["Агропосты"], name="Агропосты", marker_color='#2e7d32'))
    fig_agro.add_trace(go.Bar(x=df_agro["Область"], y=df_agro["Метеостанции"], name="Метеостанции", marker_color='#81c784'))

    fig_agro.update_layout(barmode='group', height=400, margin=dict(t=20, b=20))
    st.plotly_chart(fig_agro, use_container_width=True)

        # --- РЕТРОСПЕКТИВА (Было/Стало для Агро) ---
    st.markdown("### 📊 Агро-ретроспектива: Сравнение влагозапасов")
        
    AGRO_HIST_DATA = {
            "Акмолинская обл. (Зерновой пояс)": {
                "record_low": 45, "record_year": 2021, "current_val": 85, "norm": 100,
                "fact": "В засушливом 2021 году запасы влаги были критически низкими, что привело к снижению урожая."
        },
            "Туркестанская обл. (Хлопковый пояс)": {
                "record_low": 30, "record_year": 2019, "current_val": 55, "norm": 70,
                "fact": "Дефицит поливной воды часто совпадает с аномально жарким летом."
        }
    }

    agro_choice = st.selectbox("Выберите регион:", list(AGRO_HIST_DATA.keys()))
    a_data = AGRO_HIST_DATA[agro_choice]

    ac1, ac2 = st.columns(2)
    with ac1:
        st.markdown(f"""<div style="background-color: #fff3e0; padding:20px; border-radius:15px; border-left:8px solid #ff9800;">
                <h5 style="margin:0; color:#e65100;">📉 ИСТОРИЧЕСКИЙ МИНИМУМ</h5>
                <h2 style="margin:0;">{a_data['record_low']} мм</h2>
                <p>{a_data['record_year']} год (засуха)</p></div>""", unsafe_allow_html=True)
    with ac2:
            st.markdown(f"""<div style="background-color: #e8f5e9; padding:20px; border-radius:15px; border-left:8px solid #4caf50;">
                <h5 style="margin:0; color:#1b5e20;">💧 ТЕКУЩИЙ ЗАПАС</h5>
                <h2 style="margin:0;">{a_data['current_val']} мм</h2>
                <p>20 февраля 2026 г.</p></div>""", unsafe_allow_html=True)

    st.progress(a_data['current_val']/a_data['norm'], text=f"Влагозарядка: {int(a_data['current_val']/a_data['norm']*100)}% от нормы")
    st.info(f"💡 {a_data['fact']}")

        

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
    
# ПРОГНОЗ ПОГОДЫ   
with tabs[1]:
    # Заголовок с кастомным цветом
    st.markdown("""
        <h1 style='color: #1E3A8A; font-family: sans-serif;'>
            🌦️ Гидрометцентр Казахстана: Точность. Оперативность. Безопасность.
        </h1>
    """, unsafe_allow_html=True)
    
    # Описание основного подразделения
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #2563EB;">
        <p style="font-size: 1.1em; color: #333; margin: 0;">
            <b>Гидрометцентр — это сердце Казгидромета.</b> Мы работаем круглосуточно (24/7), 
            чтобы вовремя предупреждать вас о штормах и давать точные прогнозы в режиме реального времени.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Стили для карточек (адаптированные под 4 колонки)
    st.markdown("""
        <style>
        .forecast-card {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            height: 250px; /* Высота увеличена, так как колонки стали уже */
            transition: transform 0.2s;
            display: flex;
            flex-direction: column;
        }
        .forecast-card:hover {
            transform: translateY(-5px);
            border-color: #2563EB;
        }
        .icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
        .title {
            color: #1E3A8A;
            font-weight: bold;
            font-size: 0.95em;
            margin-bottom: 8px;
            line-height: 1.2;
        }
        .description {
            color: #4B5563;
            font-size: 0.8em;
            line-height: 1.3;
        }
        </style>
    """, unsafe_allow_html=True)

    # Создаем 4 колонки в одну строку
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("""
            <div class="forecast-card">
                <div class="icon">⚡</div>
                <div class="title">Наукастинг (2-6 часов)</div>
                <div class="description">Сверхкраткосрочный прогноз. Для тех, кто планирует выезд сейчас или работает на воздухе.</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="forecast-card">
                <div class="icon">🏔️</div>
                <div class="title">Безопасность в горах</div>
                <div class="description">Прогнозы для туристов и бюллетени селевой опасности. Мы знаем, когда в горах опасно.</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="forecast-card">
                <div class="icon">🌾</div>
                <div class="title">Поддержка агробизнеса</div>
                <div class="description">прогнозы погоды на 1-2-3 дня. </div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="forecast-card">
                <div class="icon">🌫️</div>
                <div class="title">Экология города</div>
                <div class="description">прогнозы на неделю, на 10 дней.</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
            <div class="forecast-card">
                <div class="icon">🌫️</div>
                <div class="title">Экология города</div>
                <div class="description">консультативный прогноз на месяц, сезон.</div>
            </div>
        """, unsafe_allow_html=True)    

    # Данные для графика
    accuracy_data = {
        "Срок прогноза": ["По пункту", "1 сутки", "2-3 суток", "Неделя", "Декада", "Месяц", "Сезон"],
        "Оправдываемость (%)": [91, 96, 92, 91, 86, 69, 60]
    }
    df_acc = pd.DataFrame(accuracy_data)

    # Заголовок блока
    st.markdown("<h3 style='text-align: center; color: #1E3A8A;'>📊 Насколько точны наши прогнозы?</h3>", unsafe_allow_html=True)

    # Верхний ряд: Основные метрики (интерактивные "кнопки")
    col_acc1, col_acc2, col_acc3 = st.columns(3)
    with col_acc1:
        st.metric("Суточные прогнозы", "96%", help="Высочайшая точность подтверждена верификацией")
    with col_acc2:
        st.metric("Прогнозы на 2-3 дня", "92%")
    with col_acc3:
        st.metric("Прогнозы на неделю", "91%")

    # Раскрывающийся блок с графиком и базой данных
    with st.expander("🔍 Нажмите здесь, чтобы увидеть детальный график оправдываемости и источники данных"):
        st.markdown("<h4 style='color: #1E3A8A;'>Детальная статистика и надежность</h4>", unsafe_allow_html=True)
        
        col_chart, col_info = st.columns([2, 1])
        
        with col_chart:
            # Создание графика
            fig = px.bar(df_acc, x="Срок прогноза", y="Оправдываемость (%)", 
                         text="Оправдываемость (%)", color="Оправдываемость (%)",
                         color_continuous_scale="RdYlGn", 
                         title="Средняя оправдываемость по категориям (%)")
            
            # Стилизация графика под дизайн сайта
            fig.update_layout(
                font=dict(family="sans-serif", size=12, color="#4B5563"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("*Согласно данным верификации Гидрометцентра за отчетный период")

        with col_info:
            st.info("""
            **Информационная база:**
            * **Наблюдения:** Сеть наземных и аэрологических станций Казахстана.
            * **Спутники:** Прямой прием данных Eumetsat, CMACast, НИЦ «Планета».
            * **Модели:** Глобальные системы ECMWF, немецкие ICON/COSMO и адаптированная WRF.
            """)

    st.divider()


    # --- Блок 3. Источники данных и Инфраструктура ---
    st.markdown("<h2 style='text-align: center; color: #1E3A8A; margin-top: 50px;'>📊 Глобальная сеть данных</h2>", unsafe_allow_html=True)

    # Стили для контента данных
    st.markdown("""
        <style>
        .data-box {
            background-color: #f0f4f8;
            border-radius: 10px;
            padding: 20px;
            border-left: 5px solid #1E3A8A;
            height: 100%;
        }
        .data-title {
            font-weight: bold;
            color: #1E3A8A;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .data-list {
            list-style-type: none;
            padding-left: 0;
            font-size: 0.9em;
            color: #4B5563;
        }
        .data-list li {
            margin-bottom: 8px;
            padding-left: 15px;
            position: relative;
        }
        .data-list li::before {
            content: "•";
            color: #2563EB;
            font-weight: bold;
            position: absolute;
            left: 0;
        }
        </style>
    """, unsafe_allow_html=True)

    col_d1, col_d2, col_d3 = st.columns(3)

    with col_d1:
        st.markdown("""
            <div class="data-box">
                <div class="data-title">📍 Наземный мониторинг</div>
                <ul class="data-list">
                    <li><b>Метеорологические станции:</b> непрерывный сбор данных о температуре, давлении и влажности.</li>
                    <li><b>Аэрологические станции:</b> зондирование атмосферы для анализа верхних слоев.</li>
                    <li><b>Гидрологические посты:</b> контроль уровня рек и паводковой ситуации.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col_d2:
        st.markdown("""
            <div class="data-box">
                <div class="data-title">📡 Дистанционное зондирование</div>
                <ul class="data-list">
                    <li><b>Eumetsat:</b> европейские геостационарные спутники (MSG).</li>
                    <li><b>CMACast:</b> оперативные данные китайских метеоспутников.</li>
                    <li><b>НИЦ «Планета»:</b> российские орбитальные системы серии «Метеор-М».</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col_d3:
        st.markdown("""
            <div class="data-box">
                <div class="data-title">⚙️ Численные модели</div>
                <ul class="data-list">
                    <li><b>ECMWF:</b> глобальные прогнозы с детализацией до 9 км.</li>
                    <li><b>ICON / COSMO:</b> высокоточные мезомасштабные модели.</li>
                    <li><b>WRF Казгидромет:</b> собственная адаптированная модель для территории Казахстана.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # Визуальный разделитель с пояснением
    st.warning("""
        💡 **Интеграция данных:** Все потоки информации стекаются в единый прогностический центр, 
        где дежурная смена синоптиков проводит финальный анализ и верификацию перед выпуском бюллетеней.
    """)

    st.markdown("<h2 style='text-align: center; color: #1E3A8A; margin-top: 50px;'>📢 Оперативное реагирование</h2>", unsafe_allow_html=True)

    col_reg1, col_reg2 = st.columns(2)

    with col_reg1:
        st.info("""
        **Штормовые предупреждения:**
        Выпускаются при угрозе ОЯ (опасных явлений) и СГЯ (стихийных гидрометеорологических явлений).
        * **Заблаговременность:** от 6 до 48 часов.
        * **Состав:** Дата, время, интенсивность, локация.
        """)

    with col_reg2:
        st.success("""
        **Регулярность обновлений:**
        * **1-3 дня:** Ежедневно (обновление каждые 6-12 часов).
        * **Неделя / Декада:** Регулярные уточнения по мере поступления новых данных.
        * **Месяц / Сезон:** Консультативные прогнозы (выпуск 15-го числа).
        """)
    
    st.markdown("<h3 style='color: #1E3A8A;'>💼 Погода для отраслей экономики</h3>", unsafe_allow_html=True)

    eco_data = {
        "Отрасль": ["Сельское хозяйство", "Энергетика", "Строительство", "Водные ресурсы", "Транспорт"],
        "Применение прогноза": [
            "Сроки сева, внесения удобрений и уборки урожая",
            "Расчет потребления электроэнергии в пики холода/жары",
            "Определение продолжительности строительного сезона",
            "Предотвращение наводнений и управление ирригацией",
            "Безопасность авиасообщения и автодорог (гололед, туман)"
        ]
    }
    st.table(pd.DataFrame(eco_data))

    st.markdown("### 🕒 Горизонты планирования")

    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; background: #f8f9fa; padding: 20px; border-radius: 50px; border: 1px solid #dee2e6;">
        <div style="text-align: center;"><strong>2-6 ч</strong><br><small>Наукастинг</small></div>
        <div style="color: #2563EB;">➡</div>
        <div style="text-align: center;"><strong>1-3 дня</strong><br><small>Краткосрочный</small></div>
        <div style="color: #2563EB;">➡</div>
        <div style="text-align: center;"><strong>10 дней</strong><br><small>Среднесрочный</small></div>
        <div style="color: #2563EB;">➡</div>
        <div style="text-align: center;"><strong>Месяц+</strong><br><small>Долгосрочный</small></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #1E3A8A; margin-top: 50px;'>🌍 Масштаб мониторинга</h2>", unsafe_allow_html=True)

    col_map, col_alerts = st.columns([1.5, 1])

    with col_map:
        # Здесь можно вставить реальную карту или стилизованное изображение
        st.image("https://www.kazhydromet.kz/assets/images/map-alert-preview.png", caption="Единая система метеорологического контроля РК")
        st.markdown("""
            <p style='font-size: 0.9em; color: #6B7280;'>
            Мы объединяем данные со всех областей Казахстана, чтобы обеспечить локальную точность в каждом населенном пункте.
            </p>
        """, unsafe_allow_html=True)

    with col_alerts:
        st.markdown("""
            <div style="background-color: #FFFBEB; padding: 20px; border-radius: 12px; border-left: 5px solid #F59E0B;">
                <h4 style="color: #92400E; margin-top: 0;">⚠️ Штормовой протокол</h4>
                <p style="font-size: 0.9em; color: #92400E;">
                При угрозе стихийных явлений (СГЯ) оповещение происходит <b>незамедлительно</b>.
                </p>
                <ul style="font-size: 0.85em; color: #92400E;">
                    <li><b>6–48 часов:</b> заблаговременность выпуска.</li>
                    <li><b>Детализация:</b> время, место, сила явления.</li>
                    <li><b>Адресность:</b> прямая передача в службы ЧС и госорганы.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        


    # 2. Выбор типа прогноза
    st.markdown("<h2 style='color: #1E3A8A;'>📅 Виды и регламент прогнозов</h2>", unsafe_allow_html=True)
    
    forecast_type = st.selectbox(
        "Выберите категорию прогноза:",
        ["Оперативные и специализированные", "Кратко- и среднесрочные", "Долгосрочные (месяц/сезон)"]
    )

    if forecast_type == "Оперативные и специализированные":
        st.warning("⚡ **Штормовые предупреждения (6–48 часов)**")
        st.write("Составляются незамедлительно при угрозе ОЯ/СГЯ с указанием интенсивности, места и времени.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div style='background-color: #F3F4F6; padding: 15px; border-radius: 10px; border-left: 5px solid #1E3A8A;'>
            <strong>Специализированные услуги:</strong><br>
            • 🔥 Пожарная опасность: карта классов<br>
            • 🌫️ НМУ: для городов<br>
            • 🏔️ Селевая опасность: для гор
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div style='background-color: #F3F4F6; padding: 15px; border-radius: 10px; border-left: 5px solid #2563EB;'>
            <strong>Новые направления:</strong><br>
            • ⚡ Наукастинг: прогноз на 2-6 часов<br>
            • 🏕️ Туризм: пункты маршрутов
            </div>
            """, unsafe_allow_html=True)

    elif forecast_type == "Кратко- и среднесрочные":
        st.success("📈 **Регулярные выпуски**")
        st.markdown("""
        * **Прогнозы на 1-3 дня:** ежедневно.
        * **Прогнозы на неделю и 10 дней:** регулярно.
        * **Декадные прогнозы:** выпускаются 10, 20 и 30-31 числа.
        """)

    elif forecast_type == "Долгосрочные (месяц/сезон)":
        st.markdown("<h3 style='color: #1E3A8A;'>Управление долгосрочных прогнозов</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p style='color: #4B5563;'>Используется метод <strong>года-аналога</strong> и численные модели мировых климатических центров.</p>
        <ul>
            <li><strong>Прогноз на месяц:</strong> Бюллетень 15-го числа.</li>
            <li><strong>Сезонный прогноз:</strong> 15 марта и 15 октября.</li>
        </ul>
        """, unsafe_allow_html=True)

    st.divider()

    # 3. Применение в экономике
    st.markdown("<h2 style='color: #1E3A8A;'>💼 Востребованность в отраслях экономики</h2>", unsafe_allow_html=True)
    
    sectors = {
        "🌾 Сельское хозяйство": "Сроки сева, удобрений и уборки урожая.",
        "💧 Водные ресурсы": "Предотвращение наводнений и ирригация.",
        "⚡ Электроэнергетика": "Прогноз потребления энергии.",
        "🏗️ Строительство": "Продолжительность строит. сезона.",
        "🌲 Лесная отрасль": "Защита лесов от пожаров.",
        "🗺️ Туризм": "Планирование отдыха и осадков."
    }
    
    cols = st.columns(3)
    for i, (sector, desc) in enumerate(sectors.items()):
        with cols[i % 3]:
            # Используем HTML для стилизации карточек секторов
            st.markdown(f"""
                <div style='border: 1px solid #E5E7EB; padding: 10px; border-radius: 8px; margin-bottom: 10px;'>
                    <div style='color: #1E3A8A; font-weight: bold; font-size: 1em;'>{sector}</div>
                    <div style='color: #6B7280; font-size: 0.85em;'>{desc}</div>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # 4. Визуальный мониторинг
    st.markdown("<h2 style='color: #1E3A8A;'>⚠️ Карта метеорологических предупреждений</h2>", unsafe_allow_html=True)
    st.image("https://www.kazhydromet.kz/assets/images/map-alert-preview.png") 
    st.markdown("<p style='color: #6B7280; font-style: italic; font-size: 0.9em;'>Цветовая шкала опасности: от зеленого до красного.</p>", unsafe_allow_html=True)

    if st.button("📊 Сформировать ежедневный бюллетень селевой опасности"):
        st.write("🔄 Идет обработка данных по горным районам...")


with tabs[2]:
    st.title("Агрометеорологические прогнозы")

with tabs[3]:
    st.title("Гидрологические прогнозы")

with tabs[4]:
    import streamlit as st
    import geopandas as gpd
    import folium
    from streamlit_folium import st_folium
    import os
    import pandas as pd
    import plotly.graph_objects as go

    # --- НАСТРОЙКИ И ДАННЫЕ ---
    FOLDER_PATH = r"C:\Users\eltai_a\Desktop\RES\stend\UMGPGR\шейпы"

    VXB_STATS = {
        "Арало-Сырдарьинский ВХБ": {"норма": 21.5, "местные": 3.22, "приток": 18.2, "отток": None},
        "Балхаш-Алакольский ВХБ": {"норма": 29.9, "местные": 17.2, "приток": 12.7, "отток": "В КНР: 0.67"},
        "Ертисский ВХБ": {"норма": 33.4, "местные": 26.4, "приток": 7.02, "отток": "В КНР: 2.20, В РФ: 26.2"},
        "Жайык-Каспийский ВХБ": {"норма": 12.0, "местные": 3.37, "приток": 19.6, "отток": "В РФ: 1.48"},
        "Есильский ВХБ": {"норма": 2.29, "местные": 2.29, "приток": 0, "отток": "В РФ: 1.86"},
        "Нура-Сарысуйский ВХБ": {"норма": 1.16, "местные": 1.16, "приток": 0, "отток": None},
        "Шу-Таласский ВХБ": {"норма": 4.13, "местные": 1.29, "приток": 2.24, "отток": None},
        "Тобол-Торгайский ВХБ": {"норма": 1.67, "местные": 1.34, "приток": 0.34, "отток": "В РФ: 0.46"},
        "Республика Казахстан": {"норма": 107.0, "местные": 57.1, "приток": 49.4, "отток": None}
    }

    @st.cache_data
    def load_geo_data(path):
        all_gdf = []
        rivers = None
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith("_VXB.shp"):
                    gdf = gpd.read_file(os.path.join(path, file))
                    all_gdf.append(gdf.to_crs(epsg=4326))
            rivers_path = os.path.join(path, "rivers_kz.shp")
            if os.path.exists(rivers_path):
                rivers = gpd.read_file(rivers_path).to_crs(epsg=4326)
        basins = pd.concat(all_gdf, ignore_index=True) if all_gdf else None
        return basins, rivers

    st.title("🌊 ВОДНЫЕ РЕСУРСЫ КАЗАХСТАНА")
    data_basins, data_rivers = load_geo_data(FOLDER_PATH)

    if data_basins is not None:
        tooltip_col = 'ВХБ_н_'
        
        # --- ВЕРХНЯЯ ЧАСТЬ: КАРТА И ИНФО-ПАНЕЛЬ ---
        col1, col2 = st.columns([2.2, 1])
        
        with col1:
            m = folium.Map(location=[48.0, 68.0], zoom_start=5, tiles="cartodbpositron")
            folium.GeoJson(
                data_basins,
                style_function=lambda x: {'fillColor': '#3186cc', 'color': '#1d3557', 'weight': 1, 'fillOpacity': 0.4},
                highlight_function=lambda x: {'fillColor': '#00fbff', 'color': 'white', 'weight': 3, 'fillOpacity': 0.7},
                tooltip=folium.GeoJsonTooltip(fields=[tooltip_col])
            ).add_to(m)
            if data_rivers is not None:
                folium.GeoJson(data_rivers, style_function=lambda x: {'color': '#003399', 'weight': 1.2, 'opacity': 0.7}, interactive=False).add_to(m)
            output = st_folium(m, width=None, height=500, use_container_width=True, key="vxb_map")

        # Определение выбора
        display_name = "Республика Казахстан"
        if output and output.get("last_active_drawing"):
            raw_name = output["last_active_drawing"]["properties"].get(tooltip_col, "Республика Казахстан")
            clean_name = str(raw_name).replace('\n', ' ').strip().lower()
            for key in VXB_STATS.keys():
                main_word = key.lower().split('-')[0].split(' ')[0]
                if main_word in clean_name:
                    display_name = key
                    break

        with col2:
                    # Внедряем CSS, чтобы сделать текст внутри метрик жирным
                    st.markdown("""
                        <style>
                        [data-testid="stMetricValue"] {
                            font-weight: 800 !important;
                            color: #1e3799;
                        }
                        </style>
                        """, unsafe_allow_html=True)

                    st.markdown("### 📊 Характеристики")
                    st.success(f"📍 **{display_name}**")
                    
                    cur_stats = VXB_STATS[display_name]
                    
                    # 1. Общая норма (жирный шрифт применится автоматически через CSS)
                    st.metric("💠 Норма бассейна (W)", f"{cur_stats['норма']} км³/год")
                    
                    # Разделяем на Местный сток и Приток
                    m_col1, m_col2 = st.columns(2)
                    with m_col1:
                        st.metric("🏔️ Местный сток", f"{cur_stats['местные']} км³")
                    with m_col2:
                        st.metric("💧 Приток", f"{cur_stats['приток']} км³")
                    
                    # 3. Блок оттока
                    if cur_stats.get('отток'):
                        # Внутри st.warning можно использовать стандартный жирный шрифт **
                        st.warning(f"📤 **Отток:** **{cur_stats['отток']}**")
                    else:
                        st.info("🔄 Трансграничный отток не зафиксирован")

                    st.markdown("---") 
                    
                    # 4. Стилизованная кнопка перехода
                    if display_name != "Республика Казахстан":
                        anchor_id = display_name.replace(' ', '-').lower()
                        st.markdown(f"""
                            <a href="#{anchor_id}" style="text-decoration: none;">
                                <div style="
                                    background: linear-gradient(90deg, #1e3799, #009432);
                                    color: white; 
                                    padding: 12px; 
                                    border-radius: 8px; 
                                    text-align: center;
                                    font-weight: bold;
                                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                                ">
                                    📈 Посмотреть гидрограф бассейна
                                </div>
                            </a>
                        """, unsafe_allow_html=True)
                    else:
                        st.caption("ℹ️ Выберите бассейн на карте для детального анализа")
                
      
        import streamlit as st
        import pandas as pd
        import plotly.graph_objects as go
        import numpy as np

        # 1. Подготовка данных
        data = {
            "Год": list(range(1940, 2026)),
            "Местный сток": [
                45.93, 76.95, 71.69, 47.23, 39.70, 37.49, 78.82, 66.24, 66.82, 62.22, 50.53, 34.18, 64.30, 46.73, 67.23, 
                47.32, 52.98, 55.30, 73.76, 63.77, 68.94, 53.32, 43.40, 43.52, 58.37, 39.76, 72.40, 42.05, 43.24, 75.23, 
                65.19, 68.77, 61.34, 63.95, 36.44, 43.60, 46.75, 48.22, 48.94, 66.74, 50.83, 51.30, 38.95, 53.70, 48.42, 
                62.49, 47.10, 65.61, 72.56, 50.36, 69.40, 49.43, 55.12, 83.03, 67.19, 51.71, 52.19, 52.53, 54.28, 46.72, 
                50.22, 65.06, 75.78, 51.02, 59.62, 62.79, 49.59, 63.41, 43.68, 56.43, 73.31, 51.38, 42.27, 68.59, 60.78, 
                65.09, 77.84, 75.29, 56.80, 58.40, 48.23, 45.69, 52.47, 60.47, 89.56, 58.34
            ],
            "Приток": [
                42.65, 69.16, 70.34, 49.81, 42.05, 51.71, 72.44, 60.79, 59.50, 60.28, 45.96, 42.23, 67.31, 56.83, 63.48, 
                50.14, 55.52, 57.02, 66.28, 66.41, 68.36, 44.54, 40.48, 50.45, 59.67, 36.88, 62.41, 33.95, 40.95, 88.63, 
                66.16, 55.82, 43.27, 47.28, 28.48, 26.26, 29.58, 31.05, 34.74, 42.42, 39.17, 43.43, 35.22, 36.74, 35.77, 
                40.93, 35.79, 49.80, 60.41, 39.37, 52.77, 45.06, 42.02, 64.87, 66.24, 40.77, 42.65, 39.81, 58.52, 50.33, 
                50.46, 50.68, 62.43, 59.34, 52.80, 56.29, 45.44, 46.98, 37.86, 36.84, 59.84, 40.80, 40.01, 42.86, 41.56, 
                39.47, 52.54, 58.58, 41.53, 36.47, 32.81, 28.13, 32.43, 38.03, 51.35, 35.72
            ],
            "ВХБ": [
                88.58, 146.12, 142.03, 97.04, 81.75, 89.20, 151.26, 127.04, 126.31, 122.50, 96.48, 76.41, 131.60, 103.57, 130.70, 
                97.46, 108.50, 112.32, 140.04, 130.18, 137.30, 97.86, 83.88, 93.96, 118.04, 76.64, 134.81, 76.00, 84.19, 163.86, 
                131.35, 124.59, 104.60, 111.23, 64.92, 69.87, 76.33, 79.27, 83.69, 109.16, 90.00, 94.73, 74.17, 90.44, 84.18, 
                103.42, 82.90, 115.41, 132.98, 89.73, 122.17, 94.49, 97.13, 147.90, 133.43, 92.49, 94.84, 92.34, 112.81, 97.04, 
                100.68, 115.74, 138.20, 110.35, 112.41, 119.08, 95.03, 110.39, 81.54, 93.28, 133.15, 92.18, 82.28, 111.45, 102.34, 
                104.57, 130.37, 133.87, 98.33, 94.87, 81.04, 73.82, 84.90, 98.50, 140.90, 94.06
            ]
        }

        df = pd.DataFrame(data)

        # 2. Расчет тренда
        z = np.polyfit(df['Год'], df['ВХБ'], 1)
        p = np.poly1d(z)
        df['Тренд'] = p(df['Год'])

        # 3. Создание графика
        fig = go.Figure()

        # Местный сток - Глубокий синий
        fig.add_trace(go.Bar(
            x=df['Год'], y=df['Местный сток'],
            name='Местный сток',
            marker_color='#1f77b4',  # Steel Blue
            opacity=0.9
        ))

        # Приток - Светло-голубой
        fig.add_trace(go.Bar(
            x=df['Год'], y=df['Приток'],
            name='Приток',
            marker_color='#a6cee3',  # Light Blue
            opacity=0.9
        ))

        # Линия тренда - Темно-синий/Полночный
        fig.add_trace(go.Scatter(
            x=df['Год'], y=df['Тренд'],
            mode='lines',
            name='Линия тренда (ВХБ)',
            line=dict(color='#08306b', dash='dash', width=3) 
        ))

        # Настройка оформления
        fig.update_layout(
            title=dict(
                text='Динамика водности Республики Казахстан (1940-2025)',
                font=dict(color='#08306b', size=20)
            ),
            xaxis_title='Год',
            yaxis_title='W, км³',
            barmode='stack',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified",
            height=550,
            template="plotly_white",
            # Добавляем сетку для лучшей читаемости
            yaxis=dict(gridcolor='#f0f0f0'),
            xaxis=dict(gridcolor='#f0f0f0')
        )

        # Отображение в Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # 4. Аналитическая справка
        st.info(f"""
            **Аналитическая сводка:** * Исторический максимум (ВХБ): **{df['ВХБ'].max()} км³** ({df.loc[df['ВХБ'].idxmax(), 'Год']} г.)
            * Исторический минимум (ВХБ): **{df['ВХБ'].min()} км³** ({df.loc[df['ВХБ'].idxmin(), 'Год']} г.)
            * Среднее значение за период: **{df['ВХБ'].mean():.2f} км³**
        """)

      
        # Базовый путь к папке с фотографиями
        BASE_IMAGE_PATH = r"C:\Users\eltai_a\Desktop\RES\stend\UMGPGR"

        vxb_list = [k for k in VXB_STATS.keys() if k != "Республика Казахстан"]
        
        for name in vxb_list:
            item_stats = VXB_STATS[name]
            is_active = (name == display_name)
            anchor_name = name.replace(' ', '-').lower()
            
            # Формируем путь к фото на основе названия ВХБ
            # Ожидаемый формат файла: "Название ВХБ.jpeg"
            photo_path = os.path.join(BASE_IMAGE_PATH, f"{name}.jpg")
            
            st.markdown(f"<div id='{anchor_name}'></div>", unsafe_allow_html=True)
            
            with st.container(border=is_active):
                st.markdown(f"### {'🌟' if is_active else '🔹'} {name}")
                
                img_col, info_col = st.columns([1.2, 1])
                
                with img_col:
                    # Проверяем физическое наличие файла перед выводом
                    if os.path.exists(photo_path):
                        st.image(photo_path, use_container_width=True, caption=f"ВХБ: {name}")
                    else:
                        # Если фото еще не загружено в папку
                        st.info(f"📸 Фото для {name} ожидается (файл должен называться '{name}.jpeg')")
                        st.image("https://via.placeholder.com/600x400?text=Photo+In+Progress", use_container_width=True)
                
            with info_col:
                st.markdown(f"##### 📝 Гидрологическая справка: {name}")
                
                # Авто-расчет долей
                norma = item_stats['норма']
                local_perc = (item_stats['местные'] / norma) * 100 if norma > 0 else 0
                inflow_perc = (item_stats['приток'] / norma) * 100 if norma > 0 else 0

                # Ряд основных метрик
                m1, m2, m3 = st.columns(3)
                m1.metric("Площадь", "347 757 км²")
                m2.metric("ГП в ВХБ", "58")
                m3.metric("Всего рек", "13 201")

                # Блок Местные ресурсы vs Приток
                col_res, col_inf = st.columns(2)
                with col_res:
                    st.write("🌳 **Местные ресурсы**")
                    st.caption("5 крупных рек (Калжыр, Куршим, Буктырма, Ульби, Оба) формируют ~70% стока.")
                with col_inf:
                    st.write("🌏 **Приток**")
                    st.caption("Поступает из КНР по реке Кара Ертис, фиксируется в створе у.с. Боран.")

                # График
                if "Ертисский" in name:
                    years = list(range(1940, 2025))
                    # Данные из вашей таблицы
                    local_flow = [25.49, 33.64, 28.02, 25.26, 24.65, 19.6, 41.14, 37.13, 26.61, 28.29, 26.56, 15.32, 29.44, 19.89, 31.42, 20.18, 25.12, 27.11, 37.99, 25.85, 32.94, 28.71, 21.32, 18.68, 22.39, 21.29, 35.9, 21.66, 21.05, 35.08, 28.72, 31.42, 26.58, 31.4, 16.7, 24.76, 24.51, 25.69, 21.33, 33.19, 21.11, 19.46, 18.22, 24.69, 25.4, 28.48, 23.26, 27.19, 29.77, 25.01, 30.83, 20.56, 29.86, 31.49, 28.56, 26.83, 23.46, 22.99, 22.93, 22.1, 21.44, 33.15, 30.37, 18.74, 24.62, 23.41, 24.99, 27.52, 19.34, 31.04, 31.4, 21.57, 19.08, 42.49, 30.77, 32.48, 35.51, 26.86, 26.39, 25.45, 24.9, 22.22, 22.3, 25.4, 30.65]
                    inflow = [8.17, 9.65, 10.75, 7.64, 6.46, 5.7, 10.59, 8.96, 5.83, 6.63, 7.22, 5.22, 9.88, 5.7, 7.85, 7.53, 8.88, 7.4, 10.75, 8.41, 8.86, 10.4, 6.9, 5.81, 6.97, 5.48, 11.31, 4.88, 7.67, 11.37, 9.57, 9.79, 7.34, 9.41, 3.17, 6.14, 5.17, 7.01, 4.33, 6.65, 5.68, 5.7, 3.29, 5.54, 9.44, 7.57, 5.21, 8.02, 9.72, 4.47, 6.41, 4.63, 6.64, 11.12, 9.29, 6.85, 5.51, 6.22, 6.55, 6.31, 5.89, 8.6, 7.5, 4.37, 5.67, 6.81, 5.83, 4.38, 3.63, 2.35, 7.23, 3.62, 2.85, 7.84, 5.64, 6.05, 8.5, 8.72, 7.2, 4.65, 5.31, 4.29, 3.28, 5.25, 6.98]
                    
                    mini_fig = go.Figure()
                    mini_fig.add_trace(go.Bar(x=years, y=local_flow, name='Местный сток', marker_color='#1f77b4'))
                    mini_fig.add_trace(go.Bar(x=years, y=inflow, name='Приток', marker_color='#a6cee3'))
                    mini_fig.update_layout(barmode='stack', height=180, margin=dict(l=0,r=0,t=10,b=0), template="plotly_white", showlegend=False)
                    st.plotly_chart(mini_fig, use_container_width=True)

                # Детализация (по данным из картинки)
                st.markdown("---")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("🌊 **Артерия:** Река Ертис")
                    st.write(f"📊 **Норма (W):** {norma} км³/год")
                with col_b:
                    st.write(f"🏢 **Объекты:** >82 вдхр. и прудов")
                    st.write(f"📑 **Рек (Б/С):** 6 / **Малых:** 1195")

                with st.expander("📍 Список используемых гидропостов (ГП)"):
                    st.write("1. р. Калжыр — с. Калжыр")
                    st.write("2. р. Куршим — с. Вознесенка")
                    st.write("3. р. Буктырма — с. Лесная Пристань")
                    st.write("4. р. Ульби — с. Ульби")
                    st.write("5. Перевалочная")
                    st.write("6. р. Оба — г. Шемонаиха")
                    st.write("7. р. Кара Ертис — с. Боран")
                
                st.markdown("---")
                
                
            # --- СПЕЦИАЛЬНЫЙ БЛОК ДЛЯ ЕРТИССКОГО ВХБ ---
            if "Ертисский" in name:
                st.markdown("---")
                st.markdown("### 📊 Детальный анализ стока")

                # Описание блоков перед графиками
                desc_col1, desc_col2 = st.columns(2)
                with desc_col1:
                    st.info("""**Местный сток:** Анализ базируется на 5 крупнейших реках (Калжыр, Куршим, Буктырма, Ульби, Оба). 
                    Они формируют около **70%** водных ресурсов бассейна, возникающих непосредственно на территории Казахстана.""")
                
                with desc_col2:
                    st.info("""**Приток:** Учитывается трансграничный сток реки Кара Ертис, поступающий из КНР. 
                    Наблюдения фиксируются на гидропосту у села Боран, который является ключевым входным створом бассейна.""")

                # 1. Сначала подготавливаем все данные
                years = list(range(1940, 2025))
                data_rivers = {
                    "Год": years,
                    "р. Калжыр": [22.9, 36.0, 28.5, 21.5, 20.7, 11.6, 42.2, 29.8, 18.5, 21.1, 17.6, 8.1, 25.4, 17.7, 25.6, 19.5, 22.0, 23.0, 43.2, 28.1, 27.3, 23.6, 17.5, 10.0, 14.6, 10.9, 42.2, 13.7, 17.7, 38.7, 29.1, 32.9, 25.5, 22.7, 8.4, 13.2, 15.1, 17.7, 9.2, 20.2, 14.2, 15.8, 9.7, 20.6, 25.1, 29.0, 17.0, 22.6, 39.7, 19.2, 23.9, 18.6, 28.1, 37.2, 30.0, 24.4, 19.7, 22.6, 28.9, 24.5, 16.8, 37.9, 23.8, 16.0, 25.1, 24.3, 25.5, 26.3, 15.8, 27.9, 39.7, 15.7, 14.1, 21.7, 10.9, 12.9, 13.5, 15.5, 31.3, 25.8, 20.3, 19.2, 24.3, 11.6, 17.2],
                    "р. Куршим": [52.7, 87.6, 79.3, 66.2, 53.2, 34.1, 90.3, 98.9, 55.0, 60.7, 55.2, 26.4, 77.4, 49.6, 67.8, 49.3, 61.7, 72.4, 95.6, 57.6, 63.1, 67.5, 56.2, 38.5, 49.3, 42.2, 103.0, 40.6, 54.2, 94.6, 65.2, 77.8, 51.4, 69.5, 30.6, 47.1, 39.8, 50.8, 39.0, 70.3, 48.8, 44.6, 32.2, 53.8, 66.6, 63.5, 45.6, 57.4, 77.3, 45.7, 57.6, 44.6, 74.0, 82.2, 67.3, 56.1, 55.7, 60.1, 72.7, 64.0, 49.8, 93.3, 63.6, 40.0, 68.5, 64.5, 66.5, 68.0, 45.3, 71.6, 97.1, 45.2, 41.5, 137.0, 76.6, 92.3, 109.0, 86.0, 67.1, 59.1, 69.3, 69.6, 68.8, 56.5, 83.3],
                    "р. Буктырма": [241, 290, 239, 208, 215, 170, 376, 347, 235, 217, 257, 122, 259, 166, 227, 152, 205, 195, 299, 202, 271, 229, 156, 146, 178, 170, 272, 214, 152, 307, 231, 240, 212, 235, 117, 172, 170, 193, 158, 242, 167, 147, 134, 212, 235, 236, 212, 203, 234, 184, 223, 153, 240, 254, 230, 228, 199, 189, 196, 210, 206, 292, 251, 159, 206, 199, 207, 231, 155, 305, 293, 198, 182, 404, 297, 316, 321, 217, 218, 242, 208, 195, 189, 238, 276],
                    "р. Ульби": [84, 125, 97, 91, 87, 67, 160, 134, 98, 119, 89, 49, 104, 63, 135, 79, 101, 115, 160, 102, 131, 101, 72, 63, 84, 78, 149, 76, 82, 130, 107, 124, 108, 120, 56, 104, 104, 94, 79, 154, 76, 74, 67, 90, 74, 100, 74, 96, 100, 91, 124, 73, 119, 114, 106, 92, 77, 78, 86, 67, 69, 125, 118, 55, 93, 79, 88, 99, 69, 106, 109, 82, 55, 147, 94, 101, 119, 85, 76, 73, 66, 64, 67, 88, 88],
                    "р. Оба": [148, 209, 168, 158, 153, 124, 260, 222, 169, 200, 157, 98, 178, 118, 239, 122, 150, 184, 255, 169, 236, 207, 148, 128, 148, 147, 236, 113, 136, 212, 196, 219, 178, 246, 125, 196, 196, 199, 164, 250, 137, 123, 131, 154, 146, 194, 148, 212, 201, 199, 251, 142, 193, 208, 191, 182, 148, 140, 104, 103, 109, 187, 211, 117, 135, 133, 151, 175, 115, 174, 154, 114, 101, 252, 200, 197, 228, 180, 180, 149, 171, 123, 124, 154, 209]
                }
                df_local = pd.DataFrame(data_rivers)
                pritok_values = [327, 411, 425, 307, 267, 218, 458, 372, 239, 274, 283, 193, 388, 235, 322, 298, 347, 313, 466, 364, 354, 385, 267, 218, 262, 211, 446, 198, 298, 478, 374, 385, 305, 352, 143, 245, 214, 278, 166, 274, 224, 229, 134, 229, 373, 316, 206, 328, 420, 201, 283, 219, 293, 461, 383, 290, 234, 265, 293, 273, 238, 383, 309, 204, 272, 305, 268, 224, 175, 180, 353, 177, 145, 366, 236, 254, 346, 349, 327, 251, 242, 208, 182, 254, 369]

                # 2. Создаем объекты графиков
                fig_local = go.Figure()
                colors = ['#d3d3d3', '#e74c3c', '#f1c40f', '#8e44ad', '#6e4b3c']
                for i, col_name in enumerate(df_local.columns[1:]):
                    fig_local.add_trace(go.Scatter(
                        x=df_local['Год'], y=df_local[col_name],
                        mode='lines+markers', name=col_name,
                        line=dict(color=colors[i % len(colors)], width=1.2),
                        marker=dict(size=3)
                    ))
                fig_local.update_layout(height=400, template="plotly_white", margin=dict(l=0, r=0, t=10, b=0), legend=dict(orientation="h", y=-0.2))

                fig_pritok = go.Figure()
                fig_pritok.add_trace(go.Scatter(
                    x=years, y=pritok_values,
                    mode='lines+markers', name='Приток (р. Кара Ертис)',
                    line=dict(color='#3498db', width=2)
                ))
                fig_pritok.update_layout(height=400, template="plotly_white", margin=dict(l=0, r=0, t=10, b=0), legend=dict(orientation="h", y=-0.2))

                # 3. Отображаем графики в колонках
                g_col1, g_col2 = st.columns(2)

                with g_col1:
                    st.markdown("#### 🌊 Местный сток рек")
                    st.plotly_chart(fig_local, use_container_width=True, key=f"local_chart_{name}")
                    st.caption("Динамика годовых расходов воды по ключевым рекам ВХБ.")

                with g_col2:
                    st.markdown("#### 🌍 Приток (р. Кара Ертис)")
                    st.plotly_chart(fig_pritok, use_container_width=True, key=f"pritok_chart_{name}")
                    st.caption("Поступление водных ресурсов из КНР на гидропосту Боран.")


        
            




                    
                    





        
                    
                    
                    


    
        
        
        
        
        



with tabs[6]:
    st.title("Климат Казахстана и городов")



with tabs[7]:
    st.title("Экология городов")


   
st.markdown('<div style="text-align: center; margin-top: 40px; color: #94A3B8;">РГП «Казгидромет» | 2026</div>', unsafe_allow_html=True)