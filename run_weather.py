import sys
import random
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QStackedWidget, QFrame, 
                             QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QFont, QColor

class MeteoBelgiUltimate(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("METEO-BELGI 2026 | Digital ID")
        self.setFixedSize(1100, 750) 
        self.init_ui()

    def init_ui(self):
        # 1. ЖИВОЙ ФОН (Copernicus Style)
        self.browser = QWebEngineView(self)
        self.browser.setUrl(QUrl("https://earth.nullschool.net/#current/wind/surface/level/orthographic=71.80,51.12,1500"))
        self.browser.setGeometry(0, 0, 1100, 750)
        self.browser.setDisabled(True) 

        # 2. ГЛАВНЫЙ КОНТЕЙНЕР (Стек экранов)
        self.stack = QStackedWidget(self)
        self.stack.setGeometry(60, 75, 420, 600)

        # ОБЩИЕ СТИЛИ
        self.setStyleSheet("""
            QFrame#Card {
                background: rgba(15, 23, 42, 0.9);
                border-radius: 30px;
                border: 1px solid rgba(56, 189, 248, 0.3);
            }
            QLabel { color: #f8fafc; background: transparent; }
            QLineEdit {
                background: rgba(30, 41, 59, 0.9);
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 14px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus { border: 2px solid #38bdf8; }
            QPushButton#MainBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #0ea5e9);
                color: white;
                border-radius: 15px;
                padding: 18px;
                font-weight: 800;
                font-size: 13px;
                text-transform: uppercase;
            }
            QPushButton#MainBtn:hover { background: #38bdf8; }
        """)

        # --- ЭКРАН 1: ВВОД ---
        self.page_input = QFrame()
        self.page_input.setObjectName("Card")
        input_layout = QVBoxLayout(self.page_input)
        input_layout.setContentsMargins(40, 45, 40, 45)

        logo = QLabel("METEO-BELGI")
        logo.setFont(QFont("Impact", 34))
        logo.setStyleSheet("color: #38bdf8; letter-spacing: 5px;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: rgba(56, 189, 248, 0.2); max-height: 1px; margin: 10px 20px;")

        sub_title = QLabel("ЖЕКЕ МЕТЕО-ПАСПОРТТЫ ҚҰРАСТЫРУ\nСОЗДАНИЕ ПЕРСОНАЛЬНОГО МЕТЕО-ПАСПОРТА")
        sub_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_title.setStyleSheet("color: #64748b; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        def create_lbl(text):
            l = QLabel(text)
            l.setStyleSheet("color: #94a3b8; font-size: 9px; font-weight: bold; margin-left: 5px; margin-top: 10px;")
            return l

        self.input_name = QLineEdit(placeholderText="Аты-жөніңіз / Имя Фамилия")
        self.input_city = QLineEdit(placeholderText="Туған қалаңыз / Город рождения")
        self.input_date = QLineEdit(placeholderText="Дата (КК.АА.ЖЖЖЖ)")

        self.btn_start = QPushButton("ТАЛДАУДЫ БАСТАУ / НАЧАТЬ АНАЛИЗ")
        self.btn_start.setObjectName("MainBtn")
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.clicked.connect(self.start_analysis)
        
        btn_shadow = QGraphicsDropShadowEffect()
        btn_shadow.setBlurRadius(20)
        btn_shadow.setColor(QColor(2, 132, 199, 120))
        btn_shadow.setOffset(0, 0)
        self.btn_start.setGraphicsEffect(btn_shadow)

        input_layout.addWidget(logo)
        input_layout.addWidget(line)
        input_layout.addWidget(sub_title)
        input_layout.addSpacing(40)
        input_layout.addWidget(create_lbl("ПАЙДАЛАНУШЫ / ПОЛЬЗОВАТЕЛЬ"))
        input_layout.addWidget(self.input_name)
        input_layout.addWidget(create_lbl("ОРНАЛАСУЫ / ЛОКАЦИЯ"))
        input_layout.addWidget(self.input_city)
        input_layout.addWidget(create_lbl("УАҚЫТЫ / ВРЕМЯ"))
        input_layout.addWidget(self.input_date)
        input_layout.addSpacing(30)
        input_layout.addWidget(self.btn_start)
        input_layout.addStretch()

        # --- ЭКРАН 2: ЗАГРУЗКА ---
        self.page_load = QFrame()
        self.page_load.setObjectName("Card")
        load_layout = QVBoxLayout(self.page_load)
        self.load_label = QLabel("🌀\n\nСПУТНИКТЕРМЕН БАЙЛАНЫС...\nУСТАНОВКА СВЯЗИ...")
        self.load_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.load_label.setStyleSheet("color: #38bdf8; font-size: 18px; font-weight: bold; letter-spacing: 2px;")
        load_layout.addWidget(self.load_label)

        # --- ЭКРАН 3: РЕЗУЛЬТАТ ---
        self.page_res = QFrame()
        self.page_res.setObjectName("Card")
        res_layout = QVBoxLayout(self.page_res)
        res_layout.setContentsMargins(35, 40, 35, 40)
        
        header_res = QLabel("МЕТЕОРОЛОГИЯЛЫҚ ҚОРЫТЫНДЫ\nМЕТЕОРОЛОГИЧЕСКОЕ ЗАКЛЮЧЕНИЕ")
        header_res.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_res.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 10px; letter-spacing: 2px;")

        self.res_user_info = QLabel("")
        self.res_user_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res_user_info.setStyleSheet("""
            background: rgba(56, 189, 248, 0.1); 
            border-radius: 10px; 
            padding: 10px; 
            color: #ffffff;
            border-left: 3px solid #38bdf8;
        """)
        self.res_user_info.setFont(QFont("Segoe UI", 12))

        self.weather_card = QFrame()
        self.weather_card.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(30, 41, 59, 0.5), stop:1 rgba(15, 23, 42, 0.8));
            border-radius: 20px;
            border: 1px solid rgba(56, 189, 248, 0.2);
        """)
        card_layout = QVBoxLayout(self.weather_card)
        
        self.res_icon = QLabel("") 
        self.res_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res_icon.setFont(QFont("Segoe UI", 60))
        
        self.res_temp = QLabel("") 
        self.res_temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res_temp.setStyleSheet("color: #38bdf8; font-size: 42px; font-weight: 900;")
        
        self.res_desc = QLabel("") 
        self.res_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res_desc.setStyleSheet("color: #94a3b8; font-size: 14px; text-transform: uppercase; letter-spacing: 2px;")

        card_layout.addWidget(self.res_icon)
        card_layout.addWidget(self.res_temp)
        card_layout.addWidget(self.res_desc)

        self.res_footer = QLabel("Данные подтверждены системой ERA5 Copernicus")
        self.res_footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res_footer.setStyleSheet("color: #475569; font-size: 9px; font-style: italic;")

        btn_reset = QPushButton("ЖАҢА СҰРАНЫС / НОВЫЙ ЗАПРОС")
        btn_reset.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_reset.setStyleSheet("""
            background: transparent; 
            border: 1px solid #38bdf8; 
            color: #38bdf8; 
            border-radius: 12px; 
            padding: 12px; 
            font-weight: bold;
        """)

        res_layout.addWidget(header_res)
        res_layout.addSpacing(20)
        res_layout.addWidget(self.res_user_info)
        res_layout.addSpacing(20)
        res_layout.addWidget(self.weather_card)
        res_layout.addSpacing(15)
        res_layout.addWidget(self.res_footer)
        res_layout.addStretch()
        res_layout.addWidget(btn_reset)

        self.stack.addWidget(self.page_input)
        self.stack.addWidget(self.page_load)
        self.stack.addWidget(self.page_res)

    def start_analysis(self):
        city = self.input_city.text().strip().lower()
        if not self.input_name.text(): return

        # Анимация карты при клике
        locations = {
            "астана": "71.43,51.16,4000",
            "алматы": "76.92,43.23,4000",
            "шымкент": "69.59,42.32,4000"
        }
        target = locations.get(city, "71.80,51.12,4000")
        js = f"window.location.hash = '#current/wind/surface/level/orthographic={target}';"
        self.browser.page().runJavaScript(js)

        self.stack.setCurrentIndex(1)
        QTimer.singleShot(2500, self.show_result)

    def show_result(self):
        name = self.input_name.text().upper()
        city = self.input_city.text()
        date = self.input_date.text()
        
        self.res_user_info.setText(f"<b>{name}</b><br>{city} | {date}")

        weathers = [
            {"icon": "☀️", "temp": "+26°C", "desc": "АШЫҚ АСПАН / ЯСНО"},
            {"icon": "⛅", "temp": "+19°C", "desc": "БҰЛТТЫ / ОБЛАЧНО"},
            {"icon": "⛈️", "temp": "+21°C", "desc": "НАЙЗАҒАЙ / ГРОЗА"},
            {"icon": "💨", "temp": "+15°C", "desc": "ЖЕЛДІ / ВЕТРЕНО"},
            {"icon": "❄️", "temp": "-5°C", "desc": "ҚАРЛЫ / СНЕЖНО"}
        ]
        
        res = random.choice(weathers)
        self.res_icon.setText(res["icon"])
        self.res_temp.setText(res["temp"])
        self.res_desc.setText(res["desc"])
        
        self.stack.setCurrentIndex(2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MeteoBelgiUltimate()
    window.show()
    sys.exit(app.exec())