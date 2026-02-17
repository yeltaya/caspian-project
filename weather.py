import streamlit as st
import random
from datetime import datetime, timedelta

# 1. Настройка страницы
st.set_page_config(page_title="QazHydromet.Digital", page_icon="🌤️")

# 2. Единый визуальный стиль
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #002366; }
    h1, h2, h3, p, span { color: #002366 !important; font-family: 'Segoe UI', sans-serif; }
    
    .info-card { 
        background: #f0f4f8; 
        padding: 25px; 
        border-radius: 20px; 
        border: 1px solid #d1d9e6;
        box-shadow: 4px 4px 10px #e2e8f0;
        margin-bottom: 20px;
    }
    
    .coords { font-family: 'Courier New', monospace; font-size: 13px; color: #0056b3 !important; font-weight: bold; }
    .fact-text { font-size: 20px !important; font-weight: 600; line-height: 1.3; }
    
    /* Стили для таблицы прогноза */
    .forecast-item { text-align: center; padding: 10px; border-right: 1px solid #d1d9e6; }
    .forecast-item:last-child { border-right: none; }
    </style>
""", unsafe_allow_html=True)

# 3. Данные городов
city_data = {
    "Астана": {"temp": -15, "wind": 8, "station": "МС 35173", "lat": "51.1694", "lon": "71.4491"},
    "Алматы": {"temp": 5, "wind": 2, "station": "МС 36870", "lat": "43.2389", "lon": "76.8897"},
    "Шымкент": {"temp": 12, "wind": 4, "station": "МС 38198", "lat": "42.3249", "lon": "69.5973"},
    "Атырау": {"temp": 2, "wind": 12, "station": "МС 34691", "lat": "47.0945", "lon": "51.9238"},
    "Усть-Каменогорск": {"temp": -10, "wind": 3, "station": "МС 36307", "lat": "49.9482", "lon": "82.6285"}
}

facts = [
    "Самая низкая температура в Казахстане: −57.1°C (Атбасар).",
    "Казгидромет использует суперкомпьютеры для прогнозирования паводков.",
    "В Туркестане воздух прогревался до +49.1°C — это рекорд страны.",
    "Ежедневно метеозонды улетают на 30 км в стратосферу Казахстана.",
    "Казгидромет мониторит чистоту воздуха в 45 городах онлайн."
]

# 4. Сайдбар
with st.sidebar:
    st.header("⚙️ Управление стендом")
    selected_city = st.selectbox("Выбор города:", list(city_data.keys()))
    current_temp = st.slider("Температура сейчас", -50, 45, city_data[selected_city]["temp"])
    weather_type = st.radio("Состояние:", ["Ясно", "Снег", "Дождь", "Туман"])

# 5. Экран приложения
st.markdown("<h3 style='text-align: center; margin-bottom: 0;'>Aua Raıy Live</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; letter-spacing: 2px; font-size: 12px; margin-top:0;'>QAZHYDROMET.DIGITAL</p>", unsafe_allow_html=True)

# БЛОК 1: ТЕКУЩАЯ ПОГОДА
city_info = city_data[selected_city]
st.markdown(f"""
<div class="info-card">
    <p style="margin: 0; font-size: 11px; text-transform: uppercase; opacity: 0.6;">Данные МС: {city_info['station']}</p>
    <h1 style="font-size: 36px; margin-top: 5px;">{selected_city}</h1>
    <p class="coords">📍 {city_info['lat']}° N, {city_info['lon']}° E</p>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
        <span style="font-size: 70px; font-weight: 800;">{current_temp}°</span>
        <div style="text-align: right; font-size: 15px;">
            <p style="margin:0;">Небо: <b>{weather_type}</b></p>
            <p style="margin:0;">Обновлено: <b>{datetime.now().strftime('%H:%M')}</b></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# БЛОК 2: ПРОГНОЗ НА 3 ДНЯ (Динамический)
d1 = (datetime.now() + timedelta(days=1)).strftime('%d.%m')
d2 = (datetime.now() + timedelta(days=2)).strftime('%d.%m')
d3 = (datetime.now() + timedelta(days=3)).strftime('%d.%m')

st.markdown(f"""
<div class="info-card">
    <p style="text-transform: uppercase; font-size: 11px; letter-spacing: 1px; margin-bottom: 15px; font-weight: bold;">📅 Прогноз на 3 дня:</p>
    <div style="display: flex; justify-content: space-around;">
        <div class="forecast-item">
            <p style="margin:0; font-size: 12px; opacity:0.7;">{d1}</p>
            <p style="margin:5px 0; font-size: 20px;">☀️</p>
            <p style="margin:0; font-weight:bold;">{current_temp + 2}°</p>
        </div>
        <div class="forecast-item">
            <p style="margin:0; font-size: 12px; opacity:0.7;">{d2}</p>
            <p style="margin:5px 0; font-size: 20px;">☁️</p>
            <p style="margin:0; font-weight:bold;">{current_temp - 1}°</p>
        </div>
        <div class="forecast-item" style="border:none;">
            <p style="margin:0; font-size: 12px; opacity:0.7;">{d3}</p>
            <p style="margin:5px 0; font-size: 20px;">🌥️</p>
            <p style="margin:0; font-weight:bold;">{current_temp}°</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# БЛОК 3: ФАКТ
if 'fact' not in st.session_state:
    st.session_state.fact = random.choice(facts)

st.markdown(f"""
<div class="info-card" style="border-left: 8px solid #002366; background: #eef2f7;">
    <p style="text-transform: uppercase; font-size: 11px; letter-spacing: 1px; margin-bottom: 10px; font-weight: bold;">💡 Знаете ли вы?</p>
    <p class="fact-text">«{st.session_state.fact}»</p>
</div>
""", unsafe_allow_html=True)

if st.button("СЛЕДУЮЩИЙ ФАКТ"):
    st.session_state.fact = random.choice(facts)
    st.rerun()

# Анимации
if weather_type == "Снег": st.snow()
elif weather_type == "Дождь": st.balloons()