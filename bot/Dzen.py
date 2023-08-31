import aiohttp
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from pyppeteer import launch

import requests
import random
import time

import os

LISTEN_URL = ''
TOKEN = ''
ACCESS_TOKEN = ''
GROUP_ID = ''

def load_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Разделяем строку на ключ и значение, используя знак равенства как разделитель
            key, value = line.strip().split(' = ')
            # Избавляемся от кавычек в значении, если они есть
            value = value.strip("'")
            config[key] = value
    return config



config = {}

file_path = 'config.txt'
config = load_config(file_path)

LISTEN_URL = config['LISTEN_URL']
TOKEN = config['TOKEN']
ACCESS_TOKEN = config['ACCESS_TOKEN']
GROUP_ID = config['GROUP_ID']


stop_event = asyncio.Event()
stop_event.set()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)




import vk_api


def vk_posting(allText, image_url):
  POST_TEXT = allText

  vk_session = vk_api.VkApi(token=ACCESS_TOKEN)
  vk = vk_session.get_api()

  attachments = []

  if image_url:
    try:
      response = requests.get(image_url)
      if response.status_code == 200:
        photo_data = response.content

        upload_url = vk.photos.getWallUploadServer(
          group_id=GROUP_ID)['upload_url']

        files = {'photo': ('photo.jpg', photo_data, 'image/jpeg')}
        response = requests.post(upload_url, files=files)
        json_data = response.json()

        if 'server' in json_data and 'photo' in json_data and 'hash' in json_data:
          photo_data = vk.photos.saveWallPhoto(group_id=GROUP_ID,
                                               server=json_data['server'],
                                               photo=json_data['photo'],
                                               hash=json_data['hash'])
          photo_link = f"photo{photo_data[0]['owner_id']}_{photo_data[0]['id']}"
          attachments.append(photo_link)
        else:
          print("Error uploading image to VK: ", json_data)

      else:
        print("Error downloading image: ", response.status_code)

    except Exception as e:
      print("Error while processing image: ", e)

  if attachments:
    vk.wall.post(owner_id='-' + GROUP_ID,
                 message=POST_TEXT,
                 attachments=",".join(attachments))
  else:
    vk.wall.post(owner_id='-' + GROUP_ID, message=POST_TEXT)

  print('Пост успешно опубликован.')


def text_bold_h1(allText, h1_element):
  allText += h1_element[0]
  allText += "\n\n"

  return allText


def text_bold_p(allText, p_element):
  smile = ["❗️", "📌", "🔥", "⚙️", "📍", ""]
  saveText = ""

  for i in range(len(p_element)):
    if len(p_element[i]) <= 10:
      continue
    else:
      if len(allText + p_element[i]) <= 4000:
        smileRand = random.randint(0, 5)
        allText += smile[smileRand]
        allText += p_element[i]
        allText += smile[smileRand]
        allText += "\n\n"
      else:
        smileRand = random.randint(0, 5)
        saveText += smile[smileRand]
        saveText += p_element[i]
        saveText += smile[smileRand]
        saveText += "\n\n"

  return allText, saveText


async def get_content(url):
  browser = await launch()
  page = await browser.newPage()
  await page.goto(url)

  # Ожидание загрузки всех элементов h1 на странице
  await page.waitForSelector("h1")

  # Получение всех элементов h1 на странице
  h1_elements = await page.querySelectorAll("h1")

  # Получение текстового содержимого каждого элемента h1
  h1_contents = []
  for h1_element in h1_elements:
    h1_content = await page.evaluate('(element) => element.textContent',
                                     h1_element)
    h1_contents.append(h1_content.strip())

  # Ожидание загрузки всех элементов p на странице
  await page.waitForSelector("p")

  # Получение всех элементов p на странице
  p_elements = await page.querySelectorAll("p")

  # Получение текстового содержимого каждого элемента p
  p_contents = []
  for p_element in p_elements:
    p_content = await page.evaluate('(element) => element.textContent',
                                    p_element)
    p_contents.append(p_content.strip())

  # Находим первое изображение на странице (можно настроить выбор нужного элемента)
  image_element = await page.querySelector("img")
  if image_element:
    image_url = await page.evaluate('(element) => element.src', image_element)

  await browser.close()
  return h1_contents, p_contents, image_url


