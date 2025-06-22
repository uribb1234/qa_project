from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
from unittest import TestCase
from selenium.webdriver.support.ui import Select
import os
from datetime import datetime


class TestUI(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = Chrome()
        cls.driver.maximize_window()
        cls.base_url = 'http://127.0.0.1:5000/other/home'

        if not os.path.exists('./images'):
            os.makedirs('./images')

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.close()

    def setUp(self):
        self.driver.get(self.base_url)

    def test1_popup_text_demo(self):
        self.driver.find_element(By.XPATH, '/html/body/section/main/button[1]').click()
        prompt = self.driver.switch_to.alert
        prompt.send_keys('Hello!')
        prompt.accept()
        self.driver.save_screenshot('./images/popup_text_demo.png')

    def test2_table_check(self):
        table = self.driver.find_element(By.TAG_NAME, 'table')
        tr_list = table.find_elements(By.TAG_NAME, 'tr')
        self.assertEqual(4, len(tr_list))

        td_list = tr_list[3].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(3, len(td_list))
        self.assertEqual('Berlin', td_list[1].text)
        self.driver.save_screenshot('./images/table_check.png')

    def test3_only_one_h1(self):
        h1_list = self.driver.find_elements(By.TAG_NAME, 'h1')
        self.assertEqual(1, len(h1_list))
        self.driver.save_screenshot('./images/only_one_h1.png')

    def test4_number_of_tables(self):
        tables_list = self.driver.find_elements(By.TAG_NAME, 'table')
        self.assertEqual(2, len(tables_list))
        self.driver.save_screenshot('./images/number_of_tables.png')

    def test5_cities_title(self):
        h2_list = self.driver.find_elements(By.TAG_NAME, 'h2')
        self.assertEqual('Cities of the World', h2_list[0].text)
        self.driver.save_screenshot('./images/cities_title.png')

    def test6_students_title(self):
        h2_list = self.driver.find_elements(By.TAG_NAME, 'h2')
        self.assertEqual('Student Details', h2_list[1].text)
        self.driver.save_screenshot('./images/students_title.png')

    def test7_number_of_students(self):
        tbody = self.driver.find_element(By.XPATH, '/html/body/section/main/div[2]/table/tbody')
        students_list = tbody.find_elements(By.TAG_NAME, 'tr')
        self.assertEqual(5, len(students_list))
        self.driver.save_screenshot('./images/number_of_students.png')

    def test8_passing_to_webster(self):
        self.driver.find_element(By.LINK_TEXT, 'Merriam-Webster Dictionary').click()
        outer_url = self.driver.current_url
        self.assertEqual('https://www.merriam-webster.com/', outer_url)
        self.driver.save_screenshot('./images/passing_to_webster.png')

    def test9_form(self):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        form = self.driver.find_element(By.TAG_NAME, 'fieldset')

        self.driver.save_screenshot(f'./images/form_before_fill_{timestamp}.png')
        time.sleep(1)

        fname = form.find_element(By.ID, 'first-name')
        lname = form.find_element(By.ID, 'last-name')
        city = form.find_element(By.ID, 'city')
        email = form.find_element(By.ID, 'email')
        mobile = form.find_element(By.ID, 'mobile')
        gender = form.find_element(By.ID, "female")
        math = form.find_element(By.ID, 'math')
        english = form.find_element(By.ID, 'english')

        fname.send_keys('Zoe')
        lname.send_keys('Cohen')
        select_city = Select(city)
        select_city.select_by_value('Tel Aviv')
        email.send_keys('zoe@mail.com')
        mobile.send_keys('050333444')
        gender.click()
        math.click()
        english.click()

        time.sleep(1)
        self.driver.save_screenshot(f'./images/form_after_fill_{timestamp}.png')
        time.sleep(1)

        submit_bt = self.driver.find_element(By.XPATH, '//*[@id="submit-form"]')
        submit_bt.click()

        time.sleep(2)
        self.driver.save_screenshot(f'./images/form_after_submit_{timestamp}.png')

        new_url = self.driver.current_url
        self.assertIn('http://127.0.0.1:5000/other/next', new_url)

    def test10_download_form(self):
        bt = self.driver.find_element(By.XPATH, '/html/body/section/main/fieldset[2]/button')
        bt.click()
        time.sleep(2)
        download_finish_id = self.driver.find_element(By.ID, "download-finished-msg")
        download_finish_id.is_displayed()
        bt_ok = self.driver.find_element(By.XPATH, '//*[@id="download-finished-msg"]/button')
        bt_ok.click()
        time.sleep(1)
        style = download_finish_id.get_attribute("style")
        assert "display: none" in style, f"style = {style}"
        self.driver.save_screenshot('./images/download_form.png')
