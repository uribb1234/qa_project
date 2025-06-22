from itertools import product
from unittest import TestCase
import db.init_db as db
import requests

BASE_URL = "http://127.0.0.1:5000/api/products"

class TestProductAPI(TestCase):

    @classmethod
    def setUpClass(cls):
        db.truncate_products_table()

    def test1_add_product(self):
        product = {"name": "Cola", "price": 6.50, "image": "cola.jpg"}
        response = requests.post(BASE_URL, json= product)
        print(response.text)
        print(response.status_code)
        self.assertEqual(201, response.status_code)
        self.assertIn('"id": 1', response.text)
        self.assertIn('"message": "Product added"', response.text)

    def test2_add_existing_product(self):
        product = {"name": "Cola", "price": 6.50, "image": "cola.jpg"}
        response = requests.post(BASE_URL, json= product)
        print(response.text)
        print(response.status_code)
        self.assertEqual(response.status_code, 400)
        self.assertIn('"error": "Product with name Cola already exists"', response.text)