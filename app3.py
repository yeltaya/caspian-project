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


# --- 4. СОЗДАНИЕ ВКЛАДОК ---
tabs = st.tabs([
    "📊 Мониторинг", 
    "🌤️ Прогноз погоды", 
    "🌾 Агрометео", 
    "💧 Гидропрогнозы", 
    "🌊 Водные ресурсы", 
    "🌊 Каспийское море", 
    "🇰🇿 Климат", 
    "🏭 Экология",
    "🌐 Сотрудничество"    
])

#МОНИТОРИНГ
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
                Опираясь на вековой опыт и данные государственной наблюдательной сети, мы создаем качественные аналитические продукты для стратегических отраслей экономики</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 4. МЕТРИКИ МАСШТАБА
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("История и опыт", "100+ лет наблюдений", "мониторинг 24/7")
    m2.metric("География", "17 филиалов", "весь Казахстан")
    m3.metric("Команда", "3160", "сотрудников в штате")
    m4.metric("Мировой стандарт", "ВМО (WMO)", "с 1993 года")

    st.markdown("<br>", unsafe_allow_html=True)

# 5. КАРТОЧКИ НАПРАВЛЕНИЙ
    col1, col2, col3, col4 = st.columns(4)
    
    sections = [
        {"title": "🌡️ Метеорология", "total": "351 Станция", "items": ["225 Традиционных", "126 Автоматических", "9 Аэрологических", "5 ДМРЛ"]},
        {"title": "💧 Гидрология", "total": "442 Поста", "items": ["394 Речных поста", "38 Озерных", "10 Морских станций"]},
        {"title": "🌾 Агрометеорология", "total": "226 Пунктов", "items": ["129 На станциях", "97 Постов:", "50 Автоматических", "47 Традиционных (ручных)"]},
        {"title": "🌱 Экология", "total": "175 Постов", "items": ["131 Автоматических", "44 Ручных", "15 Передвижных лабораторий"]}
    ]

    cols = [col1, col2, col3, col4]
    for i, sec in enumerate(sections):
        with cols[i]:
            # Разделяем общее количество для увеличения шрифта
            total_parts = sec['total'].split()
            v_total = total_parts[0]
            l_total = " ".join(total_parts[1:])
            
            # Собираем список подпунктов
            items_html = "".join([
                f'<li style="margin-bottom:5px;list-style:none;">'
                f'<span style="font-weight:700;color:#004A99;">{it.split()[0]}</span> '
                f'{" ".join(it.split()[1:])}</li>' 
                for it in sec["items"]
            ])

            # Возвращаем белый стиль карточки (monitor-card)
            card_content = (
                f'<div class="monitor-card" style="background: white; border: 1px solid #eee; padding: 15px; border-radius: 8px;">'
                f'<div class="card-header-text" style="font-weight:bold; margin-bottom:10px;">{sec["title"]}</div>'
                f'<div style="margin-bottom:15px;">'
                f'<span style="font-size:32px; font-weight:800; color:#004A99; line-height:1;">{v_total}</span> '
                f'<span style="font-size:16px; font-weight:600; color:#455a64;">{l_total}</span>'
                f'</div>'
                f'<ul style="padding-left:0; margin:0; font-size:0.95em;">{items_html}</ul>'
                f'</div>'
            )
            
            st.markdown(card_content, unsafe_allow_html=True)

    # Линия-разделитель после блока карточек
    st.divider()
     

