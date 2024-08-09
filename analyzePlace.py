import json


def classify_objects(data_array, calculate_center=True):
    """
    分类物体为不同类别的数组，并根据需要计算每个物体的中心点。
    :param data_array: 包含物体数据的列表,0是red,1是blue,2是basket
    :param calculate_center: 是否计算物体的中心点
    :return: 包含分类结果的字典
    """
    class_dict = {0: [], 1: [], 2: []}

    for item in data_array:
        class_id = item.get("class")
        if class_id in class_dict:
            # 如果需要计算中心点
            if calculate_center:
                box = item.get("box", {})
                x1 = box.get("x1", 0)
                y1 = box.get("y1", 0)
                x2 = box.get("x2", 0)
                y2 = box.get("y2", 0)

                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2

                item["center"] = {"x": center_x, "y": center_y}

            class_dict[class_id].append(item)

    return class_dict

"""
Args:
    data_array 记录桶物品信息

Returns:
    物体与篮子匹配后的信息

功能：
    匹配物体与篮子

"""
def map_objects(data_array):
    """
    将红色和蓝色球根据篮子的分界线映射到不同的篮子中。
    :param data_array: 包含物体数据的列表。列表的第0项是红色球，第1项是蓝色球，第2项是篮子。
    :return: 包含每个篮子的红色和蓝色球的分类结果的字典。
    """
    # 提取红色球、蓝色球和篮子的列表
    red_dict = data_array[0]
    blue_dict = data_array[1]
    basket_dict = data_array[2]

    # 按 center['x'] 坐标排序
    basket_dict.sort(key=lambda item: item["center"]["x"])
    red_dict.sort(key=lambda item: item["center"]["x"])
    blue_dict.sort(key=lambda item: item["center"]["x"])

    # 计算分界线
    basket_num = len(basket_dict)
    divideLine = []

    for i in range(basket_num - 1):
        divideLine.append(
            (basket_dict[i]["center"]["x"] + basket_dict[i + 1]["center"]["x"]) / 2
        )

    # 创建一个字典以存储每个篮子的红色和蓝色球
    classified_by_basket = {i: [] for i in range(basket_num)}

    # 将红色球分配到不同的篮子中
    for item in red_dict:
        item_x = item["center"]["x"]
        for i in range(basket_num):
            if i == basket_num - 1 or item_x < divideLine[i]:
                classified_by_basket[i].append(item)
                break

    # 将蓝色球分配到不同的篮子中
    for item in blue_dict:
        item_x = item["center"]["x"]
        for i in range(basket_num):
            if i == basket_num - 1 or item_x < divideLine[i]:
                classified_by_basket[i].append(item)
                break

    # y轴朝下，反向排序
    for basket_indexs, items in classified_by_basket.items():
        items.sort(key=lambda item: -item["center"]["y"])

    # for basket_index, items in classified_by_basket.items():
    #     print(f"Basket {basket_index}:")

    #     # 打印球
    #     if items:
    #         for item in items:
    #             print(f"  Name: {item.get('name')}")
    #             print(f"  Class: {item.get('class')}")
    #             print(f"  Center: ({item['center']['x']}, {item['center']['y']})")
    #             print(f"  Confidence: {item.get('confidence')}")
    #             print(f"  Box: {item['box']}")
    #             print()
    #     else:
    #         print("  No balls")
    return classified_by_basket


def save_to_json(data, file_path):
    """
    将数据保存到 JSON 文件中。
    :param data: 要保存的数据
    :param file_path: 文件路径
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def main():
    # 读取 JSON 文件
    with open("resultBall/data.json", "r") as file:
        data_array = json.load(file)

    # 分类物体
    classified_data = classify_objects(data_array)
    # 映射物体
    mapObjectsBall = map_objects(classified_data)

    filePath = "resultBall/data_classified.json"
    save_to_json(mapObjectsBall, file_path=filePath)


if __name__ == "__main__":
    main()
