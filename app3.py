import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np



# --- 1. КОНФИГУРАЦИЯ ЦВЕТОВ ---
DARK_BLUE = "#001F3F"
ACCENT_BLUE = "#0072FF"

# Настройка страницы
st.set_page_config(
    page_title='РГП "Казгидромет"', 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. ОБЪЕДИНЕННЫЙ CSS (Версия "Compact & Huge") ---
COMMON_CSS = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');

    /* 1. Убираем пустоту сверху от самого Streamlit */
    .block-container {{
        padding-top: 1rem !important; 
        padding-bottom: 0rem !important;
    }}

    .header-wrapper {{
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center;
        /* Резко уменьшаем внутренние отступы (было 80px) */
        padding: 20px 20px; 
        background-color: #FFFFFF; 
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03); 
        border: 1px solid #E2E8F0;
        /* Уменьшаем расстояние до вкладок снизу */
        margin-bottom: 20px; 
        /* Подтягиваем блок выше к краю браузера */
        margin-top: -10px;
        width: 100%;
    }}

    .header-main {{ 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        width: 100%;
        gap: 30px;
        /* Убираем нижний отступ, чтобы подзаголовок был ближе */
        margin-bottom: 5px; 
    }}

    .brand-title {{
        color: {DARK_BLUE} !important; 
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 900 !important;
        font-size: clamp(2.5rem, 8vw, 7rem) !important; 
        letter-spacing: 0.12em !important; 
        margin: 0 !important;
        text-transform: uppercase !important;
        line-height: 0.85 !important; /* Еще плотнее */
        display: inline-block;
    }}

    .glow-line {{
        width: 8vw; 
        max-width: 120px;
        height: 6px; 
        background-color: {ACCENT_BLUE};
        border-radius: 20px; 
        box-shadow: 0 0 20px {ACCENT_BLUE};
    }}

    .header-sub {{
        display: flex; 
        align-items: center; 
        justify-content: center; 
        gap: 20px; 
        margin-top: 10px; /* Минимальное расстояние от главного слова */
        color: #64748B;
        font-weight: 700; 
        font-size: clamp(0.6rem, 1vw, 0.9rem);
        letter-spacing: 3px; 
        text-transform: uppercase;
    }}
    /* Стилизация вкладок (Tabs) */
        button[data-baseweb="tab"] {{
            border-radius: 12px 12px 0 0 !important;
            margin: 0 5px !important;
            padding: 10px 20px !important;
            background-color: #f1f5f9 !important; /* Легкий фон для неактивных вкладок */
            transition: all 0.3s ease !important;
        }}

        button[data-baseweb="tab"] p {{
            font-size: 1.3rem !important; /* Увеличиваем размер шрифта */
            font-weight: 600 !important;   /* Делаем текст полужирным */
            color: #475569 !important;     /* Цвет текста */
        }}

        /* Стиль для активной (выбранной) вкладки */
        button[aria-selected="true"] {{
            background-color: #FFFFFF !important;
            box-shadow: 0 -4px 15px rgba(0,0,0,0.05) !important;
        }}

        button[aria-selected="true"] p {{
            color: {ACCENT_BLUE} !important; /* Активная вкладка будет вашего акцентного цвета */
            font-weight: 800 !important;
        }}
            /* Увеличение основного текста внутри вкладок */
        .stMarkdown p, .stMarkdown li {{
            font-size: 1.2rem !important; /* Увеличили размер обычного текста */
            line-height: 1.6 !important;  /* Увеличили межстрочный интервал для читаемости */
            color: #1E293B !important;
        }}

        /* Увеличение жирного текста (названия станций, цифры) */
        .stMarkdown b, .stMarkdown strong {{
            font-size: 1.25rem !important;
            color: {ACCENT_BLUE} !important; /* Делаем важные цифры акцентными */
        }}

        /* Если вы используете st.write или специфические контейнеры */
        [data-testid="stWidgetLabel"] p {{
            font-size: 1.2rem !important;
        }}
        /* 5. УВЕЛИЧЕННЫЕ ЗАГОЛОВКИ РАЗДЕЛОВ (География, История и т.д.) */
        .stMarkdown h1 {{
            font-size: 3rem !important;
            color: {DARK_BLUE} !important;
            font-weight: 800 !important;
            margin-bottom: 20px !important;
        }}

        .stMarkdown h2 {{
            font-size: 2.2rem !important; /* "География", "История" и т.д. */
            color: {DARK_BLUE} !important;
            border-bottom: 3px solid {ACCENT_BLUE};
            padding-bottom: 10px !important;
            margin-top: 30px !important;
            font-weight: 700 !important;
        }}

        .stMarkdown h3 {{
            font-size: 1.8rem !important;
            color: {ACCENT_BLUE} !important;
            font-weight: 600 !important;
        }}

        /* Увеличение текста в специальных блоках (инфо-боксы) */
        .info-box {{
            font-size: 1.25rem !important;
            padding: 20px !important;
        }}
    /* Стили для названий блоков (География, История и т.д.) */
    .section-header {{
        font-size: 2.8rem !important;
        font-weight: 850 !important;
        color: {DARK_BLUE} !important;
        border-left: 10px solid {ACCENT_BLUE};
        padding-left: 20px !important;
        margin-top: 40px !important;
        margin-bottom: 25px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    /* Блок общего количества постов */
    .total-posts-banner {{
        background: linear-gradient(90deg, {DARK_BLUE} 0%, {ACCENT_BLUE} 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 10px 20px rgba(0,114,255,0.2);
    }}
    .total-posts-count {{
        font-size: 4rem !important;
        font-weight: 900;
        line-height: 1;
        display: block;
    }}
    .total-posts-label {{
        font-size: 1.5rem;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 5px;
    }}

    /* Стили для видов постов (Выравнивание цифр и текста) */
    .post-type-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 15px 25px;
        background: white;
        border-radius: 15px;
        margin-bottom: 12px;
        border: 1px solid #E2E8F0;
        transition: transform 0.2s;
    }}
    .post-type-row:hover {{
        transform: translateX(10px);
        border-color: {ACCENT_BLUE};
    }}
    .post-label {{
        font-size: 1.3rem !important;
        font-weight: 600;
        color: #475569;
    }}
    .post-value {{
        font-size: 1.8rem !important;
        font-weight: 900;
        color: {ACCENT_BLUE};
        font-family: 'Montserrat', sans-serif;
    }}
    
    .sub-divider {{ width: 2px; height: 18px; background-color: #CBD5E1; }}

    /* Убираем стандартный отступ у заголовков в Streamlit */
    div[data-testid="stVerticalBlock"] > div:has(div.header-wrapper) {{
        gap: 0 !important;
    }}
            /* Карточка с эффектом стекла */
    .monitor-card {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 24px;
        padding: 25px;
        min-height: 380px;
        display: flex;
        flex-direction: column;
        box-shadow: 0 10px 30px rgba(0, 74, 153, 0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid #e3f2fd;
    }}

        .monitor-card:hover {{
            transform: translateY(-12px);
            box-shadow: 0 20px 40px rgba(0, 74, 153, 0.15);
        }}

        .card-header-text {{
            font-family: 'Exo 2', sans-serif;
            color: #003366;
            font-weight: 800;
            font-size: 1.4em;
            margin-bottom: 15px;
            border-bottom: 2px solid #0072FF;
            padding-bottom: 10px;
        }}

        .stat-val {{
            font-family: 'JetBrains Mono', monospace;
            color: #0072FF;
            font-weight: 800;
            font-size: 1.2em;
        }}

   
    </style>
"""

st.markdown(COMMON_CSS, unsafe_allow_html=True)

# --- 3. ШАПКА (HTML) ---
st.markdown(f"""
    <div class="header-wrapper">
        <div class="header-main">
            <div class="glow-line"></div>
            <h1 class="brand-title">KAZHYDROMET</h1>
            <div class="glow-line"></div>
        </div>
        <div class="header-sub">
            <div>NATIONAL HYDROMETEOROLOGICAL SERVICE</div>
            <div class="sub-divider"></div>
            <div>НАЦИОНАЛЬНАЯ ГИДРОМЕТЕОРОЛОГИЧЕСКАЯ СЛУЖБА</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 1. Сначала выбор языка (сверху)
col_l, col_r = st.columns([4, 1])
with col_r:
    lang = st.selectbox("Язык", ["Русский", "Қазақша", "English"], label_visibility="collapsed")
    
lang_map = {
    "Русский": "ru",
    "Қазақша": "kz",
    "English": "en"
}
lang_code = lang_map.get(lang, "ru")
    

# 2. Определяем словари названий
tabs_ru = ["🔍 Обзор", "📊 Мониторинг", "🌤️ Прогноз погоды", "🌾 Агрометео", "📈 Гидропрогнозы", "💧 Водные ресурсы", "🌊 Каспийское море", "🇰🇿 Климат", "🏭 Экология", "🌐 Сотрудничество"]
tabs_kk = ["🔍 Шолу", "📊 Мониторинг", "🌤️ Ауа райы болжамы", "🌾 Агрометео", "📈 Гидроболжамдар", "💧 Су ресурстары", "🌊 Каспий теңізі", "🇰🇿 Климат", "🏭 Экология", "🌐 Ынтымақтастық"]
tabs_en = ["🔍 Overview", "📊 Monitoring", "🌤️ Weather Forecast", "🌾 Agrometeo", "📈 Hydro-forecasts", "💧 Water Resources", "🌊 Caspian Sea", "🇰🇿 Climate", "🏭 Ecology", "🌐 Cooperation"]

# 3. ВЫБИРАЕМ активный список в зависимости от языка
if lang == "Русский":
    current_tabs = tabs_ru
elif lang == "Қазақша":
    current_tabs = tabs_kk
else:
    current_tabs = tabs_en

# 4. СОЗДАЕМ вкладки (теперь переменная tabs существует!)
tabs = st.tabs(current_tabs)

# 5. НАПОЛНЯЕМ вкладки
with tabs[0]: # ОБЗОР
    def show_top_banner():
        col_logo, col_main = st.columns([0.5, 1])
        with col_logo:
            try:
                st.image("КГМ.png", width=200)
            except:
                st.error("Логотип 'КГМ.png' не найден")

        with col_main:
            # Здесь текст тоже нужно перевести
            if lang == "Русский":
                text = "С опорой на 100-летнюю историю государственной системы наблюдений и современные технологии мы обеспечиваем точные, верифицированные данные для стратегических решений и экологической безопасности.  "
            elif lang == "Қазақша":
                text = "Мемлекеттік бақылау жүйесінің 100 жылдық тарихына және заманауи технологияларға сүйене отырып, біз стратегиялық шешімдер мен экологиялық қауіпсіздік үшін нақты, тексерілген деректерді қамтамасыз етеміз."
            else:
                text = "Building on a 100-year history of the state observation system and leveraging modern technologies, we provide accurate, verified data for strategic decision-making and environmental security."

            st.markdown(f"""
                <div style="border-left: 5px solid #004a99; padding-left: 20px; margin-top: 10px;">
                    <p style="font-size: 1.5rem; color: #1a202c; line-height: 1.3; margin: 0;">
                        <b style="color: #003366;">{text}</b>         
                    </p>
                </div>
                """, unsafe_allow_html=True) 
    
    show_top_banner()
    st.markdown("---")
    
    
    # --- СЕКЦИЯ 2: МАСШТАБ ИНФРАСТРУКТУРЫ ---

    if lang == "Русский":
        header_2 = "📊 Государственная наблюдательная сеть"
        m1_l, m1_v, m1_d = "Мониторинг", "1800+ станций и пунктов", "непрерывно"
        m2_l, m2_v, m2_d = "История", "175+ лет наблюдений", "24/7"
        m3_l, m3_v, m3_d = "География", "17 филиалов", "весь Казахстан"
        m4_l, m4_v, m4_d = "Глобальный обмен", "ВМО (WMO)", "с 1993 года"

    elif lang == "Қазақша":
        header_2 = "📊 Мемлекеттік бақылау желісі"
        m1_l, m1_v, m1_d = "Мониторинг", "1800+ станция мен пункт", "үздіксіз"
        m2_l, m2_v, m2_d = "Тарих", "175+ жыл бақылау", "24/7"
        m3_l, m3_v, m3_d = "География", "17 филиал", "бүкіл Қазақстан"
        m4_l, m4_v, m4_d = "Жаһандық алмасу", "ДМҰ (WMO)", "1993 жылдан"

    else: # English
        header_2 = "📊 State Observation Network"
        m1_l, m1_v, m1_d = "Monitoring", "1800+ stations & points", "continuous"
        m2_l, m2_v, m2_d = "History", "175+ years of records", "24/7"
        m3_l, m3_v, m3_d = "Geography", "17 branches", "all Kazakhstan"
        m4_l, m4_v, m4_d = "Global Exchange", "WMO", "since 1993"

    st.subheader(header_2)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(m1_l, m1_v, m1_d)
    m2.metric(m2_l, m2_v, m2_d)
    m3.metric(m3_l, m3_v, m3_d)
    m4.metric(m4_l, m4_v, m4_d)



    import streamlit as st
    import pandas as pd
    import folium
    from streamlit_folium import st_folium
    import re

    # Функция конвертации координат
    def dms_to_decimal(dms_str):
        try:
            if pd.isna(dms_str) or str(dms_str).strip() == "": return None
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", str(dms_str))
            if len(numbers) >= 3:
                deg, mn, sec = map(float, numbers[:3])
                return deg + mn/60 + sec/3600
            elif len(numbers) == 1:
                return float(numbers[0])
            return None
        except:
            return None

    def show_dashboard():
        try:
            # Загрузка данных
            df = pd.read_excel("station.xlsx")
            df.columns = df.columns.str.strip()
            df['lat'] = df['широта'].apply(dms_to_decimal)
            df['long'] = df['долгота'].apply(dms_to_decimal)
            df = df.dropna(subset=['lat', 'long'])

            # Создаем две колонки: 70% для карты, 30% для инфо
            col_map, col_info = st.columns([2.5, 1], gap="medium")

            with col_map:
                st.markdown("#### 🗺️ Интерактивная карта сети")
                
                # Цветовая схема
                color_map = {
                    "Гидрология": "#0066CC",
                    "Метеорология": "#FF9900",
                    "Экология": "#CC0000",
                    "Агрометеорология": "#2E7D32"
                }

                m = folium.Map(location=[48.0, 67.0], zoom_start=5, tiles="cartodbpositron")

                for _, row in df.iterrows():
                    icon_color = color_map.get(row['Направление'], '#666666')
                    folium.CircleMarker(
                        location=[row['lat'], row['long']],
                        radius=5,
                        popup=f"<b>{row['Станция/пост']}</b><br>{row['Направление']}",
                        color=icon_color,
                        fill=True,
                        fill_color=icon_color,
                        fill_opacity=0.7,
                        weight=1
                    ).add_to(m)

                st_folium(m, width="100%", height=650, returned_objects=[])

            with col_info:
                st.markdown("####")
                
                # 1. Ваши эталонные данные
                stats_data = {
                    "Метеорология": 365,
                    "Гидрология": 442,
                    "Агрометеорология": 226,
                    "Экология": 790
                }
                
                # 2. Локальный словарь названий и подписей
                if lang == "Қазақша":
                    names = {"Метеорология": "Метеорология", "Гидрология": "Гидрология", "Агрометеорология": "Агрометеорология", "Экология": "Экология"}
                    unit_text = "станция/бекет"
                elif lang == "English":
                    names = {"Метеорология": "Meteorology", "Гидрология": "Hydrology", "Агрометеорология": "Agrometeorology", "Экология": "Ecology"}
                    unit_text = "stations/posts"
                else: # Русский
                    names = {k: k for k in stats_data.keys()} # Оставляем как есть
                    unit_text = "станции/постов"

                # 3. Отрисовка карточек
                for navr, count in stats_data.items():
                    # Подбор эмодзи
                    if "Гидр" in navr: emoji, color = "💧", "#0066CC"
                    elif "Мет" in navr: emoji, color = "🌤️", "#FF9900"
                    elif "Агр" in navr: emoji, color = "🌱", "#2E7D32"
                    else: emoji, color = "🧪", "#CC0000"
                    
                    # Берем переведенное имя из словаря names
                    display_name = names.get(navr, navr)

                    st.markdown(f"""
                        <div style="
                            background-color: #f8fafc; 
                            padding: 15px; 
                            border-radius: 10px; 
                            border-left: 6px solid {color}; 
                            margin-bottom: 12px; 
                            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                        ">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 1.1rem; font-weight: 700; color: #334e68; white-space: nowrap;">
                                    {emoji} {display_name}
                                </span>
                                <span style="font-size: 2.2rem; font-weight: 900; color: {color}; line-height: 1;">
                                    {count}
                                </span>
                            </div>
                            <div style="text-align: right; font-size: 0.9rem; color: #666; margin-top: 2px;">
                                {unit_text}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        
                

        except Exception as e:
            st.error(f"Ошибка: {e}. Убедитесь, что файл station.xlsx в порядке.")

    show_dashboard()

    def show_economic_info(lang):
        # 1. Словарь переводов заголовка
        titles = {
            "Русский": "Обеспечение гидрометеорологической и экологической информацией отраслей экономики",
            "Қазақша": "Экономика салаларын гидрометеорологиялық және экологиялық ақпаратпен қамтамасыз ету",
            "English": "Providing Hydrometeorological and Environmental Information to Economic Sectors"
        }
        
        current_title = titles.get(lang, titles["Русский"])

        # Вывод заголовка
        st.markdown(f"""
            <h2 style='text-align: center; color: #003366; margin-bottom: 40px;'>
                {current_title}
            </h2>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 2. Стили CSS
        st.markdown("""
            <style>
            .forecast-card {
                background: #f8fafc;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                text-align: center;
                transition: all 0.3s ease;
                min-height: 250px;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
            }
            .forecast-card:hover {
                border-color: #3b82f6;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                background: #ffffff;
            }
            .forecast-card .icon { font-size: 3rem; margin-bottom: 12px; }
            .forecast-card .title { color: #1e293b; font-weight: 700; font-size: 1.1rem; margin-bottom: 8px; line-height: 1.2; }
            .forecast-card .description { color: #64748b; font-size: 0.95rem; line-height: 1.4; }
            </style>
        """, unsafe_allow_html=True)

        # 3. Данные для карточек
        forecast_translations = {
            "Русский": [
                {"icon": "⚡", "title": "Наукастинг<br>(2-6 часов)", "desc": "Сверхкраткосрочный прогноз погоды."},
                {"icon": "📅", "title": "Краткосрочный прогноз", "desc": "Прогноз погоды от 1 до 7 дней."},
                {"icon": "🔭", "title": "Долгосрочный прогноз", "desc": "Прогноз погоды от 10 дней до сезонов."},
                {"icon": "🏔️", "title": "Специализированный прогноз", "desc": "Прогноз условий для туризма, гор и пожарной опасности."},
                {"icon": "⚠️", "title": "Штормовые предупреждения", "desc": "Об опасных явлениях."}
            ],
            "Қазақша": [
                {"icon": "⚡", "title": "Наукастинг<br>(2-6 сағат)", "desc": "Аса қысқа мерзімді ауа райы болжамы."},
                {"icon": "📅", "title": "Қысқа мерзімді болжам", "desc": "1-ден 7 күнге дейінгі ауа райы болжамы."},
                {"icon": "🔭", "title": "Ұзақ мерзімді болжам", "desc": "10 күннен маусымдарға дейінгі ауа райы болжамы."},
                {"icon": "🏔️", "title": "Мамандандырылған болжам", "desc": "Туристік маршруттар, таулы аймақтар мен өрт қаупі бойынша болжам."},
                {"icon": "⚠️", "title": "Дауылды ескертулер", "desc": "Қауіпті құбылыстар туралы."}
            ],
            "English": [
                {"icon": "⚡", "title": "Nowcasting<br>(2-6 hours)", "desc": "Very short-range weather forecast."},
                {"icon": "📅", "title": "Short-range forecast", "desc": "Weather forecast from 1 to 7 days."},
                {"icon": "🔭", "title": "Long-range forecast", "desc": "Weather forecast from 10 days up to seasons."},
                {"icon": "🏔️", "title": "Specialized forecast", "desc": "Forecast for tourist routes, mountain areas, and fire hazards."},
                {"icon": "⚠️", "title": "Storm warnings", "desc": "On hazardous phenomena."}
            ]
        }

        current_forecasts = forecast_translations.get(lang, forecast_translations["Русский"])

        # 4. Отрисовка колонок (ВНИМАНИЕ НА ОТСТУПЫ ЗДЕСЬ)
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                item = current_forecasts[i]
                st.markdown(f"""
                    <div class="forecast-card">
                        <div class="icon">{item['icon']}</div>
                        <div class="title">{item['title']}</div>
                        <div class="description">{item['desc']}</div>
                    </div>
                """, unsafe_allow_html=True)

    # 5. Вызов функции (вне самой функции, без отступа)
    show_economic_info(lang)
    st.markdown("---")

        
# --- ИНФОРМАЦИОННЫЙ БЛОК О ПРОГНОЗЕ 2 КМ ---

    if lang == "Русский":
        promo_title = "📡 Казгидромет внедряет прогноз погоды с высоким разрешением 2 км —"
        promo_accent = "технологический прорыв, уникальный для Центральной Азии."
        promo_text = """Обеспечивая беспрецедентную точность прогнозов, критически важную для раннего предупреждения 
                        природных рисков, укрепления климатической и экологической безопасности на национальном 
                        и региональном уровнях."""
    elif lang == "Қазақша":
        promo_title = "📡 Қазгидромет 2 км жоғары ажыратымдылықтағы ауа райы болжамын енгізуде —"
        promo_accent = "Орталық Азиядағы бірегей технологиялық серпіліс."
        promo_text = """Болжамдардың теңдессіз дәлдігін қамтамасыз ете отырып, бұл табиғи қауіп-қатерлерді ерте ескерту, 
                        ұлттық және аймақтық деңгейде климаттық және экологиялық қауіпсіздікті нығайту үшін өте маңызды."""
    else: # English
        promo_title = "📡 Kazhydromet implements high-resolution 2 km weather forecasting —"
        promo_accent = "a technological breakthrough unique to Central Asia."
        promo_text = """Providing unprecedented forecasting accuracy, which is critical for early warning 
                        of natural hazards and strengthening climate and environmental security at both 
                        national and regional levels."""

    st.markdown(
        f"""
        <div style="background-color: #f0f7ff; padding: 25px; border-left: 5px solid #003366; border-radius: 10px; margin: 20px 0;">
            <h4 style="color: #003366; margin-bottom: 10px; font-weight: bold;">
                {promo_title} 
                <span style="color: #0066cc;">{promo_accent}</span>
            </h4>
            <p style="color: #334155; font-size: 1.1rem; line-height: 1.6; margin: 0;">
                {promo_text}
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("---")

        # --- CSS ДЛЯ КАРТОЧЕК ---
    st.markdown("""
            <style>
                .data-box {
                    padding: 15px;
                    border-radius: 0 0 12px 12px; /* Скругляем только низ, так как сверху картинка */
                    border-left: 5px solid;
                    background: #ffffff;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                    min-height: 280px;
                    margin-bottom: 20px;
                }
                .data-title {
                    font-weight: bold;
                    font-size: 1.1em;
                    margin-bottom: 10px;
                    color: #1f2937;
                }
                .data-list {
                    font-size: 0.9em;
                    padding-left: 20px;
                    color: #4b5563;
                }
                .card-img {
                    width: 100%;
                    height: 150px;
                    object-fit: cover;
                    border-radius: 12px 12px 0 0; /* Скругляем верх картинки */
                }
            </style>
        """, unsafe_allow_html=True)

    import os
    import streamlit as st

    # 1. ПУТИ К ФАЙЛАМ
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMG_DIR = BASE_DIR # Указывает на папку со скриптом

    # 2. ДАННЫЕ ДЛЯ КАРТОЧЕК (Три языка)
    data_content = {
        "Русский": [
            {
                "title": "📍 Наземная сеть",
                "file": "precipitation.gif",
                "color": "#3b82f6",
                "items": [
                    "<b>МС:</b> Непрерывный мониторинг параметров 24/7.",
                    "<b>Аэрология:</b> Зондирование атмосферы до 30 км.",
                    "<b>ДМРЛ:</b> Локаторы для детекции града и шквалов."
                ]
            },
            {
                "title": "🗺️ Аналитика",
                "file": "station2.gif",
                "color": "#10b981",
                "items": [
                    "<b>АРМ ГИС-Метео, Metcap+:</b> Построение синоптических карт.",
                    "<b>ГСТ ВМО:</b> Обмен данными.",
                    "<b>Сетки:</b> Анализ полей метеопараметров."
                ]
            },
            {
                "title": "📡 Спутники",
                "file": "station3.gif",
                "color": "#8b5cf6",
                "items": [
                    "<b>EUMETSAT:</b> Европейские геостационары.",
                    "<b>FengYun:</b> Оперативные данные из КНР.",
                    "<b>Метеор-М:</b> Российские орбитальные системы."
                ]
            },
            {
                "title": "⚙️ Численные модели",
                "file": "station4.gif",
                "color": "#f59e0b",
                "items": [
                    "<b>ECMWF:</b> Глобальные прогнозы до 9 км.",
                    "<b>ICON, COSMO:</b> Высокоточные мезомасштабные модели.",
                    "<b>WRF-Kaz:</b> Локальная модель Казгидромет."
                ]
            }
        ],
        "Қазақша": [
            {
                "title": "📍 Жерүсті желісі",
                "file": "precipitation.gif",
                "color": "#3b82f6",
                "items": [
                    "<b>МС:</b> Параметрлерді 24/7 үздіксіз мониторингілеу.",
                    "<b>Аэрология:</b> Атмосфераны 30 км-ге дейін зондтау.",
                    "<b>ДМРЛ:</b> Бұршақ пен дауылды анықтауға арналған локаторлар."
                ]
            },
            {
                "title": "🗺️ Аналитика",
                "file": "station2.gif",
                "color": "#10b981",
                "items": [
                    "<b>АРМ ГИС-Метео, Metcap+:</b> Синоптикалық карталарды құру.",
                    "<b>ГСТ ДМҰ:</b> Мәліметтер алмасу.",
                    "<b>Торлар:</b> Метеопараметрлер өрістерін талдау."
                ]
            },
            {
                "title": "📡 Жерсеріктер",
                "file": "station3.gif",
                "color": "#8b5cf6",
                "items": [
                    "<b>EUMETSAT:</b> Еуропалық геостационарлар.",
                    "<b>FengYun:</b> ҚХР-дан жедел деректер.",
                    "<b>Метеор-М:</b> Ресейлік орбиталық жүйелер."
                ]
            },
            {
                "title": "⚙️ Сандық модельдер",
                "file": "station4.gif",
                "color": "#f59e0b",
                "items": [
                    "<b>ECMWF:</b> 9 км-ге дейінгі жаһандық болжамдар.",
                    "<b>ICON, COSMO:</b> Жоғары дәлдіктегі мезомасштабты модельдер.",
                    "<b>WRF-Kaz:</b> Қазгидрометтің жергілікті моделі."
                ]
            }
        ],
        "English": [
            {
                "title": "📍 Ground Network",
                "file": "precipitation.gif",
                "color": "#3b82f6",
                "items": [
                    "<b>MS:</b> Continuous 24/7 monitoring of parameters.",
                    "<b>Aerology:</b> Atmospheric sounding up to 30 km.",
                    "<b>DWR:</b> Radars for hail and squall detection."
                ]
            },
            {
                "title": "🗺️ Analytics",
                "file": "station2.gif",
                "color": "#10b981",
                "items": [
                    "<b>AWS GIS-Meteo, Metcap+:</b> Synoptic chart generation.",
                    "<b>WMO GTS:</b> Data exchange.",
                    "<b>Grids:</b> Analysis of meteorological fields."
                ]
            },
            {
                "title": "📡 Satellites",
                "file": "station3.gif",
                "color": "#8b5cf6",
                "items": [
                    "<b>EUMETSAT:</b> European geostationary satellites.",
                    "<b>FengYun:</b> Operational data from China.",
                    "<b>Meteor-M:</b> Russian orbital systems."
                ]
            },
            {
                "title": "⚙️ Numerical Models",
                "file": "station4.gif",
                "color": "#f59e0b",
                "items": [
                    "<b>ECMWF:</b> Global forecasts up to 9 km.",
                    "<b>ICON, COSMO:</b> High-precision mesoscale models.",
                    "<b>WRF-Kaz:</b> Kazhydromet local model."
                ]
            }
        ]
    }

    # 3. ФУНКЦИЯ ДЛЯ ОТРИСОВКИ
    def draw_data_card(col, file_name, title, color, items):
        path = os.path.join(IMG_DIR, file_name)
        with col:
            if os.path.exists(path):
                st.image(path, use_container_width=True)
            else:
                st.warning(f"Файл {file_name} не найден")
            
            list_html = "".join([f"<li>{item}</li>" for item in items])
            st.markdown(f"""
                <div class="data-box" style="border-left-color: {color};">
                    <div class="data-title">{title}</div>
                    <ul class="data-list">
                        {list_html}
                    </ul>
                </div>
            """, unsafe_allow_html=True)

    # 4. CSS СТИЛИ
    st.markdown("""
        <style>
            .data-box {
                padding: 15px;
                border-radius: 0 0 12px 12px;
                border-left: 5px solid;
                background: #ffffff;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                min-height: 280px;
                margin-bottom: 20px;
            }
            .data-title { font-weight: bold; font-size: 1.1em; margin-bottom: 10px; color: #1f2937; }
            .data-list { font-size: 0.85em; padding-left: 20px; color: #4b5563; line-height: 1.4; }
            .data-list b { color: #1f2937; }
        </style>
    """, unsafe_allow_html=True)

    # 5. ОТОБРАЖЕНИЕ КАРТОЧЕК
    st.markdown('<div class="tab-specific-container">', unsafe_allow_html=True)

    # Получаем данные на основе текущего языка (lang)
    current_data = data_content.get(lang, data_content["Русский"])

    cols = st.columns(4)
    for i, col in enumerate(cols):
        card = current_data[i]
        draw_data_card(
            col, 
            card["file"], 
            card["title"], 
            card["color"], 
            card["items"]
        )
        
    
# Разделитель перед текстом о Казгидромете
    st.markdown("---")    
    

    import os
    import streamlit as st
    import pandas as pd

    def show_monitoring_block(lang):
        # 1. Определяем пути ВНУТРИ функции
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        path_risk = os.path.join(BASE_DIR, "risk.jpeg")
        path_hydro = os.path.join(BASE_DIR, "hydro.png")
        path_agro = os.path.join(BASE_DIR, "AGRO.jpg")
        path_agro1 = os.path.join(BASE_DIR, "agro1.jpg")

        # СЛОВАРЬ ПЕРЕВОДОВ
        translations = {
            "Русский": {
                "hydro_sub": "💧 Гидрологические прогнозы",
                "hydro_title": "#### Водная безопасность Казахстана",
                "hydro_list": """
                * 🌊 **Мониторинг рек** – равнинные и горные
                * ⚠️ **Оценка паводков** и притока к водохранилищам
                * 💧 **Моделирование стока** в реальном времени
                * 🌪 **Прогноз опасных явлений** – наводнения, ледоходы, оползни
                * 🛡 **Стратегическая поддержка** – управление ресурсами и экстренными службами
                """,
                "hydro_cap1": "Карта рисков паводков в 2026 г.",
                "hydro_cap2": "Интерактивная карта гидрологического мониторинга",
                "agro_sub": "🌾 Агрометеорологические прогнозы",
                "agro_mon": "**🔍 Мониторинг**",
                "agro_mon_list": """
                * 📉 **Прогноз запасов влаги** в почве
                * 🌽 **Фенологический мониторинг** культур
                * 🌡️ **Оценка рисков заморозков** и засухи
                * 🚜 **Рекомендации** для проведения посевных работ
                """,
                "agro_plat": "**📱 Платформа AGRODATA.kz**",
                "agro_plat_text": """
                Интерактивный агрометеорологический портал, предоставляющий фермерам:
                * Высокоточные прогнозы погоды для сельхозугодий.
                * Карты фактических запасов продуктивной влаги в почве.
                * Рекомендации по срокам посева и внесения удобрений.
                """,
                "agro_cap1": "Пункты агрометеорологического наблюдения",
                "agro_cap2": "Сроки сева зерновых культур"
            },
            "Қазақша": {
                "hydro_sub": "💧 Гидрологиялық болжамдар",
                "hydro_title": "#### Қазақстанның су қауіпсіздігі",
                "hydro_list": """
                * 🌊 **Өзендер мониторингі** – жазық және таулы
                * ⚠️ **Су тасқынын бағалау** және су қоймаларына келетін су ағыны
                * 💧 **Ағындыны нақты уақытта модельдеу**
                * 🌪 **Қауіпті құбылыстарды болжау** – су тасқыны, мұз жүру, көшкін
                * 🛡 **Стратегиялық қолдау** – ресурстарды басқару және төтенше қызметтер
                """,
                "hydro_cap1": "2026 жылғы су тасқыны қаупінің картасы",
                "hydro_cap2": "Гидрологиялық мониторингтің интерактивті картасы",
                "agro_sub": "🌾 Агрометеорологиялық болжамдар",
                "agro_mon": "**🔍 Мониторинг**",
                "agro_mon_list": """
                * 📉 **Топырақтағы ылғал қорын болжау**
                * 🌽 **Дақылдардың фенологиялық мониторингі**
                * 🌡️ **Үсік жүру және құрғақшылық қаупін бағалау**
                * 🚜 **Егіс жұмыстарын жүргізуге арналған ұсынымдар**
                """,
                "agro_plat": "**📱 AGRODATA.kz платформасы**",
                "agro_plat_text": """
                Фермерлерге арналған интерактивті агрометеорологиялық портал:
                * Ауыл шаруашылығы жерлеріне арналған жоғары дәлдіктегі ауа райы болжамдары.
                * Топырақтың өнімді ылғалдылығының нақты қорының карталары.
                * Егіс мерзімі мен тыңайтқыштарды қолдану бойынша ұсыныстар.
                """,
                "agro_cap1": "Агрометеорологиялық бақылау пункттері",
                "agro_cap2": "Дәнді дақылдарды себу мерзімдері"
            },
            "English": {
                "hydro_sub": "💧 Hydrological Forecasts",
                "hydro_title": "#### Water Security of Kazakhstan",
                "hydro_list": """
                * 🌊 **River Monitoring** – lowland and mountain rivers
                * ⚠️ **Flood Assessment** and reservoir inflow
                * 💧 **Real-time runoff modeling**
                * 🌪 **Hazard Forecasting** – floods, ice runs, landslides
                * 🛡 **Strategic Support** – resource management and emergency services
                """,
                "hydro_cap1": "Flood Risk Map 2026",
                "hydro_cap2": "Interactive Hydrological Monitoring Map",
                "agro_sub": "🌾 Agrometeorological Forecasts",
                "agro_mon": "**🔍 Monitoring**",
                "agro_mon_list": """
                * 📉 **Soil moisture reserves forecast**
                * 🌽 **Phenological monitoring** of crops
                * 🌡️ **Frost and drought risk assessment**
                * 🚜 **Recommendations** for sowing operations
                """,
                "agro_plat": "**📱 AGRODATA.kz Platform**",
                "agro_plat_text": """
                An interactive agrometeorological portal providing farmers with:
                * High-precision weather forecasts for farmland.
                * Maps of actual productive soil moisture reserves.
                * Recommendations on sowing dates and fertilizer application.
                """,
                "agro_cap1": "Agrometeorological observation points",
                "agro_cap2": "Sowing dates for grain crops"
            }
        }

        t = translations.get(lang, translations["Русский"])

        # 2. Создаем основные колонки
        col_main_left, col_main_right = st.columns(2, gap="large")

        # --- ЛЕВАЯ КОЛОНКА: ГИДРОЛОГИЯ ---
        with col_main_left:
            st.subheader(t["hydro_sub"])
            st.markdown(t["hydro_title"])
            st.write(t["hydro_list"])
            st.write("---")
            
            st.markdown("""
                <style>
                [data-testid="stImage"] img {
                    height: 300px;
                    object-fit: contain;
                }
                </style>
                """, unsafe_allow_html=True)

            img_row_col1, img_row_col2 = st.columns([1, 1.2])
            with img_row_col1:
                if os.path.exists(path_risk):
                    st.image(path_risk, caption=t["hydro_cap1"], use_container_width=True)
                else:
                    st.error("risk.jpeg not found")
            with img_row_col2:
                if os.path.exists(path_hydro):
                    st.image(path_hydro, caption=t["hydro_cap2"], use_container_width=True)
                else:
                    st.error("hydro.png not found")

        # --- ПРАВАЯ КОЛОНКА: АГРОМЕТЕОРОЛОГИЯ ---
        with col_main_right:
            st.subheader(t["agro_sub"])
            a_col1, a_col2 = st.columns(2, gap="medium")
            with a_col1:
                st.markdown(t["agro_mon"])
                st.write(t["agro_mon_list"])
            with a_col2:
                st.markdown(t["agro_plat"])
                st.write(t["agro_plat_text"])
            
            st.write("---")
            agro_col1, agro_col2 = st.columns(2)
            with agro_col1:
                if os.path.exists(path_agro):
                    st.image(path_agro, caption=t["agro_cap1"], use_container_width=True)
                else:
                    st.warning("AGRO.jpg not found")
            with agro_col2:
                if os.path.exists(path_agro1):
                    st.image(path_agro1, caption=t["agro_cap2"], use_container_width=True)
                else:
                    st.warning("agro1.jpg not found")

    # Вызов функции с передачей текущего языка
    show_monitoring_block(lang)

    import os
    import streamlit as st

    def show_ecology_block(lang):
        # 1. Названия файлов
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        path_airkz = os.path.join(BASE_DIR, "airkz_promo.png") 

        # 2. Словарь переводов
        translations = {
            "Русский": {
                "header": "🧪 Экологическая оценка",
                "sub": "Комплексный экологический мониторинг",
                "list": """
                * 🌫️ **Атмосферный воздух** — контроль уровня загрязнения в городах и промышленных зонах.
                * ❄️ **Осадки и снежный покров** — анализ химического состава и накоплений.
                * ☢️ **Радиационный мониторинг** — замер гамма-фона и плотности выпадений.
                * 🌱 **Состояние почв** — оценка содержания тяжелых металлов и пестицидов.
                * 💧 **Поверхностные воды** — контроль качества воды в реках и озерах.
                * 🌉 **Трансграничные водотоки** — мониторинг объектов на границах.
                """,
                "app_title": "#### 📱 Мобильное приложение «AirKZ»",
                "app_desc": "«AirKZ» отслеживает качество атмосферного воздуха на всей территории Казахстана. Приложение автоматически определяет ближайший пост по данным геолокации.",
                "app_caption": "📲 Доступно в App Store и Google Play",
                "silam_desc": "Интерактивная модель SILAM.",
                "silam_link": "Открыть в новом окне"
            },
            "Қазақша": {
                "header": "🧪 Экологиялық бағалау",
                "sub": "Кешенді экологиялық мониторинг",
                "list": """
                * 🌫️ **Атмосфералық ауа** — қалалар мен өнеркәсіптік аймақтардағы ластану деңгейін бақылау.
                * ❄️ **Жауын-шашын және қар жамылғысы** — химиялық құрамы мен жиналуын талдау.
                * ☢️ **Радиациялық мониторинг** — гамма-фонды және шөгу тығыздығын өлшеу.
                * 🌱 **Топырақ күйі** — ауыр металдар мен пестицидтердің мөлшерін бағалау.
                * 💧 **Беткі сулар** — өзендер мен көлдердегі су сапасын бақылау.
                * 🌉 **Трансшекаралық су ағындары** — шекарадағы нысандарды мониторингілеу.
                """,
                "app_title": "#### 📱 «AirKZ» мобильді қосымшасы",
                "app_desc": "«AirKZ» бүкіл Қазақстан аумағындағы атмосфералық ауаның сапасын бақылайды. Қосымша геолокация деректері бойынша ең жақын бекетті автоматты түрде анықтайды.",
                "app_caption": "📲 App Store және Google Play дүкендерінде қолжетімді",
                "silam_desc": "SILAM интерактивті моделі.",
                "silam_link": "Жаңа терезеде ашу"
            },
            "English": {
                "header": "🧪 Environmental Assessment",
                "sub": "Comprehensive Environmental Monitoring",
                "list": """
                * 🌫️ **Ambient Air** — monitoring pollution levels in cities and industrial zones.
                * ❄️ **Precipitation and Snow Cover** — analysis of chemical composition and accumulation.
                * ☢️ **Radiation Monitoring** — measurement of gamma background and deposition density.
                * 🌱 **Soil Condition** — assessment of heavy metals and pesticides content.
                * 💧 **Surface Waters** — water quality control in rivers and lakes.
                * 🌉 **Transboundary Watercourses** — monitoring of objects at borders.
                """,
                "app_title": "#### 📱 'AirKZ' Mobile Application",
                "app_desc": "'AirKZ' monitors atmospheric air quality throughout Kazakhstan. The app automatically determines the nearest station using geolocation data.",
                "app_caption": "📲 Available on App Store and Google Play",
                "silam_desc": "Interactive SILAM model.",
                "silam_link": "Open in new window"
            }
        }

        t = translations.get(lang, translations["Русский"])

        # 3. Отрисовка
        st.markdown("---")
        st.markdown(f"<h2 style='text-align: center; color: #003366;'>{t['header']}</h2>", unsafe_allow_html=True)
        
        col_text, col_visual = st.columns([1.2, 1.3], gap="large")

        with col_text:
            st.subheader(t['sub'])
            st.write(t['list'])
            
            st.markdown(t['app_title'])
            st.write(t['app_desc'])
            
            if os.path.exists(path_airkz):
                st.image(path_airkz, width=400)
            else:
                st.caption(t['app_caption'])

        with col_visual:
            st.write("##") # Отступ
            
            silam_url = "https://www.kazhydromet.kz/vc/silam/"
            
            st.markdown(
                f"""
                <iframe 
                    src="{silam_url}" 
                    width="100%" 
                    height="550" 
                    style="border: 1px solid #003366; border-radius: 10px;"
                    frameborder="0">
                </iframe>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown(
                f"<p style='text-align: center; color: gray; font-size: 14px;'>"
                f"{t['silam_desc']} <a href='{silam_url}' target='_blank'>{t['silam_link']}</a>"
                f"</p>", 
                unsafe_allow_html=True
            )

    # Вызов функции
    show_ecology_block(lang)




    import os
    import streamlit as st

    def show_science_block(lang):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # 1. СЛОВАРЬ ПЕРЕВОДОВ
        translations = {
            "Русский": {
                "main_title": "🔬 Научные исследования",
                "main_subtitle": "Анализ долгосрочных изменений природной среды Казахстана",
                "clime_title": "### 🌍 Климат Казахстана",
                "clime_text": """
                    За последние годы темпы потепления в Казахстане опережают среднеглобальные значения. 
                    
                    **Ключевые факты:**
                    * Средний рост: **+0.3°C** за десятилетие.
                    * Участились периоды экстремальной жары.
                    * Тренд потепления носит устойчивый характер.
                """,
                "clime_cap1": "Тренды температуры",
                "clime_cap2": "Ранг температуры",
                "caspian_title": "### 🌊 Каспийское море",
                "caspian_text": """
                    Динамика уровня моря с 1900 года показывает циклы трансгрессий и регрессий, определяющие экологию региона.
                    
                    **Текущее состояние:**
                    * Исторический минимум 1977 года (**-29.01 м**) достигнут в 2024 году.
                    * С 2006 года море потеряло более **2-х метров** уровня.
                    * Критическая ситуация для мелководного Северного Каспия.
                """,
                "caspian_cap1": "Многолетняя динамика уровня",
                "caspian_cap2": "Оценка на будущее (2006-2050)",
                "footer_quote": "«Наблюдая сегодня — защищаем завтра»",
                "footer_sub": "Всемирная метеорологическая организация (ВМО)"
            },
            "Қазақша": {
                "main_title": "🔬 Ғылыми зерттеулер",
                "main_subtitle": "Қазақстанның табиғи ортасының ұзақ мерзімді өзгерістерін талдау",
                "clime_title": "### 🌍 Қазақстан климаты",
                "clime_text": """
                    Соңғы жылдары Қазақстандағы жылыну қарқыны орташа жаһандық мәндерден озып кетті.
                    
                    **Негізгі фактілер:**
                    * Орташа өсім: онжылдықта **+0.3°C**.
                    * Экстремалды ыстық кезеңдері жиіледі.
                    * Жылыну тренді тұрақты сипатқа ие.
                """,
                "clime_cap1": "Температура трендтері",
                "clime_cap2": "Температура рангі",
                "caspian_title": "### 🌊 Каспий теңізі",
                "caspian_text": """
                    1900 жылдан бергі теңіз деңгейінің динамикасы аймақтың экологиясын анықтайтын трансгрессиялар мен регрессиялар циклдерін көрсетеді.
                    
                    **Ағымдағы жағдайы:**
                    * 1977 жылғы тарихи минимумға (**-29.01 м**) 2024 жылы қол жеткізілді.
                    * 2006 жылдан бастап теңіз деңгейі **2 метрден** астам төмендеді.
                    * Солтүстік Каспийдің таяз сулары үшін критикалық жағдай.
                """,
                "caspian_cap1": "Деңгейдің көпжылдық динамикасы",
                "caspian_cap2": "Болашаққа болжам (2006-2050)",
                "footer_quote": "«Бүгін бақылай отырып — ертеңді қорғаймыз»",
                "footer_sub": "Дүниежүзілік метеорологиялық ұйым (ДМҰ)"
            },
            "English": {
                "main_title": "🔬 Scientific Research",
                "main_subtitle": "Analysis of long-term changes in Kazakhstan's environment",
                "clime_title": "### 🌍 Climate of Kazakhstan",
                "clime_text": """
                    In recent years, the rate of warming in Kazakhstan has outpaced global average values.
                    
                    **Key Facts:**
                    * Average increase: **+0.3°C** per decade.
                    * Periods of extreme heat have become more frequent.
                    * The warming trend remains steady.
                """,
                "clime_cap1": "Temperature trends",
                "clime_cap2": "Temperature rank",
                "caspian_title": "### 🌊 Caspian Sea",
                "caspian_text": """
                    Sea level dynamics since 1900 show cycles of transgressions and regressions that define the region's ecology.
                    
                    **Current State:**
                    * The 1977 historical minimum (**-29.01 m**) was reached again in 2024.
                    * Since 2006, the sea level has dropped by more than **2 meters**.
                    * A critical situation for the shallow Northern Caspian.
                """,
                "caspian_cap1": "Long-term level dynamics",
                "caspian_cap2": "Future assessment (2006-2050)",
                "footer_quote": "«Observing today — protecting tomorrow»",
                "footer_sub": "World Meteorological Organization (WMO)"
            }
        }

        t = translations.get(lang, translations["Русский"])

        # 2. ШАПКА БЛОКА
        st.markdown(f"""
            <div style="text-align: center; margin-top: 50px;">
                <h2 style='color: #003366;'>{t['main_title']}</h2>
                <p style='color: #666; font-size: 1.1rem; margin-bottom: 40px;'>
                    {t['main_subtitle']}
                </p>
            </div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns(2, gap="large")

        # --- ЛЕВЫЙ БЛОК: КЛИМАТ ---
        with col_left:
            st.markdown(t['clime_title'])
            st.write(t['clime_text'])
            st.write("---")

            path_clime = os.path.join(BASE_DIR, "climate.png")
            path_clime1 = os.path.join(BASE_DIR, "climate1.png")

            clime_col1, clime_col2 = st.columns(2)
            with clime_col1:
                if os.path.exists(path_clime):
                    st.image(path_clime, caption=t['clime_cap1'], use_container_width=True)
            with clime_col2:
                if os.path.exists(path_clime1):
                    st.image(path_clime1, caption=t['clime_cap2'], use_container_width=True)

        # --- ПРАВЫЙ БЛОК: КАСПИЙ ---
        with col_right:
            st.markdown(t['caspian_title'])
            st.write(t['caspian_text'])
            st.write("---")

            path_cs = os.path.join(BASE_DIR, "CS.png")
            path_cs1 = os.path.join(BASE_DIR, "CS1.png")

            cs_col1, cs_col2 = st.columns(2)
            with cs_col1:
                if os.path.exists(path_cs):
                    st.image(path_cs, caption=t['caspian_cap1'], use_container_width=True)
            with cs_col2:
                if os.path.exists(path_cs1):
                    st.image(path_cs1, caption=t['caspian_cap2'], use_container_width=True)

        # 3. ФУТЕР БЛОКА (СЛОГАН)
        st.write("---")
        st.markdown(f"""
            <div style="text-align: center; padding: 40px; margin-top: 20px;">
                <h1 style="color: #003366; font-size: 36px; margin-bottom: 5px; font-weight: 400;">
                    {t['footer_quote']}
                </h1>
                <p style="color: #666; font-size: 16px; letter-spacing: 1px; text-transform: uppercase;">
                    {t['footer_sub']}
                </p>
            </div>
        """, unsafe_allow_html=True)

    # ВЫЗОВ
    show_science_block(lang)



   
#МОНИТОРИНГ
with tabs[1]:
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
       
    
    # 1. СЛОВАРЬ ПЕРЕВОДОВ ДЛЯ ХЕДЕРА И БАННЕРА
    translations = {
        "Русский": {
            "header_sub": "Национальная гидрометеорологическая служба Казахстана с 1922 года",
            "banner_title": "🌍 Глобальный мониторинг — Национальная безопасность",
            "banner_text": "«Казгидромет» — фундамент гидрометеорологической и экологической стабильности Казахстана. Опираясь на вековой опыт и данные государственной наблюдательной сети, мы создаем качественные аналитические продукты для стратегических отраслей экономики.",
            "m1": ["История и опыт", "100+ лет наблюдений", "мониторинг 24/7"],
            "m2": ["География", "17 филиалов", "весь Казахстан"],
            "m3": ["Команда", "3160", "сотрудников в штате"],
            "m4": ["Мировой стандарт", "ВМО (WMO)", "с 1993 года"]
        },
        "Қазақша": {
            "header_sub": "Қазақстанның ұлттық гидрометеорологиялық қызметі 1922 жылдан бастап",
            "banner_title": "🌍 Жаһандық мониторинг — Ұлттық қауіпсіздік",
            "banner_text": "«Қазгидромет» — Қазақстанның гидрометеорологиялық және экологиялық тұрақтылығының негізі. Ғасырлық тәжірибеге және мемлекеттік бақылау желісінің мәліметтеріне сүйене отырып, біз экономиканың стратегиялық салалары үшін сапалы талдау өнімдерін жасаймыз.",
            "m1": ["Тарих және тәжірибе", "100+ жыл бақылау", "24/7 мониторинг"],
            "m2": ["География", "17 филиал", "бүкіл Қазақстан"],
            "m3": ["Команда", "3160", "штаттағы қызметкер"],
            "m4": ["Әлемдік стандарт", "ДМҰ (WMO)", "1993 жылдан бастап"]
        },
        "English": {
            "header_sub": "National Hydrometeorological Service of Kazakhstan since 1922",
            "banner_title": "🌍 Global Monitoring — National Security",
            "banner_text": "Kazhydromet is the foundation of hydrometeorological and environmental stability in Kazakhstan. Drawing on a century of experience and data from the state observation network, we create high-quality analytical products for strategic economic sectors.",
            "m1": ["History & Experience", "100+ years of obs", "24/7 monitoring"],
            "m2": ["Geography", "17 branches", "all over Kazakhstan"],
            "m3": ["Team", "3,160", "employees on staff"],
            "m4": ["World Standard", "WMO", "since 1993"]
        }
    }

    # Получаем текущий набор текстов (предполагается, что переменная lang определена выше)
    t = translations.get(lang, translations["Русский"])

    # 2. HEADER
    st.markdown(f'<p class="promo-subtitle">{t["header_sub"]}</p>', unsafe_allow_html=True)

    # 3. ГЛАВНЫЙ ИНФО-БАННЕР
    st.markdown(f"""
        <div class="kaz-banner">
            <h3 style="color: #004a99; margin-top:0;">{t["banner_title"]}</h3>
            <p style="font-size: 1.1em; color: #334e68; max-width: 85%;">
                {t["banner_text"]}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 4. МЕТРИКИ МАСШТАБА
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t["m1"][0], t["m1"][1], t["m1"][2])
    m2.metric(t["m2"][0], t["m2"][1], t["m2"][2])
    m3.metric(t["m3"][0], t["m3"][1], t["m3"][2])
    m4.metric(t["m4"][0], t["m4"][1], t["m4"][2])

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. СЛОВАРЬ ДАННЫХ ДЛЯ КАРТОЧЕК
    sections_lang = {
        "Русский": [
            {"title": "🌡️ Метеорология", "total": "351 Станция", "items": ["225 Традиционных", "126 Автоматических", "9 Аэрологических", "5 ДМРЛ"]},
            {"title": "💧 Гидрология", "total": "442 Поста", "items": ["394 Речных", "38 Озерных", "10 Морских"]},
            {"title": "🌾 Агрометеорология", "total": "226 Пунктов", "items": ["129 Станций", "97 Постов", "50 Автоматических", "47 Традиционных"]},
            {"title": "🌱 Экология", "total": "175 Постов", "items": ["131 Автоматических", "44 Ручных", "15 Лабораторий"]}
        ],
        "Қазақша": [
            {"title": "🌡️ Метеорология", "total": "351 Станция", "items": ["225 Дәстүрлі", "126 Автоматты", "9 Аэрологиялық", "5 ДМРЛ"]},
            {"title": "💧 Гидрология", "total": "442 Бекет", "items": ["394 Өзен", "38 Көл", "10 Теңіз"]},
            {"title": "🌾 Агрометеорология", "total": "226 Пункт", "items": ["129 Станция", "97 Бекет", "50 Автоматты", "47 Дәстүрлі"]},
            {"title": "🌱 Экология", "total": "175 Бекет", "items": ["131 Автоматты", "44 Қолмен", "15 Зертхана"]}
        ],
        "English": [
            {"title": "🌡️ Meteorology", "total": "351 Stations", "items": ["225 Traditional", "126 Automatic", "9 Aerological", "5 DWR"]},
            {"title": "💧 Hydrology", "total": "442 Posts", "items": ["394 River", "38 Lake", "10 Marine"]},
            {"title": "🌾 Agrometeorology", "total": "226 Points", "items": ["129 At stations", "97 Posts", "50 Automatic", "47 Traditional"]},
            {"title": "🌱 Ecology", "total": "175 Posts", "items": ["131 Automatic", "44 Manual", "15 Laboratories"]}
        ]
    }

    # Выбираем текущие секции (lang должен быть определен в коде ранее)
    current_sections = sections_lang.get(lang, sections_lang["Русский"])

    # 2. ОТРИСОВКА КАРТОЧЕК
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]

    for i, sec in enumerate(current_sections):
        with cols[i]:
            # Логика разделения числа и текста (например, "351 Станция")
            total_parts = sec['total'].split()
            v_total = total_parts[0]
            l_total = " ".join(total_parts[1:])
            
            # Сборка списка подпунктов
            items_html = ""
            for it in sec["items"]:
                parts = it.split()
                # Первый элемент (число) делаем жирным, остальное — обычным текстом
                num = parts[0]
                desc = " ".join(parts[1:])
                items_html += (
                    f'<li style="margin-bottom:5px; list-style:none;">'
                    f'<span style="font-weight:700; color:#004A99;">{num}</span> {desc}'
                    f'</li>'
                )

            # HTML-контент карточки
            card_content = (
                f'<div class="monitor-card" style="background: white; border: 1px solid #eee; padding: 15px; border-radius: 8px; min-height: 320px;">'
                f'<div class="card-header-text" style="font-weight:bold; margin-bottom:10px; color:#1f2937;">{sec["title"]}</div>'
                f'<div style="margin-bottom:15px;">'
                f'<span style="font-size:32px; font-weight:800; color:#004A99; line-height:1;">{v_total}</span> '
                f'<span style="font-size:16px; font-weight:600; color:#455a64;">{l_total}</span>'
                f'</div>'
                f'<ul style="padding-left:0; margin:0; font-size:0.95em; color:#4b5563;">{items_html}</ul>'
                f'</div>'
            )
            
            st.markdown(card_content, unsafe_allow_html=True)

    st.divider()

     

    # 1. СЛОВАРЬ ПЕРЕВОДОВ ДЛЯ МЕТЕО-МОНИТОРИНГА
    translations = {
        "Русский": {
            "title": "Метеорологический мониторинг",
            "subtitle": "Единая национальная сеть комплексного мониторинга приземных и высоких слоев атмосферы, интегрированная в глобальную систему обмена данными ВМО",
            "label1": "Метеостанций в сети",
            "label2": "автоматизированная передача данных",
            "label3": "Срок наблюдений",
            "label4": "Глобальный обмен",
            "label5": "Вековых станций",
            "label6": "Телеграмм/год (МС)",
            "label7": "Телеграмм/год (АМС)",
            "val3": "3 часа"
        },
        "Қазақша": {
            "title": "Метеорологиялық мониторинг",
            "subtitle": "ДМҰ жаһандық деректер алмасу жүйесіне интеграцияланған атмосфераның жер беті және жоғары қабаттарының кешенді мониторингінің бірыңғай ұлттық желісі",
            "label1": "Желідегі метеостанциялар",
            "label2": "деректерді автоматты түрде беру",
            "label3": "Бақылау мерзімі",
            "label4": "Жаһандық алмасу",
            "label5": "Ғасырлық станциялар",
            "label6": "Жеделхат/жыл (МС)",
            "label7": "Жеделхат/жыл (АМС)",
            "val3": "3 сағат"
        },
        "English": {
            "title": "Meteorological Monitoring",
            "subtitle": "A unified national network for comprehensive monitoring of surface and upper layers of the atmosphere, integrated into the WMO global data exchange system",
            "label1": "Weather stations in network",
            "label2": "automated data transmission",
            "label3": "Observation interval",
            "label4": "Global exchange",
            "label5": "Centennial stations",
            "label6": "Telegrams/year (MS)",
            "label7": "Telegrams/year (AMS)",
            "val3": "3 hours"
        }
    }

    t = translations.get(lang, translations["Русский"])

    # 2. HEADER
    st.markdown(f"""
        <div style="text-align:center; margin: 40px 0 20px 0;">
            <h2 style="color: #004A99; font-family: 'Exo 2', sans-serif; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; font-size: 2.2em;">
                {t['title']}
            </h2>
            <p style="color: #546e7a; font-size: 1.1em; font-weight: 500;">{t['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. HIGHLIGHTS (Ключевые показатели)
    st.markdown(f"""
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; margin-bottom: 30px;">
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #003366; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">🏢</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">351</div>
                        <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">{t['label1']}</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #004A99; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">📲</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">100%</div>
                        <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">{t['label2']}</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #0288d1; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">⏱️</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">{t['val3']}</div>
                        <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">{t['label3']}</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #03a9f4; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">🌐</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">WMO</div>
                        <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">{t['label4']}</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #26c6da; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">🏛️</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">19</div>
                        <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">{t['label5']}</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 180px; background: #ffffff; border-left: 5px solid #4fc3f7; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">📧</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">658 800</div>
                        <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">{t['label6']}</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 180px; background: #ffffff; border-left: 5px solid #81d4fa; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">📡</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">1 106 784</div>
                        <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">{t['label7']}</div>
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
        "Метеонаблюдения": "МС.jpg",
        "Аэрология": "Aerology.jpg",
        "ДМРЛ": "DMRL.webp",
        "Кадастр": "Cadastre.png"
    }


    @st.dialog("Метеорологический мониторинг", width="large")
    def show_modal(title, img_path):
        try:
                img = Image.open(img_path)
                st.subheader(title)
                st.image(img, use_container_width=True)
        except Exception as e:
                st.error(f"Не удалось загрузить изображение: {e}")

        # 2. Улучшенный CSS с Font Awesome
    st.markdown("""
        <style>
        /* Контейнер колонки делаем базой для позиционирования */
        [data-testid="column"] {
            position: relative !important;
        }

        /* Карточка с фиксированной высотой и прокруткой */
        .hover-card {
            background: #ffffff; 
            padding: 24px; 
            border-radius: 20px; 
            border-top: 5px solid #004A99; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
            height: 520px !important; 
            overflow-y: auto !important;
            position: relative;
            z-index: 1;
        }

        /* КНОПКА: Теперь мы принудительно выносим её наверх */
        div.stButton > button[key*="icon_btn"] {
            position: absolute !important;
            top: 25px !important;    /* Фиксированный отступ сверху */
            right: 25px !important;  /* Фиксированный отступ справа */
            z-index: 99 !important;  /* Поверх карточки */
            width: 40px !important;
            height: 40px !important;
            padding: 0 !important;
            background-color: #f0f4f8 !important;
            border: 1px solid #e1e8ed !important;
            border-radius: 10px !important;
            cursor: pointer !important;
        }

        div.stButton > button[key*="icon_btn"]:hover {
            background-color: #004A99 !important;
            color: white !important;
            transform: scale(1.1);
        }

        /* Убираем пустые блоки, которые Streamlit создает для кнопок */
        div[data-testid="stVerticalBlock"] > div:has(button[key*="icon_btn"]) {
            height: 0px !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)


    met_col1, met_col2, met_col3, met_col4 = st.columns(4)

    def draw_block(col, btn_key, title, icon_html, description, list_items, img_key):
        with col:
            # 1. Сначала создаем кнопку. Она "улетит" в угол благодаря CSS position: absolute
            if st.button(icon_html, key=btn_key):
                # Ищем путь к фото во всех доступных словарях
                img_path = IMAGE_PATHS.get(img_key) or AGRO_IMAGE_PATHS.get(img_key)
                if img_path:
                    show_modal(title, img_path)
            
            # 2. Затем рисуем саму карточку
            st.markdown(f"""
                <div class="hover-card">
                    <h4 style="color: #004A99; margin-top: 0px; padding-right: 45px; font-size: 1.4em; line-height: 1.3;">
                        {title}
                    </h4>
                    <p style="font-size: 0.9em; color: #455a64; margin-bottom: 12px;">{description}</p>
                    <ul style="padding-left: 18px; font-size: 0.85em; color: #333; line-height: 1.6;">
                        {"".join([f"<li style='margin-bottom:6px;'>{item}</li>" for item in list_items])}
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        
        # Отрисовываем 4 блока

    # 1. РАСШИРЕННЫЙ СЛОВАРЬ ПЕРЕВОДОВ
    meteo_cards_data = {
        "Русский": [
            {
                "title": "🌡️ Метеонаблюдения",
                "icon": "📷",
                "desc": "Системный сбор данных о приземном состоянии атмосферы в единые синхронные сроки (8 раз в сутки).",
                "items": [
                    "<b>Атмосфера:</b> температура, влажность и давление.",
                    "<b>Ветер:</b> скорость, направление и порывы.",
                    "<b>Осадки:</b> интенсивность, тип и снежный покров.",
                    "<b>Облачность:</b> количество, форма и высота ВНГО.",
                    "<b>Почва:</b> температура на поверхности и глубинах.",
                    "<b>Явления:</b> мониторинг ОЯ, СГЯ и гололеда."
                ],
                "img_key": "Метеонаблюдения"
            },
            {
                "title": "🎈 Аэрология",
                "icon": "📸",
                "desc": "Высотное зондирование атмосферы на 9 станциях РК.",
                "items": [
                    "<b>Вертикаль:</b> мониторинг состояния до 30 км и выше.",
                    "<b>Зонды:</b> выпуск радиозондов 2 раза в сутки.",
                    "<b>Модели:</b> данные для циклонов и антициклонов.",
                    "<b>Безопасность:</b> прогноз опасных явлений погоды."
                ],
                "img_key": "Аэрология"
            },
            {
                "title": "📡 ДМРЛ",
                "icon": "🖼️",
                "desc": "Дистанционное сканирование атмосферы в радиусе до 250 км. Совместная сеть из 19 локаторов.",
                "items": [
                    "<b>Осадки:</b> тип (град/дождь), интенсивность и трек.",
                    "<b>Структура:</b> зоны зарождения гроз и шквалов.",
                    "<b>Доплер:</b> скорость движения воздушных масс.",
                    "<b>Оперативность:</b> ежеминутное обновление данных."
                ],
                "img_key": "ДМРЛ"
            },
            {
                "title": "📖 Климатический кадастр",
                "icon": "📁",
                "desc": "Официальный систематизированный свод многолетних данных о климате территории.",
                "items": [
                    "<b>Периоды:</b> средние значения за сутки, месяц, год.",
                    "<b>Экстремумы:</b> крайние показатели температуры и осадков.",
                    "<b>Явления:</b> сроки наступления климатических явлений.",
                    "<b>Фонд:</b> хранение вековых рядов наблюдений."
                ],
                "img_key": "Кадастр"
            }
        ],
        "Қазақша": [
            {
                "title": "🌡️ Метеобақылаулар",
                "icon": "📷",
                "desc": "Атмосфераның жер бетіндегі күйі туралы деректерді бірыңғай синхронды мерзімде (тәулігіне 8 рет) жүйелі жинау.",
                "items": [
                    "<b>Атмосфера:</b> температура, ылғалдылық және қысым.",
                    "<b>Жел:</b> жылдамдық, бағыт және екпін.",
                    "<b>Жауын-шашын:</b> қарқындылық, түрі және қар жамылғысы.",
                    "<b>Бұлттылық:</b> саны, пішіні және биіктігі.",
                    "<b>Топырақ:</b> беткі қабаттағы және тереңдіктегі температура.",
                    "<b>Құбылыстар:</b> ҚҚ, СҚҚ және көктайғақ мониторингі."
                ],
                "img_key": "Метеонаблюдения"
            },
            {
                "title": "🎈 Аэрология",
                "icon": "📸",
                "desc": "ҚР 9 станциясында атмосфераны биіктікте зондтау.",
                "items": [
                    "<b>Вертикаль:</b> 30 км және одан жоғары күйді бақылау.",
                    "<b>Зондтар:</b> тәулігіне 2 рет радиозондтарды шығару.",
                    "<b>Модельдер:</b> циклон мен антициклондарға арналған деректер.",
                    "<b>Қауіпсіздік:</b> қауіпті ауа райы құбылыстарын болжау."
                ],
                "img_key": "Аэрология"
            },
            {
                "title": "📡 ДМРЛ",
                "icon": "🖼️",
                "desc": "250 км радиуста атмосфераны қашықтықтан сканерлеу. 19 локатордан тұратын бірлескен желі.",
                "items": [
                    "<b>Жауын-шашын:</b> түрі (бұршақ/жаңбыр), қарқындылығы және трегі.",
                    "<b>Құрылымы:</b> найзағай мен дауылдың пайда болу аймақтары.",
                    "<b>Доплер:</b> ауа массаларының қозғалыс жылдамдығы.",
                    "<b>Жеделдік:</b> деректерді минут сайын жаңарту."
                ],
                "img_key": "ДМРЛ"
            },
            {
                "title": "📖 Климаттық кадастр",
                "icon": "📁",
                "desc": "Аумақ климаты туралы көпжылдық деректердің ресми жүйеленген жинағы.",
                "items": [
                    "<b>Кезеңдер:</b> тәулік, ай, жыл ішіндегі орташа мәндер.",
                    "<b>Экстремумдар:</b> температура мен жауын-шашынның шекті көрсеткіштері.",
                    "<b>Құбылыстар:</b> климаттық құбылыстардың басталу мерзімдері.",
                    "<b>Мұрағат:</b> ғасырлық бақылау қатарларын сақтау."
                ],
                "img_key": "Кадастр"
            }
        ],
        "English": [
            {
                "title": "🌡️ Meteorological Obs",
                "icon": "📷",
                "desc": "Systematic collection of surface atmospheric data at synchronized intervals (8 times a day).",
                "items": [
                    "<b>Atmosphere:</b> temperature, humidity, and pressure.",
                    "<b>Wind:</b> speed, direction, and gusts.",
                    "<b>Precipitation:</b> intensity, type, and snow cover.",
                    "<b>Clouds:</b> amount, form, and ceiling height.",
                    "<b>Soil:</b> surface and deep-level temperature.",
                    "<b>Phenomena:</b> monitoring of hazardous events and icing."
                ],
                "img_key": "Метеонаблюдения"
            },
            {
                "title": "🎈 Aerology",
                "icon": "📸",
                "desc": "High-altitude atmospheric sounding at 9 stations in Kazakhstan.",
                "items": [
                    "<b>Vertical:</b> monitoring conditions up to 30 km and above.",
                    "<b>Radiosondes:</b> launches twice a day.",
                    "<b>Models:</b> data for cyclone and anticyclone analysis.",
                    "<b>Safety:</b> forecasting of hazardous weather events."
                ],
                "img_key": "Аэрология"
            },
            {
                "title": "📡 DWR",
                "icon": "🖼️",
                "desc": "Remote atmospheric scanning within a radius of 250 km. Joint network of 19 radars.",
                "items": [
                    "<b>Precipitation:</b> type (hail/rain), intensity, and track.",
                    "<b>Structure:</b> lightning and squall formation zones.",
                    "<b>Doppler:</b> movement speed of air masses.",
                    "<b>Efficiency:</b> minute-by-minute data updates."
                ],
                "img_key": "ДМРЛ"
            },
            {
                "title": "📖 Climate Cadastre",
                "icon": "📁",
                "desc": "Official systematized collection of long-term climate data for the territory.",
                "items": [
                    "<b>Periods:</b> daily, monthly, and annual average values.",
                    "<b>Extremes:</b> record temperature and precipitation levels.",
                    "<b>Phenomena:</b> timing of climatic events onset.",
                    "<b>Fund:</b> storage of centennial observation records."
                ],
                "img_key": "Кадастр"
            }
        ]
    }

    # 2. ВЫЗОВ ФУНКЦИИ В ЦИКЛЕ
    current_cards = meteo_cards_data.get(lang, meteo_cards_data["Русский"])
    met_cols = st.columns(4)

    for i, col in enumerate(met_cols):
        card = current_cards[i]
        draw_block(
            col=col,
            btn_key=f"met_btn_{i}",
            title=card["title"],
            icon_html=card["icon"],
            description=card["desc"],
            list_items=card["items"],
            img_key=card["img_key"]
        )
    
    
                   
    import streamlit as st
    import geopandas as gpd
    import folium
    from streamlit_folium import st_folium
    import os

    # --- 1. CSS (Исправлен) ---
    st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                padding-left: 2rem;
                padding-right: 2rem;
            }
            iframe {
                border: none !important;
                width: 100% !important;
            }
            /* Чтобы подписи st.subheader не "уплывали" */
            h3 {
                margin-bottom: 0.5rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Инициализация состояния
    if 'selected_region_id' not in st.session_state:
        st.session_state.selected_region_id = None

    SHP_PATH = "kaz 17 obl.shp"

    import streamlit as st
    import pandas as pd
    import os

    # Инициализация - ЭТО ВАЖНО для предотвращения NameError
    df_stations = None 

    # Определение путей
    base_path = os.path.dirname(os.path.abspath(__file__))
    XLSX_PATH = os.path.join(base_path, "MS tizimi.xlsx")

    @st.cache_data
    def load_stations_from_excel(path):
        if not os.path.exists(path):
            return None
        try:
            df = pd.read_excel(path, skiprows=1)
            df.columns = [str(c).strip() for c in df.columns]
            if 'ФИЛИАЛ' in df.columns:
                df['ФИЛИАЛ'] = df['ФИЛИАЛ'].ffill()
            return df
        except Exception as e:
            st.error(f"Ошибка загрузки Excel: {e}")
            return None

    # Вызываем загрузку здесь, в глобальной области
    df_stations = load_stations_from_excel(XLSX_PATH)


    # 1. СЛОВАРЬ ПЕРЕВОДОВ ИНТЕРФЕЙСА
    ui_translations = {
        "Русский": {
            "main_header": "🇰🇿 Казахстан",
            "regional_header": "📍 РЕГИОНАЛЬНАЯ СЕТЬ",
            "info_header": "ℹ️ Государственная сеть",
            "reg_label": "Региональная сеть:",
            "ms_ams_sub": "Метеостанции и АМС",
            "t_min": "❄️ Т.Мин",
            "t_max": "🔥 Т.Макс",
            "wind": "💨 Ветер",
            "press": "🌡️ Давл.",
            "wind_unit": "м/с",
            "total_network": "Общая сеть РК",
            "total_desc": "<b>351</b> метеорологических станций, из них:",
            "trad": "традиционных",
            "auto": "автоматических",
            "click_hint": "Нажмите на любую область на карте для детализации",
            "legend_title": "Условные обозначения:",
            "ms_label": "Традиционные станции (МС)",
            "ams_label": "Автоматические станции (АМС)",
            "tooltip_alias": "Область:"
        },
        "Қазақша": {
            "main_header": "🇰🇿 Қазақстан",
            "regional_header": "📍 АЙМАҚТЫҚ ЖЕЛІ",
            "info_header": "ℹ️ Мемлекеттік желі",
            "reg_label": "Аймақтық желі:",
            "ms_ams_sub": "Метеостанциялар мен АМС",
            "t_min": "❄️ Т.Мин",
            "t_max": "🔥 Т.Макс",
            "wind": "💨 Жел",
            "press": "🌡️ Қысым",
            "wind_unit": "м/с",
            "total_network": "ҚР жалпы желісі",
            "total_desc": "<b>351</b> метеорологиялық станция, оның ішінде:",
            "trad": "дәстүрлі",
            "auto": "автоматты",
            "click_hint": "Толық мәлімет алу үшін картадағы кез келген аймақты басыңыз",
            "legend_title": "Шартты белгілер:",
            "ms_label": "Дәстүрлі станциялар (МС)",
            "ams_label": "Автоматты станциялар (АМС)",
            "tooltip_alias": "Облыс:"
        },
        "English": {
            "main_header": "🇰🇿 Kazakhstan",
            "regional_header": "📍 REGIONAL NETWORK",
            "info_header": "ℹ️ State Network",
            "reg_label": "Regional Network:",
            "ms_ams_sub": "Weather Stations & AWS",
            "t_min": "❄️ T.Min",
            "t_max": "🔥 T.Max",
            "wind": "💨 Wind",
            "press": "🌡️ Press.",
            "wind_unit": "m/s",
            "total_network": "RK General Network",
            "total_desc": "<b>351</b> meteorological stations, including:",
            "trad": "traditional",
            "auto": "automatic",
            "click_hint": "Click on any region on the map for details",
            "legend_title": "Legend:",
            "ms_label": "Traditional Stations (MS)",
            "ams_label": "Automatic Stations (AWS)",
            "tooltip_alias": "Region:"
        }
    }

    # Получаем текущий перевод (lang должен приходить из вашего основного приложения)
    t = ui_translations.get(lang, ui_translations["Русский"])


    # --- 2. СЛОВАРЬ КАЗГИДРОМЕТ (ПОЛНЫЙ МУЛЬТИЯЗЫЧНЫЙ) ---
    kaz_stats = {
        # г. Алматы
        "almaty": {"ru": "г. Алматы", "kz": "Алматы қ.", "en": "Almaty City", "ms": 19, "ams": 16, "t_min": -38, "t_max": 43, "wind": 3.45, "press": 1012},
        "г. алматы": {"ru": "г. Алматы", "kz": "Алматы қ.", "en": "Almaty City", "ms": 19, "ams": 16, "t_min": -38, "t_max": 43, "wind": 3.45, "press": 1012},
        "алматы": {"ru": "г. Алматы", "kz": "Алматы қ.", "en": "Almaty City", "ms": 19, "ams": 16, "t_min": -38, "t_max": 43, "wind": 3.45, "press": 1012},

        # Жетісу / Жетысу
        "zhetisu": {"ru": "Область Жетісу", "kz": "Жетісу облысы", "en": "Zhetisu Region", "ms": 12, "ams": 7, "t_min": -44, "t_max": 44, "wind": 3.70, "press": 1012},
        "жетісу": {"ru": "Область Жетісу", "kz": "Жетісу облысы", "en": "Zhetisu Region", "ms": 12, "ams": 7, "t_min": -44, "t_max": 44, "wind": 3.70, "press": 1012},
        "жетысуская область": {"ru": "Область Жетісу", "kz": "Жетісу облысы", "en": "Zhetisu Region", "ms": 12, "ams": 7, "t_min": -44, "t_max": 44, "wind": 3.70, "press": 1012},

        # Алматинская область
        "almaty oblast": {"ru": "Алматинская область", "kz": "Алматы облысы", "en": "Almaty Region", "ms": 12, "ams": 7, "t_min": -44, "t_max": 44, "wind": 3.70, "press": 1012},
        "алматинская область": {"ru": "Алматинская область", "kz": "Алматы облысы", "en": "Almaty Region", "ms": 12, "ams": 7, "t_min": -44, "t_max": 44, "wind": 3.70, "press": 1012},

        # Карагандинская и Улытау
        "karaganda": {"ru": "Карагандинская область", "kz": "Қарағанды облысы", "en": "Karaganda Region", "ms": 23, "ams": 10, "t_min": -50, "t_max": 45, "wind": 3.40, "press": 1019},
        "ulytau": {"ru": "Область Ұлытау", "kz": "Ұлытау облысы", "en": "Ulytau Region", "ms": 23, "ams": 10, "t_min": -50, "t_max": 45, "wind": 3.40, "press": 1019},
        "улытауская область": {"ru": "Область Ұлытау", "kz": "Ұлытау облысы", "en": "Ulytau Region", "ms": 23, "ams": 10, "t_min": -50, "t_max": 45, "wind": 3.40, "press": 1019},

        # ВКО и Абай
        "east kazakhstan": {"ru": "ВКО", "kz": "ШҚО", "en": "East Kazakhstan", "ms": 30, "ams": 14, "t_min": -50, "t_max": 45, "wind": 3.45, "press": 1050},
        "abay": {"ru": "Область Абай", "kz": "Абай облысы", "en": "Abay Region", "ms": 30, "ams": 14, "t_min": -50, "t_max": 45, "wind": 3.45, "press": 1050},

        # Туркестанская область и Шымкент
        "turkistan": {"ru": "Туркестанская область", "kz": "Түркістан облысы", "en": "Turkistan Region", "ms": 14, "ams": 6, "t_min": -43, "t_max": 51, "wind": 3.52, "press": 1047},
        "shymkent": {"ru": "г. Шымкент", "kz": "Шымкент қ.", "en": "Shymkent City", "ms": 8, "ams": 4, "t_min": -43, "t_max": 51, "wind": 3.52, "press": 1047},

        # Акмолинская область и Астана
        "akmola": {"ru": "Акмолинская область", "kz": "Ақмола облысы", "en": "Akmola Region", "ms": 15, "ams": 15, "t_min": -52, "t_max": 42, "wind": 3.48, "press": 1038},
        "astana": {"ru": "г. Астана", "kz": "Астана қ.", "en": "Astana City", "ms": 5, "ams": 5, "t_min": -52, "t_max": 42, "wind": 3.48, "press": 1038},

        # Актобе
        "aktobe": {"ru": "Актюбинская область", "kz": "Ақтөбе облысы", "en": "Aktobe Region", "ms": 17, "ams": 9, "t_min": -47, "t_max": 47, "wind": 3.48, "press": 1048},
        
        # Атырау
        "atyrau": {"ru": "Атырауская область", "kz": "Атырау облысы", "en": "Atyrau Region", "ms": 9, "ams": 2, "t_min": -42, "t_max": 46, "wind": 3.34, "press": 1058},

        # Жамбыл
        "zhambyl": {"ru": "Жамбылская область", "kz": "Жамбыл облысы", "en": "Zhambyl Region", "ms": 13, "ams": 8, "t_min": -50, "t_max": 48, "wind": 3.49, "press": 1022},

        # ЗКО
        "west kazakhstan": {"ru": "Западно-Казахстанская область", "kz": "Батыс Қазақстан облысы", "en": "West Kazakhstan", "ms": 13, "ams": 5, "t_min": -44, "t_max": 45, "wind": 3.34, "press": 1058},

        # Костанай
        "kostanay": {"ru": "Костанайская область", "kz": "Қостанай облысы", "en": "Kostanay Region", "ms": 18, "ams": 2, "t_min": -47, "t_max": 45, "wind": 3.40, "press": 1052},

        # Кызылорда
        "kyzylorda": {"ru": "Кызылординская область", "kz": "Қызылорда облысы", "en": "Kyzylorda Region", "ms": 9, "ams": 6, "t_min": -40, "t_max": 48, "wind": 3.62, "press": 1047},

        # Мангистау
        "mangystau": {"ru": "Мангистауская область", "kz": "Маңғыстау облысы", "en": "Mangystau Region", "ms": 7, "ams": 10, "t_min": -38, "t_max": 47, "wind": 3.45, "press": 1053},

        # Павлодар
        "pavlodar": {"ru": "Павлодарская область", "kz": "Павлодар облысы", "en": "Pavlodar Region", "ms": 15, "ams": 4, "t_min": -49, "t_max": 42, "wind": 3.50, "press": 1056},

        # СКО
        "north kazakhstan": {"ru": "Северо-Казахстанская область", "kz": "Солтүстік Қазақстан облысы", "en": "North Kazakhstan", "ms": 11, "ams": 5, "t_min": -48, "t_max": 41, "wind": 3.40, "press": 1055},
    }

    
    
    @st.cache_data
    def load_data(path):
        if not os.path.exists(path): 
            return None
        gdf = gpd.read_file(path)
        
        # Убираем общий контур страны (если есть)
        if 'ADMO_EN' in gdf.columns: 
            gdf = gdf[gdf['ADMO_EN'] != 'KAZ']
        
        # Определяем колонку с ID (обычно ADM1_EN)
        name_col = 'ADM1_EN' if 'ADM1_EN' in gdf.columns else gdf.select_dtypes(include=['object']).columns[0]
        
        # Функция для получения названий на всех языках сразу
        def get_all_names(val):
            clean_key = str(val).strip().lower()
            found = kaz_stats.get(clean_key)
            if not found:
                found = next((v for k, v in kaz_stats.items() if k in clean_key or clean_key in k), None)
            
            if found:
                return found['ru'], found['kz'], found['en']
            return str(val).title(), str(val).title(), str(val).title()

        # Создаем отдельные колонки под каждый язык для GeoJSON
        names_df = gdf[name_col].apply(get_all_names).apply(pd.Series)
        names_df.columns = ['NAME_RU', 'NAME_KZ', 'NAME_EN']
        gdf = pd.concat([gdf, names_df], axis=1)
        
        return gdf.to_crs(epsg=4326), name_col

    result = load_data(SHP_PATH)

    if result:
        gdf, name_col = result
        
        # --- ТРЕХБЛОЧНЫЙ ЛЕЙАУТ ---
        col_left, col_mid, col_right = st.columns([1.1, 1.3, 0.7], gap="medium")

        # Определяем, какую колонку имен использовать для тултипов (на основе lang)
        # Предполагаем, что lang_code это 'ru', 'kz' или 'en'
        lang_to_col = {"ru": "NAME_RU", "kz": "NAME_KZ", "en": "NAME_EN"}
        active_name_col = lang_to_col.get(lang_code, "NAME_RU")

        # --- ЛЕВАЯ КОЛОНКА ---
        with col_left:
            # t["main_header"] — заголовок из словаря переводов интерфейса
            st.subheader(t["main_header"])
            
            m_full = folium.Map(location=[48.0, 67.0], zoom_start=4, tiles="cartodbpositron")
            
            folium.GeoJson(
                gdf,
                style_function=lambda x: {
                    'fillColor': '#e3f2fd', 'color': '#004A99', 'weight': 1, 'fillOpacity': 0.5
                },
                highlight_function=lambda x: {'fillColor': '#004A99', 'fillOpacity': 0.2},
                tooltip=folium.GeoJsonTooltip(
                    fields=[active_name_col], 
                    aliases=[t["tooltip_alias"]], # "Область:" / "Облыс:" / "Region:"
                    localize=True
                )
            ).add_to(m_full)
            
            # Рендер карты
            out_full = st_folium(m_full, use_container_width=True, height=500, key="map_kaz_main")
            
            # Обработка клика
            if out_full and out_full.get("last_active_drawing"):
                new_id = out_full["last_active_drawing"]["properties"].get(name_col)
                if st.session_state.selected_region_id != new_id:
                    st.session_state.selected_region_id = new_id
                    st.rerun()
                    
                        
    # --- СРЕДНЯЯ КОЛОНКА: ДЕТАЛИЗАЦИЯ РЕГИОНА ---
    with col_mid:
        selected_id = st.session_state.get("selected_region_id")
        
        if selected_id:
            # Фильтруем GDF по выбранному ID
            target_data = gdf[gdf[name_col] == selected_id]
            
            if not target_data.empty:
                target_row = target_data.iloc[0]
                
                # Динамический заголовок на текущем языке
                lang_to_col = {"ru": "NAME_RU", "kz": "NAME_KZ", "en": "NAME_EN"}
                current_lang_col = lang_to_col.get(lang_code, "NAME_RU")
                st.subheader(f"📍 {target_row[current_lang_col].upper()}")
                
                # Создаем карту региона, центрированную на его геометрии
                center = target_row.geometry.centroid
                m_reg = folium.Map(location=[center.y, center.x], zoom_start=6, tiles="cartodbpositron")
                
                # Отрисовываем границы только этого региона
                folium.GeoJson(
                    target_row.geometry,
                    style_function=lambda x: {
                        'fillColor': '#004A99', 
                        'color': '#004A99', 
                        'weight': 2, 
                        'fillOpacity': 0.05
                    }
                ).add_to(m_reg)

                # --- ОТОБРАЖЕНИЕ СТАНЦИЙ ИЗ EXCEL ---
                if df_stations is not None:
                    # Используем RUS_NAME для сопоставления с Excel (т.к. manual_map на русском)
                    region_name_ru = target_row['NAME_RU'].lower().strip()
                    
                    # Словарь связки (Shapefile -> Excel "ФИЛИАЛ")
                    manual_map = {
                        "алматы": "г.Алматы",
                        "жетысу": "Жетису",
                        "жетісу": "Жетису",
                        "северо-казахстан": "СКО",
                        "западно-казахстан": "ЗКО",
                        "восточно-казахстан": "ВКО",
                        "абай": "Абай",
                        "улытау": "Улытау",
                        "астана": "ЦА",
                        "шымкент": "Шымкент",
                        "туркестан": "Туркестан",
                        "караганд": "Караганд",
                        "акмол": "Акмол"
                    }
                    
                    # Поиск термина для фильтрации в Excel
                    search_term = None
                    for key, val in manual_map.items():
                        if key in region_name_ru:
                            search_term = val
                            break
                    
                    if not search_term:
                        search_term = region_name_ru.split()[0][:5].capitalize()

                    # Фильтрация станций по филиалу
                    region_stations = df_stations[df_stations['ФИЛИАЛ'].str.contains(search_term, case=False, na=False)]
                    
                    # Поиск колонок с координатами (защита от вариаций в названиях)
                    try:
                        col_lat = [c for c in df_stations.columns if 'с.ш' in c.lower() or 'lat' in c.lower()][0]
                        col_lon = [c for c in df_stations.columns if 'в.д' in c.lower() or 'long' in c.lower()][0]
                        
                        for _, row in region_stations.iterrows():
                            lat = row[col_lat]
                            lon = row[col_lon]
                            
                            if pd.notna(lat) and pd.notna(lon):
                                # Логика цвета: АМС - зеленый, МС - синий
                                st_type = str(row.get('Вид', 'МС')).strip().upper()
                                dot_color = "#2E7D32" if "АМС" in st_type else "#1565C0"
                                
                                folium.CircleMarker(
                                    location=[float(lat), float(lon)],
                                    radius=5,
                                    color=dot_color,
                                    fill=True,
                                    fill_color=dot_color,
                                    fill_opacity=0.7,
                                    popup=folium.Popup(
                                        f"<b>{row.get('Станция', 'Без названия')}</b><br>"
                                        f"Тип: {st_type}<br>"
                                        f"Филиал: {row.get('ФИЛИАЛ', '-')}", 
                                        max_width=200
                                    ),
                                    tooltip=f"{row.get('Станция', 'Станция')} ({st_type})"
                                ).add_to(m_reg)
                    except Exception as e:
                        st.warning(f"Ошибка при поиске координат в Excel: {e}")

                # Рендер карты региона
                st_folium(m_reg, use_container_width=True, height=500, key=f"map_reg_{selected_id}")
        else:
            # Если регион не выбран, показываем заглушку
            st.info("Выберите область на карте Казахстана слева, чтобы увидеть список станций.")
            
                        

    # --- ПРАВАЯ КОЛОНКА: СТАТИСТИКА И ЛЕГЕНДА ---
    with col_right:
        # Словарь переводов для интерфейса правой колонки
        r_labels = {
            "ru": {
                "title": "ℹ️ Государственная сеть",
                "reg_net": "Региональная сеть:",
                "ms_ams": "Метеостанции и АМС",
                "total_net": "Общая сеть РК",
                "total_desc": "<b>351</b> метеорологических станций, из них:<br>• <b>225</b> традиционных<br>• <b>126</b> автоматических",
                "hint": "Нажмите на любую область на карте для детализации по региону",
                "legend": "Условные обозначения:",
                "ms_label": "Традиционные станции (МС)",
                "ams_label": "Автоматические станции (АМС)",
                "not_found": "Данные не найдены"
            },
            "kz": {
                "title": "ℹ️ Мемлекеттік желі",
                "reg_net": "Өңірлік желі:",
                "ms_ams": "Метеостанциялар және АМС",
                "total_net": "ҚР жалпы желісі",
                "total_desc": "<b>351</b> метеорологиялық станция, оның ішінде:<br>• <b>225</b> дәстүрлі<br>• <b>126</b> автоматты",
                "hint": "Аймақ бойынша толық ақпарат алу үшін картаны басыңыз",
                "legend": "Шартты белгілер:",
                "ms_label": "Дәстүрлі станциялар (МС)",
                "ams_label": "Автоматты станциялар (АМС)",
                "not_found": "Мәлімет табылмады"
            },
            "en": {
                "title": "ℹ️ State Network",
                "reg_net": "Regional Network:",
                "ms_ams": "Weather Stations & AWS",
                "total_net": "Total RK Network",
                "total_desc": "<b>351</b> meteorological stations, including:<br>• <b>225</b> traditional<br>• <b>126</b> automatic",
                "hint": "Click on any region on the map for details",
                "legend": "Legend:",
                "ms_label": "Traditional Stations (MS)",
                "ams_label": "Automatic Stations (AWS)",
                "not_found": "Data not found"
            }
        }
        
        # Получаем текущий перевод
        curr_r = r_labels.get(lang_code, r_labels["ru"])
        
        st.subheader(curr_r["title"])
        
        if selected_id:
            # --- БЛОК ВЫБРАННОГО РЕГИОНА ---
            search_name = str(selected_id).strip().lower()
            found_data = kaz_stats.get(search_name)
            
            # Если прямого ключа нет, ищем частичное совпадение
            if not found_data:
                found_data = next((val for key, val in kaz_stats.items() if key in search_name or search_name in key), None)
            
            if found_data:
                # Карточка региона (Цвет основной: #004A99)
                st.markdown(f"""
                    <div style="background:#004A99; color:white; padding:20px; border-radius:15px; margin-bottom:15px; text-align:center">
                        <span style="font-size:1.1em; font-weight:bold">{curr_r['reg_net']}</span><br>
                        <span style="font-size:1.8em">🏢 {found_data['ms']} | 📡 {found_data['ams']}</span>
                        <div style="font-size:0.8em; opacity:0.8; margin-top:5px;">{curr_r['ms_ams']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Метрики (используем стандартные st.metric)
                m1, m2 = st.columns(2)
                with m1:
                    st.metric("❄️ T.Min", f"{found_data['t_min']}°")
                    st.metric("💨 Wind", f"{found_data['wind']} m/s")
                with m2:
                    st.metric("🔥 T.Max", f"{found_data['t_max']}°")
                    st.metric("🌡️ Pres.", f"{found_data['press']}")
            else:
                st.warning(f"{curr_r['not_found']}: {selected_id}")
                
        else:
            # --- ОБЩАЯ СТАТИСТИКА (ПО УМОЛЧАНИЮ) ---
            st.markdown(f"""
                <div style="background:#f0f2f6; padding:20px; border-radius:15px; border: 1px dashed #004A99;">
                    <h4 style="margin:0; color:#004A99;">{curr_r['total_net']}</h4>
                    <p style="font-size:1.1em; margin:15px 0; line-height:1.5;">
                        {curr_r['total_desc']}
                    </p>
                    <p style="font-size:0.85em; color:#546e7a; font-style:italic; border-top: 1px solid #ccc; padding-top:10px; margin-top:10px;">
                        {curr_r['hint']}
                    </p>
                </div>
            """, unsafe_allow_html=True)

        # --- ЛЕГЕНДА (ВСЕГДА ВНИЗУ) ---
        st.markdown(f"""
            <div style="margin-top: 25px; padding: 15px; border-radius: 10px; background: white; border: 1px solid #e6e9ef; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <div style="font-size: 0.85em; font-weight: bold; color: #546e7a; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;">
                    {curr_r['legend']}
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="width: 12px; height: 12px; background-color: #1565C0; border-radius: 50%; margin-right: 12px;"></div>
                    <span style="font-size: 0.9em; color: #1a1c1f;">{curr_r['ms_label']}</span>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 12px; height: 12px; background-color: #2E7D32; border-radius: 50%; margin-right: 12px;"></div>
                    <span style="font-size: 0.9em; color: #1a1c1f;">{curr_r['ams_label']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    
          

    # --- 1. ПОДГОТОВКА ТЕКСТОВ (Мультиязычность) ---
    storm_t = {
            "ru": {
                "header": "🌩️ Мониторинг штормовой активности (2020-2025 гг.)",
                "def_title": "Штормовая активность",
                "def_text": "— это интенсивность возникновения опасных метеорологических явлений, требующих оперативного оповещения. Статистика включает в себя выпуск штормовых телеграмм по двум категориям:",
                "oy_title": "ОЯ (Опасные явления)",
                "oy_text": "метеорологические явления, которые по своей интенсивности могут нанести значительный ущерб.",
                "sgy_title": "СГЯ (Стихийные явления)",
                "sgy_text": "экстремально интенсивные явления, представляющие непосредственную угрозу жизни людей.",
                "branches": ["Акмола", "Актобе", "Жетысу", "г.Алматы", "Атырау", "ВКО", "Жамбыл", "ЗКО", "Караганды", "Костанай", "Кызылорда", "Мангистау", "Павлодар", "СКО", "Туркестан"]
            },
            "kz": {
                "header": "🌩️ Дауыл белсенділігінің мониторингі (2020-2025 жж.)",
                "def_title": "Дауыл белсенділігі",
                "def_text": "— бұл жедел хабарлауды талап ететін қауіпті метеорологиялық құбылыстардың пайда болу қарқындылығы. Статистика екі санат бойынша дауылды жеделхаттардың шығарылуын қамтиды:",
                "oy_title": "ҚҚ (Қауіпті құбылыстар)",
                "oy_text": "қарқындылығы бойынша экономика мен халыққа айтарлықтай зиян келтіруі мүмкін метеорологиялық құбылыстар.",
                "sgy_title": "ТГҚ (Төтенше гидрометеорологиялық құбылыстар)",
                "sgy_text": "адам өміріне тікелей қауіп төндіретін өте қарқынды құбылыстар.",
                "branches": ["Ақмола", "Ақтөбе", "Жетісу", "Алматы қ.", "Атырау", "ШҚО", "Жамбыл", "БҚО", "Қарағанды", "Қостанай", "Қызылорда", "Маңғыстау", "Павлодар", "СҚО", "Түркістан"]
            },
            "en": {
                "header": "🌩️ Storm Activity Monitoring (2020-2025)",
                "def_title": "Storm Activity",
                "def_text": "is the intensity of hazardous meteorological events requiring rapid notification. Statistics include storm telegrams issued in two categories:",
                "oy_title": "HP (Hazardous Phenomena)",
                "oy_text": "meteorological events that can cause significant damage due to their intensity.",
                "sgy_title": "EHP (Extreme Hydromet Phenomena)",
                "sgy_text": "extremely intense events posing a direct threat to human life.",
                "branches": ["Akmola", "Aktobe", "Zhetysu", "Almaty city", "Atyrau", "EKO", "Zhambyl", "WKO", "Karaganda", "Kostanay", "Kyzylorda", "Mangystau", "Pavlodar", "NKO", "Turkestan"]
            }
        }

    curr_st = storm_t.get(lang_code, storm_t["ru"])

# --- 2. ДАННЫЕ ---
    data_storm = {
            "Филиал": curr_st["branches"],
            "2020": [1385, 1043, 741, 932, 456, 1367, 635, 567, 1191, 952, 380, 220, 444, 650, 746],
            "2021": [1209, 998, 922, 1336, 693, 1644, 735, 776, 1185, 693, 499, 258, 348, 669, 778],
            "2022": [1228, 955, 765, 1659, 699, 1842, 755, 885, 1162, 836, 496, 229, 692, 663, 1078],
            "2023": [1518, 1055, 827, 1725, 749, 1962, 788, 813, 1391, 997, 436, 349, 684, 1007, 730],
            "2024": [2004, 1188, 734, 1579, 604, 2180, 817, 957, 1396, 1153, 457, 259, 908, 1142, 839],
            "2025": [1670, 1192, 725, 1414, 604, 2644, 652, 1162, 1262, 965, 620, 237, 897, 1188, 589]
        }

    df_storm = pd.DataFrame(data_storm)
        
        # --- ВНИМАНИЕ: ДОБАВЬТЕ ЭТИ СТРОКИ ЗДЕСЬ ---
    years = ["2020", "2021", "2022", "2023", "2024", "2025"]
    total_values = [11709, 12743, 13944, 15031, 16217, 15821]
        # ------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(curr_st["header"])

        # --- 3. ИНТЕРФЕЙС (HTML блок) ---
    st.markdown(f"""
            <div style="background-color: rgba(255, 165, 0, 0.1); padding: 15px; border-left: 5px solid #FFA500; border-radius: 5px; margin-bottom: 20px;">
                <span style="color: #FFA500; font-weight: bold;">{curr_st['def_title']}</span> {curr_st['def_text']}
                <ul style="margin-top: 10px; font-size: 0.9em;">
                    <li><b>{curr_st['oy_title']}</b> — {curr_st['oy_text']}</li>
                    <li><b>{curr_st['sgy_title']}</b> — {curr_st['sgy_text']}</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    import plotly.express as px
    import plotly.graph_objects as go

        # --- 1. СЛОВАРЬ ПЕРЕВОДОВ ---
    chart_lang = {
            "ru": {
                "m1_label": "Пик активности",
                "m2_label": "Максимум в 2025",
                "m3_label": "Среднее за год",
                "m1_delta": "телеграмм",
                "left_title": "**Анализ штормовых оповещений (по годам)**",
                "right_title": "**Распределение по регионам (Тепловая карта)**",
                "bar_name": "Количество",
                "line_name": "Динамика",
                "y_axis": "Кол-во оповещений",
                "heat_labels": dict(x="Год", y="Филиал", color="Кол-во")
            },
            "kz": {
                "m1_label": "Белсенділік шыңы",
                "m2_label": "2025 ж. максимумы",
                "m3_label": "Жылдық орташа мән",
                "m1_delta": "жеделхат",
                "left_title": "**Дауылды ескертулерді талдау (жылдар бойынша)**",
                "right_title": "**Аймақтар бойынша бөлу (Жылу картасы)**",
                "bar_name": "Саны",
                "line_name": "Динамика",
                "y_axis": "Ескертулер саны",
                "heat_labels": dict(x="Жыл", y="Филиал", color="Саны")
            },
            "en": {
                "m1_label": "Peak Activity",
                "m2_label": "2025 Maximum",
                "m3_label": "Annual Average",
                "m1_delta": "telegrams",
                "left_title": "**Storm Alert Analysis (by Year)**",
                "right_title": "**Regional Distribution (Heatmap)**",
                "bar_name": "Quantity",
                "line_name": "Trend",
                "y_axis": "Alert Count",
                "heat_labels": dict(x="Year", y="Branch", color="Count")
            }
        }

    c_t = chart_lang.get(lang_code, chart_lang["ru"])

        # --- 3. МЕТРИКИ (Теперь total_values точно определены выше) ---
    m1, m2, m3 = st.columns(3)
    with m1:
            st.metric(c_t["m1_label"], "2024", f"16 217 {c_t['m1_delta']}")
    with m2:
            st.metric(c_t["m2_label"], "EKO / ШҚО / ВКО", "2 644")
    with m3:
            avg_val = int(sum(total_values)/len(total_values))
            st.metric(c_t["m3_label"], f"{avg_val:,}".replace(",", " "))

        # --- 3. ГРАФИКИ ---
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
            st.markdown(c_t["left_title"])
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=years, y=total_values, name=c_t["bar_name"],
                marker=dict(color='rgba(52, 152, 219, 0.6)', line=dict(color='#3498db', width=1)),
                hovertemplate="Year: %{x}<br>Total: %{y}<extra></extra>"
            ))
            fig.add_trace(go.Scatter(
                x=years, y=total_values, mode='lines+markers', name=c_t["line_name"],
                line=dict(color='#FFA500', width=3),
                marker=dict(size=8, symbol='circle', color='white', line=dict(width=2, color='#FFA500'))
            ))

            fig.update_layout(
                height=450, margin=dict(l=50, r=10, t=50, b=50),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=14)),
                font=dict(color="#dee2e6"), bargap=0.3,
                yaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.1)', title=dict(text=c_t["y_axis"], font=dict(size=16)), tickfont=dict(size=14)),
                xaxis=dict(dtick=1, tickfont=dict(size=14))
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
            st.markdown(c_t["right_title"])
            fig_heat = px.imshow(
                df_storm.set_index("Филиал")[years],
                labels=c_t["heat_labels"],
                color_continuous_scale="Blues", aspect="auto"
            )
            fig_heat.update_layout(
                height=450, margin=dict(l=80, r=20, t=50, b=80),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white"),
                xaxis=dict(tickfont=dict(size=14), side='bottom'),
                yaxis=dict(tickfont=dict(size=12), autorange='reversed')
            )
            st.plotly_chart(fig_heat, use_container_width=True)
            
            
            

# --- 4. АВТОМАТИЧЕСКОЕ АНАЛИТИЧЕСКОЕ РЕЗЮМЕ ---
    st.markdown("---")
    
    # Словарь переводов для резюме
    summary_lang = {
        "ru": {
            "header": "### 📋 Аналитическая справка",
            "intro": "За анализируемый период (2020–2025 гг.) наблюдаются следующие ключевые изменения:",
            "leader": "Лидер по нагрузке",
            "leader_text": "В 2025 году наибольшее количество штормовых телеграмм выпущено филиалом",
            "dynamics": "Самая высокая динамика",
            "dynamics_text": "Наиболее резкий рост активности за 5 лет зафиксирован в регионе",
            "dynamics_val": "увеличилось на",
            "trend": "Общий тренд",
            "trend_up": "рост",
            "trend_down": "незначительное снижение",
            "trend_text": "После пиковых значений 2024 года, в 2025 году зафиксировано",
            "trend_reason": "Это может быть связано с изменением климатических циклов.",
            "disclaimer": "⚠️ Данные за 2025 год являются актуальными на текущую дату.",
            "units": "ед."
        },
        "kz": {
            "header": "### 📋 Аналитикалық анықтама",
            "intro": "Талдау кезеңінде (2020–2025 жж.) келесі негізгі өзгерістер байқалады:",
            "leader": "Жүктеме бойынша көшбасшы",
            "leader_text": "2025 жылы дауылды жеделхаттардың ең көп санын шығарған филиал —",
            "dynamics": "Ең жоғары динамика",
            "dynamics_text": "5 жыл ішінде белсенділіктің ең күрт өсуі келесі аймақта тіркелді:",
            "dynamics_val": "көрсеткіш",
            "trend": "Жалпы тренд",
            "trend_up": "өсу",
            "trend_down": "болмашы төмендеу",
            "trend_text": "2024 жылғы ең жоғары көрсеткіштерден кейін, 2025 жылы белсенділіктің",
            "trend_reason": "Бұл климаттық циклдардың өзгеруіне байланысты болуы мүмкін.",
            "disclaimer": "⚠️ 2025 жылға арналған деректер ағымдағы күнге өзекті.",
            "units": "бірлік"
        },
        "en": {
            "header": "### 📋 Analytical Summary",
            "intro": "During the analyzed period (2020–2025), the following key changes are observed:",
            "leader": "Workload Leader",
            "leader_text": "In 2025, the highest number of storm telegrams was issued by the branch",
            "dynamics": "Highest Dynamics",
            "dynamics_text": "The sharpest increase in activity over 5 years was recorded in",
            "dynamics_val": "increased by",
            "trend": "General Trend",
            "trend_up": "growth",
            "trend_down": "slight decrease",
            "trend_text": "After the peak values of 2024, in 2025 there was a",
            "trend_reason": "This may be due to changes in climate cycles.",
            "disclaimer": "⚠️ Data for 2025 is current as of today.",
            "units": "units"
        }
    }

    s_t = summary_lang.get(lang_code, summary_lang["ru"])
    st.markdown(s_t["header"])

    # Расчеты
    df_storm['Growth'] = df_storm['2025'] - df_storm['2020']
    max_growth_region = df_storm.loc[df_storm['Growth'].idxmax()]
    leader_2025 = df_storm.loc[df_storm['2025'].idxmax()]

    total_2024 = 16217
    total_2025 = 15821
    trend_pct = round(((total_2025 - total_2024) / total_2024) * 100, 1)
    
    # Логика выбора текста тренда
    current_trend_text = s_t["trend_down"] if trend_pct < 0 else s_t["trend_up"]

    # Вывод резюме
    st.write(f"""
    {s_t['intro']}

    * **{s_t['leader']}:** {s_t['leader_text']} **{leader_2025['Филиал']}** ({leader_2025['2025']} {s_t['units']}).
    * **{s_t['dynamics']}:** {s_t['dynamics_text']} **{max_growth_region['Филиал']}**. {s_t['dynamics_val']} **{max_growth_region['Growth']}** {s_t['units']} (2025 vs 2020).
    * **{s_t['trend']}:** {s_t['trend_text']} **{current_trend_text}** ({abs(trend_pct)}%). {s_t['trend_reason']}
    """)

    st.caption(s_t["disclaimer"])
    
            
# --- 1. ПОДГОТОВКА ДАННЫХ СГЯ ---
    data_sgy = {
        "Филиал": curr_st["branches"], # Используем мультиязычный список филиалов
        "2020": [25, 82, 7, 16, 0, 2, 10, 0, 18, 15, 3, 39, 3, 7, 10],
        "2021": [15, 26, 35, 17, 0, 2, 6, 5, 6, 7, 1, 26, 3, 9, 5],
        "2022": [10, 5, 56, 55, 2, 2, 6, 1, 2, 5, 8, 14, 4, 2, 12],
        "2023": [9, 65, 108, 104, 63, 32, 19, 3, 25, 5, 6, 18, 10, 31, 11],
        "2024": [11, 17, 49, 84, 7, 6, 17, 2, 9, 9, 0, 2, 11, 8, 4],
        "2025": [6, 11, 50, 30, 4, 5, 7, 3, 1, 4, 3, 3, 1, 7, 1]
    }

    df_sgy = pd.DataFrame(data_sgy)
    years_sgy = ["2020", "2021", "2022", "2023", "2024", "2025"]
    total_sgy = [237, 164, 184, 509, 236, 136]

    # --- 2. СЛОВАРЬ ПЕРЕВОДОВ ДЛЯ СГЯ ---
    sgy_lang = {
        "ru": {
            "header": "⚠️ Анализ Стихийных Гидрометеорологических Явлений (СГЯ)",
            "dist_title": "**Распределение СГЯ по годам**",
            "rating_title": "**Рейтинг регионов по количеству СГЯ (2020-2025)**",
            "x_axis": "Год", "y_axis": "Количество", "total_axis": "Всего СГЯ",
            "note_title": "Аналитическая заметка по СГЯ:",
            "anomaly": "Аномальный период: 2023 год стал экстремальным — зафиксировано",
            "risk_zones": "Зоны риска: Наибольшее суммарное количество явлений зафиксировано в",
            "current_stat": "Текущая ситуация: В 2025 году наблюдается стабилизация",
            "units": "ед."
        },
        "kz": {
            "header": "⚠️ Дүлей гидрометеорологиялық құбылыстарды талдау (ДГҚ)",
            "dist_title": "**ДГҚ жылдар бойынша бөлінуі**",
            "rating_title": "**ДГҚ саны бойынша аймақтар рейтингі (2020-2025)**",
            "x_axis": "Жыл", "y_axis": "Саны", "total_axis": "Барлығы ДГҚ",
            "note_title": "ДГҚ бойынша аналитикалық ескертпе:",
            "anomaly": "Аномальды кезең: 2023 жыл экстремалды болды — тіркелді",
            "risk_zones": "Қауіпті аймақтар: Ең көп құбылыстар саны келесі филиалдарда:",
            "current_stat": "Ағымдағы жағдай: 2025 жылы тұрақтандыру байқалады",
            "units": "бірлік"
        },
        "en": {
            "header": "⚠️ Severe Hydrometeorological Phenomena Analysis (SHP)",
            "dist_title": "**Distribution of SHP by Year**",
            "rating_title": "**Regional Rating by SHP Count (2020-2025)**",
            "x_axis": "Year", "y_axis": "Count", "total_axis": "Total SHP",
            "note_title": "Analytical Note on SHP:",
            "anomaly": "Anomalous Period: 2023 was extreme — recorded",
            "risk_zones": "Risk Zones: The highest total number of phenomena recorded in",
            "current_stat": "Current Situation: Stabilization is observed in 2025",
            "units": "units"
        }
    }
    sg_t = sgy_lang.get(lang_code, sgy_lang["ru"])

    # --- 3. ВИЗУАЛИЗАЦИЯ ---
    st.markdown("---")
    st.subheader(sg_t["header"])

    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        st.markdown(sg_t["dist_title"])
        fig_sgy_total = go.Figure(go.Bar(
            x=years_sgy, y=total_sgy,
            marker_color=['#1f4e79', '#1f4e79', '#1f4e79', '#e74c3c', '#1f4e79', '#1f4e79'], 
            text=total_sgy, textposition='auto'
        ))
        fig_sgy_total.update_layout(
            height=350, margin=dict(l=80, r=20, t=30, b=80),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"),
            xaxis=dict(tickfont=dict(size=14), title=dict(text=sg_t["x_axis"], font=dict(size=14)), type='category'),
            yaxis=dict(tickfont=dict(size=14), title=dict(text=sg_t["y_axis"], font=dict(size=14)))
        )
        st.plotly_chart(fig_sgy_total, use_container_width=True)

    with col_right:
        st.markdown(sg_t["rating_title"])
        df_sgy['Total'] = df_sgy[years_sgy].sum(axis=1)
        df_sgy_sorted = df_sgy.sort_values(by='Total', ascending=True)

        fig_sgy_reg = px.bar(
            df_sgy_sorted, x='Total', y='Филиал', orientation='h',
            text='Total', color='Total', color_continuous_scale="Blues"
        )
        fig_sgy_reg.update_traces(
            textposition='outside', textfont=dict(size=14, color="white"), 
            marker_line_color='rgb(8,48,107)', marker_line_width=1, opacity=0.9
        )
        fig_sgy_reg.update_layout(
            height=450, margin=dict(l=120, r=40, t=20, b=60), # Увеличен l для длинных названий
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"), showlegend=False, coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title=dict(text=sg_t["total_axis"], font=dict(size=14)), tickfont=dict(size=14)),
            yaxis=dict(title="", tickfont=dict(size=12))
        )
        st.plotly_chart(fig_sgy_reg, use_container_width=True)


# --- 4. АВТОМАТИЧЕСКОЕ РЕЗЮМЕ ПО СГЯ ---
    top_region_sgy = df_sgy.loc[df_sgy['Total'].idxmax()]
    
    st.info(f"""
        **{sg_t['note_title']}**
        * **{sg_t['anomaly']}** **509** {sg_t['units']}.
        * **{sg_t['risk_zones']}** **{top_region_sgy['Филиал']}**.
        * **{sg_t['current_stat']}** ({total_sgy[-1]} {sg_t['units']}).
    """)
    
        
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
                    font-size: 1.5em;
                    color: #546e7a;
                    font-weight: 600;
                    text-transform: uppercase;
                }
                </style>
        """, unsafe_allow_html=True)

# Словарь переводов
    rec_lang = {
        "ru": {
            "title": "🏆 Метео-рекорды Казахстана за сегодня",
            "source": "по сети РГП 'Казгидромет'",
            "cold": "Самый холодный",
            "warm": "Самый теплый",
            "wind": "Сильный ветер",
            "atbasar": "ст. Атбасар",
            "shymkent": "г. Шымкент",
            "dostyk": "ст. Достык (Джунгарские ворота)",
            "unit_v": "м/с"
        },
        "kz": {
            "title": "🏆 Бүгінгі Қазақстанның метео-рекордтары",
            "source": "'Қазгидромет' РМК желісі бойынша",
            "cold": "Ең суық",
            "warm": "Ең жылы",
            "wind": "Қатты жел",
            "atbasar": "Атбасар ст.",
            "shymkent": "Шымкент қ.",
            "dostyk": "Достық ст. (Жоңғар қақпасы)",
            "unit_v": "м/с"
        },
        "en": {
            "title": "🏆 Kazakhstan Weather Records for Today",
            "source": "via Kazhydromet network",
            "cold": "Coldest",
            "warm": "Warmest",
            "wind": "Strong Wind",
            "atbasar": "Atbasar st.",
            "shymkent": "Shymkent city",
            "dostyk": "Dostyk st. (Dzungarian Gate)",
            "unit_v": "m/s"
        }
    }
    r_t = rec_lang.get(lang_code, rec_lang["ru"])

    st.write(f"### {r_t['title']}")
    st.caption(f"Data as of {pd.Timestamp.now().strftime('%d.%m.%Y %H:%M')} {r_t['source']}")

    rec_col1, rec_col2, rec_col3 = st.columns(3)

    with rec_col1:
        st.markdown(f"""
            <div class="record-card">
                <div style="font-size: 2em;">❄️</div>
                <div class="record-city">{r_t['cold']}</div>
                <div class="record-val" style="color: #0288d1;">-28°C</div>
                <div style="font-size: 0.8em; color: #78909c;">{r_t['atbasar']}</div>
            </div>
        """, unsafe_allow_html=True)

    with rec_col2:
        st.markdown(f"""
            <div class="record-card">
                <div style="font-size: 2em;">☀️</div>
                <div class="record-city">{r_t['warm']}</div>
                <div class="record-val" style="color: #f57c00;">+12°C</div>
                <div style="font-size: 0.8em; color: #78909c;">{r_t['shymkent']}</div>
            </div>
        """, unsafe_allow_html=True)

    with rec_col3:
        st.markdown(f"""
            <div class="record-card">
                <div style="font-size: 2em;">💨</div>
                <div class="record-city">{r_t['wind']}</div>
                <div class="record-val" style="color: #455a64;">35 {r_t['unit_v']}</div>
                <div style="font-size: 0.8em; color: #78909c;">{r_t['dostyk']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
 
 
      
        
  # 7. ГИДРОЛОГИЧЕСКИЙ МОНИТОРИНГ        
    # 1. СЛОВАРЬ ПЕРЕВОДОВ (поместите это в начало функции или скрипта)
    hydro_translations = {
        "ru": {
            "title": "Гидрологический мониторинг",
            "subtitle": "Единая государственная система наблюдений за состоянием водных объектов и ведение водного кадастра РК",
            "posts": "Гидропостов",
            "basins": "Бассейнов",
            "century": "Вековых поста"
        },
        "kz": {
            "title": "Гидрологиялық мониторинг",
            "subtitle": "Су объектілерінің жай-күйін бақылаудың бірыңғай мемлекеттік жүйесі және ҚР су кадастрын жүргізу",
            "posts": "Гидробекеттер",
            "basins": "Алаптар",
            "century": "Ғасырлық бекет"
        },
        "en": {
            "title": "Hydrological Monitoring",
            "subtitle": "Unified state system for monitoring water bodies and maintaining the water cadastre of the RK",
            "posts": "Hydroposts",
            "basins": "Basins",
            "century": "Century posts"
        }
    }

    # 2. ПОЛУЧЕНИЕ ТЕКУЩЕГО ПЕРЕВОДА
    # Если lang_code не определен, по умолчанию ставим 'ru'
    current_lang = lang_code if 'lang_code' in locals() else "ru"
    t = hydro_translations.get(current_lang, hydro_translations["ru"])

    # --- 1. ЗАГОЛОВОК СЕКЦИИ ---
    st.markdown(f"""
        <div style="text-align:center; margin: 40px 0 20px 0;">
            <h2 style="color: #004A99; font-family: 'Exo 2', sans-serif; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; font-size: 2.2em;">
                {t['title']}
            </h2>
            <p style="color: #546e7a; font-size: 1.1em; font-weight: 500;">{t['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)

    # --- 2. HIGHLIGHTS (Верхние карточки) ---
    st.markdown(f"""
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; margin-bottom: 30px;">
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #003366; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">🏢</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">442</div>
                        <div style="font-size: 0.9em; color: #546e7a; text-transform: uppercase; font-weight: 700;">{t['posts']}</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #004A99; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">📊</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">8</div>
                        <div style="font-size: 0.9em; color: #546e7a; text-transform: uppercase; font-weight: 700;">{t['basins']}</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #0288d1; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">🏛️</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">24</div>
                        <div style="font-size: 0.9em; color: #546e7a; text-transform: uppercase; font-weight: 700;">{t['century']}</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 1. ПУТИ К ИЗОБРАЖЕНИЯМ ---
    # Убедитесь, что файлы лежат в папке с проектом или доступны по путям
    IMAGE_PATHS = {
        "HP": "HP1.jpeg",
        "Auto": "auto.png",
        "TRANS": "trans.png", # Добавил ключ для трансграничных постов
        "Cadastre": "cad.png"
    }

    # --- 2. СЛОВАРЬ ПЕРЕВОДОВ ДЛЯ БЛОКОВ ---
    blocks_lang = {
        "ru": {
            "b1_title": "🌊 Национальная сеть",
            "b1_desc": "Комплексный мониторинг рек, озер и каналов (442 поста).",
            "b1_list": [
                "<b>Инфраструктура:</b> 25 снегомерных и 2 осадкомерных маршрута",
                "<b>Регламент:</b> Замеры уровня ежедневно в 08:00 и 20:00",
                "<b>Расход воды:</b> 3 раза в месяц в межень",
                "<b>Оборудование:</b> Акустические доплеровские профилографы"
            ],
            "b2_title": "📟 Автоматические посты",
            "b2_desc": "Системы непрерывного мониторинга и передачи данных.",
            "b2_list": ["<b>Тип:</b> OTT Ecolog 1000", "<b>Режим:</b> ежечасные данные", "<b>Передача:</b> GSM связь"],
            "b3_title": "🌍 Трансграничные посты",
            "b3_desc": "Мониторинг на водных объектах с сопредельными странами.",
            "b3_list": ["<b>Всего:</b> 43 поста", "<b>РФ и КНР:</b> 23 с РФ, 11 с КНР", "<b>ЦА:</b> 7 с КР, 2 с РУз"],
            "b4_title": "💧 Водный кадастр",
            "b4_desc": "Единая система данных о водных ресурсах РК.",
            "b4_list": ["<b>Процесс:</b> сбор и анализ данных", "<b>Публикации:</b> ежегодники водных ресурсов", "<b>Цифровизация:</b> электронный банк данных"]
        },
        "kz": {
            "b1_title": "🌊 Ұлттық желі",
            "b1_desc": "Өзендерді, көлдерді және каналдарды кешенді мониторингілеу (442 бекет).",
            "b1_list": [
                "<b>Инфрақұрылым:</b> 25 қар өлшеу және 2 жауын-шашын өлшеу бағыты",
                "<b>Регламент:</b> Деңгейді күн сайын 08:00 және 20:00-де өлшеу",
                "<b>Су шығыны:</b> Саба деңгейінде айына 3 рет",
                "<b>Жабдық:</b> Акустикалық Доплер профилографтары"
            ],
            "b2_title": "📟 Автоматты бекеттер",
            "b2_desc": "Үздіксіз мониторинг және деректерді беру жүйелері.",
            "b2_list": ["<b>Түрі:</b> OTT Ecolog 1000", "<b>Режимі:</b> сағаттық деректер", "<b>Байланыс:</b> GSM байланысы"],
            "b3_title": "🌍 Трансшекаралық бекеттер",
            "b3_title": "🌍 Трансшекаралық бекеттер",
            "b3_desc": "Шекаралас мемлекеттермен бөлісетін су нысандарындағы мониторинг.",
            "b3_list": ["<b>Барлығы:</b> 43 бекет", "<b>РФ және ҚХР:</b> РФ-мен 23, ҚХР-мен 11", "<b>ОА:</b> ҚР-мен 7, ӨР-мен 2"],
            "b4_title": "💧 Су кадастры",
            "b4_desc": "ҚР су ресурстары туралы бірыңғай деректер жүйесі.",
            "b4_list": ["<b>Процесс:</b> деректерді жинау және талдау", "<b>Жарияланымдар:</b> су ресурстарының жылнамалары", "<b>Цифрландыру:</b> электрондық деректер банкі"]
        },
        "en": {
            "b1_title": "🌊 National Network",
            "b1_desc": "Comprehensive monitoring of rivers, lakes, and canals (442 posts).",
            "b1_list": [
                "<b>Infrastructure:</b> 25 snow and 2 precipitation routes",
                "<b>Schedule:</b> Level measurements daily at 08:00 and 20:00",
                "<b>Water discharge:</b> 3 times a month in low water",
                "<b>Equipment:</b> Acoustic Doppler Current Profilers"
            ],
            "b2_title": "📟 Automatic Stations",
            "b2_desc": "Continuous monitoring and data transmission systems.",
            "b2_list": ["<b>Type:</b> OTT Ecolog 1000", "<b>Mode:</b> hourly data transmission", "<b>Link:</b> GSM connection"],
            "b3_title": "🌍 Transboundary Posts",
            "b3_desc": "Monitoring of water bodies shared with neighboring states.",
            "b3_list": ["<b>Total:</b> 43 posts", "<b>RU & CN:</b> 23 with Russia, 11 with China", "<b>CA:</b> 7 with KG, 2 with UZ"],
            "b4_title": "💧 Water Cadastre",
            "b4_desc": "Unified data system on water resources of Kazakhstan.",
            "b4_list": ["<b>Process:</b> data collection and analysis", "<b>Publications:</b> annual water resource data", "<b>Digital:</b> electronic database management"]
        }
    }

    # Выбор текущего языка (используем lang_code из вашего селектора)
    b_t = blocks_lang.get(lang_code, blocks_lang["ru"])

    # --- 3. ОТРИСОВКА КОНТЕЙНЕРА ---
    with st.container():
        h_col1, h_col2, h_col3, h_col4 = st.columns(4)

        draw_block(h_col1, "hydro_btn_1", b_t["b1_title"], "📷", b_t["b1_desc"], b_t["b1_list"], "HP")
        draw_block(h_col2, "hydro_btn_2", b_t["b2_title"], "📸", b_t["b2_desc"], b_t["b2_list"], "Auto")
        draw_block(h_col3, "hydro_btn_trans", b_t["b3_title"], "🤝", b_t["b3_desc"], b_t["b3_list"], "TRANS")
        draw_block(h_col4, "hydro_btn_4", b_t["b4_title"], "📁", b_t["b4_desc"], b_t["b4_list"], "Cadastre")

    st.write("##")


    def render_hydro_chart(lang_code="ru"):
        # 1. СЛОВАРЬ ПЕРЕВОДОВ ДЛЯ ГРАФИКА
        chart_lang = {
            "ru": {
                "title": "Динамика развития гидрологической сети (1917-2026 гг.)",
                "xaxis": "Год",
                "yaxis": "Количество постов",
                "hover": "Количество постов",
                "anno": "Текущий статус (2026)"
            },
            "kz": {
                "title": "Гидрологиялық желінің даму динамикасы (1917-2026 жж.)",
                "xaxis": "Жыл",
                "yaxis": "Бекеттер саны",
                "hover": "Бекеттер саны",
                "anno": "Ағымдағы жағдайы (2026)"
            },
            "en": {
                "title": "Hydrological Network Development Dynamics (1917-2026)",
                "xaxis": "Year",
                "yaxis": "Number of Posts",
                "hover": "Number of Posts",
                "anno": "Current Status (2026)"
            }
        }
        
        # Получаем текущий перевод (по умолчанию русский)
        c_t = chart_lang.get(lang_code, chart_lang["ru"])

        # Данные
        years = [1917, 1938, 1940, 1972, 1981, 1985, 1987, 1992, 1995, 2000, 
                 2002, 2003, 2004, 2005, 2006, 2008, 2009, 2010, 2011, 2015, 
                 2018, 2020, 2021, 2024, 2025, 2026]
        posts = [123, 123, 150, 416, 506, 486, 432, 354, 322, 165, 
                 209, 206, 215, 226, 251, 276, 291, 292, 298, 302, 
                 310, 352, 377, 377, 410, 442]

        main_color = '#1f4e79'
        highlight_color = '#EF553B'
        colors = [main_color] * (len(years) - 1) + [highlight_color] 

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=years,
            y=posts,
            text=posts,
            textposition='outside',
            marker_color=colors, 
            # Используем перевод для всплывающей подсказки
            hovertemplate=f"<b>{c_t['xaxis']}: %{{x}}</b><br>{c_t['hover']}: %{{y}}<extra></extra>"
        ))

        fig.update_layout(
            title=dict(
                text=c_t['title'],
                font=dict(size=20)
            ),
            xaxis=dict(
                title=dict(text=c_t['xaxis'], font=dict(size=18)),
                type='category',
                tickangle=-45,
                tickfont=dict(size=14) # Немного уменьшил, чтобы года не слипались
            ),
            yaxis=dict(
                title=dict(text=c_t['yaxis'], font=dict(size=18)),
                range=[0, 600],
                showgrid=True,
                gridcolor='rgba(200, 200, 200, 0.2)',
                tickfont=dict(size=16)
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=60, r=20, t=80, b=80), 
            font=dict(color="white")
        )

        # Используем перевод для аннотации
        fig.add_annotation(
            x=len(years)-1, 
            y=442,
            text=c_t['anno'],
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
            font=dict(color=highlight_color, size=13, family="Arial Black")
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # --- 1. СЛОВАРЬ ПЕРЕВОДОВ ДЛЯ РЕГИОНОВ И ИНТЕРФЕЙСА ---
    regions_map = {
        "ru": [
            "Восточно-Казахстанская и Абайская", "Акмолинская", "Актюбинская", "Алматинская", "Атырауская", 
            "ЗКО", "Жамбылская", "Жетысу", "Карагандинская и Улытауская", "Костанайская", 
            "Кызылординская", "Мангистауская", "Павлодарская", "СКО", "Туркестанская"
        ],
        "kz": [
            "Шығыс Қазақстан және Абай", "Ақмола", "Ақтөбе", "Алматы", "Атырау", 
            "БҚО", "Жамбыл", "Жетісу", "Қарағанды және Ұлытау", "Қостанай", 
            "Қызылорда", "Маңғыстау", "Павлодар", "СҚО", "Түркістан"
        ],
        "en": [
            "East Kazakhstan & Abai", "Akmola", "Aktobe", "Almaty", "Atyrau", 
            "WKO", "Zhambyl", "Zhetysu", "Karaganda & Ulytau", "Kostanay", 
            "Kyzylorda", "Mangystau", "Pavlodar", "NKO", "Turkestan"
        ]
    }

    ui_labels = {
        "ru": {"sub": "📊 Мониторинг и информационная продукция", "graph": "### Региональная сеть", "axis": "Количество постов"},
        "kz": {"sub": "📊 Мониторинг және ақпараттық өнімдер", "graph": "### Өңірлік желі", "axis": "Бекеттер саны"},
        "en": {"sub": "📊 Monitoring & Information Products", "graph": "### Regional Network", "axis": "Number of Posts"}
    }

    # Текущий язык
    curr_lang = lang_code if 'lang_code' in locals() else "ru"
    labels = ui_labels.get(curr_lang, ui_labels["ru"])

    # --- 2. ПОДГОТОВКА ДАННЫХ ---
    data = {
        "Region": regions_map.get(curr_lang, regions_map["ru"]),
        "Count": [68, 45, 39, 40, 15, 30, 24, 32, 38, 28, 13, 7, 6, 27, 30]
    }

    df_posts = pd.DataFrame(data).sort_values(by="Count", ascending=True)
    top_3_cutoff = df_posts["Count"].nlargest(3).min()
    colors_posts = ['#FFA500' if x >= top_3_cutoff else '#1f4e79' for x in df_posts["Count"]]

    # --- 3. ОТРИСОВКА ---
    st.subheader(labels["sub"])
    col_graph, col_info = st.columns([2, 1], gap="large")

    with col_graph:
        st.markdown(labels["graph"])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df_posts["Region"], 
            x=df_posts["Count"],
            orientation='h', 
            marker_color=colors_posts,
            text=df_posts["Count"], 
            textposition='outside'
        ))
        
        fig.update_layout(
            height=700, 
            # l=250 чтобы длинные названия (особенно на KZ) не обрезались
            margin=dict(l=250, r=50, t=20, b=80), 
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font=dict(color="#1f4e79"),
            xaxis=dict(
                title=dict(text=labels["axis"], font=dict(size=18)),
                tickfont=dict(size=16),
                gridcolor='rgba(0,0,0,0.1)',
                automargin=True
            ),
            yaxis=dict(
                type='category', 
                tickfont=dict(size=16),
                automargin=True,
                title=dict(text="") 
            )
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        

    # --- 1. СЛОВАРЬ ПЕРЕВОДОВ (ОБЯЗАТЕЛЬНО ДОЛЖЕН БЫТЬ ТУТ) ---
    monitoring_lang = {
        "ru": {
            "prod_title": "### 📄 Выпускаемая продукция",
            "daily": "**📅 Ежедневные бюллетени**\n* Оперативные данные по уровням воды\n* Состояние снежного покрова в горах",
            "forecast": "**🌊 Прогнозы и кадастр**\n* Прогноз весеннего половодья\n* Государственный водный кадастр",
            "emergency": "**🚨 Экстренные оповещения**\n* Штормовые предупреждения (СГЯ)\n* Резкие подъемы уровней",
            "metric_label": "Общий охват сети",
            "top_3": "**Топ-3 региона:**",
            "help_text": "Данные на 2026 год"
        },
        "kz": {
            "prod_title": "### 📄 Шығарылатын өнімдер",
            "daily": "**📅 Күнделікті бюллетеньдер**\n* Су деңгейі бойынша жедел деректер\n* Таулардағы қар жамылғысының күйі",
            "forecast": "**🌊 Болжамдар және кадастр**\n* Көктемгі су тасқынының болжамы\n* Мемлекеттік су кадастры",
            "emergency": "**🚨 Шұғыл хабарламалар** \n* Дауылды ескертулер (ҚГҚ)\n* Деңгейлердің күрт көтерілуі",
            "metric_label": "Желінің жалпы қамтылуы",
            "top_3": "**Топ-3 өңір:**",
            "help_text": "2026 жылғы мәліметтер"
        },
        "en": {
            "prod_title": "### 📄 Deliverables",
            "daily": "**📅 Daily Bulletins**\n* Operational water level data\n* Mountain snow cover status",
            "forecast": "**🌊 Forecasts & Cadastre**\n* Spring flood forecast (annual)\n* State Water Cadastre",
            "emergency": "**🚨 Emergency Alerts**\n* Weather warnings (HWM)\n* Sudden water level rise alerts",
            "metric_label": "Total Network Coverage",
            "top_3": "**Top 3 Regions:**",
            "help_text": "2026 data"
        }
    }

    # 2. ОПРЕДЕЛЯЕМ ТЕКУЩИЙ ЯЗЫК И ПЕРЕМЕННУЮ m_t
    curr_lang = lang_code if 'lang_code' in locals() else "ru"
    m_t = monitoring_lang.get(curr_lang, monitoring_lang["ru"])

    # --- 3. ВАШ БЛОК ВЫВОДА ---
    with col_info:
        # Теперь m_t существует и ошибки не будет
        st.markdown(m_t["prod_title"])
        
        st.info(m_t["daily"])
        st.success(m_t["forecast"])
        st.warning(m_t["emergency"])
        
        st.divider()
        
        # Расчет метрики
        total_posts = df_posts['Count'].sum()
        st.metric(
            label=m_t["metric_label"], 
            value=f"{total_posts}", 
            help=m_t["help_text"]
        )
        
        st.write(m_t["top_3"])
        
        # Таблица ТОП-3
        top_3_df = df_posts.nlargest(3, 'Count')[['Region', 'Count']]
        display_columns = {
            "Region": "Область" if curr_lang != "en" else "Region",
            "Count": "Посты" if curr_lang == "ru" else ("Бекеттер" if curr_lang == "kz" else "Posts")
        }
        st.table(top_3_df.rename(columns=display_columns).set_index(display_columns["Region"]))
        
    # --- 1. СЛОВАРЬ ПЕРЕВОДОВ ИНТЕРФЕЙСА ---
    retro_ui = {
        "ru": {
            "title": "### 📜 Историческая память рек",
            "desc": "Сравните текущее состояние реки с самым масштабным наводнением в истории наблюдений.",
            "select": "Выберите реку для сравнения:",
            "hist_cap": "📊 ИСТОРИЧЕСКИЙ ПИК",
            "curr_cap": "🌊 ТЕКУЩИЙ УРОВЕНЬ",
            "unit": "см",
            "date": "13.04.2026"
        },
        "kz": {
            "title": "### 📜 Өзендердің тарихи жады",
            "desc": "Өзеннің ағымдағы жай-күйін бақылау тарихындағы ең ауқымды су тасқынымен салыстырыңыз.",
            "select": "Салыстыру үшін өзенді таңдаңыз:",
            "hist_cap": "📊 ТАРИХИ ШЫҢ",
            "curr_cap": "🌊 АҒЫМДАҒЫ ДЕҢГЕЙ",
            "unit": "см",
            "date": "13.04.2026"
        },
        "en": {
            "title": "### 📜 Historical River Memory",
            "desc": "Compare the current river status with the largest flood in recorded history.",
            "select": "Select a river to compare:",
            "hist_cap": "📊 HISTORICAL PEAK",
            "curr_cap": "🌊 CURRENT LEVEL",
            "unit": "cm",
            "date": "13.04.2026"
        }
    }

    # --- 2. ДАННЫЕ ДЛЯ РЕТРОСПЕКТИВЫ (Мультиязычные) ---
    HISTORICAL_DATA = {
        "Esil_Astana": {
            "name": {"ru": "р. Есиль (г. Астана)", "kz": "Есіл өз. (Астана қ.)", "en": "Esil River (Astana)"},
            "record_level": 742, "record_year": "18.04.2021", "current_level": 701, "danger_level": 742,
            "fact": {
                "ru": "В 2017 году уровень воды достиг рекордной отметки, что привело к заполнению дамбы.",
                "kz": "2017 жылы су деңгейі рекордтық шекке жетіп, бөгеттің толуына әкелді.",
                "en": "In 2017, the water level reached a record high, filling the protective dam."
            }
        },
        "Zhayik_Uralsk": {
            "name": {"ru": "р. Жайык (г. Уральск)", "kz": "Жайық өз. (Орал қ.)", "en": "Zhayik River (Uralsk)"},
            "record_level": 945, "record_year": "9.05.1942", "current_level": 349, "danger_level": 945,
            "fact": {
                "ru": "Исторический максимум зафиксирован в середине века. Сейчас уровень в норме.",
                "kz": "Тарихи максимум ғасыр ортасында тіркелді. Қазір деңгей қалыпты.",
                "en": "The historical maximum was recorded in the mid-century. Current levels are normal."
            }
        },
        "Ile_Dobyn": {
            "name": {"ru": "р. Иле (пр. Добын (КНР))", "kz": "Іле өз. (Добын (ҚХР))", "en": "Ile River (Dobyn, China)"},
            "record_level": 1980, "record_year": "08.05.2016", "current_level": 248, "danger_level": 1980,
            "fact": {
                "ru": "Максимальный уровень регулируется Бухтарминским каскадом ГЭС.",
                "kz": "Максималды деңгей Бұқтырма ГЭС каскадымен реттеледі.",
                "en": "The maximum level is regulated by the Bukhtarma HPP cascade."
            }
        },
        "Ilek_Aktobe": {
            "name": {"ru": "р. Илек (г. Актобе)", "kz": "Елек өз. (Ақтөбе қ.)", "en": "Ilek River (Aktobe)"},
            "record_level": 741, "record_year": "13.04.1941", "current_level": 137, "danger_level": 741,
            "fact": {
                "ru": "Уровень значительно зависит от весеннего снеготаяния в верховьях.",
                "kz": "Деңгей жоғарғы жағындағы көктемгі қардың еруіне байланысты.",
                "en": "The level significantly depends on spring snowmelt upstream."
            }
        },
        "Esil_Derzhavinsk": {
            "name": {"ru": "р. Есиль (г. Державинск)", "kz": "Есіл өз. (Державинск қ.)", "en": "Esil River (Derzhavinsk)"},
            "record_level": 1709, "record_year": "18.04.2024", "current_level": 433, "danger_level": 1709,
            "fact": {
                "ru": "В 2024 году зафиксирован абсолютный исторический рекорд уровня.",
                "kz": "2024 жылы деңгейдің абсолютті тарихи рекорды тіркелді.",
                "en": "In 2024, an absolute historical level record was recorded."
            }
        },
        "Talas_Zhasorken": {
            "name": {"ru": "р. Талас (а.Жасоркен)", "kz": "Талас өз. (Жасөркен а.)", "en": "Talas River (Zhasorken)"},
            "record_level": 378, "record_year": "06.11.2017", "current_level": 91, "danger_level": 378,
            "fact": {
                "ru": "Река имеет важное значение для орошения земель Жамбылской области.",
                "kz": "Өзен Жамбыл облысының жерлерін суару үшін маңызды маңызға ие.",
                "en": "The river is vital for irrigation in the Zhambyl region."
            }
        },
        "Nura_Sheshenkara": {
            "name": {"ru": "р. Нура (с. Шешенкара)", "kz": "Нұра өз. (Шешенқара а.)", "en": "Nura River (Sheshenkara)"},
            "record_level": 715, "record_year": "11.04.2015", "current_level": 400, "danger_level": 715,
            "fact": {
                "ru": "Паводки на Нуре часто угрожают населенным пунктам Карагандинской области.",
                "kz": "Нұрадағы тасқындар Қарағанды облысының елді мекендеріне жиі қауіп төндіреді.",
                "en": "Floods on the Nura often threaten settlements in the Karaganda region."
            }
        },
        "Tobyl_Kostanay": {
            "name": {"ru": "р. Тобыл (г. Костанай)", "kz": "Тобыл өз. (Қостанай қ.)", "en": "Tobyl River (Kostanay)"},
            "record_level": 730, "record_year": "12.04.2000", "current_level": 329, "danger_level": 730,
            "fact": {
                "ru": "Уровень регулируется каскадом водохранилищ (Верхне-Тобольское, Каратомарское).",
                "kz": "Деңгей су қоймалары каскадымен реттеледі.",
                "en": "The level is regulated by a cascade of reservoirs."
            }
        },
        "Syrdariya_Kokbulak": {
            "name": {"ru": "р. Сырдарья (с. Кокбулак)", "kz": "Сырдария өз. (Көкбұлақ а.)", "en": "Syrdarya River (Kokbulak)"},
            "record_level": 852, "record_year": "20.04.2003", "current_level": 591, "danger_level": 852,
            "fact": {
                "ru": "Главная водная артерия юга Казахстана, регулируемая Шардаринским вдхр.",
                "kz": "Оңтүстік Қазақстанның негізгі су артериясы, Шардара су қоймасымен реттеледі.",
                "en": "The main water artery of southern Kazakhstan, regulated by Shardara reservoir."
            }
        },
        "Ertis_Semey": {
            "name": {"ru": "р. Ертис (г. Семей)", "kz": "Ертіс өз. (Семей қ.)", "en": "Ertis River (Semey)"},
            "record_level": 635, "record_year": "11.04.1941", "current_level": 161, "danger_level": 635,
            "fact": {
                "ru": "Уровень воды в районе Семея зависит от сбросов Шульбинской ГЭС.",
                "kz": "Семей ауданындағы су деңгейі Шүлбі ГЭС-інің су жіберуіне байланысты.",
                "en": "The water level near Semey depends on releases from the Shulba HPP."
            }
        }
    }

    # --- 3. ЛОГИКА ОТОБРАЖЕНИЯ ---
    # Выбираем текущий язык (предполагаем, что lang_code определен ранее)
    lang = lang_code if 'lang_code' in locals() else "ru"
    ui = retro_ui[lang]

    st.markdown(ui["title"])
    st.write(ui["desc"])

    # Создаем список для выбора (отображаем названия на текущем языке)
    river_map = {v["name"][lang]: k for k, v in HISTORICAL_DATA.items()}
    river_choice = st.selectbox(ui["select"], list(river_map.keys()))

    # Данные выбранной реки
    selected_data = HISTORICAL_DATA[river_map[river_choice]]

    col_hist, col_curr = st.columns(2)

    with col_hist:
        st.markdown(f"""
            <div style="background-color: #f1f3f4; padding: 20px; border-radius: 15px; border-left: 8px solid #607d8b; min-height: 150px;">
                <h5 style="margin:0; color: #455a64;">{ui['hist_cap']}</h5>
                <h2 style="margin:0; color: #263238;">{selected_data['record_level']} {ui['unit']}</h2>
                <p style="font-weight: bold; color: #78909c;">{selected_data['record_year']} {"год" if lang=="ru" else ""}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_curr:
        status_color = "#2ecc71" if selected_data['current_level'] < selected_data['danger_level'] else "#e74c3c"
        st.markdown(f"""
            <div style="background-color: #e3f2fd; padding: 20px; border-radius: 15px; border-left: 8px solid {status_color}; min-height: 150px;">
                <h5 style="margin:0; color: #1565c0;">{ui['curr_cap']}</h5>
                <h2 style="margin:0; color: #0d47a1;">{selected_data['current_level']} {ui['unit']}</h2>
                <p style="font-weight: bold; color: #1e88e5;">{ui['date']}</p>
            </div>
        """, unsafe_allow_html=True)



    import streamlit as st
    import os
    import base64  # ОБЯЗАТЕЛЬНО ДОБАВЬТЕ ЭТУ СТРОКУ
                   
            
# 9. АГРОМЕТЕОРОЛОГИЧЕСКИЙ МОНИТОРИНГ

    # --- 1. ОПРЕДЕЛЕНИЕ СЛОВАРЕЙ (В самом начале блока) ---
    AGRO_CONTENT = {
        "ru": {
            "header_title": "Агрометеорологический мониторинг",
            "header_subtitle": "Гидрометеорологическое обеспечение продовольственной безопасности сельскохозяйственной отрасли Казахстана /на основе агрометеорологических наблюдений/",
            "map_title": "### 🗺️ Агрометеорологические наблюдения",
            "main_text": "Агрометеорологические наблюдения включают наблюдения за ростом и развитием сельскохозяйственных и пастбищных культур (с измерением параметров растений), за состоянием и увлажнением почвы, а также за основными метеорологическими параметрами.",
            "crops_title": "**Основные культуры:**",
            "crops": ["🌾 Зерновые", "🌽 Пропашные", "🌻 Масличные", "🍎 Плодовые"]
        },
        "kz": {
            "header_title": "Агрометеорологиялық мониторинг",
            "header_subtitle": "Қазақстанның ауыл шаруашылығы саласының азық-түлік қауіпсіздігін гидрометеорологиялық қамтамасыз ету /агрометеорологиялық бақылаулар негізінде/",
            "map_title": "### 🗺️ Агрометеорологиялық бақылаулар",
            "main_text": "Агрометеорологиялық бақылауларға ауыл шаруашылығы және жайылымдық дақылдардың өсуі мен дамуын бақылау (өсімдік параметрлерін өлшеумен), топырақтың жай-күйі мен ылғалдылығын бақылау кіреді.",
            "crops_title": "**Негізгі дақылдар:**",
            "crops": ["🌾 Дәнді дақылдар", "🌽 Пропашные дақылдар", "🌻 Майлы дақылдар", "🍎 Жеміс дақылдары"]
        },
        "en": {
            "header_title": "Agrometeorological Monitoring",
            "header_subtitle": "Hydrometeorological support for food security of the agricultural sector of Kazakhstan /based on agrometeorological observations/",
            "map_title": "### 🗺️ Agrometeorological Observations",
            "main_text": "Agrometeorological observations include monitoring the growth and development of agricultural and pasture crops, soil condition and moisture, as well as key meteorological parameters.",
            "crops_title": "**Main Crops:**",
            "crops": ["🌾 Cereals", "🌽 Row Crops", "🌻 Oilseeds", "🍎 Fruit Crops"]
        }
    }

    # --- 2. ЛОГИКА ОПРЕДЕЛЕНИЯ ЯЗЫКА ---
    # Сопоставляем то, что выбрал пользователь, с ключами словаря
    raw_lang = st.session_state.get('lang', 'Русский')
    lang_map = {"Русский": "ru", "Қазақша": "kz", "English": "en"}
    L = lang_map.get(raw_lang, "ru") # Короткая переменная для удобства

    # Получаем пакет текстов для текущего языка
    txt = AGRO_CONTENT[L]

    # --- 3. ВЫВОД ЗАГОЛОВКА (ИСПОЛЬЗУЯ ПЕРЕМЕННЫЕ) ---
    st.markdown(f"""
        <div style="text-align:center; margin: 40px 0 20px 0;">
            <h2 style="color: #1b5e20; font-family: 'Exo 2', sans-serif; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; font-size: 2.2em;">
                {txt['header_title']}
            </h2>
            <p style="color: #546e7a; font-size: 1.1em; font-weight: 500;">
                {txt['header_subtitle']}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- 4. ВЫВОД КАРТЫ И ОПИСАНИЯ ---
    st.markdown(txt["map_title"])

    col_map, col_text = st.columns([1.5, 0.5])

    with col_map:
        # Логика загрузки фото AGRO.jpg
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, "AGRO.jpg")
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/jpeg;base64,{data}" style="width:100%; border-radius:10px;">', unsafe_allow_html=True)
        else:
            st.error("Файл AGRO.jpg не найден!")

    with col_text:
        st.markdown("---")
        st.write(txt["main_text"]) # ТЕПЕРЬ ТУТ ПЕРЕМЕННАЯ
        st.markdown(txt["crops_title"])
        for crop in txt["crops"]:
            st.markdown(f"* {crop}")
            



    # Тексты для графика агроклиматических зон
    AGRO_ZONES_DATA = {
        "ru": {
            "title": "Агроклиматические зоны по областям",
            "legend_title": "Легенда зон:",
            "zones": {
                "I": "Слабо влажная умеренно-теплая", "II": "Засушливая умеренно-теплая", "III": "Засушливая теплая",
                "IV": "Очень засушливая теплая", "V": "Сухая теплая", "VI": "Сухая умеренно-теплая",
                "VII": "Очень сухая умеренно-жаркая", "VIII": "Очень сухая жаркая", "IX": "Очень сухая",
                "X": "Центрально-казахстанский мелкосопочник", "XI": "Предгорья Заилийского Алатау",
                "XIII": "Предгорья Джунгарского Алатау", "XIV": "Предгорья Северного и Западного Тянь-Шаня",
                "XV": "Долина р. Или", "XVI": "Горные районы"
            },
            "regions": {
                "АКМОЛА": "Акмолинская", "СКО": "СКО", "КОСТАНАЙ": "Костанайская", "ПАВЛОДАР": "Павлодарская",
                "ВКО": "ВКО и Абай", "ЗКО": "ЗКО", "АКТОБЕ": "Актюбинская", "КАРАГАНДЫ": "Карагандинская и Улытау",
                "АТЫРАУ": "Атырауская", "АЛМАТЫ": "Алматинская и Жетысу", "ЖАМБЫЛ": "Жамбылская",
                "МАНГИСТАУ": "Мангистауская", "ТУРКЕСТАН": "Туркестанская", "КЫЗЫЛОРДА": "Кызылординская"
            }
        },
        "kz": {
            "title": "Облыстар бойынша агроклиматтық аймақтар",
            "legend_title": "Аймақтардың шартты белгілері:",
            "zones": {
                "I": "Әлсіз ылғалды қоңыржай-жылы", "II": "Құрғақшылық қоңыржай-жылы", "III": "Құрғақшылық жылы",
                "IV": "Өте құрғақшылық жылы", "V": "Құрғақ жылы", "VI": "Құрғақ қоңыржай-жылы",
                "VII": "Өте құрғақ қоңыржай-ыстық", "VIII": "Өте құрғақ ыстық", "IX": "Өте құрғақ",
                "X": "Орталық Қазақстан ұсақ шоқысы", "XI": "Іле Алатауы етегі",
                "XIII": "Жетісу Алатауы етегі", "XIV": "Солтүстік және Батыс Тянь-Шань етегі",
                "XV": "Іле өзенінің аңғары", "XVI": "Таулы аймақтар"
            },
            "regions": {
                "АКМОЛА": "Ақмола", "СКО": "СҚО", "КОСТАНАЙ": "Қостанай", "ПАВЛОДАР": "Павлодар",
                "ВКО": "ШҚО және Абай", "ЗКО": "БҚО", "АКТОБЕ": "Ақтөбе", "КАРАГАНДЫ": "Қарағанды және Ұлытау",
                "АТЫРАУ": "Атырау", "АЛМАТЫ": "Алматы және Жетісу", "ЖАМБЫЛ": "Жамбыл",
                "МАНГИСТАУ": "Маңғыстау", "ТУРКЕСТАН": "Түркістан", "КЫЗЫЛОРДА": "Қызылорда"
            }
        },
        "en": {
            "title": "Agro-climatic Zones by Region",
            "legend_title": "Zone Legend:",
            "zones": {
                "I": "Slightly humid moderate-warm", "II": "Arid moderate-warm", "III": "Arid warm",
                "IV": "Very arid warm", "V": "Dry warm", "VI": "Dry moderate-warm",
                "VII": "Very dry moderate-hot", "VIII": "Very dry hot", "IX": "Very dry",
                "X": "Central Kazakh Uplands", "XI": "Trans-Ili Alatau Foothills",
                "XIII": "Dzungarian Alatau Foothills", "XIV": "Tien Shan Foothills",
                "XV": "Ili River Valley", "XVI": "Mountainous regions"
            },
            "regions": {
                "АКМОЛА": "Akmola", "СКО": "North Kazakhstan", "КОСТАНАЙ": "Kostanay", "ПАВЛОДАР": "Pavlodar",
                "ВКО": "East Kazakhstan & Abai", "ЗКО": "West Kazakhstan", "АКТОБЕ": "Aktobe", 
                "КАРАГАНДЫ": "Karaganda & Ulytau", "АТЫРАУ": "Atyrau", "АЛМАТЫ": "Almaty & Zhetysu",
                "ЖАМБЫЛ": "Zhambyl", "МАНГИСТАУ": "Mangystau", "ТУРКЕСТАН": "Turkistan", "КЫЗЫЛОРДА": "Kyzylorda"
            }
        }
    }

    # --- 2. ЛОГИКА ОПРЕДЕЛЕНИЯ ЯЗЫКА ---
    raw_lang = st.session_state.get('lang', 'Русский')
    lang_map = {"Русский": "ru", "Қазақша": "kz", "English": "en"}
    current_lang = lang_map.get(raw_lang, "ru")

    # --- 3. ВЕРХНИЙ ЗАГОЛОВОК ---
    header = HEADER_TRANSLATIONS[current_lang]
    st.markdown(f"""
        <div style="text-align:center; margin: 40px 0 20px 0;">
            <h2 style="color: #1b5e20; font-family: 'Exo 2', sans-serif; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; font-size: 2.2em;">
                {header['title']}
            </h2>
            <p style="color: #546e7a; font-size: 1.1em; font-weight: 500;">
                {header['subtitle']}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- 4. БЛОК С КАРТОЙ НАБЛЮДЕНИЙ ---
    agro_content = AGRO_MAP_TRANSLATIONS[current_lang]
    st.markdown(agro_content["title"])

    col_map, col_text = st.columns([1.5, 0.5])
    with col_map:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, "AGRO.jpg")
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<div style="display:flex;justify-content:center;"><img src="data:image/jpeg;base64,{data}" style="width:100%;max-width:800px;border-radius:10px;"></div>', unsafe_allow_html=True)
        else:
            st.warning("AGRO.jpg not found")

    with col_text:
        st.markdown("---")
        st.write(agro_content["main_text"])
        st.markdown(agro_content["crops_title"])
        for crop in agro_content["crops"]:
            st.markdown(f"* {crop}")

    # --- 5. ГРАФИК АГРОКЛИМАТИЧЕСКИХ ЗОН ---
    zone_content = AGRO_ZONES_DATA[current_lang]
    st.subheader(zone_content["title"])

    # Данные для графика
    raw_data = [
        ["АКМОЛА", "I", 6], ["АКМОЛА", "II", 31], ["АКМОЛА", "VI", 63],
        ["СКО", "I", 18], ["СКО", "II", 55], ["СКО", "III", 27],
        ["КОСТАНАЙ", "II", 11], ["КОСТАНАЙ", "III", 33], ["КОСТАНАЙ", "IV", 33], ["КОСТАНАЙ", "V", 11], ["КОСТАНАЙ", "VI", 6], ["КОСТАНАЙ", "VII", 6],
        ["ПАВЛОДАР", "II", 7], ["ПАВЛОДАР", "IV", 60], ["ПАВЛОДАР", "VI", 20], ["ПАВЛОДАР", "XIV", 13],
        ["ВКО", "II", 29], ["ВКО", "IV", 13], ["ВКО", "VI", 17], ["ВКО", "VII", 24], ["ВКО", "XVI", 17],
        ["ЗКО", "IV", 31], ["ЗКО", "V", 8], ["ЗКО", "VI", 46], ["ЗКО", "VII", 15],
        ["АКТОБЕ", "IV", 47], ["АКТОБЕ", "VI", 6], ["АКТОБЕ", "VII", 41], ["АКТОБЕ", "VIII", 6],
        ["КАРАГАНДЫ", "IV", 13], ["КАРАГАНДЫ", "V", 13], ["КАРАГАНДЫ", "VI", 8], ["КАРАГАНДЫ", "VII", 42], ["КАРАГАНДЫ", "VIII", 8], ["КАРАГАНДЫ", "XIV", 16],
        ["АТЫРАУ", "VII", 33], ["АТЫРАУ", "VIII", 67],
        ["АЛМАТЫ", "VII", 16], ["АЛМАТЫ", "VIII", 6], ["АЛМАТЫ", "XI", 9], ["АЛМАТЫ", "XIII", 9], ["АЛМАТЫ", "XIV", 3], ["АЛМАТЫ", "XV", 13], ["АЛМАТЫ", "XVI", 44],
        ["ЖАМБЫЛ", "VII", 8], ["ЖАМБЫЛ", "XIV", 54], ["ЖАМБЫЛ", "XVI", 38],
        ["МАНГИСТАУ", "VIII", 90], ["МАНГИСТАУ", "IX", 10],
        ["ТУРКЕСТАН", "VIII", 8], ["ТУРКЕСТАН", "XIV", 42], ["ТУРКЕСТАН", "XVI", 50],
        ["КЫЗЫЛОРДА", "VIII", 63], ["КЫЗЫЛОРДА", "IX", 37]
    ]

    zones_colors = {
        "I": "#385e26", "II": "#66ff66", "III": "#92d050", "IV": "#ffff00", 
        "V": "#e6db98", "VI": "#f8cbad", "VII": "#f1a1eb", "VIII": "#ff8080", 
        "IX": "#ff0000", "X": "#bf9000", "XI": "#c00000", "XIII": "#843c0c", 
        "XIV": "#7f6000", "XV": "#00b0f0", "XVI": "#bcbcbc"
    }

    df = pd.DataFrame(raw_data, columns=["Key", "Зона", "Процент"])
    df["Область"] = df["Key"].map(zone_content["regions"])

    col_chart, col_legend = st.columns([4, 1.2])

    with col_chart:
        fig = go.Figure()
        for zone, color in zones_colors.items():
            df_zone = df[df["Зона"] == zone]
            if not df_zone.empty:
                fig.add_trace(go.Bar(
                    name=zone, y=df_zone["Область"], x=df_zone["Процент"], orientation='h',
                    marker=dict(color=color), text=df_zone["Процент"],
                    hovertext=[zone_content["zones"][zone]] * len(df_zone),
                    hovertemplate="<b>%{hovertext}</b>: %{x}%<extra></extra>"
                ))
        fig.update_layout(
            barmode='stack', height=700, margin=dict(l=200, r=20, t=20, b=50),
            xaxis=dict(range=[0, 100]), yaxis=dict(autorange="reversed", type='category'),
            showlegend=False, plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_legend:
        st.write(f"**{zone_content['legend_title']}**")
        for zone, color in zones_colors.items():
            st.markdown(f'''
                <div style="display:flex; align-items:flex-start; margin-bottom:4px;">
                    <div style="min-width:14px; height:14px; background-color:{color}; margin-right:8px; margin-top:3px; border:1px solid #444;"></div>
                    <div style="font-size:0.85rem; line-height:1.2;"><strong>{zone}</strong>: {zone_content["zones"][zone]}</div>
                </div>
            ''', unsafe_allow_html=True)
            


    import streamlit as st
    from PIL import Image
    import os

    def render_agro_climate_comparison():
        st.markdown("---")
        # Заголовок блока
        st.markdown("### 🌡️ Анализ агроклиматических показателей")

        # Пути к файлам (используем ваши локальные пути)
        path_temp2 = "agro2.jpg"
        path_gtk = "agro 3.png"

# Функция для перевода картинки в HTML-строку (делаем крупнее через width)
        def img_to_html(img_path, width=115):
            if os.path.exists(img_path):
                with open(img_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")
                return f'<img src="data:image/jpeg;base64,{data}" style="width: {width}%; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
            return None

        # Создаем две колонки
        col_left, col_right = st.columns(2)

        with col_left:
            st.info("Суммы эффективных температур воздуха (норма)")
            html_img_temp = img_to_html(path_temp2, width=100)
            if html_img_temp:
                st.markdown(html_img_temp, unsafe_allow_html=True)
                st.caption("Карта температур за август")
            else:
                st.error(f"Файл не найден: {path_temp2}")

        with col_right:
            st.info("Гидротермический коэффициент (ГТК) Селянинова")
            html_img_gtk = img_to_html(path_gtk, width=115)
            if html_img_gtk:
                st.markdown(html_img_gtk, unsafe_allow_html=True)
                st.caption("ГТК за период 1991-2020 гг.")
            else:
                st.error(f"Файл не найден: {path_gtk}")
                
    # Вызов функции в основном теле приложения
    render_agro_climate_comparison()


        # 10. ЭКОЛОГИЧЕСКИЙ МОНИТОРИНГ
    import streamlit as st

        # --- 10. ЭКОЛОГИЧЕСКИЙ МОНИТОРИНГ ---
    st.markdown("""
            <style>
            .monitor-card {
                background: #ffffff; 
                padding: 20px; 
                border-radius: 15px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
                height: 280px; 
                transition: transform 0.3s ease;
                border-top: 5px solid;
                margin-bottom: 20px;
                display: flex;
                flex-direction: column;
            }
            .monitor-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 12px 24px rgba(0,0,0,0.12);
            }
            .monitor-title {
                font-weight: 800;
                font-size: 1.5em;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 8px;
                text-transform: uppercase;
            }
            .stat-badge {
                background: #f0f2f6;
                padding: 2px 8px;
                border-radius: 5px;
                font-weight: bold;
                color: #003366;
            }
            </style>
            
            <div style="text-align:center; margin: 40px 0 30px 0;">
                <h2 style="color: #003366; font-family: 'Exo 2'; font-weight: 800; text-transform: uppercase; letter-spacing: 2px;">
                    Экологический мониторинг Казахстана
                </h2>
                <p style="color: #546e7a; font-size: 1.2em;">Государственная сеть наблюдения за качеством природной среды</p>
            </div>
        """, unsafe_allow_html=True)

    # --- ПЕРВЫЙ РЯД КАРТОЧЕК ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="monitor-card" style="border-top-color: #004A99;">
                <div class="monitor-title" style="color: #004A99;">📡 Атмосферный воздух</div>
                <p style="font-size: 1.0em; color: #455a64;">Контроль в <b>70</b> городах на <b>175</b> постах.</p>
                <div style="font-size: 1.2em; line-height: 1.4;">
                    • <b>131</b> автоматический пост<br>
                    • <b>44</b> поста ручного отбора<br>
                    • Определение <b>30+</b> показателей (PM2.5, PM10, ЛОС, тяжелые металлы)
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="monitor-card" style="border-top-color: #0288d1;">
                <div class="monitor-title" style="color: #0288d1;">💧 Поверхностные воды</div>
                <p style="font-size: 1.0em; color: #455a64;"><b>373</b> створа на <b>134</b> водных объектах.</p>
                <div style="font-size: 1.2em; line-height: 1.4;">
                    • 88 рек, 29 озер, 13 вдхр, Каспийское море<br>
                    • <b>60</b> физико-химических показателей<br>
                    • Анализ состава и трансграничных потоков
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="monitor-card" style="border-top-color: #8d6e63;">
                <div class="monitor-title" style="color: #8d6e63;">🌱 Загрязнение почв</div>
                <p style="font-size: 1.0em; color: #455a64;">Мониторинг в <b>101</b> точке наблюдения.</p>
                <div style="font-size: 1.2em; line-height: 1.4;">
                    • Отбор проб 3 раза в год<br>
                    • Контроль тяжелых металлов и нефтепродуктов<br>
                    • Анализ зон промышленных районов
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- ВТОРОЙ РЯД КАРТОЧЕК ---
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
            <div class="monitor-card" style="border-top-color: #4fc3f7;">
                <div class="monitor-title" style="color: #03a9f4;">❄️ Осадки и снег</div>
                <p style="font-size: 1.0em; color: #455a64;">Анализ кислотности и анионно-катионного состава.</p>
                <div style="font-size: 1.2em; line-height: 1.4;">
                    • <b>47</b> станций (осадки - ежемесячно)<br>
                    • <b>40</b> станций (снег - 1 раз в год)<br>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
            <div class="monitor-card" style="border-top-color: #f44336;">
                <div class="monitor-title" style="color: #d32f2f;">☢️ Радиационный фон</div>
                <p style="font-size: 1.0em; color: #455a64;">Измерение гамма-излучения и бета-активности.</p>
                <div style="font-size: 1.2em; line-height: 1.4;">
                    • <b>89</b> метеостанций (гамма-фон)<br>
                    • <b>43</b> станции (бета-активность)<br>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
            <div class="monitor-card" style="border-top-color: #ff9800;">
                <div class="monitor-title" style="color: #ef6c00;">📍 Особый мониторинг</div>
                <p style="font-size: 1.0em; color: #455a64;">Трансграничные реки и фоновый статус.</p>
                <div style="font-size: 1.2em; line-height: 1.4;">
                    • <b>32</b> трансграничные реки (РФ, КНР, КР, УЗ)<br>
                    • <b>СКФМ «Боровое»</b>: единственная станция комплексного фонового мониторинга
                </div>
            </div>
        """, unsafe_allow_html=True)
        

        # --- ХАЙЛАЙТЫ ПО ЭКОЛОГИИ ---
    st.markdown("""
            <style>
            .eco-highlight-container {
                display: flex;
                justify-content: space-between;
                gap: 10px;
                margin: 20px 0;
            }
            .eco-card {
                flex: 1;
                background: #f8f9fa;
                border-radius: 12px;
                padding: 15px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                border-bottom: 4px solid #003366;
                transition: transform 0.2s;
            }
            .eco-card:hover {
                transform: scale(1.02);
                background: #ffffff;
            }
            .eco-val {
                font-size: 1.8em;
                font-weight: 800;
                color: #003366;
                margin-bottom: 2px;
            }
            .eco-label {
                font-size: 0.8em;
                color: #546e7a;
                text-transform: uppercase;
                font-weight: 600;
                letter-spacing: 0.5px;
                line-height: 1.2;
            }
            .eco-icon {
                font-size: 1.8em;
                margin-bottom: 5px;
                display: block;
            }
            </style>
            
            <div class="eco-highlight-container">
                <div class="eco-card" style="border-bottom-color: #004A99;">
                    <span class="eco-icon">🏙️</span>
                    <div class="eco-val">70</div>
                    <div class="eco-label">Населенных пунктов под мониторингом</div>
                </div>
                <div class="eco-card" style="border-bottom-color: #0288d1;">
                    <span class="eco-icon">📍</span>
                    <div class="eco-val">175</div>
                    <div class="eco-label">Постов наблюдения за воздухом</div>
                </div>
                    <div class="eco-card" style="border-bottom-color: #7b1fa2;">
                    <span class="eco-icon">📱</span>
                    <div class="eco-val">131</div>
                    <div class="eco-label">Автоматических постов</div>
                </div> 
                <div class="eco-card" style="border-bottom-color: #43a047;">
                    <span class="eco-icon">🌊</span>
                    <div class="eco-val">373</div>
                    <div class="eco-label">Гидрохимических створа</div>
                </div>
                <div class="eco-card" style="border-bottom-color: #fbc02d;">
                    <span class="eco-icon">🧪</span>
                    <div class="eco-val">60+</div>
                    <div class="eco-label">Показателей качества воды</div>
                </div>
                <div class="eco-card" style="border-bottom-color: #d32f2f;">
                    <span class="eco-icon">☢️</span>
                    <div class="eco-val">89</div>
                    <div class="eco-label">Станций радиационного фона</div>
            </div>
        """, unsafe_allow_html=True)

        # --- УЛУЧШЕННЫЙ БЛОК: ИНФОРМАЦИОННЫЕ РЕСУРСЫ И БЮЛЛЕТЕНИ ---
    st.markdown("""
            <div style="margin: 40px 0 20px 0; border-left: 10px solid #003366; padding-left: 20px;">
                <h2 style="color: #003366; font-family: 'Exo 2'; font-weight: 800; margin: 0;">
                    ИНФОРМАЦИОННАЯ ПРОДУКЦИЯ
                </h2>
                <p style="color: #546e7a; margin: 5px 0 0 0;">Официальные отчеты, бюллетени и цифровые сервисы</p>
            </div>
        """, unsafe_allow_html=True)

        # Группировка продукции по категориям через контейнеры
    with st.container():
            col_a, col_b = st.columns(2)

            with col_a:
                with st.expander("📂 Ежедневная и еженедельная отчетность", expanded=True):
                    st.markdown("""
                        * **Бюллетень состояния воздуха:** Данные по 70 населенным пунктам и прогноз НМУ.  
                        * **Прогноз УФ-индекса:** Еженедельный мониторинг уровней солнечной радиации.  
                        * **НМУ:** Прогноз НМУ по 22 городам.
                    """)


            with col_b:
                with st.expander("🔬 Специализированные данные", expanded=True):
                    st.markdown("""
                        * **Трансграничный перенос:** Бюллетень по токсичным компонентам и их перемещению.  
                        * **Радиационный отчет:** Сводка по гамма-фону и бета-активности атмосферы.  
                    """)

    with st.container():
        # Создаем визуальную рамку с помощью markdown, но контент внутри - стандартный
        st.markdown("---") # Линия-разделитель
        
        col_text, col_btn = st.columns([3, 1])
        
        with col_text:
            st.subheader("📱 МОБИЛЬНОЕ ПРИЛОЖЕНИЕ AirKZ")
            st.write("""
                Получайте актуальные данные о качестве атмосферного воздуха в реальном времени. 
                Сервис охватывает все города Казахстана и предоставляет информацию с автоматических станций мониторинга **ежечасно**.
            """)
            st.caption("• Прогноз НМУ • Уровни загрязнения • Интерактивная карта")
            
        with col_btn:
            # Добавляем отступ сверху, чтобы кнопка была по центру текста
            st.write("##") 
            st.link_button("СКАЧАТЬ ПРИЛОЖЕНИЕ", "https://play.google.com/store/apps/details?id=kz.khm.airkz", use_container_width=True)
        
# --- ФИНАЛЬНЫЙ ПОДВАЛ (WHITE FOOTER) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="background: #ffffff; padding: 40px; border-radius: 30px 30px 0 0; color: #001f3f; text-align: center; border-top: 1px solid #eaeaea; box-shadow: 0px -5px 15px rgba(0,0,0,0.02);">
        <p style="opacity: 0.8; font-size: 1.1rem; max-width: 800px; margin: 0 auto 25px auto; color: #444;">
            Обеспечение экологической и метеорологической безопасности Республики Казахстан через ведение непрерывного мониторинга атмосферного воздуха, водных ресурсов и климатических изменений.
        </p>
        <div style="display: flex; justify-content: center; gap: 30px; font-weight: 600; flex-wrap: wrap;">
            <span><a href="https://www.kazhydromet.kz" target="_blank" style="color: #001f3f; text-decoration: none;">🌐 www.kazhydromet.kz</a></span>
            <span><a href="mailto:info@meteo.kz" style="color: #001f3f; text-decoration: none;">📧 info@meteo.kz</a></span>
            <span><a href="tel:+77172798394" style="color: #001f3f; text-decoration: none;">📞 +7 (7172) 79-83-94</a></span>
        </div>
        <hr style="opacity: 0.1; margin: 25px 0; border: 0; border-top: 1px solid #001f3f;">
        <p style="font-size: 0.8rem; opacity: 0.6; letter-spacing: 1px; color: #666;">
            © 2026 РГП «КАЗГИДРОМЕТ» 
        </p>
    </div>
""", unsafe_allow_html=True)

    
# ПРОГНОЗ ПОГОДЫ   
with tabs[2]:
    # Заголовок с кастомным цветом
    st.markdown("""
        <h1 style='color: #1E3A8A; font-family: sans-serif;'>
            🌦️ Гидрометцентр Казахстана: Оперативность. Безопасность.
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

    import streamlit as st

    # Добавляем стили (если они еще не добавлены в коде выше)
    st.markdown("""
        <style>
        .forecast-card {
            background: #f8fafc;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            text-align: center;
            transition: all 0.3s ease;
            min-height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        .forecast-card:hover {
            border-color: #3b82f6;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            background: #ffffff;
        }
        .forecast-card .icon {
            font-size: 3rem;
            margin-bottom: 12px;
        }
        .forecast-card .title {
            color: #1e293b;
            font-weight: 700;
            font-size: 1.2rem;
            margin-bottom: 8px;
            line-height: 1.2;
        }
        .forecast-card .description {
            color: #64748b;
            font-size: 1.0rem;
            line-height: 1.4;
        }
        </style>
    """, unsafe_allow_html=True)

    # Создаем 5 колонок
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("""
            <div class="forecast-card">
                <div class="icon">⚡</div>
                <div class="title">Наукастинг<br>(2-6 часов)</div>
                <div class="description">Сверхкраткосрочные данные.</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="forecast-card">
                <div class="icon">📅</div>
                <div class="title">Краткосрочные прогнозы</div>
                <div class="description">Детальная сводка на 1-3 дня, неделю.</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="forecast-card">
                <div class="icon">🔭</div>
                <div class="title">Долгосрочные прогнозы</div>
                <div class="description">Прогнозы на декаду, месяц и сезон.</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="forecast-card">
                <div class="icon">⚠️</div>
                <div class="title">Специализированные прогнозы</div>
                <div class="description">Прогноз неблагоприятных метеорологических условии, по горной территории, пожарной опасности.</div>
            </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
            <div class="forecast-card">
                <div class="icon">🏔️</div>
                <div class="title">Штормовые предупреждения</div>
                <div class="description">Об опасных ОЯ и СГЯ.</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🕒 Горизонты планирования")

    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; background: #f8f9fa; padding: 20px; border-radius: 50px; border: 1.2px solid #dee2e6;">
        <div style="text-align: center;"><strong>2-6 ч</strong><br><small>Наукастинг</small></div>
        <div style="color: #2563EB;">➡</div>
        <div style="text-align: center;"><strong>1-3 дня</strong><br><small>Краткосрочный</small></div>
        <div style="color: #2563EB;">➡</div>
        <div style="text-align: center;"><strong>10 дней</strong><br><small>Среднесрочный</small></div>
        <div style="color: #2563EB;">➡</div>
        <div style="text-align: center;"><strong>Месяц+</strong><br><small>Долгосрочный</small></div>
    </div>
    """, unsafe_allow_html=True)
    

    # Заголовок блока
    st.markdown("<h3 style='text-align: center; color: #1E3A8A;'>📊 Средняя оправдываемость прогнозов</h3>", unsafe_allow_html=True)

    # Верхний ряд: Основные метрики (интерактивные "кнопки")
    col_acc1, col_acc2, col_acc3, col_acc4, col_acc5, col_acc6   = st.columns(6)
    with col_acc1:
        st.metric("Суточные прогнозы", "96%", help="Высочайшая точность подтверждена верификацией")
    with col_acc2:
        st.metric("Прогнозы на 2-3 дня", "92%")
    with col_acc3:
        st.metric("Прогнозы на неделю", "91%")
    with col_acc4:
        st.metric("Прогнозы на декаду", "87%")
    with col_acc5:
        st.metric("Прогнозы на месяц", "70%")
    with col_acc6:
        st.metric("Прогнозы на сезон", "60%")
    st.divider()


    # --- Блок 3. Источники данных и Инфраструктура ---
    st.markdown("<h2 style='text-align: center; color: #1E3A8A; margin-top: 50px;'>📊 Информационная база данных</h2>", unsafe_allow_html=True)

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

    import streamlit as st

    # --- CSS ДЛЯ КАРТОЧЕК ---
    st.markdown("""
        <style>
            .data-box {
                padding: 15px;
                border-radius: 0 0 12px 12px; /* Скругляем только низ, так как сверху картинка */
                border-left: 5px solid;
                background: #ffffff;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                min-height: 280px;
                margin-bottom: 20px;
            }
            .data-title {
                font-weight: bold;
                font-size: 1.1em;
                margin-bottom: 10px;
                color: #1f2937;
            }
            .data-list {
                font-size: 0.9em;
                padding-left: 20px;
                color: #4b5563;
            }
            .card-img {
                width: 100%;
                height: 150px;
                object-fit: cover;
                border-radius: 12px 12px 0 0; /* Скругляем верх картинки */
            }
        </style>
    """, unsafe_allow_html=True)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # 1. ОСНОВНЫЕ ПУТИ
    IMG_DIR = os.path.join(BASE_DIR)

    # 2. ФУНКЦИЯ ДЛЯ ОТРИСОВКИ КАРТОЧКИ С ЛОКАЛЬНЫМ ФАЙЛОМ
    def draw_data_card(col, file_name, title, color, items):
        path = os.path.join(IMG_DIR, file_name)
        with col:
            # Пытаемся отобразить картинку/гифку
            if os.path.exists(path):
                st.image(path, use_container_width=True)
            else:
                # Если файла нет, оставляем пустое место или заглушку, чтобы блоки не прыгали
                st.warning(f"Файл {file_name} не найден")
            
            # HTML-контент карточки
            list_html = "".join([f"<li>{item}</li>" for item in items])
            st.markdown(f"""
                <div class="data-box" style="border-left-color: {color};">
                    <div class="data-title">{title}</div>
                    <ul class="data-list">
                        {list_html}
                    </ul>
                </div>
            """, unsafe_allow_html=True)

    # 3. ОБЩИЙ CSS
    st.markdown("""
        <style>
            .data-box {
                padding: 15px;
                border-radius: 0 0 12px 12px;
                border-left: 5px solid;
                background: #ffffff;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                min-height: 280px; /* Немного увеличил, чтобы текст влезал */
                margin-bottom: 20px;
            }
            .data-title { font-weight: bold; font-size: 1.1em; margin-bottom: 10px; color: #1f2937; }
            .data-list { font-size: 0.85em; padding-left: 20px; color: #4b5563; line-height: 1.4; }
            .data-list b { color: #1f2937; }
        </style>
    """, unsafe_allow_html=True)

    # 4. СОЗДАНИЕ КОЛОНОК И ВЫЗОВ ФУНКЦИЙ
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)

    draw_data_card(
        col_d1, "station1.gif", "📍 Наземная сеть", "#3b82f6", 
        [
            "<b>МС:</b> Непрерывный мониторинг параметров 24/7.",
            "<b>Аэрология:</b> Зондирование атмосферы до 30 км.",
            "<b>ДМРЛ:</b> Локаторы для детекции града и шквалов."
        ]
    )

    draw_data_card(
        col_d2, "station2.gif", "🗺️ Аналитика", "#10b981", 
        [
            "<b>АРМ ГИС-Метео, Metcap+:</b> Построение синоптических карт.",
            "<b>ГСТ ВМО:</b> Обмен данными.",
            "<b>Сетки:</b> Анализ полей метеопараметров."
        ]
    )

    draw_data_card(
        col_d3, "station3.gif", "📡 Спутники", "#8b5cf6", 
        [
            "<b>EUMETSAT:</b> Европейские геостационары.",
            "<b>FengYun:</b> Оперативные данные из КНР.",
            "<b>Метеор-М:</b> Российские орбитальные системы."
        ]
    )

    draw_data_card(
        col_d4, "station4.gif", "⚙️ Численные модели", "#f59e0b", 
        [
            "<b>ECMWF:</b> Глобальные прогнозы до 9 км.",
            "<b>ICON, COSMO:</b> Высокоточные мезомасштабные модели.",
            "<b>WRF-Kaz:</b> Локальная модель Казгидромет.",
            
        ]
    )

        # Визуальный разделитель с пояснением
    st.warning("""
            💡 **Интеграция данных:** Все потоки информации стекаются в единый прогностический центр, 
            где дежурная смена синоптиков проводит финальный анализ и верификацию перед выпуском бюллетеней.
        """)
    st.divider()
    
    import streamlit as st

    # Стили для сохранения разделения блоков и цветового фона
    st.markdown("""
        <style>
        .alert-header {
            text-align: center; 
            color: #1E3A8A; 
            margin: 50px 0 30px 0;
            font-family: 'Exo 2', sans-serif;
            font-weight: 800;
            text-transform: uppercase;
        }
        .alert-card-base {
            border-radius: 12px;
            padding: 25px;
            min-height: 300px;
            border: 1px solid;
        }
        /* Цвета для блока Штормовых предупреждений */
        .storm-bg {
            background: #fff5f5;
            border-color: #feb2b2;
        }
        /* Цвета для блока НМУ */
        .nmu-bg {
            background: #edf2f7;
            border-color: #cbd5e0;
        }
        .alert-badge {
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 15px;
            display: inline-block;
        }
        .alert-title {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 12px;
        }
        .info-row {
            margin-bottom: 10px;
            font-size: 1.1rem;
            color: #2d3748;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='alert-header'>📢 Оперативное реагирование</h2>", unsafe_allow_html=True)

    col_reg1, col_reg2 = st.columns(2)

    with col_reg1:
        # Оставляем розовый фон для штормовых
        st.markdown("""
            <div class="alert-card-base storm-bg">
                <div class="alert-badge" style="background: #e53e3e;">Экстренная сводка</div>
                <div class="alert-title" style="color: #9b2c2c;">Штормовые предупреждения</div>
                <p style="font-size: 0.9rem; color: #4a5568; margin-bottom: 15px;">
                    Оперативное оповещение о возникновении <b>ОЯ</b> (опасных) и <b>СГЯ</b> (стихийных) гидрометеорологических явлений.
                </p>
                <div class="info-row"><b>⏱ Заблаговременность:</b> от 6 до 48 часов</div>
                <div class="info-row"><b>📍 Масштаб:</b> Области, города, ключевые трассы</div>
                <div class="info-row"><b>📊 Состав:</b> Интенсивность, время, рекомендации</div>
                <div class="info-row"><b>📲 Рассылка:</b> Darmen, SMS-112, телеканалы</div>
            </div>
        """, unsafe_allow_html=True)

    with col_reg2:
        # Оставляем серо-голубой фон для НМУ
        st.markdown("""
            <div class="alert-card-base nmu-bg">
                <div class="alert-badge" style="background: #4a5568;">Экологический контроль</div>
                <div class="alert-title" style="color: #2d3748;">Прогнозы НМУ</div>
                <p style="font-size: 0.9rem; color: #4a5568; margin-bottom: 15px;">
                    Прогноз метеорологических условий, способствующих накоплению вредных веществ в приземном слое атмосферы.
                </p>
                <div class="info-row"><b>🏭 Режим работы:</b> Регулирование выбросов предприятий</div>
                <div class="info-row"><b>🏙 География:</b> Крупные промышленные центры РК</div>
                <div class="info-row"><b>🌥 Критерии:</b> Штиль, температурная инверсия</div>
                <div class="info-row"><b>🔄 Регулярность:</b> Выпускается ежедневно до 15:00</div>
            </div>
        """, unsafe_allow_html=True)
    st.divider()
    
    import streamlit as st
    import streamlit.components.v1 as components

    st.set_page_config(layout="wide")

    html_content = """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body { background-color: transparent; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; justify-content: center; overflow: hidden; }
        
        .flowchart-wrapper {
            width: 1100px; /* Немного расширил общую область */
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            position: relative;
        }

        /* Анимированные линии */
        .flow-line-svg {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: -1;
            pointer-events: none;
        }

        .path-line {
            fill: none;
            stroke: #d1d8e0;
            stroke-width: 2.5;
            stroke-dasharray: 12, 6;
            animation: flow 20s linear infinite;
        }

        @keyframes flow {
            to { stroke-dashoffset: -500; }
        }

        /* Главный узел - Увеличен шрифт до 18px */
        .main-node {
            background: linear-gradient(135deg, #00b09b, #96c93d);
            color: white;
            padding: 18px 40px;
            border-radius: 60px;
            text-align: center;
            font-weight: 800;
            font-size: 20px;
            margin-bottom: 45px;
            box-shadow: 0 6px 20px rgba(0,176,155,0.3);
            border: 3px solid #fff;
            transition: all 0.3s ease;
        }

        .columns-container {
            display: flex;
            justify-content: space-between;
            width: 100%;
            gap: 25px;
        }

        .branch { width: 260px; display: flex; flex-direction: column; gap: 18px; }

        /* Блоки - Увеличен шрифт до 14px */
        .node {
            padding: 15px;
            border-radius: 14px;
            text-align: center;
            font-size: 14px;
            font-weight: 600;
            color: white;
            min-height: 75px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            line-height: 1.4;
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.1);
        }

        .node:hover {
            transform: scale(1.03);
            box-shadow: 0 12px 25px rgba(0,0,0,0.15);
        }

        .blue { background: linear-gradient(135deg, #3498db, #2980b9); }
        .orange { background: linear-gradient(135deg, #f39c12, #e67e22); min-height: 180px; font-size: 15px; }
        .green { background: linear-gradient(135deg, #2ecc71, #27ae60); }
        .purple { background: linear-gradient(135deg, #9b59b6, #8e44ad); }
        
        .red { 
            background: linear-gradient(135deg, #e74c3c, #c0392b); 
            animation: critical-pulse 2s infinite;
            font-weight: 700;
            font-size: 15px;
        }

        @keyframes critical-pulse {
            0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.5); }
            70% { box-shadow: 0 0 0 15px rgba(231, 76, 60, 0); }
            100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
        }

        .node-row { display: flex; gap: 12px; width: 100%; }
        .node-row .node { flex: 1; padding: 10px; font-size: 12px; }

        i { margin-right: 10px; font-size: 18px; }
    </style>

    <div class="flowchart-wrapper">
        <svg class="flow-line-svg">
            <path class="path-line" d="M 550 70 V 130 H 150 V 160" />
            <path class="path-line" d="M 550 70 V 160" />
            <path class="path-line" d="M 550 130 H 950 V 160" />
            <path class="path-line" d="M 550 130 H 700 V 160" />
        </svg>

        <div class="main-node">
            <i class="fas fa-satellite-dish"></i>КАЗГИДРОМЕТ<br>Штормовое предупреждение
        </div>

        <div class="columns-container">
            <div class="branch">
                <div class="node blue"><i class="fas fa-shield-alt"></i>МЧС РК</div>
                <div class="node-row">
                    <div class="node blue">Командный центр планирования</div>
                    <div class="node blue">Департаменты по ЧС (ДЧС)</div>
                </div>
                <div class="node-row">
                    <div class="node red"><i class="fas fa-sms"></i>SMS 112</div>
                    <div class="node red"><i class="fas fa-mobile-alt"></i>DARMEN</div>
                </div>
            </div>

            <div class="branch">
                <div class="node orange">
                    <i class="fas fa-university"></i>
                    Государственные и местные исполнительные органы (Министерства, Акиматы)
                </div>
            </div>

            <div class="branch">
                <div class="node green"><i class="fas fa-map-marked-alt"></i>Карта Метеоалерт</div>
                <div class="node green"><i class="fas fa-code-branch"></i>Протокол CAP</div>
            </div>

            <div class="branch">
                <div class="node purple"><i class="fas fa-globe"></i>Сайт Казгидромета</div>
                <div class="node purple"><i class="fas fa-share-alt"></i>Социальные сети</div>
                <div class="node purple"><i class="fas fa-tv"></i>СМИ</div>
            </div>
        </div>
    </div>
    """

    st.markdown("<h2 style='text-align: center; color: #1d4d2b; font-family: sans-serif;'>Схема распространения штормового предупреждения</h2>", unsafe_allow_html=True)
    components.html(html_content, height=580)

    st.divider()

#ДОЛГОСРОЧНЫЕ ПРОГНОЗЫ
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    def show_forecast_process():
        st.markdown("""
                <style>
                .big-climate-card {
                    background: #ffffff;
                    border-radius: 12px;
                    padding: 15px;
                    margin-bottom: 15px;
                    border: 1px solid #eef0f2;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    height: 100%; /* Чтобы карточки были одной высоты */
                }
                .section-title {
                    color: #1d4d2b;
                    font-weight: 800;
                    font-size: 1.2rem;
                    margin-bottom: 10px;
                    border-bottom: 3px solid #f1f3f5;
                    padding-bottom: 5px;
                }
                .info-list { list-style-type: none; padding: 0; margin: 0; }
                .info-item {
                    font-size: 0.95rem;
                    margin-bottom: 6px;
                    line-height: 1.3;
                    display: flex;
                    align-items: flex-start;
                    gap: 8px;
                }
                .highlight-val { font-weight: 700; color: #2c3e50; }
                .forecast-status-high { color: #d9534f; font-weight: 800; }
                .forecast-status-ok { color: #2ecc71; font-weight: 800; }
                </style>
            """, unsafe_allow_html=True)

            # --- ВЕРХНИЙ БЛОК (ТЕХНОЛОГИИ И ГИФКА) ---
        col_tech, col_viz = st.columns([1.5, 1], gap="large")
            
        with col_tech:
            st.title("Долгосрочный прогноз погоды")
            tab1, tab2, tab3, tab4 = st.tabs(["⏳ Декада", "📅 Месяц", "🍂 Сезон", "💡 Шторма"])
            
            with tab1:
                st.subheader("🗓️ Прогноз на 10 дней")
                st.info("**Периодичность:** 30-31, 10 и 20 числа каждого месяца.")
                st.markdown("""
                * **Детализация:** прогноз с указанием конкретных атмосферных явлений.
                * **Параметры:** температура (мин/макс), осадки, ветер, туман, гололед, метель, пыльная буря.
                * **Передача:** оперативно передается в государственные и местные исполнительные органы.
                """)

            with tab2:
                st.subheader("📋 Прогноз на месяц")
                st.success("**Тип:** Консультативный бюллетень.")
                st.markdown("""
                * **Методика:** использование метода **года-аналога** посредством АРМ-Долгосрочник (поиск схожих процессов в архивах за 30 лет).
                * **Технологии:** обработка данных 200+ станций.
                * **Выпуск:** ежемесячно к 15 числу.
                * **Регионы:** формируется по всем 17 областям РК.                
                """)

            with tab3:
                st.subheader("🍂 Прогноз на сезон")
                st.warning("**Охват:** 6 выпусков в год (на сезон и субсезон).")
                st.markdown("""
                * **Анализ:** использование метода **года-аналога** посредством АРМ-Долгосрочник (поиск схожих процессов в архивах за 30 лет).
                * **Заблаговременность:** прогноз до **3-7 месяцев**.
                * **Регионы:** формируется по территории Казахстана.
                """)

            with tab4:
                st.subheader("💡 Штормовые предупреждения")
                st.error("Штормовые предупреждения о волнах холода и тепла, обильных осадках и о засушливых условиях.")
                st.markdown("""
                * **Критерии:** отклонение t° от нормы на **7°C и более**, осадки больше/меньше нормы.
                * **Заблаговременность:** заблаговременность выпуска от **24 до 240 часов**.
                """)

               
        with col_viz:
            st.subheader("🗺️ Визуализация")
            st.image(os.path.join(BASE_DIR, "udpp.gif"), use_container_width=True)
        st.divider()
        
        

            # --- ВАШ ЗАПРОС: КЛИМАТ И ПРОГНОЗ В ОДНУ СТРОКУ ---
        col_climat_data, col_viz1 = st.columns([1, 1], gap="medium")

        with col_climat_data:
            st.markdown("#### 📜 Климатическая характеристика: Апрель")
                
                # ВАЖНО: Обновляем стили для увеличения шрифта
            st.markdown("""
                    <style>
                    .big-climate-card {
                        background: #ffffff;
                        border-radius: 12px;
                        padding: 20px;
                        margin-bottom: 10px;
                        border: 1px solid #eef0f2;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    }
                    .section-title {
                        color: #1d4d2b;
                        font-weight: 800;
                        font-size: 1.4rem !important; /* УВЕЛИЧЕНО с 1.1 до 1.4 */
                        margin-bottom: 12px;
                        border-bottom: 2px solid #f1f3f5;
                    }
                    .info-item { 
                        font-size: 1.2rem !important; /* УВЕЛИЧЕНО с 0.95 до 1.2 */
                        margin-bottom: 8px; 
                        line-height: 1.5; 
                    }
                    .val-bold {
                        font-weight: 700;
                        color: #2c3e50;
                    }
                    </style>
                """, unsafe_allow_html=True)

                # Ряд из карточек
            st.markdown("""
                <div style="display: flex; gap: 10px;">
                    <div class="big-climate-card" style="flex: 1;">
                        <div class="section-title">🌡️ Температура</div>
                        <div class="info-item">🔹 Север: <span class="val-bold">-1...+5°С</span></div>
                        <div class="info-item">🔹 Юг: <span class="val-bold">+9...+16°С</span></div>
                    </div>
                    <div class="big-climate-card" style="flex: 1;">
                        <div class="section-title">❄️ Экстремумы</div>
                        <div class="info-item">🔴 Тепло: <span class="val-bold">до +39°С</span></div>
                        <div class="info-item">🔵 Холод: <span class="val-bold">до -20°С</span></div>
                    </div>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 10px;">
                    <div class="big-climate-card" style="flex: 1;">
                        <div class="section-title">💧 Осадки</div>
                        <div class="info-item">📅 В среднем: <span class="val-bold">15-35 мм</span></div>
                        <div class="info-item">📅 Вид: <span class="val-bold">смешанные</span></div>
                    </div>
                    <div class="big-climate-card" style="flex: 1; border-left: 5px solid #f39c12;">
                        <div class="section-title">🌬️ Явления</div>
                        <div class="info-item">🚩 Туман: <span class="val-bold">2-5 суток</span></div>
                        <div class="info-item">⚡ Метель: <span class="val-bold">5-7 суток</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        with col_viz1:
            st.subheader("🗺️ Визуализация")
            
            # 1. Формируем полный путь к GIF-файлу
            gif_path = os.path.join(BASE_DIR, "udpp1.gif")
            
            # 2. Проверяем наличие файла и применяем CSS-хак
            if os.path.exists(gif_path):
                # Кодируем GIF в Base64 для вставки в HTML
                import base64 # Можно вынести в начало файла
                with open(gif_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")
                
                # Отображаем GIF через HTML/CSS, делая его шире колонки
                st.markdown(
                    f"""
                    <div style="width: 100%; display: flex; justify-content: center;">
                        <img src="data:image/gif;base64,{data}" style="width: 70%; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # На случай, если файл не найден
                st.error(f"⚠️ Файл 'udpp1.gif' не найден по пути: {gif_path}")
            
            st.divider()
            
        
               
    if __name__ == "__main__":
        show_forecast_process()
    

 
   
    with st.container():
        st.markdown("<h3 style='color: #1d4d2b; text-align: center; margin-bottom: 20px;'>💼 Отраслевое применение прогнозов</h3>", unsafe_allow_html=True)
        
        # Стили для КАРТОЧЕК БЕЗ ФОТО
        st.markdown("""
            <style>
            .sector-no-img-card {
                background: #ffffff;
                border-radius: 12px;
                padding: 15px;
                border: 1px solid #eef0f2;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                height: 250px; /* Уменьшили высоту, т.к. нет фото */
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                align-items: center;
                transition: transform 0.2s;
            }
            .sector-no-img-card:hover { transform: translateY(-5px); }
            .no-img-icon {
                font-size: 2.5rem; /* Большая иконка */
                color: #1d4d2b;
                margin-bottom: 10px;
            }
            .no-img-header {
                color: #1d4d2b;
                font-weight: 800;
                font-size: 0.9rem; /* Чуть крупнее заголовок */
                margin-bottom: 8px;
                text-transform: uppercase;
                line-height: 1.2;
                min-height: 40px; /* Фиксированная высота для заголовка */
            }
            .no-img-body { 
                font-size: 1.0rem; 
                color: #444; 
                line-height: 1.2;
                font-weight: 500;
            }
            </style>
        """, unsafe_allow_html=True)

        # Данные (сокращенные для компактности)
        sectors = [
            {"title": "Строительство", "desc": "информация о продолжительности строительного сезона", "emoji": "🏗️"},
            {"title": "Лесная отрасль", "desc": "информация об осадках и температуре в летний сезон для планирования мероприятий по охране лесов от пожаров.", "emoji": "🌲"},
            {"title": "Туризм", "desc": "информация о режиме температуры и осадков на предстоящую неделю, месяц, сезон для планирования отдыха .", "emoji": "🗺️"},
            {"title": "Сельское хозяйство", "desc": "для определения площади посевов, оптимальных сроков сева, сроков внесения удобрений и уборки урожая.", "emoji": "🌾"},
            {"title": "Управление водными ресурсами ", "desc": "для предотвращения возможных наводнений, правильного ведения работ по ирригации и др.", "emoji": "💧"},
            {"title": "Энергетика", "desc": "информация о потребностях населения и промышленности в потреблении электроэнергии в зависимости от погодных условий", "emoji": "⚡"}
        ]

        cols = st.columns(6)

        for i, sector in enumerate(sectors):
            with cols[i]:
                st.markdown(f"""
                    <div class="sector-no-img-card">
                        <div class="no-img-icon">{sector['emoji']}</div>
                        <div class="no-img-header">{sector['title']}</div>
                        <div class="no-img-body">{sector['desc']}</div>
                    </div>
                """, unsafe_allow_html=True)             
                

with tabs[3]:
    st.set_page_config(layout="wide", page_title="Агрометеорологические прогнозы 2026")


    # Добавляем стили для меток дат
    st.markdown("""
    <style>
        .forecast-item {
            margin-bottom: 10px;
            padding: 6px;
            border-radius: 3px;
            transition: 0.3s;
        }
        .forecast-item:hover {
            background-color: #f0f2f6;
        }
        .date-tag {
            display: inline-block;
            background-color: #e1f5fe;
            color: #01579b;
            font-size: 0.8rem;
            padding: 2px 8px;
            border-radius: 12px;
            margin-left: 10px;
            font-weight: 600;
        }
        .agro-card {
            background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
            color: white;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .big-number {
            font-size: 56px;
            font-weight: 600;
            line-height: 1;
        }
    </style>
    """, unsafe_allow_html=True)

    # Основной блок
    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.markdown("""
        <div class="agro-card">
            <div class="big-number">10</div>
            <div style="font-size: 1.1rem; margin-top: 10px;">Наименований<br>прогнозов</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("Прогнозы охватывают все ключевые зерносеющие регионы Казахстана.")
            
        st.markdown("""
                    <div style="background: #f1f8e9; padding: 20px; border-radius: 15px; border: 1px dashed #2e7d32; text-align: center;">
                        <h5 style="color: #1b5e20; margin-bottom: 15px;">📲 Приложение AgroData</h5>
                        <img src="https://img.icons8.com/ios/100/2e7d32/qr-code--v1.png" width="50">
                        <p style="font-size: 0.5em; margin-top: 10px; color: #455a64;">Доступ к фактическим данным для фермеров в режиме реального времени</p>
                        <a href="https://agrodata.kazhydromet.kz" target="_blank" style="text-decoration: none;">
                            <button style="background: #2e7d32; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Открыть портал</button>
                        </a>
                    </div>
        """, unsafe_allow_html=True)
                

    with col2:
        st.subheader("📅 График выпуска агрометеорологических прогнозов")
        
        # Структурируем данные
        forecast_data = [
            ("💧 Прогноз запасов продуктивной влаги (ЗПВ)", "25 марта, 25 апреля"),
            ("🌱 Оптимальные сроки сева яровых", "25 марта, 25 апреля"),
            ("☀️ Прогноз засухи (на основе SPI)", "Май, Июнь, Июль, Август"),
            ("🌾 Сроки созревания яровых зерновых", "15 июня, 15 июля"),
            ("📈 Урожайность яровых зерновых", "15 июля, 15 августа"),
            ("🏔️ Урожайность озимых (Алм. и Жамб. обл.)", "15 мая, 15 июня"),
            ("🌽 Урожайность подсолнечника, свеклы и кукурузы", "15 июля, 15 августа"),
            ("🚜 Условия уборки зерновых культур", "июль-август")
        ]
        
        # Вывод в две колонки внутри основной колонки
        sub_col1, sub_col2 = st.columns(2)
        
        for i, (name, date) in enumerate(forecast_data):
            target_col = sub_col1 if i % 2 == 0 else sub_col2
            target_col.markdown(f"""
            <div class="forecast-item">
                <strong>{name}</strong><br>
                <span class="date-tag">📅 {date}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()


    def show_enhanced_farmer_calendar():
        st.markdown("### 📅 Календарь фермера")
        
        # 1. Подготовка данных (теперь "культура" — это обычный столбец)
        months = [
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", 
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ]
        
        calendar_data = {
            "культура": ["озимая.пшеница", "яровая.пшеница", "кукуруза", "рис", "подсолнечник", "сахарная свекла"],
            "Январь": ["В", "", "", "", "", ""],
            "Февраль": ["В", "", "", "", "", ""],
            "Март": ["В", "", "", "", "", ""],
            "Апрель": ["В", "", "", "", "", "П"],
            "Май": ["В", "П", "П", "П", "П", "В"],
            "Июнь": ["У", "В", "В", "В", "В", "В"],
            "Июль": ["У", "В", "В", "В", "В", "В"],
            "Август": ["", "В", "В", "В", "В", "В"],
            "Сентябрь": ["", "У", "У", "У", "В", "У"],
            "Октябрь": ["П", "", "", "", "У", ""],
            "Ноябрь": ["В", "", "", "", "", ""],
            "Декабрь": ["В", "", "", "", "", ""]
        }
        
        df = pd.DataFrame(calendar_data)

        # 2. Функция для стилизации
        def style_cells(val):
            # Базовый стиль для всех заполненных ячеек: крупный черный шрифт
            base_style = "color: black; font-weight: 900; font-size: 16px; text-align: center;"
            
            if val == "П": # Посев
                return f"{base_style} background-color: #5d8a33;"
            elif val == "В": # Вегетация
                return f"{base_style} background-color: #bcd9ea;"
            elif val == "У": # Уборка
                return f"{base_style} background-color: #ffda66;"
            return ""

        # Применяем стили ко всем столбцам, кроме первого ("культура")
        styled_df = df.style.map(style_cells, subset=months)

        # 3. Отображение
        # Используем статичную таблицу или dataframe. 
        # Для максимального контроля над шрифтом в заголовках лучше всего подходит st.table
        st.table(styled_df)

        # 4. Легенда
        st.markdown("""
        <div style="display: flex; gap: 20px; justify-content: center; margin-top: 10px;">
            <div style="display: flex; align-items: center; gap: 5px;"><div style="width: 20px; height: 20px; background: #5d8a33; border-radius: 4px;"></div><b>П</b> — Посев</div>
            <div style="display: flex; align-items: center; gap: 5px;"><div style="width: 20px; height: 20px; background: #bcd9ea; border-radius: 4px;"></div><b>В</b> — Вегетация</div>
            <div style="display: flex; align-items: center; gap: 5px;"><div style="width: 20px; height: 20px; background: #ffda66; border-radius: 4px;"></div><b>У</b> — Уборка</div>
        </div>
        """, unsafe_allow_html=True)

    show_enhanced_farmer_calendar()


    # --- КОНФИГУРАЦИЯ СТРАНИЦЫ ---
    st.set_page_config(layout="wide", page_title="Агрометеорологические прогнозы 2026")

    # --- КАСТОМНЫЙ CSS ---
    st.markdown("""
    <style>
        /* Уменьшенный главный заголовок без подчеркивания */
        .main-title {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            color: #1b5e20;
            margin-bottom: 25px;
        }
        /* Заголовки разделов: меньше размер, без фона, просто жирный текст с линией */
        .section-header-new {
            font-size: 20px;
            font-weight: bold;
            color: #2e7d32;
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }
        .description-card {
            background-color: #f8f9fa;
            padding: 15px;
            border-left: 5px solid #2e7d32;
            border-radius: 5px;
            height: 100%;
        }
        .desc-title {
            font-weight: bold;
            color: #1b5e20;
            margin-bottom: 8px;
            display: block;
        }
        .desc-text {
            font-size: 14px;
            color: #333;
            line-height: 1.4;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- 1. ЗАГОЛОВОК И КАРТЫ ---
    st.markdown('<div class="main-title">Агрометеорологические прогнозы перед началом весенне-полевых работ 2026 года</div>', unsafe_allow_html=True)

    import base64
    import os

    col_map1, col_map2 = st.columns(2)

    # Функция для отрисовки "большого" изображения через HTML
    def get_base64_img(img_name):
        img_path = os.path.join(BASE_DIR, img_name)
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        return None

    with col_map1:
        data1 = get_base64_img("Рисунок1.jpg")
        if data1:
            st.markdown(
                f"""
                <div style="width: 100%; margin-bottom: 20px;">
                    <img src="data:image/jpeg;base64,{data1}" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <p style="text-align: center; color: gray; font-size: 0.8rem; margin-top: 5px;">Оптимальные сроки сева зерновых культур</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("Рисунок1.jpg не найден")

    with col_map2:
        data2 = get_base64_img("Рисунок2.jpg")
        if data2:
            st.markdown(
                f"""
                <div style="width: 100%; margin-bottom: 20px;">
                    <img src="data:image/jpeg;base64,{data2}" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <p style="text-align: center; color: gray; font-size: 0.8rem; margin-top: 5px;">Прогноз запасов продуктивной влаги</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("Рисунок2.jpg не найден")
            

    # --- 2. МЕТОДОЛОГИЯ ---
    st.markdown('<div class="section-header-new">📑 Методология и содержание прогнозов</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""<div class="description-card">
            <span class="desc-title">Прогноз урожайности яровой и озимой пшеницы </span>
            <p class="desc-text">Рассчитывается с использованием комплексных динамико-статистических моделей А.Н. Полевой и CGMS. Расчёты выполняются на основе агрометеорологических, статистических и климатических данных. Прогноз содержит сведения об ожидаемой урожайности яровых зерновых культур в разрезе районов по пунктам наблюдения.</p>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown("""<div class="description-card">
            <span class="desc-title">Прогноз урожайности подсолнечника, кукурузы на зерно и сахарной свеклы</span>
            <p class="desc-text">Рассчитывается с использованием комплексных динамико-статистических моделей А.Н. Полевой. Расчёты выполняются на основе агрометеорологических, статистических и климатических данных. Прогноз содержит сведения об ожидаемой урожайности в разрезе районов по пунктам наблюдения.</p>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown("""<div class="description-card">
            <span class="desc-title">Прогноз сроков созревания</span>
            <p class="desc-text">Рассчитывается по методике А.А Шиголева. Прогноз содержит сведения о наступлении фаз «колошения» и «восковой спелости» яровых зерновых культур в разрезе районов по пунктам наблюдения.
    </p>
            </div>""", unsafe_allow_html=True)
        with m4:
            st.markdown("""<div class="description-card">
                <span class="desc-title">Прогноз запасов влаги в почве </span>
                <p class="desc-text">Рассчитывается  по методике Л.А.Разумовой. Прогноз содержит сведения об ожидаемых запасах влаги в почве к началу весны по территории Казахстана (влажность почвы оценивается по категории: недостаточное, удовлетворительное и оптимальное) в разрезе районов по пунктам наблюдения.
    </p>
            </div>""", unsafe_allow_html=True)



    # --- 4. ОПРАВДЫВАЕМОСТЬ ПРОГНОЗОВ (КАК РИСУНКИ В 2 РЯДА) ---
    st.markdown('<div class="section-header-new">📊 Оправдываемость прогнозов по регионам</div>', unsafe_allow_html=True)

    # 1. Получаем путь к папке скрипта
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Формируем список путей и заголовков
    images_data = [
        {"path": os.path.join(current_dir, "image_1.png"), "caption": "Зерновые культуры"},
        {"path": os.path.join(current_dir, "image_2.png"), "caption": "Запасы влаги в почве"},
        {"path": os.path.join(current_dir, "image_3.png"), "caption": "с/х культуры"},
        {"path": os.path.join(current_dir, "image_4.png"), "caption": "Сроки созревания"}
    ]

    # 3. Вывод в два ряда по две колонки
    # Первый ряд
    row1_col1, row1_col2, row1_col3, row1_col4  = st.columns(4)

    # Собираем колонки в список для удобного обхода в цикле
    cols = [row1_col1, row1_col2, row1_col3, row1_col4]

    for i, item in enumerate(images_data):
        with cols[i]:
            if os.path.exists(item["path"]):
                st.image(item["path"], caption=item["caption"], use_container_width=True)
            else:
                st.warning(f"Файл {os.path.basename(item['path'])} не найден")
                
with tabs[4]:
    st.title("Гидрологические прогнозы")
    

    import streamlit as st
    import plotly.graph_objects as go

    # --- СТИЛИЗАЦИЯ ---
    st.markdown("""
    <style>
        .section-header-hydro {
            font-size: 22px;
            font-weight: bold;
            color: #01579b;
            margin-top: 30px;
            margin-bottom: 10px;
            border-bottom: 2px solid #01579b;
            padding-bottom: 5px;
        }
        .methodology-box {
            background-color: #f0f7f9;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #b3e5fc;
            line-height: 1.6;
            color: #333;
            margin-bottom: 25px;
        }
        .methodology-box ul {
            margin-bottom: 10px;
        }
        .calendar-box {
            background-color: #e1f5fe;
            padding: 15px;
            border-left: 5px solid #0288d1;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="methodology-box">
        Гидрологические прогнозы составляются на основании различных факторов, таких как <b>осеннее увлажнение почвы, запаса воды в снеге, сумма осадков за зиму и глубина промерзания почвы</b>. 
        Гидропрогнозисты также используют сезонные и месячные синоптические прогнозы, основанные на методе подбора года-аналога, включая прогноз суммы осадков и средней температуры воздуха. 
        <br><br>
        <b>При составлении гидрологических прогнозов применяются следующие методики:</b>
        <ul>
            <li>Множественная регрессия;</li>
            <li>Численные модели HBV и SWIM.</li>
        </ul>
        <div class="calendar-box">
            <b>📅 График выпуска прогнозов:</b><br>
            • <b>Предварительный прогноз:</b> выпускается к 5 февраля (по состоянию на 1 февраля).<br>
            • <b>Основной прогноз:</b> выпускается к 5 марта (по состоянию на 1 марта).<br>
            <i>В дальнейшем прогнозы по равнинной территории обновляются еженедельно.</i>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- ГИДРОЛОГИЧЕСКИЙ РЕЖИМ (ГОРНЫЕ И РАВНИННЫЕ РЯДОМ) ---
    st.markdown('<div class="predictor-header">📊 Особенности гидрологического режима рек Казахстана</div>', unsafe_allow_html=True)

    # Создаем две колонки для отображения блоков рядом
    col_plain, col_mountain = st.columns(2)

    with col_plain:
        st.markdown("### 🌾 Равнинные реки")
        st.markdown("""
        <div class="report-text" style="height: 100%; border-top: 5px solid #fbc02d;">
            Поверхностный сток формируется <b>исключительно за счет талых снеговых вод</b>. 
            Основной фактор — накопленные осадки за холодный период.
            <br><br>
            📅 <b>Сроки половодья:</b><br>
            <b>3-я декада марта — 3-я декада апреля.</b>
            <br><i>Дружного таяния снега в феврале исторически не наблюдалось.</i>
        </div>
        """, unsafe_allow_html=True)

    with col_mountain:
        st.markdown("### 🏔️ Горные реки")
        st.markdown("""
        <div style="background-color: #f9f9f9; padding: 10px; border-radius: 8px; border: 1px solid #e0e0e0; border-top: 5px solid #0d47a1;">
            <div class="stage-card" style="margin-bottom: 8px; padding: 8px;">
                <b>I этап: Низкогорье (Н ≤ 1000 м)</b><br>
                ⏱ <i>Конец марта — конец апреля.</i><br>
                ⚠️ <span style="color: #d32f2f; font-weight: bold;">Высокий риск затопления.</span>
            </div>
            <div class="stage-card" style="margin-bottom: 8px; padding: 8px;">
                <b>II этап: Среднегорье (Н 1000-2000 м)</b><br>
                ⏱ <i>Начало мая — начало июля.</i>
            </div>
            <div class="stage-card" style="margin-bottom: 0px; padding: 8px;">
                <b>III этап: Высокогорье (Н ≥ 2000 м)</b><br>
                ⏱ <i>Середина июля — начало сентября.</i>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
        
    # --- ГИДРОЛОГИЧЕСКИЙ РЕЖИМ (ГОРНЫЕ И РАВНИННЫЕ РЯДОМ) ---
    st.markdown('<div class="predictor-header">📊 Гидрологические прогнозы на 2026 г.</div>', unsafe_allow_html=True)

    def render_taskyn_info():
        st.markdown("""
        <style>
        .report-card {
            background-color: #f0f7ff;
            border-radius: 15px;
            padding: 25px;
            border-left: 8px solid #2e86c1;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin: 20px 0;
        }
        .card-title {
            color: #1a5276;
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .stat-row {
            display: flex;
            gap: 20px;
            margin-top: 15px;
        }
        .stat-item {
            background: white;
            padding: 10px 20px;
            border-radius: 10px;
            flex: 1;
            text-align: center;
            border: 1px solid #d4e6f1;
        }
        .stat-number {
            display: block;
            font-size: 1.8rem;
            font-weight: 800;
            color: #2e86c1;
        }
        .stat-label {
            font-size: 0.85rem;
            color: #566e7a;
        }
        .highlight-blue {
            color: #2e86c1;
            font-weight: bold;
        }
        </style>
        
        <div class="report-card">
            <div class="card-title">
                🌊 Интеграция с системой «Таскын»
            </div>
            <div class="report-text" style="font-size: 1.1rem; line-height: 1.6;">
                В <b>2025 году</b> усовершенствован долгосрочный прогноз с указанием 
                <span class="highlight-blue">максимальных уровней и расходов воды</span>. 
                Это обеспечило работу системы <b>«Таскын»</b> по моделированию возможных зон затопления.
            </div>
            <div class="stat-row">
                <div class="stat-item">
                    <span class="stat-number">2025</span>
                    <span class="stat-label">Год старта</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">251</span>
                    <span class="stat-label">Гидрологический пост</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Вызов функции
    render_taskyn_info()


    # --- СТИЛИЗАЦИЯ ЗАГОЛОВКОВ ---
    st.markdown("""
    <style>
        .predictor-header {
            font-size: 20px;
            font-weight: bold;
            color: #0d47a1;
            margin-top: 25px;
            padding-bottom: 5px;
            border-bottom: 1px solid #bbdefb;
        }
        .map-caption {
            text-align: center;
            font-size: 14px;
            color: #555;
            margin-top: -10px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            .report-text {
                font-size: 16px;
                line-height: 1.6;
                color: #333;
                text-align: justify;
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                margin-top: 10px;
            }
            .hydro-group-header {
                font-size: 18px;
                font-weight: bold;
                color: #0d47a1;
                margin-top: 20px;
            }
            .highlight-blue {
                color: #1565c0;
                font-weight: bold;
            }
            .stage-card {
                background-color: #ffffff;
                border-left: 5px solid #0d47a1;
                padding: 10px 15px;
                margin-bottom: 10px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
            }
        </style>
    """, unsafe_allow_html=True)


    # --- РАЗДЕЛ: ОСЕННЕЕ УВЛАЖНЕНИЕ ---
    st.markdown('<div class="predictor-header">🍂 Осеннее увлажнение (сентябрь–октябрь)</div>', unsafe_allow_html=True)

    import base64
    import os

    # Вспомогательная функция для обработки изображений
    def get_img_as_base64(file_name):
        # Используем BASE_DIR, который у вас определен глобально
        path = os.path.join(BASE_DIR, file_name)
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        return None

    col1, col2 = st.columns(2)

    with col1:
            data1 = get_img_as_base64("Без названия (1).jpeg")
            if data1:
                st.markdown(
                    f"""
                    <div style="width: 100%; margin-bottom: 10px;">
                        <img src="data:image/jpeg;base64,{data1}" style="width: 115%; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            st.markdown('<div class="map-caption">1) Суммы осадков за осенний период, мм</div>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="report-text">
                В ряде западных и восточных областей (преимущественно в <b>Западно-Казахстанской, Мангыстауской, Павлодарской, 
                Восточно-Казахстанской областях, области Абай, на востоке Карагандинской и севере области Жетісу</b>) наблюдаются 
                показатели осеннего увлажнения выше нормы. В отдельных точках (особенно в высокогорных зонах) зафиксированы 
                значения <span class="highlight-blue">более 150 мм</span>, указывающие на существенное переувлажнение.
            </div>
            """, unsafe_allow_html=True)

    with col2:
            data2 = get_img_as_base64("Без названия (2).jpeg")
            if data2:
                st.markdown(
                    f"""
                    <div style="width: 100%; margin-bottom: 10px;">
                        <img src="data:image/jpeg;base64,{data2}" style="width: 115%; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

            st.markdown('<div class="map-caption">2) Отклонение от нормы, %</div>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="report-text">
                В то же время на севере, центре, юге (<b>Актюбинская, Улытауская, Жамбылская, Туркестанская, Кызылординская 
                области</b>, а также большая часть <b>Атырауской, Костанайской, Акмолинской, Северо-Казахстанской, Алматинской</b> и 
                восточной части Карагандинской областей) преобладают ниже норм или умеренные уровни влаги – с минимальными 
                значениям <span class="highlight-blue"><25 мм</span>.
            </div>
            """, unsafe_allow_html=True)
        

    st.markdown("---") # Разделитель

    import base64
    import os

    # Вспомогательная функция для обработки изображений (если еще не добавлена выше)
    def get_img_as_base64(file_name):
        path = os.path.join(BASE_DIR, file_name)
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        return None

    # --- РАЗДЕЛ: ОСАДКИ ЗА ХОЛОДНЫЙ ПЕРИОД ---
    st.markdown('<div class="predictor-header">❄️ Количество осадков за холодный период</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        data3 = get_img_as_base64("Без названия (3).jpeg")
        if data3:
            st.markdown(
                f"""
                <div style="width: 100%; margin-bottom: 10px;">
                    <img src="data:image/jpeg;base64,{data3}" style="width: 115%; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.error("Файл 'Без названия (3).jpeg' не найден")

        st.markdown('<div class="map-caption">1) Суммы осадков за холодный период, мм</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="report-text">
            Превышение нормы наблюдается преимущественно на востоке (горные и предгорные части ВКО и области Абай),
            и севере (в Павлодарской области, большей части Акмолинской и Северо-Кахастанской областей, на севере
            Костанайской и Карагандинской областей). В горно-предгорных районах Туркестанкой области и восточной части
            Мангистауской области также наблюдаются осадки больше нормы.
        </div>
        """, unsafe_allow_html=True)

    with col4:
        data4 = get_img_as_base64("Без названия (4).jpeg")
        if data4:
            st.markdown(
                f"""
                <div style="width: 100%; margin-bottom: 10px;">
                    <img src="data:image/jpeg;base64,{data4}" style="width: 115%; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.error("Файл 'Без названия (4).jpeg' не найден")

        st.markdown('<div class="map-caption">2) Отклонение от нормы за холодный период, %</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="report-text">
            Накопленные осадки ниже нормы в западных (ЗКО, Актюбинская, Атырауская), южных (Туркестанская, Жамбылская), 
            юго-восточных (Алматинская, Жетісу) и центральных (Ұлытау, юг Костанайской) областях. 
            Местами (равнинные части области Абай и значительная часть Кызылординской области) накопление наблюдается около нормы.
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    
    import streamlit as st
    from PIL import Image
    import os

    # Настройка страницы (широкий формат)
    st.set_page_config(layout="wide")

    def main():
        # Создаем две колонки: левая для карты (относительная ширина 2), правая для текста (ширина 1)
        col1, col2 = st.columns([2, 1])

        import base64
        import os

        with col1:
            # Путь к изображению
            image_path = "risk.jpeg"
            
            if os.path.exists(image_path):
                # Кодируем изображение в Base64
                with open(image_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")
                
                # Выводим увеличенное изображение (120% ширины)
                st.markdown(
                    f"""
                    <div style="width: 80%; margin-bottom: 5px;">
                        <img src="data:image/jpeg;base64,{data}" style="width: 80%; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                # Подпись под увеличенным рисунком
                st.markdown('<div style="color: gray; font-size: 0.9rem; text-align: center; margin-bottom: 20px;">Карта рисков</div>', unsafe_allow_html=True)
            else:
                st.error(f"Файл {image_path} не найден в основной папке.")
                

        with col2:
            # Текстовый блок справа
            st.subheader("📋 Оценка паводко-опасных регионов")
            
            st.markdown("""
            **С повышенными рисками:** Акмолинская, СКО, Карагандинская, ВКО и область Абай.
            
            **Со средними рисками:** Костанайская, ЗКО, Актюбинская, Улытауская, Павлодарская, Туркестанская, Алматинская и область Жетісу.
            
            **С низкими рисками:** Атырауская, Мангыстауская, Кызылординская и Жамбылская области.
            """)
            
    if __name__ == "__main__":
        main()
        
    import streamlit as st
    import os
    import base64

    def render_hydrology_models_section():
        st.markdown('<div class="predictor-header">🌊 Гидрологическое моделирование: HBV и SWIM</div>', unsafe_allow_html=True)
        
        # Вспомогательная функция для отображения увеличенных картинок (115%)
        def display_big_image(img_name, caption_text):
            img_path = os.path.join(BASE_DIR, img_name)
            if os.path.exists(img_path):
                with open(img_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")
                st.markdown(
                    f"""
                    <div style="width: 100%; margin-top: 10px;">
                        <img src="data:image/jpeg;base64,{data}" style="width: 80%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <p style="color: gray; font-size: 0.85rem; text-align: center; margin-top: 5px;">{caption_text}</p>
                    </div>
                    """, unsafe_allow_html=True
                )
            else:
                st.warning(f"Изображение {img_name} не найдено. Добавьте его в папку проекта.")

        # Создаем вкладки для двух моделей
        tab_hbv, tab_swim = st.tabs(["📊 Модель HBV-light", "🌍 Модель SWIM"])

        with tab_hbv:
            col_hbv_text, col_hbv_img = st.columns([1, 1])
            
            with col_hbv_text:
                st.markdown("""
                ### Концепция HBV
                Шведская концептуальная модель для составления оперативных прогнозов стока, которая используется для не зарегулированных рек и моделирует суточный речной сток.
                
                **Этапы работы:**
                1. **Калибровка:** подбор параметров на основе архива данных.
                2. **Метеоданные:** получение суточных прогнозов.
                3. **Моделирование:** запуск процесса и визуализация.
                
                Модель адаптирована для 70 рек Казахстана и успешно применяются в оперативном прогнозирований стока рек

                """)
            
            with col_hbv_img:
                # Здесь укажите имя файла со схемой из презентации
                display_big_image("hbv_scheme.png", "Схема оперативного прогноза стока по модели HBV-light")

        with tab_swim:
            st.markdown("### SWIM (Soil and water integrated model)")
            
            col_swim_img, col_swim_text = st.columns([2, 1])
            
            with col_swim_img:
                # Путь к файлу с входными данными ГИС
                img_swim = "swim_inputs.png"
                img_path_swim = os.path.join(BASE_DIR, img_swim)
                
                if os.path.exists(img_path_swim):
                    with open(img_path_swim, "rb") as f:
                        data = base64.b64encode(f.read()).decode("utf-8")
                    
                    # Увеличиваем до 135% и сдвигаем влево на -17.5% для центровки
                    st.markdown(
                        f"""
                        <div style="width: 100%; display: flex; flex-direction: column; align-items: center;">
                            <img src="data:image/png;base64,{data}" 
                                 style="width: 100%; 
                                        max-width: none; 
                                        margin-left: 0%; 
                                        border-radius: 8px; 
                                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                            <p style="color: gray; font-size: 0.85rem; text-align: center; margin-top: 10px; width: 100%; margin-left: -17.5%;">
                                Входные ГИС-данные (почвы FAO, Land 30, гидротопы)
                            </p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                else:
                    st.error(f"Файл {img_swim} не найден. Проверьте путь в папке проекта.")
                

            with col_swim_text:
                st.info("""
                Эко-гидрологическая, полу-распределенная, непрерывная модель, впервые описана в 1989 г.
                
                **Особенности SWIM:**
                * Разработана для обеспечения комплексного моделирования, основанного на ГИС, для моделирования гидрологического и водного качества.
                * Основана на моделях SWAT и MATSALU.
                * Интегрирует гидрологическую, эрозионную и динамику питательных веществ в масштабе водосбора.
                
                Модель адаптирована для 14 рек Казахстана и применяются при оперативном прогнозирований стока рек
                """)
                
            st.divider()

    # Вызов раздела в основном приложении
    render_hydrology_models_section()


    import streamlit as st
    import pandas as pd
    import os
    import base64

    def render_selevidenie_section():
        st.markdown('<div class="predictor-header">🏔️ Мониторинг селевой опасности</div>', unsafe_allow_html=True)

        # 1. Аналитический блок (Краткая информация)
        st.markdown(f"""
        <div style="background-color: #fff4e6; border-left: 5px solid #e67e22; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <strong>География риска:</strong> Селеопасные районы занимают около <b>13%</b> территории Казахстана (горы и предгория). 
            Мониторинг дождевого генезиса ведется по <b>11 основным районам</b>.
        </div>
        """, unsafe_allow_html=True)

        # 2. Визуализация: Карта селевой опасности (Увеличенная)
        col_map_sele, col_info_sele = st.columns([2, 1])

        with col_map_sele:
            img_name = "sele_map.jpg" # Укажите ваше имя файла Рис. 1
            img_path = os.path.join(BASE_DIR, img_name)
            
            if os.path.exists(img_path):
                with open(img_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")
                st.markdown(
                    f"""
                    <div style="width: 80%;">
                        <img src="data:image/jpeg;base64,{data}" style="width: 80%; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                        <p style="color: gray; font-size: 0.85rem; text-align: center; margin-top: 10px;">Карта селевой опасности территории РК</p>
                    </div>
                    """, unsafe_allow_html=True
                )
            else:
                st.info("🖼️ [Место для карты селевой опасности]")

        with col_info_sele:
            st.markdown("### 📋 Выпускаемая продукция")
            st.markdown(f"""
            * 📅 **Ежегодный бюллетень** (дождевой генезис)
            * 🕒 **Ежедневный бюллетень**
            * ⚡ **Прогнозы:** краткосрочные и сверхкраткосрочные
            * ⚠️ **Штормовые предупреждения**
            """)
            
            # Новый блок: перечисление районов в два столбца
            st.markdown("---")
            st.markdown("#### 📍 Селеопасные районы:")
            st.markdown("""
            <div style="column-count: 2; column-gap: 20px; font-size: 0.9rem; color: #333;">
                • Иле Алатау<br>
                • Кунгей Алатау<br>
                • Терискей Алатау<br>
                • Жетысу Алатау<br>
                • Киргизский Алатау<br>
                • Таласский Алатау<br>
                • Угамский хребет<br>
                • горы Мангистау<br>
                • Тарбагатай<br>
                • Саур<br>
                • Каз. Алтай
            </div>
            """, unsafe_allow_html=True)
            
            st.success("**Потребители:** Госорганы управления и население РК.")
            

        st.divider()


       # 4. Факторы формирования и критерии
        col_fact1, col_fact2 = st.columns(2)
        
        with col_fact1:
            st.warning("⚠️ **Генезис селей в РК:**")
            st.markdown("""
            1. Интенсивные дожди 🌧️
            2. Прорыв моренных озер 🌊
            3. Землетрясения и оползни 🌋
            4. Антропогенный фактор 🚜
            """)
            
        with col_fact2:
            st.info("⚖️ **Критерии осадков:**")
            st.markdown("""
            * **Сильные:** 15−29 мм
            * **Очень сильные:** ≥30 мм
            *(согласно Наставлению 2005 г.)*
            """)

        # Итоговый вывод
        st.markdown("""
        <div style="text-align: center; color: #555; font-style: italic; margin-top: 20px;">
            Наибольшая активность в 2023 году зафиксирована в августе, преимущественно в Иле Алатау.
        </div>
        """, unsafe_allow_html=True)

    # Вызов функции
    render_selevidenie_section()
      

  # ВОДНЫЕ РЕСУРСЫ
with tabs[5]:
    import streamlit as st
    import geopandas as gpd
    import folium
    from streamlit_folium import st_folium
    import os
    import pandas as pd
    import plotly.graph_objects as go
     
    
    base_path = os.path.dirname(os.path.abspath(__file__))
        
        
    # --- НАСТРОЙКИ И ДАННЫЕ ---
    FOLDER_PATH = os.path.join(BASE_DIR, "shp")

    VXB_STATS = {
        "Арало-Сырдарьинский ВХБ": {"норма": 21.42, "местные": 3.22, "приток": 18.21, "отток": None},
        "Балкаш-Алакольский ВХБ": {"норма": 29.91, "местные": 17.20, "приток": 12.71, "отток": "В КНР: 0.67"},
        "Ертисский ВХБ": {"норма": 33.38, "местные": 26.36, "приток": 7.03, "отток": "В КНР: 2.20, В РФ: 26.2"},
        "Жайык-Каспийский ВХБ": {"норма": 12.00, "местные": 3.36, "приток": 8.63, "отток": "В РФ: 1.48"},
        "Есильский ВХБ": {"норма": 2.29, "местные": 2.29, "приток": 0, "отток": "В РФ: 1.86"},
        "Нура-Сарысуйский ВХБ": {"норма": 1.16, "местные": 1.16, "приток": 0, "отток": None},
        "Шу-Таласский ВХБ": {"норма": 4.12, "местные": 1.29, "приток": 2.84, "отток": None},
        "Тобыл-Торгайский ВХБ": {"норма": 1.67, "местные": 1.33, "приток": 0.34, "отток": "В РФ: 0.46"},
        "Республика Казахстан": {"норма": 106.0, "местные": 56.2, "приток": 49.8, "отток": None}
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
                    
                    # 1. Основные полигоны ВХБ
                    folium.GeoJson(
                        data_basins,
                        style_function=lambda x: {'fillColor': '#3186cc', 'color': '#1d3557', 'weight': 1, 'fillOpacity': 0.4},
                        highlight_function=lambda x: {'fillColor': '#00fbff', 'color': 'white', 'weight': 3, 'fillOpacity': 0.7},
                        tooltip=folium.GeoJsonTooltip(fields=[tooltip_col])
                    ).add_to(m)

                    # 2. ДОБАВЛЯЕМ НАЗВАНИЯ НА КАРТУ
                    for _, row in data_basins.iterrows():
                        # Вычисляем центр бассейна для размещения текста
                        centroid = row.geometry.centroid
                        name = row[tooltip_col]
                        
                        # Создаем текстовую метку
                        folium.Marker(
                            location=[centroid.y, centroid.x],
                            icon=folium.DivIcon(
                                html=f"""<div style="
                                    font-family: sans-serif; 
                                    color: #1d3557; 
                                    font-size: 9pt; 
                                    font-weight: bold; 
                                    text-shadow: 1px 1px 2px white;
                                    width: 150px;
                                    text-align: center;
                                    transform: translate(-50%, -50%);
                                    pointer-events: none;
                                ">{name}</div>"""
                            )
                        ).add_to(m)

                    # 3. Реки
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
                    # Используем символ '💧' (U+1F4A7) с модификатором текста для затемнения
                        st.metric("💧︎ Местный сток", f"{cur_stats['местные']} км³")
    
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
            xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=16, color='black'),tickfont=dict(size=14, color='black')),
            yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=16, color='black'),tickfont=dict(size=14, color='black'))
            )

        # Отображение в Streamlit
        st.plotly_chart(fig, use_container_width=True)

    def show_water_resources_analysis():
        st.subheader("📊 Анализ суммарных водных ресурсов РК (1940–2024 гг.)")
        
        # Создаем контейнер для визуального выделения блока
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("""
                Анализ графика суммарных водных ресурсов Республики Казахстан за **1940–2024 гг.** показывает постепенное 
                плавное снижение объемов речного стока. Такая динамика линии тренда отражает естественную реакцию 
                гидрологической системы на современные климатические изменения.
                """)
            
            with col2:
                # Маленький индикатор тренда для наглядности
                st.metric(label="Тренд стока", value="Снижение", delta="- плавный", delta_color="inverse")

            st.divider()

            st.write("""
            Согласно данным, наблюдаемое уменьшение водных ресурсов связано с тем, что рост испаряемости и изменения 
            в режиме осадков начинают преобладать над приточностью. Несмотря на то, что в отдельные годы мы видим 
            значительные пики водности, общая тенденция указывает на постепенное сокращение среднемноголетнего стока.
            """)

            # Используем блок внимания для ключевого вывода
            st.info("""
            **Ключевой фактор:** Перестройка структуры питания рек, где доля ледникового стока стабилизируется, 
            а трансграничный приток испытывает влияние хозяйственной деятельности в верховьях.
            """, icon="💧")

            st.warning("""
            **Вывод:** Нисходящая линия тренда — это важный индикатор, который призывает к более 
            рациональному и бережному использованию имеющихся запасов воды в долгосрочной перспективе.
            """, icon="⚠️")

    # Вызов функции в основном приложении
    if __name__ == "__main__":
        show_water_resources_analysis()
    
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
        BASE_IMAGE_PATH = os.path.join(BASE_DIR)
        

        vxb_list = [k for k in VXB_STATS.keys() if k != "Республика Казахстан"]

        # Создайте этот словарь ПЕРЕД циклом for name in vxb_list:
        # Создайте этот словарь ПЕРЕД циклом for name in vxb_list:
        VXB_FULL_DATA = {
            "Ертисский ВХБ": {
                "photo": "Ертисский.tiff",
                "площадь": "347 757 км²",
                "гп_кол": "58",
                "рек_всего": "13 201",
                "артерия": "Река Ертис - крупнейшая по водности река Казахстана и основная транзитная водная артерия страны. Формирует значительную часть поверхностного стока восточного и северо-восточного Казахстана, обладает развитым каскадом водохранилищ и ГЭС. Играет ключевую роль в межбассейновом перераспределении водных ресурсов (в том числе через канал Иртыш–Караганда).",
                "объекты": ">82 вдхр. и прудов",
                "рек_инфо": "6 / Малых: 1195",
                "местные_текст": "5 крупных рек (Калжыр, Куршим, Буктырма, Ульби, Оба) формируют ~70% стока.",
                "приток_текст": "Поступает из КНР по реке Кара Ертис, створ с. Боран.",
                "years": list(range(1940, 2024)),
                "local_flow": [25.49, 33.64, 28.02, 25.26, 24.65, 19.6, 41.14, 37.13, 26.61, 28.29, 26.56, 15.32, 29.44, 19.89, 31.42, 20.18, 25.12, 27.11, 37.99, 25.85, 32.94, 28.71, 21.32, 18.68, 22.39, 21.29, 35.9, 21.66, 21.05, 35.08, 28.72, 31.42, 26.58, 31.4, 16.7, 24.76, 24.51, 25.69, 21.33, 33.19, 21.11, 19.46, 18.22, 24.69, 25.4, 28.48, 23.26, 27.19, 29.77, 25.01, 30.83, 20.56, 29.86, 31.49, 28.56, 26.83, 23.46, 22.99, 22.93, 22.1, 21.44, 33.15, 30.37, 18.74, 24.62, 23.41, 24.99, 27.52, 19.34, 31.04, 31.4, 21.57, 19.08, 42.49, 30.77, 32.48, 35.51, 26.86, 26.39, 25.45, 24.9, 22.22, 22.3, 25.4, 30.65],
                "inflow": [8.17, 9.65, 10.75, 7.64, 6.46, 5.7, 10.59, 8.96, 5.83, 6.63, 7.22, 5.22, 9.88, 5.7, 7.85, 7.53, 8.88, 7.4, 10.75, 8.41, 8.86, 10.4, 6.9, 5.81, 6.97, 5.48, 11.31, 4.88, 7.67, 11.37, 9.57, 9.79, 7.34, 9.41, 3.17, 6.14, 5.17, 7.01, 4.33, 6.65, 5.68, 5.7, 3.29, 5.54, 9.44, 7.57, 5.21, 8.02, 9.72, 4.47, 6.41, 4.63, 6.64, 11.12, 9.29, 6.85, 5.51, 6.22, 6.55, 6.31, 5.89, 8.6, 7.5, 4.37, 5.67, 6.81, 5.83, 4.38, 3.63, 2.35, 7.23, 3.62, 2.85, 7.84, 5.64, 6.05, 8.5, 8.72, 7.2, 4.65, 5.31, 4.29, 3.28, 5.25, 6.98],
                "river_table_data": [
                    {"Река / Створ": "р. Калжыр – с. Калжыр", "Норма": 22.6, "Пик": "47.6 (2001)", "Мин": "7.8 (2012)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Куршим – с. Вознесенка", "Норма": 58.6, "Пик": "137.0 (2013)", "Мин": "26.4 (1951)", "Динамика": "↗ Рост"},
                    {"Река / Створ": "р. Буктырма – с. Л. Пристань", "Норма": 208.0, "Пик": "404.0 (2013)", "Мин": "117.0 (1974)", "Динамика": "↗ Рост"},
                    {"Река / Створ": "р. Ульби – с. Ульби Перевалочная", "Норма": 104.0, "Пик": "160.0 (1946)", "Мин": "49.3 (1951)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Оба – г. Шемонаиха", "Норма": 162.0, "Пик": "255.0 (1958)", "Мин": "85.8 (1951)", "Динамика": "↔ Стабильно"},
                    {"Река / Створ": "р. Кара Ертис – с. Боран", "Норма": 301.0, "Пик": "478.0 (1969)", "Мин": "134.0 (1982)", "Динамика": "↘ Снижение"}
            ]
        },
            "Арало-Сырдарьинский ВХБ": {
                "photo": "Арал-Сырдария.tiff",
                "площадь": "345 000 км²",
                "гп_кол": "41",
                "рек_всего": "1500-2000",
                "артерия": "Река Сырдарья - крупная трансграничная река аридной зоны Центральной Азии с ледниково-снеговым питанием в верховьях. В пределах Казахстана её сток существенно зарегулирован водохранилищами и используется преимущественно для ирригации. Является основным водотоком северной части Аральского бассейна.",
                "объекты": "Свыше 33 водохранилищ и прудов",
                "рек_инфо": "Общее количество рек: 1500 - 2000 / Большие и средние: 497",
                "местные_текст": "Сток формируется реками Арыс, Шаян, Бугунь.",
                "приток_текст": "Трансграничный приток из Узбекистана.",
                "years": list(range(1940, 2024)),
                "local_flow": [2.15, 3.24, 3.43, 2.70, 2.09, 2.33, 3.16, 2.35, 2.56, 4.93, 3.30, 2.40, 4.65, 3.73, 4.93, 3.39, 3.09, 3.00, 5.71, 5.36, 4.86, 2.19, 2.29, 2.91, 3.85, 2.36, 2.49, 2.79, 3.65, 8.33, 3.21, 2.57, 4.06, 3.41, 2.40, 2.97, 2.97, 2.61, 3.58, 5.29, 3.42, 3.50, 2.77, 2.27, 2.99, 3.51, 2.29, 4.35, 3.43, 2.71, 4.15, 2.52, 3.05, 3.93, 3.74, 2.40, 2.21, 2.31, 3.00, 2.66, 2.39, 2.40, 3.84, 3.16, 2.86, 4.36, 2.98, 3.31, 2.22, 2.72, 3.34, 2.06, 3.19, 3.15, 4.25, 2.96, 4.09, 4.96, 2.40, 2.86, 2.24, 2.92, 2.96, 2.69, 3.13], 
                "inflow": [15.40, 21.41, 25.80, 22.42, 17.04, 24.16, 22.83, 16.87, 21.50, 28.79, 17.72, 18.67, 33.20, 27.88, 33.11, 22.96, 22.74, 14.07, 28.35, 28.92, 31.27, 14.00, 12.20, 19.02, 22.61, 11.48, 25.13, 11.61, 14.45, 50.46, 19.68, 14.03, 14.04, 16.90, 4.57, 4.16, 6.23, 7.22, 10.09, 14.13, 11.45, 11.38, 11.70, 9.05, 9.80, 9.90, 8.77, 12.84, 19.95, 12.87, 14.35, 14.00, 16.22, 21.44, 25.76, 14.44, 15.81, 14.13, 23.87, 18.54, 14.10, 13.53, 21.26, 27.28, 23.56, 22.26, 16.49, 17.98, 12.43, 14.60, 24.94, 13.37, 17.93, 13.56, 17.60, 14.63, 12.24, 22.39, 15.20, 13.94, 12.33, 9.40, 12.71, 14.66, 16.89],
                "river_table_data": [
                    {"Река / Створ": "р. Сырдарья – н.б. Шардаринского вдхр", "Норма": 728.0, "Пик": "1066 (1952)", "Мин": "167 (1975)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Сырдарья – ж.-д.ст. Томенарык", "Норма": 682.0, "Пик": "1023.0 (1952)", "Мин": "122.0 (1975)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Сырдарья – г. Казалы", "Норма": 492.0, "Пик": "670.0 (1954)", "Мин": "15.2 (1977)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р.Келес – устье", "Норма": 13.0, "Пик": "30.9 (2024)", "Мин": "1.5 (1987)", "Динамика": "↗ Рост"},
                    {"Река / Створ": "р.Арысь – ж.-д.ст. Арысь", "Норма": 162.0, "Пик": "94.89 (1969)", "Мин": "5.79 (1986)", "Динамика": "↔ Стабильно"},
                    {"Река / Створ": "р. Аксу - с. Саркырама", "Норма": 47.5, "Пик": "19.2 (1969)", "Мин": "2.57 (1944)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Бадам - с. Караспан", "Норма": 5.39, "Пик": "26.7 (2010)", "Мин": "85.8 (1951)", "Динамика": "↔ Стабильно"},
                    {"Река / Створ": "р. Шаян - в 3,3 км ниже устья р. Акбет", "Норма": 2.27, "Пик": "4.98 (1969)", "Мин": "0.5 (1996)", "Динамика": "↔ Стабильно"},
                    {"Река / Створ": "р. Бугунь - с. Екпенды", "Норма": 4.28, "Пик": "13.3 (1969)", "Мин": "0.12 (1994)", "Динамика": "↔ Стабильно"}
            ]                
        },
            "Балкаш-Алакольский ВХБ": {
                "photo": "Балхаш-Алакольский ВХБ.tiff",
                "площадь": "406 000 км²",
                "гп_кол": "69",
                "рек_всего": "Более 52000",
                "артерия": "Река Иле - трансграничная река с истоками в горах Тянь-Шаня, характеризуется ледниково-снеговым типом питания. Обеспечивает основную часть притока в озеро Балхаш, определяя его гидрологический режим и минерализацию. Дельта реки представляет собой важный водно-болотный комплекс международного значения.",
                "объекты": "Свыше 24300 озер и водоемов",
                "рек_инфо": "более 52000 / Малых и средних: около 45000",
                "местные_текст": "Сток формируется реками Шарын, Шилик, Иле, Каратал, Лепси.",
                "приток_текст": "Трансграничный приток из КНР.",
                "years": list(range(1940, 2024)),
                "local_flow": [13.06, 19.48, 18.71, 9.84, 9.75, 10.15, 18.42, 14.89, 13.28, 15.49, 15.44, 12.78, 20.37, 16.57, 19.47, 17.71, 18.19, 11.28, 20.73, 21.07, 19.56, 14.70, 12.99, 14.66, 20.07, 11.19, 21.44, 15.07, 14.41, 23.97, 17.96, 19.55, 17.91, 18.93, 11.55, 12.15, 13.14, 13.76, 14.34, 16.57, 16.58, 18.02, 12.89, 13.18, 14.22, 16.41, 14.02, 22.39, 29.59, 16.62, 20.91, 15.58, 17.21, 24.02, 22.41, 13.48, 19.35, 16.35, 19.94, 17.23, 16.98, 22.50, 24.21, 23.55, 21.07, 20.65, 18.00, 19.17, 17.65, 19.25, 31.09, 21.20, 14.98, 17.23, 12.89, 17.38, 24.81, 23.17, 19.00, 20.76, 14.10, 14.59, 15.82, 13.72, 17.56], 
                "inflow": [12.37, 15.33, 14.39, 10.75, 12.23, 11.97, 13.80, 12.29, 11.81, 12.42, 12.81, 11.43, 13.10, 12.48, 13.91, 13.14, 14.29, 10.50, 14.28, 15.85, 15.35, 11.83, 11.27, 12.22, 15.04, 10.95, 13.88, 11.39, 10.42, 15.84, 14.36, 13.72, 12.12, 13.82, 10.47, 10.15, 10.87, 11.21, 11.03, 12.24, 13.19, 13.18, 11.28, 10.97, 10.80, 12.41, 11.25, 13.89, 17.31, 11.65, 12.09, 12.04, 10.37, 13.56, 12.33, 9.49, 12.31, 10.75, 14.28, 15.08, 13.74, 14.14, 15.04, 13.16, 9.62, 11.98, 14.99, 12.90, 11.80, 13.42, 18.12, 14.01, 10.75, 10.49, 8.21, 11.71, 19.10, 14.22, 10.82, 11.84, 8.66, 9.01, 9.52, 9.76, 11.0],
                "river_table_data": [
                    {"Река / Створ": "р.Шарын - уроч Сарытогай", "Норма": 36.8, "Пик": "66.2 (2010)", "Мин": "22.6 (1944)", "Динамика": "↗ умеренное увеличение"},
                    {"Река / Створ": "р. Шилик - с. Малыбай", "Норма": 32.3, "Пик": "50.6 (2002)", "Мин": "26.1 (1957)", "Динамика": "↗ слабо выраженное увеличение"},
                    {"Река / Створ": "р. Каратал - с. Каратальское", "Норма": 24.9, "Пик": "55.6 (2016)", "Мин": "16.0 (1933)", "Динамика": "↔ существенных отклонений от нормы не выявлено"},
                    {"Река / Створ": "р. Лепсы - аул Лепси", "Норма": 19.6, "Пик": "32.3 (2010)", "Мин": "10.8 (1933)", "Динамика": "↗ отмечается умеренный рост стока"},
                    {"Река / Створ": "р. Тентек - аул Тонкерис", "Норма": 48.5, "Пик": "74.8 (2010)", "Мин": "23.2 (2020)", "Динамика": "↘ выраженное снижение среднегодовых расходов"},
                    {"Река / Створ": "р. Коргас – в 11 км выше с. Баскуншы", "Норма": 17.9, "Пик": "24.3 (2016)", "Мин": "10.9 (1957)", "Динамика": "↗ умеренное увеличение"},
                    {"Река / Створ": "р. Нарынкол – с. Нарынкол", "Норма": 1.50, "Пик": "2.32 (1942)", "Мин": "0.72 (2014)", "Динамика": "↔ близкая к стационарной"},
                    {"Река / Створ": "р. Текес – с. Текес", "Норма": 8.98, "Пик": "15.9 (2010)", "Мин": "5.05 (1944)", "Динамика": "↗ умеренное увеличение водности"},
                    {"Река / Створ": "р. Или – пр. Добын", "Норма": 423.0, "Пик": "642.0 (2016)", "Мин": "287.0 (2014)", "Динамика": "↗ слабо выраженная тенденция увеличения среднегодовых расходов воды"},
                    {"Река / Створ": "р. Баянкол – с. Баянкол", "Норма": 10.98, "Пик": "15.6 (1953)", "Мин": "5.55 (1946)", "Динамика": "↗ слабо выраженная тенденция увеличения среднегодовых расходов воды"},
                    {"Река / Створ": "р. Емель – пос. Кызылту", "Норма": 12.78, "Пик": "31.4 (2010)", "Мин": "2.51 (2023)", "Динамика": "↗ слабо выраженная тенденция увеличения среднегодовых расходов воды"}
            ]                
        },
            "Жайык-Каспийский ВХБ": {
                "photo": "Жайык-Каспий.tiff",
                "площадь": "645 000 км²",
                "гп_кол": "52",
                "рек_всего": "200-240",
                "артерия": "Река Жайык - трансграничная река бассейна Каспийского моря с преимущественно снеговым типом питания. Для реки характерен интенсивный весенний паводочный период, имеет высокую рыбохозяйственную значимость, включая нерестовые миграции осетровых. Географически служит естественной линией разграничения Европы и Азии.",
                "объекты": "Около 30 водохранилищ",
                "рек_инфо": "Больших и средних: 10 / Малых: 180-200 ",
                "местные_текст": "Сток формируется реками Илек, Большая Кобда, Орь, Уил, Эмба.",
                "приток_текст": "Трансграничный приток из России.",
                "years": list(range(1940, 2024)),
                "local_flow": [2.44, 8.12, 10.59, 3.36, 1.01, 2.16, 8.28, 2.86, 10.75, 4.52, 1.55, 1.03, 6.33, 1.61, 3.04, 1.35, 3.34, 7.63, 3.39, 4.56, 3.63, 1.90, 2.15, 3.91, 3.17, 1.27, 5.73, 0.20, 1.61, 2.09, 8.30, 5.54, 3.81, 3.43, 2.21, 1.56, 2.07, 1.85, 2.66, 5.22, 4.58, 4.32, 1.35, 4.23, 0.69, 5.60, 1.16, 3.42, 2.33, 1.63, 2.85, 3.88, 1.12, 9.85, 4.28, 1.65, 2.51, 4.73, 4.58, 2.02, 4.34, 1.55, 3.94, 1.31, 4.38, 6.08, 1.04, 4.96, 1.18, 0.75, 1.44, 2.26, 1.33, 0.56, 2.73, 3.03, 4.70, 3.64, 2.32, 0.50, 0.56, 0.72, 7.07, 12.83, 23.19], 
                "inflow": [4.15, 18.72, 14.63, 5.82, 3.70, 6.69, 21.48, 18.80, 16.72, 8.90, 4.90, 3.93, 7.24, 6.88, 5.02, 3.07, 6.22, 21.41, 8.53, 9.38, 8.78, 5.37, 7.38, 10.38, 11.70, 6.44, 8.60, 2.90, 5.39, 5.92, 18.82, 14.95, 6.78, 4.93, 8.18, 3.77, 5.50, 4.02, 7.17, 7.06, 6.83, 10.59, 6.88, 8.84, 3.69, 8.56, 8.57, 11.89, 10.25, 7.76, 16.40, 11.92, 6.40, 15.46, 14.46, 7.26, 6.62, 6.67, 10.63, 6.98, 13.41, 11.75, 13.85, 9.86, 9.75, 10.46, 5.12, 8.66, 7.50, 3.67, 5.47, 6.27, 5.48, 7.78, 7.23, 4.18, 7.36, 7.99, 4.78, 3.19, 3.95, 3.33, 4.34, 5.84, 12.50],
                "river_table_data": [
                    {"Река / Створ": "р. Орь – с. Бугетсай", "Норма": 5.44, "Пик": "30.4 (2024)", "Мин": "0.12 (1967)", "Динамика": "↔ Стабильно"},
                    {"Река / Створ": "р. Илек – г. Актобе", "Норма": 16.3, "Пик": "59.3 (2024)", "Мин": "1.57 (1967)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Б.Кобда – с. Кобда", "Норма": 5.77, "Пик": "26 (2024)", "Мин": "1.00 (1944)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Уил – пос. Уил", "Норма": 7.87, "Пик": "74.7 (2024)", "Мин": "0.19 (2021)", "Динамика": "↗ Рост"},
                    {"Река / Створ": "р. Эмба – с. Акмечеть", "Норма": 14.3, "Пик": "156 (2024)", "Мин": "0.06 (2021)", "Динамика": "↔ Стабильно"},
                    {"Река / Створ": "р. Жайык – пос. Январцево", "Норма": 343, "Пик": "793 (1957)", "Мин": "96 (1967)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Шаган – с. Чувашинское", "Норма": 8.71, "Пик": "29.8 (1946)", "Мин": "1.02 (2020)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Быковка – с. Чеботарево", "Норма": 0.40, "Пик": "1.24 (1946)", "Мин": "0.07 (2021)", "Динамика": "↘ Снижение"}
            ]                
        },
            "Есильский ВХБ": {
                "photo": "Есильский.tiff",
                "площадь": "237 226 км²",
                "гп_кол": "43",
                "рек_всего": "2 000",
                "артерия": "Река Есиль - равнинная река степной зоны с преимущественно снеговым питанием и продолжительным весенним половодьем. Отличается значительной межгодовой изменчивостью стока. Формирует водно-экологический каркас северных регионов и играет важную роль в водоснабжении населённых пунктов.",
                "объекты": "Около 50 водохранилищ.",
                "рек_инфо": " Большие и средние: 20-25/ Малые:более 1900",
                "местные_текст": "Сток формируется реками Есиль, Калкутан, Жабай.",
                "приток_текст": "",                
                "years": list(range(1940, 2024)),
                "local_flow": [1.05, 4.15, 4.06, 2.32, 0.68, 0.57, 3.36, 3.72, 6.06, 3.72, 0.95, 0.99, 0.57, 1.27, 3.76, 1.93, 0.73, 1.24, 1.58, 2.41, 2.97, 2.88, 1.52, 0.98, 4.02, 1.20, 2.31, 0.30, 0.46, 0.60, 2.32, 4.12, 4.49, 2.44, 1.19, 0.64, 1.45, 0.81, 3.15, 2.66, 2.46, 2.44, 1.49, 5.32, 2.48, 4.68, 2.90,3.79, 2.76, 1.30, 5.16, 3.02, 0.86, 5.63, 3.10, 3.44, 1.55, 2.91, 0.73, 0.42, 0.59, 2.08, 6.14, 1.08, 1.34, 3.10, 0.57,	3.79, 1.00, 0.71, 1.54, 1.16, 1.09, 1.81, 5.98, 2.83, 3.07, 8.88, 1.66, 4.41, 2.74, 2.11, 1.28, 3.10, 6.56],
                "inflow": [None],
                "river_table_data": [
                    {"Река / Створ": "р. Есиль – с. Астана", "Норма": 4.73, "Пик": "22.1 (1948)", "Мин": "0.10 (1967)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Жабай – с. Атбасар", "Норма": 9.93, "Пик": "70.5 (2017)", "Мин": "0.97 (1937)", "Динамика": "↗ Рост"},
                    {"Река / Створ": "р. Калкутан – с. Калкутан", "Норма": 7.24, "Пик": "33.3 (2002)", "Мин": "0.10 (1977)", "Динамика": "↘ Снижение"},
            ]                
        },
            "Нура-Сарысуйский ВХБ": {
                "photo": "Нура-Сарысу.tiff",
                "площадь": "290 210 км²",
                "гп_кол": "27",
                "рек_всего": "15",
                "артерия": "Река Нура - река центрального Казахстана с преимущественно снеговым питанием и ограниченным водным стоком. Впадает в бессточную систему озёр Тенгиз-Коргалжынской впадины. Имеет значимое экологическое значение в формировании водно-болотных угодий.",
                "объекты": "около 400 водохранилищ, прудов и искусственных накопителей воды различного размера и назначения",
                "рек_инфо": " Основные: 2 / Притоки: 13",
                "местные_текст": "Сток формируется реками Нура, Сарысу, Каракенгир, Жиланды.",
                "приток_текст": "",                   
                "years": list(range(1940, 2024)),
                "local_flow": [0.49, 2.10, 1.28, 1.51, 0.48, 1.33, 1.06, 0.99, 2.68, 2.98, 0.73, 0.55, 0.78, 0.90, 2.35, 0.93, 0.63, 0.69, 1.95, 1.57, 1.87, 1.19, 1.08, 0.42, 1.15, 0.72, 1.51, 0.27, 0.36, 0.96, 1.16, 1.48, 1.75, 1.33, 0.48, 0.22, 0.89, 1.87, 0.71, 1.04, 0.63, 0.85, 0.92, 0.97, 0.96, 0.91, 1.54, 1.23, 1.45, 0.78, 1.77, 1.84, 0.97, 2.37, 0.66, 1.16, 0.84, 1.42, 0.59, 0.32, 0.66, 1.16, 2.33, 0.74, 1.89, 0.80, 0.32, 1.36, 0.50, 0.37, 1.53, 0.71, 0.42, 1.36, 1.42, 3.80, 2.39, 3.81, 1.83, 2.24, 1.24, 0.78, 1.30, 0.75, 2.26], 
                "inflow": [None],
                "river_table_data": [
                    {"Река / Створ": "р. Нура - ж.-д. ст. Балыкты", "Норма": 9.03, "Пик": "42.2 (2015)", "Мин": "0.36 (1936)", "Динамика": "↘ Рост"},
                    {"Река / Створ": "р. Нура - с. Р. Кошкарбаева", "Норма": 22.6, "Пик": "108.5 (2017)", "Мин": "1.44 (1939)", "Динамика": "↗ Рост"},
                    {"Река / Створ": "р. Шерубайнура - раз. Карамурын", "Норма": 5.81, "Пик": "20.9 (2017)", "Мин": "0.40 (1975)", "Динамика": "↗ Стабильно"},
                    {"Река / Створ": "р. Сарысу - раз. № 189", "Норма": 3.02, "Пик": "29.3 (2015)", "Мин": "0.02 (2012)", "Динамика": "↘ Рост"},
                    {"Река / Створ": "р. Каракенгир - 12 км выше устья р. Жиланды", "Норма": 4.08, "Пик": "19.4 (1949)", "Мин": "0.00 (1937)", "Динамика": "↔ Снижение"}
            ]               
        },
            "Шу-Таласский ВХБ": {
                "photo": "Шу-Таласс.tiff",
                "площадь": "160 500 км²",
                "гп_кол": "22",
                "рек_всего": "850",
                "артерия": "Река Шу - трансграничная река с истоками в горных районах Кыргызстана. В пределах Казахстана характеризуется снижением стока вследствие инфильтрации и водоотбора. Гидрологический режим определяется сочетанием снегового и ледникового питания. Река Талас - горная трансграничная река с выраженным весенне-летним максимумом стока. Значительная часть воды используется для орошения, что приводит к уменьшению водности в нижнем течении. Исторически играла роль в формировании оазисных систем региона.",
                "объекты": "Свыше 21 водохранилищ и прудов",
                "рек_инфо": "Большие и средние: 25-30 / Малых: 800",
                "местные_текст": "Сток формируется реками Курагаты и Терис.",
                "приток_текст": "Трансграничный приток из Кыргызстана фиксируется в створах 7 рек -  Шу, Талас, Ассы -  Карабалта, Аксу, Саргоу, Токташ.",
                "years": list(range(1940, 2024)),
                "local_flow": [0.63, 0.74, 1.02, 0.75, 0.82, 0.70, 0.78, 0.72, 1.00, 0.89, 0.86, 0.78, 1.10, 1.10, 1.00, 1.21, 1.03, 0.69, 1.36, 1.74, 1.61, 1.05, 0.95, 1.11, 1.33, 1.01, 1.51, 1.59, 1.45, 3.26, 1.60, 1.48, 1.61, 1.95, 1.00, 1.04, 1.08, 1.09, 1.47, 1.69, 1.25, 1.08, 0.93, 0.87, 1.02, 1.23, 0.83, 1.42, 1.60, 1.10, 1.56, 1.17, 1.29, 1.80, 2.08, 1.37, 1.45, 1.02, 1.42, 1.34, 1.05, 1.04, 2.02, 1.70, 1.60, 1.63, 1.47, 1.16, 1.00, 1.35, 1.46, 1.47, 1.38, 1.41, 1.71, 1.58, 2.05, 2.61, 1.85, 1.86, 1.69, 1.67, 0.94, 1.00, 1.08], 
                "inflow": [2.37, 2.85, 3.74, 2.77, 2.45, 2.97, 3.12, 2.83, 2.79, 3.35, 2.93, 2.78, 3.63, 3.29, 3.47, 3.35, 3.20, 2.50, 4.20, 3.56, 3.55, 2.71, 2.55, 2.76, 3.08, 2.39, 3.21, 2.97, 2.83, 4.56, 2.98, 2.85, 2.71, 2.09, 1.85, 1.98, 1.66, 1.53, 1.82, 2.18, 1.89, 2.22, 1.95, 1.96, 1.86, 2.11, 1.92, 2.94, 2.93, 2.47, 2.76, 2.20, 2.26, 2.44, 3.39, 2.36, 2.26, 1.90, 2.98, 3.13, 2.52, 2.22, 4.14, 4.35, 3.90, 4.02, 2.82, 2.47, 1.98, 2.73, 3.85, 3.25, 2.66, 2.67, 2.55, 2.82, 5.08, 5.01, 3.32, 2.76, 2.41, 1.91, 2.52, 2.28, 3.06],
                "river_table_data": [
                    {"Река / Створ": "р. Терис – с. Нурлыкент", "Норма": 5.32, "Пик": "13.2 (1969)", "Мин": "2.19 (1957)", "Динамика": "↔ Стабильно"},
                    {"Река / Створ": "р. Курагаты – ж.-д. ст. Аспара", "Норма": 4.15, "Пик": "15.8 (1969)", "Мин": "0.31 (1945)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Шу – с. Кайнар", "Норма": 56.7, "Пик": "100.0 (1969)", "Мин": "28.7 (1977)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Талас – с. Жасоркен", "Норма": 24.5, "Пик": "44.7 (2016)", "Мин": "11.8 (2015)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Асса – ж.-д.ст. Маймак", "Норма": 10.5, "Пик": "24.9 (1969)", "Мин": "5.48 (1980)", "Динамика": "↔ Стабильно"},
                    {"Река / Створ": "р. Саргоу – Трансграничный", "Норма": 0.29, "Пик": "0.52 (2018)", "Мин": "0.088 (2021)", "Динамика": "↔ Стабильно"},
                    {"Река / Створ": "р. Токташ – с. Жаугаш Батыра", "Норма": 1.26, "Пик": "2.23 (2016)", "Мин": "0.67 (2022)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Аксу – а. Аксу", "Норма": 15.3, "Пик": "32.0 (2016)", "Мин": "2.81 (2024)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Карабалта – а. Баласагун", "Норма": 1.40, "Пик": "4.0 (2016)", "Мин": "0.15 (2024)", "Динамика": "↔ Стабильно"}
]
        },
            "Тобыл-Торгайский ВХБ": {
                "photo": "Тобыл-Торгай.tiff",
                "площадь": "347 680 км²",
                "гп_кол": "25",
                "рек_всего": "Свыше 350",
                "артерия": "Река Тобыл - левобережный приток Ертиса, формирующийся в условиях лесостепной и степной зон. Отличается развитой озёрной системой в бассейне и значительным антропогенным регулированием стока. Входит в трансграничную водную систему бассейна Оби.",
                "объекты": "Свыше 180-190 водохранилищ и прудов.",
                "рек_инфо": "2 / Большие и средные: 21",
                "местные_текст": "Для оценки водных ресурсов, формирующихся в Тобыл-Торгайском ВХБ выбраны постоянно действующие 4 реки бассейна с наибольшей водностью таких как: Тобыл, Аят, Кара Торгай, Иргиз, определяющих в основном поверхностные водные ресурсы, которые в сумме составляют около 76 % всех местных водных ресурсов.",
                "приток_текст": "Приток, поступающий в пределы Тобыл-Торгайского водохозяйственного бассейна из РФ по реке Тобыл и Тогызак.",
                "years": list(range(1940, 2025)),
                "local_flow": [0.62, 5.48, 4.59, 1.50, 0.21, 0.65, 2.61, 3.59, 3.88, 1.39, 1.14, 0.35, 1.07, 1.67, 1.26, 0.62, 0.85, 3.66, 1.05, 1.22, 1.50, 0.71, 1.09, 0.84, 2.38, 0.71, 1.51, 0.17, 0.24, 0.94, 1.93, 2.61, 1.12, 1.05, 0.91, 0.26, 0.65, 0.55, 1.71, 1.08, 0.80, 1.64, 0.38, 2.16, 0.66, 1.68, 1.11, 1.83, 1.65, 1.21, 2.17, 0.86, 0.76, 3.94, 2.35, 1.40, 0.81, 0.80, 1.09, 0.64, 2.77, 1.18, 2.93, 0.74, 1.86, 2.76, 0.21, 2.14, 0.79, 0.25, 1.51, 0.94, 0.80, 0.57, 1.03, 1.03, 1.22, 1.36, 1.34, 0.33, 0.74, 0.66, 0.81, 0.98, 5.13, 0.71], 
                "inflow": [0.19, 1.19, 1.03, 0.42, 0.15, 0.23, 0.62, 1.04, 0.84, 0.18, 0.37, 0.21, 0.26, 0.61, 0.12, 0.09, 0.19, 1.16, 0.17, 0.29, 0.54, 0.22, 0.19, 0.26, 0.27, 0.14, 0.27, 0.21, 0.19, 0.49, 0.74, 0.47, 0.27, 0.14, 0.23, 0.07, 0.15, 0.06, 0.31, 0.17, 0.11, 0.35, 0.13, 0.38, 0.17, 0.38, 0.08, 0.23, 0.25, 0.14, 0.76, 0.27, 0.12, 0.84, 1.01, 0.37, 0.13, 0.13, 0.21, 0.29, 0.80, 0.44, 0.65, 0.31, 0.30, 0.76, 0.19, 0.59, 0.52, 0.08, 0.22, 0.28, 0.34, 0.52, 0.33, 0.08, 0.25, 0.24, 0.21, 0.08, 0.15, 0.19, 0.07, 0.23, 0.93, 0.28],
                "river_table_data": [
                    {"Река / Створ": "р. Тобыл – с. Гришенка", "Норма": 7.95, "Пик": "38.7 (1941)", "Мин": "0.12 (1991)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Тобыл – г. Костанай", "Норма": 13.06, "Пик": "64.5 (1942)", "Мин": "0.93 (1979)", "Динамика": "↗ Снижение"},
                    {"Река / Створ": "р. Аят – с. Варваринка", "Норма": 6.47, "Пик": "23.9 (1941)", "Мин": "0.81 (2015)", "Динамика": "↗ Снижение"},
                    {"Река / Створ": "р. Тогызак – с. Тогузак", "Норма": 2.97, "Пик": "10.7 (1947)", "Мин": "0.26 (1936)", "Динамика": "↘ Снижение"},
                    {"Река / Створ": "р. Кара-Торгай – г. Урпек", "Норма": 10.49, "Пик": "26.3 (1948)", "Мин": "0.74 (1968)", "Динамика": "↔ Снижение"},
                    {"Река / Створ": "р. Иргиз – с. Шенбертал", "Норма": 9.28, "Пик": "41.5 (1941)", "Мин": "0.095 (2019)", "Динамика": "↘ Снижение"}
            ]                
        }
            # Добавьте сюда остальные ВХБ по аналогии
    }
    
                
    import base64

    for name in vxb_list:
        details = VXB_FULL_DATA.get(name, {})
        if not details:
            st.warning(f"Данные для {name} еще не внесены в справочник.")
            continue

        item_stats = VXB_STATS[name]
        is_active = (name == display_name)
        anchor_name = name.replace(' ', '-').lower()
        
        # Формируем путь к фото
        photo_filename = details.get("photo", "")
        photo_path = os.path.join(BASE_IMAGE_PATH, photo_filename)
        
        st.markdown(f"<div id='{anchor_name}'></div>", unsafe_allow_html=True)
        
        with st.container(border=is_active):
            st.markdown(f"### {'🌟' if is_active else '🔹'} {name}")
            
            # Увеличиваем пропорцию колонки для изображения
            img_col, info_col = st.columns([2, 1])
            

        import base64
        import os
        from PIL import Image
        import io

        with img_col:
            # Используем photo_path (проверьте, что переменная определена выше)
            if photo_filename and os.path.exists(photo_path):
                try:
                    # Открываем TIFF изображение через Pillow
                    with Image.open(photo_path) as img:
                        # Конвертируем в RGB (важно для TIFF, если там CMYK или слои)
                        img = img.convert("RGB")
                        
                        # Сохраняем в буфер памяти как PNG или JPEG
                        buffer = io.BytesIO()
                        img.save(buffer, format="PNG")
                        file_bytes = buffer.getvalue()
                        
                        # Кодируем в Base64
                        encoded_base64 = base64.b64encode(file_bytes).decode("utf-8")
                    
                    # Теперь MIME-тип всегда image/png, так как мы сконвертировали
                    mime_type = "image/png"

                    html_code = f"""
                        <div style="width: 100%; text-align: center;">
                            <img src="data:{mime_type};base64,{encoded_base64}" 
                                 style="width: 100%; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                            <p style="color: gray; margin-top: 8px;">Вид бассейна: {name}</p>
                        </div>
                    """
                    st.markdown(html_code, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Ошибка при обработке TIFF: {e}")
            else:
                st.warning(f"Файл не найден по пути: {photo_path}")
                
                                        
            with info_col:
                st.markdown(f"##### 📝 Гидрологическая справка: {name}")
                
                # Динамические метрики из справочника
                m1, m2, m3 = st.columns(3)
                m1.metric("Площадь", details["площадь"])
                m2.metric("ГП в ВХБ", details["гп_кол"])
                m3.metric("Всего рек", details["рек_всего"])

                # Блок Местные ресурсы vs Приток
                col_res, col_inf = st.columns(2)
                with col_res:
                    st.write("💧︎ **Местные ресурсы**")
                    st.caption(details["местные_текст"])
                with col_inf:
                    st.write("💧 **Приток**")
                    st.caption(details["приток_текст"])

                # ГРАФИК (Теперь рисуется для каждого ВХБ свой!)
                mini_fig = go.Figure()
                mini_fig.add_trace(go.Bar(
                    x=details["years"], y=details["local_flow"], 
                    name='Местный сток', marker_color='#1f77b4'
                ))
                mini_fig.add_trace(go.Bar(
                    x=details["years"], y=details["inflow"], 
                    name='Приток', marker_color='#a6cee3'
                ))
                mini_fig.update_layout(
                    barmode='stack', height=180, 
                    margin=dict(l=0,r=0,t=10,b=0), 
                    template="plotly_white", showlegend=False,
                    xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                    yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
                )
                # ВАЖНО: используем уникальный key для каждого графика
                st.plotly_chart(mini_fig, use_container_width=True, key=f"mini_chart_{name}")

                # Детализация внизу блока
                st.markdown("---")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"🌊 **Артерия:** {details['артерия']}")

                with col_b:
                    st.write(f"🏢 **Объекты:** {details['объекты']}")
                    st.write(f"📊 **Норма (W):** {item_stats['норма']} км³/год")
                # НОВЫЙ БЛОК: Текстовая справка по рекам
                        
            # Проверяем наличие нового ключа с данными для таблицы
            if "river_table_data" in details:
                st.markdown("---")
                st.markdown("#### 📋 Сводная таблица гидрологических показателей")
               
                st.markdown("""
                    <style>
                    [data-testid="stTable"] {
                        font-size: 20px;
                    }
                    /* Для старых версий Streamlit или специфических контейнеров */
                    .css-110034a, .stDataFrame div {
                        font-size: 1.2rem !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)
    

               
                # Создаем DataFrame из списка словарей
                df_rivers = pd.DataFrame(details["river_table_data"])
                
                # Отображаем таблицу
                st.dataframe(
                    df_rivers,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Река / Створ": st.column_config.TextColumn("🌊 Река / Створ", width="large"),
                        "Норма": st.column_config.NumberColumn("Норма (W)", format="%.1f м³/с"),
                        "Пик": st.column_config.TextColumn("🚀 Максимум"),
                        "Мин": st.column_config.TextColumn("📉 Минимум"),
                        "Динамика": st.column_config.TextColumn("Тренд")
                    }
                )
                
                # Если вам нужно сохранить старые текстовые описания, их можно вывести так:
                # (Но только если в словаре остался старый ключ river_descriptions с текстом)
                if "river_descriptions" in details and isinstance(details["river_descriptions"], dict):
                    with st.expander("🔍 Читать полные текстовые описания анализа"):
                        for r, t in details["river_descriptions"].items():
                            st.write(f"**{r}:** {t}")
                


               
        # --- СПЕЦИАЛЬНЫЙ БЛОК ДЛЯ АРАЛО-СЫРДАРЬИНСКОГО ВХБ ---
        if "Арало-Сырдарьинский" in name:
            st.markdown("---")
            st.markdown("### 📊 Детальный анализ стока по основным водным артериям")

            # Описание блоков (используем st.status или красивые контейнеры)
            desc_col1, desc_col2 = st.columns(2)
            with desc_col1:
                st.info("""**Местный сток:** Для оценки водных ресурсов, формирующихся в Арало-Сырдарьинского ВХБ выбраны постоянно действующие 3 крупных рек бассейна с наибольшей водностью таких как: Арысь, Шаян и Бугунь, определяющих в основном поверхностные водные ресурсы, которые в сумме составляют около 50 % всех местных водных ресурсов.""")   
            with desc_col2:
                st.info("""**Приток:** Приток, поступающий в пределы Арало-Сырдариинского водохозяйственного бассейна из РУ по реке Сырдарья фиксируется в створе выше устья р. Келес.""")

            # 1. Подготовка данных
            years = list(range(1940, 2025))
            data_rivers = {
                "Год": years,
                "р. Сырдарья - н.б. Шардаринского водохранилища": [492, 690, 824, 716, 544, 773, 732, 539, 687, 929, 567, 598, 1066, 894, 1065, 737, 724, 450, 923, 930, 882, 438, 353, 631, 728, 245, 592, 469, 564, 917, 574, 538, 519, 559, 245, 167, 210, 225, 275, 405, 336, 304, 298, 250, 248, 269, 226, 336, 581, 402, 466, 449, 510, 678, 627, 402, 492, 439, 665, 546, 412, 386, 606, 677, 664, 703, 536, 551, 347, 471, 842, 426, 587, 413, 533, 468, 466, 728, 392, 451, 316, 268, 346, 349, 328],
                "р. Сырдарья - ж.-д. ст. Томенарык": [457, 631, 808, 692, 496, 713, 713, 471, 596, 856, 505, 602, 1023, 872, 986, 703, 678, 431, 836, 871, 985, 423, 294, 563, 690, 247, 509, 439, 438, 840, 489, 426, 443, 505, 201, 122, 148, 152, 208, 348, 278, 269, 234, 183, 183, 198, 160, 273, 501, 320, 340, 343, 388, 593, 669, 422, 430, 373, 504, 521, 300, 330, 501, 547, 565, 566, 434, 482, 313, 360, 694, 345, 511, 350, 510, 444, 502, 690, 404, 429, 319, 299, 317, 375, 371],
                "р. Сырдарья - г. Казалы": [402, 455, 524, 513, 385, 490, 519, 340, 422, 508, 378, 419, 595, 620, 670, 530, 520, 300, 568, 580, 667, 401, 184, 335, 473, 149, 304, 277, 231, 554, 313, 259, 221, 283, 61.2, 19.4, 17.9, 15.2, 24.8, 100, 89.4, 76.8, 55.2, 29.8, 19.0, 21.6, 26.6, 64.8, 217, 138, 114, 117, 144, 296, 310, 84.3, 139, 109, 257, 144, 77.1, 62.2, 316, 329, 305, 314, 252, 255, 144, 163, 341, 205, 212, 228, 236, 63.0, 58.6, 350, 186, 167, 72.9, 76, 75, 112, 128],
                "р. Келес - устье": [2.70, 10.50, 6.70, 7.20, 7.80, 7.20, 8.50, 3.20, 8.20, 22.70, 8.80, 2.50, 6.70, 9.50, 13.20, 8.70, 6.20, 5.20, 19.00, 14.00, 18.00, 7.70, 8.00, 11.80, 14.70, 7.00, 7.03, 14.10, 13.40, 27.60, 11.70, 7.86, 15.30, 10.90, 6.83, 5.65, 9.16, 8.79, 15.70, 16.40, 13.30, 13.40, 9.14, 6.14, 8.61, 12.80, 6.29, 1.50, 16.30, 13.20, 19.50, 16.00, 19.70, 27.20, 24.50, 14.80, 16.10, 17.20, 26.10, 22.20, 14.50, 13.70, 23.80, 25.50, 21.40, 24.80, 19.20, 25.00, 14.50, 27.20, 29.30, 18.60, 26.50, 24.60, 25.60, 26.40, 28.10, 28.50, 20.40, 25.20, 20.4, 16.60, 24.10, 23.9, 30.9],
                "р. Арысь - ж.-д. ст. Арысь": [30.9, 44.9, 48.6, 39.7, 29.0, 33.4, 45.7, 35.6, 37.8, 70.0, 47.8, 36.1, 65.5, 54.3, 69.0, 50.4, 45.0, 34.9, 80.7, 76.2, 70.3, 31.0, 22.2, 32.3, 44.9, 11.9, 16.2, 14.9, 20.0, 94.9, 26.7, 17.9, 33.3, 27.4, 12.5, 16.4, 10.5, 11.0, 15.6, 34.5, 19.0, 15.1, 13.7, 10.3, 14.4, 12.9, 5.8, 21.3, 13.9, 8.67, 27.7, 16.1, 23.5, 38.6, 55.3, 24.7, 15.5, 17.5, 33.9, 22.4, 13.1, 11.5, 53.8, 36.1, 29.2, 62.7, 29.5, 37.1, 15.9, 22.3, 38.6, 17.3, 39.6, 23.8, 39.6, 31.8, 40.5, 64.7, 20.5, 22.4, 13.5, 17.7, 22.5, 23.6, 32.4],
                "р. Аксу - с. Саркырама": [8.49, 10.60, 11.50, 9.27, 2.57, 9.13, 11.70, 8.28, 10.60, 10.80, 7.96, 8.72, 13.10, 10.20, 10.60, 9.37, 9.20, 5.90, 13.50, 12.00, 12.10, 6.38, 6.64, 9.64, 9.11, 6.70, 10.60, 9.20, 11.80, 19.20, 10.40, 8.90, 9.97, 10.10, 5.93, 6.70, 7.68, 7.16, 11.30, 12.30, 8.14, 8.79, 5.83, 7.35, 7.79, 9.39, 8.06, 13.50, 11.20, 7.07, 12.70, 8.74, 11.60, 14.20, 14.70, 10.40, 11.60, 19.00, 15.00, 12.70, 8.54, 9.68, 16.00, 15.20, 12.00, 14.20, 11.10, 11.70, 8.01, 11.10, 17.90, 10.60, 11.90, 10.20, 12.90, 12.60, 13.20, 16.10, 10.30, 9.79, 6.60, 8.07, 10.20, 10.3, 11.6],
                "р. Бадам - с. Караспан ": [5.91, 7.91, 8.76, 6.65, 0.30, 6.51, 8.95, 5.71, 7.91, 8.74, 4.29, 5.79, 10.90, 8.61, 7.91, 8.95, 6.58, 4.67, 16.90, 8.58, 12.50, 5.24, 4.01, 5.69, 7.29, 3.70, 3.43, 4.56, 6.51, 16.05, 7.56, 4.89, 8.47, 7.05, 3.66, 2.26, 2.11, 5.73, 8.40, 9.52, 6.05, 4.37, 3.67, 2.50, 3.59, 3.70, 3.29, 6.04, 5.14, 4.03, 8.01, 6.69, 9.47, 13.40, 15.60, 8.23, 6.86, 6.74, 17.40, 12.80, 6.40, 5.20, 15.60, 13.10, 9.16, 16.00, 11.00, 15.10, 8.07, 13.70, 26.70, 8.68, 8.74, 9.87, 11.70, 9.24, 12.10, 13.60, 8.31, 7.84, 6.23, 3.82, 6.24, 5.9, 11],
                "р. Шаян - в 3,3 км ниже устья р. Акбет": [1.52, 2.79, 2.63, 1.69, 1.78, 1.69, 2.17, 1.21, 1.45, 3.90, 2.44, 1.12, 3.40, 2.45, 3.83, 1.67, 1.96, 1.30, 4.45, 3.90, 2.93, 1.57, 1.42, 1.31, 3.59, 1.29, 1.67, 1.78, 2.23, 4.98, 1.73, 1.33, 2.66, 2.60, 1.80, 3.40, 1.86, 1.53, 2.20, 2.64, 2.29, 2.44, 2.65, 1.69, 2.85, 2.60, 0.83, 2.35, 1.67, 1.46, 3.15, 2.51, 2.98, 3.23, 2.51, 1.85, 0.50, 0.87, 1.40, 1.09, 0.91, 1.15, 3.19, 3.30, 1.99, 2.73, 2.02, 2.07, 1.22, 1.93, 2.41, 1.04, 2.53, 2.08, 4.00, 3.44, 4.23, 3.43, 1.38, 2.71, 1.52, 2.03, 2.53, 1.98, 2.7],
                "р. Бугунь - с. Екпенды": [1.91, 5.36, 4.93, 2.38, 2.62, 2.36, 3.67, 1.06, 2.06, 7.89, 3.75, 1.42, 7.89, 4.51, 9.00, 3.48, 3.31, 2.00, 10.00, 8.95, 7.18, 2.60, 1.84, 2.34, 5.97, 2.01, 1.65, 1.73, 3.96, 13.30, 3.05, 1.70, 4.91, 4.16, 2.22, 4.06, 2.24, 1.85, 3.75, 6.42, 3.20, 3.53, 3.22, 1.36, 3.84, 4.16, 0.38, 5.60, 3.07, 1.75, 5.02, 2.82, 3.86, 5.30, 0.12, 2.81, 0.68, 2.23, 3.58, 2.11, 1.48, 1.38, 6.20, 6.05, 4.25, 6.66, 3.54, 4.01, 2.23, 3.04, 3.69, 1.64, 4.18, 4.04, 6.46, 5.30, 8.41, 8.92, 2.30, 4.13, 2.38, 4.34, 4.77, 4.53, 9.2],
            }
            df_local = pd.DataFrame(data_rivers)
            pritok_values = [487, 679, 818, 711, 539, 766, 724, 535, 680, 913, 562, 592, 1050, 884, 1050, 728, 719, 446, 899, 917, 989, 444, 387, 603, 715, 364, 797, 368, 457, 1600, 624, 445, 444, 536, 145, 132, 197, 229, 320, 448, 362, 361, 371, 287, 310, 314, 278, 407, 631, 408, 455, 444, 513, 680, 817, 458, 500, 448, 757, 588, 446, 429, 674, 865, 745, 706, 523, 570, 393, 463, 791, 424, 567, 430, 558, 464, 387, 710, 482, 442, 390, 298, 403, 465, 534]

            import plotly.graph_objects as go
# Настройки для легенды в 3 столбца
            legend_style = dict(
                orientation="h",
                y=-0.3,
                x=0.5,
                xanchor="center",
                entrywidth=0.4, # Устанавливаем ширину каждого элемента в 30% от общей ширины
                entrywidthmode="fraction" 
            )

            # --- 1. ГРАФИК МЕСТНОГО СТОКА ---
            fig_local = go.Figure()
            excel_colors = ['#ffffff', '#ff0000', '#ffff00', '#7030a0', '#996633'] 

            for i, col_name in enumerate(df_local.columns[1:]):
                fig_local.add_trace(go.Scatter(
                    x=df_local['Год'], 
                    y=df_local[col_name],
                    mode='markers+lines',
                    name=col_name,
                    line=dict(color='black', width=1),
                    marker=dict(
                        color=excel_colors[i % len(excel_colors)],
                        size=6,
                        line=dict(color='black', width=1)
                    ),
                    hovertemplate=f"<b>{col_name}</b><br>Год: %{{x}}<br>Сток: %{{y}} м³/с<extra></extra>"
                ))

            fig_local.update_layout(
                title="<b>ОСНОВНЫЕ РЕКИ БАССЕЙНА</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                height=500, # Немного увеличим высоту, чтобы легенда влезла комфортно
                template="plotly_white",
                hovermode="x unified",
                legend=legend_style, # ПРИМЕНЯЕМ СТИЛЬ С 3 СТОЛБЦАМИ
                margin=dict(l=40, r=20, t=60, b=100), # Увеличили b для легенды
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
            )

            # --- 2. ГРАФИК ПРИТОКА ---
            fig_pritok = go.Figure()

            fig_pritok.add_trace(go.Scatter(
                x=years, 
                y=pritok_values,
                mode='markers+lines',
                name='Значение стока',
                line=dict(color='black', width=1.5),
                marker=dict(color='#3498db', size=6, line=dict(color='black', width=1)),
                hovertemplate="Год: %{x}<br>Сток: %{y} м³/с<extra></extra>"
            ))

            # Тренд
            fig_pritok.update_layout(
                title="<b>ПРИТОК БАССЕЙНА</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                height=500,
                template="plotly_white",
                hovermode="x",
                legend=legend_style, # ПРИМЕНЯЕМ СТИЛЬ С 3 СТОЛБЦАМИ
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
           )

            # Отображение
            g_col1, g_col2 = st.columns(2)
            with g_col1:
                st.plotly_chart(fig_local, use_container_width=True, key=f"fixed_local_3col_{name}")
            with g_col2:
                st.plotly_chart(fig_pritok, use_container_width=True, key=f"fixed_pritok_3col_{name}")
                
            # 1. Объявляем функцию
            def show_aral_analysis():
                st.subheader("📊 Анализ суммарных водных ресурсов бассейна (1940–2024 гг.)")
                
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown("""
                        За рассматриваемый период с **1940 по 2024 гг.** прослеживается отчетливая тенденция к снижению объема стока, который в последние десятилетия часто опускается ниже исторической нормы.
                        """)
                    
                    with col2:
                        st.metric(label="Тренд стока", value="Снижение", delta="- плавный", delta_color="inverse")

                    st.divider()

                    st.write("""
                    Тенденция к сокращению объема стока объясняется тем, что в Арало-Сырдарьинском бассейне темпы роста температуры значительно опережают увеличение осадков, что ведет к деградации оледенения.
                    """)

                    st.info("""
                    **Ключевой фактор:** В отличие от северных бассейнов, здесь антропогенная нагрузка в виде интенсивного безвозвратного водопотребления на орошение и испарения из водохранилищ превышает естественные возможности восполнения рек, что формирует устойчивый отрицательный тренд и дефицит водных ресурсов в низовьях.
                    """, icon="💧")

                    st.warning("""
                    **Вывод:** Нисходящая линия тренда — это важный индикатор, который призывает к более 
                    рациональному и бережному использованию имеющихся запасов воды.
                    """, icon="⚠️")

            # 2. СРАЗУ ВЫЗЫВАЕМ
            show_aral_analysis()


          
        # --- СПЕЦИАЛЬНЫЙ БЛОК БАЛХАШ-АЛАКОЛЬСКОГО ВХБ ---
        if "Балкаш-Алакольский" in name:
            st.markdown("---")
            st.markdown("### 📊 Детальный анализ стока по основным водным артериям")

            desc_col1, desc_col2 = st.columns(2)
            with desc_col1:
                st.info("""**Местный сток:** Для оценки местных водных ресурсов территория бассейна поделена на 2 части:
    1. Иле-Балкашский бассейн; 2. Бассейн оз. Алаколь. 
Для оценки водных ресурсов, формирующихся в Иле-Балкашском бассейне выбраны постоянно действующие 4 крупные реки бассейна с наибольшей водностью таких как: рр. Шарын, Шилик впадающие в р. Иле, рр. Каратал, Лепси - в оз. Балкаш, определяющие в основном поверхностные водные ресурсы, которые в сумме составляют около 30 % всех местных водных ресурсов""")   
            with desc_col2:
                st.info("""**Приток:** В Балкаш-Алакольский ВХБ приток поступающий из КНР по реке Иле фиксируется в створе пр. Добын. Оценивается приток за вычетом оттока по рекам Текес, Баянкол, Нарынкол и сток реки Коргас в створе 11 км выше с. Баскуншы, который впадает в р. Иле выше створа пр. Добын. Приток из КНР по реке Емель поступающий в бассейн оз. Алаколь, фиксируется в створе пос. Кызылту""")

            # 1. Подготовка данных (Используем локальные имена переменных, чтобы не было "утечек")
            years_b = list(range(1940, 2025))
            data_rivers_b = {
                "Год": years_b,
                "р. Шарын - ур. Сарытогай": [29.4, 37.1, 38.8, 24.6, 22.6, 26.5, 35.2, 30.2, 30.7, 33.0, 34.3, 33.1, 38.5, 37.8, 53.1, 39.0, 46.3, 33.0, 38.8, 47.3, 41.8, 35.2, 30.4, 34.4, 46.0, 32.4, 38.7, 38.8, 29.6, 53.2, 46.0, 43.2, 38.3, 43.0, 32.2, 34.7, 29.1, 26.8, 29.3, 34.8, 35.6, 38.2, 30.5, 30.3, 26.4, 37.2, 33.1, 49.2, 54.9, 41.5, 38.2, 33.7, 32.7, 42.6, 44.6, 25.4, 39.6, 33.9, 44.5, 32.3, 42.9, 50.1, 53.2, 59.1, 62.1, 51.2, 43.3, 41.1, 37.6, 46.7, 66.2, 46.9, 35.3, 39.6, 27.7, 38.8, 56.7, 54.5, 45.7, 50.6, 45.7, 39.3, 33.1, 27.9, 36.1],
                "р. Шилик - с. Малыбай": [26.8, 33.1, 37.4, 29.7, 30.7, 34.4, 34.0, 33.1, 31.7, 33.9, 34.2, 32.2, 36.3, 35.0, 34.8, 33.3, 35.7, 26.1, 29.1, 34.2, 31.2, 29.1, 31.5, 28.6, 31.0, 30.2, 35.8, 29.8, 30.6, 32.5, 34.9, 34.0, 31.8, 35.5, 28.9, 28.5, 29.9, 30.1, 34.4, 29.0, 30.0, 31.7, 27.1, 32.0, 31.5, 31.4, 29.1, 32.0, 48.6, 34.0, 39.8, 41.7, 38.4, 39.7, 43.6, 35.4, 37.0, 47.9, 42.7, 40.9, 41.3, 39.7, 50.6, 43.0, 39.9, 37.0, 39.6, 41.9, 35.2, 33.6, 41.1, 45.6, 41.9, 32.3, 30.1, 38.1, 38.5, 41.8, 36.1, 39.7, 35.4, 34.2, 39.0, 27.1, 34.2],
                "р. Каратал - с. Каратальское": [24.6, 34.4, 29.7, 17.1, 16.3, 16.7, 30.4, 25.1, 24.4, 24.7, 23.7, 20.8, 33.7, 23.0, 24.2, 27.7, 27.1, 17.8, 34.6, 33.2, 35.1, 23.0, 21.4, 24.1, 28.9, 16.4, 33.3, 21.4, 23.2, 34.9, 23.8, 30.3, 28.5, 31.8, 17.9, 18.2, 21.5, 25.0, 24.9, 31.3, 31.4, 27.6, 20.4, 24.8, 28.8, 32.4, 24.3, 37.6, 49.6, 29.1, 38.1, 28.6, 32.2, 47.4, 44.8, 33.9, 37.0, 28.6, 32.4, 29.9, 24.9, 40.5, 43.2, 34.5, 18.6, 21.7, 19.3, 31.3, 35.5, 29.6, 55.4, 32.3, 25.1, 33.7, 31.3, 31.0, 55.5, 45.1, 36.9, 35.2, 25.1, 30.0, 32.2, 32.9, 42.7],
                "р. Лепсы - аул Лепси": [17.1, 25.7, 21.8, 13.6, 14.1, 12.1, 21.9, 18.5, 16.2, 19.5, 19.2, 15.8, 23.6, 19.6, 19.6, 21.0, 21.7, 13.7, 26.6, 26.0, 23.4, 18.7, 16.8, 18.6, 23.6, 14.9, 28.8, 18.5, 19.5, 29.0, 22.9, 25.4, 24.1, 18.6, 16.0, 16.1, 18.1, 18.7, 18.7, 20.7, 21.2, 25.0, 16.9, 15.2, 19.3, 17.8, 18.5, 26.0, 31.4, 15.6, 19.2, 13.2, 16.9, 21.9, 20.6, 13.2, 16.7, 16.5, 19.3, 19.0, 16.5, 19.9, 20.3, 19.4, 20.2, 25.3, 21.1, 19.8, 16.1, 17.6, 32.3, 27.4, 18.9, 21.7, 16.4, 23.2, 26.6, 20.5, 23.0, 22.6, 11.7, 15.6, 17.5, 21.8, 19.3],
                "р. Тентек - аул Тонкерис": [30.9, 44.9, 48.6, 39.7, 29.0, 33.4, 45.7, 35.6, 37.8, 70.0, 47.8, 36.1, 65.5, 54.3, 69.0, 50.4, 45.0, 34.9, 80.7, 76.2, 70.3, 31.0, 22.2, 32.3, 44.9, 11.9, 16.2, 14.9, 20.0, 94.9, 26.7, 17.9, 33.3, 27.4, 12.5, 16.4, 10.5, 11.0, 15.6, 34.5, 19.0, 15.1, 13.7, 10.3, 14.4, 12.9, 5.8, 21.3, 13.9, 8.67, 27.7, 16.1, 23.5, 38.6, 55.3, 24.7, 15.5, 17.5, 33.9, 22.4, 13.1, 11.5, 53.8, 36.1, 29.2, 62.7, 29.5, 37.1, 15.9, 22.3, 38.6, 17.3, 39.6, 23.8, 39.6, 31.8, 40.5, 64.7, 20.5, 22.4, 13.5, 17.7, 22.5, 23.6, 32.4]            
            }
            df_balhash_local = pd.DataFrame(data_rivers_b)
            # Приток - используем список (обязательно 85 элементов)
            pritok_list_b = [391, 486, 456, 341, 387, 380, 438, 390, 374, 394, 406, 362, 414, 396, 441, 417, 452, 333, 453, 502, 486, 375, 357, 387, 476, 347, 440, 361, 330, 502, 455, 435, 383, 438, 332, 322, 344, 355, 350, 388, 417, 418, 358, 348, 342, 393, 357, 440, 548, 369, 383, 382, 328, 430, 391, 301, 389, 341, 453, 478, 434, 448, 477, 417, 304, 380, 475, 409, 373, 425, 575, 444, 340, 333, 260, 371, 604, 451, 343, 376, 274, 286, 302, 309, 349]


# Настройки легенды в 3 столбца (общие для обоих графиков)
            legend_3col_style = dict(
                orientation="h",
                y=-0.35, # Смещаем ниже, так как подписи лет вертикальные
                x=0.5,
                xanchor="center",
                entrywidth=0.33, # 33% ширины на каждый элемент = 3 столбца
                entrywidthmode="fraction"
            )

            # --- 1. ГРАФИК МЕСТНОГО СТОКА (Балхаш-Алаколь) ---
            fig_b_local = go.Figure()
            excel_colors_b = ['#ffffff', '#ff0000', '#ffff00', '#7030a0', '#996633']
            
            for i, col_name in enumerate(df_balhash_local.columns[1:]):
                fig_b_local.add_trace(go.Scatter(
                    x=df_balhash_local['Год'], 
                    y=df_balhash_local[col_name],
                    mode='lines+markers',
                    name=col_name,
                    line=dict(color='black', width=1),
                    marker=dict(
                        color=excel_colors_b[i % len(excel_colors_b)],
                        size=6,
                        line=dict(color='black', width=1)
                    ),
                    hovertemplate=f"<b>{col_name}</b><br>Год: %{{x}}<br>Сток: %{{y}} м³/с<extra></extra>"
                ))
            
            fig_b_local.update_layout(
                title="<b>МЕСТНЫЙ СТОК: БАЛХАШ-АЛАКОЛЬСКИЙ БАССЕЙН</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                height=500, # Увеличили высоту для комфортного размещения легенды
                template="plotly_white",
                hovermode="x unified",
                legend=legend_3col_style, # Применяем 3 столбца
                margin=dict(l=40, r=20, t=60, b=100), # b=100 чтобы легенда не накладывалась на годы
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
           )

            # --- 2. ГРАФИК ПРИТОКА (С ЛИНЕЙНОЙ ТРЕНДА) ---
            fig_b_pritok = go.Figure()

            fig_b_pritok.add_trace(go.Scatter(
                x=years_b, 
                y=pritok_list_b,
                mode='lines+markers',
                name='Иле (пр. Добын)',
                line=dict(color='black', width=1.2),
                marker=dict(
                    color='#3498db',
                    size=7,
                    line=dict(color='black', width=1)
                ),
                hovertemplate="<b>Приток (Иле)</b><br>Год: %{x}<br>Сток: %{y} м³/с<extra></extra>"
            ))

            
            fig_b_pritok.update_layout(
                title="<b>ТРАНСГРАНИЧНЫЙ ПРИТОК ИЗ КИТАЯ (Р. ИЛЕ)</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                height=500, # Увеличили высоту
                template="plotly_white",
                hovermode="x",
                legend=legend_3col_style, # Применяем 3 столбца
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
           )

            # 3. Отображение
            g_col1, g_col2 = st.columns(2)
            with g_col1:
                st.plotly_chart(fig_b_local, use_container_width=True, key=f"balhash_spec_local_{name}")
            with g_col2:
                st.plotly_chart(fig_b_pritok, use_container_width=True, key=f"balhash_spec_pritok_{name}")
                           
        # --- ЭТОТ БЛОК ВСТАВЛЯТЬ ТОЛЬКО В РАЗДЕЛ БАЛКАШ-АЛАКОЛЬСКОГО ВХБ ---
            # Убедитесь, что этот блок стоит на том же уровне, что и графики для Балхаша
            st.subheader("📊 Анализ суммарных водных ресурсов бассейна (1940–2024 гг.)")

            # border=True работает в новых версиях Streamlit (1.30+)
            with st.container(border=True):
                col_text, col_metric = st.columns([3, 1])
                
                with col_text:
                    st.markdown("""
                    График демонстрирует слабоположительную линейную тенденцию, что на фоне 
                    современной деградации оледенения интерпретируется как фаза **«пика стока»**.
                    """)
                
                with col_metric:
                    # metric автоматически подсвечивает дельту
                    st.metric(label="Тренд стока", value="Рост", delta="+ небольшой")

                st.divider()

                st.write("""
                Наблюдаемый рост стока в Балкаш-Алакольском бассейне связан с интенсивным таянием высокогорных ледников. 
                Однако этот эффект является временным: по мере сокращения площади оледенения, приточность начнет неизбежно снижаться.
                """)

                st.info("""
                **Ключевой фактор:** Несмотря на визуальный тренд к росту, высокая межгодовая изменчивость и цикличность притока р. Или указывают на то, что текущие показатели находятся в пределах верхней границы многолетней нормы, за которой неизбежно последует фаза дефицита из-за сокращения ледникового питания.
                """, icon="💧")

                st.warning("""
                **Вывод:** Текущий «пик стока» — это обманчивый индикатор. Необходимо адаптировать систему к снижению водности.
                """, icon="⚠️")
                
        
        # --- СПЕЦИАЛЬНЫЙ БЛОК ДЛЯ ЕРТИССКОГО ВХБ ---
        if "Ертисский" in name:
            st.markdown("---")
            st.markdown("### 📊 Детальный анализ стока по основным водным артериям")

            desc_col1, desc_col2 = st.columns(2)
            with desc_col1:
                st.info("""**Местный сток:** Для оценки водных ресурсов, формирующихся в Ертисском ВХБ выбраны постоянно действующие 5 крупных рек бассейна с наибольшей водностью таких как: Калжыр, Куршим, Буктырма, Ульби и Оба, определяющих в основном поверхностные водные ресурсы, которые в сумме составляют около 70 % всех местных водных ресурсов..""")   
            with desc_col2:
                st.info("""**Приток:** Приток, поступающий в пределы Ертисского водохозяйственного бассейна из КНР по реке Кара Ертис фиксируется в створе у с. Боран*..""")

            # 1. Подготовка данных (Используем суффикс _ert для изоляции)
            years_ert = list(range(1940, 2025))
            data_rivers_ert = {
                "Год": years_ert,
                "р. Калжыр": [22.9, 36.0, 28.5, 21.5, 20.7, 11.6, 42.2, 29.8, 18.5, 21.1, 17.6, 8.1, 25.4, 17.7, 25.6, 19.5, 22.0, 23.0, 43.2, 28.1, 27.3, 23.6, 17.5, 10.0, 14.6, 10.9, 42.2, 13.7, 17.7, 38.7, 29.1, 32.9, 25.5, 22.7, 8.4, 13.2, 15.1, 17.7, 9.2, 20.2, 14.2, 15.8, 9.7, 20.6, 25.1, 29.0, 17.0, 22.6, 39.7, 19.2, 23.9, 18.6, 28.1, 37.2, 30.0, 24.4, 19.7, 22.6, 28.9, 24.5, 16.8, 37.9, 23.8, 16.0, 25.1, 24.3, 25.5, 26.3, 15.8, 27.9, 39.7, 15.7, 14.1, 21.7, 10.9, 12.9, 13.5, 15.5, 31.3, 25.8, 20.3, 19.2, 24.3, 11.6, 17.2],
                "р. Куршим": [52.7, 87.6, 79.3, 66.2, 53.2, 34.1, 90.3, 98.9, 55.0, 60.7, 55.2, 26.4, 77.4, 49.6, 67.8, 49.3, 61.7, 72.4, 95.6, 57.6, 63.1, 67.5, 56.2, 38.5, 49.3, 42.2, 103.0, 40.6, 54.2, 94.6, 65.2, 77.8, 51.4, 69.5, 30.6, 47.1, 39.8, 50.8, 39.0, 70.3, 48.8, 44.6, 32.2, 53.8, 66.6, 63.5, 45.6, 57.4, 77.3, 45.7, 57.6, 44.6, 74.0, 82.2, 67.3, 56.1, 55.7, 60.1, 72.7, 64.0, 49.8, 93.3, 63.6, 40.0, 68.5, 64.5, 66.5, 68.0, 45.3, 71.6, 97.1, 45.2, 41.5, 137.0, 76.6, 92.3, 109.0, 86.0, 67.1, 59.1, 69.3, 69.6, 68.8, 56.5, 83.3],
                "р. Буктырма": [241, 290, 239, 208, 215, 170, 376, 347, 235, 217, 257, 122, 259, 166, 227, 152, 205, 195, 299, 202, 271, 229, 156, 146, 178, 170, 272, 214, 152, 307, 231, 240, 212, 235, 117, 172, 170, 193, 158, 242, 167, 147, 134, 212, 235, 236, 212, 203, 234, 184, 223, 153, 240, 254, 230, 228, 199, 189, 196, 210, 206, 292, 251, 159, 206, 199, 207, 231, 155, 305, 293, 198, 182, 404, 297, 316, 321, 217, 218, 242, 208, 195, 189, 238, 276],
                "р. Ульби": [84, 125, 97, 91, 87, 67, 160, 134, 98, 119, 89, 49, 104, 63, 135, 79, 101, 115, 160, 102, 131, 101, 72, 63, 84, 78, 149, 76, 82, 130, 107, 124, 108, 120, 56, 104, 104, 94, 79, 154, 76, 74, 67, 90, 74, 100, 74, 96, 100, 91, 124, 73, 119, 114, 106, 92, 77, 78, 86, 67, 69, 125, 118, 55, 93, 79, 88, 99, 69, 106, 109, 82, 55, 147, 94, 101, 119, 85, 76, 73, 66, 64, 67, 88, 88],
                "р. Оба": [148, 209, 168, 158, 153, 124, 260, 222, 169, 200, 157, 98, 178, 118, 239, 122, 150, 184, 255, 169, 236, 207, 148, 128, 148, 147, 236, 113, 136, 212, 196, 219, 178, 246, 125, 196, 196, 199, 164, 250, 137, 123, 131, 154, 146, 194, 148, 212, 201, 199, 251, 142, 193, 208, 191, 182, 148, 140, 104, 103, 109, 187, 211, 117, 135, 133, 151, 175, 115, 174, 154, 114, 101, 252, 200, 197, 228, 180, 180, 149, 171, 123, 124, 154, 209]
            } 
            
            # 2. Создаем DataFrame Ертисского бассейна (ИСПРАВЛЕНО)
            df_local_ert = pd.DataFrame(data_rivers_ert)
            
            # Суммарный приток
            pritok_vals_ert = [327, 411, 425, 307, 267, 218, 458, 372, 239, 274, 283, 193, 388, 235, 322, 298, 347, 313, 466, 364, 354, 385, 267, 218, 262, 211, 446, 198, 298, 478, 374, 385, 305, 352, 143, 245, 214, 278, 166, 274, 224, 229, 134, 229, 373, 316, 206, 328, 420, 201, 283, 219, 293, 461, 383, 290, 234, 265, 293, 273, 238, 383, 309, 204, 272, 305, 268, 224, 175, 180, 353, 177, 145, 366, 236, 254, 346, 349, 327, 251, 242, 208, 182, 254, 369]


            # Общие настройки легенды в 3 столбца
            legend_3col_style = dict(
                orientation="h",
                y=-0.35, 
                x=0.5,
                xanchor="center",
                entrywidth=0.33, 
                entrywidthmode="fraction"
            )

            # --- 1. ГРАФИК МЕСТНОГО СТОКА (Ертисский ВХБ) ---
            fig_ert_local = go.Figure()
            # Палитра для маркеров (Excel-style)
            excel_colors_ert = ['#ffffff', '#ff0000', '#ffff00', '#7030a0', '#996633']
            
            for i, col_name in enumerate(df_local_ert.columns[1:]):
                fig_ert_local.add_trace(go.Scatter(
                    x=df_local_ert['Год'], 
                    y=df_local_ert[col_name],
                    mode='lines+markers', # Линии + точки
                    name=col_name,
                    line=dict(
                        color='black',    # Тонкая черная линия
                        width=1
                    ),
                    marker=dict(
                        color=excel_colors_ert[i % len(excel_colors_ert)], # Цветная заливка
                        size=6,
                        line=dict(color='black', width=1) # Ободок
                    ),
                    hovertemplate=f"<b>{col_name}</b><br>Год: %{{x}}<br>Сток: %{{y}} м³/с<extra></extra>"
                ))
            
            fig_ert_local.update_layout(
                title="<b>МЕСТНЫЙ СТОК ОСНОВНЫХ РЕК (ЕРТИССКИЙ ВХБ)</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                height=500,
                template="plotly_white",
                hovermode="x unified",
                legend=legend_3col_style, # 3 столбца снизу
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
          )

            # --- 2. ГРАФИК ПРИТОКА (С ЛИНЕЙНОЙ ТРЕНДА) ---
            fig_ert_pritok = go.Figure()

            # Основной график притока
            fig_ert_pritok.add_trace(go.Scatter(
                x=years_ert, 
                y=pritok_vals_ert,
                mode='lines+markers',
                name='Кара Ертис (с. Боран)',
                line=dict(color='black', width=1.2),
                marker=dict(
                    color='#3498db', # Голубой маркер
                    size=7,
                    line=dict(color='black', width=1)
                ),
                hovertemplate="<b>Приток (с. Боран)</b><br>Год: %{x}<br>Сток: %{y} м³/с<extra></extra>"
            ))

            # Расчет линии тренда
            
            fig_ert_pritok.update_layout(
                title="<b>ТРАНСГРАНИЧНЫЙ ПРИТОК ИЗ КНР (ЕРТИССКИЙ ВХБ)</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                height=500,
                template="plotly_white",
                hovermode="x",
                legend=legend_3col_style, # 3 столбца снизу
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
          )

            # Отображение
            g_col1, g_col2 = st.columns(2)
            with g_col1:
                st.plotly_chart(fig_ert_local, use_container_width=True, key=f"ertis_local_graph_{name}")
            with g_col2:
                st.plotly_chart(fig_ert_pritok, use_container_width=True, key=f"ertis_pritok_graph_{name}")


            # Убедитесь, что этот блок стоит на том же уровне, что и графики 
            st.subheader("📊 Анализ суммарных водных ресурсов бассейна (1940–2024 гг.)")

            # border=True работает в новых версиях Streamlit (1.30+)
            with st.container(border=True):
                col_text, col_metric = st.columns([3, 1])
                
                with col_text:
                    st.markdown("""
                    За рассматриваемый период с 1940-2024 гг. прослеживается тенденция в пределах нормы объема стока.
                    """)
                
                with col_metric:
                    # metric автоматически подсвечивает дельту
                    st.metric(label="Тренд стока", value="Рост", delta="+ небольшой")

                st.divider()

                st.write("""
                Тенденция сохранения объёма стока в пределах нормы объясняется тем, что за 1940–2024 гг. изменения осадков и температуры в бассейне Ертис носили непостоянный характер, поэтому увеличение испарения в тёплые годы компенсировалось ростом снегозапасов и увлажнения в холодные периоды.
                """)

                st.info("""
                **Ключевой фактор:** В результате естественная климатическая изменчивость сглаживала отклонения, не формируя устойчивого тренда изменения стока.
                """, icon="💧")

                st.warning("""
                **Вывод:** Текущее состояние — это временное влияние таяния ледников.
                """, icon="⚠️")
                

                
        # --- СПЕЦИАЛЬНЫЙ БЛОК ЖАЙЫК-КАСПИЙСКОГО ВХБ ---
        if "Жайык-Каспийский" in name:
            st.markdown("---")
            st.markdown("### 📊 Детальный анализ стока по основным водным артериям")

            desc_col1, desc_col2 = st.columns(2)
            with desc_col1:
                st.info("""**Местный сток:** В качестве основы для оценки ежегодных водных ресурсов речного стока использованы основные реки такие как: Илек – г. Актобе, р. Большая Кобда – с. Кобда, р. Орь – с. Бугетсай, р. Уил - с. Уил и р. Эмба – с. Акмечеть за период 1940-2024 гг., которые в сумме составляют около 47 % всех местных ресурсов. .""")   
            with desc_col2:
                st.info("""**Приток:** Ресурсы речного стока, поступающие из России в пределы Жайык-Каспийского ВХБ оцениваются, как сумма стока рек: 
р. Жайык – пос. Январцево, р. Шаган – с. Чувашинское, 
р. Быковка – с. Чеботарево.""")

            # 1. Подготовка данных
            years_zhk = list(range(1940, 2025))
            
            # Данные местного стока
            data_local_zhk = {
                "Год": years_zhk,
                "р.Орь - с. Бугетсай": [1.84, 13.6, 21.5, 5.65, 0.55, 2.85, 16.4, 4.05, 15.1, 9.85, 1.75, 1.65, 10.7, 2.85, 4.17, 2.07, 3.77, 15.1, 6.88, 6.42, 6.53, 2.23, 4.09, 1.33, 6.31, 2.60, 8.65, 0.12, 1.53, 1.63, 8.55, 11.10, 9.18, 4.26, 2.73, 0.80, 3.12, 3.06, 4.53, 4.90, 16.3, 5.17, 0.75, 7.31, 0.48, 9.11, 3.88, 9.51, 3.06, 2.66, 5.83, 5.83, 1.34, 15.2, 4.50, 1.80, 2.75, 11.3, 4.49, 1.66, 4.93, 2.85, 4.92, 0.56, 4.25, 6.97, 0.61, 8.92, 0.75, 0.30, 6.24, 4.32, 4.21, 0.18, 6.76, 7.59, 9.25, 12.4, 2.51, 0.14, 0.36, 0.38, 7.13, 20.1, 30.4],
                "р. Илек - г. Актобе": [7.97, 37.3, 57.0, 17.5, 4.74, 10.5, 44.4, 13.5, 41.2, 28.0, 7.74, 7.51, 30.2, 10.5, 13.8, 8.56, 12.8, 41.0, 18.0, 16.5, 19.7, 9.04, 11.6, 14.8, 20.7, 7.84, 27.8, 1.57, 11.2, 9.90, 26.2, 28.8, 20.7, 13.3, 13.0, 4.90, 9.89, 7.53, 14.7, 14.3, 25.8, 22.4, 7.48, 21.9, 4.46, 22.7, 8.46, 13.3, 15.5, 14.0, 28.9, 18.0, 9.4, 40.2, 28.8, 7.01, 9.13, 18.7, 14.6, 7.52, 15.7, 10.5, 13.7, 7.59, 14.0, 20.8, 6.38, 10.8, 7.07, 6.85, 6.69, 8.40, 8.71, 7.23, 12.9, 6.60, 19.2, 22.6, 8.87, 3.47, 2.97, 5.90, 8.53, 20.7, 59.3],
                "р. Б.Кобда- с. Кобда": [2.36, 14.7, 23.0, 6.36, 1.00, 3.42, 17.7, 4.68, 16.3, 10.8, 2.26, 2.16, 11.7, 3.42, 4.81, 2.61, 4.39, 16.2, 6.57, 5.94, 7.28, 2.88, 2.70, 6.97, 4.75, 3.01, 10.8, 1.08, 1.88, 4.35, 11.7, 11.9, 8.21, 1.90, 4.89, 1.60, 2.82, 2.10, 3.49, 5.51, 6.41, 9.71, 3.21, 8.75, 1.46, 13.6, 2.63, 3.32, 3.5, 2.29, 4.69, 5.69, 1.60, 14.6, 9.27, 1.12, 6.04, 10.1, 5.14, 2.17, 5.97, 3.02, 5.70, 2.73, 7.46, 7.56, 1.96, 6.83, 2.39, 1.62, 2.18, 3.59, 1.87, 1.44, 5.94, 4.94, 7.89, 6.42, 5.30, 1.19, 1.54, 2.24, 13.8, 19.5, 26],
                "р. Уил - пос. Уил": [8.65, 18.1, 17.9, 7.18, 3.63, 5.68, 14.5, 7.25, 28.5, 6.27, 4.45, 1.99, 13.7, 2.98, 7.93, 2.90, 10.0, 13.4, 6.66, 13.3, 7.10, 5.29, 5.10, 12.1, 5.45, 2.48, 12.7, 0.88, 3.70, 5.64, 25.6, 10.2, 6.4, 11.0, 4.61, 5.14, 5.49, 5.23, 7.20, 17.5, 9.36, 8.44, 2.37, 8.30, 1.08, 9.20, 0.99, 9.42, 6.05, 4.09, 6.39, 10.4, 2.78, 26.9, 8.96, 5.73, 4.31, 7.95, 14.9, 6.46, 12.6, 2.84, 11.0, 2.78, 11.5, 18.8, 2.24, 13.4, 2.44, 1.29, 2.01, 5.20, 2.52, 0.61, 4.13, 6.43, 10.8, 6.15, 4.30, 0.59, 0.44, 0.19, 16.9, 34.6, 74.7],
                "р. Эмба - с.Акмечеть": [16.9, 21.9, 36.4, 13.8, 6.2, 10.6, 29.2, 13.9, 42.5, 11.8, 7.9, 3.9, 29.9, 6.0, 26.6, 6.0, 10.9, 27.4, 15.0, 21.4, 12.6, 5.7, 16.2, 7.4, 13.3, 9.9, 20.3, 0.2, 9.9, 9.2, 18.6, 20.1, 12.0, 21.9, 8.3, 9.4, 10.2, 11.1, 10.2, 9.9, 18.4, 16.4, 3.5, 16.1, 0.8, 18.0, 6.7, 12.5, 32.1, 9.4, 9.2, 15.6, 3.7, 19.4, 12.6, 4.1, 12.2, 14.3, 11.4, 7.8, 13.3, 10.1, 13.0, 9.8, 15.0, 15.1, 0.8, 9.7, 0.7, 0.6, 17.6, 9.7, 8.9, 0.1, 4.5, 10.6, 14.9, 13.1, 1.5, 0.3, 1.6, 0.6, 11.2, 19.0, 156.2]            
            }
            
            # Данные притока
            data_pritok_zhk = {
                "Год": years_zhk,
                "р. Жайык - пос. Январцево": [142, 685, 624, 229, 123, 233, 791, 611, 644, 346, 179, 137, 320, 238, 186, 113, 223, 793, 309, 336, 322, 188, 253, 363, 408, 219, 350, 96, 187, 218, 670, 552, 276, 182, 289, 129, 195, 146, 255, 257, 282, 381, 241, 344, 134, 333, 291, 414, 347, 270, 556, 427, 229, 576, 510, 255, 235, 265, 368, 238, 450, 382, 461, 333, 356, 386, 178, 303, 256, 130, 191, 219, 194, 254, 265, 155, 279, 311, 174, 111, 130, 121, 169, 248, 542],
                "р. Шаган-с.Чувашинское": [8.1, 24.9, 23.0, 7.1, 2.8, 7.3, 29.8, 22.5, 14.6, 11.8, 6.7, 8.5, 10.4, 7.0, 3.7, 5.0, 9.9, 27.4, 10.4, 10.7, 6.4, 5.7, 7.6, 15.0, 11.3, 5.0, 6.5, 1.6, 8.9, 1.6, 11.8, 7.2, 1.9, 2.4, 4.8, 2.6, 5.9, 2.7, 6.1, 8.0, 8.0, 8.8, 12.1, 5.9, 1.6, 4.5, 10.8, 9.1, 7.3, 4.8, 7.4, 10.0, 3.6, 20.1, 22.6, 1.7, 3.2, 7.1, 10.9, 6.6, 19.9, 20.8, 18.3, 13.5, 4.7, 5.9, 3.8, 9.2, 3.9, 2.5, 5.2, 9.6, 6.1, 8.1, 5.0, 1.3, 4.4, 7.5, 4.3, 2.3, 1.0, 2.1, 2.8, 8.9, 14.0],
                "р. Быковка - с. Чеботарево": [0.37, 1.05, 0.97, 0.33, 0.16, 0.34, 1.24, 0.95, 0.64, 0.52, 0.32, 0.39, 0.47, 0.33, 0.20, 0.25, 0.45, 1.15, 0.47, 0.48, 0.31, 0.28, 0.35, 0.65, 0.50, 0.25, 0.31, 0.11, 0.41, 0.12, 0.52, 0.34, 0.13, 0.15, 0.24, 0.15, 0.29, 0.16, 0.29, 0.37, 0.37, 0.40, 0.53, 0.29, 0.11, 0.23, 0.48, 0.42, 0.34, 0.24, 0.35, 0.45, 0.20, 0.85, 0.95, 0.12, 0.18, 0.33, 0.48, 0.32, 0.84, 0.88, 0.78, 0.59, 0.24, 0.28, 0.20, 0.42, 0.46, 0.16, 0.26, 0.51, 0.15, 0.26, 0.12, 0.10, 0.22, 0.35, 0.30, 0.16, 0, 0.07, 0.11, 0.21, 0.24]
            }

            df_local_zhk = pd.DataFrame(data_local_zhk)
            df_pritok_zhk = pd.DataFrame(data_pritok_zhk)

            colors_zhk = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

            # Единый стиль легенды в 3 столбца
            legend_3col_style = dict(
                orientation="h",
                y=-0.35, 
                x=0.5,
                xanchor="center",
                entrywidth=0.33, 
                entrywidthmode="fraction"
            )

            # Цвета маркеров (Excel-style)
            excel_colors_zhk = ['#ffffff', '#ff0000', '#ffff00', '#7030a0', '#996633']

            # --- ГРАФИК 1: МЕСТНЫЙ СТОК (Жайык-Каспийский ВХБ) ---
            fig_zhk_local = go.Figure()
            for i, col_name in enumerate(df_local_zhk.columns[1:]):
                fig_zhk_local.add_trace(go.Scatter(
                    x=df_local_zhk['Год'], 
                    y=df_local_zhk[col_name],
                    mode='lines+markers',
                    name=col_name,
                    line=dict(color='black', width=1),
                    marker=dict(
                        color=excel_colors_zhk[i % len(excel_colors_zhk)],
                        size=6,
                        line=dict(color='black', width=1)
                    ),
                    hovertemplate=f"<b>{col_name}</b><br>Год: %{{x}}<br>Сток: %{{y}} м³/с<extra></extra>"
                ))

            fig_zhk_local.update_layout(
                title="<b>МЕСТНЫЙ СТОК (ЖАЙЫК-КАСПИЙСКИЙ ВХБ)</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                template="plotly_white",
                height=500,
                hovermode="x unified",
                legend=legend_3col_style,
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
          )

            # --- ГРАФИК 2: ТРАНСГРАНИЧНЫЙ ПРИТОК ---
            fig_zhk_pritok = go.Figure()
            for i, col_name in enumerate(df_pritok_zhk.columns[1:]):
                # Рисуем основные линии притока
                fig_zhk_pritok.add_trace(go.Scatter(
                    x=df_pritok_zhk['Год'], 
                    y=df_pritok_zhk[col_name],
                    mode='lines+markers',
                    name=col_name,
                    line=dict(color='black', width=1),
                    marker=dict(
                        color=excel_colors_zhk[(i+2) % len(excel_colors_zhk)], # Смещение цвета для отличия от первого графика
                        size=6,
                        line=dict(color='black', width=1)
                    ),
                    hovertemplate=f"<b>{col_name}</b><br>Год: %{{x}}<br>Сток: %{{y}} м³/с<extra></extra>"
                ))

            fig_zhk_pritok.update_layout(
                title="<b>ТРАНСГРАНИЧНЫЙ ПРИТОК (РФ -> РК)</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                template="plotly_white",
                height=500,
                hovermode="x unified",
                legend=legend_3col_style,
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
          )

            # --- ВЫВОД В STREAMLIT ---
            col_a, col_b = st.columns(2)
            with col_a:
                st.plotly_chart(fig_zhk_local, use_container_width=True, key=f"zhk_local_graph_{name}")
            with col_b:
                st.plotly_chart(fig_zhk_pritok, use_container_width=True, key=f"zhk_pritok_graph_{name}")
            st.divider()   

            # Убедитесь, что этот блок стоит на том же уровне, что и графики 
            st.subheader("📊 Анализ суммарных водных ресурсов бассейна (1940–2024 гг.)")

            # border=True работает в новых версиях Streamlit (1.30+)
            with st.container(border=True):
                col_text, col_metric = st.columns([3, 1])
                
                with col_text:
                    st.markdown("""
                    Суммарные ресурсы Жайык–Каспийского ВХБ за период 1940–2024 гг. в целом наблюдается тенденция к снижению водных ресурсов при сохранении высокой межгодовой изменчивости, причём в последние десятилетия значения часто формируются ниже многолетней нормы.
                    """)
                
                with col_metric:
                    # metric автоматически подсвечивает дельту
                    st.metric(label="Тренд стока", value="Снижение", delta="- постепенное")

                st.divider()

                st.write("""
                Сокращение обусловлено ростом температуры и испаряемости, а также регулирующим воздействием хозяйственной деятельности в верховьях, при этом решающую роль в формировании общего водного баланса играет приток, определяющий уровень водообеспеченности нижнего течения и прикаспийской зоны.
                """)

                st.info("""
                **Ключевой фактор:** В результате естественная климатическая изменчивость сглаживала отклонения, не формируя устойчивого тренда изменения стока.
                """, icon="💧")

                st.warning("""
                **Вывод:** Текущее состояние — это временное влияние таяния ледников.
                """, icon="⚠️")
                
                
                

            
         # --- СПЕЦИАЛЬНЫЙ БЛОК ЕСИЛЬСКОГО ВХБ ---
        if "Есильский" in name:
            st.markdown("---")
            st.markdown("### 📊 Детальный анализ стока по основным водным артериям")

            desc_col1, desc_col2 = st.columns(2)
            with desc_col1:
                st.info("""**Местный сток:** Для оценки водных ресурсов, формирующихся в Есильском ВХБ выбраны постоянно действующие 3 реки бассейна с наибольшей водностью, определяющих в основном поверхностные местные водные ресурсы: Есиль, Калкутан, Жабай, которые в сумме составляют около 70 % всех местных водных ресурсов, кроме того, к сумме речного стока прибавлена величина 1 м3/с, представляющая собой забор воды на заполнение малых водохранилищ в верховьях реки Есиль, расположенных в Карагандинской области;.""")   
            with desc_col2:
                st.success("""**Особенность:** Есильский бассейн является внутренним, основной приток формируется за счет талых вод и местных рек.""")

            # 1. Подготовка данных
            years_es = list(range(1940, 2025))
            data_local_es = {
                "Год": years_es,
                "р. Есиль - г. Астана": [1.10, 11.50, 14.60, 10.50, 2.05, 1.64, 7.82, 7.00, 22.10, 16.20, 3.06, 4.56, 2.35, 2.60, 9.32, 5.40, 1.57, 5.64, 6.40, 9.43, 10.70, 8.11, 7.93, 1.26, 9.60, 2.50, 10.80, 0.10, 1.58, 0.46, 3.10, 10.10, 12.60, 11.00, 1.98, 0.77, 2.24, 1.08, 0.68, 6.53, 0.89, 0.71, 0.44, 6.29, 4.76, 9.43, 8.16, 6.85, 6.20, 2.01, 10.40, 6.33, 4.37, 13.00, 1.47, 0.21, 5.97, 4.37, 0.63, 0.20, 0.21, 1.05, 5.63, 1.87, 2.28, 4.44, 0.75, 0.56, 0.68, 0.57, 1.86, 0.46, 0.60, 0.66, 3.29, 5.45, 2.62, 7.78, 6.71, 9.57, 1.42, 6.74, 0.81, 0.26, 9.66],
                "р. Жабай - г. Атбасар": [7.25, 13.40, 11.84, 6.50, 2.81, 1.95, 11.72, 17.80, 16.90, 5.64, 3.53, 3.28, 1.58, 7.55, 11.50, 7.40, 3.18, 3.32, 5.20, 8.24, 13.00, 12.10, 3.48, 4.18, 18.30, 6.95, 7.81, 1.85, 1.97, 3.43, 8.56, 15.00, 9.42, 6.41, 5.99, 3.28, 5.69, 3.12, 15.40, 8.33, 10.30, 9.10, 8.14, 27.40, 11.10, 13.70, 11.60, 11.40, 7.49, 6.42, 19.10, 11.50, 4.55, 16.60, 15.00, 14.00, 5.65, 6.72, 2.87, 1.84, 3.39, 8.11, 20.10, 5.22, 3.69, 11.60, 3.73, 17.50, 3.79, 3.29, 5.20, 5.34, 5.75, 8.48, 45.00, 5.20, 18.40, 70.50, 7.13, 31.40, 14.40, 10.90, 4.86, 20.70, 46.60],
                "р. Калкутан-с. Калкутан": [1.77, 17.11, 14.68, 6.37, 1.47, 1.55, 14.49, 12.84, 22.15, 15.85, 2.51, 1.72, 1.19, 2.34, 17.21, 6.55, 2.10, 3.16, 4.09, 6.56, 6.21, 8.87, 3.69, 4.02, 12.65, 2.35, 4.58, 0.33, 0.46, 1.62, 6.92, 14.43, 21.40, 4.42, 3.93, 0.87, 2.43, 0.10, 14.10, 12.10, 10.60, 13.70, 4.18, 17.70, 7.25, 25.00, 9.84, 17.70, 12.70, 3.04, 21.30, 6.32, 1.20, 24.30, 13.50, 13.50, 5.11, 15.30, 2.09, 0.61, 0.71, 5.13, 33.30, 3.13, 3.56, 14.80, 0.43, 15.80, 1.28, 1.31, 3.95, 3.35, 1.91, 2.95, 6.77, 7.70, 6.06, 6.86, 2.20, 4.48, 5.07, 1.23, 1.24, 8.19, 12.00],
            }
            
            df_es = pd.DataFrame(data_local_es)
            
            # Считаем суммарный сток + 1 м3/с (как указано в вашем описании)
            df_es['Суммарный местный сток (+1)'] = df_es.iloc[:, 1:].sum(axis=1) + 1.0

            colors_es = ['#3498db', '#e67e22', '#2ecc71', '#9b59b6']

            # Единый стиль легенды в 3 столбца
            legend_3col_style = dict(
                orientation="h",
                y=-0.35, 
                x=0.5,
                xanchor="center",
                entrywidth=0.33, 
                entrywidthmode="fraction"
            )

            # Цвета маркеров (Excel-style)
            excel_colors_es = ['#ffffff', '#ff0000', '#ffff00', '#7030a0', '#996633']

            # --- ГРАФИК 1: ПОГРАФИЧНО РЕКИ (Есильский бассейн) ---
            fig_es_rivers = go.Figure()
            river_cols = ["р. Есиль - г. Астана", "р. Жабай - г. Атбасар", "р. Калкутан-с. Калкутан"]
            
            for i, col in enumerate(river_cols):
                fig_es_rivers.add_trace(go.Scatter(
                    x=df_es['Год'], y=df_es[col],
                    mode='lines+markers', # Линии + точки
                    name=col,
                    line=dict(color='black', width=1), # Тонкая черная линия
                    marker=dict(
                        color=excel_colors_es[i % len(excel_colors_es)],
                        size=6,
                        line=dict(color='black', width=1)
                    ),
                    hovertemplate=f"<b>{col}</b><br>Год: %{{x}}<br>Сток: %{{y}} м³/с<extra></extra>"
                ))
            
            fig_es_rivers.update_layout(
                title="<b>СТОК ОСНОВНЫХ РЕК ЕСИЛЬСКОГО БАССЕЙНА</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                template="plotly_white", 
                height=500, 
                hovermode="x unified",
                legend=legend_3col_style,
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
          )

            # --- ГРАФИК 2: ОБЩИЙ РЕСУРС (С ТРЕНДОМ) ---
            fig_es_total = go.Figure()
            
            # Основная линия суммарного стока
            fig_es_total.add_trace(go.Scatter(
                x=df_es['Год'], y=df_es['Суммарный местный сток (+1)'],
                mode='lines+markers', 
                name='Суммарный сток',
                line=dict(color='black', width=1.5),
                marker=dict(
                    color='#2ecc71', # Зеленый маркер для ресурсов
                    size=7,
                    line=dict(color='black', width=1)
                ),
                hovertemplate="Год: %{x}<br>Сумма: %{y:.2f} м³/с<extra></extra>"
            ))

            
            fig_es_total.update_layout(
                title="<b>СУММАРНЫЕ ПОВЕРХНОСТНЫЕ ВОДНЫЕ РЕСУРСЫ</b>",
                xaxis_title="ГОД", 
                yaxis_title="Q, м³/с",
                template="plotly_white", 
                height=500,
                legend=legend_3col_style,
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
          )

            # --- ВЫВОД В STREAMLIT ---
            col_a, col_b = st.columns(2)
            with col_a:
                st.plotly_chart(fig_es_rivers, use_container_width=True, key=f"esil_rivers_{name}")
            with col_b:
                st.plotly_chart(fig_es_total, use_container_width=True, key=f"esil_total_{name}")
            st.divider()                   

        # --- ЭТОТ БЛОК ВСТАВЛЯТЬ ТОЛЬКО В РАЗДЕЛ БАЛКАШ-АЛАКОЛЬСКОГО ВХБ ---
            # Убедитесь, что этот блок стоит на том же уровне, что и графики для Балхаша
            st.subheader("📊 Анализ суммарных водных ресурсов бассейна (1940–2024 гг.)")

            # border=True работает в новых версиях Streamlit (1.30+)
            with st.container(border=True):
                col_text, col_metric = st.columns([3, 1])
                
                with col_text:
                    st.markdown("""
                    За период 1940–2024 гг. прослеживается тенденция к увеличению объёма стока.
                    """)
                
                with col_metric:
                    # metric автоматически подсвечивает дельту
                    st.metric(label="Тренд стока", value="Рост", delta="+ небольшой")

                st.divider()

                st.write("""
                Рост водности обусловлен увеличением количества осадков в холодный период и усилением снегового питания на фоне повышения температуры воздуха, что подтверждается исследованиями по северу Казахстана.
                """)

                st.info("""
                **Ключевой фактор:** Несмотря на визуальный тренд к росту, высокая межгодовая изменчивость и цикличность притока р. Или указывают на то, что текущие показатели находятся в пределах верхней границы многолетней нормы, за которой неизбежно последует фаза дефицита из-за сокращения ледникового питания.
                """, icon="💧")

                st.warning("""
                **Вывод:** Текущий «пик стока» — это обманчивый индикатор. Необходимо адаптировать систему к снижению водности.
                """, icon="⚠️")
                

                
# --- СПЕЦИАЛЬНЫЙ БЛОК НУРА-САРЫСУЙСКОГО ВХБ ---
        if "Нура-Сарысуйский" in name:
            st.markdown("---")
            st.markdown("### 📊 Детальный анализ стока по основным водным артериям")

            desc_col1, desc_col2 = st.columns(2)
            with desc_col1:
                st.info("""**Местный сток:** Для оценки выбраны 4 основные реки (Нура, Сарысу, Каракенгир, Жиланды), которые составляют около 77 % всех местных водных ресурсов бассейна.""")   
            with desc_col2:
                st.success("""**Особенность:** Бассейн является бессточным (внутренним). Питание рек преимущественно снеговое.""")

            # 1. Подготовка данных
            years_n = list(range(1940, 2025))
            data_local_n = {
                "Год": years_n,
                "р. Нура - ж.-д. ст. Балыкты": [1.95, 11.80, 4.14, 8.24, 5.42, 8.93, 2.21, 9.69, 23.00, 11.70, 7.02, 1.21, 5.36, 3.30, 16.00, 3.98, 1.11, 1.44, 8.12, 8.51, 14.60, 6.75, 8.04, 0.85, 3.68, 2.42, 9.81, 0.42, 1.54, 4.72, 4.34, 10.90, 6.61, 7.64, 6.62, 9.05, 9.90, 17.40, 7.35, 10.40, 7.12, 6.70, 7.67, 9.71, 7.31, 9.92, 13.40, 7.87, 15.10, 8.83, 16.10, 14.50, 3.23, 19.90, 4.58, 12.90, 4.28, 6.57, 5.79, 3.53, 3.22, 9.69, 14.20, 2.92, 14.80, 6.86, 1.58, 8.14, 3.88, 1.95, 8.63, 3.03, 4.24, 11.90, 13.30, 42.20, 11.30, 36.20, 21.10, 22.70, 8.61, 7.44, 12.40, 5.02, 21.00],
                "р. Нура - с. Р. Кошкарбаева": [3.32, 34.50, 19.80, 21.30, 3.30, 17.40, 13.20, 15.60, 51.60, 54.60, 8.03, 4.89, 8.76, 12.10, 36.70, 12.40, 5.21, 8.26, 25.50, 33.00, 49.90, 21.10, 22.50, 4.10, 16.70, 5.69, 9.00, 3.52, 4.72, 10.40, 16.30, 27.00, 36.90, 21.10, 8.51, 6.97, 16.00, 22.70, 14.00, 31.20, 12.00, 14.40, 13.30, 24.50, 22.90, 25.90, 28.00, 24.50, 41.50, 22.70, 62.40, 46.20, 14.00, 63.60, 15.40, 26.00, 14.40, 23.00, 9.04, 6.47, 5.43, 12.50, 40.20, 10.70, 36.40, 17.47, 4.68, 12.80, 12.60, 6.44, 17.40, 9.40, 6.34, 17.00, 8.72, 28.40, 63.79, 108.46, 32.70, 53.00, 33.20, 32.10, 25.20, 9.26, 71.50],
                "р. Шерубайнура - раз. Карамурын": [2.03, 10.20, 4.41, 8.42, 5.04, 13.40, 3.94, 8.07, 15.70, 17.00, 3.21, 1.63, 2.71, 4.51, 10.50, 3.55, 1.18, 1.56, 11.40, 9.64, 9.89, 7.03, 3.51, 1.50, 4.84, 3.68, 8.41, 0.70, 0.71, 3.58, 4.78, 5.07, 8.03, 6.52, 1.74, 0.40, 2.63, 6.21, 2.21, 4.57, 1.18, 1.29, 4.12, 4.01, 3.14, 4.45, 8.03, 3.92, 7.87, 3.22, 11.00, 8.52, 2.76, 15.60, 2.79, 4.97, 1.01, 6.18, 1.65, 1.01, 2.77, 8.40, 13.70, 2.58, 9.51, 2.44, 0.90, 5.41, 1.47, 0.50, 2.93, 3.41, 1.67, 4.25, 5.67, 18.00, 18.80, 20.90, 5.52, 14.80, 6.68, 2.46, 5.73, 3.01, 11.90],
                "р. Сарысу - раз. № 189": [1.83, 7.02, 3.19, 4.72, 0.54, 7.70, 0.80, 0.41, 4.86, 12.50, 0.80, 0.54, 1.74, 1.02, 17.30, 1.46, 0.71, 0.56, 9.99, 3.05, 5.97, 3.05, 1.79, 0.17, 3.99, 0.35, 2.86, 0.05, 0.06, 1.78, 4.58, 0.69, 5.90, 2.22, 0.62, 0.09, 0.27, 2.49, 0.14, 0.47, 0.30, 0.47, 0.96, 2.67, 1.00, 0.93, 1.45, 1.03, 3.60, 0.62, 1.09, 2.98, 0.19, 1.35, 0.60, 2.82, 0.31, 1.00, 0.53, 0.12, 0.31, 1.38, 11.10, 1.08, 6.30, 0.24, 0.19, 1.33, 0.09, 0.07, 2.65, 0.18, 0.02, 0.60, 1.32, 29.30, 9.25, 15.50, 3.07, 7.52, 2.15, 1.17, 1.11, 2.19, 16.10],
                "р. Каракенгир - устье": [2.64, 9.45, 6.65, 5.71, 0.37, 1.97, 5.10, 0.83, 9.37, 19.40, 1.27, 0.27, 0.99, 1.39, 6.56, 1.33, 1.61, 1.62, 8.28, 5.73, 3.07, 1.28, 2.79, 1.81, 6.17, 2.60, 3.71, 0.75, 0.74, 3.60, 5.91, 7.83, 12.80, 5.02, 0.80, 0.07, 5.17, 4.57, 3.90, 5.10, 2.82, 6.29, 2.87, 6.30, 5.02, 2.08, 6.19, 9.73, 4.01, 3.47, 5.06, 7.85, 6.35, 6.57, 0.93, 4.93, 7.29, 7.35, 2.30, 0.01, 1.34, 0.57, 14.10, 2.49, 6.51, 2.74, 0.24, 4.30, 0.23, 0.89, 7.86, 0.29, 0.18, 2.12, 1.77, 6.82, 6.19, 4.71, 5.14, 1.27, 2.01, 1.30, 1.45, 2.23, 4.72],
            }
            
            df_n = pd.DataFrame(data_local_n)
            
            # Считаем суммарный сток (без +1, если это не требовалось специально)
            df_n['Суммарный сток'] = df_n.iloc[:, 1:].sum(axis=1)

            # Список цветов (минимум 5 для 5 рек)
            colors_n = ['#3498db', '#e67e22', '#2ecc71', '#9b59b6', '#f1c40f']



            # Унифицированный стиль легенды в 3 столбца
            legend_3col_style = dict(
                orientation="h",
                y=-0.35, 
                x=0.5,
                xanchor="center",
                entrywidth=0.33, 
                entrywidthmode="fraction"
            )

            # Цвета маркеров в стиле Excel
            excel_colors_n = ['#ffffff', '#ff0000', '#ffff00', '#7030a0', '#996633']

            # --- ГРАФИК 1: ПОГРАФИЧНО РЕКИ (Нура-Сарысуйский бассейн) ---
            fig_n_rivers = go.Figure()
            river_cols = [c for c in df_n.columns if c not in ["Год", "Суммарный сток"]]
            
            for i, col in enumerate(river_cols):
                fig_n_rivers.add_trace(go.Scatter(
                    x=df_n['Год'], y=df_n[col],
                    mode='lines+markers', # Линии + точки
                    name=col,
                    line=dict(color='black', width=1), # Тонкая черная линия
                    marker=dict(
                        color=excel_colors_n[i % len(excel_colors_n)],
                        size=6,
                        line=dict(color='black', width=1)
                    ),
                    hovertemplate=f"<b>{col}</b><br>Год: %{{x}}<br>Сток: %{{y}} м³/с<extra></extra>"
                ))
            
            fig_n_rivers.update_layout(
                title="<b>ДИНАМИКА СТОКА РЕК НУРА-САРЫСУЙСКОГО БАССЕЙНА</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                template="plotly_white", 
                height=500, 
                hovermode="x unified",
                legend=legend_3col_style,
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
          )

            # --- ГРАФИК 2: ОБЩИЙ РЕСУРС (С ТРЕНДОМ) ---
            fig_n_total = go.Figure()
            
            # Основная линия суммарного стока
            fig_es_total = go.Figure() # Исправлено название переменной для консистентности
            fig_n_total.add_trace(go.Scatter(
                x=df_n['Год'], y=df_n['Суммарный сток'],
                mode='lines+markers', 
                name='Суммарный сток',
                line=dict(color='black', width=1.5),
                marker=dict(
                    color='#3498db', # Синий маркер для суммарного стока
                    size=7,
                    line=dict(color='black', width=1)
                ),
                hovertemplate="Год: %{x}<br>Сумма: %{y:.2f} м³/с<extra></extra>"
            ))

            
            fig_n_total.update_layout(
                title="<b>СУММАРНЫЕ ВОДНЫЕ РЕСУРСЫ (ОСНОВНЫЕ РЕКИ)</b>",
                xaxis_title="ГОД", 
                yaxis_title="Q, м³/с",
                template="plotly_white", 
                height=500,
                legend=legend_3col_style,
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
          )

            # --- ВЫВОД В STREAMLIT ---
            col_a, col_b = st.columns(2)
            with col_a:
                st.plotly_chart(fig_n_rivers, use_container_width=True, key=f"nura_rivers_{name}")
            with col_b:
                st.plotly_chart(fig_n_total, use_container_width=True, key=f"nura_total_{name}")
            st.divider()   

        # --- ЭТОТ БЛОК ВСТАВЛЯТЬ ТОЛЬКО В РАЗДЕЛ БАЛКАШ-АЛАКОЛЬСКОГО ВХБ ---
            # Убедитесь, что этот блок стоит на том же уровне, что и графики для Балхаша
            st.subheader("📊 Анализ суммарных водных ресурсов бассейна (1940–2024 гг.)")

            # border=True работает в новых версиях Streamlit (1.30+)
            with st.container(border=True):
                col_text, col_metric = st.columns([3, 1])
                
                with col_text:
                    st.markdown("""
                   За рассматриваемый период с 1940 по 2024 гг. прослеживается слабая тенденция к росту (или сохранению) среднего объема стока, несмотря на высокую межгодовую изменчивость.
                    """)
                
                with col_metric:
                    # metric автоматически подсвечивает дельту
                    st.metric(label="Тренд стока", value="Рост", delta="+ небольшой")

                st.divider()

                st.write("""
                Тенденция сохранения и незначительного роста тренда объясняется тем, что в данном бассейне наблюдается увеличение количества зимних осадков и изменение интенсивности весеннего снеготаяния, что при сохранении промерзания почвы способствует формированию более высоких паводковых пиков в отдельные годы.
                """)

                st.info("""
                **Ключевой фактор:**В результате, несмотря на рост летних температур, увеличение увлажненности в холодный период и приток паводковых вод нивелируют потери на испарение, удерживая линию тренда от падения.
                """, icon="💧")

                st.warning("""
                **Вывод:** Зимние осадки удерживают сток в норме ($1{,}16$ км³/год), компенсируя испарение, но резкие паводки повышают риски.
                """, icon="⚠️")
                
             
          
# --- СПЕЦИАЛЬНЫЙ БЛОК Шу-Таласского ВХБ ---
        if "Шу-Таласский" in name:
            st.markdown("---")
            st.markdown("### 📊 Детальный анализ стока по основным водным артериям")

            desc_col1, desc_col2 = st.columns(2)
            with desc_col1:
                st.info("""**Местный сток::** Приток, поступающий в пределы Шу-Таласского водохозяйственного бассейна из КР фиксируется в створах 7 рек -  Шу, Талас, Ассы -  Карабалта, Аксу, Саргоу, Токташ.""")   
            with desc_col2:
                st.success("""**приток:** Для оценки водных ресурсов, формирующихся в Шу-Таласском ВХБ выбраны постоянно действующие 2 крупных рек бассейна с наибольшей водностью таких как: р. Курагаты- ж.-д. ст. Аспара и р. Терис –с. Нурлыкент, определяющих в основном поверхностные водные ресурсы, которые в сумме составляют около 23 % всех местных водных ресурсов.""")

            # 1. Подготовка данных
            years_st = list(range(1940, 2025))
            
            # Данные притока из КР (7 рек)
            data_inflow_st = {
                "Год": years_st,
                "р. Шу - с. Кайнар": [49.4, 58.8, 75.1, 57.8, 53.9, 58.0, 62.1, 54.3, 56.9, 63.0, 59.7, 54.0, 67.6, 67.6, 64.9, 63.6, 65.3, 53.0, 78.3, 68.0, 66.0, 58.3, 51.4, 57.0, 63.0, 51.6, 61.6, 63.6, 53.7, 100.0, 55.5, 59.1, 55.3, 37.1, 37.0, 44.7, 34.3, 28.7, 36.8, 44.2, 39.7, 46.6, 40.4, 37.7, 36.6, 46.0, 41.0, 65.7, 63.5, 49.7, 62.4, 46.1, 47.6, 54.3, 66.5, 44.0, 49.7, 40.4, 66.3, 70.6, 53.4, 50.9, 93.6, 95.6, 83.5, 89.9, 69.2, 55.2, 46.9, 60.5, 82.5, 71.9, 50.3, 46.9, 48.3, 49.4, 73.6, 79.6, 55.0, 47.1, 39.0, 33.9, 44.5, 45.7, 50.5],
                "р. Талас - с. Жасоркен": [20.7, 24.6, 36.5, 23.4, 20.0, 27.2, 28.5, 30.6, 27.2, 32.7, 26.0, 26.3, 36.8, 28.2, 33.1, 33.5, 29.1, 19.6, 40.5, 35.5, 34.9, 21.8, 24.2, 26.1, 27.8, 19.3, 33.9, 24.6, 29.6, 32.7, 32.6, 24.9, 24.8, 23.6, 18.2, 14.6, 15.2, 16.9, 17.0, 19.4, 21.3, 20.3, 18.7, 21.6, 19.5, 17.4, 16.6, 24.5, 26.1, 26.4, 21.5, 21.2, 21.1, 20.1, 34.7, 26.2, 19.5, 17.1, 23.7, 24.4, 24.1, 17.7, 33.7, 37.2, 36.6, 32.1, 18.6, 19.0, 12.3, 22.8, 36.1, 26.9, 18.9, 16.7, 12.2, 11.8, 44.7, 38.5, 19.8, 20.5, 18.3, 13.4, 23.7, 13.1, 18.4],
                "р. Асса - ст. Маймак": [7.62, 10.4, 11.9, 9.68, 8.23, 12.4, 11.8, 8.15, 9.72, 14.9, 11.0, 11.0, 16.7, 13.7, 15.4, 14.1, 11.8, 8.78, 19.7, 16.5, 17.8, 10.5, 9.46, 8.97, 11.0, 8.13, 12.5, 10.2, 12.3, 24.9, 11.5, 11.6, 13.8, 12.5, 7.04, 7.77, 7.89, 7.72, 11.3, 15.1, 5.48, 8.15, 6.27, 5.48, 7.38, 9.35, 6.13, 9.43, 9.49, 6.63, 11.7, 8.4, 10.2, 12.2, 16.1, 10.8, 11.7, 7.59, 11.4, 9.35, 6.34, 6.21, 10.2, 10.1, 8.91, 12.7, 7.61, 9.44, 7.96, 7.29, 9.91, 8.23, 8.27, 8.91, 11.6, 10.5, 10.5, 17.9, 9.76, 10.1, 7.02, 9.02, 8.78, 9.78, 11.4],
                "р. Аксу - а. Аксу": [0]*72 + [8.74, 14.2, 12.9, 20.3, 32.0, 29.2, 23.9, 13.5, 13.3, 8.35, 7.13, 8.28, 20.1]
            }
            
            # Данные местного стока (РК)
            data_local_st = {
                "Год": years_st,
                "р. Курагаты": [0.5, 0.68, 1.92, 0.98, 0.53, 0.31, 1.07, 0.53, 1.37, 1.23, 1.31, 1.13, 1.61, 2.37, 3.08, 3.82, 2.27, 1.35, 4.77, 6.86, 6.58, 2.56, 1.79, 3.09, 5.91, 3.38, 5.55, 8.07, 5.09, 15.8, 7.52, 6.13, 4.83, 9.19, 3.17, 2.73, 2.76, 2.83, 3.88, 3.75, 2.75, 2.72, 2.46, 2.63, 2.42, 3.18, 2.01, 4.38, 6.24, 3.31, 4.07, 2.4, 2.39, 5.16, 7.63, 4.05, 2.07, 2.03, 3.87, 4.85, 3.18, 2.63, 10.4, 8.66, 7.2, 5.6, 5.26, 2.87, 2.32, 5.99, 4.87, 7.45, 5.62, 5.47, 6.62, 6.07, 10.8, 11.3, 9.2, 9.06, 9.53, 8.0, 0.84, 0.84, 0.58],
                "р. Терис": [2.52, 3.40, 4.96, 3.13, 4.35, 3.34, 3.40, 3.30, 5.29, 4.34, 3.95, 3.30, 6.02, 5.31, 3.55, 4.87, 4.65, 2.19, 5.45, 7.07, 6.08, 4.53, 4.33, 4.65, 4.02, 3.32, 6.12, 4.39, 6.01, 13.20, 5.02, 5.28, 7.88, 6.89, 3.48, 4.34, 4.67, 4.69, 7.42, 9.70, 6.41, 4.73, 3.52, 2.74, 4.46, 5.76, 2.93, 6.46, 6.31, 4.30, 8.12, 5.94, 7.10, 9.37, 9.74, 6.25, 9.07, 4.78, 6.90, 5.13, 4.01, 4.41, 6.37, 4.87, 5.38, 7.29, 6.03, 5.33, 4.34, 4.12, 6.37, 3.88, 4.82, 5.25, 7.06, 6.30, 6.29, 11.30, 5.82, 6.07, 3.98, 5.32, 5.16, 5.83, 6.90],
            }

            df_inflow = pd.DataFrame(data_inflow_st)
            df_local = pd.DataFrame(data_local_st)

            colors_st = ['#2980b9', '#e67e22', '#27ae60', '#d35400', '#8e44ad', '#c0392b', '#16a085']


            # Унифицированный стиль легенды в 3 столбца
            legend_3col_style = dict(
                orientation="h",
                y=-0.35, 
                x=0.5,
                xanchor="center",
                entrywidth=0.33, 
                entrywidthmode="fraction"
            )

            # Цвета маркеров (Excel-style)
            excel_colors_st = ['#ffffff', '#ff0000', '#ffff00', '#7030a0', '#996633']

            # --- ГРАФИК 1: ПРИТОК ИЗ КР (Кыргызстан -> Казахстан) ---
            fig_st_inflow = go.Figure()
            for i, col in enumerate(df_inflow.columns[1:]):
                fig_st_inflow.add_trace(go.Scatter(
                    x=df_inflow['Год'], y=df_inflow[col],
                    mode='lines+markers', # Прямые линии + маркеры
                    name=col,
                    line=dict(color='black', width=1),
                    marker=dict(
                        color=excel_colors_st[i % len(excel_colors_st)],
                        size=6,
                        line=dict(color='black', width=1)
                    ),
                    hovertemplate=f"<b>{col}</b><br>Год: %{{x}}<br>Сток: %{{y}} м³/с<extra></extra>"
                ))
                
            fig_st_inflow.update_layout(
                title="<b>ТРАНСГРАНИЧНЫЙ ПРИТОК (КЫРГЫЗСТАН -> КАЗАХСТАН)</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                template="plotly_white", 
                height=500, 
                hovermode="x unified",
                legend=legend_3col_style,
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
          )

            # --- ГРАФИК 2: МЕСТНЫЙ СТОК (Шу-Таласский ВХБ внутри РК) ---
            fig_st_local = go.Figure()
            for i, col in enumerate(df_local.columns[1:]):
                fig_st_local.add_trace(go.Scatter(
                    x=df_local['Год'], y=df_local[col],
                    mode='lines+markers',
                    name=col,
                    line=dict(color='black', width=1),
                    marker=dict(
                        color=excel_colors_st[(i+4) % len(excel_colors_st)], # Смещение цвета
                        size=6,
                        line=dict(color='black', width=1)
                    ),
                    hovertemplate=f"<b>{col}</b><br>Год: %{{x}}<br>Сток: %{{y}} м³/с<extra></extra>"
                ))

            fig_st_local.update_layout(
                title="<b>МЕСТНЫЙ СТОК ШУ-ТАЛАССКОГО ВХБ (ВНУТРИ РК)</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                template="plotly_white", 
                height=500, 
                hovermode="x unified",
                legend=legend_3col_style,
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
          )

            # --- ВЫВОД ---
            col_a, col_b = st.columns(2)
            with col_a:
                st.plotly_chart(fig_st_inflow, use_container_width=True, key=f"st_inflow_graph_{name}")
            with col_b:
                st.plotly_chart(fig_st_local, use_container_width=True, key=f"st_local_graph_{name}")
            st.divider()                

        # --- ЭТОТ БЛОК ВСТАВЛЯТЬ ТОЛЬКО В РАЗДЕЛ БАЛКАШ-АЛАКОЛЬСКОГО ВХБ ---
            # Убедитесь, что этот блок стоит на том же уровне, что и графики для Балхаша
            st.subheader("📊 Анализ суммарных водных ресурсов бассейна (1940–2024 гг.)")

            # border=True работает в новых версиях Streamlit (1.30+)
            with st.container(border=True):
                col_text, col_metric = st.columns([3, 1])
                
                with col_text:
                    st.markdown("""
                   За рассматриваемый период наблюдается слабовыраженная положительная тенденция изменения объёма стока.
                    """)
                
                with col_metric:
                    # metric автоматически подсвечивает дельту
                    st.metric(label="Тренд стока", value="Рост", delta="+ небольшой")

                st.divider()

                st.write("""
                Увеличение водности связано с интенсификацией снегово-ледникового питания в высокогорной части бассейна на фоне деградации ледников Тянь-Шаня и изменением режима осадков, что временно компенсирует рост испаряемости и формирует рост суммарного притока в отдельные многоводные годы.
                """)

                st.info("""
                **Ключевой фактор:**В результате, несмотря на рост летних температур, увеличение увлажненности в холодный период и приток паводковых вод нивелируют потери на испарение, удерживая линию тренда от падения.
                """, icon="💧")

                st.warning("""
                **Вывод:** Зимние осадки удерживают сток в норме ($1{,}16$ км³/год), компенсируя испарение, но резкие паводки повышают риски.
                """, icon="⚠️")

                
                
# --- СПЕЦИАЛЬНЫЙ БЛОК Тобол-Торгайского ВХБ ---
        if "Тобыл-Торгайский" in name:
            st.markdown("---")
            st.markdown("### 📊 Детальный анализ стока по основным водным артериям")

            desc_col1, desc_col2 = st.columns(2)
            with desc_col1:
                st.info("""**Местный сток:** Для оценки водных ресурсов, формирующихся в Тобыл-Торгайском ВХБ выбраны постоянно действующие 4 реки бассейна с наибольшей водностью таких как: Тобыл, Аят, Кара Торгай, Иргиз, определяющих в основном поверхностные водные ресурсы, которые в сумме составляют около 76 % всех местных водных ресурсов.""")   
            with desc_col2:
                st.success("""**Приток:** Приток, поступающий в пределы Тобыл-Торгайского водохозяйственного бассейна из РФ по реке Тобыл и Тогызак.""")

            # 1. Подготовка данных
            years_tt = list(range(1940, 2025))
            
            # Данные трансграничного притока (РФ -> РК)
            # ВАЖНО: Убедитесь, что количество элементов совпадает с len(years_tt) = 85
            data_inflow_tt = {
                "Год": years_tt,
                "р. Аят - с. Варваринка": [3.13, 23.89, 20.25, 6.85, 2.68, 4.14, 11.18, 18.57, 14.82, 3.16, 6.32, 2.84, 4.87, 10.50, 2.04, 1.63, 3.40, 23.60, 2.82, 5.12, 11.10, 4.11, 2.91, 4.88, 4.53, 2.13, 5.12, 3.48, 3.18, 9.47, 12.90, 8.91, 4.85, 2.34, 4.53, 1.07, 2.73, 0.81, 5.87, 3.26, 2.10, 6.84, 2.43, 7.83, 2.61, 7.32, 1.21, 4.22, 4.29, 2.37, 14.80, 5.13, 2.14, 18.30, 20.00, 6.89, 2.22, 2.33, 3.22, 5.72, 15.20, 8.40, 12.70, 5.72, 5.45, 14.51, 3.22, 11.84, 10.00, 1.16, 3.58, 5.60, 6.28, 8.11, 5.12, 0.81, 3.64, 3.70, 3.54, 0.89, 2.28, 3.52, 0.86, 4.74, 17.50],
                "р. Тогызак - с. Тогызак": [2.11, 7.89, 7.53, 5.18, 1.22, 1.72, 6.12, 10.70, 8.88, 1.70, 4.05, 3.29, 1.84, 6.84, 0.97, 0.61, 1.41, 6.86, 1.72, 2.95, 2.90, 1.65, 2.43, 2.02, 2.78, 1.72, 2.07, 2.26, 1.91, 3.45, 8.18, 3.78, 2.38, 1.14, 1.11, 0.34, 1.23, 0.78, 2.23, 0.97, 0.64, 2.42, 0.51, 1.74, 2.20, 2.55, 0.70, 1.60, 2.55, 1.17, 5.53, 1.69, 0.98, 2.72, 7.25, 2.84, 1.28, 0.96, 2.80, 1.60, 6.64, 3.25, 4.72, 2.42, 2.60, 6.08, 1.71, 3.77, 3.97, 0.84, 2.57, 1.27, 2.82, 7.22, 4.67, 1.54, 3.63, 3.22, 2.23, 1.26, 1.95, 1.42, 0.77, 0.99, 8.03],
                "р. Тобол - г. Костанай": [4.56, 58.20, 64.50, 18.20, 4.22, 10.70, 37.80, 63.00, 41.00, 6.43, 18.20, 4.61, 15.10, 21.40, 6.78, 5.22, 8.78, 39.60, 7.48, 16.10, 16.40, 7.03, 10.30, 8.30, 18.40, 5.33, 6.66, 2.66, 2.09, 2.84, 36.20, 29.30, 6.66, 3.03, 2.11, 1.49, 1.09, 1.02, 1.84, 0.93, 1.25, 1.66, 2.41, 5.70, 2.20, 18.40, 3.82, 3.50, 9.85, 8.85, 29.70, 6.28, 3.14, 35.60, 44.50, 6.16, 2.30, 1.85, 11.50, 3.52, 37.10, 14.50, 24.30, 9.97, 14.40, 30.50, 4.02, 9.44, 8.38, 4.93, 2.98, 3.76, 6.25, 9.26, 9.43, 5.43, 9.00, 7.16, 5.99, 5.92, 4.68, 4.46, 3.49, 2.79, 54.20]
            }
            
            # Данные местного стока (РК)
            data_local_tt = {
                "Год": years_tt,
                "р. Кара-Торгай": [8.16, 19.87, 16.90, 10.40, 1.25, 4.20, 15.10, 2.58, 26.30, 25.20, 4.87, 3.56, 5.90, 12.20, 21.60, 7.46, 8.28, 10.50, 14.80, 12.30, 7.79, 5.43, 10.20, 10.00, 15.50, 8.16, 14.80, 1.91, 0.74, 6.57, 11.10, 12.30, 10.60, 15.90, 16.28, 5.60, 10.45, 9.45, 11.10, 10.20, 10.20, 7.94, 4.29, 13.86, 13.21, 8.92, 14.50, 18.28, 15.50, 11.11, 15.60, 9.71, 14.69, 12.99, 3.32, 12.42, 15.59, 15.64, 8.90, 3.72, 4.70, 5.11, 14.80, 5.11, 6.84, 12.04, 3.01, 15.27, 4.66, 4.44, 10.20, 4.12, 1.88, 4.77, 7.30, 10.70, 14.00, 19.20, 13.60, 8.44, 14.70, 8.65, 12.80, 8.22, 21.50],
                "р. Иргиз": [3.35, 41.54, 34.85, 10.19, 2.53, 5.21, 18.16, 31.76, 24.86, 3.41, 9.23, 2.81, 8.68, 9.34, 4.32, 4.47, 5.72, 25.99, 4.99, 7.02, 9.37, 6.55, 7.21, 4.08, 23.70, 5.77, 9.75, 0.16, 1.85, 2.50, 9.00, 21.90, 8.04, 7.10, 0.97, 1.60, 2.82, 3.78, 10.50, 11.20, 6.61, 12.60, 2.41, 16.40, 0.70, 13.30, 6.54, 16.30, 10.20, 11.00, 4.02, 6.61, 1.45, 32.60, 4.56, 8.06, 2.50, 2.01, 8.28, 4.53, 23.21, 8.52, 21.15, 4.90, 16.82, 19.71, 0.32, 12.40, 0.29, 2.04, 18.60, 5.13, 4.07, 0.27, 1.59, 7.31, 6.77, 5.39, 5.16, 0.10, 0.17, 0.10, 5.65, 3.21, 39.20]
            }

            # Создание DataFrame с обработкой длины списков (на всякий случай)
            df_inflow_tt = pd.DataFrame({k: pd.Series(v) for k, v in data_inflow_tt.items()})
            df_local_tt = pd.DataFrame({k: pd.Series(v) for k, v in data_local_tt.items()})

            colors_tt = ['#34495e', '#e74c3c', '#27ae60', '#f39c12', '#9b59b6']

            # Унифицированный стиль легенды в 3 столбца
            legend_3col_style = dict(
                orientation="h",
                y=-0.35, 
                x=0.5,
                xanchor="center",
                entrywidth=0.33, 
                entrywidthmode="fraction"
            )

            # Цвета маркеров в стиле Excel
            excel_colors_tt = ['#ffffff', '#ff0000', '#ffff00', '#7030a0', '#996633']

            # --- ГРАФИК 1: ТРАНСГРАНИЧНЫЙ ПРИТОК (РФ -> РК) ---
            fig_tt_inflow = go.Figure()
            for i, col in enumerate(df_inflow_tt.columns[1:]):
                fig_tt_inflow.add_trace(go.Scatter(
                    x=df_inflow_tt['Год'], y=df_inflow_tt[col],
                    mode='lines+markers', # Линии + точки
                    name=col,
                    line=dict(color='black', width=1),
                    marker=dict(
                        color=excel_colors_tt[i % len(excel_colors_tt)],
                        size=6,
                        line=dict(color='black', width=1)
                    ),
                    hovertemplate=f"<b>{col}</b><br>Год: %{{x}}<br>Сток: %{{y}} м³/с<extra></extra>"
                ))
                

            fig_tt_inflow.update_layout(
                title="<b>ПРИТОК ТРАНСГРАНИЧНЫХ РЕК (РФ -> РК)</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                template="plotly_white", 
                height=500, 
                hovermode="x unified",
                legend=legend_3col_style,
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
           )

            # --- ГРАФИК 2: МЕСТНЫЙ СТОК (РК) ---
            fig_tt_local = go.Figure()
            for i, col in enumerate(df_local_tt.columns[1:]):
                fig_tt_local.add_trace(go.Scatter(
                    x=df_local_tt['Год'], y=df_local_tt[col],
                    mode='lines+markers',
                    name=col,
                    line=dict(color='black', width=1),
                    marker=dict(
                        color=excel_colors_tt[(i+2) % len(excel_colors_tt)], # Смещение цвета
                        size=6,
                        line=dict(color='black', width=1)
                    ),
                    hovertemplate=f"<b>{col}</b><br>Год: %{{x}}<br>Сток: %{{y}} м³/с<extra></extra>"
                ))

            fig_tt_local.update_layout(
                title="<b>МЕСТНЫЙ СТОК (РЕКИ КАРА-ТОРГАЙ И ИРГИЗ)</b>",
                xaxis_title="ГОД",
                yaxis_title="Q, м³/с",
                template="plotly_white", 
                height=500, 
                hovermode="x unified",
                legend=legend_3col_style,
                margin=dict(l=40, r=20, t=60, b=100),
                xaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, tickangle=-90, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black')),
                yaxis=dict(showgrid=True, gridcolor='lightgrey', linecolor='black', mirror=True, zeroline=False, title_font=dict(size=14, color='black'),tickfont=dict(size=12, color='black'))
          )

            # --- ВЫВОД В STREAMLIT ---
            col_a, col_b = st.columns(2)
            with col_a:
                st.plotly_chart(fig_tt_inflow, use_container_width=True, key=f"tt_inflow_graph_{name}")
            with col_b:
                st.plotly_chart(fig_tt_local, use_container_width=True, key=f"tt_local_graph_{name}")
                
        # --- ЭТОТ БЛОК ВСТАВЛЯТЬ ТОЛЬКО В РАЗДЕЛ БАЛКАШ-АЛАКОЛЬСКОГО ВХБ ---
            # Убедитесь, что этот блок стоит на том же уровне, что и графики для Балхаша
            st.subheader("📊 Анализ суммарных водных ресурсов бассейна (1940–2024 гг.)")

            # border=True работает в новых версиях Streamlit (1.30+)
            with st.container(border=True):
                col_text, col_metric = st.columns([3, 1])
                
                with col_text:
                    st.markdown("""
                   Суммарные ресурсы Тобыл-Торгайского ВХБ за рассматриваемый период с 1940 по 2024 гг. на графике прослеживается выраженная тенденция к снижению объема стока, при этом ресурсы бассейна характеризуются экстремальной многолетней неравномерностью.
                    """)
                
                with col_metric:
                    # metric автоматически подсвечивает дельту
                    st.metric(label="Тренд стока", value="Рост", delta="+ небольшой")

                st.divider()

                st.write("""
                Тенденция к снижению объема стока в Тобыл-Торгайском бассейне объясняется сочетанием климатических изменений — уменьшением количества осадков в теплые сезоны при росте испаряемости — и значительным антропогенным воздействием, включая зарегулированность стока каскадом водохранилищ (Верхне-Тобольское, Каратомарское) и интенсивный водозабор для нужд промышленности и сельского хозяйства. 
                """)

                st.info("""
                **Ключевой фактор:**В отличие от северных рек, данный бассейн является наиболее маловодным в Казахстане, где естественное сокращение стока из-за потепления не компенсируется осадками, что ведет к устойчивому дефициту воды.
                """, icon="💧")

                st.warning("""
                **Вывод:** Сочетание засухи и водозабора ведет к устойчивому дефициту воды, формируя выраженный тренд на снижение стока в самом маловодном бассейне Казахстана.
                """, icon="⚠️")
                

    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go

    def show_water_resources_block():
        st.write("---")
        st.header("🌊 ОЦЕНКА ИЗМЕНЕНИЯ СТОКА РЕК КАЗАХСТАНА НА ПЕРСПЕКТИВУ ДО 2050 ГОДА")
        
        col_method, col_scenarios = st.columns([1.2, 1], gap="large")
        
        with col_method:
            st.subheader("📊 Материалы и методы исследования")
            st.markdown("""
            * **Данные наблюдений**: Сеть Казахстана.
            * **Климатические архивы**: **Terra Climate**.
            * **Прогнозные модели**: **23 модели** (МОЦАО) до 2050 г.
            * **Базисный период**: Норма стока за **1930-2019 гг.**.
            """)

        with col_scenarios:
            st.subheader("🌡️ Климатические сценарии")
            st.markdown("""
            <div style="display: flex; flex-direction: column; gap: 8px;">
                <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; border-left: 8px solid #ff4b4b; font-size: 1.1em;">
                    <span style="color: #ff4b4b; font-weight: bold;">RCP 8.5</span> — Жесткий
                </div>
                <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; border-left: 8px solid #ffa500; font-size: 1.1em;">
                    <span style="color: #ffa500; font-weight: bold;">RCP 4.5</span> — Умеренный
                </div>
                <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; border-left: 8px solid #28a745; font-size: 1.1em;">
                    <span style="color: #28a745; font-weight: bold;">RCP 2.6</span> — Мягкий
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    def draw_basin_card(name, norm_text, data_dict, highlights):
        # Создаем уникальный ID на основе имени бассейна
        unique_id = name.replace(" ", "_").lower()
        
        with st.container():
            st.markdown(f"""
                <div style="border: 1px solid #e6e9ef; border-radius: 10px; padding: 20px; background-color: #ffffff; margin-bottom: 20px;">
                    <h3 style="color: #1f77b4; margin-top: 0; font-size: 24px;">{name}</h3>
                    <p style="font-size: 18px; color: #333;">{norm_text}</p>
                </div>
            """, unsafe_allow_html=True)
            
            periods = list(data_dict.keys())
            rcp26 = [data_dict[p][0] for p in periods]
            rcp45 = [data_dict[p][1] for p in periods]
            rcp85 = [data_dict[p][2] for p in periods]

            fig = go.Figure()
            fig.add_trace(go.Bar(name='RCP 2.6', x=periods, y=rcp26, marker_color='#00a65a', text=rcp26, textposition='outside', textfont=dict(size=16)))
            fig.add_trace(go.Bar(name='RCP 4.5', x=periods, y=rcp45, marker_color='#ffc107', text=rcp45, textposition='outside', textfont=dict(size=16)))
            fig.add_trace(go.Bar(name='RCP 8.5', x=periods, y=rcp85, marker_color='#ff0000', text=rcp85, textposition='outside', textfont=dict(size=16)))

            fig.update_layout(
                barmode='group', height=500, margin=dict(t=40, b=20, l=10, r=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(size=16)),
                font=dict(size=14),
                yaxis=dict(title=dict(text="Объем воды, км³", font=dict(size=16)), tickfont=dict(size=14), autorange=True),
                xaxis=dict(tickfont=dict(size=16, color="black")),
                plot_bgcolor='white', paper_bgcolor='white'
            )
            
            fig.update_yaxes(showgrid=True, gridcolor='lightgrey')
            
            # КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: добавляем параметр key
            st.plotly_chart(fig, use_container_width=True, key=f"chart_{unique_id}")
            
            st.write("**Среднее значение стока (км³):**")
            h_cols = st.columns(3)
            colors = ["#28a745", "#f39c12", "#d32f2f"]
            for i, (scen, val) in enumerate(highlights.items()):
                with h_cols[i]:
                    st.markdown(f"""
                        <div style="text-align: center; padding: 15px; border-radius: 10px; background: #f0f2f6; border: 1px solid #ddd;">
                            <div style="font-size: 14px; color: #666; font-weight: bold; margin-bottom: 5px;">{scen}</div>
                            <div style="font-size: 26px; font-weight: bold; color: {colors[i]};">{val}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    

    # --- ЗАПУСК ---
    show_water_resources_block()

    st.markdown("## 💧 Прогноз водных ресурсов по бассейнам")

    # Данные бассейнов (все переменные выровнены по левому краю)
    data_balhash = {
        "2022-2030 гг.": [33.50, 33.30, 33.40],
        "2031-2040 гг.": [32.80, 32.70, 33.60],
        "2041-2050 гг.": [33.30, 32.80, 33.70]
    }

    data_ertis = {
        "2022-2030 гг.": [38.5, 38.5, 43.9],
        "2031-2040 гг.": [39.8, 39.7, 42.6],
        "2041-2050 гг.": [40.3, 39.5, 43.9]
    }

    data_aral = {
        "2022-2030 гг.": [23.4, 25.4, 26.6],
        "2031-2040 гг.": [22.2, 25.2, 25.7],
        "2041-2050 гг.": [23.4, 25.2, 26.3]
    }

    data_zhayik = {
        "2022-2030 гг.": [14.5, 12.8, 13.8],
        "2031-2040 гг.": [14.4, 13, 13.3],
        "2041-2050 гг.": [14.6, 13.6, 13.3]
    }

    data_shu_talas = {
        "2022-2030 гг.": [2.80, 3.00, 3.00],
        "2031-2040 гг.": [2.70, 2.90, 2.90],
        "2041-2050 гг.": [2.90, 3.00, 3.20]
    }

    data_obyl_torgay = {
        "2022-2030 гг.": [1.81, 2.16, 2.11],
        "2031-2040 гг.": [1.76, 2.17, 2.04],
        "2041-2050 гг.": [1.81, 2.13, 2.17]
    }

    data_nura_sarysu = {
        "2022-2030 гг.": [1.38, 1.39, 1.42],
        "2031-2040 гг.": [1.36, 1.4, 1.41],
        "2041-2050 гг.": [1.43, 1.41, 1.46]
    }

    data_esil = {
        "2022-2030 гг.": [2.80, 3.00, 3.00],
        "2031-2040 гг.": [2.70, 2.90, 2.90],
        "2041-2050 гг.": [2.90, 3.00, 3.20]
    }

    # Средние значения (Highlights)
    highlights_balhash = {"RCP 2.6": 33.20, "RCP 4.5": 32.93, "RCP 8.5": 33.57}
    highlights_ertis = {"RCP 2.6": 39.5, "RCP 4.5": 39.2, "RCP 8.5": 43.4}
    highlights_aral = {"RCP 2.6": 23.0, "RCP 4.5": 25.2, "RCP 8.5": 26.2}
    highlights_zhayik = {"RCP 2.6": 14.5, "RCP 4.5": 13.1, "RCP 8.5": 13.4}
    highlights_shu = {"RCP 2.6": 2.8, "RCP 4.5": 2.9, "RCP 8.5": 3.0}
    highlights_torgay = {"RCP 2.6": 1.79, "RCP 4.5": 2.15, "RCP 8.5": 2.10}
    highlights_nura = {"RCP 2.6": 1.39, "RCP 4.5": 1.40, "RCP 8.5": 1.43}
    highlights_esil = {"RCP 2.6": 2.80, "RCP 4.5": 3.0, "RCP 8.5": 3.0}

    # Создаем ряды колонок
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    row3_col1, row3_col2 = st.columns(2)
    row4_col1, row4_col2 = st.columns(2)

    # РЯД 1
    with row1_col1:
        draw_basin_card("БАЛКАШ – АЛАКОЛЬСКИЙ БАССЕЙН", "В результате оценки изменения стока к 2050 г. ожидается увеличение относительно нормы (29,9 км³).", data_balhash, highlights_balhash)
    with row1_col2:
        draw_basin_card("ЕРТИССКИЙ БАССЕЙН", "В результате оценки изменения стока к 2050 г. ожидается увеличение относительно нормы (33.4 км³).", data_ertis, highlights_ertis)

    # РЯД 2
    with row2_col1:
        draw_basin_card("АРАЛО – СЫРДАРЬИНСКИЙ БАССЕЙН", "В результате оценки изменения стока к 2050 г. ожидается увеличение по «умеренно-жесткому» и «жесткому» сценарию, а по «мягкому» сценарию сокращение относительно нормы (21,4 км³).", data_aral, highlights_aral)
    with row2_col2:
        draw_basin_card("ЖАЙЫК – КАСПИЙСКИЙ БАССЕЙН", "В результате оценки изменения стока к 2050 г. ожидается увеличение относительно нормы (12.0 км³).", data_zhayik, highlights_zhayik)

    # РЯД 3
    with row3_col1:
        draw_basin_card("ШУ – ТАЛАССКИЙ БАССЕЙН", "В результате оценки изменения стока к 2050 г. ожидается увеличение относительно нормы (4,12 км³).", data_shu_talas, highlights_shu)
    with row3_col2:
        draw_basin_card("ТОБЫЛ – ТОРГАЙСКИЙ БАССЕЙН", "В результате оценки изменения стока к 2050 г. ожидается увеличение относительно нормы (1,67 км³).", data_obyl_torgay, highlights_torgay)

    # РЯД 4
    with row4_col1:
        draw_basin_card("НУРА-САРЫСУЙСКИЙ БАССЕЙН", "В результате оценки изменения стока к 2050 г. ожидается увеличение относительно нормы (1,16 км³).", data_nura_sarysu, highlights_nura)
    with row4_col2:
        draw_basin_card("ЕСИЛЬСКИЙ БАССЕЙН", "В результате оценки изменения стока к 2050 г. ожидается увеличение относительно нормы (2,29 км³).", data_esil, highlights_esil)
        
        

# --- Твой основной контент по Каспию идет во вкладку №5 (индекс 5) ---
with tabs[6]:
    st.markdown('<h1 class="main-title">🌊 Исследование Каспийского моря</h1>', unsafe_allow_html=True)
    # ВСЕ СТРОКИ НИЖЕ ДОЛЖНЫ ИМЕТЬ ОТСТУП (4 ПРОБЕЛА)
        
    
    if 'selected_param' not in st.session_state:
        st.session_state.selected_param = "Уровень моря"

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
        # Увеличили font-size до 1.3rem для заголовка и 1.1rem для текста
        st.markdown('<div class="white-label-header"><p style="font-size: 3.0rem; font-weight: bold; margin-bottom: 10px;">📡 Сеть</p></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 1.4rem; line-height: 1.5; margin-bottom: 15px;">РГП «Казгидромет» осуществляет непрерывный гидрометеорологический и экологический мониторинг казахстанского сектора Каспийского моря.</div>', unsafe_allow_html=True)
        st.markdown("""<div style="font-size: 1.2rem; line-height: 2.0;">🚢 <b>10</b> морских станций<br>🌦️ <b>28</b> метеостанций<br>💧 <b>4</b> гидропоста<br>🧪 <b>50</b> точек качества</div>""", unsafe_allow_html=True)

    with t_col2:
        st.markdown('<div class="white-label-header"><p style="font-size: 2.2rem; font-weight: bold; margin-bottom: 10px;">🔎 Параметры</p></div>', unsafe_allow_html=True)
        
        # Сделали приписку про 2025 год крупнее (1.0rem) и темнее
        st.markdown('<div style="color: #1E293B; font-size: 1.0rem; margin-bottom: 10px; font-weight: 700;">📅 Оперативные данные за 2025 г.</div>', unsafe_allow_html=True)
        
        p_c1, p_c2 = st.columns(2)
        params = [
            ("🌊", "Уровень моря"), ("🌡️", "Температура воздуха"), 
            ("💧", "Температура воды"), ("🧪", "Соленость"), 
            ("❄️", "Лед"), ("🌬️", "Ветер"), ("〰️", "Волнение")
        ]
        
        for i, (emoji, name) in enumerate(params):
            with [p_c1, p_c2][i % 2]:
                # Кнопки в Streamlit нельзя увеличить напрямую через font-size без кастомного CSS, 
                # но use_container_width=True делает их массивнее.
                if st.button(f"{emoji} {name}", key=f"top_{name}", use_container_width=True):
                    st.session_state.selected_param = name
                

    with t_col3:
        current_unit = units.get(st.session_state.selected_param, "")
        st.markdown(f'<div class="white-label-header"><p style="font-size: 2.2rem; font-weight: bold; margin-bottom: 10px;">📊 Сезонный ход ({current_unit})</p></div>', unsafe_allow_html=True)
        
        display_data = seasonal_data.get(st.session_state.selected_param, [0]*12)
        
        fig_s = go.Figure()
        fig_s.add_trace(go.Scatter(
            x=months, y=display_data,
            mode='lines+markers', 
            line=dict(color='#0072FF', width=4, shape='spline'), # Увеличили толщину линии до 4
            marker=dict(size=10, color='white', line=dict(color='#0072FF', width=2)), # Увеличили маркер
            name=st.session_state.selected_param
        ))
        
        fig_s.update_layout(
            height=300, # Увеличили высоту для лучшей видимости
            margin=dict(l=50, r=10, t=30, b=50), # Увеличили l и b для подписей
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified",
            # Настройки шрифта для всего графика
            font=dict(color="black") 
        )

        # Применяем ЧЕРНЫЙ цвет и КРУПНЫЙ шрифт к осям
        fig_s.update_xaxes(
            showgrid=False, 
            tickfont=dict(size=14, color='black', family="Arial"), # Крупные черные месяцы
            linecolor='black'
        )
        fig_s.update_yaxes(
            showgrid=True, 
            gridcolor='#E2E8F0', 
            tickfont=dict(size=14, color='black', family="Arial"), # Крупные черные значения
            title_font=dict(size=16, color='black'),
            linecolor='black'
        )
        
        st.plotly_chart(fig_s, use_container_width=True, config={'displayModeBar': False})
    
    st.divider()
    
    # --- НИЖНИЙ БЛОК ---
    b_col1, b_col2 = st.columns([1.8, 1])
    
       
            
    with b_col1:
        # Увеличили заголовок до 1.3rem и сделали его жирным
        st.markdown('<div class="white-label-header"><p style="font-size: 3.0rem; font-weight: bold; margin-bottom: 12px;">📉 Динамика уровня Каспийского моря</p></div>', unsafe_allow_html=True) 
        
        # Главный тезис: увеличили до 1.2rem и добавили насыщенный черный цвет
        st.markdown('<div style="font-size: 1.2rem; font-weight: 700; color: #1E293B; margin-bottom: 10px; line-height: 1.4;">Уровень Каспийского моря подвержен значительным колебаниям</div>', unsafe_allow_html=True)
        
        # Основное описание: увеличили до 1.1rem, сделали межстрочный интервал шире для легкости чтения
        st.markdown('<div style="font-size: 1.1rem; color: #334155; line-height: 1.6; text-align: justify;">В 2025 г. уровень моря в его казахстанской части достиг отметки <span style="color: #E11D48; font-weight: bold;">минус 29,35 м БС</span>. Это один из самых низких показателей за последние 100 лет в казахстанской части Каспийского моря.</div>', unsafe_allow_html=True)
        
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
# Увеличиваем шрифты и меняем цвета на черные
        fig_hist.update_xaxes(
            showgrid=False, 
            linecolor='black',       # Сделали линию оси черной
            linewidth=1,             # Сделали линию чуть толще
            range=[1920, 2026],
            tickfont=dict(size=14, color='black', family="Arial"), # Крупные цифры годов
            title_font=dict(size=16, color='black')               # Крупный заголовок (если есть)
        )
        
        fig_hist.update_yaxes(
            showgrid=True, 
            gridcolor='#E2E8F0', 
            linecolor='black',       # Сделали линию оси черной
            linewidth=1,
            zeroline=False,
            tickfont=dict(size=14, color='black', family="Arial"), # Крупные значения уровня
            title_font=dict(size=16, color='black')               # Крупный заголовок "м БС"
        )

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
                        <span style="font-size: 1.0rem;">Обусловлено активным строительством ГЭС на Волге и длительным периодом засухи.</span>
                    </div>
                """, unsafe_allow_html=True)
                
            with c_phase2:
                st.markdown("""
                    <div style="border-left: 3px solid #0072FF; padding-left: 15px;">
                        <span style="color: #0072FF; font-weight: 800;">1978 — 1995</span><br>
                        <b>Аномальный подъем</b><br>
                        <span style="font-size: 1.0rem;">Внезапное увеличение стока рек и изменение атмосферной циркуляции. Уровень вырос на 2.5 метра.</span>
                    </div>
                """, unsafe_allow_html=True)
                
            with c_phase3:
                st.markdown("""
                    <div style="border-left: 3px solid #D32F2F; padding-left: 15px;">
                        <span style="color: #D32F2F; font-weight: 800;">2005 — н.в.</span><br>
                        <b>Текущий спад</b><br>
                        <span style="font-size: 1.0rem;">Снижение притока и рост испарения из-за глобального потепления. Фаза, требующая адаптации.</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background: #F8FAFC; border-radius: 10px; padding: 15px; margin-top: 20px; border: 1px dashed #CBD5E1; font-size: 0.95rem;">
                    <b>💡 Мнение ученых:</b> Каспий живет циклами. Нынешнее состояние — это вызов для экономики, но с точки зрения геологии море неоднократно проходило через подобные и даже более глубокие минимумы.
                </div>
            """, unsafe_allow_html=True)

    # --- КОНЕЦ БЛОКА ЦИКЛИЧНОСТИ ---

    with b_col2:
        # 1. Заголовок
        st.markdown('<div class="white-label-header"><p class="section-header-text">⏳ Исторические минимумы и максимумы</p></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <style>
            .metric-card {
                background: linear-gradient(145deg, #ffffff, #f0f7ff);
                padding: 30px 15px;
                border-radius: 20px;
                border: 2px solid #3498db;
                box-shadow: 0 10px 25px rgba(52, 152, 219, 0.2);
                text-align: center;
                margin-bottom: 20px;
                min-height: 150px; /* Немного увеличили высоту для иконок */
                display: flex;
                flex-direction: column;
                justify-content: center;
                transition: 0.3s;
            }
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(52, 152, 219, 0.3);
            }
            
            /* Год - Крупный синий */
            .metric-year { 
                color: #3498db; 
                font-size: 1.6rem; 
                font-weight: 800; 
                margin: 0; 
                text-transform: uppercase; 
            }
            
            /* ГЛАВНОЕ ЗНАЧЕНИЕ - Сделали гигантским */
            .metric-value { 
                color: black; /* По умолчанию черный */
                font-size: 3.8rem; /* Очень крупно */
                font-weight: 900; 
                margin: 15px 0; 
                line-height: 1; 
            }
            
            /* Красный цвет для отрицательных значений */
            .metric-value-red { 
                color: #e74c3c; 
                font-size: 3.8rem; 
                font-weight: 900; 
                margin: 15px 0; 
                line-height: 1; 
            }
            
            /* Иконка - Крупная */
            .metric-icon { 
                font-size: 3rem; 
                margin-top: 10px; 
            }
            
            /* Подпись - Четкая */
            .metric-label { 
                color: #475569; 
                font-size: 1.3rem; 
                font-weight: 600; 
                margin: 0; 
                margin-top: 5px;
            }
        </style>
        """, unsafe_allow_html=True)


        # 3. Данные (без привязки к колонкам)
        history_data = [
            # Максимум 1903 г. - ставим нейтральную или волну
            {"year": "1903", "val": "-25,74 м", "label": "Максимум", "icon": "🌊"},
            # Минимум XX в. - стрелка вниз
            {"year": "1977", "val": "-29,01 м", "label": "Минимум XX в.", "icon": "📉"},
            # Пик подъема 1995 г. - стрелка вверх
            {"year": "1995", "val": "-26,62 м", "label": "Пик подъема", "icon": "📈"},
            # Текущий спад 2024 г. - стрелка вниз
            {"year": "2024", "val": "-29,05 м", "label": "Текущий спад", "icon": "📉"},
        ]


        # 4. Динамическое создание сетки (по 2 карточки в ряд)
# Используем автоматическое распределение по 2 колонки
        for i in range(0, len(history_data), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(history_data):
                    card = history_data[i + j]
                    
                    # ЛОГИКА: Если в значении есть минус, используем красный класс
                    if "-" in str(card['val']):
                        value_class = "metric-value-red"
                    else:
                        value_class = "metric-value"
                        
                    with cols[j]:
                        st.markdown(f"""
                            <div class="metric-card">
                                <p class="metric-year">{card['year']} год</p>
                                <p class="{value_class}">{card['val']}</p>
                                <div class="metric-icon">{card['icon']}</div>
                                <p class="metric-label">{card['label']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        


    # Создаем две колонки с равной шириной
    col1, col2 = st.columns(2)

    with col1:
        # 3. ПЕРВЫЙ БЛОК: ИЗМЕНЕНИЕ АКВАТОРИИ
        st.markdown("""
            <div style="background: #F0F9FF; padding: 20px; border-radius: 20px; border: 1px solid #BAE6FD; height: 250px; font-family: 'Montserrat', sans-serif;">
                <p style="margin: 0 0 15px 0; color: #0369A1; font-weight: 600; font-size: 1.1rem; text-align: center; text-transform: uppercase;">
                    Изменение акватории (2006 — 2024)
                </p>
                <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 10px; margin-top: 25px;">
                    <div style="text-align: center;">
                        <p style="margin: 0; color: #64748B; font-size: 0.7rem;">2006 г.</p>
                        <p style="margin: 0; color: #0C4A6E; font-size: 1.1rem; font-weight: 400;">392.3 <span style="font-size: 0.6rem;">тыс. км²</span></p>
                    </div>
                    <div style="flex-grow: 1; position: relative; margin: 0 15px; text-align: center;">
                        <div style="height: 2px; background: #0EA5E9; width: 100%;"></div>
                        <div style="position: absolute; right: -2px; top: -5px; width: 10px; height: 10px; border-top: 2px solid #0EA5E9; border-right: 2px solid #0EA5E9; transform: rotate(45deg);"></div>
                        <span style="background: #0EA5E9; color: white; padding: 1px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: 600; position: relative; top: -20px;">
                            -36.6 тыс. км²
                        </span>
                    </div>
                    <div style="text-align: center;">
                        <p style="margin: 0; color: #0369A1; font-size: 0.7rem; font-weight: 400;">2024 г.</p>
                        <p style="margin: 0; color: #0369A1; font-size: 1.1rem; font-weight: 400;">355.7 <span style="font-size: 0.6rem;">тыс. км²</span></p>
                    </div>
                </div>
                <p style="margin: 15px 0 0 0; text-align: center; color: #0C4A6E; font-size: 0.85rem; line-height: 1.4;">
                    За этот период Каспий потерял объем воды, равный <b>47.6 км³</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # 4. ВТОРОЙ БЛОК: КРИТИЧЕСКИЙ ПОРОГ (-34 см)
        st.markdown("""
            <div style="background: #FFF5F5; padding: 20px; border-radius: 20px; border: 1px solid #FECACA; height: 250px; font-family: 'Montserrat', sans-serif; box-shadow: 0 4px 15px rgba(211, 47, 47, 0.05);">
                <p style="margin: 0 0 15px 0; color: #D32F2F; font-weight: 800; font-size: 0.9rem; text-align: center; text-transform: uppercase;">
                    Превышение критического порога
                </p>
                <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 10px; margin-top: 25px;">
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
                <p style="margin: 15px 0 0 0; text-align: center; color: #334155; font-size: 0.85rem; line-height: 1.4;">
                    Уровень моря опустился ниже самого низкого значения XX века.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    
    # 1. Уменьшаем отступы у линии (с 80px до 30px например)
    st.markdown("<hr style='margin: 30px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # 2. Уменьшаем размер шрифта заголовка (5.0rem — это очень много, обычно 2.0-2.5 достаточно)
    # И убираем margin-bottom, если он не нужен
    st.markdown('<div class="white-label-header"><p style="font-size: 3.5rem; font-weight: bold; margin-bottom: 0px;">🔍 Основные факторы, влияющие на изменение уровня</p></div>', unsafe_allow_html=True) 

    # 3. Убираем лишний margin-bottom у подзаголовка
    st.markdown("""
        <div style="margin-bottom: 10px; text-align: center;">
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
    st.divider()
    
    
    # --- БЛОК: ГЛОБАЛЬНЫЕ ПОСЛЕДСТВИЯ ---
    st.markdown("<hr style='margin: 20px 0; opacity: 0.1;'>", unsafe_allow_html=True)
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

    st.divider()
    
    # --- БЛОК: ПРОГНОЗЫ И ПРОДУКЦИЯ С ЭФФЕКТОМ НАЖАТИЯ ---
    st.markdown("<hr style='margin: 20px 0; opacity: 0.1;'>", unsafe_allow_html=True)
    st.markdown('<div class="white-label-header"><p class="section-header-text">📈 Прогнозы и информационная продукция</p></div>', unsafe_allow_html=True)

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
                    <div style="margin-bottom:18px;"><span style="font-size:1.15em; font-weight:700;">🌀 Обзор сгонно-нагонных явлений</span><br><span style="color:#0072FF; font-weight:600;">Раз в месяц</span></div>
                    <div style="margin-bottom:18px;"><span style="font-size:1.15em; font-weight:700;">📈 Прогноз уровня и волнения</span><br><span style="color:#0072FF; font-weight:600;">2 раза в неделю</span></div>
                    <div style="margin-bottom:18px;"><span style="font-size:1.15em; font-weight:700;">📁 Водный кадастр</span><br><span style="color:#0072FF; font-weight:600;">Ежегодно</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        
    st.divider()        
        
    # --- БЛОК: ДОЛГОСРОЧНЫЙ ПРОГНОЗ ---
    st.markdown("<hr style='margin: 40px 0; opacity: 0.1;'>", unsafe_allow_html=True)
    st.markdown('<div class="white-label-header"><p class="section-header-text">📈 Оценка долгосрочных изменений</p></div>', unsafe_allow_html=True)
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
                    Анализ многолетних колебаний и расчет сценариев изменения уровня моря до конца XXI века на основе данных глобальных климатических моделей.
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
            legend=dict(orientation="h", y=-0.25, xanchor="center", x=0.5, font=dict(size=14)),
            yaxis=dict(title="м БС", gridcolor='#E2E8F0', range=[-35, -26], tickfont=dict(size=12)),
            xaxis=dict(showgrid=False, dtick=5, tickfont=dict(size=12))
        )
        
        # Линия раздела (начало прогноза)
        fig_lt.add_vline(x=2024, line_width=1, line_dash="solid", line_color="#94a3b8")
        
        st.plotly_chart(fig_lt, use_container_width=True, config={'displayModeBar': False})


    with lt_plot_col2:
        st.markdown('<div class="promo-bold" style="font-size: 1.3em; margin-bottom: 10px;">🌊 Прогноз высоты волн (SSP5-8.5)</div>', unsafe_allow_html=True)

        # 1. Подготовка данных (замените эти списки на ваши данные или загрузите из df)
        years = list(range(2015, 2051))
        
        # Пример данных (замените на свои реальные значения)
        fort_shevchenko = [2.25, 2.01, 2.08, 2.20, 2.18, 2.03, 2.00, 2.08, 2.09, 1.96, 1.96, 2.00, 2.06, 2.00, 2.13, 2.03, 2.11, 2.03, 1.99, 1.96, 1.99, 2.07, 2.18, 2.29, 1.90, 1.98, 1.90, 1.95, 1.83, 2.15, 2.13, 2.02, 2.03, 1.96, 1.89, 2.21]
        aktau = [2.28, 2.05, 2.10, 2.29, 2.23, 2.07, 2.07, 2.12, 2.14, 2.05, 2.07, 2.07, 2.11, 2.09, 2.32, 2.14, 2.17, 2.10, 2.04, 2.12, 2.11, 2.15, 2.29, 2.30, 1.96, 2.09, 1.99, 2.06, 1.95, 2.18, 2.25, 2.05, 2.07, 2.05, 1.88, 2.25]
        kuryk = [2.32, 2.08, 2.15, 2.31, 2.26, 2.11, 2.09, 2.14, 2.17, 2.06, 2.08, 2.08, 2.12, 2.10, 2.33, 2.16, 2.20, 2.13, 2.08, 2.13, 2.13, 2.16, 2.33, 2.36, 1.98, 2.11, 1.99, 2.08, 1.96, 2.21, 2.29, 2.09, 2.12, 2.06, 1.91, 2.31]

        # 2. Создание графика Plotly
        fig = go.Figure()

        # Линия для Форт-Шевченко
        fig.add_trace(go.Scatter(x=years, y=fort_shevchenko, name='Форт-Шевченко',
                                 line=dict(color='#4F7942', width=3)))

        # Линия для Актау
        fig.add_trace(go.Scatter(x=years, y=aktau, name='Актау',
                                 line=dict(color='#A0C4DE', width=3)))

        # Линия для Курык
        fig.add_trace(go.Scatter(x=years, y=kuryk, name='Курык',
                                 line=dict(color='#D35400', width=3)))

        # 3. Настройка оформления (максимально близко к вашему скрину)
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=0, r=0, t=20, b=0),
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            hovermode="x unified" # Показывает значения всех линий при наведении на год
        )

        # Настройка осей
        fig.update_xaxes(title="год", showline=True, linewidth=1, linecolor='black', mirror=True, 
                         tickmode='linear', dtick=1, tickangle=90, gridcolor='#f0f0f0', autorange='reversed')
        fig.update_yaxes(title="высота волны, м", showline=True, linewidth=1, linecolor='black', mirror=True, 
                         range=[1.5, 2.5], gridcolor='#f0f0f0')

        # 4. Отображение в Streamlit
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

     

    # Описание прогнозов
    st.markdown("""
        <div style="margin-bottom: 35px; color: #1E293B; line-height: 1.6; font-family: 'Montserrat', sans-serif;">
            <p style="font-size: 1.15rem; border-left: 4px solid #3B82F6; padding-left: 15px;">
                Согласно международным климатическим моделям <b>IPCC</b>, уровень Каспийского моря продолжит снижаться под влиянием глобального потепления.
            </p>
        </div>
    """, unsafe_allow_html=True)



    st.divider()
    
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
            
            .ecology-container {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 150px;
                padding: 40px;
                background-color: #ffffff;
                font-family: 'Montserrat', sans-serif;
            }

            .ecology-content {
                text-align: center;
                max-width: 800px;
            }

            .ecology-title {
                color: #1E293B;
                font-size: 2.2rem;
                font-weight: 700;
                margin-bottom: 30px;
                border: none !important; /* Убираем линию Streamlit */
            }

            .ecology-text {
                color: #475569;
                font-size: 1.25rem;
                line-height: 1.8;
                margin: 0 auto;
            }

            .highlight {
                color: #3B82F6;
                font-weight: 300;
            }
        </style>

        <div class="ecology-container">
            <div class="ecology-content">
                <h2 class="ecology-title">Сохраним Каспий вместе</h2>
                <p class="ecology-text">
                    Каспийское море — это уникальное природное наследие, которое требует нашего общего внимания и заботы. 
                    Сегодня, перед лицом глобальных климатических изменений, <span class="highlight">совместная работа</span> 
                    всех прикаспийских государств и научных центров становится единственным путем к сохранению его экосистемы.
                    <br><br>
                    Бережное отношение к ресурсам и постоянный мониторинг — это наш общий вклад в будущее, 
                    который позволит передать живое море следующим поколениям.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)




   

with tabs[7]:
    st.title("🌍 Климат Казахстана и регионов")

    # Основной слоган (Header)
    st.markdown("### «Земля контрастов в эпоху перемен: Казахстан теплеет в 2 раза быстрее, чем планета в среднем»")
    
    # Текстовый блок с описанием
    st.write("""
    Казахстан находится в центре крупнейшего континента, вдали от смягчающего влияния океанов. 
    Это делает нашу экосистему крайне уязвимой к глобальным изменениям. 
    """)

    # Акцентный блок для ключевого факта
    st.info("""
    **За последние 50 лет средняя температура в стране выросла на 0,40 ºС каждые 10 лет**, 
    что уже сегодня меняет облик сельского хозяйства, водных ресурсов и образа жизни миллионов людей.
    """)

    st.markdown("---") # Разделительная линия перед основным контентом (графиками/картами)
    

    import streamlit as st
    import streamlit.components.v1 as components

    # 1. Сначала принудительно выравниваем все колонки по верхнему краю через CSS
    st.markdown("""
        <style>
        [data-testid="stHorizontalBlock"] {
            align-items: flex-start !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. Создаем колонки. 
# Пропорции колонок
    col1, col2, col3 = st.columns([1.3, 0.8, 1.3], gap="medium")

    with col1:
        st.subheader("🌏 Глобальный мониторинг")
        # УМЕНЬШЕННАЯ ВЫСОТА ГЛОБУСА
        components.iframe("https://pulse.climate.copernicus.eu", height=500, scrolling=False)
        st.caption("Данные: Copernicus Climate Pulse")

    with col2:
        st.subheader("📈 Глобальный контекст")
        # Хайлайт 1: Глобальный рекорд
        st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #ffa500; margin-bottom: 15px;">
                <b style="color: #e67e22; font-size: 1.1rem;">📈 Рекордное потепление</b><br>
                <span style="font-size: 1.15rem; color: #1a1a1a;">
                    Согласно докладу Всемирной метеорологической организации с 1980-х годов, 
                    каждое последующее десятилетие было теплее, чем любое предыдущее десятилетие с 1850 года.
                </span>
            </div>
        """, unsafe_allow_html=True)

        # Хайлайт 2: Специфика Казахстана
        st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #2ecc71; margin-bottom: 15px;">
                <b style="color: #27ae60; font-size: 1.1rem;">🇰🇿 Климат Казахстана меняется быстрее</b><br>
                <span style="font-size: 1.15rem; color: #1a1a1a;">
                    Территория Казахстана, находящаяся в центре Евразийского континента и удаленная от океана на значительное расстояние, 
                    прогревается более значительными темпами, чем земной шар в среднем.
                </span>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:  
        st.subheader("📊 Аналитика климатических изменений")

        st.markdown("""
            <style>
            .analytics-vertical-wrapper {
                display: flex;
                flex-direction: column;
                gap: 20px;
                margin: 20px 0;
            }
            /* Контейнер для двух элементов в одной строке */
            .m-top-row {
                display: flex;
                flex-direction: row;
                gap: 20px;
                width: 100%;
            }
            .m-row-item {
                flex: 1; /* Растягивает элементы поровну */
                display: flex;
                flex-direction: column;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 8px;
                border-left: 6px solid #1a4fa3;
            }
            .m-label {
                color: #666;
                font-size: 0.9rem;
                font-weight: 500;
                margin-bottom: 5px;
            }
            .m-value {
                color: #1a4fa3;
                font-size: 2.0rem;
                font-weight: 850;
                line-height: 1;
            }
            .m-sub {
                font-size: 0.8rem;
                color: #888;
                margin-top: 5px;
            }
            .m-badge {
                display: inline-block;
                align-self: flex-start;
                padding: 4px 10px;
                border-radius: 5px;
                font-size: 0.75rem;
                font-weight: bold;
                margin-top: 10px;
                text-transform: uppercase;
            }
            .b-red { background: #fee2e2; color: #b91c1c; }
            .b-orange { background: #fef3c7; color: #d97706; }
            
            /* Адаптивность для мобильных устройств */
            @media (max-width: 768px) {
                .m-top-row { flex-direction: column; }
            }
            </style>

            <div class="analytics-vertical-wrapper">
                <div class="m-top-row">
                    <div class="m-row-item">
                        <div class="m-label">Темп потепления</div>
                        <div class="m-value">+0.40°С</div>
                        <div class="m-sub">за 10 лет (в среднем)</div>
                        <div class="m-badge b-red">↑ ВЫШЕ МИРОВОГО</div>
                    </div>                   
                    <div class="m-row-item">
                        <div class="m-label">Аномалия 2025</div>
                        <div class="m-value">+2.96 °С</div>
                        <div class="m-sub">от нормы 1961-1990</div>
                        <div class="m-badge b-red">РАНГ №1</div>
                    </div>
                </div>
                <div class="m-row-item">
                    <div class="m-label">Дефицит осадков</div>
                    <div class="m-value">-2.5 мм</div>
                    <div class="m-sub">критическое снижение влажности в июне и октябре</div>
                    <div class="m-badge b-orange">⚠ РИСК ЗАСУШЛИВОСТИ</div>
                </div>
            </div>
        """, unsafe_allow_html=True)


        # И плашка под ними
        st.info("💡 Наблюдается устойчивый тренд на ускорение прогрева территории республики.")


    # --- 1. ОБЩИЕ ДАННЫЕ ---
    years = list(range(1940, 2026))

    # Данные аномалий температуры
    temp_vals = [
        0.24, -0.33, -0.86, -1.05, 0.09, -1.28, -0.67, -0.52, 0.24, -1.18, -1.59, -0.47, -1.13, -0.19, -2.03, 0.04, 
        -0.92, -0.48, -0.61, -1.17, -1.58, 0.39, 0.76, 0.81, -0.96, 0.44, -0.26, -0.01, -0.51, -2.31, -0.40, 0.44, 
        -1.46, 0.27, -0.66, 0.86, -1.28, 0.25, 0.18, 0.04, -0.06, 0.86, 0.60, 1.76, -1.20, -0.40, -0.08, -0.32, 
        0.47, 0.79, 1.04, 0.90, 0.12, -1.01, -0.14, 1.41, -0.77, 1.26, 0.40, 1.07, 0.91, 0.96, 1.55, 0.35, 1.53, 
        1.08, 1.20, 1.46, 1.37, 0.62, 0.80, -0.04, 0.38, 1.89, 0.15, 1.64, 1.48, 1.30, 0.04, 1.50, 1.92, 1.58, 
        1.78, 2.58, 1.72, 2.96
    ]

    # Данные аномалий осадков (примерные, синхронизированные с твоими показателями)
    precip_vals = [
        5.2, -10.4, 15.1, -2.3, 8.7, -25.4, 12.0, -4.5, 30.1, -12.3, 
        -5.9, 14.7, -11.3, -0.19, -20.3, 10.4, -9.2, -14.8, 6.1, -11.7, 
        -15.8, 3.9, 17.6, 8.1, -19.6, 14.4, -2.6, -10.1, -5.1, -23.1, 
        14.0, 4.4, -14.6, 12.7, -6.6, 18.6, -12.8, 2.5, 11.8, 4.4, 
        -6.6, 8.6, 16.0, 7.6, -12.0, -14.0, -8.0, -13.2, 4.7, 7.9, 
        10.4, 9.0, 1.2, -10.1, -11.4, 14.1, -7.7, 12.6, 4.0, 10.7, 
        -9.1, 9.6, 15.5, 3.5, 15.3, -10.8, 12.0, -14.6, 13.7, 6.2, 
        8.0, -10.4, 3.8, 18.9, 1.5, -16.4, 14.8, 13.0, 0.4, -15.0, 
        9.2, 5.8, -17.8, -25.8, -17.2, -2.5
    ]

    df_climate = pd.DataFrame({
        'Год': years,
        'Температура': temp_vals,
        'Осадки': precip_vals
    })

    # --- 1. CSS ДЛЯ НАСТОЯЩИХ ХАЙЛАЙТОВ (СТИЛЬ ПЛАШЕК) ---
    st.markdown("""
        <style>
        /* Контейнер для плашек */
        .highlight-wrapper {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
        }
        /* Сама плашка как на скриншоте 19589a */
        .highlight-box {
            background-color: rgba(240, 242, 246, 0.5); /* Светлый нейтральный фон */
            border-radius: 10px;
            padding: 12px 18px;
            border-left: 4px solid #ccc;
        }
        .h-temp-box { border-left-color: #d32f2f; background-color: #fff5f5; } /* Легкий красный оттенок */
        .h-precip-box { border-left-color: #2e7d32; background-color: #f6fff6; } /* Легкий зеленый оттенок */
        
        .h-label {
            font-size: 0.7rem;
            font-weight: 700;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .h-content {
            font-size: 0.95rem;
            color: #31333F;
            line-height: 1.4;
        }
        .h-bold { font-weight: 800; color: #1a1a1a; }
        </style>
    """, unsafe_allow_html=True)

    # --- 2. УНИВЕРСАЛЬНАЯ ФУНКЦИЯ С ЛЕГЕНДОЙ И ХАЙЛАЙТАМИ ---
    def render_climate_section(title, description, column_name, colorscale, bar_colors, unit, highlights, h_style_class):
        st.markdown(f"### {title}")
        
        # --- ХАЙЛАЙТЫ ПЕРЕД ГРАФИКОМ ---
        st.markdown(f"""
            <div class="highlight-wrapper">
                <div class="highlight-box {h_style_class}">
                    <div class="h-label">Текущее состояние</div>
                    <div class="h-content">{highlights['current']}</div>
                </div>
                <div class="highlight-box {h_style_class}">
                    <div class="h-label">Многолетний тренд</div>
                    <div class="h-content">{highlights['trend']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.caption(description)
        
        # 1. Warming Stripes
        fig_stripes = px.imshow([df_climate[column_name]], x=df_climate['Год'], 
                                color_continuous_scale=colorscale, aspect="auto", color_continuous_midpoint=0)
        fig_stripes.update_layout(height=60, margin=dict(l=0, r=0, t=5, b=5), yaxis={'visible': False},
                                  xaxis=dict(showgrid=False, tickmode='linear', dtick=20),
                                  coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_stripes, use_container_width=True, config={'displayModeBar': False})
        
        # 2. Основной график с легендой
        fig_chart = go.Figure()
        colors = [bar_colors[0] if x > 0 else bar_colors[1] for x in df_climate[column_name]]
        
        # Столбцы (Аномалии)
        fig_chart.add_trace(go.Bar(
            x=df_climate['Год'], 
            y=df_climate[column_name], 
            marker_color=colors, 
            opacity=0.6, 
            name='Ежегодная аномалия' # Имя для легенды
        ))
        
        # Линия скользящего среднего (Тренд)
        df_climate[f'SMA_{column_name}'] = df_climate[column_name].rolling(window=10, min_periods=1, center=True).mean()
        fig_chart.add_trace(go.Scatter(
            x=df_climate['Год'], 
            y=df_climate[f'SMA_{column_name}'], 
            mode='lines', 
            line=dict(color='#222', width=2.5), 
            name='10-летнее среднее' # Имя для легенды
        ))

        fig_chart.update_layout(
            height=320, 
            margin=dict(l=0, r=0, t=10, b=10),
            # Настройка легенды
            showlegend=True, 
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#f0f0f0', dtick=20),
            yaxis=dict(title=f"Аномалия ({unit})", showgrid=True, gridcolor='#f0f0f0', zeroline=True, zerolinecolor='#ccc')
        )
        st.plotly_chart(fig_chart, use_container_width=True)

    # --- 3. ВЕРСТКА БЛОКА ---
    st.subheader("📈 Климат Казахстана")
    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        render_climate_section(
            "Температура воздуха",
            "Графическое представление аномалий температуры (отклонение от нормы).",
            "Температура", 'RdBu_r', ['#d32f2f', '#1f77b4'], "°C",
            {
                "current": "Средняя (1941-2025): 5,67 ºC. В 2025 году достигла <span class='h-bold'>8,4 ºC</span>.",
                "trend": "Повышение на <span class='h-bold'>0,40 ºC каждые 10 лет</span> за последние полвека."
            },
            "h-temp-box"
        )

    with col_r:
        render_climate_section(
            "Атмосферные осадки",
            "Анализ изменчивости осадков и трендов увлажнения.",
            "Осадки", 'BrBG', ['#2e7d32', '#8d6e63'], "мм",
            {
                "current": "Средняя норма: 320 мм. В 2025 году зафиксирован дефицит <span class='h-bold'>-2,5 мм</span>.",
                "trend": "Снижение уровня влажности на <span class='h-bold'>1,2% каждое десятилетие</span>."
            },
            "h-precip-box"
        )

    
    import streamlit as st
    import streamlit.components.v1 as components

    # --- ДАННЫЕ РЕЙТИНГА ---
    rank_data = [
        {"rank": 1, "year": 2025, "value": 2.96, "color": "#990000"},
        {"rank": 2, "year": 2023, "value": 2.58, "color": "#b30000"},
        {"rank": 3, "year": 2020, "value": 1.92, "color": "#d32f2f"},
        {"rank": 4, "year": 2013, "value": 1.89, "color": "#d32f2f"},
        {"rank": 5, "year": 2022, "value": 1.78, "color": "#e57373"},
        {"rank": 6, "year": 1983, "value": 1.76, "color": "#e57373"},
        {"rank": 7, "year": 2024, "value": 1.72, "color": "#ef9a9a"},
        {"rank": 8, "year": 2015, "value": 1.64, "color": "#ef9a9a"},
        {"rank": 9, "year": 2021, "value": 1.58, "color": "#ffcdd2"},
        {"rank": 10, "year": 2002, "value": 1.55, "color": "#ffcdd2"}
    ]



    st.markdown("### 🏆 Анализ температурных рекордов")

    # Создаем колонки
    col_info, col_chart, col_map = st.columns([1, 1, 1], gap="large")

    with col_info:
        # Текстовый хайлайт
        st.markdown("""
            <div style="background-color: #fff5f5; padding: 20px; border-radius: 12px; border-left: 6px solid #d32f2f; margin-top: 10px;">
                <h4 style="margin-top: 0; color: #d32f2f;">Беспрецедентный рост</h4>
                <p style="font-size: 1rem; line-height: 1.5;">
                    <span style="font-weight: 800; font-size: 1.2rem;">2025 год</span> официально признан самым жарким в истории наблюдений Казахстана.
                    Климат стал теплее обычного почти на <b>3 градуса</b> (+2,96°C).
                </p>
                <p style="font-size: 0.9rem; color: #666;">
                    Примечательно, что <b>9 из 10</b> самых теплых лет пришлись на XXI век, что подтверждает ускорение глобального потепления.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_chart:
        st.caption("Самые теплые годы в Казахстане (1941–2025)")
        
        # Генерация HTML для инфографики
        rows_html = ""
        max_val = 2.96
        for item in rank_data:
            width = (item["value"] / max_val) * 100
            rows_html += f"""
            <div style="display: flex; align-items: center; margin-bottom: 6px; height: 28px; font-family: sans-serif;">
                <div style="width: 25px; font-size: 11px; font-weight: bold; color: #888;">{item['rank']}</div>
                <div style="width: 45px; font-size: 12px; font-weight: 600; color: #333;">{item['year']}</div>
                <div style="flex-grow: 1; background-color: #f0f2f6; border-radius: 4px; height: 100%; position: relative;">
                    <div style="width: {width}%; background-color: {item['color']}; height: 100%; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; border-radius: 4px;">
                        <span style="color: white; font-size: 11px; font-weight: bold;">+{item['value']}°C</span>
                    </div>
                </div>
            </div>
            """
                # Отрисовка через iframe для стабильности
        components.html(f"""
            <div style="padding-top: 5px;">
                {rows_html}
            </div>
        """, height=350)

   
            
    with col_map:
        map_path = "temp1.gif"
        
        if os.path.exists(map_path):
            # Чтобы HTML увидел файл, он должен быть доступен (например, в папке со скриптом)
            # Но проще всего вывести через st.image(contents) как выше.
            # Если все же нужен HTML:
            import base64
            with open(map_path, "rb") as f:
                data_url = base64.b64encode(f.read()).decode("utf-8")
            
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="map gif" style="width:100%;">',
                unsafe_allow_html=True,
            )
            st.caption("Карта аномалий")
        
        
    st.divider()


    st.markdown("### 🏆 Анализ влажности")
    
    col_info2, col_chart2, col_map2 = st.columns([1, 1, 1], gap="large")
    
# --- ДАННЫЕ РЕЙТИНГА ОСАДКОВ (ЗАСУХА) ---
    # Гамма синхронизирована с оранжевыми оттенками карты аномалий
    rank_data_precip = [
        {"rank": 1, "year": 1944, "value": 73.5, "color": "#B85B28"}, # Насыщенный коричнево-оранжевый
        {"rank": 2, "year": 1975, "value": 77.0, "color": "#D47A3B"},
        {"rank": 3, "year": 1974, "value": 78.3, "color": "#E6914B"},
        {"rank": 4, "year": 1995, "value": 78.8, "color": "#F2A762"},
        {"rank": 5, "year": 1991, "value": 78.9, "color": "#F7B97D"},
        {"rank": 6, "year": 2008, "value": 81.6, "color": "#FACB96"},
        {"rank": 7, "year": 1955, "value": 82.4, "color": "#FBD9B0"},
        {"rank": 8, "year": 1936, "value": 82.6, "color": "#FDE5C7"},
        {"rank": 9, "year": 2020, "value": 85.2, "color": "#FEF0DE"},
        {"rank": 10, "year": 2021, "value": 85.5, "color": "#FFF8F0"}  # Самый светлый, почти песочный
    ]
    
 
    with col_info2:
            st.markdown("""
                <div style="background-color: #fdfaf5; padding: 20px; border-radius: 12px; border-left: 6px solid #8d6e63; margin-top: 0px;">
                    <h4 style="margin-top: 0; color: #5d4037;">Динамика увлажнения</h4>
                    <p style="font-size: 0.95rem; line-height: 1.4;">
                        <span style="font-weight: 800;">За последние 50 лет</span> наблюдается слабая тенденция к увеличению годовых сумм атмосферных осадков на 2,5 мм/10 лет, в основном за счет осадков весеннего сезона. 
                        <br><br>
                        Уменьшение осадков наблюдалось в центральных и южных регионах. Изменения максимальной продолжительности бездождных периодов с осадками менее 1 мм в сутки достигли 1–4 дней за десятилетие, как в сторону увеличения, так и в сторону уменьшения.
                    </p>
                </div>
            """, unsafe_allow_html=True)

        
    # 2. КОЛОНКА С ГРАФИКОМ
    with col_chart2:
        # Крупный заголовок как в верхнем блоке
        st.markdown("""
            <div style="font-size: 1.1rem; font-weight: 600; color: #555; margin-bottom: 15px; font-family: sans-serif;">
                Самые сухие годы в Казахстане <span style="font-weight: 400; font-size: 0.9rem; color: #888;">(1941–2025 гг.)</span>
            </div>
        """, unsafe_allow_html=True)
        
        rows_html = ""
        max_val_precip = 100 # База для процентов
        
        for item in rank_data_precip:
            width = (item["value"] / max_val_precip) * 100
            rows_html += f"""
            <div style="display: flex; align-items: center; margin-bottom: 6px; height: 26px; font-family: sans-serif;">
                <div style="width: 25px; font-size: 11px; font-weight: bold; color: #888;">{item['rank']}</div>
                <div style="width: 45px; font-size: 12px; font-weight: 600; color: #333;">{item['year']}</div>
                <div style="flex-grow: 1; background-color: #f0f2f6; border-radius: 4px; height: 100%; position: relative;">
                    <div style="width: {width}%; background-color: {item['color']}; height: 100%; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; border-radius: 4px;">
                        <span style="color: white; font-size: 11px; font-weight: bold;">{item['value']}%</span>
                    </div>
                </div>
            </div>
            """
        
        components.html(f"<div style='margin-top: 5px;'>{rows_html}</div>", height=340)
              
        
    with col_map2:
        map_path = "Precipitation.gif"
        
        if os.path.exists(map_path):
            # Чтобы HTML увидел файл, он должен быть доступен (например, в папке со скриптом)
            # Но проще всего вывести через st.image(contents) как выше.
            # Если все же нужен HTML:
            import base64
            with open(map_path, "rb") as f:
                data_url = base64.b64encode(f.read()).decode("utf-8")
            
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="map gif" style="width:100%;">',
                unsafe_allow_html=True,
            )
            st.caption("Карта аномалий")
        
            
    st.divider()

    # Основной заголовок секции
    st.header("🔮 Изменение климата в будущем")

    st.markdown("""
    Изменение климата — это не просто сухие цифры прогнозов, а вызов, который определит облик нашей страны в ближайшие десятилетия. 
    Ниже представлены инструменты и данные, позволяющие заглянуть в будущее Казахстана.
    """)

    # Создаем две колонки: левая для карты, правая для текста
    col_map, col_text = st.columns([1.5, 1])

    with col_map:
        st.subheader("🗺️ Интерактивная карта прогнозов")
        # Ссылка на инструмент Потсдамского института
        pik_url = "http://10.0.2.121:8080/forecast"
        
        # Отображение карты через iframe
        st.components.v1.iframe(pik_url, height=800, scrolling=True)
        
        st.caption("Данные предоставлены Потсдамским институтом изучения климатических изменений (PIK).")

    with col_text:
        # 1. Сценарии SSP
        st.markdown("### 🌍 Выбор будущего (SSP)")
        st.info("""
        **Будущее не предопределено.** Оно зависит от пути, который выберет человечество (Shared Socioeconomic Pathways):
        * **🌱 Зеленый путь (SSP1):** Быстрый переход на ВИЭ, резкое сокращение CO2.
        * **⚖️ Средний путь (SSP2):** Развитие по текущему вектору.
        * **🏭 Интенсивный путь (SSP5):** Активное использование угля и нефти.
        """)

        # 2. Модели CMIP6
        st.markdown("### 💻 Математика климата (CMIP6)")
        st.write("""
        Мы используем **CMIP6** — «золотой стандарт» науки. Это сложнейшие модели ($GCM$), 
        которые имитируют движение атмосферы и океанов на суперкомпьютерах.
        """)

        # 3. Специфика Казахстана
        st.markdown("### 🇰🇿 Масштаб Казахстана")
        st.warning("""
        **Важно:** Казахстан прогревается в **1.5–2 раза быстрее**, чем планета в среднем. 
        Мы применяем «даунскейлинг», чтобы перенести глобальные расчеты на наш рельеф.
        """)
        
        st.markdown("### 📉 Новая реальность к 2100 году")
        st.write("""
        Где «волны жары» станут нормой и как изменится зимний режим?
        В каких регионах усилится засуха, а где возможны паводки из-за таяния снегов?
        """)
        
        st.success("Эти данные помогают планировать развитие городов и сельского хозяйства Казахстана уже сегодня.")
        


    st.markdown("---")
    st.subheader("📈 Климат областей")
    import streamlit as st
    import pandas as pd
    import streamlit.components.v1 as components



    # --- 1. БАЗА ДАННЫХ ВСЕХ 17 ОБЛАСТЕЙ ---
    # Вы можете дополнять этот словарь данными для каждой области
    ALL_REGIONS_DATABASE = {
        "Северо-Казахстанская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. Область является критически важным аграрным регионом, где продуктивность сельского хозяйства напрямую зависит от режима увлажнения и температурного режима в период вегетации. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3,6%",
            "temp_2025": 5.1,
            "norm_temp": 1.1,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "trend_temp": "+0,36 °С",
            "trend_precip": "+6,1 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 2010, "val": 239.04, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 1975, "val": 248.90, "col": "#2e7d32"},
                {"year": 1965, "val": 253.16, "col": "#4caf50"},
                {"year": 1951, "val": 255.49, "col": "#81c784"},
                {"year": 1991, "val": 260.34, "col": "#a5d6a7"}
            ],
            "risks": [
            {"title": "🔥 Экстремальные температуры", "text": "Рост 0.36 °С за 10 лет. 2025 год — рекорд (+5.09 °С).", "level": 95, "color": "#d32f2f"},
            {"title": "🌾 Засухи и дефицит влаги", "text": "Снижение осадков в июне и октябре. Угроза урожаю.", "level": 70, "color": "#f57c00"},
            {"title": "🌊 Весенние паводки", "text": "Рост осадков весной (+6.1 мм/10 лет) провоцирует наводнения.", "level": 45, "color": "#1976d2"}
            ],
            "final_conclusion": "На территории СКО наблюдается интенсивное потепление, опережающее среднемировые темпы. 2025 год официально зафиксирован как ранг №1 в списке самых теплых лет. Несмотря на общую слабую тенденцию к увеличению годовых осадков (+11 мм/10 лет), сохраняется риск «аграрных засух» из-за перераспределения влаги: её становится больше весной, но меньше в ключевые летние и осенние месяцы. Это требует пересмотра сроков посевных работ и внедрения технологий сохранения весенней влаги в почве.",            
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -15.5, "sp": 2.5, "su": 18.2, "au": 2.1, "y": 1.8},
            "t_anom_2025": {"w": 5.98, "sp": 4.64, "su": 0.5, "au": 2.5, "y": 3.28},
            "p_norm": {"w": 47.3, "sp": 65.6, "su": 152.6, "au": 87.1, "y": 352.6},
            "p_anom_2025": {"w": 11.1, "sp": 51.2, "su": 22.5, "au": 1.6, "y": 87.3}
        },
        "Акмолинская область": {
            "geo_text": "Акмолинская область расположена в центральной части Северного Казахстана. Климат региона резко континентальный и засушливый, с суровыми малоснежными зимами и коротким, но жарким летом. Территория находится в зоне активного земледелия, где ключевым фактором является наличие влаги в почве перед началом вегетации. ",
            "stations": 8,
            "area": "146 219 км²",
            "area_perc": "5.4%",
            "temp_2025": 5.4,
            "norm_temp": 1.1,
            "anom_2025": 3.31,
            "precip_2025": 439.8,
            "prec_norm": "121.4%",
            "temp_extreme": {"max": "+23.6°С (июль 1998)", "min": "-30.2°С (январь 1969)"},
            "trend_temp": "+0,37 °С",
            "trend_precip": "+5,1 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",
            "top_years": [
                {"year": 2025, "val": 5.4, "col": "#990000"},
                {"year": 2023, "val": 4.7, "col": "#b30000"},
                {"year": 2020, "val": 4.7, "col": "#d32f2f"},
                {"year": 1983, "val": 4.1, "col": "#e57373"},
                {"year": 2002, "val": 3.9, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1951, "val": 206.65, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 1955, "val": 214.91, "col": "#2e7d32"},
                {"year": 1998, "val": 222.1, "col": "#4caf50"},
                {"year": 1697, "val": 228.11, "col": "#81c784"},
                {"year": 1991, "val": 228.89, "col": "#a5d6a7"}
            ], 
            "risks": [
            {"title": "🔥 Экстремальное потепление ", "text": "Повышение на 0,37 °С каждые 10 лет. 2025 год — самый теплый за всю историю.", "level": 95, "color": "#d32f2f"},
            {"title": "🌾 Аграрные засухи ", "text": "Снижение осадков в апреле, мае и июне. Дефицит влаги именно в период посевной и активного роста культур создает прямую угрозу урожайности.", "level": 70, "color": "#f57c00"},
            {"title": "🌊 Переувлажнение в межсезонье ", "text": "Рост осадков весной (+6.1 мм/10 лет) провоцирует наводнения.", "level": 45, "color": "#1976d2"}
            ],
            "final_conclusion": "Акмолинская область входит в число регионов с наиболее выраженным темпом потепления. Характерной чертой является «сезонный дисбаланс» осадков: их количество растет зимой, но сокращается в критически важные для сельского хозяйства весенне-летние месяцы. Климатическая адаптация региона должна быть направлена на удержание зимней влаги и внедрение засухоустойчивых технологий возделывания почв.",            
            "zones": [
            {
                "title": "🌳 Лесостепная (~30%)",
                "desc": "Северная часть (район Борового, Кокшетау). Обилие озер и березовых лесов.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~70%)",
                "desc": "Центральная и южная части. Открытые равнины, зона интенсивного зернового хозяйства.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -12.2, "sp": 6.2, "su": 21.1, "au": 5.7, "y": 5.4},
            "t_anom_2025": {"w": 5.41, "sp": 5.03, "su": 0.62, "au": 2.48, "y": 3.31},
            "p_norm": {"w": 47.5, "sp": 69.2, "su": 130.1, "au": 78.2, "y": 325.0},
            "p_anom_2025": {"w": 19.9, "sp": 15.5, "su": 24.4, "au": 4.2, "y": 69.5}           
        },
        "Западно-Казахстанская область": {
            "geo_text": "Западно-Казахстанская область расположена на северо-западе страны, в пределах Прикаспийской низменности и Предуральского плато. Климат региона резко континентальный, с выраженным дефицитом влаги в летний период. Особенностью региона является крайне интенсивное весеннее потепление и высокая изменчивость увлажнения.",
            "stations": 8,
            "area": "151 339 км²",
            "area_perc": "5.6%",
            "temp_2025": 9.9,
            "norm_temp": 1.1,            
            "anom_2025": 2.9,
            "precip_2025": 265.5,
            "prec_norm": "94.4%",
            "temp_extreme": {"max": "+29.1°С (июль 2010)", "min": "-25.8°С (февраль 1954)"},
            "trend_temp": "+0,59 °С",
            "trend_precip": "-0,03 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",
            "top_years": [
                {"year": 2025, "val": 9.9, "col": "#990000"},
                {"year": 2023, "val": 9.3, "col": "#b30000"},
                {"year": 1995, "val": 9.0, "col": "#d32f2f"},
                {"year": 2020, "val": 8.9, "col": "#e57373"},
                {"year": 2021, "val": 8.9, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1996, "val": 158.99, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 1949, "val": 162.44, "col": "#2e7d32"},
                {"year": 1972, "val": 167.91, "col": "#4caf50"},
                {"year": 1955, "val": 172.61, "col": "#81c784"},
                {"year": 2014, "val": 175.39, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🔥 Интенсивное потепление", "text": "Повышение на 0,59 °С каждые 10 лет . 2025 год — самый теплый за всю историю (Ранг №1). Наиболее выраженный рост температур наблюдается в марте (+1,09 °С/10 лет).", "level": 95, "color": "#d32f2f"},
            {"title": "🌾 Сезонный дефицит влаги и засухи ", "text": "Годовое количество осадков стабильно (−0,03 мм/10 лет), но происходит опасное перераспределение. Уменьшение осадков летом (−3,17 мм/10 лет) и зимой (−1,43 мм/10 лет). Особенно критично сокращение в августе (−3,32 мм/10 лет).", "level": 70, "color": "#f57c00"},
            {"title": "❄️ Риск раннего снеготаяния ", "text": "Рост весенних осадков (+5,23 мм/10 лет) на фоне резкого потепления в марте. Повышает вероятность интенсивных весенних половодий на реках региона.", "level": 45, "color": "#1976d2"}
            ],
            "final_conclusion": "В Западно-Казахстанской области наблюдается «сдвиг» климатических сезонов: весна становится более теплой и влажной, в то время как лето и зима аридизируются (становятся суше). 2025 год подтвердил статус региона как зоны активного температурного роста (+3,5 °С к календарной норме). Главным вызовом для сельского хозяйства является усиление дефицита влаги в августе и сентябре, что требует адаптации сроков уборки и управления водными ресурсами.",            
            "zones": [
            {
                "title": "🌾 Степная (~40%)",
                "desc": "Обводненная северная часть (бассейн реки Урал).",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🏜️ Полупустынная (~60%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -10.4, "sp": 7.0, "su": 22.1, "au": 6.6, "y": 6.3},
            "t_anom_2025": {"w": 4.7, "sp": 4.1, "su": 1.2, "au": 3.8, "y": 3.5},
            "p_norm": {"w": 65.5, "sp": 57.9, "su": 79.5, "au": 78.4, "y": 281.3},
            "p_anom_2025": {"w": -21.8, "sp": 3.5, "su": -3.0, "au": -2.8, "y": -15.8}   
        },
        "Атырауская область": {
            "geo_text": "Атырауская область расположена в Прикаспийской низменности, в зоне пустынь и полупустынь. Климат региона резко континентальный и крайне засушливый. Особенностью области является близость Каспийского моря, которое оказывает влияние на влажность воздуха, однако общая тенденция потепления ведет к усилению аридности (сухости) в летний период.",
            "stations": 3,
            "area": "118 631 км²",
            "area_perc": "4.4%",
            "temp_2025": 12.0,
            "norm_temp": 1.1,            
            "anom_2025": 2.9,
            "precip_2025": 146.7,
            "prec_norm": "97.6%",
            "temp_extreme": {"max": "+29.4°С (июль 2018)", "min": "-21.4°С (январь 1954)"},
            "trend_temp": "+0,54 °С",
            "trend_precip": "+4,73 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",            
            "top_years": [
                {"year": 2023, "val": 12.1, "col": "#990000"},
                {"year": 2025, "val": 12.0, "col": "#b30000"},
                {"year": 2021, "val": 11.7, "col": "#d32f2f"},
                {"year": 2024, "val": 11.5, "col": "#e57373"},
                {"year": 2022, "val": 11.4, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1972, "val": 69.90, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 1984, "val": 70.63, "col": "#2e7d32"},
                {"year": 2018, "val": 86.33, "col": "#4caf50"},
                {"year": 1968, "val": 88.6, "col": "#81c784"},
                {"year": 2020, "val": 96.17, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🌡️ Экстремальное весеннее потепление ", "text": "Повышение температуры на 0,54 °С каждые 10 лет. Наиболее интенсивный рост температур зафиксирован в феврале и марте (+0,96 °С/10 лет). Сокращение периода залегания снежного покрова и сверхраннее наступление весенних процессов.", "level": 95, "color": "#d32f2f"},
            {"title": "🌾 Летняя засуха и дефицит влаги ", "text": "Несмотря на общий рост годовых осад (+4,73 мм/10 лет), наблюдается устойчивое сокращение летних дождей (−2,59 мм/10 лет). Наибольшее снижение осадков в августе (−1,14 мм/10 лет). Это ведет к иссушению почв и деградации растительности в самый жаркий период.", "level": 90, "color": "#d32f2f"},
            {"title": "🌊 Сезонный дисбаланс увлажнения", "text": "Рост осадков происходит исключительно зимой и весной (+5,61 мм/10 лет в весенний период). Увеличение весенней влаги при росте летних температур усиливает испаряемость, что не компенсирует летний дефицит воды для пастбищ.", "level": 70, "color": "#f57c00"}
            ],
            "final_conclusion": "Атырауская область демонстрирует классический сценарий опустынивания: температуры растут во все месяцы года (особенно в феврале-марте), а осадки перераспределяются. Год становится более влажным зимой и весной, но более сухим летом и осенью. 2025 год подтвердил статус региона как зоны температурных рекордов (+12,0 °С). Главный вызов экстремальная жара в июле (до +29,4 °С в среднем за месяц) на фоне дефицита летних осадков.",            
            "zones": [
            {
                "title": "🏜️ Полупустынная (~20%)",
                "desc": "Северные окраины области, полынно-злаковая растительность.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🏜️🔥 Пустынная (~80%)",
                "desc": "Большая часть области, Прикаспийская низменность. Солончаки и пески.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -6.3, "sp": 9.7, "su": 24.0, "au": 9.0, "y": 9.1},
            "t_anom_2025": {"w": 3.3, "sp": 1.2, "su": 3.5, "au": 1.6, "y": 3.0},
            "p_norm": {"w": 62.2, "sp": 92.7, "su": 128.0, "au": 111.2, "y": 394.1},
            "p_anom_2025": {"w": -0.6, "sp": -9.6, "su": 21.0, "au": -17.8, "y": -3.5}   
        },
        "Мангистауская область": {
            "geo_text": "Мангистауская область — это регион с крайне суровыми пустынными условиями. Расположенный на восточном побережье Каспийского моря, он обладает наиболее аридным (засушливым) климатом в Казахстане. Ограниченность водных ресурсов и зависимость от Каспия делают регион крайне уязвимым к наблюдаемым изменениям климата. ",
            "stations": 1,
            "area": "165 642 км²",
            "area_perc": "6.1%",
            "temp_2025": 6.7,
            "norm_temp": 1.1,            
            "anom_2025": 2.1,
            "precip_2025": 118.5,
            "prec_norm": "83.1%",
            "temp_extreme": {"max": "+29.7°С (июль 2018)", "min": "-11.6°С (январь 1954)"},
            "trend_temp": "+0,59 °С",
            "trend_precip": "-5,8 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",            
            "top_years": [
                {"year": 2023, "val": 14.3, "col": "#990000"},
                {"year": 2024, "val": 14.1, "col": "#b30000"},
                {"year": 2022, "val": 14.0, "col": "#d32f2f"},
                {"year": 2025, "val": 13.9, "col": "#e57373"},
                {"year": 2004, "val": 13.8, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 2021, "val": 42.60, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 1942, "val": 54.00, "col": "#2e7d32"},
                {"year": 1949, "val": 56.00, "col": "#4caf50"},
                {"year": 1994, "val": 69.60, "col": "#81c784"},
                {"year": 1986, "val": 70.70, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🏜️ Интенсивное опустынивание ", "text": "Уменьшение годовых осадков на 5,8 мм каждые 10 лет. Сокращение происходит в самые важные периоды — весной (−3,62 мм/10 лет) и летом (−2,28 мм/10 лет). В мае и апреле зафиксировано наибольшее падение увлажнения, что ведет к уничтожению естественного пастбищного покрова.", "level": 95, "color": "#d32f2f"},
            {"title": "☀️ Тепловые волны ", "text": "Максимальная среднемесячная температура июля достигла +29,7 °С. Повышение нагрузки на энергетические системы и системы опреснения воды, рост рисков для здоровья населения.", "level": 70, "color": "#f57c00"},
            {"title": "❄️ Экстремальный рост зимне-весенних температур ", "text": "Потепление на 0,59 °С за десятилетие. Наибольший рост температур отмечается в феврале (+0,76 °С/10 лет). Сверхраннее наступление жары при отсутствии весенних дождей усиливает испарение скудных запасов влаги. ", "level": 70, "color": "#f57c00"}
            ],
            "final_conclusion": "Мангистауская область находится в состоянии климатического стресса. В отличие от других регионов, здесь отрицательный тренд осадков охватывает три сезона из четырех (весна, лето, осень). Рост осадков наблюдается только зимой (+1,37 мм/10 лет), что не компенсирует их катастрофическую нехватку в теплый период года. 2025 год подтвердил долгосрочный тренд: область становится всё более жаркой и сухой, что требует немедленных мер по адаптации водного хозяйства.",            
            "zones": [
            {
                "title": "🌊 Морская прибрежная (~15%)",
                "desc": "Узкая полоса вдоль Каспия. Относительно мягкая зима и высокая влажность воздуха.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🏜️☀️ Экстремально-пустынная (~85%)",
                "desc": "Внутренние плато (Устюрт) и впадины. Зона жесточайшего дефицита влаги.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -0.9, "sp": 11.0, "su": 24.4, "au": 12.7, "y": 11.8},
            "t_anom_2025": {"w": 1.9, "sp": 2.3, "su": 1.8, "au": 2.4, "y": 2.1},
            "p_norm": {"w": 24.0, "sp": 46.7, "su": 34.6, "au": 37.3, "y": 142.6},
            "p_anom_2025": {"w": 10.8, "sp": 5.4, "su": -24.4, "au": -20.9, "y": -24.1} 
        },
        "Актюбинская область": {
            "geo_text": "Актюбинская область — обширный регион, объединяющий черты степной, полупустынной и пустынной зон. Климат резко континентальный, с суровой зимой и жарким летом. Регион является важным промышленным и сельскохозяйственным узлом, где изменение режима осадков напрямую влияет на продуктивность пастбищ и урожайность зерновых культур. ",
            "stations": 12,
            "area": "300 629 км²",
            "area_perc": "11.0%",
            "temp_2025": 8.5,
            "norm_temp": 1.1,            
            "anom_2025": 3.2,
            "precip_2025": 258.8,
            "prec_norm": "98.2%",
            "temp_extreme": {"max": "+27.5°С (июль 1984)", "min": "-25.2°С (февраль 1969)"},
            "trend_temp": "+0,50 °С",
            "trend_precip": "-1,46 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",
            "top_years": [
                {"year": 2025, "val": 8.5, "col": "#990000"},
                {"year": 2023, "val": 8.2, "col": "#b30000"},
                {"year": 2020, "val": 7.5, "col": "#d32f2f"},
                {"year": 2013, "val": 7.5, "col": "#e57373"},
                {"year": 2021, "val": 7.4, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1944, "val": 143.07, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 2018, "val": 165.43, "col": "#2e7d32"},
                {"year": 1955, "val": 165.47, "col": "#4caf50"},
                {"year": 1951, "val": 166.32, "col": "#81c784"},
                {"year": 2012, "val": 166.76, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🌡️ Интенсивное весеннее потепление", "text": "Повышение на 0,50 °С каждые 10 лет. Наиболее резкий рост температур зафиксирован в марте (+1,12 °С/10 лет). Сверхбыстрое снеготаяние и раннее иссушение верхнего слоя почвы.", "level": 95, "color": "#d32f2f"},
            {"title": "🌾 Осенне-летняя аридизация ", "text": "Устойчивое снижение осадков летом (−1,2 мм/10 лет) и особенно осенью (−3,2 мм/10 лет). Сокращение влаги в июне и октябре ведет к дефициту влагозарядки почвы перед зимой и плохим условиям для вегетации поздних культур.", "level": 70, "color": "#f57c00"},
            {"title": "🌊 Изменение структуры увлажнения ", "text": "Рост осадков наблюдается только весной (+2,74 мм/10 лет), преимущественно в марте. Общий годовой тренд отрицательный (−1,46 мм/10 лет), так как весенний прирост не компенсирует летние и осенние потери.", "level": 45, "color": "#1976d2"}
            ],
            "final_conclusion": "Актюбинская область сталкивается с двойным вызовом: быстрым ростом температур и снижением годовых сумм осадков. 2025 год продемонстрировал значительный температурный скачок (на 3 °С выше исторической нормы). Основной риск для региона заключается в сдвиге влаги на раннюю весну, что при экстремально жарком лете приводит к быстрому опустыниванию южных и центральных районов области.",            
            "zones": [
            {
                "title": "🌾 Степная (~35%)",
                "desc": "Северная часть. Ковыльные степи, более мягкое лето.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Полупустынная (~65%)",
                "desc": "Центр и Юг. Полынные степи, переход к пескам Шалкара.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -12.3, "sp": 5.9, "su": 22.1, "au": 5.7, "y": 5.3},
            "t_anom_2025": {"w": 4.7, "sp": 4.4, "su": 0.8, "au": 3.5, "y": 3.2},
            "p_norm": {"w": 59.5, "sp": 64.1, "su": 67.8, "au": 72.2, "y": 263.6},
            "p_anom_2025": {"w": -0.1, "sp": 5.2, "su": 11.8, "au": -32.3, "y": -4.8} 
        },
        "Область Ұлытау": {
            "geo_text": "Область Ұлытау характеризуется резко континентальным, крайне засушливым климатом. Регион расположен в зоне полупустынь и пустынь Центрального Казахстана. Географическая удаленность от океанов и открытость северным ветрам обуславливают экстремальные перепады температур: от суровых морозов зимой до изнуряющей жары летом. ",
            "stations": 3,
            "area": "188 936 км²",
            "area_perc": "6.9%",
            "temp_2025": 8.1,
            "norm_temp": 1.1,            
            "anom_2025": 3.7,
            "precip_2025": 153.8,
            "prec_norm": "71.3%",
            "temp_extreme": {"max": "+26.4°С (июль 2023)", "min": "-27.9°С (январь 1969)"},
            "trend_temp": "+0,41 °С",
            "trend_precip": "+0,67 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",            
            "top_years": [
                {"year": 2025, "val": 8.1, "col": "#990000"},
                {"year": 2023, "val": 7.5, "col": "#b30000"},
                {"year": 2013, "val": 6.8, "col": "#d32f2f"},
                {"year": 1983, "val": 6.6, "col": "#e57373"},
                {"year": 2022, "val": 6.5, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1944, "val": 110.5, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 1936, "val": 117.6, "col": "#2e7d32"},
                {"year": 1995, "val": 118.25, "col": "#4caf50"},
                {"year": 1951, "val": 121.17, "col": "#81c784"},
                {"year": 1991, "val": 123.87, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "☀️ Сверхбыстрое весеннее потепление ", "text": "Рост температуры в марте на 1,36 °С каждые 10 лет. Это самый высокий показатель среди всех регионов. Стремительный переход от зимы к лету («взрывная весна»), что ведет к быстрому испарению талых вод и иссушению пастбищ. ", "level": 95, "color": "#d32f2f"},
            {"title": "🏜️ Дефицит увлажнения ", "text": "Хотя годовой тренд осадков слабоположительный (+0,67 мм/10 лет), 2025 год показал жесткий дефицит влаги (лишь 71% нормы).Уменьшение осадков в январе (−1,4 мм/10 лет) и осенью (−0,52 мм/10 лет) на фоне экстремальной жары усиливает аридность региона.", "level": 70, "color": "#f57c00"},
            {"title": "☀️ Летний тепловой стресс ", "text": "Максимальная среднемесячная температура июля достигла +26,4 °С (в 2023 г.). Рост пожароопасности в степных и полупустынных районах.", "level": 70, "color": "#f57c00"}
            ],
            "final_conclusion": "Область Ұлытау находится в эпицентре температурных изменений Казахстана. Аномалия 2025 года (+3,7 °С) является одной из самых высоких в стране. Главная климатическая особенность — феноменальный рост мартовских температур, который полностью меняет гидрологический режим начала года. Увеличение осадков в теплый период (лето: +1,84 мм/10 лет) лишь частично компенсирует зимне-осеннее иссушение, сохраняя высокий риск опустынивания.",            
            "zones": [
            {
                "title": "🏜️ Полупустынная (~40%)",
                "desc": "Северная часть мелкосопочника.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🏜️☀️ Пустынная (~60%)",
                "desc": "Юг, переход в пустыню Бетпак-Дала.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -13.7, "sp": 5.3, "su": 21.5, "au": 4.6, "y": 4.4},
            "t_anom_2025": {"w": 4.0, "sp": 4.2, "su": 1.8, "au": 3.3, "y": 3.7},
            "p_norm": {"w": 52.6, "sp": 59.4, "su": 53.9, "au": 49.8, "y": 215.7},
            "p_anom_2025": {"w": -16.0, "sp": -23.5, "su": -9.9, "au": -23.9, "y": -61.9}     
        },
        "Восточно-Казахстанская область": {
            "geo_text": "Восточно-Казахстанская область отличается сложным рельефом, сочетающим высокогорья Алтая и обширные межгорные котловины. Это обуславливает высокую пестроту климата. Регион является «водной башней» страны, и изменение режима осадков здесь напрямую влияет на гидрологический режим крупнейших рек (Иртыш) и состояние ледников. ",
            "stations": 9,
            "area": "97 859 км²",
            "area_perc": "3.6%",
            "temp_2025": 4.9,
            "norm_temp": 1.1,            
            "anom_2025": 2.2,
            "precip_2025": 163.9,
            "prec_norm": "117.7%",
            "temp_extreme": {"max": "+23.7°С (июль 1974)", "min": "-28.4°С (январь 1969)"},
            "trend_temp": "+0,33 °С",
            "trend_precip": "+6,7 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",            
            "top_years": [
                {"year": 2023, "val": 5.2, "col": "#990000"},
                {"year": 2020, "val": 4.9, "col": "#b30000"},
                {"year": 2025, "val": 4.9, "col": "#d32f2f"},
                {"year": 2015, "val": 4.8, "col": "#e57373"},
                {"year": 2024, "val": 3.8, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1974, "val": 256.38, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 2008, "val": 263.84, "col": "#2e7d32"},
                {"year": 1997, "val": 277.4, "col": "#4caf50"},
                {"year": 1962, "val": 285.4, "col": "#81c784"},
                {"year": 1955, "val": 294.28, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🔥 «Взрывное» весеннее потепление", "text": "Рост температуры в марте на 1,17 °С каждые 10 лет. Стремительное снеготаяние в предгорьях Алтая, что при одновременном росте мартовских осадков резко повышает риски разрушительных паводков.", "level": 95, "color": "#d32f2f"},
            {"title": "🌊 Изменение структуры увлажнения", "text": "Положительный тренд осадков (+6,7 мм/10 лет) за счет зимы и весны. Наибольший рост зафиксирован в марте (+3,7 мм/10 лет). Увеличение снежности зим и влажности весны на фоне дефицита влаги в мае (−2,7 мм/10 лет).", "level": 70, "color": "#f57c00"},
            {"title": "🌾 Аграрные риски мая", "text": "Единственный месяц с существенным снижением осадков — май (−2,7 мм/10 лет). Иссушение почвы в период посевных работ, что критично для растениеводства в восточных районах.", "level": 70, "color": "#f57c00"}
            ],
            "final_conclusion": "ВКО демонстрирует тренд на «смягчение» зим и увлажнение начала года. 2025 год подтвердил общую тенденцию потепления (аномалия +2,2 °С). Единственный месяц с небольшим отрицательным температурным трендом — сентябрь (−0,03 °С/10 лет), что может способствовать более длительному периоду уборки урожая. Однако быстрый рост температур в марте (+1,17 °С) в сочетании с ростом осадков требует усиленного мониторинга паводковой ситуации в горных районах.",            
            "zones": [
            {
                "title": "🏔️🌲 Горно-лесная (~60%)",
                "desc": "Алтайские горы, хвойные леса, высокая влажность..",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная / Сухостепная(~40%)",
                "desc": "Предгорья и равнины (Прииртышье).",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -15.6, "sp": 3.6, "su": 19.1, "au": 3.7, "y": 2.7},
            "t_anom_2025": {"w": 3.1, "sp": 3.4, "su": 1.5, "au": 0.7, "y": 2.2},
            "p_norm": {"w": 62.2, "sp": 92.7, "su": 128.0, "au": 111.2, "y": 394.1},
            "p_anom_2025": {"w": 10.5, "sp": 9.3, "su": 14.5, "au": 29.6, "y": 69.9}    
        },
        "Область Абай": {
            "geo_text": "Область Абай расположена в восточной части Казахстана. Рельеф региона разнообразен: от равнинных степей до мелкосопочника и горных хребтов. Климат резко континентальный. Регион подвержен влиянию как сибирских антициклонов зимой, так и жарких воздушных масс из Центральной Азии летом, что создает высокую амплитуду температур. ",
            "stations": 11,
            "area": "185 500 км²",
            "area_perc": "6.8%",
            "temp_2025": 6.1,
            "norm_temp": 1.1,            
            "anom_2025": 2.5,
            "precip_2025": 311.4,
            "prec_norm": "108.4%",
            "temp_extreme": {"max": "+24.3°С (июль 1974)", "min": "-27.7°С (январь 1969)"},
            "trend_temp": "+0,32 °С",
            "trend_precip": "+6,0 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",          
            "top_years": [
                {"year": 2025, "val": 6.1, "col": "#990000"},
                {"year": 2023, "val": 6.0, "col": "#b30000"},
                {"year": 2007, "val": 5.7, "col": "#d32f2f"},
                {"year": 2002, "val": 5.7, "col": "#e57373"},
                {"year": 2024, "val": 5.6, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1974, "val": 168.25, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 2008, "val": 191.58, "col": "#2e7d32"},
                {"year": 1991, "val": 208.73, "col": "#4caf50"},
                {"year": 1997, "val": 212.46, "col": "#81c784"},
                {"year": 1982, "val": 214.34, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🌡️ Стабильное потепление ", "text": "Повышение температуры на 0,32 °С каждые 10 лет. Наиболее активный рост наблюдается в апреле (+0,74 °С/10 лет), что ускоряет сход снежного покрова.Сентябрь — единственный месяц с «замиранием» потепления (тренд −0,01 °С/10 лет).", "level": 70, "color": "#f57c00"},
            {"title": "🌊 Рост паводковой нагрузки", "text": "Наибольший рост месячных осадков зафиксирован в марте (+3,1 мм/10 лет). Сочетание потепления и роста осадков в марте повышает вероятность интенсивных весенних паводков на реках бассейна Иртыша.", "level": 70, "color": "#f57c00"},
            {"title": "💧 Весенний дефицит влаги ", "text": "Уменьшение осадков в мае (−1,8 мм/10 лет) и апреле (−1,0 мм/10 лет). Несмотря на общий рост годовых осадков (+6,0 мм/10 лет), иссушение в пик посевной (май) может негативно сказываться на ранних этапах вегетации.", "level": 45, "color": "#1976d2"}
            ],
            "final_conclusion": "Климат области Абай становится более влажным: рост осадков наблюдается практически во все сезоны, особенно летом (+3,0 мм/10 лет). 2025 год подтвердил статус региона как зоны умеренных, но устойчивых изменений (+2,5 °С к норме). Положительным фактором является рост осадков в августе (+2,3 мм/10 лет), что смягчает летнюю засушливость, однако дефицит осадков в мае остается главным вызовом для аграрного сектора.",            
            "zones": [
            {
                "title": "🌾 Степная (~45%)",
                "desc": "Северная часть и мелкосопочник.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🏜️ Полупустынная (~55%)",
                "desc": "Юг, район озера Балхаш и Зайсанская впадина.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -14.3, "sp": 4.5, "su": 20.1, "au": 4.1, "y": 3.6},
            "t_anom_2025": {"w": 3.3, "sp": 3.9, "su": 2.0, "au": 0.8, "y": 2.5},
            "p_norm": {"w": 57.4, "sp": 68.1, "su": 86.6, "au": 75.2, "y": 287.3},
            "p_anom_2025": {"w": 9.2, "sp": -4.4, "su": -1.4, "au": 22.9, "y": 24.1}      
        },
        "Костанайская область": {
            "geo_text": "Костанайская область расположена в северной части Казахстана, преимущественно в степной и лесостепной зонах. Климат региона резко континентальный с выраженными сезонами. Благодаря равнинному рельефу территория открыта как для арктических вторжений, так и для жарких воздушных масс с юга, что обуславливает высокую межгодовую изменчивость климатических параметров. ",
            "stations": 9,
            "area": "196 001 км²",
            "area_perc": "7.2%",
            "temp_2025": 6.7,
            "norm_temp": 1.1,            
            "anom_2025": 3.51,
            "precip_2025": 292.6,
            "prec_norm": "104.3%",
            "temp_extreme": {"max": "+25.6°С (июль 1998)", "min": "-29.3°С (февраль 1969)"},
            "trend_temp": "+0,43 °С",
            "trend_precip": "+0,1 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",            
            "top_years": [
                {"year": 2025, "val": 6.5, "col": "#990000"},
                {"year": 2023, "val": 5.6, "col": "#b30000"},
                {"year": 2020, "val": 5.5, "col": "#d32f2f"},
                {"year": 1983, "val": 5.2, "col": "#e57373"},
                {"year": 2004, "val": 4.8, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1964, "val": 338, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 1950, "val": 387, "col": "#2e7d32"},
                {"year": 2013, "val": 384, "col": "#4caf50"},
                {"year": 1993, "val": 382, "col": "#81c784"},
                {"year": 1990, "val": 376, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🔥 Экстремальный рост температур ", "text": "Повышение на 0,43 °С каждые 10 лет. 2025 год стал аномально жарким. Превышение нормы на 3,51 °C свидетельствует о серьезном изменении термического режима.", "level": 95, "color": "#d32f2f"},
            {"title": "💧 Нестабильность увлажнения ", "text": "Слабоположительный тренд осадков (+0,1 мм/10 лет) фактически означает стагнацию увлажнения на фоне сильного потепления. Повышение температуры ускоряет испарение. Даже при сохранении нормы осадков, почва становится суше.", "level": 70, "color": "#f57c00"},
            {"title": "🌦️ Изменение внутригодового распределения осадков ", "text": "Рост осадков наблюдается в большинстве месяцев (январь–май, июль–август) в пределах 0,11–2,55 мм/10 лет. Основной прирост обеспечивают зимний, весенний и летний сезоны, что несколько смягчает риски засух в период вегетации.", "level": 45, "color": "#1976d2"}
            ],
            "final_conclusion": "Костанайская область демонстрирует один из самых высоких уровней температурных аномалий в северном Казахстане. В 2025 году среднегодовая температура (+6,7 °С) более чем в два раза превысила историческую норму региона. Несмотря на слабую тенденцию к росту осадков, интенсивное потепление создает риски для зернового хозяйства. Положительным фактором является то, что рост осадков затрагивает май и август, что крайне важно для формирования урожая пшеницы.",            
            "zones": [
            {
                "title": "🌳 Лесостепная (~25%)",
                "desc": "Север (Узункольский, Мендыкаринский р-ны). Березовые колки, высокая влажность.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~75%)",
                "desc": "Центр и Юг. Открытые равнины, черноземы и каштановые почвы.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -11.2, "sp": 6.2, "su": 21.1, "au": 5.7, "y": 5.4},
            "t_anom_2025": {"w": 6.04, "sp": 5.0, "su": 0.71, "au": 3.14, "y": 3.51},
            "p_norm": {"w": 48.8, "sp": 59.7, "su": 107.4, "au": 73.9, "y": 289.8},
            "p_anom_2025": {"w": -11.6, "sp": 8.9, "su": 9.3, "au": -5.8, "y": 12.5}    
        },
        "Павлодарская область": {
            "geo_text": "Павлодарская область расположена в северо-восточной части страны в пределах Западно-Сибирской равнины. Регион пересекает крупнейшая водная артерия — река Иртыш. Климат резко континентальный, характеризующийся продолжительной холодной зимой (с самыми низкими температурами в стране) и коротким, но жарким и сухим летом. ",
            "stations": 5,
            "area": "124 755 км²",
            "area_perc": "4.6%",
            "temp_2025": 5.4,
            "norm_temp": 1.1,            
            "anom_2025": 3.0,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24.3°С (июль 1965)", "min": "-30.9°С (январь 1969)"},
            "trend_temp": "+0,32 °С",
            "trend_precip": "+8,4 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",           
            "top_years": [
                {"year": 2025, "val": 3.02, "col": "#990000"},
                {"year": 2020, "val": 2.97, "col": "#b30000"},
                {"year": 2023, "val": 2.64, "col": "#d32f2f"},
                {"year": 1983, "val": 2.33, "col": "#e57373"},
                {"year": 2002, "val": 2.28, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1951, "val": 173.34, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 1997, "val": 196.26, "col": "#2e7d32"},
                {"year": 1955, "val": 197.06, "col": "#4caf50"},
                {"year": 1988, "val": 215.06, "col": "#81c784"},
                {"year": 1981, "val": 218.26, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🔥 Экстремальные температурные колебания", "text": "Повышение на 0,32 °С каждые 10 лет. Огромная амплитуда между историческим минимумом января (−30,9 °С) и максимумом июля (+24,3 °С). 2025 год показал резкий скачок средней температуры до +5,4 °С.", "level": 95, "color": "#d32f2f"},
            {"title": "🌦️ Сдвиг сезонного увлажнения ", "text": "Положительный тренд годовых осадков (+8,4 мм/10 лет). Сокращение осадков в мае и июле (на 0,14–1,41 мм/10 лет) создает угрозу «летней засухи» на фоне общего роста годовых показателей.", "level": 70, "color": "#f57c00"},
            {"title": "💧 Весенние паводки", "text": "Устойчивый рост весенних осадков на 2,6 мм/10 лет. Это благоприятно для накопления влаги в почве перед посевной, но может осложнить полевые работы при чрезмерных осадках в начале сезона.", "level": 45, "color": "#1976d2"}
            ],
            "final_conclusion": "Павлодарская область демонстрирует устойчивый тренд к «смягчению» климата и росту годовых сумм осадков. 2025 год стал аномально влажным (124,7% нормы) и теплым (аномалия +3,0 °С). Главный риск заключается в дефиците осадков в мае и июле, что при растущих температурах увеличивает испаряемость и может негативно влиять на урожайность зерновых, несмотря на общую «дождливость» года.",            
            "zones": [
            {
                "title": "🌾 Степная (~70%)",
                "desc": "Север и центр. Разнотравные степи поймы Иртыша.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾☀️ Сухостепная (~30%)",
                "desc": "Южные районы, переход к полупустыне.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -15.5, "sp": 2.9, "su": 19.4, "au": 2.7, "y": 2.4},
            "t_anom_2025": {"w": 5.2, "sp": 4.4, "su": 0.9, "au": 1.4, "y": 3.0},
            "p_norm": {"w": 44.8, "sp": 55.0, "su": 120.7, "au": 72.3, "y": 292.8},
            "p_anom_2025": {"w": 7.86, "sp": 3.68, "su": 46.7, "au": 32.7, "y": 94.54}    
        },
        "Алматинская область": {
            "geo_text": "Алматинская область характеризуется сложным рельефом — от пустынь Прибалхашья до вечных снегов Заилийского Алатау. Это один из самых климатически разнообразных регионов, где сельское хозяйство и водоснабжение мегаполиса напрямую зависят от состояния горных ледников и сезонного распределения осадков.",
            "stations": 9,
            "area": "105 263 км²",
            "area_perc": "3.9%",
            "temp_2025": 9.5,
            "norm_temp": 1.1,            
            "anom_2025": 2.73,
            "precip_2025": 348.2,
            "prec_norm": "72.4%",
            "temp_extreme": {"max": "+23.9°С (июль 2015)", "min": "-16.5°С (январь 1969)"},
            "trend_temp": "+0,36 °С",
            "trend_precip": "+0,4 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",          
            "top_years": [
                {"year": 2025, "val": 9.46, "col": "#990000"},
                {"year": 2023, "val": 8.86, "col": "#b30000"},
                {"year": 2022, "val": 8.76, "col": "#d32f2f"},
                {"year": 1997, "val": 8.76, "col": "#e57373"},
                {"year": 2015, "val": 8.6, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1944, "val": 284.06, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 1991, "val": 294.98, "col": "#2e7d32"},
                {"year": 1997, "val": 318.99, "col": "#4caf50"},
                {"year": 1995, "val": 337.83, "col": "#81c784"},
                {"year": 2020, "val": 348.0, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🌾 Интенсивное летнее иссушение ", "text": "Снижение летних осадков на 2,5 мм каждые 10 лет. Уменьшение влаги в июне и июле на фоне роста температур усиливает риск засух и лесных пожаров в предгорьях.", "level": 95, "color": "#d32f2f"},
            {"title": "🌦 Деградация осадков в вегетационный период ", "text": "Сокращение осадков в апреле, мае и октябре (на 0,55–3,91 мм/10 лет). Дефицит влаги в период активного роста сельхозкультур требует пересмотра графиков орошения.", "level": 70, "color": "#f57c00"},
            {"title": "🔥 Температурный стресс ", "text": "Повышение на 0,36 °С за десятилетие. 2025 год стал одним из самых теплых (+9,5 °С), что ускоряет абляцию (таяние) ледников, сокращая долгосрочные запасы пресной воды.", "level": 70, "color": "#f57c00"}
            ],
            "final_conclusion": "Алматинская область входит в фазу «засушливого потепления». Несмотря на символический рост общегодового количества осадков (+0,4 мм/10 лет), их распределение становится крайне невыгодным: летние месяцы катастрофически теряют влагу. 2025 год с его показателем в 72,4% от нормы осадков является ярким индикатором нарастающего водного дефицита. Региону требуется адаптация к уменьшению летнего стока рек и внедрение технологий сбережения талых вод.",            
            "zones": [
            {
                "title": "🏔️ Горная / Предгорная (~30%)",
                "desc": "Юг и Восток. Заилийский Алатау, обилие рек.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾☀️ Пустынно-степная(~70%)",
                "desc": "Север (Прибалхашье). Пески, сухие равнины.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -7.0, "sp": 7.4, "su": 19.6, "au": 6.9, "y": 6.7},
            "t_anom_2025": {"w": 1.76, "sp": 3.46, "su": 2.79, "au": 1.67, "y": 2.73},
            "p_norm": {"w": 64.5, "sp": 177.5, "su": 138.2, "au": 100.8, "y": 481.0},
            "p_anom_2025": {"w": 11.2, "sp": 21.9, "su": 73.3, "au": 31.0, "y": 132.8}     
        },
        "Область Жетісу": {
            "geo_text": "Область Жетісу — край «семи рек», сочетающий в себе высокогорные хребты, предгорные равнины и пустынные зоны Балхашской впадины. Климат региона резко континентальный, с выраженной высотной поясностью. Экономика региона тесно связана с водными ресурсами, формирующимися за счет таяния ледников и сезонных осадков.",
            "stations": 8,
            "area": "118 648 км²",
            "area_perc": "4.4%",
            "temp_2025": 9.0,
            "norm_temp": 1.1,            
            "anom_2025": 2.43,
            "precip_2025": 331.7,
            "prec_norm": "86.4%",
            "temp_extreme": {"max": "+24.8°С (июль 2023)", "min": "-4.9°С (январь 2022 г.)"},
            "trend_temp": "+0,32 °С",
            "trend_precip": "+3,6 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",            
            "top_years": [
                {"year": 2025, "val": 14.6, "col": "#990000"},
                {"year": 2023, "val": 14.0, "col": "#b30000"},
                {"year": 2022, "val": 13.7, "col": "#d32f2f"},
                {"year": 2019, "val": 13.6, "col": "#e57373"},
                {"year": 2021, "val": 13.6, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 2016, "val": 597, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 1993, "val": 589, "col": "#2e7d32"},
                {"year": 2010, "val": 560, "col": "#4caf50"},
                {"year": 2002, "val": 550, "col": "#81c784"},
                {"year": 1958, "val": 541, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🔥 Стабильное потепление ", "text": "Повышение на 0,32 °С каждые 10 лет. 2025 год подтвердил тренд на перегрев, показав среднюю температуру на 2,1 °C выше нормы. Ускорение таяния ледников Джунгарского Алатау, что в долгосрочной перспективе грозит маловодьем.", "level": 70, "color": "#f57c00"},
            {"title": "🌦️ Сезонный дисбаланс осадков ", "text": "Общий годовой тренд осадков отрицательный (−3,6 мм/10 лет). Уменьшение влаги в теплый период года на фоне роста температур усиливает засушливость пастбищ.", "level": 70, "color": "#f57c00"},
            {"title": "💧 Рост зимне-весеннего увлажнения ", "text": "Значительный рост осадков в январе, феврале и марте (до 5,36 мм/10 лет). Накопление большего объема снега в горах, что при резком весеннем потеплении повышает риск селей и паводков.", "level": 45, "color": "#1976d2"}
            ],
            "final_conclusion": "Климат области Жетісу становится более контрастным. Наблюдается выраженное потепление при сокращении годовой суммы осадков. Однако положительным фактором является «увлажнение» зимнего и ранневесеннего периодов, что способствует накоплению влаги в горах. 2025 год зафиксирован как засушливый (86% нормы), что в сочетании с высокой температурой требует усиленного контроля за рациональным распределением поливной воды в вегетационный период.",            
            "zones": [
            {
                "title": "🏔️ Высокогорная (~35%)",
                "desc": "Хребты Джунгарского Алатау, ледники.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🏜️☀️ Пустынно-степная (~65%)",
                "desc": "Балхаш-Алакольская низменность, сухие равнины.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -9.4, "sp": 7.9, "su": 20.9, "au": 7.0, "y": 6.6},
            "t_anom_2025": {"w": 1.58, "sp": 4.03, "su": 2.56, "au": 2.20, "y": 2.93},
            "p_norm": {"w": 73.0, "sp": 118.5, "su": 91.7, "au": 100.6, "y": 383.8},
            "p_anom_2025": {"w": 2.9, "sp": 3.1, "su": -1.8, "au": -0.8, "y": 3.6}     
        },
        "Туркестанкая область": {
            "geo_text": "Туркестанская область характеризуется самым жарким в Казахстане резко континентальным климатом. Регион расположен на стыке пустыни Кызылкум и хребтов Тянь-Шаня. Основу экономики составляет орошаемое земледелие и хлопководство, что делает регион тотально зависимым от водных ресурсов и температурного режима.",
            "stations": 9,
            "area": "116 247 км²",
            "area_perc": "4.3%",
            "temp_2025": 14.2,
            "norm_temp": 1.1,            
            "anom_2025": 2.93,
            "precip_2025": 240.0,
            "prec_norm": "55.1%",
            "temp_extreme": {"max": "+29.7°С (июль 2019)", "min": "-12.9°С (февраль 1969)"},
            "trend_temp": "+0,40 °С",
            "trend_precip": "+2,3 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",            
            "top_years": [
                {"year": 2025, "val": 14.6, "col": "#990000"},
                {"year": 2023, "val": 14.0, "col": "#b30000"},
                {"year": 2022, "val": 13.7, "col": "#d32f2f"},
                {"year": 2019, "val": 13.6, "col": "#e57373"},
                {"year": 2021, "val": 13.6, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1969, "val": 722.0, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 1958, "val": 685.3, "col": "#2e7d32"},
                {"year": 2003, "val": 641.0, "col": "#4caf50"},
                {"year": 1993, "val": 598.2, "col": "#81c784"},
                {"year": 1998, "val": 596.7, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🏜️ Усиление аридности ", "text": "Снижение годовых осадков на 2,3 мм каждые 10 лет. В 2025 году выпало чуть больше половины годовой нормы осадков. Уменьшение влаги наблюдается практически во все ключевые месяцы (апрель–июль, сентябрь–октябрь).", "level": 95, "color": "#d32f2f"},
            {"title": "🔥 Экстремальный тепловой стресс ", "text": "Повышение на 0,40 °С каждые 10 лет. Среднемесячная температура июля достигает +29,7 °С. Рост испаряемости и увеличение потребности в поливной воде при одновременном её дефиците. ", "level": 95, "color": "#d32f2f"},
            {"title": "💧 Деградация водных ресурсов ", "text": "Значительное уменьшение осадков во все сезоны года. Сокращение снежного покрова в горах и снижение стока рек (Сырдарья), что ставит под угрозу продовольственную безопасность.", "level": 70, "color": "#f57c00"}
            ],
            "final_conclusion": "Туркестанская область находится в зоне повышенного климатического риска. В отличие от северных регионов, где рост температур частично компенсируется ростом осадков, здесь наблюдается синхронный процесс: быстрый рост тепла и стабильное сокращение влаги. 2025 год продемонстрировал сценарий «жесткой засухи», когда при аномально высокой температуре (+14,2 °С) регион получил лишь 55% необходимых осадков. Адаптация требует тотального перехода на водосберегающие технологии.",            
            "zones": [
            {
                "title": "🏜️☀️ Пустынная (~75%)",
                "desc": "Западная часть (Кызылкум), жаркое сухое лето.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🏔️ Предгорная (~25%)",
                "desc": "Предгорная	Восток и Юго-восток (каштановые почвы).",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -11.2, "sp": 6.2, "su": 21.1, "au": 5.7, "y": 5.4},
            "t_anom_2025": {"w": 1.58, "sp": 4.03, "su": 2.56, "au": 2.2, "y": 2.93},
            "p_norm": {"w": 150.6, "sp": 167.4, "su": 24.3, "au": 94.0, "y": 436.3},
            "p_anom_2025": {"w": -50.6, "sp": -106.8, "su": -15.8, "au": -67.5, "y": -196.0}   
        },
        "Кызылординская область": {
            "geo_text": "Кызылординская область расположена в зоне пустынь Туранской низменности. Климат региона характеризуется экстремальной континентальностью, высокой солнечной радиацией и острым дефицитом влаги. Регион находится в зоне прямого влияния последствий высыхания Аральского моря, что усиливает процессы опустынивания и частоту соле-пылевых бурь. ",
            "stations": 5,
            "area": "226 019 км²",
            "area_perc": "8.3%",
            "temp_2025": 12.8,
            "norm_temp": 1.1,            
            "anom_2025": 3.5,
            "precip_2025": 111.8,
            "prec_norm": "79.1%",
            "temp_extreme": {"max": "+30.4°С (июль 2019)", "min": "-20.7°С (январь 1969)"},
            "trend_temp": "+0,53 °С",
            "trend_precip": "+5,7 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",            
            "top_years": [
                {"year": 2025, "val": 12.82, "col": "#990000"},
                {"year": 2023, "val": 12.74, "col": "#b30000"},
                {"year": 2013, "val": 11.83, "col": "#d32f2f"},
                {"year": 2016, "val": 11.78, "col": "#e57373"},
                {"year": 2022, "val": 11.70, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1971, "val": 88.2, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 2021, "val": 90.7, "col": "#2e7d32"},
                {"year": 2000, "val": 90.78, "col": "#4caf50"},
                {"year": 1944, "val": 92.5, "col": "#81c784"},
                {"year": 1951, "val": 97.78, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🌡️ Экстремальный темп потепления ", "text": "Повышение температуры на 0,53 °С каждые 10 лет. Это один из самых высоких показателей на юге страны. 2025 год продемонстрировал аномалию +3,5 °С — регион фактически перешел в новый температурный режим.", "level": 95, "color": "#d32f2f"},
            {"title": "🌾 Прогрессирующая аридизация ", "text": "Снижение годовых осадков на 5,7 мм за десятилетие. Наиболее выраженное падение увлажнения происходит осенью (−3,7 мм/10 лет). Это ведет к деградации пастбищ и затрудняет естественное восстановление растительности.", "level": 90, "color": "#d32f2f"},
            {"title": "🔥 Тепловой стресс и испаряемость ", "text": "Максимальная среднемесячная температура июля достигла +30,4 °С. При крайне малом количестве осадков (111 мм) и такой жаре коэффициент испаряемости в десятки раз превышает количество влаги, что делает богарное (неполивное) земледелие невозможным.", "level": 70, "color": "#f57c00"}
            ],
            "final_conclusion": "Кызылординская область является «горячей точкой» климатических изменений в Казахстане. 2025 год подтвердил опасный тренд: область становится всё более жаркой и сухой одновременно. Незначительный рост осадков в зимне-весенний период и июле (+0,05–0,66 мм) не способен компенсировать резкое осеннее иссушение и общее падение годовых сумм. Основной вызов — сохранение водного баланса реки Сырдарья в условиях, когда локальные осадки составляют менее 80% от и без того низкой нормы.",            
            "zones": [
            {
                "title": "☀️ Пустынная (~90%)",
                "desc": "Почти вся территория. Пустыня Кызылкум, зона Аральского бедствия.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🏞️💧 Долина реки (~10%)",
                "desc": "Пойма Сырдарьи. Тугайные леса и орошаемые земли.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -3.7, "sp": 15.8, "su": 27.5, "au": 11.3, "y": 12.8},
            "t_anom_2025": {"w": 4.1, "sp": 5.3, "su": 2.0, "au": 2.4, "y": 3.5},
            "p_norm": {"w": 40.0, "sp": 49.1, "su": 19.1, "au": 33.2, "y": 141.4},
            "p_anom_2025": {"w": 6.5, "sp": 21.6, "su": 2.2, "au": 23.5, "y": 29.6}    
        },
        "Жамбылская область": {
            "geo_text": "Жамбылская область расположена на юге Казахстана, в зоне полупустынь и пустынь, переходящих на юге в предгорья Тянь-Шаня. Климат региона резко континентальный и крайне засушливый. Особенностью является высокая зависимость сельского хозяйства от трансграничных рек и талых вод горных ледников, которые подвержены деградации из-за глобального потепления. ",
            "stations": 7,
            "area": "144 264 км²",
            "area_perc": "5.3%",
            "temp_2025": 12.6,
            "norm_temp": 1.1,            
            "anom_2025": 2.98,
            "precip_2025": 138.4,
            "prec_norm": "45.4%",
            "temp_extreme": {"max": "+28.2°С (июль 2019)", "min": "-17.8°С (февораль 1969)"},
            "trend_temp": "+0,36 °С",
            "trend_precip": "+3,0 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",            
            "top_years": [
                {"year": 2025, "val": 12.6, "col": "#990000"},
                {"year": 2022, "val": 12.0, "col": "#b30000"},
                {"year": 2023, "val": 11.9, "col": "#d32f2f"},
                {"year": 2013, "val": 11.7, "col": "#e57373"},
                {"year": 2018, "val": 11.7, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 2025, "val": 138.4, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 2012, "val": 177.7, "col": "#2e7d32"},
                {"year": 2008, "val": 192.7, "col": "#4caf50"},
                {"year": 1995, "val": 193.8, "col": "#81c784"},
                {"year": 2020, "val": 202.2, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🌾 Аридность и экстремальное снижение осадков ", "text": "Уменьшение годовой суммы осадков на 7,4 мм каждые 10 лет. 2025 год стал экстремально засушливым (выпало менее половины нормы).Сокращение влаги в ключевые месяцы (апрель–июнь и сентябрь–ноябрь) на 0,8–2,6 мм/10 лет ведет к деградации пастбищ. ", "level": 95, "color": "#d32f2f"},
            {"title": "🔥 Тепловой стресс ", "text": "Повышение температуры на 0,36 °С за десятилетие. Рост числа дней с температурой выше +40 °С, что пагубно влияет на здоровье населения и вегетацию культур.", "level": 70, "color": "#f57c00"},
            {"title": "🌊 Дефицит водных ресурсов ", "text": "Снижение осадков осеннего сезона и общего годового фона. Истощение запасов в водохранилищах и снижение стока рек, что при текущем тренде потепления усиливает опустынивание южных районов.", "level": 90, "color": "#d32f2f"}
            ],
            "final_conclusion": "Жамбылская область находится в зоне высокого климатического риска. В отличие от севера страны, здесь наблюдается не только рост температур, но и устойчивое сокращение осадков. 2025 год продемонстрировал опасное сочетание рекордного тепла (Ранг №1) и критической засухи. Адаптационные меры должны включать переход на жесткое водосбережение, капельное орошение и восстановление деградированных пастбищных земель.",            
            "zones": [
            {
                "title": "🏜️☀️ Пустынная (~70%)",
                "desc": "Северная часть (глинистая пустыня Бетпак-Дала и пески Мойынкум).",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🏔️ Предгорно-горная (~30%)",
                "desc": "Южная часть вдоль хребтов Киргизского Алатау. Зона поливного земледелия.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -11.2, "sp": 6.2, "su": 21.1, "au": 5.7, "y": 5.4},
            "t_anom_2025": {"w": 2.40, "sp": 4.01, "su": 2.52, "au": 1.64, "y": 2.98},
            "p_norm": {"w": 73.4, "sp": 119.2, "su": 38.1, "au": 74.0, "y": 304.7},
            "p_anom_2025": {"w": -31.9, "sp": -79.8, "su": -15.4, "au": -44.9, "y": -116.3},      
        },
        "Карагандинская область": {
            "geo_text": "Карагандинская область расположена в центральной части Казахского мелкосопочника (Сарыарка). Климат региона резко континентальный и крайне засушливый. Особенностью региона является высокая повторяемость пыльных бурь и метелей, а также резкие температурные скачки, обусловленные открытостью территории для арктических и сибирских воздушных масс. ",
            "stations": 7,
            "area": "239 045 км²",
            "area_perc": "8.8%",
            "temp_2025": 6.3,
            "norm_temp": 1.1,            
            "anom_2025": 2.7,
            "precip_2025": 224.4,
            "prec_norm": "88.1%",
            "temp_extreme": {"max": "+24.2°С (июль 1974)", "min": "-26.8°С (январь 1969)"},
            "trend_temp": "+0,29 °С",
            "trend_precip": "+2,19 мм",
            "analysis_text": "Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.",           
            "top_years": [
                {"year": 2025, "val": 6.3, "col": "#990000"},
                {"year": 2023, "val": 6.1, "col": "#b30000"},
                {"year": 2013, "val": 5.5, "col": "#d32f2f"},
                {"year": 2002, "val": 5.3, "col": "#e57373"},
                {"year": 1983, "val": 5.3, "col": "#ef9a9a"}
            ],
            "top_precip_years": [
                {"year": 1974, "val": 155.54, "col": "#1b5e20"}, # Темно-зеленый
                {"year": 1944, "val": 164.97, "col": "#2e7d32"},
                {"year": 1951, "val": 166.66, "col": "#4caf50"},
                {"year": 1955, "val": 172.64, "col": "#81c784"},
                {"year": 1950, "val": 177.39, "col": "#a5d6a7"}
            ],            
            "risks": [
            {"title": "🔥 Экстремальный рост весенних температур ", "text": "Повышение на 0,29 °С каждые 10 лет. В марте зафиксирован аномальный рост — +1,15 °С за десятилетие. Это ведет к сверхраннему разрушению устойчивого снежного покрова и ложной весне.", "level": 95, "color": "#d32f2f"},
            {"title": "🌦️ Летнее перераспределение осадков ", "text": "Общий годовой рост осадков (+2,19 мм/10 лет) за счет летнего сезона (+3,14 мм/10 лет). Рост осадков в июле и августе часто носит ливневый характер, что при высоких температурах не компенсирует засушливость, а может приводить к эрозии почв.", "level": 70, "color": "#f57c00"},
            {"title": "💧 Весенне-осенний дефицит влаги ", "text": "Снижение осадков в мае (−2,76 мм/10 лет) и осенью (−1,21 мм/10 лет). Майское иссушение почв критично для посевной кампании зерновых в центральном регионе.", "level": 70, "color": "#f57c00"}
            ],
            "final_conclusion": "Карагандинская область демонстрирует специфический сценарий: климат становится более влажным летом, но при этом экстремально жарким весной. 2025 год подтвердил статус региона как зоны активных изменений (аномалия +2,7 °С). Единственный месяц с отрицательным температурным трендом, сентябрь (−0,06 °С/10 лет), что несколько продлевает условия для созревания культур, однако общее иссушение в мае остается главным аграрным вызовом.",            
            "zones": [
            {
                "title": "🌾 Степная (~40%)",
                "desc": "Север и Сарыарка. Мелкосопочник, умеренное увлажнение.",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🏜️ Полупустынная (~60%)",
                "desc": "Южная часть. Сухие степи, высокая испаряемость.",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ],
            "t_norm": {"w": -13.4, "sp": 4.2, "su": 19.6, "au": 3.7, "y": 3.5},
            "t_anom_2025": {"w": 2.9, "sp": 3.8, "su": 1.7, "au": 1.4, "y": 2.7},
            "p_norm": {"w": 50.7, "sp": 64.6, "su": 77.4, "au": 61.9, "y": 254.6},
            "p_anom_2025": {"w": 3.9, "sp": -20.2, "su": -4.0, "au": -12.1, "y": -30.2}            
        } 
}



    @st.cache_data
    def load_all_data():
        # Попытка загрузить файлы по их реальным именам из репозитория
        try:
            # Вариант 1 (из последних загрузок)
            df_temp = pd.read_excel("Summary_Anom_T_1941-2025.xlsx")
            df_precip = pd.read_excel("Summary_Anom_R_1941-2025.xlsx")
# 2. ОБЯЗАТЕЛЬНО блок EXCEPT (именно его не хватает)
        except FileNotFoundError:
            # Если не нашли, пробуем старые названия (для страховки)
            try:
                df_temp = pd.read_csv("Summary_Anom_T_1941-2025.xlsx - Temp.csv")
                df_precip = pd.read_csv("Summary_Anom_R_1941-2025.xlsx - Sheet1.csv")
            except:
                st.error("Файлы данных не найдены! Проверьте названия в репозитории.")
                return None, None, {}

        mapping = {
            "Область Абай": {"col_t": "АБАЙ.ОБЛ", "col_p": "Абайск.обл"},
            "Акмолинская область": {"col_t": "АКМОЛ.ОБЛ", "col_p": "Акм обл"},
            "Актюбинская область": {"col_t": "АКТЮБИН.ОБЛ", "col_p": "Актю обл"},
            "Алматинская область": {"col_t": "АЛМАТИН.ОБЛ", "col_p": "Алмат обл"},
            "Атырауская область": {"col_t": "АТЫРАУ.ОБЛ", "col_p": "Атыр обл"},
            "Восточно-Казахстанская область": {"col_t": "ВКО", "col_p": "ВКО"},
            "Жамбылская область": {"col_t": "ЖАМБЫЛ.ОБЛ", "col_p": "жамб обл"},
            "Область Жетісу": {"col_t": "ЖЕТЫСУ.ОБЛ", "col_p": "Жетысус обл"},
            "Западно-Казахстанская область": {"col_t": "ЗКО", "col_p": "ЗКО"},
            "Карагандинская область": {"col_t": "КАРАГ.ОБЛ", "col_p": "Караг обл"},
            "Костанайская область": {"col_t": "КОСТ.ОБЛ", "col_p": "Кост обл"},
            "Кызылординская область": {"col_t": "КЫЗЫЛ.ОБЛ", "col_p": "КЗО"},
            "Мангистауская область": {"col_t": "МАНГИС.ОБЛ", "col_p": "Мангист обл"},
            "Павлодарская область": {"col_t": "ПАВЛ.ОБЛ", "col_p": "Павл обл"},
            "Северо-Казахстанская область": {"col_t": "СКО", "col_p": "СКО"},
            "Туркестанская область": {"col_t": "ТУРКЕСТ.ОБЛ", "col_p": "Турк обл"},
            "Область Ұлытау": {"col_t": "УЛЫТАУ.ОБЛ", "col_p": "Улытау обл"},
            "Казахстан (в целом)": {"col_t": "КАЗАХСТАН", "col_p": "Казахстан"}
        }

        return df_temp, df_precip, mapping
    
    df_temp, df_precip, name_mapping = load_all_data()    

     
    def render_climate_charts(df, column_name, title, subtitle, colorscale, bar_colors, unit):
        st.subheader(title)
        st.caption(subtitle)
        
        # Создаем график
        fig_chart = go.Figure()
        
        # Определяем цвета столбцов
        colors = [bar_colors[0] if x > 0 else bar_colors[1] for x in df[column_name]]
        
        fig_chart.add_trace(go.Bar(
            x=df['Год'], 
            y=df[column_name], 
            marker_color=colors, 
            opacity=0.6, 
            name='Ежегодная аномалия'
        ))
        
        # Тренд (скользящее среднее)
        sma = df[column_name].rolling(window=10, min_periods=1, center=True).mean()
        fig_chart.add_trace(go.Scatter(
            x=df['Год'], y=sma, mode='lines', 
            line=dict(color='#222', width=2), name='Тренд'
        ))

        st.plotly_chart(fig_chart, use_container_width=True)
        
        
    # 1. Выбор области (используем ключи из твоей базы ALL_REGIONS_DATABASE)
    selected_name = st.selectbox("Выберите область Казахстана:", list(ALL_REGIONS_DATABASE.keys()))

    # 2. Получаем данные по области из статической базы (площадь, описание зон и т.д.)
    reg = ALL_REGIONS_DATABASE[selected_name]

    # 3. Связываем выбор пользователя с названиями колонок в CSV через mapping
    region_cols = name_mapping.get(selected_name)

    if region_cols:
        col_t = region_cols['col_t']
        col_p = region_cols['col_p']
        
    
        # Извлекаем последние данные (2025 год) для карточек
        # df_temp и df_precip должны быть загружены заранее
        current_temp_anom = df_temp[col_t].iloc[-1]
        current_precip_anom = df_precip[col_p].iloc[-1]
        
        # Расчет текущей температуры: Норма + Аномалия
        temp_2025 = float(reg['norm_temp']) + current_temp_anom

        # --- 4. ОБНОВЛЕННЫЕ КАРТОЧКИ ---
        c1, c2, c3, c4 = st.columns(4)

        # Карточка 1: Территория (без изменений)
        c1.metric("Территория", reg['area'], delta=f"{reg['area_perc']} от РК", delta_color="off")

        # Карточка 2: Температура (динамическая из CSV)
        c2.metric(
            label="Температура 2025", 
            value=f"{temp_2025:.1f} °С", 
            delta=f"{current_temp_anom:+.2f} °С к норме",
            delta_color="inverse"
        )

        # Карточка 3: Аномалия (динамическая из CSV)
        c3.metric(
            label="Текущая аномалия", 
            value=f"{current_temp_anom:+.2f} °С", 
            delta="Ранг №1" if current_temp_anom > 2.0 else "Выше нормы",
            delta_color="normal"
        )

        # Карточка 4: Осадки (динамическая из CSV)
        c4.metric(
            label="Осадки 2025", 
            value=f"{current_precip_anom:+.1f} %", 
            delta="отклонение",
            delta_color="off"
        )
  
 
    st.markdown("### 🗺️ Природно-климатические зоны")

    # Получаем данные
    zones = reg.get("zones", []) 

    # Используем пропорцию [2, 1], чтобы текст справа имел достаточно места
    col_left, col_right = st.columns([1, 1])
    with col_left:
        try:
            # Картинка растянется на все 85% ширины контейнера
            st.image("Natural Zones.jpeg", use_container_width=True)
            
            # Добавим небольшую подпись под картой
            st.markdown(
                "<p style='text-align: center; color: gray;'>Карта природных зон Казахстана</p>", 
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Ошибка при загрузке карты: {e}")
            
            

    with col_right:
        try:
            # УМЕНЬШАЕМ ЛЕГЕНДУ: вместо use_container_width задаем фиксированную ширину
            # Это сделает шкалу аккуратной и не даст ей растянуться на всю колонку
            st.image("Клим_зоны_Шкала.jpeg", width=500) 
        except:
            pass

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        if zones:
            for zone in zones:
                z_bg = zone.get('bg', '#f8f9fa')
                z_col = zone.get('color', '#333')
                z_title = zone.get('title', 'Зона')
                z_desc = zone.get('desc', '')

                # ЕЩЕ БОЛЬШЕ ТЕКСТА: заголовок 20px, описание 17px
                st.markdown(f"""
                    <div style="
                        background-color: {z_bg}; 
                        border-radius: 14px; 
                        padding: 22px; 
                        border-left: 8px solid {z_col};
                        margin-bottom: 20px;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                    ">
                        <div style="color: {z_col}; font-weight: 850; font-size: 20px; margin-bottom: 10px; letter-spacing: -0.5px;">
                            {z_title}
                        </div>
                        <div style="color: #111; font-size: 17px; line-height: 1.6; font-weight: 400;">
                            {z_desc}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Данные по зонам уточняются.")
            
 
# --- 5. ПОДГОТОВКА ДАННЫХ ДЛЯ ГРАФИКОВ ОБЛАСТИ ---
        # Извлекаем топ лет и рекорды осадков именно для выбранной области
    region_top_years = reg.get("top_years", [])
    region_precip_records = reg.get("precip_records_mm", []) # Используем мм, как ты просил

           
        # --- 5. ГРАФИКИ (ВЫЗОВ ТВОЕЙ ФУНКЦИИ) ---
    st.markdown("---")
            # --- ОТДЕЛЬНЫЙ БЛОК ТРЕНДОВ (ВНЕ КОЛОНОК) ---
    st.markdown("### 📊 Климатические тренды областей")      
     
    col_l, col_r = st.columns(2)

    with col_l:
            render_climate_charts(
                df_temp, col_t, 
                "Температура воздуха", 
                "Аномалии температуры (°C)",
                'RdBu_r',                
                ['#d32f2f', '#1f77b4'], "°C"
            )

    with col_r:
            render_climate_charts(
                df_precip, col_p, 
                "Осадки", 
                "Отклонение осадков от нормы (%)", 
                'BrBG',                
                ['#2e7d32', '#8d6e63'], "%"
        )
        
 
    # Извлекаем значения из базы (с заглушками, если данных нет)
    t_val = reg.get("trend_temp", "н/д")
    p_val = reg.get("trend_precip", "н/д")
    analysis = reg.get("analysis_text", "Анализ для данной области уточняется.")

    # Стили оставляем в markdown (их можно вынести отдельно, чтобы не дублировать)
    st.markdown(f"""
        <style>
        .trends-container {{
            display: flex;
            justify-content: flex-start;
            gap: 30px;
            margin: 15px 0;
        }}
        .trend-card {{
            flex: 0 1 auto;
            padding: 15px 25px;
            border-radius: 10px;
            background-color: #fcfcfc;
            border: 1px solid #eee;
            min-width: 200px;
        }}
        .trend-label {{ font-size: 0.9rem; color: #666; margin-bottom: 5px; }}
        .trend-value {{ font-size: 1.8rem; font-weight: 800; line-height: 1.1; }}
        .v-green {{ color: #28a745; }}
        .v-orange {{ color: #f39c12; }}
        .trend-note {{ font-size: 0.8rem; color: #888; margin-top: 8px; font-style: italic; }}
        </style>
        
        <div class="trends-container">
            <div class="trend-card" style="border-left: 5px solid #28a745;">
                <div class="trend-label">тренд</div>
                <div class="trend-value v-green">📈 {t_val}</div>
                <div class="trend-note">прирост на каждые 10 лет</div>
            </div>
            <div class="trend-card" style="border-left: 5px solid #f39c12;">
                <div class="trend-label">тренд</div>
                <div class="trend-value v-orange">📈 {p_val}</div>
                <div class="trend-note">прирост на каждые 10 лет</div>
            </div>
            <div style="flex: 1; display: flex; align-items: center; padding-left: 10px;">
                <p style="color: #444; font-size: 0.95rem; border-left: 2px dashed #ccc; padding-left: 20px;">
                    💡 <b>Анализ:</b> {analysis}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")  
    
# --- 4. ДЕТАЛЬНАЯ СТАТИСТИКА ---
    st.markdown("### 📉 Статистический анализ")

    # Получаем данные региона (reg уже определен выше через selected_name)
    tn = reg.get('t_norm', {"w": 0, "sp": 0, "su": 0, "au": 0, "y": 0})
    pn = reg.get('p_norm', {"w": 0, "sp": 0, "su": 0, "au": 0, "y": 0})

    # Расчет значений 2025 года на основе аномалии из CSV
    # Температура: Норма + Аномалия
    t25 = {k: v + current_temp_anom for k, v in tn.items()}
    # Осадки: Норма * (1 + % аномалии / 100)
    p25 = {k: v * (1 + current_precip_anom / 100) for k, v in pn.items()}

    col_main_temp, col_main_precip = st.columns(2, gap="large")

    # --- ЛЕВАЯ КОЛОНКА: ТЕМПЕРАТУРА ---
    with col_main_temp:
        st.subheader("🌡️ Температурный режим")
        t_col1, t_col2 = st.columns([1.6, 1])
        
        with t_col1:
            st.markdown(f"**Сезонные показатели (°C)**")
            temp_df = pd.DataFrame({
                "Период": ["Норма", "2025"],
                "Зима": [f"{tn['w']}", f"{t25['w']:.1f}"],
                "Весна": [f"{tn['sp']}", f"{t25['sp']:.1f}"],
                "Лето": [f"{tn['su']}", f"{t25['su']:.1f}"],
                "Осень": [f"{tn['au']}", f"{t25['au']:.1f}"],
                "Год": [f"{tn['y']}", f"{t25['y']:.1f}"]
            })
            st.table(temp_df)
            extreme = reg.get('temp_extreme', {"max": "н/д", "min": "н/д"})
            st.caption(f"💡 Макс: {extreme['max']}, Мин: {extreme['min']}")

        with t_col2:
            st.markdown("**🏆 Самые теплые годы**")
            # Используем данные ТОП-5 из вашего словаря
            top_data = reg.get('top_years', [])
            if top_data:
                max_val = max([item['val'] for item in top_data])
                rows_html = "".join([f"""
                    <div style="display:flex; align-items:center; margin-bottom:8px; font-family:sans-serif;">
                        <div style="width:35px; font-size:11px; font-weight:bold;">{item['year']}</div>
                        <div style="flex-grow:1; background:#eee; height:12px; border-radius:2px; margin:0 5px;">
                            <div style="width:{(item['val']/max_val)*100}%; background:{item['col']}; height:100%; border-radius:2px;"></div>
                        </div>
                        <div style="width:35px; text-align:right; font-size:11px; font-weight:bold;">{item['val']:.1f}°</div>
                    </div>""" for item in top_data])
                st.components.v1.html(rows_html, height=160)

    # --- ПРАВАЯ КОЛОНКА: ОСАДКИ ---
    with col_main_precip:
        st.subheader("💧 Режим увлажнения")
        p_col1, p_col2 = st.columns([1.6, 1])
        
        with p_col1:
            st.markdown(f"**Сезонные осадки (мм)**")
            prec_df = pd.DataFrame({
                "Период": ["Норма", "2025"],
                "Зима": [f"{pn['w']}", f"{p25['w']:.0f}"],
                "Весна": [f"{pn['sp']}", f"{p25['sp']:.0f}"],
                "Лето": [f"{pn['su']}", f"{p25['su']:.0f}"],
                "Осень": [f"{pn['au']}", f"{p25['au']:.0f}"],
                "Год": [f"{pn['y']}", f"{p25['y']:.0f}"]
            })
            st.table(prec_df)
            st.caption(f"Процент от нормы: {current_precip_anom + 100:.1f}%")

        with p_col2:
            st.markdown("**🏆 Самые сухие годы**")
            
            # 1. Получаем список из базы (тот, что вы прислали)
            records = reg.get("top_precip_years", [])
            
            if records:
                # 2. Находим максимум для масштабирования полосок
                max_val = max([r['val'] for r in records]) if records else 1
                
                # 3. Генерируем HTML, используя данные из списка
                p_html = "".join([f"""
                    <div style="display:flex; align-items:center; margin-bottom:8px; font-family:sans-serif;">
                        <div style="width:40px; font-size:11px; font-weight:bold; color:#333;">{r['year']}</div>
                        <div style="flex-grow:1; background:#eee; height:12px; border-radius:2px; margin:0 8px;">
                            <div style="width:{(r['val']/max_val)*100}%; background:{r['col']}; height:100%; border-radius:2px;"></div>
                        </div>
                        <div style="width:50px; text-align:right; font-size:11px; font-weight:bold; color:#333;">{r['val']:.0f} мм</div>
                    </div>""" for r in records])
                
                # 4. Выводим результат
                st.components.v1.html(f"<div style='margin-top:10px;'>{p_html}</div>", height=160)
            else:
                st.info("Данные о рекордах отсутствуют")
        
            
 
    st.markdown("### 🚨 Основные климатические риски")

    # Определение функции (если она еще не определена выше)
    def risk_box(title, text, level, color):
        st.markdown(f"""
            <div style="background: white; border-left: 5px solid {color}; padding: 15px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b style="color: #333; font-size: 16px;">{title}</b>
                    <span style="color: {color}; font-weight: bold; font-size: 12px;">УРОВЕНЬ: {level}%</span>
                </div>
                <div style="background: #eee; height: 4px; width: 100%; margin: 8px 0; border-radius: 2px;">
                    <div style="background: {color}; height: 100%; width: {level}%; border-radius: 2px;"></div>
                </div>
                <p style="margin: 0; font-size: 13px; color: #666;">{text}</p>
            </div>
        """, unsafe_allow_html=True)

    # --- ДИНАМИЧЕСКИЙ ВЫВОД РИСКОВ ---
    # Берем данные из текущей области 'reg'
    region_risks = reg.get("risks", [])

    if region_risks:
        for r in region_risks:
            risk_box(r['title'], r['text'], r['level'], r['color'])
    else:
        st.info("Данные по климатическим рискам для этого региона уточняются.")

    # --- 6. ОБЩИЙ ВЫВОД ---
    conclusion = reg.get("final_conclusion", "Анализ данных продолжается.")
    st.info(f"💡 **Общие выводы:** {conclusion}")

    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import io

    st.title("🌍 Климатические индексы ")

    st.markdown("""
    > **Климатический индекс** — это расчетный диагностический показатель, который используется для количественной оценки интенсивности, частоты и продолжительности конкретных погодных явлений.
    > 
    > В отличие от простых метеорологических величин, индекс базируется на **пороговых значениях**, имеющих критическое значение для физических, биологических или экономических систем.
    """)

    st.divider()

    # --- 2. ДАННЫЕ ДЛЯ ГРАФИКОВ (Пример загрузки) ---

    def get_data(index_name):
        # 1. Настройка соответствия индексов и имен файлов
        # Убедитесь, что названия файлов в точности совпадают с файлами в GitHub
        file_mapping = {
            "GDD (Grow)": "gdd_data.csv",
            "GSL": "gsl_data.csv",
            "WSDI": "wsdi_data.csv",
            "txge30": "txge30_data.csv",
            "hwd": "hwd_data.csv",           
            "TR": "tr_data.csv",
            "HDD (heat)": "hdd_data.csv",
            "CDD": "cdd_data.csv",
            "tnltm2 / tnltm20": "tnltm20_data.csv",
            "FD": "fd_data.csv",            
        }
        
        file_name = file_mapping.get(index_name)
        
        if not file_name:
            return pd.DataFrame(columns=["Year", "Казахстан"])

        # 2. Список возможных путей (в корне или в папке data)
        possible_paths = [
            file_name,
            os.path.join("data", file_name),
            os.path.join("src", file_name)
        ]
        
        # 3. Перебор путей и кодировок
        for path in possible_paths:
            if os.path.exists(path):
                # Пробуем разные кодировки, чтобы не было UnicodeDecodeError
                for enc in ['utf-8', 'cp1251', 'latin1', 'utf-8-sig']:
                    try:
                        # Пробуем разные разделители (запятая или табуляция)
                        df = pd.read_csv(path, sep=None, engine='python', encoding=enc)
                        
                        # Проверка: если pandas не нашел колонки, пробуем принудительно табуляцию
                        if "Year" not in df.columns:
                            df = pd.read_csv(path, sep='\t', encoding=enc)
                            
                        return df
                    except (UnicodeDecodeError, Exception):
                        continue
        
        # Если файл так и не найден после всех попыток
        st.error(f"Файл {file_name} не найден в репозитории по путям: {possible_paths}")
        return pd.DataFrame(columns=["Year", "Казахстан"])
        

    # --- 3. КОНФИГУРАЦИЯ СЕКТОРОВ ---
    sectors_config = {
        "Сельское хозяйство": {
            "GDD (Grow)": {
                "desc": "🌱 **Градусо-дни роста.** Показывает накопленное тепло, необходимое для созревания культур (пшеницы, кукурузы).",
                "desc1": "В южной и западной частях территории страны рост суммы температур значительно выше, чем в северной и восточной частях. Наибольшее статистически значимое увеличение, более чем на 100 градусо-дней/10 лет, прослеживается по данным большинства станций юго-западной части Западно-Казахстанской, Атырауской, Мангистауской, Актюбинской, Кызылординской, Туркестанской, Жамбылской и Алматинской областей.  ",
                "map": "GDDgrow10.jpeg"
            },
            "GSL": {
                "desc": "📅 **Продолжительность вегетационного периода.** Время от последних весенних заморозков до первых осенних.",
                "desc1": "Статистически значимое увеличение на 3–6 суток за 10 лет прослеживается по данным большинства станций Западно-Казахстанской, Актюбинской, Кызылординской, Туркестанской, Жамбылской, Алматинской, Карагандинской, Жетісу, Абай и Восточно-Казахстанской областей. Здесь и далее на рисунках красными или зелеными кружками выделены пункты, по данным которых коэффициенты тренда статистически значимы на 5 %-м уровне. Наименьшее увеличение продолжительности вегетационного периода отмечалось в северных и северо-восточных регионах. Наиболее значимое увеличение продолжительности вегетационного периода наблюдалось на метеорологической станции Шардара в Туркестанской области и составило 6 суток/10 лет.",
                "map": "gsl.jpeg"
            },
            "WSDI": {
                "desc": "🔥 **Индекс продолжительности тепловой волны.** Критичен для «запала» зерновых. Падение урожайности при долгой жаре.",
                "desc1": "Повышение температуры воздуха во все сезоны года ведет к увеличению общей за год продолжительности волн тепла (когда, как минимум, 6 последовательных дней суточная максимальная температура воздуха была выше 90-го процентиля, индекс WSDI) на всей территории республики. В северных районах и в некоторых центральных, южных и восточных регионах увеличение составляет на 1–3 суток/10лет. Наиболее существенное увеличение (на 3–6 суток/10лет) наблюдается на западной половине страны.",                
                "map": "WSDI_1.jpeg"
            },
            "txge30": {
                "desc": "☀️ **Дни с температурой ≥ 30°C.** Порог, при котором у многих культур замедляется фотосинтез и наступает тепловой стресс.",
                "desc1": "В условиях жаркого и засушливого лета в южных регионах Казахстана это оказывает негативное воздействие не только на растительность, но и на организм человека и животных. Например, практически повсеместно увеличивается число дней с температурой выше 30 ºС, особенно заметно в западных и южных регионах страны – на 4–7 дней за 10 лет (индекс TXge30). Наибольшая скорость увеличения повторяемости высоких летних температур наблюдалась на метеорологических станциях Актау (7,3 суток/10 лет, Мангистауская область) и Арал Тенизи (6,7 суток/10 лет, Кызылординская область). ",                
                "map": "txge30_2.jpeg"
            }
        },
        "Здравоохранение": { 
            "hwd": {
                "desc": "🌱 **Длительность волн жары.** Самый опасный показатель для сердечно-сосудистой системы.",
                "desc1": "На большей части территории республики наблюдается статистически значимая положительная тенденция общей продолжительности всех волн жары в теплый период (волна жары – это три и более суток подряд, когда коэффициент избытка тепла имеет положительное значение, индекс HWF). Наибольшая статистически значимая положительная тенденция (более 6–9 суток/10лет) наблюдалась на 3 метеорологических станциях: Актау (8 суток/10 лет) в Мангистауской, Казыгурт и Кызылорда (6 суток/10 лет) в Туркестанской и Кызылординской областях, соответственно",                
                "map": "hwd.jpeg"
            },
            "TR": {
                "desc": "☀️ **Тропические ночи (T min > 20°C).** Индекс показывает, когда организм человека не успевает восстановиться ночью после дневной жары.",
                "desc1": "температуры, примерно в половине случаев — более быстрыми темпами по сравнению с ростом суточного максимума. На рисунке представлено изменение количества суток, когда минимальная температура ≥ 20 °C (индекс TR). За последние более чем 60 лет в Казахстане прослеживается в основном увеличение количества таких суток, максимально в западных и юго-западных регионах страны (от 4 суток/10лет и более). В Мангистауской, Атырауской, Кызылординской и Туркестанской областях количество тропических ночей достигало от 6 суток/10 лет и более. Таким образом, здесь значительно ухудшаются условия для ночного отдыха организма человека от дневной жары, которая, как показано выше, тоже усиливается.",                
                "map": "tr.jpeg"
            },
            "txge30": {
                "desc": "🔥 **Дни с температурой ≥ 30°C.** Дни сильной жары, когда резко возрастает количество вызовов скорой помощи.",
                "desc1": "В условиях жаркого и засушливого лета в южных регионах Казахстана это оказывает негативное воздействие не только на растительность, но и на организм человека и животных. Например, практически повсеместно увеличивается число дней с температурой выше 30 ºС, особенно заметно в западных и южных регионах страны – на 4–7 дней за 10 лет (индекс TXge30). Наибольшая скорость увеличения повторяемости высоких летних температур наблюдалась на метеорологических станциях Актау (7,3 суток/10 лет, Мангистауская область) и Арал Тенизи (6,7 суток/10 лет, Кызылординская область).",                
                "map": "txge30_2.jpeg"
            }
        },
        "Энергетика": { 
            "HDD (heat)": {
                "desc": "🌱 **Градусо-дни отопления.** Показывает, сколько энергии потребуется на обогрев зданий зимой. С потеплением этот показатель в РК падает, что экономит топливо.",
                "desc1": "Сокращение количества дней с отрицательными температурами приводит к повсеместному сокращению дефицита тепла в холодный период года. Здесь, за пороговое значение температуры воздуха, которую желательно поддерживать в помещении, принята температура 23 °С. На большей части территории Казахстана диапазон сокращения дефицита тепла находится в пределах 60–100 градусо-дней за каждые 10 лет. Сокращение дефицита тепла на большей части северного и восточной части центрального регионов составляет до 40 градусо-дней за каждые 10 лет, но в некоторых районах этих регионов сокращение дефицита тепла отсутствует. Наибольшие изменения зафиксированы локально на западе, юго-западе и в ряде районов восточного Казахстана, где сокращение дефицита тепла достигает 130–160 градусо-дней/10 лет.",                
                "map": "HDDheat23_trend_2024.png"
            },
            "CDD": {
                "desc": "☀️ **Градусо-дни охлаждения.** Этот индекс растет, показывая резкое увеличение спроса на электричество для кондиционирования летом.",
                "desc1": "Следствием высоких температур воздуха значительную часть теплого периода года, особенно в западных и южных регионах Казахстана, наблюдалась острая необходимость в поддержании в помещениях благоприятной температуры, т.е. кондиционирования. В данном случае в качестве благоприятной температуры принят порог в 23 °С, превышение которого означает дефицит холода (индекс CDDcold23). Наибольшие значения индекса наблюдались в Мангистауской и Туркестанской областях, где дефицит холода достигал 543-654 градусо-суток.",                
                "map": "cddcold23_2.jpeg"
            },
            "FD": {
                "desc": "🔥 **Морозные дни (T min < 0°C).** Важны для мониторинга рисков обледенения линий электропередач.",
                "desc1": "Как следствие повышения температуры воздуха, по всей территории Казахстана сокращается количество суток в году, когда суточная минимальная температура равна или опускается ниже 0 ºС (сутки с заморозком, индекс FD0). Скорость сокращения варьирует по территории, в основном, от 0 до 4 суток/10лет, местами скорость сокращения выше 5–6 суток за 10 лет.",                
                "map": "fd.jpeg"
            }
        },
        "Водное хозяйство ": { 
            "CDD (Cold)": {
                "desc": "🌱 **Продолжительность сухого периода.** Максимальное количество идущих подряд дней без осадков. Ключевой индикатор для прогнозирования засух в степных зонах РК.",
                "desc1": "По территории Казахстана отмечены слабые тенденции, как в сторону уменьшения, так и в сторону увеличения бездождного периода на 1–4 суток/10 лет. Тренды, в основном, незначимы, за исключением некоторых станций северных, северо-восточных и северной части центральных регионов, а также локально восточных, юго-восточных и южных районов, где зафиксировано статистически значимое уменьшение такого периода; а в югозападном регионе, Приаралье и некоторых горных районов юго-восточного региона зафиксировано увеличение максимальной продолжительности бездождного периода на 1– 6 дня/10 лет.",                
                "map": "CDD_trend_2024.png"
            },
            "tnltm2 / tnltm20": {
                "desc": "☀️ **Ночи с экстремальным холодом.** Влияют на промерзание почвы и последующие весенние паводки (если почва замерзла, она не впитывает талую воду).",
                "desc1": "На территории республики практически повсеместно сокращается количество дней с очень жесткими морозами (когда суточный минимум температуры воздуха ниже минус 20 °C, индекс TNltm20). Существенное сокращение числа таких суток наблюдается в северо-западных и центральных регионах, а также в Прибалхашском районе — на 2–3 суток/10 лет. В некоторых районах Восточно-Казахстанской области повторяемость суток с очень жесткими морозами уменьшается более значительными темпами – на 4–5 суток/10лет.",                
                "map": "tnltm20_trend_2024.png"
            }
        },
        "Лесное хозяйство ": { 
            "WSDI": {
                "desc": "🌱 **Индекс продолжительности тепловой волны.** Длительная жара при отсутствии дождей — главный фактор лесных пожаров (как в Абайской и Костанайской областях).",
                "desc1": "Повышение температуры воздуха во все сезоны года ведет к увеличению общей за год продолжительности волн тепла (когда, как минимум, 6 последовательных дней суточная максимальная температура воздуха была выше 90-го процентиля, индекс WSDI) на всей территории республики. В северных районах и в некоторых центральных, южных и восточных регионах увеличение составляет на 1–3 суток/10лет. Наиболее существенное увеличение (на 3–6 суток/10лет) наблюдается на западной половине страны.",                
                "map": "WSDI_1.jpeg"
            },
            "GDD": {
                "desc": "☀️ **Градусо-дни роста.** Влияет на скорость роста лесных массивов и, соответственно, на объем депонирования (поглощения) углерода из атмосферы.",
                "desc1": "В южной и западной частях территории страны рост суммы температур значительно выше, чем в северной и восточной частях. Наибольшее статистически значимое увеличение, более чем на 100 градусо-дней/10 лет, прослеживается по данным большинства станций юго-западной части Западно-Казахстанской, Атырауской, Мангистауской, Актюбинской, Кызылординской, Туркестанской, Жамбылской и Алматинской областей",                
                "map": "GDDgrow10.jpeg"
            }
        }
        
    }

    # --- 4. ИНТЕРФЕЙС ---
    import os

    col_nav, col_display = st.columns([1, 4]) # Немного увеличим область контента

    with col_nav:
        st.subheader("Навигация")
        sel_sector = st.selectbox("Сектор:", list(sectors_config.keys()))
        sel_index = st.radio("Индекс:", list(sectors_config[sel_sector].keys()))

    with col_display:
        st.header(f"Анализ: {sel_index}")
        
        # 1. Достаем данные индекса в переменную, чтобы код был чище
        index_data = sectors_config[sel_sector][sel_index]
        
        # 2. Выводим основное описание
        st.info(index_data["desc"])
        
        # 3. ПРОВЕРКА: если есть desc1, выводим его дополнительно
        if "desc1" in index_data:
            st.write(index_data["desc1"])
        
        # Создаем два столбца для Карты и Графика
        col_map, col_chart = st.columns(2)
    
        
        # --- БЛОК КАРТЫ ---
        with col_map:
            st.write("**🗺️ Пространственное распределение**")
            image_name = sectors_config[sel_sector][sel_index]['map']
            
            # Логика поиска пути файла
            if os.path.exists(image_name):
                image_path = image_name
            elif os.path.exists(f"maps/{image_name}"):
                image_path = f"maps/{image_name}"
            else:
                image_path = image_name
                
            try:
                # use_container_width=True подстроит карту под ширину узкой колонки
                st.image(image_path, use_container_width=True)
            except:
                st.error(f"Файл {image_name} не найден.")

        # --- БЛОК ГРАФИКА ---
        with col_chart:
            st.write("**📈 Временная динамика**")
            df = get_data(sel_index)
            
            fig = px.line(df, x="Year", y="Казахстан", 
                          markers=True, 
                          line_shape="spline",
                          height=300) # Ограничиваем высоту для компактности
            
            fig.update_traces(line_color='#e74c3c')
            # Убираем лишние отступы в графике
            fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
            
            st.plotly_chart(fig, use_container_width=True)
            

    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import os

    def render_wind_dashboard():
        # --- НАСТРОЙКИ ---
        data_file = "Max_wind.csv"
        image_path = "wind_RES5.jpg"
        
        # ОБЯЗАТЕЛЬНО ОБЪЯВЛЯЕМ ПРОЦЕНТ (иначе будет ошибка NameError)
        map_percent = 125  # Меняйте это число для управления размером карты
        # -----------------

        st.title("💨 Мониторинг ветровой активности Казахстана")
        st.divider()
        
          # --- СЕКЦИЯ 1: КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ ---
        st.subheader("Интересные факты")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Экстремальный рекорд", value="60 м/с", delta="Жаланашколь")
            st.caption("Зафиксировано в 1979, 1982, 1983 гг.")
            
        with col2:
            st.metric(label="Общая тенденция", value="-3.3 м/с", delta_color="normal")
            st.caption("Снижение макс. скорости за 45 лет")
            
        with col3:
            st.metric(label="Пиковая аномалия", value="+0.5 м/с", delta="в 1980-х")
            st.caption("Отклонение от нормы")

        st.divider()
        

        # Пропорции колонок: 3 к 2
        col_map, col_charts = st.columns([1, 1])

        with col_map:
            st.subheader("🗺️ Карта ветровых режимов")

            if os.path.exists(image_path):
                # Читаем файл и кодируем в base64 для вставки в HTML
                with open(image_path, "rb") as f:
                    data = f.read()
                    encoded = base64.b64encode(data).decode()
                
                # HTML вставка: ставим ширину в зависимости от процентов от ширины экрана (vw)
                # Или просто используем style="width: 100%;"
                html_code = f"""
                    <div style="text-align: center;">
                        <img src="data:image/png;base64,{encoded}" 
                             style="width: {map_percent}%; min-width: 400px; border-radius: 10px;">
                        <p style="color: gray; font-size: 0.8rem;">Масштаб: {map_percent}%</p>
                    </div>
                """
                st.markdown(html_code, unsafe_allow_html=True)
            else:
                st.error(f"Файл {image_path} не найден.")
        
                
            st.info("**Справка:** Жетісуские ворота — самая ветреная точка, где скорость достигает 60 м/с.")

        with col_charts:
            st.subheader("📈 Динамика по регионам")
            
            if os.path.exists(data_file):
                try:
                    df = pd.read_csv(data_file, sep=';', encoding='utf-8-sig')
                    regions = [col for col in df.columns if col != 'Год']
                    selected_region = st.selectbox("Выберите область для анализа:", regions)
                    
                    if selected_region:
                        df[selected_region] = pd.to_numeric(df[selected_region].replace('#Н/Д', None), errors='coerce')
                        df_plot = df.dropna(subset=[selected_region, 'Год']).sort_values('Год')

                        # Создаем график
                        fig = px.line(
                            df_plot, 
                            x='Год', 
                            y=selected_region,
                            title=f"Абсолютный максимум: {selected_region}",
                            markers=True,
                            color_discrete_sequence=['#00CC96']
                        )
                        
                        fig.update_layout(yaxis_title="м/с", xaxis_title="Год", hovermode="x unified")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # --- БЛОК АВТОМАТИЧЕСКОГО АНАЛИЗА ---
                        st.markdown("### 📝 Анализ данных")
                        
                        # 1. Основные показатели
                        max_val = df_plot[selected_region].max()
                        year_max = df_plot.loc[df_plot[selected_region].idxmax(), 'Год']
                        avg_val = df_plot[selected_region].mean()
                        
                        # 2. Определение тренда (сравнение начала и конца периода)
                        first_val = df_plot[selected_region].iloc[0]
                        last_val = df_plot[selected_region].iloc[-1]
                        trend_diff = last_val - first_val
                        
                        if trend_diff > 1:
                            trend_desc = "наблюдается тенденция к **увеличению** силы ветра"
                        elif trend_diff < -1:
                            trend_desc = "наблюдается тенденция к **снижению** ветровой нагрузки"
                        else:
                            trend_desc = "показатели остаются относительно **стабильными**"

                        # 3. Вывод анализа в интерфейс
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Максимум", f"{max_val} м/с", f"год: {year_max}", delta_color="inverse")
                        with col2:
                            st.metric("Среднее значение", f"{avg_val:.1f} м/с")

                        analysis_text = f"""
                        Для региона **{selected_region}** за анализируемый период {df_plot['Год'].min()}-{df_plot['Год'].max()} гг. 
                        {trend_desc}. Средняя скорость экстремальных порывов составляет **{avg_val:.1f} м/с**. 
                        
                        Наиболее критическая ситуация зафиксирована в **{year_max} году**, когда скорость ветра 
                        достигла рекордных **{max_val} м/с**, что требует особого внимания при проектировании 
                        инфраструктуры в данной области.
                        """
                        st.info(analysis_text)

                except Exception as e:
                    st.error(f"Ошибка при обработке файла: {e}")
            else:
                st.error(f"Файл {data_file} не найден.")
                

    # Запуск приложения
    if __name__ == "__main__":
        # Рекомендуется добавить wide mode для больших карт
        st.set_page_config(page_title="Wind Monitor", layout="wide")
        render_wind_dashboard()
    
    



        # --- СЕКЦИЯ 2: ПРИЧИНЫ И ОРОГРАФИЯ ---
        st.subheader("Причины экстремальных ветров")
        
        with st.expander("🌍 Особенности региона Жаланашколь и Жетісуских ворот", expanded=True):
            st.write("""
            Экстремальные условия обусловлены **климато-орографическими особенностями**. 
            Станция Жаланашколь находится в районе **Жетісуских ворот** — это узкий межгорный проход между 
            хребтами **Жетісуского Алатау** и **Тарбагатая**.
            
            Здесь формируется уникальный аэродинамический эффект: воздушные массы ускоряются, проходя через «узкое горлышко» ущелий.
            """)
            
            c1, c2 = st.columns(2)
            c1.info("**Ветер «Ибэ»**: Сухой юго-восточный поток из Китая в холодный сезон.")
            c2.success("**Ветер «Сайкан»**: Северо-западный поток из казахских степей через Джунгарский проход.")

        st.divider()


 
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go

    # Настройка страницы
    st.set_page_config(page_title="Мониторинг снега в РК", layout="wide")

    # Заголовок
    st.title("❄️ Динамика снежного покрова по областям РК")

    @st.cache_data
    def load_data():
        # Загрузка с учетом разделителя ';'
        try:
            df = pd.read_csv('Максимальная высота снега.csv', sep=';')
            df.columns = [c.strip() for c in df.columns]
            df['Год'] = df['Год'].astype(int)
            return df
        except Exception as e:
            st.error(f"Ошибка при чтении файла: {e}")
            return None

    df = load_data()

    if df is not None:
        # --- ПОДГОТОВКА СПИСКА ОБЛАСТЕЙ ---
        excluded = ['Год', 'высота макс', 'сред высота снега']
        region_options = [col for col in df.columns if col not in excluded]

        # --- ОСНОВНОЙ МАКЕТ (2 Колонки) ---
        col_chart, col_analysis = st.columns([2, 1])

        with col_chart:
            # Выбор областей прямо над графиком для удобства
            selected_regions = st.multiselect(
                "Выберите области для сравнения:", 
                options=region_options, 
                default=[region_options[0]] if region_options else None
            )

            # Создание динамического графика Plotly
            fig = go.Figure()

            # 1. Линия среднего (если включено)
            if show_avg:
                fig.add_trace(go.Scatter(
                    x=df['Год'], y=df['сред высота снега'],
                    name='Среднее по РК',
                    line=dict(color='rgba(150, 150, 150, 0.5)', dash='dash'),
                    fill='tozeroy', fillcolor='rgba(200, 200, 200, 0.2)'
                ))

            # 2. Линии выбранных областей
            for region in selected_regions:
                fig.add_trace(go.Scatter(
                    x=df['Год'], y=df[region],
                    mode='lines+markers',
                    name=region,
                    hovertemplate='Год: %{x}<br>Высота: %{y} см'
                ))

            # 3. Линия максимума (если включено)
            if show_total_max:
                fig.add_trace(go.Scatter(
                    x=df['Год'], y=df['высота макс'],
                    name='Абс. максимум РК',
                    line=dict(color='red', width=1, dash='dot')
                ))

            fig.update_layout(
                hovermode="x unified",
                margin=dict(l=0, r=0, t=30, b=0),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis_title="Год",
                yaxis_title="Высота снега (см)",
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

        with col_analysis:
            st.subheader("📊 Аналитика")
            
            if selected_regions:
                # Берем первую из выбранных областей для детальной аналитики
                main_region = selected_regions[0]
                
                local_max = df[main_region].max()
                local_max_year = df.loc[df[main_region] == local_max, 'Год'].values[0]
                current_val = df[main_region].iloc[-1]
                
                st.info(f"Анализ по области: **{main_region}**")
                
                m1, m2 = st.columns(2)
                m1.metric(f"Тек. высота ({df['Год'].max()})", f"{current_val} см")
                m2.metric(f"Пик ({local_max_year})", f"{local_max} см")
                
                st.markdown(f"""
                **Ключевые выводы:**
                * В **{main_region}** самый снежный период зафиксирован в **{local_max_year}** году.
                * **Общий тренд:** По РК высота снега растет на **0.62 см** в год.
                * **Прогноз:** Увеличение высоты ведет к росту влагозапасов и рискам паводков.
                """)
                
                if current_val > df['сред высота снега'].iloc[-1]:
                    st.warning("Выше среднего по стране")
                else:
                    st.success("Ниже среднего по стране")
            else:
                st.write("Выберите область слева, чтобы увидеть аналитику.")

    

with tabs[8]:
    st.title("🌱Мониторинг качества окружающей среды в Республике Казахстан")
    
    # Стилизация через CSS для красивых карточек
    st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stCard {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            border-left: 5px solid #007bff;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .stMetric {
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)

    # Вводная часть
    st.info("Сбор, обработка, анализ данных экологического мониторинга для обеспечения экологической безопасности граждан Казахстана.")

    st.markdown("### 📊 Статистика мониторинга РГП «Казгидромет»")

    # Используем колонки, чтобы разделить список на две логические части для экономии места
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("""
        #### 🌬️ Атмосферный воздух
        * **Населенных пунктов:** 70 
        * **Постов наблюдений:** 175 *(131 авто / 44 ручных)*
        * **Загрязняющих веществ:** 36 видов
        * **Охват:** 17 областей РК
        
        #### 💧 Поверхностные воды
        * **Водных объектов:** 134 *(88 рек, 29 озер, 13 вдхр)*
        * **Гидрохимических створов:** 373
        * **Морской мониторинг:** 1 (Каспийское море)
        """)

    with col_right:
        st.markdown("""
        #### 🏜️ Почва и осадки
        * **Мониторинг почв:** 101 населенный пункт
        * **Атмосферные осадки:** 47 метеостанций
        * **Снежный покров:** 40 метеостанций
        
        #### ☢️ Радиационный мониторинг
        * **Гамма-фон:** 89 станций (ежедневно)
        * **Радиоактивное загрязнение:** 43 станции
        * **География:** все 17 областей Казахстана
        """)

    st.info("💡 Различные типы постов (ручные, автоматические, передвижные) измеряют широкий спектр тяжелых металлов и загрязнителей.")


    st.divider()

    # Основной контент через вкладки (Tabs)
    tab1, tab2, tab3, tab4 = st.tabs([
        "💨 НМУ", 
        "☀️ УФ-индекс", 
        "🏜️ Прогноз качества воздуха", 
        "📱 AirKZ"
    ])

    import streamlit as st
    import base64

    # 1. Функция для чтения локального файла в формат base64
    def get_base64_image(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except FileNotFoundError:
            return None

    # 2. Получаем строку изображения
    img_data = get_base64_image("nmu.png")

        
    with tab1:
        st.markdown("### 🌬️ Прогноз неблагоприятных метеорологических условий")
        
        # col_a — текст, col_b — изображение nmu.png и iframe под ним
        col_a, col_b = st.columns([1, 2])
        
        with col_a:
            # Текстовое описание в левой колонке
            st.markdown(f"""
            <div class="stCard">
                <h4>Прогноз НМУ</h4>
                <p><b>Неблагоприятные метеоусловия (НМУ)</b> — это сочетание краткосрочных метеорологических факторов (штиль, слабый ветер, туман, инверсия), которые способствуют накоплению вредных веществ в приземном слое атмосферы.</p>
                <p>Предоставляем прогнозы НМУ, важные для предупреждения возможных проблем с качеством воздуха.</p>
                <p>Бюллетени для городов Казахстана публикуются на официальном сайте, предоставляя жителям информацию о предстоящих условиях.</p>
                <p>Прогноз помогает вовремя принять меры:</p>
                <ul>
                    <li>Предприятиям — снизить объем выбросов.</li>
                    <li>Жителям — сократить время пребывания на открытом воздухе.</li>
                </ul>
                <p>Данные обновляются ежедневно на основе бюллетеней Казгидромета для всех крупных городов Казахстана.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_b:
            # 1. Отображаем изображение nmu.png (без ссылки)
            if img_data:
                st.markdown(
                    f'<img src="data:image/png;base64,{img_data}" style="width:70%; border-radius:8px; border: 1px solid #ddd; margin-bottom: 15px;">', 
                    unsafe_allow_html=True
                )
            else:
                st.info("Изображение nmu.png не найдено")
            
                              
    with tab2:
        col_text, col_img = st.columns([1, 2])  # Соотношение 1:2 для картинки и текста
            
               
        with col_text:
                st.markdown("""
                    <div class="stCard">
                        <h4>☀️ Прогноз УФ индекса</h4>
                        <p><b>Период:</b> май – сентябрь.</p>
                        <p>В теплое полугодие выпускается бюллетень с прогнозом уровня ультрафиолета на ближайшие <b>7 дней</b>.</p>
                        <p style="font-size: 0.9em; color: #555;">
                        Также в бюллетене даны рекомендации для различных групп лиц. 
                        Продукция доступна на казахском, русском и английском языках.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

        with col_img:
                # Отображение GIF из вашей папки
                st.image("uf.gif", use_column_width=True)
                
                        
    with tab3:
        col_text, col_b= st.columns([1, 2])  # Соотношение 1:2 для картинки и текста
            
               
        with col_text:
                st.markdown("""
                    <div class="stCard">
                        <h4>🏜️ SILAM</h4>
                        <p>В 2020 году при поддержке Финского метеорологического института на базе модели SILAM был разработан и внедрен прогноз концентраций загрязняющих веществ в атмосферном воздухе городов Казахстана. </p>
                        <p style="font-size: 0.9em; color: #555;">
                       Визуальная модель совмещена с интерактивной картой и позволяет просматривать состояние атмосферного воздуха в динамике по часам с заблаговременностью до 48 часов.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

        with col_b:
                # Вставляем интерактивную карту через iframe
                st.components.v1.iframe("https://www.kazhydromet.kz/vc/silam/", height=600, scrolling=True)
                
                
    with tab4:
        st.markdown("### 📱 Мобильное приложение AirKz")
        st.write("Инструмент среди жителей Казахстана для контроля качества воздуха в реальном времени.")
        
        st.success("✅ **Что нового в обновлении:**")
        st.markdown("""
        * **Новый дизайн и интерфейс**
        * **Знак тревоги** при превышении ПДК
        * **Описания загрязнителей**, согласованные с Минздравом РК
        """)
        
        st.info("💡 Более 10 000 активных пользователей")


    st.markdown("---")  
    
    import streamlit as st
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np

    # 1. Списки названий для разных структур массивов
    labels_standard = ["Пыль", "PM-2.5", "PM-10", "SO2", "CO", "NO2", "NO", "O3"]
    labels_aktobe = ["SO2", "CO", "NO2", "NO", "H2S"]
    labels_karaganda = ["Пыль", "PM-2.5", "PM-10", "SO2", "CO", "NO2", "NO", "O3", "H2S", "Фенол"]
    labels_aktau = ["CO", "NO2", "NO", "H2S"]
    labels_atyrau = ["Взвешенные", "PM-2.5", "PM-10", "SO2", "CO", "NO2", "NO", "O3", "H2S", "Фенол", "Аммиак"]
    labels_kokshetau = ["SO2", "CO"]
    labels_kostanay = ["PM-10", "SO2", "CO", "NO2", "NO"]
    labels_kyzylorda = ["SO2", "CO", "NO"]
    labels_pavlodar = ["PM-2.5", "PM-10", "SO2", "CO", "H2S", "O3", "Хлористый водород"]
    labels_petropavl = ["Пыль", "SO2", "CO", "NO2", "NO", "H2S", "Фенол", "Формальдегид"]
    labels_semey = ["SO2", "CO", "NO2", "NO", "H2S", "O3"]
    labels_taraz = ["Взвешенные", "SO2", "CO", "NO2", "NO", "H2S"]
    labels_turkestan = ["NO2", "SO2", "NO", "CO", "O3", "H2S"]
    labels_uk = ["PM-2.5", "PM-10", "SO2", "CO", "NO2", "NO", "O3", "H2S", "Фенол", "Фтористый водород", "Хлор", "Хлористый водород", "Кислота серная", "Формальдегид", "Аммиак"]
    labels_uralsk = ["Взвешенные", "SO2", "CO", "NO2", "NO", "H2S", "O3"]
    labels_shymkent = ["Взвешенные", "SO2", "CO", "NO2", "NO", "H2S", "Аммиак", "Формальдегид"]

    # 2. Словарь соответствия: Город -> (Массив, Список подписей)
    kazakhstan_pollution_data = {
        'Алматы': (np.array([[3, 1, 3, 5, 8, 4, 0, 0, 1, 2, 0, 1], [553, 417, 65, 25, 60, 28, 34, 61, 48, 57, 332, 451], [370, 168, 5, 4, 8, 1, 0, 3, 6, 11, 75, 121], [2, 0, 742, 489, 6, 126, 0, 1, 143, 6, 70, 119], [382, 266, 9, 4, 0, 3, 3, 0, 4, 16, 66, 145], [1993, 2355, 1922, 1489, 1508, 1519, 308, 105, 77, 278, 624, 131], [501, 180, 384, 122, 14, 6, 23, 19, 64, 291, 502, 643], [9, 1, 2, 0, 0, 0, 1, 50, 12, 1, 0, 1]]), labels_standard),
        'Астана': (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [410, 135, 613, 0, 0, 68, 0, 0, 0, 0, 619, 628], [332, 48, 382, 0, 0, 2, 0, 0, 0, 0, 382, 382], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35, 35], [7, 9, 36, 2, 2, 20, 7, 19, 34, 34, 199, 203], [0, 0, 0, 4, 14, 0, 6, 40, 102, 102, 341, 343], [11, 0, 18, 3, 2, 7, 3, 0, 0, 0, 62, 62], [105, 112, 1014, 1133, 0, 797, 48, 4, 0, 0, 1084, 1084], [32, 285, 787, 1395, 508, 470, 1210, 508, 332, 332, 6896, 7034]]), labels_standard + ["H2S"]), # Добавил H2S к стандарту
        'Актобе': (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 14], [0, 5, 1, 1, 1, 0, 0, 0, 2, 4, 8, 3], [0, 59, 0, 0, 0, 0, 1, 245, 9, 143, 106, 179], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 36, 0], [3, 16, 22, 119, 130, 45, 148, 126, 179, 3, 19, 3]]), labels_aktobe),
        'Караганда': (np.array([[49, 59, 55, 85, 74, 77, 47, 35, 90, 61, 87, 34], [2532, 2404, 2575, 2509, 2923, 2494, 2752, 2711, 2600, 2603, 2672, 2685], [872, 1073, 618, 273, 107, 23, 12, 31, 220, 691, 561, 680], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [256, 154, 112, 19, 16, 23, 13, 8, 12, 291, 148, 72], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [173, 49, 0, 0, 0, 0, 2, 0, 20, 40, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [19, 2, 4, 2, 795, 3, 15, 6, 54, 393, 349, 67], [1, 1, 1, 0, 0, 0, 0, 11, 8, 7, 10, 24]]), labels_karaganda),
        'Актау': (np.array([[6, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [157, 128, 98, 0, 274, 364, 367, 13, 29, 52, 143, 11]]), labels_aktau),
        'Атырау': (np.array([[8, 0, 3, 1, 4, 3, 6, 0, 0, 4, 0, 3], [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 15, 0, 3, 0, 0, 0, 0], [0, 0, 8, 12, 34, 49, 0, 18, 19, 9, 2, 3], [328, 6395, 4882, 2956, 1882, 1895, 16, 385, 521, 1137, 1464, 921], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 366, 9, 13, 195], [1, 1773, 1961, 1851, 197, 259, 66, 7, 8, 1, 2, 1], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]]), labels_atyrau),
        'Кокшетау': (np.array([[0, 2, 4, 0, 3, 3, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), labels_kokshetau),
        'Костанай': (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 62, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0], [13, 13, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0], [0, 0, 84, 17, 22, 4, 24, 51, 192, 169, 0, 0], [2, 116, 174, 0, 14, 0, 0, 14, 123, 171, 0, 0]]), labels_kostanay),
        'Кызылорда': (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0], [2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]]), labels_kyzylorda),
        'Павлодар': (np.array([[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1], [0, 0, 5, 1, 0, 0, 0, 0, 0, 3, 9, 0], [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0], [10, 51, 204, 28, 22, 7, 26, 81, 89, 102, 669, 114], [25, 26, 111, 47, 0, 10, 37, 6, 0, 39, 302, 186], [0, 0, 7, 0, 0, 43, 0, 1, 0, 0, 51, 0], [4, 18, 2, 0, 0, 0, 0, 8, 0, 7, 41, 0]]), labels_pavlodar),
        'Петропавловск': (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 379, 89, 98, 108, 0, 0, 0, 143], [9, 0, 0, 6, 0, 0, 1, 0, 0, 0, 0, 0], [197, 245, 192, 612, 208, 129, 74, 130, 233, 256, 57, 90], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), labels_petropavl),
        'Семей': (np.array([[0, 0, 0, 8, 5, 3, 38, 0, 17, 169, 0, 240], [10, 29, 37, 18, 0, 0, 0, 0, 23, 395, 116, 628], [23, 72, 51, 0, 0, 0, 3, 0, 0, 11, 0, 160], [0, 0, 0, 0, 0, 0, 0, 0, 0, 84, 0, 84], [0, 0, 3, 0, 13, 2, 100, 2, 19, 20, 6, 165], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), labels_semey),
        'Тараз': (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 3, 0, 0, 4, 1, 3, 8, 1, 9, 21, 9], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 19, 2, 4, 9, 15, 5]]), labels_taraz),
        'Туркестан': (np.array([[882, 991, 1096, 1023, 1098, 1020, 1125, 1156, 1065, 1145, 618, 231], [980, 652, 436, 97, 52, 36, 167, 102, 378, 669, 1064, 1068], [0, 0, 0, 0, 2, 1, 17, 0, 0, 17, 3, 0], [18, 0, 1, 0, 0, 13, 0, 0, 2, 18, 56, 14], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 0, 56, 0, 0, 0, 0, 0, 0, 0]]), labels_turkestan),
        'Усть-Каменогорск': (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 165, 13, 27, 31, 48, 45, 57, 89, 183, 75, 56], [118, 507, 208, 15, 4, 7, 1, 0, 46, 144, 86, 80], [0, 0, 0, 0, 7, 0, 0, 0, 11, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0, 20, 4, 2, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [226, 316, 282, 67, 128, 166, 204, 162, 217, 137, 315, 189], [24, 32, 2, 9, 50, 0, 5, 31, 6, 19, 25, 11], [0, 0, 4, 3, 0, 0, 1, 0, 0, 5, 5, 10], [0, 0, 4, 0, 0, 1, 0, 0, 0, 0, 0, 0], [24, 92, 49, 34, 36, 8, 1, 50, 11, 28, 36, 56], [5, 8, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), labels_uk),
        'Уральск': (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 29, 0, 0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]]), labels_uralsk),
        'Шымкент': (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [13, 4, 0, 1, 0, 0, 0, 0, 0, 5, 12, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [905, 456, 402, 202, 238, 176, 362, 268, 82, 322, 641, 265], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), labels_shymkent)
    }

    all_historical_data = {
        "Актау": {
            "Взвешенные вещества": [20.4, 0.6, 1.0, 0.8, 0.8, 0.6, 0.4, 0.8, 0.6, 0.6, 0.5],
            "PM-2.5": [3.5, 1.7, 3.9, 3.7, 7.2, 15.6, 6.2, 1.3, 6.3, 0.1, 0.0],
            "PM-10": [11.4, 7.2, 8.3, 13.2, 22.3, 12.8, 3.3, 1.2, 3.3, 0.7, 0.7],
            "Диоксид серы": [0.1, 0.2, 0.5, 0.7, 0.2, 0.1, 0.4, 0.1, 0.1, 0.1, 0.4],
            "Оксид углерода": [0.8, 2.0, 2.4, 0.9, 1.0, 0.9, 1.9, 1.2, 3.5, 1.3, 1.5],
            "Диоксид азота": [1.1, 1.2, 1.2, 0.6, 1.0, 1.7, 2.6, 2.7, 0.8, 0.4, 0.3],
            "Сероводород": [6.8, 3.5, 0, 0, 0.6, 6.3, 9.2, 9.0, 0.5, 5.7, 4.6]
        },
        "Актобе": {
            "Взвешенные вещества": [1.0, 0.6, 0.8, 0.8, 1.5, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
            "PM-2.5": [3.68, 3.4, 3.1, 3.4, 2.1, 1.2, 6.2, 0.1, 0.1, 0.0, 0.0],
            "PM-10": [9.06, 9.8, 6.3, 7.6, 7.6, 1.9, 3.3, 0.1, 0.2, 0.0, 0.0],
            "Диоксид серы": [3.57, 7.9, 7.0, 10.0, 10.0, 1.7, 0.9, 1.2, 0.7, 0.1, 1.4],
            "Оксид углерода": [2.14, 10.0, 4.8, 12.8, 9.9, 3.0, 1.7, 2.7, 2.4, 9.2, 2.0],
            "Диоксид азота": [1.06, 2.8, 1.3, 1.8, 1.3, 7.4, 6.3, 3.2, 4.0, 3.2, 2.2],
            "Оксид азота": [5.56, 6.4, 1.4, 1.4, 0.8, 3.3, 2.8, 4.4, 8.7, 1.0, 3.2],
            "Сероводород": [29.94, 29.9, 29.9, 4.0, 20.8, 19.8, 13.1, 14.1, 13.5, 21.3, 16.1],
            "Формальдегид": [1.44, 1.6, 3.3, 0.7, 0.3, 0.2, 0.14, 0.4, 0.1, 0.0, 0.0]
        },
        "Алматы": {
                "Пыль": [2.4, 1.8, 1.4, 2.0, 1.8, 1.9, 1.4, 1.6, 1.1, 1.3, 2.0],
                "PM-2.5": [0, 3.9, 4.4, 5.2, 6.3, 5.8, 6.3, 6.0, 4.9, 5.7, 4.7], # 0 там, где нет данных
                "PM-10": [3.3, 3.2, 3.5, 3.4, 3.5, 4.1, 3.3, 3.2, 2.7, 3.1, 2.3],
                "Диоксид серы": [4.0, 2.3, 3.5, 4.0, 4.0, 4.8, 9.8, 4.0, 7.8, 2.7, 2.0],
                "Оксид углерода": [5.2, 3.0, 4.1, 2.5, 3.2, 5.1, 6.3, 3.4, 15.6, 5.7, 4.8],
                "Диоксид азота": [8.7, 5.0, 2.5, 9.1, 9.5, 4.8, 5.3, 5.2, 9.6, 5.1, 5.3],
                "Оксид азота": [5.4, 2.5, 1.8, 4.0, 1.8, 2.4, 2.5, 2.5, 2.5, 2.5, 9.6],
                "Озон": [0, 0, 0, 0, 0, 3.9, 6.7, 9.5, 7.9, 6.4, 0] # Данные появились с 2020
        },
        "Астана": {
                "Взвешенные частицы": [7.6, 8.0, 8.8, 12.6, 9.8, 6.6, 7.8, 1.2, 2.0, 4.2, 12.4],
                "PM-2.5": [0, 2.1, 4.1, 5.5, 7.9, 9.6, 8.7, 9.5, 6.5, 6.7, 3.6],
                "PM-10": [3.3, 3.1, 2.6, 3.3, 7.7, 6.4, 4.7, 5.1, 3.3, 4.3, 1.9],
                "Диоксид серы": [1.4, 3.2, 1.9, 2.3, 4.0, 6.5, 4.0, 4.0, 0.7, 4.0, 1.1],
                "Оксид углерода": [2.2, 2.0, 2.0, 2.6, 7.0, 7.2, 6.2, 3.4, 2.8, 3.2, 3.0],
                "Диоксид азота": [10.2, 7.1, 8.7, 8.4, 6.5, 5.5, 5.0, 5.0, 4.9, 4.9, 4.0],
                "Сероводород": [0, 0, 0, 0, 0, 10.7, 9.4, 12.9, 16.3, 11.3, 16.3],
                "Фтористый водород": [6.35, 7.1, 5.1, 17.2, 19.7, 5.1, 0.5, 5.8, 1.0, 0.4, 0.3],
                "Озон": [0, 0, 0, 0, 0, 0, 1.3, 5.0, 1.8, 7.0, 6.9],
                "Цинк (Zn)": [0, 0, 0, 0, 0, 7.0, 0, 0, 0, 0, 0]
        },
        "Атырау": {
            "Взвешенные вещества": [4.0, 2.4, 2.4, 2.7, 4.2, 2.2, 2.0, 1.8, 1.8, 1.4, 1.8],
            "PM-2.5": [2.4, 0.8, 2.6, 3.8, 1.4, 3.3, 3.1, 4.6, 1.4, 1.1, 1.0],
            "PM-10": [4.8, 1.7, 5.0, 3.1, 4.7, 9.9, 9.0, 3.3, 0.8, 0.6, 0.6],
            "Диоксид серы": [0.57, 0.4, 1.1, 0.2, 0.1, 0.6, 0.8, 2.2, 0.5, 0.3, 14.1],
            "Оксид углерода": [7.03, 1.0, 0.8, 1.2, 4.0, 1.6, 3.4, 1.7, 1.2, 1.6, 16.0],
            "Диоксид азота": [0.88, 0.7, 1.1, 0.9, 0.8, 0.6, 1.8, 3.1, 3.5, 3.4, 11.1],
            "Сероводород": [10.3, 8.9, 17.2, 51.9, 13.6, 16.1, 10.3, 7.7, 4.2, 2.6, 19.7],
            "Аммиак": [0.74, 0.2, 0.2, 1.5, 0.9, 0.7, 1.9, 0.5, 0.5, 0.7, 3.4],
            "Фенол": [0.4, 0, 0.7, 0.4, 0.5, 0.4, 0.4, 0.5, 0.4, 0.5, 1.7]
        },
        "Караганда": {
            "Пыль": [25.6, 1.8, 1.4, 6.0, 0.0, 1.4, 2.0, 4.0, 4.8, 9.0, 8.8],
            "PM-2.5": [9.6, 20.6, 15.9, 20.8, 19.8, 19.8, 20.5, 37.3, 22.6, 26.6, 27.4],
            "PM-10": [8.0, 11.0, 8.5, 11.1, 10.6, 10.6, 11.0, 19.9, 12.1, 14.2, 14.7],
            "Диоксид серы": [1.3, 1.0, 0.9, 0.6, 0.2, 0.5, 0.8, 2.5, 5.4, 0.2, 0.6],
            "Оксид углерода": [3.1, 17.0, 14.5, 5.5, 3.8, 9.0, 2.7, 3.4, 4.2, 4.1, 5.0],
            "Диоксид азота": [3.1, 2.6, 2.3, 1.5, 1.6, 1.0, 1.9, 7.5, 11.1, 1.4, 1.3],
            "Сероводород": [6.3, 6.5, 6.0, 6.3, 8.6, 5.9, 6.4, 6.9, 6.6, 9.4, 8.4],
            "Фенол": [2.2, 2.2, 1.8, 5.0, 1.1, 1.0, 0.8, 2.1, 1.3, 2.2, 4.0],
            "Формальдегид": [0.44, 0.5, 0.54, 0.4, 0.5, 0.46, 0.39, 0.72, 0.52, 1.08, 0.8]
        },        
        "Кокшетау": {
            "Пыль": [2.8, 2.2, 2.2, 2.78, 1.6, 3.3, 0.0, 0.0, 0.0, 0.0, 0.0],
            "PM-2.5": [0.0, 0.3, 1.2, 0.83, 1.2, 0.46, 1.42, 2.0, 2.3, 1.1, 0.7],
            "PM-10": [1.65, 0.2, 0.6, 0.77, 0.81, 0.19, 0.98, 1.1, 1.3, 0.9, 0.6],
            "Диоксид серы": [0.59, 1.43, 0.95, 1.0, 0.02, 0.18, 0.93, 0.56, 0.5, 1.3, 1.2],
            "Оксид углерода": [2.74, 1.0, 0.98, 0.71, 0.57, 0.86, 0.84, 0.96, 2.8, 0.96, 1.6],
            "Диоксид азота": [1.57, 0.91, 1.4, 3.5, 0.95, 0.74, 1.46, 3.0, 3.4, 0.8, 0.7],
            "Оксид азота": [2.12, 2.25, 1.6, 1.34, 2.0, 0.97, 0.89, 2.5, 1.9, 1.0, 0.99]
        },
        "Костанай": {
            "PM-2.5": [0.0, 0.0, 0.0, 325.0, 22.0, 37.0, 119.0, 491.0, 674.0, 1055.0, 128.0],
            "PM-10": [9.0, 899.0, 26.0, 122.0, 2.0, 6.0, 3.0, 0.0, 0.0, 1.0, 66.0],
            "Диоксид серы": [116.0, 0.0, 3.0, 122.0, 3.0, 6.0, 700.0, 895.0, 0.0, 2840.0, 0.0],
            "Оксид углерода": [34.0, 12.0, 39.0, 15.0, 3.0, 70.0, 250.0, 4.0, 56.0, 73.0, 13.0],
            "Диоксид азота": [2754.0, 69.0, 82.0, 43.0, 39.0, 72.0, 0.0, 42.0, 53.0, 717.0, 709.0],
            "Оксид азота": [6764.0, 2601.0, 93.0, 24.0, 9.0, 9.0, 219.0, 32.0, 7.0, 28.0, 618.0],
            "Озон": [0.0, 0.0, 0.0, 0.0, 0.0, 1178.0, 2412.0, 0.0, 0.0, 0.0, 0.0]
        },
        "Кызылорда": {
            "Взвешенные вещества": [1.0, 0.6, 2.0, 0.0, 1.0, 0.1, 0.3, 0.28, 0.32, 0.2, 0.8],
            "PM-2.5": [0.0, 3.2, 2.1, 1.6, 2.1, 0.0, 0.91, 0.61, 1.33, 0.6, 0.3],
            "PM-10": [1.2, 3.1, 3.4, 0.0, 0.3, 0.0, 0.97, 0.95, 1.0, 1.0, 0.7],
            "Диоксид серы": [0.6, 0.7, 0.6, 0.8, 0.7, 0.3, 0.64, 0.33, 0.42, 0.9, 4.2],
            "Оксид углерода": [0.9, 2.0, 1.9, 0.8, 4.9, 0.1, 0.97, 0.74, 0.99, 1.6, 1.8],
            "Диоксид азота": [1.0, 1.7, 1.4, 1.1, 2.3, 0.3, 1.0, 0.72, 1.0, 1.9, 0.8],
            "Оксид азота": [0.3, 1.0, 1.1, 0.9, 1.4, 0.0, 0.97, 0.41, 0.97, 1.8, 1.1],
            "Озон": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.06, 1.0, 1.0, 4.0, 0.3],
            "Сероводород": [0.3, 0.1, 0.1, 0.1, 0.3, 0.1, 0.78, 0.0, 0.0, 0.0, 0.0],
            "Формальдегид": [10.0, 0.3, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        },
        "Павлодар": {
            "Пыль": [2.6, 1.2, 2.0, 1.4, 1.8, 4.2, 1.2, 1.8, 1.8, 0.6, 0.8],
            "PM-2.5": [5.38, 2.9, 2.8, 1.4, 1.8, 1.9, 3.5, 2.7, 1.3, 0.0, 1.6],
            "PM-10": [3.27, 2.6, 3.2, 1.1, 1.2, 3.2, 3.0, 3.4, 1.6, 0.0, 1.3],
            "Аммиак": [6.68, 0.4, 1.0, 0.4, 0.9, 1.0, 0.3, 0.7, 1.0, 0.8, 0.8],
            "Диоксид азота": [1.49, 3.4, 3.2, 1.7, 5.0, 2.2, 1.0, 2.2, 7.6, 2.8, 0.6],
            "Диоксид серы": [0.6, 1.0, 0.7, 1.0, 0.9, 1.0, 1.0, 0.8, 2.5, 1.0, 1.4],
            "Оксид углерода": [4.37, 6.0, 3.8, 2.3, 2.3, 1.84, 2.24, 3.9, 1.0, 9.3, 9.5],
            "Сероводород": [6.83, 4.0, 3.8, 1.4, 2.0, 1.9, 1.55, 2.1, 3.7, 3.0, 6.4],
            "Озон": [0.94, 4.9, 1.0, 2.4, 1.0, 1.0, 1.0, 0.9, 0.8, 4.1, 2.1],
            "Хлор": [0.2, 0.1, 0.2, 0.3, 0.7, 0.7, 0.6, 0.5, 1.5, 0.7, 0.3],
            "Хлористый водород": [2.0, 0.4, 0.4, 0.5, 1.5, 1.4, 1.45, 1.4, 0.5, 2.4, 1.4]
        },
        "Петропавловск": {
            "Взвешенные частицы": [0.2, 0.8, 0.4, 0.8, 0.8, 0.6, 2.0, 0.6, 0.0, 0.4, 0.2],
            "PM-2.5": [3.21, 1.8, 0.4, 1.6, 1.4, 1.2, 0.2, 0.6, 0.2, 0.0, 0.0],
            "PM-10": [2.98, 3.3, 0.4, 1.0, 0.8, 2.3, 1.4, 1.1, 0.1, 0.0, 0.0],
            "Диоксид серы": [0.7, 4.0, 0.5, 1.0, 0.7, 0.2, 0.4, 1.0, 0.5, 0.9, 3.3],
            "Диоксид азота": [3.84, 0.9, 0.0, 2.1, 1.1, 2.8, 2.7, 2.7, 3.4, 2.4, 3.6],
            "Оксид углерода": [1.4, 2.0, 3.7, 1.2, 0.9, 2.2, 2.8, 0.0, 1.4, 3.6, 1.1],
            "Сероводород": [9.28, 24.4, 0.4, 5.6, 6.4, 6.6, 15.2, 10.5, 9.7, 9.8, 23.8],
            "Формальдегид": [0.18, 0.4, 0.5, 0.9, 0.8, 0.8, 6.0, 2.1, 2.1, 0.6, 0.2],
            "Аммиак": [2.58, 9.4, 0.3, 0.8, 1.2, 1.2, 4.1, 5.0, 0.0, 0.0, 0.0],
            "Фенол": [0.3, 1.3, 0.4, 2.1, 1.7, 0.9, 2.0, 2.0, 1.0, 0.8, 0.4]
        },
        "Семей": {
            # Заполняем 2015-2022 нулями, 2023-2025 — вашими данными
            "Диоксид серы": [0, 0, 0, 0, 0, 0, 0, 0, 4.72, 4.50, 4.92],
            "Оксид углерода": [0, 0, 0, 0, 0, 0, 0, 0, 2.60, 2.70, 4.94],
            "Диоксид азота": [0, 0, 0, 0, 0, 0, 0, 0, 1.91, 1.74, 1.68],
            "Оксид азота": [0, 0, 0, 0, 0, 0, 0, 0, 1.84, 3.20, 1.84],
            "Озон": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.20, 0.62],
            "Сероводород": [0, 0, 0, 0, 0, 0, 0, 0, 4.13, 4.75, 2.46]
        },
        "Тараз": {
            "Взвешенные вещества": [3.4, 2.6, 4.2, 2.0, 3.4, 1.2, 2.0, 0.6, 0.8, 1.8, 1.0],
            "PM-10": [3.3, 2.7, 1.5, 0.8, 1.7, 0.3, 2.6, 0.79, 0.0, 0.0, 0.0],
            "Диоксид серы": [0.7, 0.4, 4.0, 0.1, 0.7, 0.8, 0.5, 0.65, 0.6, 0.9, 0.9],
            "Оксид углерода": [7.6, 3.0, 3.0, 2.2, 3.2, 2.8, 3.5, 3.45, 4.0, 2.6, 2.4],
            "Диоксид азота": [2.7, 1.3, 1.5, 3.2, 1.9, 1.9, 1.7, 1.05, 1.6, 0.9, 1.0],
            "Сероводород": [1.6, 2.5, 3.0, 4.1, 4.3, 5.4, 0.0, 2.14, 6.7, 3.9, 3.6],
            "Фтористый водород": [2.7, 2.95, 1.0, 1.15, 1.4, 0.35, 0.8, 0.8, 0.0, 1.5, 0.75],
            "Формальдегид": [1.1, 0.6, 0.92, 0.86, 0.56, 0.99, 0.72, 1.04, 0.68, 0.82, 0.48]
        },        
        "Туркестан": {
            "Взвешенные частицы": [0, 0, 0, 3.3, 1.98, 2.0, 1.97, 1.85, 2.21, 0, 0],
            "PM-2.5": [0, 0, 0, 0, 0, 0, 0, 0, 2.29, 0, 0],
            "PM-10": [0, 0, 3.31, 0, 0, 0, 0, 0, 3.33, 0, 0],
            "Диоксид азота": [1.0, 0.3, 1.0, 1.1, 1.1, 1.8, 1.2, 3.71, 3.8, 3.8, 3.8],
            "Диоксид серы": [0.0, 0.2, 0.5, 1.5, 0.7, 0.5, 0.5, 3.19, 5.9, 4.2, 4.9],
            "Оксид азота": [0.6, 0.4, 0.8, 0.7, 0.6, 1.8, 1.9, 0.04, 1.9, 1.9, 1.8],
            "Оксид углерода": [6.7, 3.0, 3.4, 2.9, 2.2, 1.9, 1.1, 2.32, 2.8, 2.2, 2.8],
            "Сероводород": [0, 0.5, 0, 4.4, 6.9, 4.1, 0, 14.56, 3.7, 4.6, 3.7],
            "Озон": [0, 0.9, 0, 0, 0, 0, 0.6, 0.9, 3.3, 1.6, 0.6]
        },
        "Усть-Каменогорск": {
            "Пыль": [6.0, 2.6, 2.8, 4.4, 4.0, 2.0, 1.8, 0.6, 0.0, 0.0, 0.0],
            "PM-2.5": [0, 0, 0, 0, 0, 4.5, 6.1, 0.77, 0.03, 0.09, 0.0],
            "PM-10": [0, 0.0, 3.3, 3.3, 3.3, 3.3, 3.3, 3.3, 0.36, 1.5, 0.05],
            "Диоксид серы": [5.0, 8.8, 7.2, 11.4, 9.9, 10.9, 9.9, 8.7, 6.93, 1.15, 4.78],
            "Диоксид азота": [3.3, 2.3, 3.8, 2.8, 3.9, 2.1, 1.4, 9.7, 2.22, 2.47, 2.66],
            "Сероводород": [5.0, 6.1, 62.1, 131.7, 23.1, 20.4, 7.9, 8.2, 5.28, 1.0, 4.23],
            "Фенол": [2.1, 1.8, 4.5, 2.1, 1.3, 1.5, 3.7, 0.9, 2.2, 5.44, 2.5],
            "Фтористый водород": [0, 0, 3.0, 1.9, 1.2, 1.3, 1.5, 0.8, 1.35, 2.1, 1.75],
            "Хлор": [0.4, 0.9, 1.4, 0.7, 0.9, 0.7, 0.9, 0.6, 0.9, 2.0, 1.2],
            "Хлористый водород": [0, 0, 0.7, 0.8, 0.8, 1.1, 1.3, 0.9, 2.0, 6.0, 2.4],
            "Серная кислота": [0.93, 1.17, 1.6, 1.67, 0.6, 1.2, 0.7, 0.2, 0.27, 2.65, 1.63],
            "Оксид углерода": [2.4, 3.0, 3.4, 5.7, 2.9, 4.1, 2.3, 4.3, 2.59, 6.61, 5.38],
            "Аммиак": [0.46, 0.36, 0, 0.27, 0, 0.3, 0.3, 0.4, 0, 2.13, 1.19]
        },
        "Уральск": {
            "PM-2.5": [0.0, 0.0, 1.4, 0.9, 1.6, 1.7, 0.8, 0.0, 0.0, 0.0, 0.0],
            "PM-10": [0.0, 0.0, 2.2, 0.9, 3.4, 1.0, 0.9, 0.0, 0.0, 0.0, 0.0],
            "Диоксид серы": [0.0, 0.0, 3.2, 1.0, 0.2, 1.9, 0.2, 0.5, 0.5, 2.4, 1.75],
            "Оксид углерода": [0.0, 0.0, 4.5, 1.9, 2.3, 2.3, 4.3, 2.7, 2.5, 2.4, 1.26],
            "Диоксид азота": [0.0, 0.0, 1.0, 1.0, 1.1, 1.8, 2.1, 2.42, 1.7, 1.1, 0.96],
            "Оксид азота": [0.0, 0.0, 1.3, 1.0, 2.3, 1.3, 0.9, 1.62, 1.0, 0.7, 0.75],
            "Сероводород": [0.0, 0.0, 4.0, 1.7, 4.0, 4.1, 1.0, 1.81, 6.3, 7.3, 1.73],
            "Озон": [0.0, 0.0, 1.0, 1.0, 0.9, 1.0, 0.8, 6.68, 0.5, 0.9, 2.27],
            "Аммиак": [0.0, 0.0, 0.31, 0.6, 0.6, 2.7, 0.9, 0.28, 0.1, 0.6, 1.0]
        },
        "Шымкент": {
            "Взвешенные вещества": [1.8, 1.4, 1.4, 1.8, 1.0, 1.0, 1.0, 0.8, 0.8, 0.8, 1.0],
            "PM-2.5": [4.1, 2.4, 5.9, 3.8, 2.6, 3.1, 1.5, 1.52, 0.3, 0.0, 0.0],
            "PM-10": [17.3, 4.3, 9.7, 3.2, 3.9, 2.8, 3.9, 1.08, 0.3, 0.0, 0.0],
            "Диоксид серы": [8.9, 0.4, 0.8, 0.0, 0.2, 0.0, 0.9, 0.73, 3.2, 7.8, 0.5],
            "Оксид углерода": [4.0, 3.0, 2.6, 3.6, 3.8, 2.8, 1.7, 3.35, 2.8, 2.0, 2.2],
            "Диоксид азота": [3.0, 2.0, 1.0, 3.3, 4.2, 2.9, 0.6, 0.6, 1.8, 3.1, 0.5],
            "Сероводород": [9.5, 4.4, 3.4, 0.4, 0.4, 0.8, 2.5, 3.23, 4.9, 185.8, 3.6],
            "Аммиак": [7.4, 4.1, 2.0, 0.9, 1.3, 0.4, 0.2, 0.5, 0.4, 0.4, 0.2],
            "Формальдегид": [1.7, 1.8, 1.5, 0.9, 0.8, 3.0, 0.8, 0.72, 0.6, 0.6, 0.6]
        },           

    }          
    


    # --- 2. ИНТЕРФЕЙС ---
    st.set_page_config(page_title="Эко-Мониторинг Казахстана", layout="wide")
    st.title("🍀 Экологический мониторинг городов Казахстана")

    # Выбор города — он стоит НАД вкладками, поэтому влияет на всё сразу
    city = st.selectbox(
        "Выберите город для анализа:", 
        list(kazakhstan_pollution_data.keys()), 
        key="main_city_selector"
    )

    # Сразу извлекаем данные для выбранного города
    heatmap_data, current_pollutants = kazakhstan_pollution_data[city]

    st.divider() # Красивая линия под выбором города

    # --- 4. СОЗДАНИЕ ВКЛАДОК ---
    tab1, tab2 = st.tabs([
        "📊 Тепловая карта (2025)", 
        "📈 Годовая динамика"
    ])

    with tab1:
        st.subheader(f"Карта превышений ПДК по месяцам: {city}")
        months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]
        
        fig_heat = px.imshow(
            heatmap_data,
            labels=dict(x="Месяц", y="Примесь", color="Случаев > ПДК"),
            x=months,
            y=current_pollutants,
            color_continuous_scale="Reds",
            aspect="auto",
            text_auto=True
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        st.info("💡 Насыщенность цвета показывает частоту превышений нормы.")
        
    with tab2:
        st.subheader(f"📈 Историческая динамика загрязнения: {city}")

        city_history = all_historical_data.get(city, {})

        if not city_history:
            st.error(f"Данные по истории для города {city} отсутствуют.")
        else:
            # --- БЛОК УПРАВЛЕНИЯ ---
            col1, col2, col3 = st.columns([3, 1.5, 1])
            
            with col2:
                years = list(range(2015, 2026))
                year_range = st.select_slider(
                    "Период:", options=years, value=(2015, 2025), key="slider_tab2"
                )

            with col1:
                selected_pollutants = st.multiselect(
                    "Выберите примеси:",
                    options=list(city_history.keys()),
                    default=list(city_history.keys())[:3]
                )
                
            with col3:
                # Важнейшая функция для ваших данных
                use_log = st.checkbox("Логарифм. шкала", help="Используйте при больших пиках (напр. Шымкент 185.8)")

            # --- ПОДГОТОВКА ДАННЫХ ---
            start_idx = years.index(year_range[0])
            end_idx = years.index(year_range[1]) + 1
            filtered_years = years[start_idx:end_idx]

            fig_line = go.Figure()

            # Цветовые зоны риска (фоновые полосы)
            fig_line.add_hrect(y0=0, y1=1, fillcolor="rgba(0, 255, 0, 0.1)", line_width=0, annotation_text="Безопасно")
            fig_line.add_hrect(y0=1, y1=5, fillcolor="rgba(255, 255, 0, 0.05)", line_width=0, annotation_text="Повышенный риск")

            # Отрисовка линий
            for p in selected_pollutants:
                values = city_history[p][start_idx:end_idx]
                fig_line.add_trace(go.Scatter(
                    x=filtered_years, y=values, name=p,
                    mode='lines+markers',
                    line=dict(width=3 if city == "Шымкент" and p == "Сероводород" else 2),
                    hovertemplate="<b>%{x} год</b><br>Кратность: %{y} ПДК<extra></extra>"
                ))

            fig_line.update_layout(
                yaxis_type="log" if use_log else "linear",
                yaxis_title="Кратность превышения ПДК",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=0, r=0, t=30, b=0),
                height=500
            )
            st.plotly_chart(fig_line, use_container_width=True)

            # --- БЛОК АВТОМАТИЧЕСКОЙ АНАЛИТИКИ ---
            st.markdown("### 🔍 Аналитический разбор")
            
            # Собираем статистику по выбранным веществам
            stats = []
            for p in selected_pollutants:
                vals = [v for v in city_history[p][start_idx:end_idx] if v > 0]
                if vals:
                    max_val = max(vals)
                    max_year = filtered_years[vals.index(max_val)]
                    avg_val = sum(vals) / len(vals)
                    stats.append({"Примесь": p, "Пик (ПДК)": max_val, "Год пика": max_year, "Среднее": round(avg_val, 2)})

            if stats:
                c1, c2 = st.columns([2, 1])
                with c1:
                    # Находим самый опасный показатель
                    worst = max(stats, key=lambda x: x["Пик (ПДК)"])
                    if worst["Пик (ПДК)"] > 10:
                        st.warning(f"⚠️ **Критический уровень:** Вещество **{worst['Примесь']}** достигало **{worst['Пик (ПДК)']} ПДК** в {worst['Год пика']} году.")
                    else:
                        st.success(f"✅ В выбранный период {year_range[0]}-{year_range[1]} критических скачков (>10 ПДК) не обнаружено.")
                    
                    # Общая тенденция
                    last_vals = [city_history[p][end_idx-1] for p in selected_pollutants]
                    avg_now = sum(last_vals) / len(last_vals) if last_vals else 0
                    trend = "снижается" if avg_now < stats[0]["Среднее"] else "растет или стабильно"
                    st.write(f"📊 Общий экологический фон к 2025 году: **{trend}** (среднее по выборке: {round(avg_now, 2)} ПДК).")

                with c2:
                    # Компактная таблица рекордов
                    st.dataframe(stats, hide_index=True)

            st.caption("Данные основаны на ежегодных отчетах мониторинга качества атмосферного воздуха РК.")
   

    # --- ОБЩИЙ НАСТРОЙКИ СТРАНИЦЫ ---
    st.set_page_config(page_title="Мониторинг вод РК", layout="wide")

    # --- УНИВЕРСАЛЬНАЯ ФУНКЦИЯ ОТРИСОВКИ ---
    def render_charts(df, key_prefix):
        st.divider()
        col_chart, col_info = st.columns([2, 1])

        with col_chart:
            # Цветовая логика: зеленый (1), желтый (3), оранжевый (4-5), красный (6)
            colors = []
            for c in df['Класс']:
                if c <= 1: colors.append('#2ecc71')
                elif c <= 3: colors.append('#f1c40f')
                elif c <= 5: colors.append('#e67e22')
                else: colors.append('#e74c3c')
                
            fig = go.Figure(go.Bar(
                x=df['Класс'], 
                y=df['Объект'], 
                orientation='h', 
                marker_color=colors,
                text=df['Класс'],
                textposition='auto'
            ))
            fig.update_layout(
                title="Классы качества воды (2025 год)", 
                yaxis=dict(autorange="reversed"), 
                height=400,
                xaxis_title="Класс (чем меньше, тем чище)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_info:
            selected_obj = st.selectbox("Подробная справка по объекту:", df['Объект'], key=f"select_{key_prefix}")
            obj_info = df[df['Объект'] == selected_obj].iloc[0]
            
            st.info(f"### {selected_obj}")
            st.write(f"**Характеристика:** {obj_info['Характеристика']}")
            st.write(f"**Основные загрязнители:** {obj_info['Показатели']}")
            st.caption(f"ℹ️ {obj_info['Пригодность']}")

    # --- ФУНКЦИИ ОБЛАСТЕЙ ---
    def show_almaty_dashboard():
        st.subheader("📍 г. Алматы, Алматинская область и область Жетысу")  
        st.markdown("*Наблюдение ведется на 5 водных объектах (17 створа) по 37 показателям.*")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Створов", "42")
        c2.metric("Показателей", "44")
        c3.metric("Лидер", "р. Тургень")
        c4.metric("Зона риска", "не обнаружены")

        water_2025 = [
            {"Объект": "р. Киши Алматы", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "медь"},
            {"Объект": "р. Есентай", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "медь"},
            {"Объект": "р. Улкен Алматы", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "железо общее"},
            {"Объект": "р. Иле", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний, медь"},
            {"Объект": "р. Шилик", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний, медь"},
            {"Объект": "р. Шарын", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний, медь"},
            {"Объект": "р. Текес", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "аммоний ион, медь, магний"},
            {"Объект": "р. Коргас", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "медь"},
            {"Объект": "р. Баянкол", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "медь"},
            {"Объект": "р. Есик", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "медь"},
            {"Объект": "р. Каскелен", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний, медь"},
            {"Объект": "р. Каркара", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний"},
            {"Объект": "р. Тургень", "Класс": 1, "Характеристика": "очень хорошее", "Пригодность": "Для всех видов использования", "Показатели": "В норме"},
            {"Объект": "р. Талгар", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "медь"},
            {"Объект": "р. Темерлик", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний, медь"},            
            {"Объект": "р. Лепси", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "медь, железо общее"},
            {"Объект": "р. Аксу", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний, железо общее, медь"},
            {"Объект": "р. Каратал", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "железо общее, медь"},
            {"Объект": "вдхр. Капшагай", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний"}  
        ]
        render_charts(pd.DataFrame(water_2025), "almaty")
        
        
    def show_akmola_dashboard():
        st.subheader("📍 г. Астана и Акмолинская область")  
        st.markdown("*Наблюдение ведется на 25 водных объектах (60 створа) по 36 показателям.*")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Створов", "60")
        c2.metric("Показателей", "36")
        c3.metric("Лидер", "Астанинское вдхр.")
        c4.metric("Зона риска", "р. Сарыбулак")

        water_2025 = [
            {"Объект": "Астанинское вдхр.", "Класс": 1, "Характеристика": "очень хорошее", "Пригодность": "Для всех видов использования", "Показатели": "В норме"},
            {"Объект": "р. Есиль", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний, фосфор"},
            {"Объект": "р. Акбулак", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "Только транспорт/гидроэнергетика", "Показатели": "хлориды"},
            {"Объект": "р. Сарыбулак", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "Только транспорт/гидроэнергетика", "Показатели": "хлориды, аммоний-ион"},
            {"Объект": "р. Нура", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "Только транспорт/гидроэнергетика", "Показатели": "железо общее, взвещенные вещества"},
            {"Объект": "канал Нура-Есиль", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний, сульфаты"},
            {"Объект": "р. Беттыбулак", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "аммоний-ион, медь"},
            {"Объект": "р. Жабай", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний"},
            {"Объект": "р. Силеты", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний, аммоний-ион"},
            {"Объект": "р. Аксу", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "Только транспорт/гидроэнергетика", "Показатели": "хлориды"},
            {"Объект": "р. Кылшыкты", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "Только транспорт/гидроэнергетика", "Показатели": "хлориды"},
            {"Объект": "р. Шагалалы", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "Нужна очистка для питья", "Показатели": "магний, медь"},
            {"Объект": "р. Ащылыайрык", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "Только транспорт/гидроэнергетика", "Показатели": "хлориды"}                        
        ]
        render_charts(pd.DataFrame(water_2025), "akmola")

    def show_atyrau_dashboard(): 
        st.subheader("📍 Атырауская область")  
        st.markdown("*Включая мониторинг Северной части Каспийского моря.*")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Створов", "21")
        c2.metric("Показателей", "43")
        c3.metric("Лидер", "нет")
        c4.metric("ЭВЗ", "не обнаружены")

        water_2025 = [
            {"Объект": "р. Жайык", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "БПК5, ХПК, магний, нефтепродукты"},
            {"Объект": "р. Кигаш", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "нужна очистка", "Показатели": "БПК5, ХПК, магний, кадмий, нефтепродукты"},
            {"Объект": "р. Перетаска", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "БПК5, ХПК, магний, нефтепродукты"},
            {"Объект": "р. Яик", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "нужна очистка", "Показатели": "БПК5, ХПК, магний, нефтепродукты"},
            {"Объект": "протока Шаранова", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "БПК5, ХПК, магний, нефтепродукты"},
            {"Объект": "р. Эмба", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "нужна очистка", "Показатели": "БПК5, магний, сульфаты, нефтепродукты"}
            
        ]
        render_charts(pd.DataFrame(water_2025), "atyrau")
        
    def show_aktobe_dashboard(): 
        st.subheader("📍 Актюбинская область")  
        st.markdown("*Наблюдение ведется на 12 водных объектах (19 створа) по 42 показателям.*")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Створов", "19")
        c2.metric("Показателей", "42")
        c3.metric("Лидер", "нет")
        c4.metric("ЭВЗ", "не обнаружены")

        water_2025 = [
            {"Объект": "р. Елек", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "фенолы"},
            {"Объект": "р. Каргалы", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "фенолы"},
            {"Объект": "р. Эмба", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "фенолы"},
            {"Объект": "р. Темир", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "фенолы"},                        
            {"Объект": "р. Орь", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "фенолы"},
            {"Объект": "р. Актасты", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "взвещенные вещества, фенолы"},
            {"Объект": "р. Косестек", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "фенолы"},
            {"Объект": "р. Ойыл", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "фенолы"},
            {"Объект": "р. Улькен Кобда", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "фенолы"},
            {"Объект": "р. Кара Кобда", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "взвещенные вещества, фенолы"},
            {"Объект": "р. Ыргыз", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "фенолы"}          
        ]
        render_charts(pd.DataFrame(water_2025), "aktobe")

        
    def show_karaganda_dashboard(): 
        st.subheader("📍 Карагандинская и Улытауская области")  
        st.markdown("*Наблюдение ведется на 13 водных объектах (42 створа) по 33 показателям.*")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Створов", "42")
        c2.metric("Показателей", "33")
        c3.metric("Лидер", "нет")
        c4.metric("ЭВЗ", "не обнаружены")

        water_2025 = [
            {"Объект": "р. Нура", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "технические нужды", "Показатели": "взвещенные вещества"},
            {"Объект": "вдхр. Самаркан", "Класс": 5, "Характеристика": "очень загрязненное", "Пригодность": "не пригодна для всех видов водопользования", "Показатели": "взвещенные вещества"},
            {"Объект": "р. Сокыр", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "технические нужды", "Показатели": "аммоний-ион, фосфор общий, фосфаты"},
            {"Объект": "р. Шерубайнура", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "технические нужды", "Показатели": "аммоний-ион, фосфор общий, фосфаты"},                        
            {"Объект": "канал им. К. Сатпаева", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "взвещенные вещества"},
            {"Объект": "вдхр. Кенгир", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "сульфаты, магний, марганец, медь"},
            {"Объект": "р. Кара-Кенгир", "Класс": 5, "Характеристика": "очень загрязненное", "Пригодность": "не пригодна для всех видов водопользования", "Показатели": "минерализация, аммоний-мон"}     
        ]
        render_charts(pd.DataFrame(water_2025), "karaganda")

    def show_zko_dashboard(): 
        st.subheader("📍 Западно-Казахстанская область")  
        st.markdown("*Наблюдение ведется на 9 водных объектах (18 створа) по 43 показателям.*")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Створов", "18")
        c2.metric("Показателей", "43")
        c3.metric("Лидер", "нет")
        c4.metric("ЭВЗ", "не обнаружены")

        water_2025 = [
            {"Объект": "р. Жайык", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "фосфаты, БПК5, магний, железо общее"},
            {"Объект": "р. Шанан", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "фосфаты, БПК5, магний, железо общее"},
            {"Объект": "р. Дерколь", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "фосфаты, БПК5, магний, железо общее, фосфор общий"},
            {"Объект": "р. Елек", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "фосфаты, БПК5, магний, железо общее"},                        
            {"Объект": "р. Шынгырлау", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "фосфаты, БПК5, магний, железо общее"},
            {"Объект": "р. Сарыозен", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "фосфаты, БПК5, магний, железо общее"},
            {"Объект": "р. Караозен", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "фосфаты, БПК5, магний, железо общее"},     
            {"Объект": "Кошимский канал", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "фосфаты, БПК5, магний, железо общее"}     
        ]
        render_charts(pd.DataFrame(water_2025), "karaganda")
        
        
    def show_turkestan_dashboard(): 
        st.subheader("📍 Туркестанская область")  
        st.markdown("*Наблюдение ведется на 7 водных объектах (12 створа) по 40 показателям.*")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Створов", "12")
        c2.metric("Показателей", "40")
        c3.metric("Лидеры", "Аксу, Арыс")
        c4.metric("Зона риска", "р. Келес")

        water_2025 = [
            {"Объект": "р. Аксу", "Класс": 1, "Характеристика": "очень хорошее", "Пригодность": "Все категории", "Показатели": "В норме"},
            {"Объект": "р. Арыс", "Класс": 1, "Характеристика": "очень хорошее", "Пригодность": "Все категории", "Показатели": "В норме"},
            {"Объект": "р. Катта-бугунь", "Класс": 1, "Характеристика": "очень хорошее", "Пригодность": "Все категории", "Показатели": "В норме"},
            {"Объект": "р. Келес", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "Технические нужды", "Показатели": "взвешенные вещества"},
            {"Объект": "р. Сырдария", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "сульфаты"},
            {"Объект": "р. Бадам", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "сульфаты"},
            {"Объект": "Шардара вдхр.", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "сульфаты"}
        ]
        render_charts(pd.DataFrame(water_2025), "turkestan")
        
        
    def show_Severo_Kazakhstanskaya_dashboard(): 
            st.subheader("📍 Северо-Казахстанская область")  
            st.markdown("*Наблюдение ведется на 2 водных объектах (6 створа) по 47 показателям.*")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Створов", "6")
            c2.metric("Показателей", "47")
            c3.metric("Лидер", "нет")
            c4.metric("ЭВЗ", "не обнаружены")

            water_2025 = [
                {"Объект": "р. Есиль", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "фенолы, взвешенные вещества"},
                {"Объект": "Сергеевское вдхр.", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "для орошения и промышленности,для хозяйственно питьевого водоснабжения требуется методы глубокой водоподготовки", "Показатели": "фенолы, БПК5"}
            ]
            render_charts(pd.DataFrame(water_2025), "Severo_Kazakhstanskaya")

    def show_kostanay_dashboard(): 
            st.subheader("📍 Костанайская область")  
            st.markdown("*Наблюдение ведется на 11 водных объектах (16 створа) по 37 показателям.*")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Створов", "16")
            c2.metric("Показателей", "37")
            c3.metric("Лидер", "нет")
            c4.metric("ЭВЗ", "не обнаружены")

            water_2025 = [
     {"Объект": "р. Тобыл", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "минерализация, хлориды, магний"},
     {"Объект": "р. Айет ", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "цинк, никель, взвешенные вещества"},
     {"Объект": "р. Обаган ", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "минерализация, хлориды, магний"},
     {"Объект": "р. Тогызак ", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "цинк, никель"},  
     {"Объект": "р. Уй ", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "взвешенные вещества, марганец, никель, цинк"},  
     {"Объект": "р. Желкуар", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "цинк, никель, магний"},
     {"Объект": "р. Торгай", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "цинк, минерализация, никель,БПК5"},
     {"Объект": "Каратомар вдхр.", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "взвешенные вещества, БПК5, никель, цинк"}, 
     {"Объект": "Жогаргы Тобыл вдхр.", "Класс": 5, "Характеристика": "очень загрязненное", "Пригодность": "не пригодна для всех видов водопользования", "Показатели": "взвещенные вещества"},
     {"Объект": "Аманкельды вдхр.", "Класс": 5, "Характеристика": "очень загрязненное", "Пригодность": "не пригодна для всех видов водопользования", "Показатели": "взвещенные вещества"},
     {"Объект": "Шортанды вдхр.", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "хлориды"}
            ]
            render_charts(pd.DataFrame(water_2025), "kostanay")


    def show_vko_dashboard(): 
            st.subheader("📍 Восточно-Казахстанкая область")  
            st.markdown("*Наблюдение ведется на 19 водных объектах (53 створа) по 48 показателям.*")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Створов", "53")
            c2.metric("Показателей", "48")
            c3.metric("Лидер", "р. Арасан")
            c4.metric("ЭВЗ", "не обнаружены")

            water_2025 = [

     {"Объект": "р. Кара Ертис ", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "взвешенные вещества"},
     {"Объект": "р. Ертис ", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "цинк"},
     {"Объект": "р. Буктырма", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "железо общее, медь, марганец"},
     {"Объект": "р. Брекса", "Класс": 5, "Характеристика": "очень загрязненное", "Пригодность": "не пригодна для всех видов водопользования", "Показатели": "цинк"},
     {"Объект": "р. Тихая", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "цинк"},
     {"Объект": "р. Ульби", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "цинк"},
     {"Объект": "р. Глубочанка", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "цинк"},
     {"Объект": "р. Красноярка", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "цинк"},
     {"Объект": "р. Оба ", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "цинк"},
     {"Объект": "р. Емель ", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "взвешенные вещества"},
     {"Объект": "р. Аягоз ", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "взвешенные вещества"},
     {"Объект": "р. Уржар ", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "взвешенные вещества"},
     {"Объект": "р. Маховка", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "БПК5,  магний, железо общее, аммоний ион, медь, марганец"},
     {"Объект": "р. Секисовка", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "железо общее, медь, марганец, аммоний ион"},
     {"Объект": "р. Арасан", "Класс": 1, "Характеристика": "очень хорошее", "Пригодность": "Для всех видов использования", "Показатели": "В норме"},
     {"Объект": "р. Киши Каракожа ", "Класс": 6, "Характеристика": "высоко загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "кадмий, свинец, медь, цинк, марганец, магний, железо общее"},
     {"Объект": "Усть-Каменогорское вдхр.", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "медь"},
     {"Объект": "Буктырма вдхр.", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "медь"}
            ]
            render_charts(pd.DataFrame(water_2025), "vko")


    def show_kyzylorda_dashboard(): 
            st.subheader("📍 Кызылординская область")  
            st.markdown("*Наблюдение ведется на 2 водных объектах (7 створа) по 33 показателям.*")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Створов", "7")
            c2.metric("Показателей", "33")
            c3.metric("Лидер", "нет")
            c4.metric("ЭВЗ", "не обнаружены")

            water_2025 = [

     {"Объект": "р. Сырдария", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "минерализация, сульфаты, железо общее, медь, магний"}
            ]
            render_charts(pd.DataFrame(water_2025), "kyzylorda")


    def show_pavlodar_dashboard(): 
            st.subheader("📍 Павлодарская область")  
            st.markdown("*Наблюдение ведется на 5 водных объектах (16 створа) по 48 показателям.*")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Створов", "16")
            c2.metric("Показателей", "48")
            c3.metric("Лидер", "нет")
            c4.metric("ЭВЗ", "не обнаружены")

            water_2025 = [

     {"Объект": "р. Ертис", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "медь"},
     {"Объект": "р. Усолка", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "медь"}
            ]
            render_charts(pd.DataFrame(water_2025), "pavlodar")

    def show_zhambul_dashboard(): 
            st.subheader("📍 Жамбылская область")  
            st.markdown("*Наблюдение ведется на 8 водных объектах (13 створа) по 36 показателям.*")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Створов", "13")
            c2.metric("Показателей", "36")
            c3.metric("Лидер", "нет")
            c4.metric("ЭВЗ", "есть")

            water_2025 = [

     {"Объект": "р. Талас", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "ХПК, сульфаты, магний, медь"},
     {"Объект": "р. Асса", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "взвешенные вещества"},
     {"Объект": "р. Шу", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "БПК5, ХПК, сульфаты, магний, медь"},
     {"Объект": "р. Аксу ", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "ХПК"},
     {"Объект": "р. Карабалта", "Класс": 5, "Характеристика": "очень загрязненное", "Пригодность": "не пригодна для всех видов водопользования", "Показатели": "сульфаты"},
     {"Объект": "р. Токташ", "Класс": 3, "Характеристика": "умеренно загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "БПК5, ХПК, сульфаты, магний, медь, минерализация, сухой остаток"},
     {"Объект": "р. Тасоткель", "Класс": 4, "Характеристика": "загрязненное", "Пригодность": "рекреация без ограничений", "Показатели": "ХПК"}
            ]
            render_charts(pd.DataFrame(water_2025), "zhambul")




    def show_mangystau_dashboard(): 
            st.subheader("📍 Жамбылская область")  
            st.markdown("*Наблюдение ведется на 0 водных объектах (0 створа) по 29 показателям.*")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Створов", "0")
            c2.metric("Показателей", "29")
            c3.metric("Лидер", "нет")
            c4.metric("ЭВЗ", "не обнаружены")

            water_2025 = [
            ]
            render_charts(pd.DataFrame(water_2025), "mangystau")

        

    # --- ГЛАВНАЯ ЛОГИКА ПРИЛОЖЕНИЯ ---

    st.title("💧 Мониторинг качества поверхностных вод Казахстана")

    # Создаем выбор области вверху (или можно в st.sidebar.selectbox)
    region = st.selectbox(
        "Выберите регион для просмотра данных:",
        ["Акмолинская область", "Атырауская область", "Туркестанская область", "Карагандинская область", "Алматы и Жетісу"]
    )

    # Переключатель отображения
    if region == "Акмолинская область":
        show_akmola_dashboard()
    elif region == "Атырауская область":
        show_atyrau_dashboard()
    elif region == "Туркестанская область":
        show_turkestan_dashboard()
    elif region == "г. Алматы, Алматинская область и область Жетысу":
        show_almaty_dashboard()
    elif region == "Актюбинская область":
        show_aktobe_dashboard()
    elif region == "Западно-Казахстанская область":
        show_zko_dashboard()
    elif region == "Северо-Казахстанская область":
        show_Severo_Kazakhstanskaya_dashboard()
    elif region == "Костанайская область":
        show_kostanay_dashboard()
    elif region == "Восточно-Казахстанкая область":
        show_vko_dashboard()
    elif region == "Кызылординская областьи":
        show_kyzylorda_dashboard()
    elif region == "Павлодарская область":
        show_pavlodar_dashboard()
    elif region == "Жамбылская область":
        show_zhambul_dashboard()
        
    else:
        st.info("Раздел находится в разработке или данные загружаются.")
        
    
        
  
with tabs[9]:
    st.header("🌐 Международное сотрудничество")
    
    # CSS: Немного уменьшим min-height и padding, так как карточки в одну строку будут уже
    st.markdown("""
        <style>
        [data-testid="column"] {
            border: 1px solid #e6e9ef;
            border-radius: 10px;
            padding: 10px !important;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
            transition: transform 0.2s ease;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 180px; 
        }
        
        [data-testid="column"]:hover {
            transform: translateY(-3px);
            border-color: #1f4e78;
        }
        </style>
    """, unsafe_allow_html=True)

    # Цитата (без изменений)
    st.markdown("""
        <div style="border-left: 5px solid #1f4e78; padding-left: 20px; margin-bottom: 30px; background-color: #f8f9fa; padding: 15px;">
            <p style="color: #1f4e78; font-style: italic; font-weight: 400; line-height: 1.4; margin: 0; font-size: 1.1rem;">
                «Международное сотрудничество является фундаментом нашей деятельности, объединяя глобальный опыт и передовые технологии для обеспечения климатической и водной безопасности региона».
            </p>
        </div>
    """, unsafe_allow_html=True)

    partners = [
        {"name": "ВМО", "image": "wmo_logo.png"},
        {"name": "МСГ-СНГ", "image": "cis_logo.png"},
        {"name": "КАСПКОМ", "image": "caspcom_logo.png"},
        {"name": "ПРООН", "image": "undp_logo.png"},
        {"name": "Всемирный банк", "image": "worldbank_logo.png"},
        {"name": "EUMETSAT", "image": "eumetsat_logo.png"}
    ]

    # Создаем ровно столько колонок, сколько партнеров в списке
    cols = st.columns(len(partners))

    for j, partner in enumerate(partners):
        with cols[j]:
            # Название организации
            st.markdown(f'<div style="text-align: center; font-weight: bold; color: #1f4e78; font-size: 0.8rem; margin-bottom: 8px; height: 30px; display: flex; align-items: center; justify-content: center;">{partner["name"]}</div>', unsafe_allow_html=True)
            
            # Логотип
            try:
                # В одну строку лучше использовать use_container_width=True, 
                # чтобы они автоматически подстраивались под узкие колонки
                st.image(partner["image"], use_container_width=True)
            except:
                st.caption(f"Ошибка {partner['name']}")
                
# Добавляем разделитель или небольшой отступ
    st.write("---")
    
    # Заголовок для блока достижений
    st.markdown("<h4 style='text-align: center; color: #1f4e78; margin-bottom: 25px;'>Ключевые показатели за 2024-2025 гг.</h4>", unsafe_allow_html=True)

    # Создаем 3 колонки для метрик
    m_col1, m_col2, m_col3 = st.columns(3)

    with m_col1:
        st.markdown("""
            <div style="text-align: center; background-color: #f0f4f8; padding: 20px; border-radius: 10px;">
                <h2 style="color: #1f4e78; margin: 0;">5</h2>
                <p style="color: #555; font-weight: bold; margin: 0;">Международных меморандумов</p>
                <p style="color: #888; font-size: 0.8rem; margin: 0;">заключено в 2025 году</p>
            </div>
        """, unsafe_allow_html=True)

    with m_col2:
        st.markdown("""
            <div style="text-align: center; background-color: #f0f4f8; padding: 20px; border-radius: 10px;">
                <h2 style="color: #1f4e78; margin: 0;">>50</h2>
                <p style="color: #555; font-weight: bold; margin: 0;">Специалистов обучено</p>
                <p style="color: #888; font-size: 0.8rem; margin: 0;">онлайн и офлайн форматах</p>
            </div>
        """, unsafe_allow_html=True)

    with m_col3:
        st.markdown("""
            <div style="text-align: center; background-color: #f0f4f8; padding: 20px; border-radius: 10px;">
                <h2 style="color: #1f4e78; margin: 0;">25+</h2>
                <p style="color: #555; font-weight: bold; margin: 0;">Встреч с партнерами</p>
                <p style="color: #888; font-size: 0.8rem; margin: 0;">для обмена опытом и данными</p>
            </div>
        """, unsafe_allow_html=True)
        
        
    st.write("---")
    
    st.subheader("📍 Ключевые направления работы с ВМО")

    # Создаем первый ряд колонок
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        with st.expander("📊 Региональный центр по паводкам (CARFFGS)", expanded=True):
            st.markdown("""
            **Выполнение функций Регионального центра по быстроразвивающимся паводкам в странах ЦА.**
            * Обеспечение оперативного мониторинга и прогнозирования паводковых явлений.
            * Координация усилий стран Центральноазиатского региона.
            """)

    with row1_col2:
        with st.expander("💧 Гидрологический мониторинг (HydroSoS)", expanded=True):
            st.markdown("""
            **Реализация инициативы HydroSoS:**
            * Мониторинг и прогнозирование состояния водных ресурсов.
            * Оценка водных ресурсов по речному стоку для обеспечения устойчивого водопользования.
            """)

    # Создаем второй ряд колонок
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        with st.expander("📡 Интегрированная система ВМО (WIGOS)", expanded=True):
            st.markdown("""
            **Совместный Региональный Центр WIGOS (Суб-регионы VI и II):**
            * Пилотный проект: Казахстан, Россия и Беларусь (по ротации).
            * Повышение качества наблюдений и обмена данными.
            """)

    with row2_col2:
        with st.expander("📢 Глобальная инициатива (EW4All)", expanded=True):
            st.info("""
            **Ключевая роль НГМС РК:**
            * **Председатель Целевой группы** для Региона II (Азия).
            * Региональный участник в Восточной Европе и ЦА.
            """)

    # Стилизация для аккуратного вида
    st.markdown("""
        <style>
        .stExpander {
            border: 1px solid #e6e9ef !important;
            border-radius: 8px !important;
            margin-bottom: 10px !important;
            height: 100%; /* Чтобы блоки в одном ряду были одинаковой высоты */
        }
        </style>
    """, unsafe_allow_html=True)
    
    
    
    st.write("---")
    st.subheader("📋 Детализация ключевых проектов по организациям")

    # Используем колонки для компактного размещения карточек организаций
    org_col1, org_col2 = st.columns(2)

    with org_col1:
        with st.expander("🏛️ ЮНЕСКО", expanded=False):
            st.markdown("""
            * **Проект по криосфере:** Активное участие в исследованиях ледников и снежного покрова.
            * **Проект OUTLAST:** Разработка многосекторальной глобальной системы прогнозирования опасности засухи.
            """)
        
        with st.expander("🌿 GIZ (Германия)", expanded=False):
            st.markdown("""
            * **Зеленая Центральная Азия:** Управление водными ресурсами с учетом климатических изменений.
            * **German Water Partnership:** Технологическое сотрудничество в водном секторе.
            """)

    with org_col2:
        with st.expander("🌍 Адаптационный Фонд", expanded=False):
            st.markdown("""
            * **Региональное управление засухами:** Интегрированные программы для стран Центральной Азии.
            * **Межрегиональное взаимодействие:** Управление засухами для стран Южного Кавказа, Казахстана и Молдовы.
            """)
        
        with st.expander("🤝 Двустороннее сотрудничество (2024-2027)", expanded=False):
            st.info("""
            Реализация **Производственных Программ** по обмену данными, опытом и методологиями с:
            * 🇷🇺 Россия | 🇧🇾 Беларусь
            * 🇺🇿 Узбекистан | 🇹🇯 Таджикистан
            * 🇦🇿 Азербайджан
            """)

# Специальный блок: Казгидромет как площадка (Светлый вариант без синего фона)
    st.write("")
    st.markdown("""
        <div style="border: 2px solid #1f4e78; padding: 25px; border-radius: 12px; background-color: #fcfdfe;">
            <h4 style="margin-top: 0; color: #1f4e78; border-bottom: 1px solid #e6e9ef; padding-bottom: 10px;">
                🚀 Казгидромет — международная образовательная платформа
            </h4>
            <p style="color: #333; margin-top: 15px;">В отчетном периоде на базе РГП «Казгидромет» проведены ключевые международные мероприятия:</p>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 10px;">
                    <span style="color: #1f4e78;">📍</span> <b>Семинар ВМО:</b> Управление климатическими данными 
                    <br><small style="color: #666; padding-left: 25px;">(Эксперты из 8 стран: Турция, Германия, Франция, Канада, Бразилия, Австралия, Индонезия)</small>
                </li>
                <li style="margin-bottom: 10px;">
                    <span style="color: #1f4e78;">📍</span> <b>Семинар GIZ:</b> Внедрение гидрологической модели SWIM для трансграничных бассейнов ЦА
                </li>
                <li style="margin-bottom: 10px;">
                    <span style="color: #1f4e78;">📍</span> <b>Технологический воркшоп:</b> Практическое применение приложения Snowmapper
                </li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    
    st.write("---")   

    # Основной баннер нового статуса
    st.info("""
    ### 🏆 Субрегиональный Центр ИГСНВ (WIGOS) RAVI / RAII
    **Статус:** С 1 января 2026 года Казахстан официально стал субрегиональным центром в рамках пилотного проекта Всемирной метеорологической организации (ВМО).
    """)

    # Разделение на Задачи и Страны-участницы
    col_tasks, col_regions = st.columns([1.5, 1])

    with col_tasks:
        st.subheader("🎯 Основные задачи РЦИ")
        
        tasks = [
            ("🗂️ Централизация данных", "Обеспечение доступа к гидрометеорологическим и экологическим данным стран Центральной Азии."),
            ("📈 Аналитика и прогнозы", "Формирование отчетов для региональных и международных организаций."),
            ("💧 Совместный мониторинг", "Поддержка проектов по контролю водных ресурсов и атмосферы."),
            ("🧠 Обмен технологиями", "Трансфер знаний и современных технологий между странами региона.")
        ]
        
        for title, desc in tasks:
            with st.expander(title, expanded=True):
                st.write(desc)

    with col_regions:
        st.subheader("🌍 Значение для региона")
        st.write("Центр координирует взаимодействие и обмен данными между следующими странами:")
        
        # Список стран с флагами для визуальной привлекательности
        countries = [
            "🇦🇲 Армения", "🇧🇾 Беларусь", "🇰🇿 Казахстан", 
            "🇷🇺 РФ", "🇰🇬 Кыргызстан", "🇹🇲 Туркменистан", 
            "🇹🇯 Таджикистан", "🇺🇿 Узбекистан"
        ]
        
        # Вывод стран списком в стилизованном контейнере
        st.markdown(
            f"""
            <div style="background-color: rgba(31, 78, 121, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #1f4e79;">
                {'<br>'.join([f'<b style="color: #5B9BD5;">•</b> {c}' for c in countries])}
            </div>
            """, 
            unsafe_allow_html=True
        )

