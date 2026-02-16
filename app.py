
# 2. Улучшенная стилизация
import streamlit as st

# 1. Настройка страницы
st.set_page_config(
    page_title="Наблюдательная сеть РГП Казгидромет", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Улучшенная стилизация с "цифровыми" шрифтами
st.markdown("""
    <style>
    /* Подключаем цифровые и футуристичные шрифты */
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;600;800&family=Orbitron:wght@400;700;900&family=JetBrains+Mono:wght@700&family=Inter:wght@400;600&display=swap');

    /* Основной фон */
    .stApp { 
        background-color: #F8FAFC;
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Outline_Map_of_Kazakhstan.svg/1000px-Outline_Map_of_Kazakhstan.svg.png');
        background-repeat: no-repeat;
        background-position: center 200px;
        background-attachment: fixed;
        background-size: 55%; 
        font-family: 'Inter', sans-serif; /* Основной текст более читаемый */
    }
    
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(180deg, rgba(248,250,252,0.92) 0%, rgba(240,244,248,0.85) 100%);
        z-index: -1;
    }

    /* Заголовок в стиле Hi-Tech */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(180deg, #001f3f, #004A99);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 900;
        font-size: 4.8em;
        text-transform: uppercase;
        margin: 10px 0 40px 0;
        letter-spacing: 4px;
        filter: drop-shadow(0px 4px 2px rgba(0, 74, 153, 0.1));
    }

    /* Карточка мониторинга */
.monitor-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 24px;
        padding: 35px;
        /* ИЗМЕНЕНИЯ ТУТ: */
        height: auto;              /* Карточка сама подстраивается под текст */
        min-height: 480px;         /* Но не становится слишком маленькой (для симметрии) */
        display: flex;
        flex-direction: column;
        box-shadow: 0 15px 35px rgba(0, 74, 153, 0.1);
        transition: all 0.5s cubic-bezier(0.22, 1, 0.36, 1);
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;       /* Добавляем отступ снизу */
    }

/* Базовый hover для всех карточек */
    .monitor-card:hover {
        transform: translateY(-12px);
        background: rgba(255, 255, 255, 0.98);
        border-color: rgba(255, 255, 255, 0.5);
    }

    /* Метео - КРАСНОЕ свечение */
    .card-meteo:hover {
        box-shadow: 0 20px 40px rgba(231, 76, 60, 0.4);
        border-bottom: 4px solid #e74c3c;
    }

    /* Гидро - СИНЕЕ свечение */
    .card-hydro:hover {
        box-shadow: 0 20px 40px rgba(52, 152, 219, 0.4);
        border-bottom: 4px solid #3498db;
    }

    /* Агро - ЗЕЛЕНОЕ свечение */
    .card-agro:hover {
        box-shadow: 0 20px 40px rgba(46, 204, 113, 0.4);
        border-bottom: 4px solid #2ecc71;
    }

    /* Эко - СЕРОЕ свечение */
    .card-eco:hover {
        box-shadow: 0 20px 40px rgba(149, 165, 166, 0.4);
        border-bottom: 4px solid #95a5a6;
    }

    .card-header {
        font-family: 'Exo 2', sans-serif;
        color: #003366;
        font-weight: 800;
        font-size: 1.8em;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 25px;
        min-height: 70px;
    }

    /* Статистические значения (цифры) */
    .stat-val {
        font-family: 'JetBrains Mono', monospace;
        color: #0072FF;
        font-weight: 700;
        font-size: 1.4em;
        letter-spacing: -1px;
    }

    .total-label {
        font-family: 'Exo 2', sans-serif;
        font-weight: 600;
        font-size: 1.4em;
        color: #004A99;
        border-bottom: 2px solid #2ECC71;
        display: inline-block;
        margin-bottom: 20px;
    }

    /* Стилизация параметров внизу */
    .param-card {
        font-family: 'Exo 2', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        border: 2px solid rgba(0, 74, 153, 0.05);
    }
    
    /* Добавляем неоновое свечение при наведении на параметры */
    .param-card:hover {
        background: #004A99;
        box-shadow: 0 0 20px rgba(0, 114, 255, 0.6);
    }

    li {
        font-family: 'Inter', sans-serif;
        font-size: 1.1em;
        letter-spacing: 0.2px;
    }

/* Стили для информационных блоков */
    .info-section {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(0, 74, 153, 0.1);
        margin-top: 40px;
        color: #2D3436;
        line-height: 1.6;
    }
    .info-header {
        font-family: 'Exo 2', sans-serif;
        color: #003366;
        font-weight: 800;
        font-size: 1.4em;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }
    .data-point {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid #0072FF;
        font-size: 0.95em;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }


    </style>
    """, unsafe_allow_html=True)

# 3. Контент
st.markdown('<h1 class="main-title">📡 Мониторинг РГП "Казгидромет"</h1>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

cards_data = [
    {
        "title": "🌡️ Метеорологический мониторинг",
        "class": "card-meteo",  # НОВОЕ ПОЛЕ
        "total": "351 станция",
        "items": [
            ("225", "Традиционных"), ("126", "Автоматических"),
            ("43", "Актинометрических"), ("9", "Аэрологических"), ("5", "Озонометрических")
        ],
        "link": "http://10.0.2.121:8507/"
    },
    {
        "title": "💧 Гидрологический мониторинг",
        "class": "card-hydro",  # НОВОЕ ПОЛЕ
        "total": "442 поста",
        "items": [
            ("394", "Речных поста"), ("38", "Озерных постов"), ("10", "Морских станций")
        ],
        "link": "http://10.0.2.121:8507/"
    },
    {
        "title": "🌾 Агрометеорологический мониторинг",
        "class": "card-agro",   # НОВОЕ ПОЛЕ
        "total": "226 пунктов",
        "items": [
            ("129", "На метеостанциях"), ("97", "Агрометеопостов"),
            ("50", "Автоматических"), ("47", "Традиционных")
        ],
        "link": "http://10.0.2.121:8507/"
    },
    {
        "title": "🌱 Экологический мониторинг",
        "class": "card-eco",    # НОВОЕ ПОЛЕ
        "total": "175 постов",
        "items": [
            ("131", "Автоматических"), ("44", "Ручного отбора"),
            ("15", "Передвижных лабараторий"), ("70", "Населенных пунктов")
        ],
        "link": "http://10.0.2.121:8507/"
    }
]

cols = [col1, col2, col3, col4]

for i, card in enumerate(cards_data):
    with cols[i]:
        items_html = "".join([f'<li><span><span class="stat-val">{val}</span> {text}</span></li>' for val, text in card["items"]])
        st.markdown(f"""
            <a href="{card['link']}" target="_blank" style="text-decoration: none; color: inherit;">
                <div class="monitor-card {card['class']}">
                    <div class="card-header">{card['title']}</div>
                    <div class="accent-line"></div>
                    <p style="font-weight:700; font-size:1.3em; color:#004A99;">{card['total']}:</p>
                    <ul>
                        {items_html}
                    </ul>
                </div>
            </a>
        """, unsafe_allow_html=True)


# 2. Улучшенная стилизация
st.markdown("""
    <style>
    /* ... здесь ваши старые стили (main-title, monitor-card и т.д.) ... */

    /* ДОБАВЬТЕ ЭТО ВНУТРЬ ТЕГА <style> */
    
    /* Метео (Красное свечение) */
    .param-meteo:hover {
        border-color: #ff4b4b !important;
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.4) !important;
        background: rgba(255, 75, 75, 0.05) !important;
        transform: translateY(-5px);
    }

    /* Гидро (Синее свечение) */
    .param-hydro:hover {
        border-color: #0072FF !important;
        box-shadow: 0 0 20px rgba(0, 114, 255, 0.4) !important;
        background: rgba(0, 114, 255, 0.05) !important;
        transform: translateY(-5px);
    }

    /* Эко/Почва (Серое свечение) */
    .param-eco:hover {
        border-color: #95a5a6 !important;
        box-shadow: 0 0 20px rgba(149, 165, 166, 0.4) !important;
        background: rgba(149, 165, 166, 0.05) !important;
        transform: translateY(-5px);
    }
    
    /* Обязательно убедитесь, что основной класс тоже есть */
    .param-card {
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.1);
        border-radius: 15px;
        padding: 15px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: white;
    }
    </style>
""", unsafe_allow_html=True)


# --- Нижняя панель параметров ---
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
    <div style="background: linear-gradient(90deg, #003366, #004A99); color: white; text-align: center; 
                padding: 20px; border-radius: 20px; font-weight: 700; 
                font-size: 1.8em; text-transform: uppercase; margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,74,153,0.3);">
        🔎 Ключевые параметры наблюдения
    </div>
""", unsafe_allow_html=True)

params_cols = st.columns(8)
# Обновленный список: (Эмодзи, Название, CSS-класс)
params = [
    ("🌡️", "Температура воздуха", "param-meteo"), 
    ("⏲️", "Давление", "param-meteo"), 
    ("🌬️", "Скорость ветра", "param-meteo"), 
    ("❄️", "Высота снега", "param-meteo"), 
    ("🌧️", "Осадки", "param-meteo"), 
    ("☀️", "Радиация", "param-meteo"),
    ("🌊", "Уровень воды", "param-hydro"), 
    ("📉", "Расход воды", "param-hydro"), 
    ("🌡️💧", "Температура воды", "param-hydro"), 
    ("🧪", "Загрязнение воздуха", "param-eco"), 
    ("⚗️", "Качество почв", "param-eco"),
    ("⚠️", "Шторма", "param-meteo") # Добавил 12-й для ровной сетки
]

# Создаем 6 колонок
params_cols = st.columns(6) 

for i, (emoji, title, p_class) in enumerate(params):
    col_index = i % 6  
    
    with params_cols[col_index]:
        st.markdown(f"""
            <div class="param-card {p_class}" style="margin-bottom: 25px;">
                <div style="font-size: 2.2em; margin-bottom: 10px;">{emoji}</div>
                <div style="color: #004A99; font-weight: 700; font-size: 0.85em; text-transform: uppercase; line-height: 1.2;">
                    {title}
                </div>
            </div>
        """, unsafe_allow_html=True)


# --- ИНФОРМАЦИОННЫЙ БЛОК (Методология) ---
st.markdown("---") # Разделительная линия

st.markdown("""<h3 style='font-family: "Orbitron", sans-serif; text-align:center; color:#003366;'>📋 Регламент и объем мониторинга</h3>""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💧 Гидрология", "🌤️ Метео и Агро", "🌱 Экология"])

with tab1:
    st.markdown("""
    <div class="info-section">
        <div class="info-header">🌊 Регламент гидрологических наблюдений</div>
        <div class="info-grid">
            <div class="data-point"><b>Стандартный режим:</b> Наблюдения за уровнем, температурой воды и воздуха производятся ежедневно 2 раза в день.</div>
            <div class="data-point"><b>Замеры расходов:</b> Производятся подекадно, а в периоды половодья и паводков — в учащенном режиме.</div>
            <div class="data-point"><b>Зимний период:</b> Мониторинг ледовой обстановки, замеры толщины льда и высоты снега на льду.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="info-section">
        <div class="info-header">🛰️ Метеорологический и агрометео мониторинг</div>
        <p>Наблюдения проводятся в <b>8 основных синхронных сроков</b>. Характеристики:</p>
        <div class="info-grid">
            <div class="data-point">🌡️ Температура и влажность воздуха, давление, ветер.</div>
            <div class="data-point">🌍 Температура почвы (поверхность и глубины).</div>
            <div class="data-point">❄️ Снежный покров: высота, плотность, запас воды.</div>
            <div class="data-point">⛈️ Атмосферные явления (ОЯ и СГЯ), гололед, осадки.</div>
        </div>
        <p style="margin-top:20px;"><b>Агрометеопункты:</b> Дополнительно ведется мониторинг суммарной солнечной радиации и состояния сельскохозяйственных и пастбищных культур.</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="info-section">
        <div class="info-header">🔬 Экологический мониторинг РК</div>
        <div class="info-grid">
            <div class="data-point">🏙️ <b>Воздух:</b> 70 населенных пунктов, 175 постов, 15 лабораторий.</div>
            <div class="data-point">💧 <b>Вода:</b> 373 створа на 134 водных объектах.</div>
            <div class="data-point">☢️ <b>Радиация:</b> Гамма-фон на 89 станциях, бета-активность на 43.</div>
            <div class="data-point">🧪 <b>Почвы:</b> Качественное состояние в 101 точке наблюдения.</div>
            <div class="data-point">🌊 <b>Донные отложения:</b> Мониторинг на 32 объектах.</div>
            <div class="data-point">⚗️ <b>Аналитика:</b> 16 химико-аналитических лабораторий.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    
    # Футер / Подсказка
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; color: #636E72; font-size: 0.9em;">
        © {st.session_state.get('year', 2024)} РГП «Казгидромет» | Информационная панель мониторинга
    </div>
""", unsafe_allow_html=True)