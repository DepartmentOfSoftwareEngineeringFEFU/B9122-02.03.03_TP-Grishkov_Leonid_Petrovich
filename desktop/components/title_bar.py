import sys
import qtawesome as qta
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

# Подключаем WinAPI функции для Windows
if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32

class CustomTitleBar(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        
        self.setFixedHeight(55) 
        self.setObjectName("CustomTitleBar")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 0, 0)
        layout.setSpacing(0) # <-- ИСПРАВЛЕНО: Убираем любые зазоры между кнопками
        # layout.setSpacing(5)
        
        self.icon_label = QLabel()
        self.icon_label.setPixmap(qta.icon("fa5s.building", color="#0067B8").pixmap(24, 24))
        
        self.title_label = QLabel("Мини-ERP Система")
        self.title_label.setObjectName("TitleBarText")
        
        btn_size = QSize(55, 55)
        icon_size = QSize(16, 16)
        
        self.btn_minimize = QPushButton()
        self.btn_minimize.setIcon(qta.icon("fa5s.window-minimize", color="#333333"))
        self.btn_minimize.setFixedSize(btn_size)
        self.btn_minimize.setIconSize(icon_size)
        self.btn_minimize.clicked.connect(self.parent_window.showMinimized)
        
        self.btn_maximize = QPushButton()
        self.btn_maximize.setIcon(qta.icon("fa5s.window-maximize", color="#333333"))
        self.btn_maximize.setFixedSize(btn_size)
        self.btn_maximize.setIconSize(icon_size)
        self.btn_maximize.clicked.connect(self.toggle_maximize)
        
        self.btn_close = QPushButton()
        self.btn_close.setObjectName("TitleBtnClose")
        self.btn_close.setIcon(qta.icon("fa5s.times", color="#333333", color_active="#FFFFFF"))
        self.btn_close.setFixedSize(btn_size)
        self.btn_close.setIconSize(icon_size)
        self.btn_close.clicked.connect(self.parent_window.close)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.btn_minimize)
        layout.addWidget(self.btn_maximize)
        layout.addWidget(self.btn_close)

    def toggle_maximize(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.btn_maximize.setIcon(qta.icon("fa5s.window-maximize", color="#333333"))
        else:
            self.parent_window.showMaximized()
            self.btn_maximize.setIcon(qta.icon("fa5s.window-restore", color="#333333"))

    def mousePressEvent(self, event):
        # Передаем перетаскивание на уровень операционной системы Windows
        if event.button() == Qt.LeftButton and sys.platform == "win32":
            user32.ReleaseCapture()
            
            # Явно приводим идентификатор окна к int()
            window_handle = int(self.parent_window.winId())
            
            # Отправляем сообщение WM_NCLBUTTONDOWN с параметром HTCAPTION (2)
            user32.SendMessageW(window_handle, 0x00A1, 2, 0)
            event.accept()
        else:
            super().mousePressEvent(event)