def trim_urls(urls):
  trimmed_urls = []
  for url in urls:
    trimmed_url = url.split("?")[0]
    trimmed_urls.append(trimmed_url)
  return trimmed_urls


def remove_duplicates_from_list(input_list):
  return list(set(input_list))


async def get_href(url):
  try:
    print("запуск браузера")
    browser = await launch()
    print("браузер запустился")
    page = await browser.newPage()
    print("создаем новую страницу")
    await page.goto(url)
    print("переходим по url")
    await page.waitForXPath(
      "//a[contains(@class, 'card-image-compact-view__clickable')]",
      timeout=30000)
    print("ждем 50 секунд загрузки классов")
    # Прокрутка вниз, чтобы загрузить оставшиеся ссылки
    while True:
      last_height = await page.evaluate("document.body.scrollHeight")
      await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

      # Ожидание перед следующей прокруткой (1 секунда)
      await asyncio.sleep(5)

      new_height = await page.evaluate("document.body.scrollHeight")
      if new_height == last_height:
        break  # Прокрутка больше не загружает новые элементы, выходим из цикла

    # Получение всех элементов a с классом 'card-image-compact-view__clickable' на странице
    article_links_elements = await page.xpath(
      "//a[contains(@class, 'card-image-compact-view__clickable')]")

    # Преобразуем элементы в список ссылок
    article_links = [
      await page.evaluate('(element) => element.href', el)
      for el in article_links_elements
    ]

    article_links = trim_urls(article_links)

    article_links = remove_duplicates_from_list(article_links)

    await browser.close()
    return article_links
  except Exception as e:
    print(f"Произошла ошибка: {e}")
    return None


async def get_image_url(url):
  browser = await launch()
  page = await browser.newPage()
  await page.goto(url)

  # Находим первое изображение на странице (можно настроить выбор нужного элемента)
  image_element = await page.querySelector("img")
  if image_element:
    image_url = await page.evaluate('(element) => element.src', image_element)
    await browser.close()
    return image_url
  else:
    await browser.close()
    return None


async def href_process_url(user_url):
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(user_url) as response:
        if response.status == 200:
          print("connect 200")
          href_contents = await get_href(user_url)
          return href_contents
        else:
          print("connect 400")
          return None
  except Exception as e:
    return None


async def process_url(user_url):
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(user_url) as response:
        if response.status == 200:
          print("connect 200")
          h1_contents, p_contents, image_url = await get_content(user_url)

          allText = ""
          saveText = ""
          allText = text_bold_h1(allText, h1_contents)
          allText, saveText = text_bold_p(allText, p_contents)
          return allText, saveText, image_url
        else:
          print("connect 400")
          return None, None, None
  except Exception as e:
    return None, None, None


async def periodic_job(listenUrl, message):
  print("sss", listenUrl, "\n")
  while True:
    await asyncio.sleep(30)  # Пауза в (30 секунд)
    urls = await href_process_url(listenUrl)

    if urls:
      with open("bd.txt", "r") as file:
        print("открыли файл")
        urlsFile = file.readlines()

      existing_urls = {url.strip() for url in urlsFile}

      new_urls = [link for link in urls if link not in existing_urls]
      print(new_urls)
      if new_urls != []:
        with open("bd.txt", "a") as file:
          for link in new_urls:
            file.write(link + "\n")
        print("Ссылки успешно записаны в базу данных bd.txt")
        for url in new_urls:
          print("url получен")
          allText, saveText, image_url = await process_url(url)
          print("контент получен")
          if allText:
            await message.reply(f"{allText}")
          if saveText:
            await message.reply(f"{saveText}")

          if image_url:
            await message.reply_photo(image_url)
          else:
            await message.reply("На странице нет изображений.")
          if allText and image_url:
            vk_posting(allText + saveText, image_url)
          await asyncio.sleep(5)
      else:
        print("Новых ссылок нет")

        #Здесь надо начинать парсинг статей.

    else:
      print("Новых ссылок нет")

    if stop_event.is_set():  # Проверяем, что событие установлено (прослушивание приостановлено)
      break



