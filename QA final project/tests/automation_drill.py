from unittest import TestCase
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import os
import db.init_db as db  # used for database actions
from selenium.common.exceptions import NoAlertPresentException

class TestUI(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://127.0.0.1:5000"
        cls.driver = Chrome()
        cls.driver.maximize_window()

        if not os.path.exists('./images'):
            os.makedirs('./images')

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.close()

    def setUp(self):
        db.truncate_products_table()
        time.sleep(1)
        self.driver.get(self.base_url)

    def test_h1(self):
        h1 = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual("Product Manager", h1.text)
        self.driver.save_screenshot('./images/h1_title.png')

    def test1_add_product(self):
        tbody = self.driver.find_element(By.ID, "product-table")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(0, len(rows))

        name = self.driver.find_element(By.ID, "name")
        price = self.driver.find_element(By.ID, "price")
        image = self.driver.find_element(By.ID, "image")
        bt = self.driver.find_element(By.XPATH, '//*[@id="product-form"]/button')

        name.send_keys("TV")
        price.send_keys("3000")
        image.send_keys("tv.jpg")
        bt.click()
        time.sleep(3)
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(1, len(rows))
        self.driver.save_screenshot('./images/add_product.png')

    def test2_link_to_other_site(self):
        link = self.driver.find_element(By.TAG_NAME, "a")
        link.click()
        time.sleep(2)

        final_url = "http://127.0.0.1:5000/other/home"
        self.assertIn(final_url, self.driver.current_url)
        self.driver.save_screenshot('./images/link_to_other_page.png')

    def test3_delete_product(self):
        tbody = self.driver.find_element(By.ID, "product-table")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(0, len(rows))

        name = self.driver.find_element(By.ID, "name")
        price = self.driver.find_element(By.ID, "price")
        image = self.driver.find_element(By.ID, "image")
        bt = self.driver.find_element(By.XPATH, '//*[@id="product-form"]/button')
        name.send_keys("bed")
        price.send_keys("300")
        image.send_keys("bed.jpg")
        bt.click()
        time.sleep(3)

        rows = tbody.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(1, len(rows))

        delete_button = self.driver.find_element(By.XPATH, '//*[@id="product-table"]/tr/td[5]/button[3]')
        delete_button.click()
        time.sleep(1)

        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            self.fail("Expected alert did not appear")

        time.sleep(2)

        rows = tbody.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(0, len(rows))
        self.driver.save_screenshot('./images/delete_product.png')

    def test4_update_product(self):
        tbody = self.driver.find_element(By.ID, "product-table")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(0, len(rows))

        name = self.driver.find_element(By.ID, "name")
        price = self.driver.find_element(By.ID, "price")
        image = self.driver.find_element(By.ID, "image")
        bt = self.driver.find_element(By.XPATH, '//*[@id="product-form"]/button')

        name.send_keys("Book")
        price.send_keys("30")
        image.send_keys("book.jpg")
        bt.click()
        time.sleep(3)
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(1, len(rows))

        bt_edit = self.driver.find_element(By.XPATH, '//*[@id="product-table"]/tr/td[5]/button[2]')
        bt_edit.click()
        price.clear()
        price.send_keys('10')
        bt.click()
        time.sleep(3)
        price_repr = self.driver.find_element(By.XPATH, '//*[@id="product-table"]/tr/td[3]')
        self.assertEqual('$10.00', price_repr.text)
        self.driver.save_screenshot('./images/update_product.png')

    def test5_view_product(self):
        tbody = self.driver.find_element(By.ID, "product-table")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(0, len(rows))

        name = self.driver.find_element(By.ID, "name")
        price = self.driver.find_element(By.ID, "price")
        image = self.driver.find_element(By.ID, "image")
        bt = self.driver.find_element(By.XPATH, '//*[@id="product-form"]/button')

        name.send_keys("Book")
        price.send_keys("30")
        image.send_keys("book.jpg")
        bt.click()
        time.sleep(3)
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(1, len(rows))

        bt_details = self.driver.find_element(By.XPATH,'//*[@id="product-table"]/tr/td[5]/button[1]')
        bt_details.click()

        demo_table = self.driver.find_element(By.CLASS_NAME, 'card')
        demo_table.is_displayed()
        self.driver.save_screenshot('./images/view_product.png')
