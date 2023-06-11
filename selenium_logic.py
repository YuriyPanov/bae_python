from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time, re

def get_by_reg_exp(text):
    numbers = re.findall('\\b[\\d]+\\b', text)
    return int(''.join(numbers))

class TicketsGetter:
    tickets = {}
    types = ["Сидячий", "Купе", "Плацкартный", "СВ"]

    def __init__(self, city_from, city_to):
        self.city_from = city_from
        self.city_to = city_to

        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 500)

    def set_new_date(self, new_date):
        self.date = new_date
        self.tickets[self.date] = {}
        self.driver.get("https://www.rzd.ru")
        for type_vague in self.types:
            self.tickets[self.date][type_vague] = -1

    def wait_load(self, name):
        if name == "rzd-suggestion":
            self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, name)))
            if len(self.driver.find_elements(By.CLASS_NAME, name)) != 0:
                self.wait.until(lambda driver: len(driver.find_elements(By.CLASS_NAME, name)) > 0 
                                and "ПОПУЛЯРНЫЕ НАПРАВЛЕНИЯ" not in driver.find_elements(By.CLASS_NAME, name)[0].text)
        else:
            self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "button--terminal")))
            return len(self.driver.find_elements(By.CLASS_NAME, name))

    def first_load(self):

        elems = [
            self.driver.find_element(By.ID, "direction-from"),
            self.driver.find_element(By.ID, "direction-to"),
            self.driver.find_element(By.ID, "datepicker-from")
        ]

        data = [
            self.city_from,
            self.city_to,
            self.date
        ]

        for i in range(0, 3):
            elems[i].send_keys(data[i])
            if i > 1:
                continue

            self.wait_load("rzd-suggestion")
            elements = self.driver.find_elements(By.CLASS_NAME, "rzd-suggestion")
            elements[1].click()

        elem = self.driver.find_element(By.CLASS_NAME, "rzd-button")
        elem.click()

    def get_types_tickets(self):
        elems_quantity = self.driver.find_elements(By.CLASS_NAME, "card-class__quantity")

        elems_price = self.driver.find_elements(By.CLASS_NAME, "card-class__price")

        elems_name = self.driver.find_elements(By.CLASS_NAME, "card-class__name")
        
        for i in range(0, len(elems_name)):
            if elems_name[i].text not in self.tickets[self.date].keys():
                continue

            cost = get_by_reg_exp(elems_price[i].text)
            if self.tickets[self.date][elems_name[i].text] == -1:
                self.tickets[self.date][elems_name[i].text] = cost
            elif self.tickets[self.date][elems_name[i].text] > cost:
                self.tickets[self.date][elems_name[i].text] = cost