import aiohttp
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from pyppeteer import launch

import vk_api

import os

import requests
import random
import time

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import sys

LISTEN_URL = 'https://dzen.ru/da_artemov?tab=articles'
TOKEN = '6314588415:AAGYMNfc_Q6IJfeVS2G0XpPQuvGDT-5B17k'
ACCESS_TOKEN = 'vk1.a.u4qARQbioCvQbJXrNlkjwE1sRVLelvnnKW646vsIQ7HKB6UCJcOqLdjBo20P7O6CnmpX0U0LOrpH45cc17_84mntwPEkxEoOLKsIUEwad-0FlcF4Kbxl1pS18jp16mLAggVaMpmzohb1733HMz2u7iPx9yBA2eyAFPNZl1HLmN6PrzwsR5UC0qcN6XUEssilR-O0jtDI_kYk2dQsQDYL1A'
GROUP_ID = '221189347'

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
        self.buttonApiTgKey.clicked.connect(self.save_api_tg_key) #Сюда поместить функцию

        self.inputApiVkKey = QTextEdit(self)
        self.inputApiVkKey.setFixedSize(300, 30)
        self.inputApiVkKey.setText("Введите API ключ к ВК аккаунту")

        self.buttonApiVkKey = QPushButton("Сохранить", self)
        self.buttonApiVkKey.setFixedSize(100, 30)
        self.buttonApiVkKey.clicked.connect(self.save_api_vk_key) #Сюда поместить функцию

        self.inputId = QTextEdit(self)
        self.inputId.setFixedSize(300, 30)
        self.inputId.setText("Введите ID группы ВК")

        self.buttonId = QPushButton("Сохранить", self)
        self.buttonId.setFixedSize(100, 30)
        self.buttonId.clicked.connect(self.save_id_vk) #Сюда поместить функцию

        self.inputURL = QTextEdit(self)
        self.inputURL.setFixedSize(300, 30)
        self.inputURL.setText("Введите URL блога с “Яндекс Дзен”")

        self.buttonURL = QPushButton("Сохранить", self)
        self.buttonURL.setFixedSize(100, 30)
        self.buttonURL.clicked.connect(self.save_url) #Сюда поместить функцию


        self.startPost = QPushButton("Запустить автопостинг", self)
        self.startPost.setFixedSize(200, 30)
        self.startPost.clicked.connect(self.save_id_vk)

        self.stopPost = QPushButton("Остановить автопостинг", self)
        self.stopPost.setFixedSize(200, 30)
        self.stopPost.clicked.connect(self.save_id_vk)

        self.radio_button = QRadioButton('Автозапуск приложения\nпри включении Windows')
        # self.radio_button.setChecked(True)
        self.radio_button.clicked.connect(self.run_app_radio_button)

        self.ClearURL = QPushButton("Очистить базу данных URL", self)
        self.ClearURL.setFixedSize(200, 30)
        self.ClearURL.clicked.connect(self.save_id_vk)
        # button.clicked.connect() #Сюда поместить функцию
        
        self.ClearSetings = QPushButton("Сброс настроек", self)
        self.ClearSetings.setFixedSize(200, 30)
        self.ClearSetings.clicked.connect(self.save_id_vk)
        # button.clicked.connect() #Сюда поместить функцию

        label_one = QLabel('Данный парсер разработан с целью\nавтопостинга из Яндекс Дзена в соцсети')
        label_one.setFixedSize(300, 40)
        label_two = QLabel('Возможности:\n1. Автопостинг в телеграм\n2. Автопостинг в ВК')
        label_two.setFixedSize(300, 80)
        label_three = QLabel('Как работает?\nПриложение считывает указанные вами\nключи и начинает сканирование блога в\nЯндекс Дзен.')
        label_three.setFixedSize(300, 80)
        label_four = QLabel('После сканирования он заносит\nвсе статьи в базу данных чтобы\nпредотвратить повторный постинг.')
        label_four.setFixedSize(300, 80)
        label_five = QLabel('Все что вам нужно сделать - это\nввести ключи и нажать кнопку\n“Запустить автопостинг”')
        label_five.setFixedSize(300, 80)
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
        grid.setRowStretch(8, 30)
        grid.setRowStretch(9, 30)
        grid.setRowStretch(10, 30)
        grid.setRowStretch(11, 30)
        grid.setRowStretch(12, 30)
        grid.setRowStretch(13, 30)


        #ПРАВЫЙ СТОЛБЕЦ
        grid.addWidget(self.buttonApiTgKey, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.buttonApiVkKey, 3, 1, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.buttonId, 5, 1, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.buttonURL, 7, 1, alignment=Qt.AlignmentFlag.AlignRight)
        
        grid.addWidget(self.startPost, 9, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.stopPost, 10, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.radio_button, 11, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.ClearURL, 12, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.ClearSetings, 13, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        #grid.addWidget(self.inputApiTgKey, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        grid.addWidget(self.inputApiTgKey, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.inputApiVkKey, 2, 1, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.inputId, 4, 1, alignment=Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.inputURL, 6, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # grid.addWidget(8, 1, alignment=Qt.AlignmentFlag.AlignRight)


        #Левый столбец
        # label_one
        # grid.addWidget(label_one, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        # grid.addWidget(label_two, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        # grid.addWidget(label_three, 3, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        # grid.addWidget(label_four, 5, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        # grid.addWidget(label_five, 7, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.setLayout(grid)
        self.setStyleSheet("#MainWindow{background-image:url(background.png)}")

        # self.setGeometry(300, 300, 350, 300)
        self.show()

    api_tg_key = ""
    api_vk_key = ""
    id_vk = ""
    url = ""


    def save_api_tg_key(self):
        global TOKEN
        self.api_tg_key = self.inputApiTgKey.toPlainText()
        TOKEN = self.api_tg_key
        print(self.api_tg_key)

    def save_api_vk_key(self):
        global ACCESS_TOKEN
        self.api_vk_key = self.inputApiVkKey.toPlainText()
        ACCESS_TOKEN = self.api_vk_key
        print(self.api_vk_key)

    def save_id_vk(self):
        global GROUP_ID
        self.api_vk_key = self.inputId.toPlainText()
        GROUP_ID = self.api_vk_key
        print(self.api_vk_key)

    def save_url(self):
        global LISTEN_URL
        self.url = self.inputURL.toPlainText()
        LISTEN_URL = self.url
        print(self.url, LISTEN_URL)

    def run_app_radio_button(self):
        global LISTEN_URL
        if self.radio_button.isChecked():            
            file_path = sys.argv[0]
            file_name = file_path.split('\\')[-1]
            path = '%userprofile%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\'
            os.system(f'copy "{file_path}" "{path}{file_name}"')
            print("Файл добавлен в автозапуск")
        else:
            file_path = sys.argv[0]
            file_name = file_path.split('\\')[-1]
            path = '%userprofile%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\'
            os.system(f'del {path+file_name}')
            print("Файл удален из автозапуск")

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
    QLabel {
        font-size: 13px;
        padding-left: 8px;
        background-color: gray;
        color: white;
        border-radius: 30px;
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
    window.resize(300, 640)

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