# 7. МЕТЕОРОЛОГИЧЕСКИЙ МОНИТОРИНГ
    st.markdown("""
            <div style="text-align:center; margin: 40px 0 20px 0;">
                <h2 style="color: #004A99; font-family: 'Exo 2', sans-serif; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; font-size: 2.2em;">
                    Метеорологический мониторинг
                </h2>
                <p style="color: #546e7a; font-size: 1.1em; font-weight: 500;">Единая национальная сеть комплексного мониторинга приземных и высоких слоев атмосферы, интегрированная в глобальную систему обмена данными ВМО</p>
            </div>
        """, unsafe_allow_html=True)
        

    # 7.1 HIGHLIGHTS (Ключевые показатели метеосети)
    st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; margin-bottom: 30px;">
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #003366; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 0.8em;">🏢</span>
                        <div>
                            <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">351</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">Метеостанций в сети</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #004A99; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">📲</span>
                        <div>
                            <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">100%</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">автоматизированная передача данных</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #0288d1; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">⏱️</span>
                        <div>
                            <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">3 часа</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">Срок наблюдений</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #03a9f4; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">🌐</span>
                        <div>
                            <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">WMO</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">Глобальный обмен</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #26c6da; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">🏛️</span>
                        <div>
                            <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">19</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">Вековых станций</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 180px; background: #ffffff; border-left: 5px solid #4fc3f7; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">📧</span>
                        <div>
                            <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">658 800</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">Телеграмм/год (МС)</div>
                        </div>
                    </div>
                </div>
                <div style="flex: 1; min-width: 180px; background: #ffffff; border-left: 5px solid #81d4fa; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.8em;">📡</span>
                        <div>
                            <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">1 106 784</div>
                            <div style="font-size: 0.7em; color: #546e7a; text-transform: uppercase; font-weight: 700; letter-spacing: 1.0px;">Телеграмм/год (АМС)</div>
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
            "Высотное зондирование атмосферы на 9 станциях РК.", 
            [
                "<b>Вертикаль:</b> мониторинг состояния до 30 км и выше.", 
                "<b>Зонды:</b> выпуск радиозондов 2 раза в сутки.", 
                "<b>Модели:</b> данные для циклонов и антициклонов.",
                "<b>Безопасность:</b> прогноз опасных и стихийных явлений погоды."
            ], 
            "Аэрология"
        )

        # 3. ДМРЛ (Доплеровские метеорологические радиолокаторы)
    draw_block(
            met_col3, 
            "icon_btn_3", 
            "📡 ДМРЛ", 
            "🖼️", 
            """Дистанционное сканирование атмосферы в радиусе до 250 км. 
            
            Совместная сеть с <b>РГП «Казаэронавигация»</b> состоит из <b>19 ДМРЛ</b> 
            (5 — Казгидромет, 14 — Казаэронавигация).""", 
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
            "📖 Государственный климатический кадастр", 
            "📁", 
            "Официальный систематизированный свод многолетних данных о климате территории, сформированный по результатам регулярных наблюдений метеорологических станций.", 
            [
                "<b>Периоды:</b> средние значения за сутки, месяц, сезон, год, многолетний период.", 
                "<b>Экстремумы:</b> крайние показатели температуры, осадков, ветра и др.", 
                "<b>Явления:</b> сведения о сроках наступления климатических явлений (морозы, заморозки, устойчивый снежный покров, переход температуры через определённые пороги) и их продолжительности.",
                "<b>Фонд:</b> хранение вековых рядов наблюдений."
            ], 
            "Кадастр"
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

# --- 2. СЛОВАРЬ КАЗГИДРОМЕТ (ОПТИМИЗИРОВАННЫЙ) ---
    kaz_stats = {
        # г. Алматы (Отдельно согласно списку: 19 МС / 16 АМС)
        "almaty": {"ru": "г. Алматы", "ms": 19, "ams": 16, "t_min": -38, "t_max": 43, "wind": 3.45, "press": 1012},
        "г. алматы": {"ru": "г. Алматы", "ms": 19, "ams": 16, "t_min": -38, "t_max": 43, "wind": 3.45, "press": 1012},
        "алматы": {"ru": "г. Алматы", "ms": 19, "ams": 16, "t_min": -38, "t_max": 43, "wind": 3.45, "press": 1012},

        # Жетісу / Жетысу (Отдельно: 12 МС / 7 АМС)
        "zhetisu": {"ru": "Область Жетісу", "ms": 12, "ams": 7, "t_min": -44, "t_max": 44, "wind": 3.70, "press": 1012},
        "жетісу": {"ru": "Область Жетісу", "ms": 12, "ams": 7, "t_min": -44, "t_max": 44, "wind": 3.70, "press": 1012},
        "область жетісу": {"ru": "Область Жетісу", "ms": 12, "ams": 7, "t_min": -44, "t_max": 44, "wind": 3.70, "press": 1012},
        "жетысуская область": {"ru": "Область Жетісу", "ms": 12, "ams": 7, "t_min": -44, "t_max": 44, "wind": 3.70, "press": 1012},

        # Алматинская область (Отдельно: 12 МС / 7 АМС)
        "almaty oblast": {"ru": "Алматинская область", "ms": 12, "ams": 7, "t_min": -44, "t_max": 44, "wind": 3.70, "press": 1012},
        "алматинская область": {"ru": "Алматинская область", "ms": 12, "ams": 7, "t_min": -44, "t_max": 44, "wind": 3.70, "press": 1012},

        # Карагандинская и Улытау (Объединены: 23 МС / 10 АМС)
        "karaganda": {"ru": "Карагандинская и Улытау", "ms": 23, "ams": 10, "t_min": -50, "t_max": 45, "wind": 3.40, "press": 1019},
        "карагандинская область": {"ru": "Карагандинская и Улытау", "ms": 23, "ams": 10, "t_min": -50, "t_max": 45, "wind": 3.40, "press": 1019},
        "ulytau": {"ru": "Карагандинская и Улытау", "ms": 23, "ams": 10, "t_min": -50, "t_max": 45, "wind": 3.40, "press": 1019},
        "улытауская область": {"ru": "Карагандинская и Улытау", "ms": 23, "ams": 10, "t_min": -50, "t_max": 45, "wind": 3.40, "press": 1019},

        # ВКО и Абай (Объединены: 30 МС / 14 АМС)
        "east kazakhstan": {"ru": "ВКО и Абай", "ms": 30, "ams": 14, "t_min": -50, "t_max": 45, "wind": 3.45, "press": 1050},
        "vostochno-kazakhstanskaya": {"ru": "ВКО и Абай", "ms": 30, "ams": 14, "t_min": -50, "t_max": 45, "wind": 3.45, "press": 1050},
        "восточно-казахстанская область": {"ru": "ВКО и Абай", "ms": 30, "ams": 14, "t_min": -50, "t_max": 45, "wind": 3.45, "press": 1050},
        "abay": {"ru": "ВКО и Абай", "ms": 30, "ams": 14, "t_min": -50, "t_max": 45, "wind": 3.45, "press": 1050},
        "область абай": {"ru": "ВКО и Абай", "ms": 30, "ams": 14, "t_min": -50, "t_max": 45, "wind": 3.45, "press": 1050},

        # Туркестанская область и Шымкент (14 МС / 6 АМС)
        "turkistan": {"ru": "Туркестанская область", "ms": 14, "ams": 6, "t_min": -43, "t_max": 51, "wind": 3.52, "press": 1047},
        "туркестанская область": {"ru": "Туркестанская область", "ms": 14, "ams": 6, "t_min": -43, "t_max": 51, "wind": 3.52, "press": 1047},
        "shymkent": {"ru": "г. Шымкент", "ms": 8, "ams": 4, "t_min": -43, "t_max": 51, "wind": 3.52, "press": 1047},
        "шымкент": {"ru": "г. Шымкент", "ms": 8, "ams": 4, "t_min": -43, "t_max": 51, "wind": 3.52, "press": 1047},

        # Акмолинская область и Астана
        "akmola": {"ru": "Акмолинская область", "ms": 15, "ams": 15, "t_min": -52, "t_max": 42, "wind": 3.48, "press": 1038},
        "акмолинская область": {"ru": "Акмолинская область", "ms": 15, "ams": 15, "t_min": -52, "t_max": 42, "wind": 3.48, "press": 1038},
        "astana": {"ru": "г. Астана", "ms": 5, "ams": 5, "t_min": -52, "t_max": 42, "wind": 3.48, "press": 1038},
        "астана": {"ru": "г. Астана", "ms": 5, "ams": 5, "t_min": -52, "t_max": 42, "wind": 3.48, "press": 1038},

        # Остальные регионы
        "aktobe": {"ru": "Актюбинская область", "ms": 17, "ams": 9, "t_min": -47, "t_max": 47, "wind": 3.48, "press": 1048},
        "актюбинская область": {"ru": "Актюбинская область", "ms": 17, "ams": 9, "t_min": -47, "t_max": 47, "wind": 3.48, "press": 1048},

        "atyrau": {"ru": "Атырауская область", "ms": 9, "ams": 2, "t_min": -42, "t_max": 46, "wind": 3.34, "press": 1058},
        "атырауская область": {"ru": "Атырауская область", "ms": 9, "ams": 2, "t_min": -42, "t_max": 46, "wind": 3.34, "press": 1058},

        "zhambyl": {"ru": "Жамбылская область", "ms": 13, "ams": 8, "t_min": -50, "t_max": 48, "wind": 3.49, "press": 1022},
        "жамбылская область": {"ru": "Жамбылская область", "ms": 13, "ams": 8, "t_min": -50, "t_max": 48, "wind": 3.49, "press": 1022},

        "west kazakhstan": {"ru": "Западно-Казахстанская область", "ms": 13, "ams": 5, "t_min": -44, "t_max": 45, "wind": 3.34, "press": 1058},
        "западно-казахстанская область": {"ru": "Западно-Казахстанская область", "ms": 13, "ams": 5, "t_min": -44, "t_max": 45, "wind": 3.34, "press": 1058},

        "kostanay": {"ru": "Костанайская область", "ms": 18, "ams": 2, "t_min": -47, "t_max": 45, "wind": 3.40, "press": 1052},
        "костанайская область": {"ru": "Костанайская область", "ms": 18, "ams": 2, "t_min": -47, "t_max": 45, "wind": 3.40, "press": 1052},

        "kyzylorda": {"ru": "Кызылординская область", "ms": 9, "ams": 6, "t_min": -40, "t_max": 48, "wind": 3.62, "press": 1047},
        "кызылординская область": {"ru": "Кызылординская область", "ms": 9, "ams": 6, "t_min": -40, "t_max": 48, "wind": 3.62, "press": 1047},

        "mangystau": {"ru": "Мангистауская область", "ms": 7, "ams": 10, "t_min": -38, "t_max": 47, "wind": 3.45, "press": 1053},
        "мангистауская область": {"ru": "Мангистауская область", "ms": 7, "ams": 10, "t_min": -38, "t_max": 47, "wind": 3.45, "press": 1053},

        "pavlodar": {"ru": "Павлодарская область", "ms": 15, "ams": 4, "t_min": -49, "t_max": 42, "wind": 3.50, "press": 1056},
        "павлодарская область": {"ru": "Павлодарская область", "ms": 15, "ams": 4, "t_min": -49, "t_max": 42, "wind": 3.50, "press": 1056},

        "north kazakhstan": {"ru": "Северо-Казахстанская область", "ms": 11, "ams": 5, "t_min": -48, "t_max": 41, "wind": 3.40, "press": 1055},
        "северо-казахстанская область": {"ru": "Северо-Казахстанская область", "ms": 11, "ams": 5, "t_min": -48, "t_max": 41, "wind": 3.40, "press": 1055},
    }
    
    
    
    @st.cache_data
    def load_data(path):
        if not os.path.exists(path): 
            return None
        gdf = gpd.read_file(path)
        
        # Убираем общий контур страны, если он мешает
        if 'ADMO_EN' in gdf.columns: 
            gdf = gdf[gdf['ADMO_EN'] != 'KAZ']
        
        # Определяем колонку с ID (обычно ADM1_EN)
        name_col = 'ADM1_EN' if 'ADM1_EN' in gdf.columns else gdf.select_dtypes(include=['object']).columns[0]
        
        def get_ru_name(val):
            # Чистим входящее имя: в нижний регистр и убираем лишние пробелы
            clean_key = str(val).strip().lower()
            # Пытаемся найти в словаре kaz_stats
            found = kaz_stats.get(clean_key)
            if not found:
                # Если точного совпадения нет, ищем частичное (например, 'aktobe' в 'aktobe region')
                found = next((v for k, v in kaz_stats.items() if k in clean_key or clean_key in k), None)
            
            # Возвращаем русское имя или само значение с заглавной буквы, если не нашли
            return found['ru'] if found else str(val).title()

        # Создаем колонку с гарантированно русским названием для тултипов и заголовков
        gdf['RUS_NAME'] = gdf[name_col].apply(get_ru_name)
        
        return gdf.to_crs(epsg=4326), name_col
        
        

    result = load_data(SHP_PATH)

    if result:
        gdf, name_col = result
        
        # ТРЕХБЛОЧНЫЙ ЛЕЙАУТ
        col_left, col_mid, col_right = st.columns([1.1, 1.3, 0.7], gap="medium")

        # --- ЛЕВАЯ КОЛОНКА ---
# --- ЛЕВАЯ КОЛОНКА ---
        with col_left:
            st.subheader("🇰🇿 Казахстан")
            m_full = folium.Map(location=[48.0, 67.0], zoom_start=4, tiles="cartodbpositron")
            folium.GeoJson(
                gdf,
                style_function=lambda x: {
                    'fillColor': '#e3f2fd', 'color': '#004A99', 'weight': 1, 'fillOpacity': 0.5
                },
                # ЗДЕСЬ: теперь при наведении будет русский язык
                tooltip=folium.GeoJsonTooltip(fields=['RUS_NAME'], aliases=['Область:']) 
            ).add_to(m_full)
            # ... далее ваш код st_folium ...
            
            
            # Важно: фиксированная высота для соответствия CSS
            out_full = st_folium(m_full, use_container_width=True, height=500, key="map_kaz_main")
            
            if out_full and out_full.get("last_active_drawing"):
                new_id = out_full["last_active_drawing"]["properties"].get(name_col)
                if st.session_state.selected_region_id != new_id:
                    st.session_state.selected_region_id = new_id
                    st.rerun()


        import pandas as pd
        import os
        import streamlit as st
        import folium
        from streamlit_folium import st_folium
        # ОПРЕДЕЛЯЕМ БАЗОВЫЙ ПУТЬ (Добавьте это обязательно!)
        base_path = os.path.dirname(os.path.abspath(__file__))

        # --- ПУТЬ К ФАЙЛУ ---
        XLSX_PATH = os.path.join(base_path, "MS tizimi.xlsx")

        @st.cache_data
        def load_stations_from_excel(path):
            if not os.path.exists(path):
                return None
            # Читаем Excel, пропуская первую пустую строку заголовка
            df = pd.read_excel(path, skiprows=1)
            
            # Очищаем названия столбцов от лишних пробелов
            df.columns = [str(c).strip() for c in df.columns]
            
            # Заполняем объединенные ячейки в колонке ФИЛИАЛ
            if 'ФИЛИАЛ' in df.columns:
                df['ФИЛИАЛ'] = df['ФИЛИАЛ'].ffill()
                
            return df

        df_stations = load_stations_from_excel(XLSX_PATH)

                # --- СРЕДНЯЯ КОЛОНКА ---
        with col_mid:
            selected_id = st.session_state.selected_region_id
            if selected_id:
                target_data = gdf[gdf[name_col] == selected_id]
                
                if not target_data.empty:
                    target_row = target_data.iloc[0]
                    st.subheader(f"📍 {target_row['RUS_NAME'].upper()}")
                    
                    center = target_row.geometry.centroid
                    m_reg = folium.Map(location=[center.y, center.x], zoom_start=6, tiles="cartodbpositron")
                    
                    folium.GeoJson(
                        target_row.geometry,
                        style_function=lambda x: {'fillColor': '#004A99', 'color': '#004A99', 'weight': 2, 'fillOpacity': 0.05}
                    ).add_to(m_reg)

                    if df_stations is not None:
                        # Получаем чистое название из карты
                        region_name = target_row['RUS_NAME'].lower().strip()
                        
                        # --- УЛУЧШЕННЫЙ МАППИНГ ДЛЯ ПОИСКА В EXCEL ---
                        # Этот словарь связывает имя из Shapefile с тем, как оно написано в колонке ФИЛИАЛ в Excel
                        manual_map = {
                            "алматинская": "г.Алматы",
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
                            "карагандин": "Караганд"
                        }
                        
                        # Ищем подходящий поисковый запрос
                        search_term = None
                        for key, val in manual_map.items():
                            if key in region_name:
                                search_term = val
                                break
                        
                        # Если в словаре нет (например, Павлодар, Актобе), берем корень слова
                        if not search_term:
                            search_term = region_name.split()[0][:5].capitalize() # Берем первые 5 букв

                        # Фильтрация станций
                        region_stations = df_stations[df_stations['ФИЛИАЛ'].str.contains(search_term, case=False, na=False)]
                        
                        # Если совсем ничего не нашли, попробуем очень широкий поиск по 3 буквам
                        if region_stations.empty:
                             region_stations = df_stations[df_stations['ФИЛИАЛ'].str.contains(search_term[:3], case=False, na=False)]

                        for _, row in region_stations.iterrows():
                            try:
                                # Динамический поиск колонок координат (на случай пробелов в Excel)
                                col_lat = [c for c in df_stations.columns if 'с.ш' in c.lower()][0]
                                col_lon = [c for c in df_stations.columns if 'в.д' in c.lower()][0]
                                
                                lat, lon = float(row[col_lat]), float(row[col_lon])
                                
                                if pd.notna(lat) and pd.notna(lon):
                                    st_type = str(row['Вид']).strip().upper()
                                    dot_color = "green" if "АМС" in st_type else "blue"
                                    
                                    folium.CircleMarker(
                                        location=[lat, lon],
                                        radius=6,
                                        color=dot_color,
                                        fill=True,
                                        fill_color=dot_color,
                                        fill_opacity=0.8,
                                        popup=f"<b>{row['Станция']}</b><br>Тип: {st_type}<br>Филиал: {row['ФИЛИАЛ']}",
                                        tooltip=f"{row['Станция']} ({st_type})"
                                    ).add_to(m_reg)
                            except:
                                continue
                    
                    st_folium(m_reg, use_container_width=True, height=500, key=f"map_reg_{selected_id}")
                    

# --- ПРАВАЯ КОЛОНКА ---
        with col_right:
            st.subheader("ℹ️ Государственная сеть")
            
            if selected_id:
                # --- БЛОК ВЫБРАННОГО РЕГИОНА ---
                search_name = str(selected_id).strip().lower()
                found_data = kaz_stats.get(search_name)
                if not found_data:
                    found_data = next((val for key, val in kaz_stats.items() if key in search_name or search_name in key), None)
                
                if found_data:
                    st.markdown(f"""
                        <div style="background:#004A99; color:white; padding:20px; border-radius:15px; margin-bottom:15px; text-align:center">
                            <span style="font-size:1.1em; font-weight:bold">Региональная сеть:</span><br>
                            <span style="font-size:1.8em">🏢 {found_data['ms']} | 📡 {found_data['ams']}</span>
                            <div style="font-size:0.8em; opacity:0.8; margin-top:5px;">Метеостанции и АМС</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    m1, m2 = st.columns(2)
                    with m1:
                        st.metric("❄️ Т.Мин", f"{found_data['t_min']}°")
                        st.metric("💨 Ветер", f"{found_data['wind']} м/с")
                    with m2:
                        st.metric("🔥 Т.Макс", f"{found_data['t_max']}°")
                        st.metric("🌡️ Давл.", f"{found_data['press']}")
                else:
                    st.warning(f"Данные для '{selected_id}' не найдены.")
            
            else:
                # --- ОБЩАЯ СТАТИСТИКА (ПО УМОЛЧАНИЮ) ---
                st.markdown(f"""
                    <div style="background:#f0f2f6; padding:20px; border-radius:15px; border: 1px dashed #004A99;">
                        <h4 style="margin:0; color:#004A99;">Общая сеть РК</h4>
                        <p style="font-size:1.1em; margin:15px 0; line-height:1.5;">
                            <b>351</b> метеорологических станций, из них:<br>
                            • <b>225</b> традиционных<br>
                            • <b>126</b> автоматических
                        </p>
                        <p style="font-size:0.85em; color:#546e7a; font-style:italic; border-top: 1px solid #ccc; padding-top:10px; margin-top:10px;">
                            Нажмите на любую область на карте для детализации по региону
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            # --- ЛЕГЕНДА (ОТОБРАЖАЕТСЯ ВСЕГДА ВНИЗУ КОЛОНКИ) ---
            st.markdown("""
                <div style="margin-top: 25px; padding: 10px; border-radius: 10px; background: white; border: 1px solid #e6e9ef;">
                    <div style="font-size: 0.85em; font-weight: bold; color: #546e7a; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">
                        Условные обозначения:
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                        <div style="width: 12px; height: 12px; background-color: blue; border-radius: 50%; margin-right: 10px;"></div>
                        <span style="font-size: 0.9em; color: #1a1c1f;">Традиционные станции (МС)</span>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 12px; height: 12px; background-color: green; border-radius: 50%; margin-right: 10px;"></div>
                        <span style="font-size: 0.9em; color: #1a1c1f;">Автоматические станции (АМС)</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
          

        # --- 1. ПОДГОТОВКА ДАННЫХ ---
    data_storm = {
            "Филиал": [
                "Акмола", "Актобе", "Жетысу", "г.Алматы", "Атырау", "ВКО", 
                "Жамбыл", "ЗКО", "Караганды", "Костанай", "Кызылорда", 
                "Мангистау", "Павлодар", "СКО", "Туркестан"
            ],
            "2020": [1385, 1043, 741, 932, 456, 1367, 635, 567, 1191, 952, 380, 220, 444, 650, 746],
            "2021": [1209, 998, 922, 1336, 693, 1644, 735, 776, 1185, 693, 499, 258, 348, 669, 778],
            "2022": [1228, 955, 765, 1659, 699, 1842, 755, 885, 1162, 836, 496, 229, 692, 663, 1078],
            "2023": [1518, 1055, 827, 1725, 749, 1962, 788, 813, 1391, 997, 436, 349, 684, 1007, 730],
            "2024": [2004, 1188, 734, 1579, 604, 2180, 817, 957, 1396, 1153, 457, 259, 908, 1142, 839],
            "2025": [1670, 1192, 725, 1414, 604, 2644, 652, 1162, 1262, 965, 620, 237, 897, 1188, 589]
        }

    df_storm = pd.DataFrame(data_storm)
    years = ["2020", "2021", "2022", "2023", "2024", "2025"]
    total_values = [11709, 12743, 13944, 15031, 16217, 15821]
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    # --- 2. ИНТЕРФЕЙС ---
    st.subheader("🌩️ Мониторинг штормовой активности (2020-2025 гг.)")

    # --- ДОБАВЛЕННЫЙ ТЕКСТ С ПОЯСНЕНИЕМ ---
    st.markdown("""
        <div style="background-color: rgba(255, 165, 0, 0.1); padding: 15px; border-left: 5px solid #FFA500; border-radius: 5px; margin-bottom: 20px;">
            <span style="color: #FFA500; font-weight: bold;">Штормовая активность</span> — это интенсивность возникновения опасных метеорологических явлений, требующих оперативного оповещения. 
            Статистика включает в себя выпуск штормовых телеграмм по двум категориям:
            <ul style="margin-top: 10px; font-size: 0.9em;">
                <li><b>ОЯ (Опасные явления)</b> — метеорологические явления, которые по своей интенсивности или времени возникновения могут нанести значительный ущерб экономике и населению.</li>
                <li><b>СГЯ (Стихийные гидрометеорологические явления)</b> — экстремально интенсивные явления (ураганный ветер, сильные ливни, аномальная жара/мороз), представляющие непосредственную угрозу жизни людей.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)


        # Верхние метрики
    m1, m2, m3 = st.columns(3)
    with m1:
            st.metric("Пик активности", "2024 г.", "16 217 телеграмм")
    with m2:
            st.metric("Максимум в 2025", "ВКО", "2 644")
    with m3:
            st.metric("Среднее за год", f"{int(sum(total_values)/len(total_values))}")

        # Разделение на графики
    col_left, col_right = st.columns([1.2, 1])

    import plotly.graph_objects as go

    with col_left:
            st.markdown("**Анализ штормовых оповещений (по годам)**")
            
            fig = go.Figure()

            # 1. Столбцы для объемов (более наглядно для сравнения лет)
            fig.add_trace(go.Bar(
                x=years,
                y=total_values,
                name="Количество",
                marker=dict(
                    color='rgba(52, 152, 219, 0.6)', # Полупрозрачный синий
                    line=dict(color='#3498db', width=1)
                ),
                hovertemplate="Год: %{x}<br>Всего: %{y}<extra></extra>"
            ))

            # 2. Линия тренда поверх столбцов
            fig.add_trace(go.Scatter(
                x=years,
                y=total_values,
                mode='lines+markers',
                name="Динамика",
                line=dict(color='#FFA500', width=3), # Яркий оранжевый для контраста
                marker=dict(size=8, symbol='circle', color='white', line=dict(width=2, color='#FFA500')),
                hoverinfo="skip" # Чтобы не дублировать подсказку
            ))

            # Настройка внешнего вида
            fig.update_layout(
                height=450,
                margin=dict(l=50, r=10, t=50, b=50), # Увеличили отступы (l и b), чтобы крупные цифры не обрезались
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(
                    orientation="h", 
                    yanchor="bottom", 
                    y=1.02, 
                    xanchor="right", 
                    x=1,
                    font=dict(size=14) # Размер текста в легенде
                ),
                font=dict(color="#dee2e6"),
                bargap=0.3,
                yaxis=dict(
                    showgrid=True, 
                    gridcolor='rgba(200,200,200,0.1)',
                    zeroline=False,
                    title=dict(text="Кол-во оповещений", font=dict(size=16)), # Размер заголовка оси Y
                    tickfont=dict(size=16) # РАЗМЕР ШРИФТА ЧИСЕЛ ВДОЛЬ ОСИ Y
                ),
                xaxis=dict(
                    dtick=1, 
                    showgrid=False,
                    tickfont=dict(size=16) # РАЗМЕР ШРИФТА ГОДОВ ВДОЛЬ ОСИ X
                )
            )



            st.plotly_chart(fig, use_container_width=True)
        

    with col_right:
            st.markdown("**Распределение по регионам (Тепловая карта)**")
            # Heatmap для наглядности интенсивности
            fig_heat = px.imshow(
                df_storm.set_index("Филиал")[years],
                labels=dict(x="Год", y="Филиал", color="Кол-во"),
                color_continuous_scale="Blues",
                aspect="auto"
            )
            
            # Исправленный блок для Heatmap
            fig_heat.update_layout(
                height=450, # Немного увеличим высоту для крупных шрифтов
                margin=dict(l=80, r=20, t=50, b=80), # Увеличили отступы, чтобы шрифт 16 не обрезался
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white"),
                
                # Настройка горизонтальной оси (X)
                xaxis=dict(
                    tickfont=dict(size=16),
                    side='bottom' # Гарантирует, что подписи будут снизу
                ),
                
                # Настройка вертикальной оси (Y)
                yaxis=dict(
                    tickfont=dict(size=16),
                    autorange='reversed' # Важно для тепловых карт, чтобы данные шли сверху вниз
                )
            )

            st.plotly_chart(fig_heat, use_container_width=True)


        # --- 4. АВТОМАТИЧЕСКОЕ АНАЛИТИЧЕСКОЕ РЕЗЮМЕ ---
    st.markdown("---")
    st.markdown("### 📋 Аналитическая справка")

        # Расчеты для резюме
        # 1. Находим регион с максимальным ростом (сравнение 2025 к 2020)
    df_storm['Growth'] = df_storm['2025'] - df_storm['2020']
    max_growth_region = df_storm.loc[df_storm['Growth'].idxmax()]

        # 2. Находим регион-лидер по количеству в 2025 году
    leader_2025 = df_storm.loc[df_storm['2025'].idxmax()]

        # 3. Общая тенденция (2025 vs 2024)
    total_2024 = 16217
    total_2025 = 15821
    trend_pct = round(((total_2025 - total_2024) / total_2024) * 100, 1)
    trend_text = "незначительное снижение" if trend_pct < 0 else "рост"

        # Вывод резюме в стильном блоке
    st.write(f"""
        За анализируемый период (2020–2025 гг.) наблюдаются следующие ключевые изменения в штормовой активности:

        * **Лидер по нагрузке:** В 2025 году наибольшее количество штормовых телеграмм было выпущено филиалом **{leader_2025['Филиал']}** ({leader_2025['2025']} ед.).
        * **Самая высокая динамика:** Наиболее резкий рост активности за 5 лет зафиксирован в регионе **{max_growth_region['Филиал']}**. Количество штормовых оповещений здесь увеличилось на **{max_growth_region['Growth']}** единиц по сравнению с 2020 годом.
        * **Общий тренд:** После пиковых значений 2024 года, в 2025 году зафиксировано **{trend_text}** активности на **{abs(trend_pct)}%**. Это может быть связано с изменением климатических циклов или частоты опасных метеорологических явлений в текущем году.
        """)

        # Небольшой дисклеймер или примечание
    st.caption("⚠️ Данные за 2025 год являются актуальными на текущую дату и могут быть уточнены по итогам годового отчета.")

            
    # --- 1. ПОДГОТОВКА ДАННЫХ СГЯ ---
    data_sgy = {
            "Филиал": [
                "Акмола", "Актобе", "Жетысу", "г.Алматы", "Атырау", "ВКО", 
                "Жамбыл", "ЗКО", "Караганды", "Костанай", "Кызылорда", 
                "Мангистау", "Павлодар", "СКО", "Туркестан"
            ],
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

        # --- 2. ВИЗУАЛИЗАЦИЯ ---
    st.markdown("---")
    st.subheader("⚠️ Анализ Стихийных Гидрометеорологических Явлений (СГЯ)")

    col_left, col_right = st.columns([1, 1.2])

    with col_left:
            st.markdown("**Распределение СГЯ по годам**")
            # Используем Waterfall или Bar для демонстрации аномалии 2023 года
            fig_sgy_total = go.Figure(go.Bar(
                x=years_sgy, y=total_sgy,
                marker_color=['#1f4e79', '#1f4e79', '#1f4e79', '#e74c3c', '#1f4e79', '#1f4e79'], # Выделяем 2023 красным
                text=total_sgy, textposition='auto'
            ))
            fig_sgy_total.update_layout(
                height=350, 
                # l=80 и b=80 дадут запас для шрифта 16
                margin=dict(l=80, r=20, t=30, b=80),
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color="white"),
                
                # Горизонтальная ось
                xaxis=dict(
                    tickfont=dict(size=16),
                    title=dict(text="Год", font=dict(size=16)), # Добавил заголовок, если нужен
                    automargin=True,
                    type='category' # Гарантирует, что года/категории встанут ровно
                ),
                
                # Вертикальная ось
                yaxis=dict(
                    tickfont=dict(size=16),
                    title=dict(text="Количество", font=dict(size=16)),
                    automargin=True
                )
            )
            st.plotly_chart(fig_sgy_total, use_container_width=True)


    with col_right:
                st.markdown("**Рейтинг регионов по количеству СГЯ (2020-2025)**")
                
                # 1. Считаем общую сумму за все годы
                df_sgy['Total'] = df_sgy[years_sgy].sum(axis=1)
                
                # 2. Сортируем данные для наглядности (самые активные сверху)
                df_sgy_sorted = df_sgy.sort_values(by='Total', ascending=True)

                # 3. Строим горизонтальный график
                fig_sgy_reg = px.bar(
                    df_sgy_sorted, 
                    x='Total', 
                    y='Филиал',
                    orientation='h',
                    text='Total', # Выводим цифры прямо на столбцах
                    color='Total', # Цвет зависит от значения
                    color_continuous_scale="Blues"
                )

                fig_sgy_reg.update_layout(
                    height=450, # Увеличили высоту, чтобы все названия влезли
                    margin=dict(l=10, r=40, t=20, b=10),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white"),
                    showlegend=False,
                    coloraxis_showscale=False # Убираем цветовую шкалу справа
                )

                # 1. Настройка самих столбцов и цифр НАД ними
                fig_sgy_reg.update_traces(
                    textposition='outside', # Цифры снаружи столбцов
                    # УВЕЛИЧИВАЕМ ШРИФТ ЦИФР НАД СТОЛБЦАМИ
                    textfont=dict(size=16, color="white"), 
                    marker_line_color='rgb(8,48,107)',
                    marker_line_width=1,
                    opacity=0.9
                )

                # 2. Настройка горизонтальной оси (X)
                fig_sgy_reg.update_xaxes(
                    showgrid=True, 
                    gridcolor='rgba(255,255,255,0.1)', 
                    title=dict(text="Всего СГЯ", font=dict(size=18)), # Размер заголовка оси
                    tickfont=dict(size=16) # Размер чисел на оси X
                )

                # 3. Настройка вертикальной оси (Y)
                fig_sgy_reg.update_yaxes(
                    title="",
                    tickfont=dict(size=16) # Размер названий (регионов/категорий) на оси Y
                )

                # 4. Не забываем про отступы в layout, чтобы крупные названия не обрезались
                fig_sgy_reg.update_layout(
                    margin=dict(l=100, r=20, t=40, b=60), # Увеличил отступ слева (l) для названий регионов
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white")
                )

                st.plotly_chart(fig_sgy_reg, use_container_width=True)

                
        # --- 3. АВТОМАТИЧЕСКОЕ РЕЗЮМЕ ПО СГЯ ---
    max_sgy_year = 2023
    max_sgy_val = 509
    top_region_sgy = df_sgy.loc[df_sgy['Total'].idxmax()]

    st.info(f"""
        **Аналитическая заметка по СГЯ:**
        * **Аномальный период:** 2023 год стал экстремальным для Казахстана — зафиксировано **{max_sgy_val}** явлений, что более чем в 2 раза превышает средние показатели.
        * **Зоны риска:** Наибольшее суммарное количество стихийных явлений за 6 лет зафиксировано в филиалах **{top_region_sgy['Филиал']}**.
        * **Текущая ситуация:** В 2025 году наблюдается стабилизация и снижение количества СГЯ ({total_sgy[-1]} ед.).
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
    # --- 1. ЗАГОЛОВОК СЕКЦИИ ---
    st.markdown("""
        <div style="text-align:center; margin: 40px 0 20px 0;">
            <h2 style="color: #004A99; font-family: 'Exo 2', sans-serif; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; font-size: 2.2em;">
                Гидрологический мониторинг
            </h2>
            <p style="color: #546e7a; font-size: 1.1em; font-weight: 500;">Единая государственная система наблюдений за состоянием водных объектов и ведение водного кадастра РК</p>
        </div>
    """, unsafe_allow_html=True)

    # --- 2. HIGHLIGHTS (Верхние карточки) ---
    st.markdown("""
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; margin-bottom: 30px;">
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #003366; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">🏢</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">442</div>
                        <div style="font-size: 1.0em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Гидропостов</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #004A99; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">📊</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">8</div>
                        <div style="font-size: 1.0em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Бассейнов</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #0288d1; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">🏛️</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #003366; line-height: 1.1;">24</div>
                        <div style="font-size: 1.0em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Вековых поста</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
            
            
            # 1. Словарь с путями к фото
    IMAGE_PATHS = {
                "HP": "HP1.jpeg",
                "Auto": "Aerology.jpeg",
                "TDS": "DMRL.jpeg",
                "Cadastre": "Cadastre.jpeg"
        }

    # 1. Создаем контейнер для карточек
    with st.container():
            h_col1, h_col2, h_col3, h_col4 = st.columns(4)

                # 3. Отрисовываем блоки (используем h_col вместо met_col, чтобы не путать с метео)
            draw_block(h_col1, "hydro_btn_1", "🌊 Национальная сеть гидрологических наблюдений", "📷", 
                           "Комплексный мониторинг рек, озер и каналов (442 поста).", 
                           [
                            "<b>Инфраструктура:</b> 25 снегомерных и 2 осадкомерных маршрута, 15 испарительных площадок",
                            "<b>Регламент:</b> Замеры уровня и температуры ежедневно в 08:00 и 20:00 (учащенно в паводки)",
                            "<b>Расход воды:</b> 3 раза в месяц в межень; 5-8 раз на подъеме и спаде половодья",
                            "<b>Оборудование:</b> Водомерные рейки, термометры, вертушки и Акустические доплеровские профилографы"
                            ], "HP")

            draw_block(h_col2, "hydro_btn_2", "📟 Автоматические посты", "📸", 
                           "Системы непрерывного мониторинга и передачи данных.", 
                           ["<b>Тип:</b> OTT Ecolog 1000", "<b>Режим:</b> поступление ежечасных данных каждые 4 часа", "<b>Передача:</b> GSM связь"], "Auto")

                # Блок трансграничного мониторинга
            draw_block(
                h_col3, 
                "hydro_btn_trans", 
                "🌍 Трансграничные посты", 
                "🤝", 
                "Мониторинг на водных объектах, разделяемых с сопредельными государствами.", 
                [
                    "<b>Всего:</b> 43 трансграничных гидрологических поста",
                    "<b>РФ и КНР:</b> 23 поста с Россией и 11 с Китаем",
                    "<b>Центральная Азия:</b> 7 постов с Кыргызстаном и 2 с Узбекистаном",
                    "<b>Цель:</b> совместный контроль водных ресурсов и обмен данными"
                ], 
                "TRANS"
            )

            draw_block(h_col4, "hydro_btn_4", "💧 Водный кадастр", "📁", 
                           "Единая система данных о водных ресурсах Казахстана.", 
                           ["<b>Процесс:</b> сбор, контроль, обработка и анализ данных гидронаблюдений",
                            "<b>Публикации:</b> ежегодные данные о режиме и ресурсах вод суши",
                            "<b>Справочники:</b> многолетние данные и материалы по испарению",
                            "<b>Цифровизация:</b> ведение электронного банка многолетних данных"
                            ],"Cadastre")
            st.write("##")


               # Данные на основе предоставленного изображения
            years = [
                1917, 1938, 1940, 1972, 1981, 1985, 1987, 1992, 1995, 2000, 
                2002, 2003, 2004, 2005, 2006, 2008, 2009, 2010, 2011, 2015, 
                2018, 2020, 2021, 2024, 2025, 2026
            ]
            posts = [
                123, 123, 150, 416, 506, 486, 432, 354, 322, 165, 
                209, 206, 215, 226, 251, 276, 291, 292, 298, 302, 
                310, 352, 377, 377, 410, 442
            ]

    def render_hydro_chart():
            # Основной цвет — темно-синий (#1f4e79), акцентный для 2026 — красный (#EF553B)
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
                hovertemplate="<b>Год: %{x}</b><br>Количество постов: %{y}<extra></extra>"
            ))

            fig.update_layout(
                title=dict(
                    text="Динамика развития гидрологической сети (1917-2026 гг.)",
                    font=dict(size=20) # Увеличили размер заголовка
                ),
                xaxis=dict(
                    title=dict(text="Год", font=dict(size=18)), # Шрифт заголовка оси X
                    type='category',
                    tickangle=-45,
                    tickfont=dict(size=16) # РАЗМЕР ШРИФТА ГОДОВ
                ),
                yaxis=dict(
                    title=dict(text="Количество постов", font=dict(size=18)), # Шрифт заголовка оси Y
                    range=[0, 600],
                    showgrid=True,
                    gridcolor='rgba(200, 200, 200, 0.2)',
                    tickfont=dict(size=16) # РАЗМЕР ШРИФТА ЧИСЕЛ (100, 200...)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                # УВЕЛИЧИЛИ ОТСТУПЫ (l=60, b=80), чтобы крупные подписи влезли
                margin=dict(l=60, r=20, t=80, b=80), 
                font=dict(color="white")
            )

            # Аннотация для выделения текущего статуса (2026 г. - 442 поста)
            fig.add_annotation(
                x=len(years)-1, 
                y=442,
                text="Текущий статус (2026)",
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-40,
                font=dict(color=highlight_color, size=13, family="Arial Black")
            )
            
            st.plotly_chart(fig, use_container_width=True)

    render_hydro_chart()

        # --- 1. ПОДГОТОВКА ДАННЫХ ---
    data = {
            "Область": [
                "Восточно-Казахстанская и Абайская", "Акмолинская", "Актюбинская", "Алматинская", "Атырауская", 
                "ЗКО", "Жамбылская", "Жетысу", "Карагандинская и Улытауская", "Костанайская", 
                "Кызылординская", "Мангистауская", "Павлодарская", "СКО", "Туркестанская"
            ],
            "Гидропосты": [68, 45, 39, 40, 15, 30, 24, 32, 38, 28, 13, 7, 6, 27, 30]
        }

    df_posts = pd.DataFrame(data).sort_values(by="Гидропосты", ascending=True)
    top_3_cutoff = df_posts["Гидропосты"].nlargest(3).min()
    colors_posts = ['#FFA500' if x >= top_3_cutoff else '#1f4e79' for x in df_posts["Гидропосты"]]

        # --- 2. ЗАГОЛОВОК ---
    st.subheader("📊 Мониторинг и информационная продукция")

        # --- 3. РАЗДЕЛЕНИЕ НА ЛЕВЫЙ И ПРАВЫЙ БЛОКИ ---
    col_graph, col_info = st.columns([2, 1], gap="large")

    with col_graph:
            # ЛЕВЫЙ БЛОК: ГРАФИК
            st.markdown("### Региональная сеть")
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=df_posts["Область"], x=df_posts["Гидропосты"],
                name="Посты", orientation='h', marker_color=colors_posts,
                text=df_posts["Гидропосты"], textposition='outside'
            ))
            
            fig.update_layout(
                barmode='group', 
                height=700, 
                # Увеличиваем левый отступ (l), так как названия областей длинные
                margin=dict(l=200, r=50, t=50, b=100), 
                
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color="#1f4e79"), # Темно-синий текст для светлой темы (как на фото)
                
                # Горизонтальная ось (теперь здесь ЧИСЛА)
                xaxis=dict(
                    visible=True,
                    showticklabels=True,
                    tickfont=dict(size=16, color="#1f4e79"),
                    title=dict(
                        text="Количество постов", 
                        font=dict(size=18, color="#1f4e79")
                    ),
                    gridcolor='rgba(0,0,0,0.1)',
                    automargin=True
                ),
                
                # Вертикальная ось (теперь здесь НАЗВАНИЯ ОБЛАСТЕЙ)
                yaxis=dict(
                    visible=True,
                    showticklabels=True,
                    # Указываем тип 'category' здесь, так как области по вертикали
                    type='category', 
                    tickfont=dict(size=16, color="#1f4e79"),
                    automargin=True,
                    # Убираем заголовок оси Y, так как названия регионов говорят сами за себя
                    title=dict(text="") 
                )
            )

            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})



    with col_info:
            # ПРАВЫЙ БЛОК: ПРОДУКЦИЯ (Стиль как на фото)
            st.markdown("### 📄 Выпускаемая продукция")
            
            # Стилизация карточек через Markdown
            st.info("""
            **📅 Ежедневные бюллетени**
            * Оперативные данные по уровням воды
            * Состояние снежного покрова в горах
            """)
            
            st.success("""
            **🌊 Прогнозы и кадастр**
            * Прогноз весеннего половодья (ежегодно)
            * Государственный водный кадастр
            * Справочники многолетних данных
            """)
            
            st.warning("""
            **🚨 Экстренные оповещения**
            * Штормовые предупреждения (ОЯ/НЯ)
            * Уведомления о резких подъемах уровней
            """)
            
            # Дополнительная метрика снизу
            st.divider()
            st.metric("Общий охват сети", f"{df_posts['Гидропосты'].sum()} постов", help="Данные на 2026 год")
            
            # Маленькая таблица ТОП-3
            st.write("**Топ-3 региона:**")
            st.table(df_posts.nlargest(3, 'Гидропосты')[['Область', 'Гидропосты']].set_index('Область'))


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

                
            
