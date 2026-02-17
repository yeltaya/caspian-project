import streamlit as st
import random
from datetime import datetime, timedelta

# 1. Настройка
st.set_page_config(page_title="QazHydromet.Digital", page_icon="🌤️")

# 2. Стили (добавлены стили для вкладок и рекордов)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .brand-title { text-align: center; font-family: 'Segoe UI Black', sans-serif; font-size: 52px !important; line-height: 0.9; color: #002366; text-transform: uppercase; margin-bottom: 5px; }
    .brand-subtitle { text-align: center; font-family: 'Segoe UI', sans-serif; font-size: 16px !important; font-weight: 800; color: #002366; letter-spacing: 4px; margin-bottom: 20px; }
    
    .record-card {
        background: linear-gradient(135deg, #002366 0%, #0044bb 100%);
        color: white;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        text-align: center;
    }
    .record-value { font-size: 32px; font-weight: 900; margin: 5px 0; }
    .record-label { font-size: 14px; text-transform: uppercase; opacity: 0.8; letter-spacing: 1px; }
    
    .info-card { background: #f0f4f8; padding: 25px; border-radius: 25px; border: 2px solid #d1d9e6; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# 3. Брендинг (всегда сверху)
st.markdown('<p class="brand-title">Aua Raıy<br>Live</p>', unsafe_allow_html=True)
st.markdown('<p class="brand-subtitle">QAZHYDROMET.DIGITAL</p>', unsafe_allow_html=True)

# 4. СОЗДАНИЕ ВКЛАДОК
tab1, tab2 = st.tabs(["🌐 МОНИТОРИНГ", "🏆 РЕКОРДЫ КАЗАХСТАНА"])

with tab1:
    # Здесь остается ваш текущий код с городами, температурой и прогнозом
    st.info("Здесь отображается текущая погода и прогноз (ваш основной код)")

with tab2:
    st.markdown("### 🏛️ Цифровая выставка экстремумов")
    
    # Инфографика рекордов
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""<div class="record-card">
            <div class="record-label">Абсолютный минимум</div>
            <div class="record-value">$-57.1$ °C</div>
            <div style="font-size: 12px;">Атбасар (1893 г.)</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="record-card" style="background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);">
            <div class="record-label">Самый глубокий снег</div>
            <div class="record-value">155 см</div>
            <div style="font-size: 12px;">Риддер</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class="record-card" style="background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%);">
            <div class="record-label">Абсолютный максимум</div>
            <div class="record-value">$+49.1$ °C</div>
            <div style="font-size: 12px;">Туркестан</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="record-card" style="background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);">
            <div class="record-label">Сильнейший ветер</div>
            <div class="record-value">76 м/с</div>
            <div style="font-size: 12px;">Жаланашколь</div>
        </div>""", unsafe_allow_html=True)

    # Интерактив: Квиз
    st.markdown("---")
    st.subheader("🎯 Проверь свои знания")
    
    question = "В каком регионе Казахстана выпадает больше всего осадков?"
    options = ["Западно-Казахстанская", "Восточно-Казахстанская (Алтай)", "Туркестанская"]
    
    user_choice = st.radio(question, options)
    if st.button("Проверить ответ"):
        if user_choice == "Восточно-Казахстанская (Алтай)":
            st.success("Верно! В горах Алтая выпадает до 1600 мм осадков в год.")
        else:
            st.error("Не совсем. Правильный ответ: ВКО (Алтайские горы).")

    # Чек-лист
    with st.expander("💡 Как подготовиться к рекордам?"):
        st.write("""
        1. Проверяй мобильное приложение **Darmen**.
        2. Соблюдай принцип многослойности в одежде.
        3. Не выезжай на трассы при штормовом предупреждении.
        """)