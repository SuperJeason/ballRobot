import unittest
from analyzePlace import map_objects

class TestMapObjects(unittest.TestCase):
    def setUp(self):
        self.data_array = [
            [{"center": {"x": 10, "y": 30}, "name": "Red Ball 1", "class": "red", "confidence": 0.9, "box": [5, 15, 25, 35]},
             {"center": {"x": 20, "y": 20}, "name": "Red Ball 2", "class": "red", "confidence": 0.8, "box": [15, 25, 35, 45]}],
            [{"center": {"x": 30, "y": 10}, "name": "Blue Ball 1", "class": "blue", "confidence": 0.7, "box": [25, 35, 45, 55]},
             {"center": {"x": 40, "y": 5}, "name": "Blue Ball 2", "class": "blue", "confidence": 0.6, "box": [35, 45, 55, 65]}],
            [{"center": {"x": 25, "y": 15}, "name": "Basket 1", "class": "basket", "confidence": 1.0, "box": [20, 30, 30, 40]},
             {"center": {"x": 35, "y": 10}, "name": "Basket 2", "class": "basket", "confidence": 1.0, "box": [30, 40, 40, 50]}]
        ]

    def test_map_objects(self):
        # 测试map_objects函数
        result = map_objects(self.data_array)

        # 定义期望的结果
        expected_result = {
            0: [{"center": {"x": 10, "y": 30}, "name": "Red Ball 1", "class": "red", "confidence": 0.9, "box": [5, 15, 25, 35]}],
            1: [{"center": {"x": 20, "y": 20}, "name": "Red Ball 2", "class": "red", "confidence": 0.8, "box": [15, 25, 35, 45]},
                {"center": {"x": 30, "y": 10}, "name": "Blue Ball 1", "class": "blue", "confidence": 0.7, "box": [25, 35, 45, 55]},
                {"center": {"x": 40, "y": 5}, "name": "Blue Ball 2", "class": "blue", "confidence": 0.6, "box": [35, 45, 55, 65]}]
        }

        # 检查结果是否符合预期
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()