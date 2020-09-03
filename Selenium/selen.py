from selenium import webdriver
from bs4 import BeautifulSoup

chromedriver = 'C:\Program Files\ChromeDriver\chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')  # для открытия headless-браузера
browser = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)
browser.get(
    'https://bilet.railways.kz/sale/default/route/search?route_search_form%5BdepartureStation%5D=2708001'
    '&route_search_form%5BarrivalStation%5D=2708952&route_search_form%5BforwardDepartureDate%5D=24-06-2020%2C+%D1%81'
    '%D1%80%D0%B4&route_search_form%5BbackwardDepartureDate%5D=&_locale=ru')

button = browser.find_element_by_class_name('ktj info link')
button.click()
sp = browser.page_source
soup = BeautifulSoup(sp, 'lxml')
desc = soup.select_one('div.scrolling.content.train-modal-body ')

print(desc)