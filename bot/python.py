import aiohttp
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from pyppeteer import launch

import requests
import random
import time

LISTEN_URL = 'https://dzen.ru/da_artemov?tab=articles'
TOKEN = '6314588415:AAGYMNfc_Q6IJfeVS2G0XpPQuvGDT-5B17k'
ACCESS_TOKEN = 'vk1.a.u4qARQbioCvQbJXrNlkjwE1sRVLelvnnKW646vsIQ7HKB6UCJcOqLdjBo20P7O6CnmpX0U0LOrpH45cc17_84mntwPEkxEoOLKsIUEwad-0FlcF4Kbxl1pS18jp16mLAggVaMpmzohb1733HMz2u7iPx9yBA2eyAFPNZl1HLmN6PrzwsR5UC0qcN6XUEssilR-O0jtDI_kYk2dQsQDYL1A'
GROUP_ID = '221189347'
print(LISTEN_URL)
# START = False

stop_event = asyncio.Event()
stop_event.clear()
# stop_event.set()

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

    # print(article_links)
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


@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
  global LISTEN_URL
  # Создаем клавиатуру с двумя кнопками
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  keyboard.add(types.KeyboardButton("/start"))
  # keyboard.add(types.KeyboardButton("/startListen"))
  keyboard.add(types.KeyboardButton("/stopListen"))
  keyboard.add(types.KeyboardButton("/ChekAPI"))
  # keyboard.add(types.KeyboardButton("/newArticle"))
  keyboard.add(types.KeyboardButton("/newDzenUrl"))
  keyboard.add(types.KeyboardButton("/newVkApiKey"))
  keyboard.add(types.KeyboardButton("/newVkGroupKey"))
  keyboard.add(types.KeyboardButton("Начать прослушивание"))
  keyboard.add(types.KeyboardButton("/help"))
  # keyboard.add(types.KeyboardButton("/exit"))

  await message.reply("Привет! Выберите кнопку:", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def handle_start(message: types.Message):
  await message.reply("/start - начало работы с ботом")
  await message.reply("/ChekAPI - проверить установленные ключи доступа")
  await message.reply("/newDzenUrl - установить новый url Блога")
  await message.reply("/newVkApiKey - ввести новый VK API ключ")
  await message.reply("/newVkGroupKey - ввести новый VK id группы")
  await message.reply(
    "Начать прослушивание - запуск парсинга яндекс дзена (проверка на новые статьи осуществляется каждые 3 секунды!"
  )
  await message.reply("/start")
  await message.reply("/start")
  await message.reply("/start")


@dp.message_handler(commands=['newArticle'])
async def handle_start(message: types.Message):
  await message.reply("Привет! Введите URL сайта:")


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


# @dp.message_handler(commands=['exit'])
# async def handle_start(message: types.Message):
# await exit()


@dp.message_handler(commands=['startListen'])
async def cmd_start(message: types.Message):
  global stop_event
  stop_event.clear()
  await message.reply(
    "Начать прослушивание статьи каждые 5 минут, чтобы завершить введите /stop"
  )


@dp.message_handler(commands=['stopListen'])
async def cmd_stop(message: types.Message):
  global stop_event
  stop_event.set()
  await message.reply("Прослушивание приостановлено!")


async def periodic_job(listenUrl, message):
  # global LISTEN_URL
  # listenUrl = LISTEN_URL
  print("sss", listenUrl, "\n")
  while True:
    await asyncio.sleep(3)  # Пауза в 5 минут (300 секунд)
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

    if stop_event.is_set(
    ):  # Проверяем, что событие установлено (прослушивание приостановлено)
      break


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
      # print("url получен")
      # allText, saveText, image_url = await process_url(user_url)
      # print("контент получен")

      # await message.reply(f"{allText}")
      # await message.reply(f"{saveText}")

      # if image_url:
      #   await message.reply_photo(image_url)
      # else:
      #   await message.reply("На странице нет изображений.")

      # vk_posting(allText + saveText, image_url)
  elif 'Начать прослушивание' in user_url:
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_job(LISTEN_URL, message))
  elif 'vk' in user_url:
    ACCESS_TOKEN = user_url
    await message.reply(f"{ACCESS_TOKEN}")
  elif len(user_url) < 10 and len(user_url) > 0:
    GROUP_ID = user_url
    await message.reply(f"{GROUP_ID}")
  else:
    await message.reply("Прости, я не понял, введи /start")


def start_scraping_time():
  start = True
  while (start):

    time.sleep(3)


if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)
