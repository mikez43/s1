import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:/SF/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()


   yield

   pytest.driver.quit()

def test_show_my_pets():
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

def test_all_pets_exist():
   pytest.driver.get('http://petfriends.skillfactory.ru/my_pets')
   sum_pets_loc = WebDriverWait(pytest.driver, 5).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, 'div.task3.fill div.\.col-sm-4.left'))
   )
   #Разбиваем текстовые данные по :, пробелу и переносу строки с выделением и преобразованием 4 элемента в int
   sum_pets = int(re.split(":| |\n", sum_pets_loc.text)[3])
   #Определяем локатор количества карточек питомцев на странице
   sum_card_loc = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
   sum_card = len(sum_card_loc)
   print(sum_card)
   assert sum_pets == sum_card

def test_foto_half_pets():
   pytest.driver.implicitly_wait(5)
   pytest.driver.get('http://petfriends.skillfactory.ru/my_pets')
   sum_pets_loc = pytest.driver.find_element(By.CSS_SELECTOR, 'div.task3.fill div.\.col-sm-4.left')
   sum_pets = int(re.split(":| |\n", sum_pets_loc.text)[3])
   pytest.driver.implicitly_wait(5)
   sum_foto_loc = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img[contains(@src, "data")]')
   sum_foto = len(sum_foto_loc)
   assert (sum_pets/2) <= sum_foto

def test_pets_have_name_age_breed():
   pytest.driver.implicitly_wait(5)
   pytest.driver.get('http://petfriends.skillfactory.ru/my_pets')
   sum_pets_loc = pytest.driver.find_element(By.CSS_SELECTOR, 'div.task3.fill div.\.col-sm-4.left')
   sum_pets = int(re.split(":| |\n", sum_pets_loc.text)[3])

   for i in range(sum_pets):
      name_loc = pytest.driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[' + str(i+1) + ']/td[1]')
      age_loc = pytest.driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[' + str(i+1) + ']/td[3]')
      breed_loc = pytest.driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[' + str(i+1) + ']/td[2]')

      assert (name_loc.text != '' and age_loc.text != '' and breed_loc.text != '')
      print(i+1)

def test_uniq_name():
   pytest.driver.implicitly_wait(5)
   pytest.driver.get('http://petfriends.skillfactory.ru/my_pets')
   sum_pets_loc = pytest.driver.find_element(By.CSS_SELECTOR, 'div.task3.fill div.\.col-sm-4.left')
   sum_pets = int(re.split(":| |\n", sum_pets_loc.text)[3])
   names = []

   for i in range(sum_pets):
       name_loc = pytest.driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[' + str(i + 1) + ']/td[1]')
       names.append(name_loc.text)

   duplicate = {x for x in names if names.count(x) > 1}
   assert duplicate == {}