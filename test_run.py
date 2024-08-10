import unittest
import argparse
from analyzePlace import map_objects
from scoreBasket import showBasket

class TestMapObjects(unittest.TestCase):
    def setUp(self):
        self.data_array = [
            # 红色球
            [
                {"center": {"x": 10, "y": 30}, "name": "Red Ball 1", "class": "red", "confidence": 0.9, "box": [5, 15, 25, 35]},
                {"center": {"x": 20, "y": 20}, "name": "Red Ball 2", "class": "red", "confidence": 0.8, "box": [15, 25, 35, 45]},
                {"center": {"x": 35, "y": 20}, "name": "Red Ball 3", "class": "red", "confidence": 0.7, "box": [15, 25, 35, 45]}
            ],
            # 蓝色球
            [
                {"center": {"x": 30, "y": 10}, "name": "Blue Ball 1", "class": "blue", "confidence": 0.7, "box": [25, 35, 45, 55]},
                {"center": {"x": 40, "y": 15}, "name": "Blue Ball 2", "class": "blue", "confidence": 0.6, "box": [35, 45, 55, 65]}
            ],
            # 篮子
            [
                {"center": {"x": 25, "y": 15}, "name": "Basket 1", "class": "basket", "confidence": 1.0, "box": [20, 30, 30, 40]},
                {"center": {"x": 35, "y": 10}, "name": "Basket 2", "class": "basket", "confidence": 1.0, "box": [30, 40, 40, 50]}
            ]
        ]

    def test_map_objects(self):
        result = map_objects(self.data_array)

        expected_result = {
            0: [
                {"center": {"x": 10, "y": 30}, "name": "Red Ball 1", "class": "red", "confidence": 0.9, "box": [5, 15, 25, 35]},
                {"center": {"x": 20, "y": 20}, "name": "Red Ball 2", "class": "red", "confidence": 0.8, "box": [15, 25, 35, 45]}
            ],
            1: [
                {"center": {"x": 35, "y": 20}, "name": "Red Ball 3", "class": "red", "confidence": 0.7, "box": [15, 25, 35, 45]},
                {"center": {"x": 40, "y": 15}, "name": "Blue Ball 2", "class": "blue", "confidence": 0.6, "box": [35, 45, 55, 65]},
                {"center": {"x": 30, "y": 10}, "name": "Blue Ball 1", "class": "blue", "confidence": 0.7, "box": [25, 35, 45, 55]}
            ]
        }

        self.assertEqual(result, expected_result)

class TestShowBasket(unittest.TestCase):
    def test_empty_basket(self):
        data_array = {}
        expected_output = {}
        self.assertEqual(showBasket(data_array), expected_output)

    def test_single_item_basket(self):
        data_array = {'篮子1': [{'name': '红色', 'class': '球', 'confidence': 0.9}]}
        expected_output = {'篮子1': 1}
        self.assertEqual(showBasket(data_array), expected_output)

    def test_multiple_items_basket(self):
        data_array = {
            '篮子1': [
                {'name': '红色', 'class': '球', 'confidence': 0.9},
                {'name': '绿色', 'class': '球', 'confidence': 0.8}
            ]
        }
        expected_output = {'篮子1': 2}
        self.assertEqual(showBasket(data_array), expected_output)

    def test_multiple_baskets(self):
        data_array = {
            '篮子1': [
                {'name': '红色', 'class': '球', 'confidence': 0.9}
            ],
            '篮子2': [
                {'name': '绿色', 'class': '球', 'confidence': 0.8},
                {'name': '黄色', 'class': '球', 'confidence': 0.7}
            ]
        }
        expected_output = {'篮子1': 1, '篮子2': 2}
        self.assertEqual(showBasket(data_array), expected_output)

def main(test_case):
    if test_case == "map_objects":
        unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestMapObjects))
    elif test_case == "show_basket":
        unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestShowBasket))
    else:
        print("wuxiaoceshi")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run specific tests.")
    parser.add_argument("test_case", choices=["map_objects", "show_basket"], help="Specify which test case to run")
    args = parser.parse_args()
    
    main(args.test_case)
