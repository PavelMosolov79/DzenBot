
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.window_title()
        self.button_start()

    def window_title(self):
        # self.setFixedSize(QSize(650, 700))
        # self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('icon.png'))

    def button_start(self):
        #Ввод для API TG
        self.inputApiTgKey = QTextEdit(self)
        self.inputApiTgKey.setFixedSize(300, 30)
        self.inputApiTgKey.setText("Введите API ключ к боту телеграмма")

        self.buttonApiTgKey = QPushButton("Сохранить", self)
        self.buttonApiTgKey.setFixedSize(100, 30)
        # button.clicked.connect() #Сюда поместить функцию

        self.inputApiVkKey = QTextEdit(self)
        self.inputApiVkKey.setFixedSize(300, 30)
        self.inputApiVkKey.setText("Введите API ключ к ВК аккаунту")

        self.buttonApiVkKey = QPushButton("Сохранить", self)
        self.buttonApiVkKey.setFixedSize(100, 30)
        # button.clicked.connect() #Сюда поместить функцию

        self.inputId = QTextEdit(self)
        self.inputId.setFixedSize(300, 30)
        self.inputId.setText("Введите ID группы ВК")

        self.buttonId = QPushButton("Сохранить", self)
        self.buttonId.setFixedSize(100, 30)
        self.buttonId.clicked.connect() #Сюда поместить функцию

        self.inputURL = QTextEdit(self)
        self.inputURL.setFixedSize(300, 30)
        self.inputURL.setText("Введите URL блога с “Яндекс Дзен”")

        self.buttonURL = QPushButton("Сохранить", self)
        self.buttonURL.setFixedSize(100, 30)
        # button.clicked.connect() #Сюда поместить функцию


        self.startPost = QPushButton("Запустить автопостинг", self)
        self.startPost.setFixedSize(200, 30)

        self.stopPost = QPushButton("Остановить автопостинг", self)
        self.stopPost.setFixedSize(200, 30)

        self.radio_button = QRadioButton('Автозапуск приложения\nпри включении Windows')
        self.radio_button.setChecked(True)

        self.ClearURL = QPushButton("Очистить базу данных URL", self)
        self.ClearURL.setFixedSize(200, 30)
        # button.clicked.connect() #Сюда поместить функцию
        
        self.ClearSetings = QPushButton("Сброс настроек", self)
        self.ClearSetings.setFixedSize(200, 30)
        # button.clicked.connect() #Сюда поместить функцию

        label_one = QLabel('Данный парсер разработан с целью автопостинга из Яндекс Дзена в соцсет')
        label_two = QLabel('Возможности:\n1. Автопостинг в телеграм\n2. Автопостинг в ВК')
        label_one.setFixedSize(200, 30)
        grid = QGridLayout()
        
        # grid.setHorizontalSpacing(100)
        # grid.color("black")
        # grid.setSpacing(10)
        grid.setRowStretch(0, 30)
        grid.setRowStretch(1, 30)
        grid.setRowStretch(2, 30)
        grid.setRowStretch(3, 30)
        grid.setRowStretch(4, 30)
        grid.setRowStretch(5, 30)
        grid.setRowStretch(6, 30)
        grid.setRowStretch(7, 30)

        # grid.setRowStretch(1, 10)
        # grid.setRowStretch(2, 10)
        # grid.setRowStretch(3, 10)


        #ПРАВЫЙ СТОЛБЕЦ
        grid.addWidget(self.buttonApiTgKey, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.buttonApiVkKey, 3, 2, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.buttonId, 5, 2, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.buttonURL, 7, 2, alignment=Qt.AlignmentFlag.AlignRight)
        
        grid.addWidget(self.startPost, 9, 1, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.stopPost, 10, 1, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.radio_button, 11, 1, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.ClearURL, 12, 1, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.ClearSetings, 13, 1, alignment=Qt.AlignmentFlag.AlignRight)
        
        #grid.addWidget(self.inputApiTgKey, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.inputApiTgKey, 0, 2, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.inputApiVkKey, 2, 2, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.inputId, 4, 2, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.inputURL, 6, 2, alignment=Qt.AlignmentFlag.AlignRight)
        # grid.addWidget(8, 1, alignment=Qt.AlignmentFlag.AlignRight)


        #Левый столбец
        # label_one
        grid.addWidget(label_one, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(label_two, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(grid)
        self.setStyleSheet("#MainWindow{background-image:url(background.png)}")

        # self.setGeometry(300, 300, 350, 300)
        self.show()

def ui_interfase():

    app = QApplication(sys.argv)
    app.setStyle('Breeze')

    app.setStyleSheet("""
    QTextEdit {
        background-color: white;
        border-radius: 30px;
         color: #A1A1A1;
    }
    QPushButton {
        font-size: 16px;
        background-color: #494949;
        border-radius: 30px;
        color: white;
    }

    QPushButton:hover {
        font-size: 16px;
        background-color: black;
        border-radius: 30px;
        color: white;
    }
    QLineEdit {
        background-color: "white";
        color: "black";
    }

    """)
    
    # ui = MainWindow()
    

    window = MainWindow()

    window.setStyleSheet("#MainWindow{border-image:url(background.png)}")
    window.setWindowTitle('DzenParserApp')
    window.setWindowIcon(QIcon('icon.png'))
    window.resize(640, 640)

    window.show()

    sys.exit(app.exec())
    # app = QApplication(sys.argv)
    

    # Создаём виджет Qt — окно.
    # window = QMainWindow()
    # window.setObjectName("MainWindow")
    # window.setStyleSheet("#MainWindow{border-image:url(background.png)}")
    # window.setWindowTitle('DzenParserApp')
    # window.setWindowIcon(QIcon('icon.png'))

    # window.resize(640, 640)

    # window.show()  # Важно: окно по умолчанию скрыто.

    # # Запускаем цикл событий.
    # sys.exit(app.exec())

if __name__ == "__main__":
    ui_interfase()