@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
  global LISTEN_URL
  # Создаем клавиатуру с двумя кнопками
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  keyboard.add(types.KeyboardButton("/start"))
  keyboard.add(types.KeyboardButton("/ChekAPI"))
  keyboard.add(types.KeyboardButton("/Начать прослушивание"))
  keyboard.add(types.KeyboardButton("/Остановить прослушивание"))
  keyboard.add(types.KeyboardButton("/help"))
  keyboard.add(types.KeyboardButton("/Очистить базу данных URl"))


  await message.reply("Привет! Выберите кнопку:", reply_markup=keyboard)

@dp.message_handler(commands=['help'])
async def handle_start(message: types.Message):
  await message.reply(""" 
  /start - начало работы с ботом\n
/ChekAPI - проверить установленные ключи доступа\n
Начать прослушивание - запуск парсинга яндекс дзена (проверка на новые статьи осуществляется каждые 3 секунды!\n
Остановить прослушивание - запуск парсинга яндекс дзена (проверка на новые статьи осуществляется каждые 3 секунды!\n
Автозапуск бота при включении Windows - добавляет приложение в автозапуск\n
Очистить базу данных URl - Удалаяет записи всех статей из базы данных, которые были найдены в блоге, после очистки при нажатии на "Начать прослушивание" бот снова выложит все статьи. СОХРАНИТЕ КОПИЮ ФАЙЛА ПЕРЕД УДАЛЕНИЕМ В ДРУГОЕ МЕСТО. ОСТОРОЖНО! ДАННОЕ ДЕСТВИЕ НЕЛЬЗЯ ОБРАТИТЬ!""")


@dp.message_handler(commands=['newVkApiKey'])
async def handle_start(message: types.Message):
  await message.reply("Введите новый VK API ключ:")


@dp.message_handler(commands=['newVkGroupKey'])
async def handle_start(message: types.Message):
  await message.reply("Введите новый VK id группы:")


@dp.message_handler(commands=['newDzenUrl'])
async def handle_start(message: types.Message):
  await message.reply("Введите новый адресс блога:")


@dp.message_handler(commands=['ChekAPI'])
async def handle_start(message: types.Message):
  await message.reply(f"VK API: {ACCESS_TOKEN}\nVK GROUP ID: {GROUP_ID}")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
  global ACCESS_TOKEN, GROUP_ID, LISTEN_URL

  global stop_event
  if not stop_event.is_set():
    await message.reply("Прослушивание идет!")

  user_url = message.text

  if 'https://dzen.ru' in user_url:
    print("url получен")
    if ACCESS_TOKEN == "":
      print("url получен")
      await message.reply(
        "VK API ключ отсутствует.\n\nКомманда для ввода ключа - /newVkApiKey")
    elif GROUP_ID == "":
      await message.reply(
        "id группы VK отсутствует.\n\nКомманда для ввода id - /newVkGroupKey")
    else:
      LISTEN_URL = user_url
  elif 'Начать прослушивание' in user_url:
    stop_event.clear()
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_job(LISTEN_URL, message))
  elif 'Остановить прослушивание' in user_url:
    stop_event.set()
    await message.reply("Прослушивание приостановлено!")
  elif 'Очистить базу данных URl' in user_url:
    file_path = 'bd.txt'
    with open(file_path, 'w') as file:
      pass
    await message.reply("База URL адресов очищена")
  elif 'vk' in user_url:
    ACCESS_TOKEN = user_url
    await message.reply(f"{ACCESS_TOKEN}")
  elif len(user_url) < 10 and len(user_url) > 0:
    GROUP_ID = user_url
    await message.reply(f"{GROUP_ID}")
  else:
    await message.reply("Прости, я не понял, введи /start")


if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)