# 9. АГРОМЕТЕОРОЛОГИЧЕСКИЙ МОНИТОРИНГ
    st.markdown("""
            <div style="text-align:center; margin: 40px 0 20px 0;">
                <h2 style="color: #1b5e20; font-family: 'Exo 2', sans-serif; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; font-size: 2.2em;">
                    Агрометеорологический мониторинг
                </h2>
                <p style="color: #546e7a; font-size: 1.1em; font-weight: 500;">Гидрометеорологическое обеспечение продовольственной безопасности сельскохозяйственной отрасли Казахстана /на основе агрометеорологических наблюдений/
</p>
            </div>
        """, unsafe_allow_html=True)
        
        
            # 9.1 HIGHLIGHTS (Обновленная агро-статистика на основе слайда)
    st.markdown(f"""
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 12px; margin-bottom: 30px;">
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #1b5e20; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">📍</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #1b5e20; line-height: 1.1;">226</div>
                        <div style="font-size: 1.0em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Пунктов наблюдений</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #2e7d32; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">📲</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #1b5e20; line-height: 1.1;">100%</div>
                        <div style="font-size: 1.0em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Цифровая передача</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #43a047; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">📊</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #1b5e20; line-height: 1.1;">10</div>
                        <div style="font-size: 1.0em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Видов прогнозов</div>
                    </div>
                </div>
            </div>
            <div style="flex: 1; min-width: 160px; background: #ffffff; border-left: 5px solid #81c784; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8em;">🎯</span>
                    <div>
                        <div style="font-size: 1.5em; font-weight: 800; color: #1b5e20; line-height: 1.1;">78%</div>
                        <div style="font-size: 1.0em; color: #546e7a; text-transform: uppercase; font-weight: 700;">Оправдываемость</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


            # --- БЛОКИ С ПОДРОБНОСТЯМИ ---
            # 1. Словарь с путями к фото (Замените на актуальные пути для агро)
    AGRO_IMAGE_PATHS = {
                "Soil": "DMRL.jpeg",
                "Phenology": "DMRL.jpeg",
                "AutoAgro": "DMRL.jpeg",
        }

    a_col1, a_col2, a_col3  = st.columns(3)

    draw_block(a_col1, "agro_btn_1", "🌱 Традиционные наблюдения", "🚜", 
                       "На государственной агрометеорологической сети проводятся наблюдения за температурой и влажностью  воздуха, осадками, атмосферными явлениями, ветром, суммарной солнечной радиацией, температурой и состоянием почвы, за ростом сельскохозяйственных и пастбищных культур.", 
                       ["<b>129:</b> метеорологических станций", "<b>47:</b> агрометеорологических постов"], "Phenology")

    draw_block(a_col2, "agro_btn_2", "💧 Специальные измерения", "📉", 
                       "Наблюдения за влиянием погоды на растениеводство и животноводство.", 
                       ["<b>134:</b> пункта влажность почвы", "<b>100:</b> районов с маршрутными обследованиями"], "Soil")

    draw_block(a_col3, "agro_btn_3", "📡 Автоматизировано ", "📲", 
                       "Современные агрометеорологические посты оснащены автоматическими датчиками с передачей данных в центр обработки. Визуальные наблюдения и данные с ручных постов передаются автоматически после заноски данных с помощью планшета. ", 
                       ["<b>50:</b> агрометеорологических постов ", "<b>96:</b> влагомеров почвы"], "AutoAgro")


    import os
    import streamlit as st

    # 1. Используем глобальный BASE_DIR (определен в начале файла)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def render_final_agro_map():
        st.markdown("### 🗺️ Карта агромониторинга по областям")
        
        # Формируем путь к вашему изображению
        # Убедитесь, что файл на GitHub называется именно AGRO.jpg (регистр важен!)
        img_filename = "AGRO.jpg"
        img_path = os.path.join(BASE_DIR, img_filename)
        
        # Создаем две колонки: для карты и для пояснительного текста
        col_map, col_text = st.columns([3, 1])
        
        with col_map:
            # Проверка наличия файла, чтобы избежать MediaFileStorageError
            if os.path.exists(img_path):
                st.image(
                    img_path, 
                    caption="Схема агрометеорологических наблюдений с/х культур", 
                    use_container_width=True
                )
            else:
                st.error(f"⚠️ Файл '{img_filename}' не найден в репозитории.")
                # Подсказка для отладки
                st.info(f"Искал по пути: {img_path}")
                
        with col_text:
            st.markdown("""
            **О карте:**
            Данная схема отображает пункты агрометеорологического мониторинга по всей территории РК.
            
            **Основные культуры:**
            * 🌾 Зерновые
            * 🌽 Пропашные
            * 🌻 Масличные
            * 🍎 Плодовые
            """)
            
            # Кнопка для скачивания (если нужно)
            if os.path.exists(img_path):
                with open(img_path, "rb") as file:
                    st.download_button(
                        label="📂 Скачать карту",
                        data=file,
                        file_name="Agro_Map_Kazhydromet.jpg",
                        mime="image/jpg"
                    )

    # Вызов функции
    render_final_agro_map()


    
#АГРОКЛИМАТИЧЕСИК ЗОНЫ
    import streamlit as st
    import plotly.graph_objects as go
    import pandas as pd

    # Настройка широкого экрана
    st.set_page_config(layout="wide", page_title="Агроклиматический мониторинг")

    # 1. Справочник зон (Цвета и описания из предоставленной легенды)
    zones_info = {
        "I": {"color": "#385e26", "desc": "Слабо влажная умеренно-теплая"},
        "II": {"color": "#66ff66", "desc": "Засушливая умеренно-теплая"},
        "III": {"color": "#92d050", "desc": "Засушливая теплая"},
        "IV": {"color": "#ffff00", "desc": "Очень засушливая теплая"},
        "V": {"color": "#e6db98", "desc": "Сухая теплая"},
        "VI": {"color": "#f8cbad", "desc": "Сухая умеренно-теплая"},
        "VII": {"color": "#f1a1eb", "desc": "Очень сухая умеренно-жаркая"},
        "VIII": {"color": "#ff8080", "desc": "Очень сухая жаркая"},
        "IX": {"color": "#ff0000", "desc": "Очень сухая"},
        "X": {"color": "#bf9000", "desc": "Центрально-казахстанский мелкосопочник"},
        "XI": {"color": "#c00000", "desc": "Предгорья Заилийского Алатау"},
        "XIII": {"color": "#843c0c", "desc": "Предгорья Джунгарского Алатау"},
        "XIV": {"color": "#7f6000", "desc": "Предгорья Северного и Западного Тянь-Шаня"},
        "XV": {"color": "#00b0f0", "desc": "Долина р. Или"},
        "XVI": {"color": "#bcbcbc", "desc": "Горные районы"}
    }

    # 2. Полные данные (Оцифровано с вашего графика)
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

    df = pd.DataFrame(raw_data, columns=["Область", "Зона", "Процент"])

    st.subheader("Агроклиматические зоны по областям")

    # 3. Разделение на колонки: График (80%) и Легенда (20%)
    col_chart, col_legend = st.columns([4, 1])

    with col_chart:
        fig = go.Figure()

        # Отрисовка слоев зон
        for zone, info in zones_info.items():
            df_zone = df[df["Зона"] == zone]
            if not df_zone.empty:
                fig.add_trace(go.Bar(
                    name=zone,
                    y=df_zone["Область"],
                    x=df_zone["Процент"],
                    orientation='h',
                    marker=dict(color=info["color"]),
                    text=df_zone["Процент"],
                    textposition='inside',
                    insidetextanchor='middle',
                    textfont=dict(color="black", size=11, family="Arial Black"),
                    hovertemplate=f"<b>Зона {zone}</b>: %{{x}}%<extra></extra>"
                ))

        # Настройки отображения графика
        fig.update_layout(
            barmode='stack',
            height=750,
            # УВЕЛИЧИВАЕМ ОТСТУП СЛЕВА ДО 250. 
            # Названия типа "Восточно-Казахстанская и Абайская" требуют много места.
            margin=dict(l=250, r=20, t=50, b=50), 
            
            # Ось X (проценты снизу)
            xaxis=dict(
                visible=True, 
                range=[0, 100],
                tickfont=dict(size=16, color="#1f4e79"),
                title=dict(text="%", font=dict(size=14, color="#1f4e79")),
                gridcolor='rgba(0,0,0,0.1)'
            ),
            
            # Ось Y (ЗДЕСЬ НАЗВАНИЯ ОБЛАСТЕЙ)
            yaxis=dict(
                visible=True,           # ПРИНУДИТЕЛЬНО ВКЛЮЧИТЬ
                showticklabels=True,    # ПОКАЗАТЬ ПОДПИСИ
                autorange="reversed", 
                type='category',        # ЯВНО УКАЗЫВАЕМ, ЧТО ЭТО ТЕКСТ
                tickfont=dict(
                    size=16, 
                    family="Arial", 
                    color="#1f4e79"     # ТЕМНО-СИНИЙ (не белый!)
                ),
                automargin=False        # Отключаем авто, так как мы задали l=250 вручную
            ),
            
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        # Шрифт цифр внутри полосок
        fig.update_traces(
            textfont=dict(size=18, family="Arial Black", color="black"),
            textposition='inside'
        )

        st.plotly_chart(fig, use_container_width=True)

    # 4. Наполнение правой колонки легендой
    with col_legend:
        st.markdown("<br><br>", unsafe_allow_html=True) # Отступ сверху
        st.write("**Легенда зон:**")
        
        for zone, info in zones_info.items():
            # HTML-контейнер для каждой строки легенды
            st.markdown(
                f'''
                <div style="display: flex; align-items: flex-start; margin-bottom: 6px;">
                    <div style="
                        min-width: 16px; 
                        height: 16px; 
                        background-color: {info["color"]}; 
                        margin-right: 8px; 
                        margin-top: 2px;
                        border: 1px solid #444;">
                    </div>
                    <div style="font-size: 1.0rem; line-height: 1.1;">
                        <strong>{zone}</strong>: {info["desc"]}
                    </div>
                </div>
                ''', 
                unsafe_allow_html=True
            )


    import streamlit as st
    from PIL import Image
    import os

    def render_agro_climate_comparison():
        st.markdown("---")
        # Заголовок блока
        st.markdown("### 🌡️ Сравнительный анализ климатических показателей")

        # Пути к файлам (используем ваши локальные пути)
        path_temp2 = "agro2.jpg"
        path_gtk = "agro 3.png"

        # Создаем две колонки для визуального сопоставления
        col_left, col_right = st.columns(2)

        with col_left:
            st.info("Суммы эффективных температур воздуха (норма)")
            if os.path.exists(path_temp2):
                img_temp = Image.open(path_temp2)
                st.image(img_temp, use_container_width=True, caption="Карта температур за август")
            else:
                st.error(f"Файл не найден: {path_temp2}")

        with col_right:
            st.info("Гидротермический коэффициент (ГТК) Селянинова")
            if os.path.exists(path_gtk):
                img_gtk = Image.open(path_gtk)
                st.image(img_gtk, use_container_width=True, caption="ГТК за период 1991-2020 гг.")
                
                # Добавляем расшифровку ГТК прямо под картинкой для удобства
                with st.expander("🔍 Показать расшифровку ГТК"):
                    st.markdown("""
                    * 🟦 **ГТК > 0.8** — хорошо увлажнено
                    * 🟩 **ГТК = 0.6 - 0.8** — слабо увлажнено
                    * 🟧 **ГТК = 0.4 - 0.6** — средне засушливо
                    * 🟨 **ГТК < 0.4** — сильно засушливо
                    """)
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
with tabs[1]:
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
                <div class="title">Консультативные прогнозы</div>
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
    col_acc1, col_acc2, col_acc3, col_acc4, col_acc5  = st.columns(5)
    with col_acc1:
        st.metric("Суточные прогнозы", "96%", help="Высочайшая точность подтверждена верификацией")
    with col_acc2:
        st.metric("Прогнозы на 2-3 дня", "92%")
    with col_acc3:
        st.metric("Прогнозы на неделю", "91%")
    with col_acc4:
        st.metric("Прогнозы на месяц", "75%")
    with col_acc5:
        st.metric("Прогнозы на сезон", "65%")
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
                <div class="info-row"><b>🔄 Регулярность:</b> Выпускается ежедневно в 20:00</div>
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
        col_climat_data, col_viz1 = st.columns([1.2, 1], gap="medium")

        with col_climat_data:
            st.markdown("#### 📜 Климатическая характеристика: Март")
                
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
                        <div class="info-item">🔹 Север: <span class="val-bold">-9...-14°С</span></div>
                        <div class="info-item">🔹 Юг: <span class="val-bold">+6...+8°С</span></div>
                    </div>
                    <div class="big-climate-card" style="flex: 1;">
                        <div class="section-title">❄️ Экстремумы</div>
                        <div class="info-item">🔴 Тепло: <span class="val-bold">до +35°С</span></div>
                        <div class="info-item">🔵 Холод: <span class="val-bold">до -47°С</span></div>
                    </div>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 10px;">
                    <div class="big-climate-card" style="flex: 1;">
                        <div class="section-title">💧 Осадки</div>
                        <div class="info-item">📅 В среднем: <span class="val-bold">14-25 мм</span></div>
                        <div class="info-item">📅 Вид: <span class="val-bold">смешанные</span></div>
                    </div>
                    <div class="big-climate-card" style="flex: 1; border-left: 5px solid #f39c12;">
                        <div class="section-title">🌬️ Явления</div>
                        <div class="info-item">🚩 Метели: <span class="val-bold">до 20 дн.</span></div>
                        <div class="info-item">⚡ Гололед: <span class="val-bold">2-3 раза</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        with col_viz1:
            st.subheader("🗺️ Визуализация")
            st.image(os.path.join(BASE_DIR, "udpp1.gif"), use_container_width=True)
            
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
                height: 180px; /* Уменьшили высоту, т.к. нет фото */
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
            {"title": "Строительство", "desc": "информация о продолжительности строительного сезона.", "emoji": "🏗️"},
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
                
                

with tabs[2]:
    st.title("Агрометеорологические прогнозы")

with tabs[3]:
    st.title("Гидрологические прогнозы")

  # ВОДНЫЕ РЕСУРСЫ
with tabs[4]:
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
    
                
    for name in vxb_list:
        # Берем данные из нашего справочника. Если данных нет — берем пустой словарь
        details = VXB_FULL_DATA.get(name, {})
        
        if not details:
            st.warning(f"Данные для {name} еще не внесены в справочник.")
            continue

        item_stats = VXB_STATS[name]
        is_active = (name == display_name)
        anchor_name = name.replace(' ', '-').lower()
        
        # Путь к фото теперь берется из справочника
        photo_path = os.path.join(BASE_IMAGE_PATH, details["photo"])
        
        st.markdown(f"<div id='{anchor_name}'></div>", unsafe_allow_html=True)
        
        with st.container(border=is_active):
            st.markdown(f"### {'🌟' if is_active else '🔹'} {name}")
            
            img_col, info_col = st.columns([1.2, 1])
            
            with img_col:
                if os.path.exists(photo_path):
                    st.image(photo_path, use_container_width=True, caption=f"Вид бассейна: {name}")
                else:
                    st.info(f"📸 Фото для {name} ожидается")
                    st.image("https://via.placeholder.com/600x400?text=Photo+Missing", use_container_width=True)
            
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
                

  

# --- Твой основной контент по Каспию идет во вкладку №5 (индекс 5) ---
with tabs[5]:
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
                        

        # 3. ПЕРВЫЙ БЛОК: ИЗМЕНЕНИЕ АКВАТОРИИ
        st.markdown("""
            <div style="background: #F0F9FF; padding: 20px; border-radius: 20px; border: 1px solid #BAE6FD; margin-top: 15px; font-family: 'Montserrat', sans-serif;">
                <p style="margin: 0 0 15px 0; color: #0369A1; font-weight: 600; font-size: 1.1rem; text-align: center; text-transform: uppercase;">
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

    st.divider()
    
    # --- ОБЩИЙ БЛОК: ОСНОВНЫЕ ФАКТОРЫ ---
    st.markdown("<hr style='margin: 40px 0; opacity: 0.1;'>", unsafe_allow_html=True)
    st.markdown('<div class="white-label-header"><p style="font-size: 3.0rem; font-weight: bold; margin-bottom: 12px;">🔍 Основные факторы, влияющие на изменение уровня</p></div>', unsafe_allow_html=True) 

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
    st.divider()
    
    
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

    st.divider()
    
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
        
        
    st.divider()        
        
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

    st.divider()
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

    st.divider()
    
    
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

    

with tabs[6]:
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
                        <div class="m-value">+0.29 °С</div>
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

    st.markdown("---")
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
                    Отклонение от нормы составило рекордные <b>+2,96°С</b>.
                </p>
                <p style="font-size: 0.9rem; color: #666;">
                    Примечательно, что <b>9 из 10</b> самых теплых лет пришлись на XXI век, что подтверждает ускорение глобального потепления.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_chart:
        st.caption("Ранг лет с наибольшими положительными аномалиями (1941–2025)")
        
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
        # Путь к вашему изображению
        map_path = r"C:\Users\eltai_a\Desktop\RES\stend\02_зима_нд.jpg"
        
        if os.path.exists(map_path):
            st.image(map_path, caption="Карта аномалий: Зима (анализ данных)", use_container_width=True)
        else:
            st.error(f"Файл не найден по пути: {map_path}")
            # Заглушка, если файла нет
            st.info("Здесь должна быть карта: 02_зима_нд.jpg")
            
            

    st.subheader("📈 Климат областей")
    import streamlit as st
    import pandas as pd
    import streamlit.components.v1 as components



    # --- 1. БАЗА ДАННЫХ ВСЕХ 17 ОБЛАСТЕЙ ---
    # Вы можете дополнять этот словарь данными для каждой области
    ALL_REGIONS_DATABASE = {
        "Северо-Казахстанская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Акмолинская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Западно-Казахстанская": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Атырауская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Мангистауская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Актюбинская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Улытауская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Восточно-Казахстанская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Абайская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Костанайская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Павлодарская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Алматинская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Жетысуская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Туркестанкая область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Кызылординская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Жамбылская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        },
        "Павлодарская область": {
            "geo_text": "Северо-Казахстанская область расположена на севере Казахстана, занимая южную окраину Западно-Сибирской равнины. Климат региона резко континентальный, характеризующийся значительными температурными амплитудами. ",
            "stations": 7,
            "area": "97 993 км²",
            "area_perc": "3.6%",
            "temp_2025": 5.1,
            "norm_temp": 1.8,
            "anom_2025": 3.28,
            "precip_2025": 439.8,
            "prec_norm": "124.7%",
            "temp_extreme": {"max": "+24°С (июль 1989)", "min": "-29.8°С (январь 1969)"},
            "top_years": [
                {"year": 2025, "val": 5.09, "col": "#990000"},
                {"year": 2020, "val": 4.98, "col": "#b30000"},
                {"year": 2023, "val": 4.43, "col": "#d32f2f"},
                {"year": 1983, "val": 4.01, "col": "#e57373"},
                {"year": 1995, "val": 3.73, "col": "#ef9a9a"}
            ],
            "zones": [
            {
                "title": "🌳 Лесостепная (~45%)",
                "desc": "Северная часть, обилие березовых колков и озер.",
                "precip": "Повышенные (380-450 мм)",
                "color": "#2e7d32",
                "bg": "#f1f8e9"
            },
            {
                "title": "🌾 Степная (~55%)",
                "desc": "Южная часть, открытые равнинные пространства.",
                "precip": "Умеренные (320-380 мм)",
                "color": "#f57c00",
                "bg": "#fff3e0"
            }
            ]      
        } 
}

    import pandas as pd
    import plotly.graph_objects as go

    # 1. Полный массив данных (1940-2025)
    data_list = [
        {"Год": 1940, "ЗКО": -0.445, "Атырау": -0.497, "Мангистау": 0.1, "Актюбинская": 0.25, "Карагандинская": -0.168, "Улытауская": 1.003, "ВКО": 0.177, "Абай": 0.2, "СКО": -0.626, "Акмола": -0.174, "Костанай": -0.087, "Павлодар": 0.092, "Алматиснкая": 1.443, "Жетысу": 0.89, "Туркестанская": 0.861, "Кызылординская": 0.672, "Жамбылская": 0.9},
        {"Год": 1941, "ЗКО": -2.3, "Атырау": -0.794, "Мангистау": -0.458, "Актюбинская": -1.49, "Карагандинская": -0.196, "Улытауская": -0.194, "ВКО": 0.602, "Абай": 0.361, "СКО": -2.675, "Акмола": -1.904, "Костанай": -2.322, "Павлодар": -1.492, "Алматиснкая": -0.349, "Жетысу": 1.509, "Туркестанская": 1.369, "Кызылординская": 0.742, "Жамбылская": 1.505},
        {"Год": 1942, "ЗКО": -2.904, "Атырау": -2.21, "Мангистау": -1.767, "Актюбинская": -1.837, "Карагандинская": -0.469, "Улытауская": -0.656, "ВКО": -0.259, "Абай": -0.107, "СКО": -1.356, "Акмола": -1.245, "Костанай": -1.733, "Павлодар": -0.24, "Алматиснкая": -0.532, "Жетысу": -0.343, "Туркестанская": -0.079, "Кызылординская": -0.023, "Жамбылская": -0.407},
        {"Год": 1943, "ЗКО": -1.319, "Атырау": -0.937, "Мангистау": -0.933, "Актюбинская": -1.254, "Карагандинская": -1.587, "Улытауская": -1.8, "ВКО": -0.644, "Абай": -0.62, "СКО": -1.17, "Акмола": -1.282, "Костанай": -1.138, "Павлодар": -1.025, "Алматиснкая": -0.429, "Жетысу": -0.664, "Туркестанская": -1.118, "Кызылординская": -1.253, "Жамбылская": -1.151},
        {"Год": 1944, "ЗКО": 0.291, "Атырау": 0.606, "Мангистау": 0.383, "Актюбинская": 0.613, "Карагандинская": 0.28, "Улытауская": 0.533, "ВКО": -0.815, "Абай": -0.627, "СКО": 0.235, "Акмола": 0.433, "Костанай": 0.509, "Павлодар": 0.119, "Алматиснкая": -0.652, "Жетысу": -0.62, "Туркестанская": 0.539, "Кызылординская": 0.788, "Жамбылская": 0.033},
        {"Год": 1945, "ЗКО": -2.705, "Атырау": -2.186, "Мангистау": -1.85, "Актюбинская": -2.254, "Карагандинская": -0.96, "Улытауская": -1.481, "ВКО": -0.123, "Абай": -0.372, "СКО": -1.967, "Акмола": -1.643, "Костанай": -2.051, "Павлодар": -1.27, "Алматиснкая": -0.629, "Жетысу": -0.238, "Туркестанская": -0.827, "Кызылординская": -1.827, "Жамбылская": -1.118},
        {"Год": 1946, "ЗКО": -0.263, "Атырау": 0.075, "Мангистау": 0, "Актюбинская": -0.304, "Карагандинская": -1.413, "Улытауская": -1.099, "ВКО": -0.501, "Абай": -0.608, "СКО": -1.154, "Акмола": -1.321, "Костанай": -0.961, "Павлодар": -0.978, "Алматиснкая": -0.265, "Жетысу": -0.516, "Туркестанская": -0.423, "Кызылординская": -0.352, "Жамбылская": -0.42},
        {"Год": 1947, "ЗКО": -0.515, "Атырау": -0.044, "Мангистау": -0.058, "Актюбинская": -0.512, "Карагандинская": -0.959, "Улытауская": -0.578, "ВКО": -0.701, "Абай": -0.73, "СКО": -0.917, "Акмола": -0.905, "Костанай": -0.84, "Павлодар": -0.928, "Алматиснкая": -0.165, "Жетысу": -0.281, "Туркестанская": 0.17, "Кызылординская": 0.048, "Жамбылская": -0.263},
        {"Год": 1948, "ЗКО": 0.736, "Атырау": 0.599, "Мангистау": 0.25, "Актюбинская": 0.669, "Карагандинская": -0.297, "Улытауская": 0.1, "ВКО": 0.677, "Абай": 0.402, "СКО": 0.157, "Акмола": 0.083, "Костанай": 0.457, "Павлодар": 0.228, "Алматиснкая": -1.073, "Жетысу": -0.106, "Туркестанская": -0.235, "Кызылординская": 0.63, "Жамбылская": -0.187},
        {"Год": 1949, "ЗКО": -0.856, "Атырау": -1.117, "Мангистау": -1.033, "Актюбинская": -1.233, "Карагандинская": -1.598, "Улытауская": -1.736, "ВКО": -0.912, "Абай": -1.141, "СКО": -0.705, "Акмола": -1.13, "Костанай": -1.04, "Павлодар": -0.855, "Алматиснкая": -0.818, "Жетысу": -1.151, "Туркестанская": -1.746, "Кызылординская": -1.505, "Жамбылская": -1.432},
        {"Год": 1950, "ЗКО": -1.604, "Атырау": -1.672, "Мангистау": -1.125, "Актюбинская": -1.785, "Карагандинская": -1.482, "Улытауская": -1.939, "ВКО": -1.807, "Абай": -1.619, "СКО": -1.589, "Акмола": -1.854, "Костанай": -1.795, "Павлодар": -1.542, "Алматиснкая": -0.738, "Жетысу": -1.083, "Туркестанская": -1.687, "Кызылординская": -2.055, "Жамбылская": -1.535},
        {"Год": 1951, "ЗКО": -0.557, "Атырау": -0.814, "Мангистау": -0.342, "Актюбинская": -0.199, "Карагандинская": -0.427, "Улытауская": -0.664, "ВКО": -0.101, "Абай": -0.16, "СКО": -0.117, "Акмола": -0.258, "Костанай": -0.295, "Павлодар": 0.308, "Алматиснкая": -0.94, "Жетысу": -0.827, "Туркестанская": -0.944, "Кызылординская": -0.813, "Жамбылская": -1.413},
        {"Год": 1952, "ЗКО": -0.873, "Атырау": -0.758, "Мангистау": -0.308, "Актюбинская": -0.528, "Карагандинская": -1.456, "Улытауская": -0.997, "ВКО": -2.02, "Абай": -1.886, "СКО": -1.13, "Акмола": -1.065, "Костанай": -0.908, "Павлодар": -1.3, "Алматиснкая": 0.149, "Жетысу": -1.463, "Туркестанская": -0.601, "Кызылординская": -0.683, "Жамбылская": -1.201},
        {"Год": 1953, "ЗКО": -0.929, "Атырау": -0.475, "Мангистау": -0.433, "Актюбинская": -0.644, "Карагандинская": -0.27, "Улытауская": 0.067, "ВКО": 0.623, "Абай": 0.275, "СКО": -0.851, "Акмола": -0.431, "Костанай": -0.797, "Павлодар": 0.12, "Алматиснкая": -1.846, "Жетысу": 0.286, "Туркестанская": -0.226, "Кызылординская": 0.163, "Жамбылская": 0.051},
        {"Год": 1954, "ЗКО": -1.594, "Атырау": -1.939, "Мангистау": -0.95, "Актюбинская": -1.582, "Карагандинская": -2.317, "Улытауская": -2.028, "ВКО": -2.488, "Абай": -2.426, "СКО": -2.262, "Акмола": -2.241, "Костанай": -1.845, "Павлодар": -2.798, "Алматиснкая": 0.017, "Жетысу": -2.043, "Туркестанская": -1.596, "Кызылординская": -1.722, "Жамбылская": -2.239},
        {"Год": 1955, "ЗКО": 0.245, "Атырау": 0.275, "Мангистау": 0.683, "Актюбинская": 0.088, "Карагандинская": -0.03, "Улытауская": 0.308, "ВКО": 0.145, "Абай": 0.027, "СКО": -0.734, "Акмола": -0.211, "Костанай": -0.431, "Павлодар": 0.133, "Алматиснкая": 0.044, "Жетысу": -0.093, "Туркестанская": 0.605, "Кызылординская": 0.493, "Жамбылская": -0.03},
        {"Год": 1956, "ЗКО": -2.182, "Атырау": -2.044, "Мангистау": -1.325, "Актюбинская": -1.399, "Карагандинская": -0.496, "Улытауская": -1.144, "ВКО": -1.305, "Абай": -0.863, "СКО": -1.327, "Акмола": -1.001, "Костанай": -1.371, "Павлодар": -0.818, "Алматиснкая": -0.923, "Жетысу": -0.153, "Туркестанская": -0.201, "Кызылординская": -0.782, "Жамбылская": -0.257},
        {"Год": 1957, "ЗКО": 0.304, "Атырау": 0.146, "Мангистау": 0.767, "Актюбинская": -0.049, "Карагандинская": -0.868, "Улытауская": -0.942, "ВКО": -0.536, "Абай": -0.541, "СКО": 0.243, "Акмола": -0.298, "Костанай": -0.083, "Павлодар": -0.165, "Алматиснкая": -0.294, "Жетысу": -0.847, "Туркестанская": -1.406, "Кызылординская": -0.762, "Жамбылская": -1.13},
        {"Год": 1958, "ЗКО": -0.26, "Атырау": -0.038, "Мангистау": -0.117, "Актюбинская": -0.455, "Карагандинская": -1.268, "Улытауская": -1.183, "ВКО": -1.08, "Абай": -0.946, "СКО": -0.487, "Акмола": -0.977, "Костанай": -0.562, "Павлодар": -0.994, "Алматиснкая": -0.754, "Жетысу": -0.449, "Туркестанская": -0.299, "Кызылординская": -0.12, "Жамбылская": -0.482},
        {"Год": 1959, "ЗКО": -1.909, "Атырау": -1.799, "Мангистау": -1.558, "Актюбинская": -1.815, "Карагандинская": -1.236, "Улытауская": -1.403, "ВКО": -1.096, "Абай": -1.013, "СКО": -0.775, "Акмола": -0.953, "Костанай": -1.279, "Павлодар": -0.623, "Алматиснкая": -1.16, "Жетысу": -0.845, "Туркестанская": -0.819, "Кызылординская": -1.575, "Жамбылская": -1.01},
        {"Год": 1960, "ЗКО": -0.755, "Атырау": -0.478, "Мангистау": -0.417, "Актюбинская": -1.583, "Карагандинская": -2.143, "Улытауская": -2.422, "ВКО": -1.986, "Абай": -2.015, "СКО": -1.705, "Акмола": -1.909, "Костанай": -1.592, "Павлодар": -2.073, "Алматиснкая": 0.194, "Жетысу": -1.582, "Туркестанская": -1.006, "Кызылординская": -1.475, "Жамбылская": -1.524},
        {"Год": 1961, "ЗКО": 0.641, "Атырау": 0.828, "Мангистау": 0.475, "Актюбинская": 0.728, "Карагандинская": 0.205, "Улытауская": 0.069, "ВКО": -0.186, "Абай": -0.053, "СКО": 0.818, "Акмола": 0.496, "Костанай": 0.821, "Павлодар": 0.563, "Алматиснкая": 0.384, "Жетысу": -0.007, "Туркестанская": 0.555, "Кызылординская": 0.258, "Жамбылская": 0.444},
        {"Год": 1962, "ЗКО": 1.065, "Атырау": 0.758, "Мангистау": 0.833, "Актюбинская": 0.801, "Карагандинская": 0.474, "Улытауская": 0.35, "ВКО": 1.083, "Абай": 1.001, "СКО": 1.751, "Акмола": 1.266, "Костанай": 1.194, "Павлодар": 1.05, "Алматиснкая": 0.919, "Жетысу": 0.532, "Туркестанская": -0.114, "Кызылординская": -0.002, "Жамбылская": 0.114},
        {"Год": 1963, "ЗКО": -0.304, "Атырау": 0.228, "Мангистау": -0.108, "Актюбинская": 0.242, "Карагандинская": 0.968, "Улытауская": 1.189, "ВКО": 1.119, "Абай": 1.192, "СКО": 1.037, "Акмола": 1.158, "Костанай": 0.869, "Павлодар": 1.458, "Алматиснкая": -0.926, "Жетысу": 0.847, "Туркестанская": 0.745, "Кызылординская": 1.015, "Жамбылская": 0.767},
        {"Год": 1964, "ЗКО": -1.249, "Атырау": -0.916, "Мангистау": -0.8, "Актюбинская": -1.31, "Карагандинская": -0.973, "Улытауская": -0.903, "ВКО": -0.337, "Абай": -0.621, "СКО": -1.0, "Акмола": -0.966, "Костанай": -1.018, "Павлодар": -0.392, "Алматиснкая": 0.521, "Жетысу": -1.144, "Туркестанская": -1.217, "Кызылординская": -0.995, "Жамбылская": -1.108},
        {"Год": 1965, "ЗКО": 0, "Атырау": -0.414, "Мангистау": -0.55, "Актюбинская": 0.102, "Карагандинская": 0.364, "Улытауская": 0.511, "ВКО": 0.396, "Абай": 0.607, "СКО": 0.91, "Акмола": 0.841, "Костанай": 0.337, "Павлодар": 0.713, "Алматиснкая": 0.038, "Жетысу": 0.71, "Туркестанская": 0.436, "Кызылординская": 0.313, "Жамбылская": 0.645},
        {"Год": 1966, "ЗКО": 1.09, "Атырау": 0.775, "Мангистау": 1.417, "Актюбинская": 0.396, "Карагандинская": -0.331, "Улытауская": 0.014, "ВКО": -1.422, "Абай": -1.191, "СКО": -1.15, "Акмола": -0.954, "Костанай": -0.599, "Павлодар": -1.522, "Алматиснкая": -0.614, "Жетысу": -0.02, "Туркестанская": 0.573, "Кызылординская": 0.395, "Жамбылская": 0.083},
        {"Год": 1967, "ЗКО": 0.796, "Атырау": -0.006, "Мангистау": 0.1, "Актюбинская": 0.927, "Карагандинская": 0.113, "Улытауская": 0.003, "ВКО": -1.036, "Абай": -0.648, "СКО": 0.551, "Акмола": 0.486, "Костанай": 0.449, "Павлодар": 0.038, "Алматиснкая": -0.369, "Жетысу": -0.807, "Туркестанская": 0.005, "Кызылординская": -0.133, "Жамбылская": -0.401},
        {"Год": 1968, "ЗКО": -0.778, "Атырау": -0.164, "Мангистау": 0.225, "Актюбинская": -0.526, "Карагандинская": -0.327, "Улытауская": -0.525, "ВКО": -0.419, "Абай": -0.564, "СКО": -0.856, "Акмола": -0.395, "Костанай": -0.594, "Павлодар": -0.87, "Алматиснкая": -1.689, "Жетысу": -0.385, "Туркестанская": -0.244, "Кызылординская": -0.635, "Жамбылская": -0.625},
        {"Год": 1969, "ЗКО": -2.57, "Атырау": -1.722, "Мангистау": -1.775, "Актюбинская": -2.206, "Карагандинская": -2.115, "Улытауская": -2.078, "ВКО": -2.682, "Абай": -2.697, "СКО": -2.769, "Акмола": -2.719, "Костанай": -2.545, "Павлодар": -3.09, "Алматиснкая": -0.141, "Жетысу": -1.822, "Туркестанская": -1.882, "Кызылординская": -1.863, "Жамбылская": -2.23},
        {"Год": 1970, "ЗКО": -0.438, "Атырау": 0.108, "Мангистау": 0.158, "Актюбинская": -0.568, "Карагандинская": -0.448, "Улытауская": -0.603, "ВКО": -0.634, "Абай": -0.633, "СКО": -0.465, "Акмола": -0.607, "Костанай": -0.405, "Павлодар": -0.698, "Алматиснкая": 0.465, "Жетысу": -0.31, "Туркестанская": 0.087, "Кызылординская": -0.147, "Жамбылская": -0.248},
        {"Год": 1971, "ЗКО": 0.2, "Атырау": 0.294, "Мангистау": 0.692, "Актюбинская": 0.379, "Карагандинская": 0.32, "Улытауская": 0.567, "ВКО": 0.424, "Абай": 0.189, "СКО": 0.594, "Акмола": 0.446, "Костанай": 0.702, "Павлодар": 0.218, "Алматиснкая": -1.344, "Жетысу": 0.497, "Туркестанская": 0.737, "Кызылординская": 0.433, "Жамбылская": 0.54},
        {"Год": 1972, "ЗКО": -0.419, "Атырау": -0.878, "Мангистау": -0.417, "Актюбинская": -1.24, "Карагандинская": -1.868, "Улытауская": -2.3, "ВКО": -0.731, "Абай": -1.347, "СКО": -1.698, "Акмола": -1.873, "Костанай": -1.469, "Павлодар": -1.508, "Алматиснкая": 0.383, "Жетысу": -1.405, "Туркестанская": -2.232, "Кызылординская": -2.003, "Жамбылская": -1.911},
        {"Год": 1973, "ЗКО": 0.222, "Атырау": -0.069, "Мангистау": -0.517, "Актюбинская": -0.031, "Карагандинская": 0.451, "Улытауская": 0.114, "ВКО": 1, "Абай": 0.758, "SКО": -0.01, "Акмола": -0.073, "Костанай": -0.083, "Павлодар": 0.438, "Алматиснкая": -1.056, "Жетысу": 0.376, "Туркестанская": 0.143, "Кызылординская": -0.152, "Жамбылская": 0.501},
        {"Год": 1974, "ЗКО": -0.001, "Атырау": -0.242, "Мангистау": -0.142, "Актюбинская": 0.117, "Карагандинская": -0.602, "Улытауская": -0.658, "ВКО": -0.813, "Абай": -0.814, "SКО": -0.51, "Акмола": -0.559, "Костанай": -0.208, "Павлодар": -1.148, "Алматиснкая": 0.184, "Жетысу": -1.049, "Туркестанская": -1.018, "Кызылординская": -1.103, "Жамбылская": -1.336},
        {"Год": 1975, "ЗКО": 1.531, "Атырау": 1.294, "Мангистау": 0.967, "Актюбинская": 1.144, "Карагандинская": 0.79, "Улытауская": 0.778, "ВКО": 0.858, "Абай": 0.817, "SКО": 1.207, "Акмола": 1.1, "Костанай": 1.088, "Павлодар": 1.093, "Алматиснкая": -0.608, "Жетысу": 0.22, "Туркестанская": 0.517, "Кызылординская": 0.797, "Жамбылская": 0.546},
        {"Год": 1976, "ЗКО": -2.216, "Атырау": -1.278, "Мангистау": -1.225, "Актюбинская": -1.903, "Карагандинская": -1.363, "Улытауская": -1.867, "ВКО": -0.984, "Абай": -1.061, "SКО": -1.487, "Акмола": -1.621, "Костанай": -2.026, "Павлодар": -1.125, "Алматиснкая": 0.325, "Жетысу": -0.656, "Туркестанская": -0.501, "Кызылординская": -1.347, "Жамбылская": -0.645},
        {"Год": 1977, "ЗКО": 0.181, "Атырау": -0.05, "Мангистау": -0.275, "Актюбинская": 0.344, "Карагандинская": 0.336, "Улытауская": 0.289, "ВКО": 0.48, "Абай": 0.183, "SКО": 0.162, "Акмола": 0.185, "Костанай": -0.024, "Павлодар": 0.047, "Алматиснкая": 0.467, "Жетысу": 0.438, "Туркестанская": 0.308, "Кызылординская": 0.262, "Жамбылская": 0.318},
        {"Год": 1978, "ЗКО": -0.878, "Атырау": -0.286, "Мангистау": -0.408, "Актюбинская": -0.511, "Карагандинская": 0.337, "Улытауская": -0.064, "ВКО": 0.905, "Абай": 0.868, "SКО": 0.249, "Акмола": 0.254, "Костанай": 0.051, "Павлодар": 0.552, "Алматиснкая": 0.065, "Жетысу": 0.608, "Туркестанская": -0.045, "Кызылординская": -0.262, "Жамбылская": 0.326},
        {"Год": 1979, "ЗКО": 0.484, "Атырау": 1.125, "Мангистау": 0.9, "Актюбинская": 0.447, "Карагандинская": -0.119, "Улытауская": 0.469, "ВКО": -0.359, "Абай": -0.454, "SКО": -0.525, "Акмола": -0.421, "Костанай": -0.26, "Павлодар": -0.257, "Алматиснкая": 0.741, "Жетысу": 0.013, "Туркестанская": 0.281, "Кызылординская": 1.042, "Жамбылская": 0.185},
        {"Год": 1980, "ЗКО": -0.807, "Атырау": -0.642, "Мангистау": -0.408, "Актюбинская": -0.79, "Карагандинская": 0.418, "Улытауская": 0.025, "ВКО": 0.313, "Абай": 0.429, "SКО": -0.665, "Акмола": -0.457, "Костанай": -0.946, "Павлодар": -0.288, "Алматиснкая": 0.184, "Жетысу": 0.771, "Туркестанская": 0.393, "Кызылординская": -0.438, "Жамбылская": 0.639},
        {"Год": 1981, "ЗКО": 1.531, "Атырау": 1.294, "Мангистау": 0.967, "Актюбинская": 1.144, "Карагандинская": 0.79, "Улытауская": 0.778, "ВКО": 0.858, "Абай": 0.817, "SКО": 1.207, "Акмола": 1.1, "Костанай": 1.088, "Павлодар": 1.093, "Алматиснкая": 0.357, "Жетысу": 0.22, "Туркестанская": 0.517, "Кызылординская": 0.797, "Жамбылская": 0.546},
        {"Год": 1982, "ЗКО": 0.356, "Атырау": -0.669, "Мангистау": -0.7, "Актюбинская": 0.1, "Карагандинская": 0.773, "Улытауская": 0.539, "ВКО": 1.54, "Абай": 1.49, "SКО": 1.027, "Акмола": 0.867, "Костанай": 0.711, "Павлодар": 1.415, "Алматиснкая": 1.241, "Жетысу": 0.586, "Туркестанская": -0.356, "Кызылординская": -0.082, "Жамбылская": 0.242},
        {"Год": 1983, "ЗКО": 1.575, "Атырау": 1.456, "Мангистау": 0.575, "Актюбинская": 1.797, "Карагандинская": 1.745, "Улытауская": 2.189, "ВКО": 1.677, "Абай": 1.944, "SКО": 2.193, "Акмола": 2.056, "Костанай": 2.207, "Павлодар": 2.327, "Алматиснкая": -1.292, "Жетысу": 1.425, "Туркестанская": 1.186, "Кызылординская": 2.137, "Жамбылская": 1.599},
        {"Год": 1984, "ЗКО": -0.193, "Атырау": -0.272, "Мангистау": -0.517, "Актюбинская": -0.481, "Карагандинская": -1.35, "Улытауская": -0.878, "ВКО": -2.18, "Абай": -1.993, "SКО": -1.285, "Акмола": -1.352, "Костанай": -0.619, "Павлодар": -1.708, "Алматиснкая": -0.255, "Жетысу": -1.442, "Туркестанская": -1.214, "Кызылординская": -1.072, "Жамбылская": -1.451},
        {"Год": 1985, "ЗКО": -0.313, "Атырау": -0.558, "Мангистау": -0.775, "Актюбинская": -0.206, "Карагандинская": -0.235, "Улытауская": 0.139, "ВКО": -1.008, "Абай": -0.589, "SКО": -0.79, "Акмола": -0.619, "Костанай": -0.565, "Павлодар": -0.715, "Алматиснкая": 0.126, "Жетысу": -0.281, "Туркестанская": -0.008, "Кызылординская": 0.188, "Жамбылская": -0.186},
        {"Год": 1986, "ЗКО": -0.414, "Атырау": 0.108, "Мангистау": 0.367, "Актюбинская": -0.245, "Карагандинская": -0.148, "Улытауская": -0.117, "ВКО": 0.017, "Абай": 0.229, "SКО": -0.705, "Акмола": -0.465, "Костанай": -0.565, "Павлодар": -0.437, "Алматиснкая": 0.581, "Жетысу": 0.176, "Туркестанская": 0.418, "Кызылординская": 0.117, "Жамбылская": 0.502},
        {"Год": 1987, "ЗКО": -1.784, "Атырау": -1.292, "Мангистау": -0.717, "Актюбинская": -1.063, "Карагандинская": -0.207, "Улытауская": -0.289, "ВКО": -0.386, "Абай": -0.155, "SКО": -0.463, "Акмола": -0.645, "Костанай": -0.756, "Павлодар": -0.37, "Алматиснкая": 0.311, "Жетысу": 0.604, "Туркестанская": 0.397, "Кызылординская": -0.255, "Жамбылская": 0.651},
        {"Год": 1988, "ЗКО": 0.046, "Атырау": 0.081, "Мангистау": 0.142, "Актюбинская": 0.372, "Карагандинская": 0.564, "Улытауская": 0.881, "ВКО": 0.144, "Абай": 0.232, "SКО": 0.785, "Акмола": 0.844, "Костанай": 0.638, "Павлодар": 0.643, "Алматинская": 0.059, "Жетысу": 0.184, "Туркестанская": 0.876, "Кызылординская": 0.878, "Жамбылская": 0.488},
        {"Год": 1989, "ЗКО": 1.035, "Атырау": 1.172, "Мангистау": 0.825, "Актюбинская": 0.547, "Карагандинская": 0.731, "Улытауская": 1.242, "ВКО": 1.6, "Абай": 1.307, "SКО": 1.052, "Акмола": 0.952, "Костанай": 0.99, "Павлодар": 1.12, "Алматинская": 1.054, "Жетысу": 0.417, "Туркестанская": -0.03, "Кызылординская": 0.932, "Жамбылская": 0.28},
        {"Год": 1990, "ЗКО": 0.892, "Атырау": 0.794, "Мангистау": 0.333, "Актюбинская": 0.892, "Карагандинская": 0.575, "Улытауская": 0.629, "ВКО": 1.556, "Абай": 1.32, "SКО": 1.564, "Акмола": 1.025, "Костанай": 1.302, "Павлодар": 1.382, "Алматинская": 0.656, "Жетысу": 0.97, "Туркестанская": 0.533, "Кызылординская": 0.932, "Жамбылская": 0.89},
        {"Год": 1991, "ЗКО": 1.123, "Атырау": 1.056, "Мангистау": 0.667, "Актюбинская": 1.061, "Карагандинская": 0.85, "Улытауская": 0.922, "ВКО": 1.076, "Абай": 1.085, "SКО": 1.326, "Акмола": 1.246, "Костанай": 1.27, "Павлодар": 0.983, "Алматинская": 0.476, "Жетысу": 0.671, "Туркестанская": 0.107, "Кызылординская": 0.555, "Жамбылская": 0.539},
        {"Год": 1992, "ЗКО": -0.066, "Атырау": 0.081, "Мангистау": -0.2, "Актюбинская": -0.49, "Карагандинская": -0.149, "Улытауская": -0.206, "ВКО": 0.352, "Абай": 0.48, "SКО": 0.008, "Акмола": -0.106, "Костанай": -0.315, "Павлодар": 0.352, "Алматинская": -0.471, "Жетысу": 0.464, "Туркестанская": 0.262, "Кызылординская": 0.223, "Жамбылская": 0.582},
        {"Год": 1993, "ЗКО": -1.334, "Атырау": -1.231, "Мангистау": -1.4, "Актюбинская": -1.604, "Карагандинская": -1.574, "Улытауская": -1.403, "ВКО": -0.436, "Абай": -0.846, "SКО": -0.893, "Акмола": -1.156, "Костанай": -1.325, "Павлодар": -0.622, "Алматинская": 0.134, "Жетысу": -0.668, "Туркестанская": -0.956, "Кызылординская": -1.281, "Жамбылская": -0.565},
        {"Год": 1994, "ЗКО": -1.147, "Атырау": -0.942, "Мангистау": -0.65, "Актюбинская": -1.166, "Карагандинская": 0.21, "Улытауская": 0.15, "ВКО": 0.976, "Абай": 0.701, "SКО": -0.457, "Акмола": -0.307, "Костанай": -0.459, "Павлодар": 0.453, "Алматинская": 0.594, "Жетысу": 0.217, "Туркестанская": -0.117, "Кызылординская": -0.442, "Жамбылская": 0.06},
        {"Год": 1995, "ЗКО": 2.622, "Атырау": 2.232, "Мангистау": 1.542, "Актюбинская": 1.833, "Карагандинская": 0.721, "Улытауская": 1.488, "ВКО": 1.123, "Абай": 1.085, "SКО": 1.911, "Акмола": 1.636, "Костанай": 2.096, "Павлодар": 1.778, "Алматинская": -0.488, "Жетысу": 0.817, "Туркестанская": 0.856, "Кызылординская": 1.707, "Жамбылская": 0.819},
        {"Год": 1996, "ЗКО": -0.387, "Атырау": -0.011, "Мангистау": 0.408, "Актюбинская": -0.956, "Карагандинская": -1.243, "Улытауская": -1.097, "ВКО": -0.433, "Абай": -0.457, "SКО": -1.387, "Акмола": -1.532, "Костанай": -1.425, "Павлодар": -1.255, "Алматинская": 1.356, "Жетысу": -0.426, "Туркестанская": -0.441, "Кызылординская": -0.582, "Жамбылская": -0.557},
        {"Год": 1997, "ЗКО": 0.135, "Атырау": 0.192, "Мангистау": 0.283, "Актюбинская": 0.423, "Карагандинская": 1.523, "Улытауская": 1.658, "ВКО": 2.024, "Абай": 1.946, "SКО": 1.375, "Акмола": 1.517, "Костанай": 1.314, "Павлодар": 1.897, "Алматинская": 0.513, "Жетысу": 1.504, "Туркестанская": 0.885, "Кызылординская": 1.202, "Жамбылская": 1.264},
        {"Год": 1998, "ЗКО": 0.471, "Атырау": 0.319, "Мангистау": 0.658, "Актюбинская": 0.199, "Карагандинская": 0.139, "Улытауская": 0.222, "ВКО": 0.554, "Абай": 0.361, "SКО": 0.327, "Акмола": 0.461, "Костанай": 0.894, "Павлодар": 0.247, "Алматинская": 0.976, "Жетысу": 0.458, "Туркестанская": 0.277, "Кызылординская": 0.103, "Жамбылская": 0.429},
        {"Год": 1999, "ЗКО": 1.766, "Атырау": 1.564, "Мангистау": 1.458, "Актюбинская": 0.988, "Карагандинская": 0.517, "Улытауская": 1.153, "ВКО": 1.131, "Абай": 1.109, "SКО": 0.872, "Акмола": 0.826, "Костанай": 0.842, "Павлодар": 1.138, "Алматинская": 1.013, "Жетысу": 0.901, "Туркестанская": 1.007, "Кызылординская": 1.548, "Жамбылская": 1.256},
        {"Год": 2000, "ЗКО": 1.641, "Атырау": 1.485, "Мангистау": 1.242, "Актюбинская": 0.987, "Карагандинская": 0.23, "Улытауская": 0.789, "ВКО": 0.467, "Абай": 0.623, "SКО": 0.808, "Акмола": 0.432, "Костанай": 0.984, "Павлодар": 0.348, "Алматинская": 0.997, "Жетысу": 0.758, "Туркестанская": 1.265, "Кызылординская": 1.647, "Жамбылская": 1.46},
        {"Год": 2001, "ЗКО": 1.385, "Атырау": 1.293, "Мангистау": 1.033, "Актюбинская": 1.007, "Карагандинская": 0.646, "Улытауская": 1.306, "ВКО": 0.477, "Абай": 0.664, "SКО": 0.61, "Акмола": 1.13, "Костанай": 1.094, "Павлодар": 1.075, "Алматинская": 1.522, "Жетысу": 0.773, "Туркестанская": 1.186, "Кызылординская": 1.21, "Жамбылская": 0.985},
        {"Год": 2002, "ЗКО": 1.069, "Атырау": 0.917, "Мангистау": 0.65, "Актюбинская": 1.012, "Карагандинская": 1.764, "Улытауская": 2.011, "ВКО": 1.998, "Абай": 2.083, "SКО": 1.329, "Акмола": 1.814, "Костанай": 1.525, "Павлодар": 2.278, "Алматинская": 0.137, "Жетысу": 1.71, "Туркестанская": 1.021, "Кызылординская": 1.617, "Жамбылская": 1.52},
        {"Год": 2003, "ЗКО": 0.472, "Атырау": 0.478, "Мангистау": -0.05, "Актюбинская": 0.093, "Карагандинская": -0.044, "Улытауская": 0.208, "ВКО": 0.389, "Абай": 0.148, "SКО": 0.752, "Акмола": 0.443, "Костанай": 0.624, "Павлодар": 0.857, "Алматинская": 1.332, "Жетысу": -0.002, "Туркестанская": 0.477, "Кызылординская": 0.623, "Жамбылская": 0.511},
        {"Год": 2004, "ЗКО": 1.978, "Атырау": 1.941, "Мангистау": 2.042, "Актюбинская": 1.915, "Карагандинская": 1.105, "Улытауская": 1.606, "ВКО": 1.019, "Абай": 1.165, "SКО": 1.451, "Акмола": 1.553, "Костанай": 1.857, "Павлодар": 1.262, "Алматинская": 1.02, "Жетысу": 1.278, "Туркестанская": 1.597, "Кызылординская": 2.303, "Жамбылская": 1.531},
        {"Год": 2005, "ЗКО": 1.416, "Атырау": 1.845, "Мангистау": 1.233, "Актюбинская": 1.014, "Карагандинская": 1.245, "Улытауская": 1.489, "ВКО": 0.519, "Абай": 0.978, "SКО": 0.979, "Акмола": 0.967, "Костанай": 1.012, "Павлодар": 0.948, "Алматинская": 1.481, "Жетысу": 0.892, "Туркестанская": 1.166, "Кызылординская": 1.967, "Жамбылская": 0.987},
        {"Год": 2006, "ЗКО": 0.925, "Атырау": 0.603, "Мангистау": 0.842, "Актюбинская": 1.268, "Карагандинская": 1.311, "Улытауская": 1.442, "ВКО": 1.322, "Абай": 1.495, "SКО": 0.61, "Акмола": 1.043, "Костанай": 1.331, "Павлодар": 0.803, "Алматинская": 1.478, "Жетысу": 1.546, "Туркестанская": 0.958, "Кызылординская": 1.192, "Жамбылская": 1.383},
        {"Год": 2007, "ЗКО": 1.661, "Атырау": 1.75, "Мангистау": 1.767, "Актюбинская": 0.686, "Карагандинская": 1.329, "Улытауская": 1.389, "ВКО": 1.834, "Абай": 2.114, "SКО": 1.482, "Акмола": 1.394, "Костанай": 1.064, "Павлодар": 1.948, "Алматинская": 1.206, "Жетысу": 1.567, "Туркестанская": 1.062, "Кызылординская": 1.607, "Жамбылская": 1.565},
        {"Год": 2008, "ЗКО": 1.559, "Атырау": 0.558, "Мангистау": 0.458, "Актюбинская": 1.549, "Карагандинская": 1.234, "Улытауская": 1.608, "ВКО": 1.381, "Абай": 1.476, "SКО": 1.777, "Акмола": 1.454, "Костанай": 1.805, "Павлодар": 1.623, "Алматинская": 0.764, "Жетысу": 1.43, "Туркестанская": 0.732, "Кызылординская": 1.142, "Жамбылская": 1.155},
        {"Год": 2009, "ЗКО": 1.336, "Атырау": 0.742, "Мангистау": 0.892, "Актюбинская": 0.768, "Карагандинская": 0.292, "Улытауская": 0.819, "ВКО": 0.097, "Абай": 0.228, "SКО": 0.418, "Акмола": 0.325, "Костанай": 0.619, "Павлодар": -0.187, "Алматинская": 0.879, "Жетысу": 0.663, "Туркестанская": 0.919, "Кызылординская": 1.257, "Жамбылская": 1.004},
        {"Год": 2010, "ЗКО": 2.258, "Атырау": 2.175, "Мангистау": 2.008, "Актюбинская": 2.034, "Карагандинская": 0.088, "Улытауская": 1.172, "ВКО": -0.793, "Абай": -0.809, "SКО": 0.296, "Акмола": 0.536, "Костанай": 1.196, "Павлодар": -0.803, "Алматинская": 0.386, "Жетысу": 0.584, "Туркестанская": 1.691, "Кызылординская": 1.898, "Жамбылская": 1.021},
        {"Год": 2011, "ЗКО": -0.223, "Атырау": -0.058, "Мангистау": 0.4, "Актюбинская": -0.44, "Карагандинская": -0.096, "Улытауская": -0.053, "ВКО": 0.118, "Абай": 0.011, "SКО": -0.308, "Акмола": -0.222, "Костанай": -0.544, "Павлодар": 0.172, "Алматинская": 0.094, "Жетысу": -0.007, "Туркестанская": 0.404, "Кызылординская": 0.272, "Жамбылская": 0.185},
        {"Год": 2012, "ЗКО": 1.756, "Атырау": 1.019, "Мангистау": 0.867, "Актюбинская": 1.746, "Карагандинская": -0.452, "Улытауская": 0.164, "ВКО": -0.465, "Абай": -0.533, "SКО": 0.463, "Акмола": 0.471, "Костанай": 1.022, "Павлодар": -0.182, "Алматинская": 1.707, "Жетысу": -0.376, "Туркестанская": 0.309, "Кызылординская": 0.712, "Жамбылская": 0.032},
        {"Год": 2013, "ЗКО": 2.235, "Атырау": 1.944, "Мангистау": 1.658, "Актюбинская": 2.208, "Карагандинская": 1.895, "Улытауская": 2.422, "ВКО": 1.997, "Абай": 1.91, "SКО": 1.514, "Акмола": 1.528, "Костанай": 1.796, "Павлодар": 1.523, "Алматинская": 0.031, "Жетысу": 1.684, "Туркестанская": 1.669, "Кызылординская": 2.55, "Жамбылская": 2.033},
        {"Год": 2014, "ЗКО": 0.434, "Атырау": 0.706, "Мангистау": 1.108, "Актюбинская": 0.274, "Карагандинская": -0.526, "Улытауская": -0.044, "ВКО": 0.587, "Абай": 0.25, "SКО": 0.086, "Акмола": -0.011, "Костанай": 0.499, "Павлодар": 0.363, "Алматинская": 1.863, "Жетысу": 0.131, "Туркестанская": -0.124, "Кызылординская": -0.298, "Жамбылская": -0.221},
        {"Год": 2015, "ЗКО": 1.782, "Атырау": 1.447, "Мангистау": 1.425, "Актюбинская": 1.206, "Карагандинская": 1.408, "Улытауская": 1.928, "ВКО": 2.091, "Абай": 1.892, "SКО": 1.042, "Акмола": 1.249, "Костанай": 1.23, "Павлодар": 1.745, "Алматинская": 1.769, "Жетысу": 1.985, "Туркестанская": 1.6, "Кызылординская": 2.143, "Жамбылская": 1.932},
        {"Год": 2016, "ЗКО": 1.808, "Атырау": 1.806, "Мангистау": 1.542, "Актюбинская": 1.757, "Карагандинская": 0.929, "Улытауская": 1.614, "ВКО": 1.246, "Абай": 1.033, "SКО": 0.933, "Акмола": 1.076, "Костанай": 1.255, "Павлодар": 1.093, "Алматинская": 1.316, "Жетысу": 1.503, "Туркестанская": 1.877, "Кызылординская": 2.5, "Жамбылская": 1.849},
        {"Год": 2017, "ЗКО": 1.375, "Атырау": 1.617, "Мангистау": 1.758, "Актюбинская": 1.163, "Карагандинская": 1.094, "Улытауская": 1.267, "ВКО": 1.538, "Абай": 1.568, "SКО": 1.169, "Акмола": 1.475, "Костанай": 1.103, "Павлодар": 1.422, "Алматинская": 0.356, "Жетысу": 1.147, "Туркестанская": 1.079, "Кызылординская": 1.465, "Жамбылская": 1.088},
        {"Год": 2018, "ЗКО": 0.62, "Атырау": 0.897, "Мангистау": 1.542, "Актюбинская": 0.239, "Карагандинская": -0.635, "Улытауская": -0.553, "ВКО": 0.104, "Абай": -0.081, "SКО": -0.693, "Акмола": -0.726, "Костанай": -0.3, "Павлодар": -0.788, "Алматинская": 1.682, "Жетысу": 0.16, "Туркестанская": 0.913, "Кызылординская": 0.37, "Жамбылская": 0.196},
        {"Год": 2019, "ЗКО": 1.599, "Атырау": 1.811, "Мангистау": 1.667, "Актюбинская": 1.454, "Карагандинская": 0.957, "Улытауская": 1.172, "ВКО": 1.695, "Абай": 1.407, "SКО": 1.114, "Акмола": 1.13, "Костанай": 1.25, "Павлодар": 1.107, "Алматинская": 1.147, "Жетысу": 1.548, "Туркестанская": 1.909, "Кызылординская": 2.225, "Жамбылская": 2.012},
        {"Год": 2020, "ЗКО": 2.546, "Атырау": 2.275, "Мангистау": 1.817, "Актюбинская": 2.228, "Карагандинская": 1.289, "Улытауская": 1.306, "ВКО": 2.213, "Абай": 1.893, "SКО": 3.163, "Акмола": 2.6, "Костанай": 2.547, "Павлодар": 2.968, "Алматинская": 1.592, "Жетысу": 1.229, "Туркестанская": 0.754, "Кызылординская": 1.758, "Жамбылская": 0.961},
        {"Год": 2021, "ЗКО": 2.502, "Атырау": 2.627, "Мангистау": 2.039, "Актюбинская": 2.099, "Карагандинская": 1.132, "Улытауская": 1.48, "ВКО": 1.211, "Абай": 1.247, "SКО": 0.954, "Акмола": 1.02, "Костанай": 1.628, "Павлодар": 0.942, "Алматинская": 2.031, "Жетысу": 1.385, "Туркестанская": 1.893, "Кызылординская": 2.28, "Жамбылская": 1.585},
        {"Год": 2022, "ЗКО": 2.118, "Атырау": 2.325, "Мангистау": 2.208, "Актюбинская": 1.599, "Карагандинская": 1.457, "Улытауская": 2.075, "ВКО": 1.823, "Абай": 1.78, "SКО": 1.349, "Акмола": 1.258, "Костанай": 1.254, "Павлодар": 1.202, "Алматинская": 2.128, "Жетысу": 1.914, "Туркестанская": 2.047, "Кызылординская": 2.415, "Жамбылская": 2.329},
        {"Год": 2023, "ЗКО": 2.935, "Атырау": 3.019, "Мангистау": 2.475, "Актюбинская": 2.905, "Карагандинская": 2.504, "Улытауская": 3.108, "ВКО": 2.496, "Абай": 2.417, "SКО": 2.619, "Акмола": 2.651, "Костанай": 2.608, "Павлодар": 2.635, "Алматинская": 1.726, "Жетысу": 2.114, "Туркестанская": 2.352, "Кызылординская": 3.46, "Жамбылская": 2.258},
        {"Год": 2024, "ЗКО": 2.092, "Атырау": 2.353, "Мангистау": 2.256, "Актюбинская": 1.667, "Карагандинская": 1.396, "Улытауская": 1.911, "ВКО": 2.067, "Абай": 2.032, "SКО": 1.265, "Акмола": 1.225, "Костанай": 1.446, "Павлодар": 1.634, "Алматинская": 2.726, "Жетысу": 1.678, "Туркестанская": 1.535, "Кызылординская": 2.301, "Жамбылская": 1.643},
        {"Год": 2025, "ЗКО": 3.511, "Атырау": 2.906, "Мангистау": 2.1, "Актюбинская": 3.226, "Карагандинская": 2.744, "Улытауская": 3.653, "ВКО": 2.197, "Абай": 2.543, "SКО": 3.276, "Акмола": 3.309, "Костанай": 3.515, "Павлодар": 3.025, "Алматинская": None, "Жетысу": 2.494, "Туркестанская": 2.926, "Кызылординская": 3.537, "Жамбылская": 2.977}
    ]

    df_anom = pd.DataFrame(data_list)

    # 2. Маппинг (соответствие) названий
    column_mapping = {
        "Западно-Казахстанская область": "ЗКО",
        "Атырауская область": "Атырау",
        "Мангистауская область": "Мангистау",
        "Актюбинская область": "Актюбинская",
        "Карагандинская область": "Карагандинская",
        "Улытауская область": "Улытауская",
        "Восточно-Казахстанская область": "ВКО",
        "Область Абай": "Абай",
        "Северо-Казахстанская область": "СКО",
        "Акмолинская область": "Акмола",
        "Костанайская область": "Костанай",
        "Павлодарская область": "Павлодар",
        "Алматинская область": "Алматинская",
        "Область Жетысу": "Жетысу",
        "Туркестанская область": "Туркестанская",
        "Кызылординская область": "Кызылординская",
        "Жамбылская область": "Жамбылская"
    }


    # 1. Создаем переменную (убедитесь, что имя совпадает!)
    selected_name = st.selectbox("Выберите область Казахстана:", list(ALL_REGIONS_DATABASE.keys()))

    # 2. Извлекаем данные (эта строка тоже должна использовать selected_name)
    reg = ALL_REGIONS_DATABASE[selected_name]
    
    # --- 4. КАРТОЧКИ ПОКАЗАТЕЛЕЙ (ДИНАМИЧЕСКИЕ) ---
    c1, c2, c3, c4 = st.columns(4)

    # 1. Территория
    c1.metric(
        label="Территория", 
        value=reg['area'], 
        delta=f"{reg['area_perc']} от РК", 
        delta_color="off"
    )

    # 2. Температура (с принудительным преобразованием в float для вычислений)
    temp_val = float(reg['temp_2025'])
    norm_val = float(reg['norm_temp'])
    diff = temp_val - norm_val

    c2.metric(
        label="Температура 2025", 
        value=f"{temp_val} °С", 
        delta=f"{diff:+.2f} °С к норме", # Автоматически добавит '+' или '-'
        delta_color="inverse" # Красный цвет при потеплении (так как это риск)
    )

    # 3. Аномалия
    c3.metric(
        label="Аномалия", 
        value=f"+{reg['anom_2025']} °С", 
        delta="Ранг №1 в истории",
        delta_color="normal"
    )

    # 4. Осадки
    c4.metric(
        label="Осадки 2025", 
        value=f"{reg['precip_2025']} мм", 
        delta=f"{reg['prec_norm']} от нормы",
        delta_color="off"
    )

    # --- 3. КЛИМАТИЧЕСКИЕ ЗОНЫ (ДИНАМИЧЕСКИЕ) ---
    st.markdown("### 🗺️ Климатические зоны области")

    # Берем список зон для выбранной области
    region_zones = reg.get("zones", [])

    if region_zones:
        # Создаем колонки динамически по количеству зон
        cols = st.columns(len(region_zones))
        
        for idx, zone in enumerate(region_zones):
            with cols[idx]:
                st.markdown(f"""
                    <div style="background: white; border: 1px solid #e6e9ef; border-radius: 12px; padding: 15px; height: 100%;">
                        <h4 style="color:{zone['color']}; margin-top:0;">{zone['title']}</h4>
                        <p style="font-size:0.9rem; color:#555;">{zone['desc']}</p>
                        <div style="background:{zone['bg']}; padding:8px; border-radius:6px; font-size:0.85rem;">
                            <b>Осадки:</b> {zone['precip']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Информация о климатических зонах для данного региона уточняется.")
    
    
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    import streamlit as st

    def render_climate_charts(df, column_name, title, subtitle, colorscale, bar_colors, unit):
        st.subheader(title)
        st.caption(subtitle)
        
       
        # 2. Основной график (Столбцы + Линия тренда)
        fig_chart = go.Figure()
        
        # Определяем цвета столбцов: красный если > 0, синий если < 0
        colors = [bar_colors[0] if x > 0 else bar_colors[1] for x in df[column_name]]
        
        # Добавляем столбцы аномалий
        fig_chart.add_trace(go.Bar(
            x=df['Год'], 
            y=df[column_name], 
            marker_color=colors, 
            opacity=0.6, 
            name='Ежегодная аномалия'
        ))
        
        # Считаем скользящее среднее (Тренд)
        sma_col = df[column_name].rolling(window=10, min_periods=1, center=True).mean()
        fig_chart.add_trace(go.Scatter(
            x=df['Год'], 
            y=sma_col, 
            mode='lines', 
            line=dict(color='#222', width=2.5), 
            name='10-летнее среднее'
        ))

        fig_chart.update_layout(
            height=320, 
            margin=dict(l=0, r=0, t=10, b=10),
            showlegend=True, 
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#f0f0f0', dtick=20),
            yaxis=dict(title=f"Аномалия ({unit})", showgrid=True, gridcolor='#f0f0f0', zeroline=True, zerolinecolor='#ccc')
        )
        st.plotly_chart(fig_chart, use_container_width=True)

    # --- ПРИМЕР ВЫЗОВА В КОЛОНКАХ ---

    # Допустим, ты уже создал DataFrame из словаря, как мы обсуждали ранее:
    # df_anom = pd.DataFrame(data_anom) 

    col_l, col_r = st.columns(2)

    with col_l:
        render_climate_charts(
            df_anom, "СКО", 
            "Температура воздуха", 
            "Графическое представление аномалий температуры (отклонение от нормы).",
            'RdBu_r', ['#d32f2f', '#1f77b4'], "°C"
        )

    # Вместо "Осадки_СКО" используй точное имя из твоего словаря
    with col_r:
        render_climate_charts(
            df_anom, "СКО", 
            "Осадки", 
            "Графическое представление аномалийосадков (отклонение от нормы).",
            'BrBG', ['#2e7d32', '#8d6e63'], "мм"
        )


    # --- ОТДЕЛЬНЫЙ БЛОК ТРЕНДОВ (ВНЕ КОЛОНОК) ---
    st.markdown("### 📊 Климатические тренды")

    # Стили для горизонтального отображения трендов
    st.markdown("""
        <style>
        .trends-container {
            display: flex;
            justify-content: flex-start;
            gap: 30px;
            margin: 15px 0;
        }
        .trend-card {
            flex: 0 1 auto;
            padding: 15px 25px;
            border-radius: 10px;
            background-color: #fcfcfc;
            border: 1px solid #eee;
            min-width: 200px;
        }
        .trend-label {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 5px;
        }
        .trend-value {
            font-size: 1.8rem;
            font-weight: 800;
            line-height: 1.1;
        }
        .v-green { color: #28a745; }
        .v-orange { color: #f39c12; }
        .trend-note {
            font-size: 0.8rem;
            color: #888;
            margin-top: 8px;
            font-style: italic;
        }
        </style>
        
        <div class="trends-container">
            <div class="trend-card" style="border-left: 5px solid #28a745;">
                <div class="trend-label">тренд</div>
                <div class="trend-value v-green">📈 +0,36 °С</div>
                <div class="trend-note">прирост на каждые 10 лет</div>
            </div>
            <div class="trend-card" style="border-left: 5px solid #f39c12;">
                <div class="trend-label">тренд</div>
                <div class="trend-value v-orange">📈 +6,1 мм</div>
                <div class="trend-note">прирост на каждые 10 лет</div>
            </div>
            <div style="flex: 1; display: flex; align-items: center; padding-left: 10px;">
                <p style="color: #444; font-size: 0.95rem; border-left: 2px dashed #ccc; padding-left: 20px;">
                    💡 <b>Анализ:</b> Общий рост увлажнения происходит за счет <b>весеннего периода</b>, в то время как летние месяцы демонстрируют опасную тенденцию к засушливости.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    
     # --- 4. ДЕТАЛЬНАЯ СТАТИСТИКА (В ОДНУ СТРОКУ) ---
    st.markdown("### 📉 Статистический анализ")

    # Создаем две основные колонки для Температуры и Осадков
    col_main_temp, col_main_precip = st.columns(2, gap="large")

    # --- ЛЕВАЯ КОЛОНКА: ТЕМПЕРАТУРА ---
    with col_main_temp:
        st.subheader("🌡️ Температурный режим")
        
        # Внутреннее разделение для таблицы и рейтинга
        t_col1, t_col2 = st.columns([1.6, 1])
        
        with t_col1:
            st.markdown("**Сезонные температуры (СКО)**")
            temp_data = {
                "Период": ["Норма", "2025"],
                "Зима": ["-15.5", "-9.5"],
                "Весна": ["2.5", "7.2"],
                "Лето": ["18.2", "18.7"],
                "Осень": ["2.1", "4.8"],
                "Год": ["1.8", "5.1"]
            }
            st.table(pd.DataFrame(temp_data))
            st.caption("💡 Макс: +24°С (1989), Мин: -29.8°С (1969)")

        with t_col2:
            st.markdown("**🏆 Топ лет**")
            sko_ranks = [
                {"y": 2025, "v": 5.09, "c": "#990000"},
                {"y": 2020, "v": 4.98, "c": "#b30000"},
                {"y": 2023, "v": 4.43, "c": "#d32f2f"},
                {"y": 1983, "v": 4.01, "c": "#e57373"},
                {"y": 1995, "v": 3.73, "c": "#ef9a9a"}
            ]
            rows_html = "".join([f"""
                <div style="display:flex; align-items:center; margin-bottom:8px; height:20px;">
                    <div style="width:35px; font-size:10px; font-weight:bold;">{item['y']}</div>
                    <div style="flex-grow:1; background:#eee; height:12px; border-radius:2px;">
                        <div style="width:{(item['v']/5.09)*100}%; background:{item['c']}; height:100%; border-radius:2px;"></div>
                    </div>
                    <div style="width:35px; text-align:right; font-size:10px; font-weight:bold; margin-left:5px;">{item['v']}°</div>
                </div>""" for item in sko_ranks])
            components.html(f'<div style="font-family:sans-serif; padding-top:10px;">{rows_html}</div>', height=160)

    # --- ПРАВАЯ КОЛОНКА: ОСАДКИ ---
    with col_main_precip:
        st.subheader("💧 Режим увлажнения")
        
        p_col1, p_col2 = st.columns([1.6, 1])
        
        with p_col1:
            st.markdown("**Сезонные осадки, мм (СКО)**")
            prec_data = {
                "Период": ["Норма", "2025"],
                "Зима": ["47.3", "58.4"],
                "Весна": ["65.6", "116.8"],
                "Лето": ["152.6", "175.1"],
                "Осень": ["87.1", "88.7"],
                "Год": ["352.6", "439.9"]
            }
            st.table(pd.DataFrame(prec_data))

        with p_col2:
            st.markdown("**🏆 Топ лет**")
            sko_ranks = [
                {"y": 2025, "v": 5.09, "c": "#990000"},
                {"y": 2020, "v": 4.98, "c": "#b30000"},
                {"y": 2023, "v": 4.43, "c": "#d32f2f"},
                {"y": 1983, "v": 4.01, "c": "#e57373"},
                {"y": 1995, "v": 3.73, "c": "#ef9a9a"}
            ]
            rows_html = "".join([f"""
                <div style="display:flex; align-items:center; margin-bottom:8px; height:20px;">
                    <div style="width:35px; font-size:10px; font-weight:bold;">{item['y']}</div>
                    <div style="flex-grow:1; background:#eee; height:12px; border-radius:2px;">
                        <div style="width:{(item['v']/5.09)*100}%; background:{item['c']}; height:100%; border-radius:2px;"></div>
                    </div>
                    <div style="width:35px; text-align:right; font-size:10px; font-weight:bold; margin-left:5px;">{item['v']}°</div>
                </div>""" for item in sko_ranks])
            components.html(f'<div style="font-family:sans-serif; padding-top:10px;">{rows_html}</div>', height=160)


    st.markdown("### 🚨 Основные климатические риски")

    def risk_box(title, text, level, color):
        # level — число от 0 до 100
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

    risk_box("🔥 Экстремальные температуры", "Рост 0.36 °С за 10 лет. 2025 год — рекорд (+5.09 °С).", 95, "#d32f2f")
    risk_box("🌾 Засухи и дефицит влаги", "Снижение осадков в июне и октябре. Угроза урожаю.", 70, "#f57c00")
    risk_box("🌊 Весенние паводки", "Рост осадков весной (+6.1 мм/10 лет) провоцирует наводнения.", 45, "#1976d2")

    # --- 6. ОБЩИЙ ВЫВОД ---
    st.info("💡 **Общие выводы:** Интенсивное потепление в СКО опережает среднемировые темпы. Несмотря на рост годовых осадков, их неравномерное распределение (дефицит летом при избытке весной) требует адаптации агротехнологий.")





   

with tabs[7]:
    st.title("Экология городов")

    import streamlit as st
    import pandas as pd
    import plotly.express as px

    def show_water_quality_dashboard():
        st.title("💧 Мониторинг качества поверхностных вод")
        st.markdown("""
        **Регион:** Восточно-Казахстанская и Абайская области. 
        *Наблюдение ведется на 19 водных объектах (53 створа) по 48 показателям.*
        """)

        # --- СТАТИСТИКА В ЦИФРАХ ---
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        col_stat1.metric("Объектов мониторинга", "19", "16 рек, 2 оз, 2 вдхр")
        col_stat2.metric("Показателей качества", "48", "Физ-хим + Тяжелые металлы")
        col_stat3.metric("Лидер чистоты (1 класс)", "р. Арасан", "Стабильно 2020-2025")

        # --- ДАННЫЕ ДЛЯ СРАВНЕНИЯ (2025 vs 2024) ---
        st.subheader("📊 Распределение водных объектов по классам качества")
        
        # Подготовка данных для графика
        quality_data = {
            "Класс": ["1 класс", "2 класс", "3 класс", "4 класс", "5 класс", ">5 класса"],
            "2025 год (объектов)": [1, 0, 5, 3, 1, 8],
            "2024 год (объектов)": [3, 4, 5, 1, 2, 3]
        }
        df_q = pd.DataFrame(quality_data)

        fig_compare = px.bar(df_q, x="Класс", y=["2025 год (объектов)", "2024 год (объектов)"],
                             barmode="group", color_discrete_sequence=["#004A99", "#A5D6A7"],
                             title="Динамика изменения классов качества (Кол-во объектов)")
        st.plotly_chart(fig_compare, use_container_width=True)

        # --- СЛУЧАИ ВЫСОКОГО ЗАГРЯЗНЕНИЯ (ВЗ) ---
        st.error("⚠️ Случаи высокого загрязнения (ВЗ) за 2025 год")
        col_vz1, col_vz2 = st.columns(2)
        
        with col_vz1:
            st.markdown("""
            * **р. Ульби:** 25 случаев (Цинк, Железо)
            * **р. Глубочанка:** 6 случаев (Цинк)
            * **р. Тихая:** 8 случаев (Цинк)
            """)
        with col_vz2:
            st.markdown("""
            * **р. Красноярка:** 8 случаев (Цинк)
            * **р. Ертис:** 6 случаев (Цинк)
            * **р. Брекса:** 2 случая (Железо)
            """)

        # --- ИНТЕРАКТИВНАЯ ТАБЛИЦА ПО КЛАССАМ ---
        st.subheader("🔍 Детальная классификация (2025 год)")
        
        tab_2025, tab_trends = st.tabs(["📋 Реестр объектов 2025", "📉 Тренды 2021-2024"])

        with tab_2025:
            data_2025 = {
                "Класс": ["1 (Очень хорошее)", "3 (Умеренное)", "4 (Загрязненное)", "5 (Очень загрязн.)", "6 (Высоко загрязн.)"],
                "Пригодность": [
                    "Все виды водопользования",
                    "Нежелательно для лососевых рыб",
                    "Только орошение и пром. нужды",
                    "Только пром. нужды после отстаивания",
                    "Только гидроэнергетика и транспорт"
                ],
                "Объекты": [
                    "р. Арасан",
                    "р. Буктырма, р. Секисовка, р. Маховка, вдхр. Буктырма",
                    "р. Кара Ертис, р. Ертис, р. Оба",
                    "р. Брекса (Цинк)",
                    "р. Тихая, р. Ульби, р. Глубочанка, р. Красноярка, р. Аягоз, р. Уржар, р. Емель"
                ]
            }
            st.table(pd.DataFrame(data_2025))

        with tab_trends:
            st.write("**Изменения качества в сравнении с прошлыми периодами:**")
            col_up, col_down = st.columns(2)
            with col_up:
                st.success("✅ Улучшение: р. Аягоз (с 5 до 3 класса)")
            with col_down:
                st.warning("❌ Ухудшение: р. Кара Ертис (со 2 до >5), р. Уржар (с 1 до >5), р. Емель, р. Маховка")

        # --- СПРАВОЧНАЯ ИНФОРМАЦИЯ ---
        with st.expander("ℹ️ Какие показатели определяются в пробах?"):
            st.write("""
            В каждой пробе анализируется **48 показателей**, включая:
            * **Биогенные:** Азот, фосфор, растворенный кислород.
            * **Тяжелые металлы:** Цинк, кадмий, медь, марганец, свинец.
            * **Органика:** Нефтепродукты, фенолы, БПК5, ХПК.
            * **Пестициды:** ГХЦГ, ДДТ.
            """)

    if __name__ == "__main__":
        show_water_quality_dashboard()
        


with tabs[8]:
    st.title("Международное сотрудничество")

    import streamlit as st

    # --- НАСТРОЙКА ВКЛАДКИ МЕЖДУНАРОДНОГО СОТРУДНИЧЕСТВА ---
    st.header("🌐 Международное сотрудничество")

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

    # Дополнительный блок визуализации (Карта или схема потоков данных)
    st.markdown("---")
    st.write("### 🔗 Роль Казахстана в глобальной сети WIGOS")
    st.caption("""
    Субрегиональный центр РЦИ в Казахстане выступает связующим звеном между региональными ассоциациями RAVI (Европа) и RAII (Азия), 
    обеспечивая интеграцию национальных систем наблюдений в единую глобальную сеть.
    """)

    # Интерактивная метрика (если нужно подчеркнуть масштаб)
    st.button("📄 Запросить аналитический отчет РЦИ")

    
st.markdown('<div style="text-align: center; margin-top: 40px; color: #94A3B8;">РГП «Казгидромет» | 2026</div>', unsafe_allow_html=True)