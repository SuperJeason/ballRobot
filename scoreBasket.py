import json

"""
Args:
    data_array 记录桶物品信息

Returns:
    返回各桶中物品的数量。

功能：
    打印物品信息

"""
def showBasket(data_array):

    # 创建一个新字典，键是篮子的名称，值是每个篮子的物品数量
    basket_item_count = {basket: len(items) for basket, items in data_array.items()}
    print(f"每个篮子的物品数量: {basket_item_count}")

    for basket, items in data_array.items():
        print(f"篮子 {basket} 的物品:")
        for item in items:
            print(
                f"  颜色: {item['name']}, 类别: {item['class']}, 置信度: {item['confidence']}"
            )
    return basket_item_count


"""
Args:
    无

Returns:
    无返回值，函数运行结束后会直接打印游戏胜利或游戏结束。

功能：
    根据读取的 JSON 文件中的数据，判断游戏的胜负情况。
    首先，根据读取的 JSON 文件中的分类数据，统计每个篮子中物品的数量，并将篮子按照物品数量分类。
    然后，遍历有三个物品的篮子，判断其中是否包含至少两个自己阵营的球，并且第三个球也是自己阵营的，如果是，则胜利桶数量加一。
    最后，根据胜利桶的数量判断游戏的胜负情况，如果胜利桶数量大于等于3，则打印"游戏胜利"，否则根据篮子的优先级选择目标篮子。

"""


def main():

    # 定义自己阵营
    myTeam = "red"

    # 读取 JSON 文件
    with open("resultBall/data_classified.json", "r") as file:
        data_array = json.load(file)

    basket_item_count = showBasket(data_array)
    zero_basket = []
    one_basket = []
    two_basket = []
    third_basket = []
    for basket, num in basket_item_count.items():
        if num == 0:
            zero_basket.append(basket)
        elif num == 1:
            one_basket.append(basket)
        elif num == 2:
            two_basket.append(basket)
        else:
            third_basket.append(basket)

    # print(f"有 0 个物品的篮子: {zero_basket}")
    # print(f"有 1 个物品的篮子: {one_basket}")
    # print(f"有 2 个物品的篮子: {two_basket}")
    # print(f"有 3 个物品的篮子: {third_basket}")

    if len(third_basket) == len(basket_item_count):
        print("游戏结束，所有桶已经满了")
    else:
        # 判断胜利桶
        vactory_basket_count = 0
        for basket in third_basket:
            temp_basket = data_array[basket]
            team_ball_count = 0
            for item in temp_basket:
                if item["name"] == myTeam:
                    team_ball_count += 1
            # 大胜桶判断
            if team_ball_count >= 2 and data_array[basket][2]["name"] == myTeam:
                vactory_basket_count += 1
        if vactory_basket_count >= 3:
            print("游戏胜利")
        else:
            # 判断目标篮子
            # 有两个球的篮子优先放该框
            if two_basket.__le__ != 0:
                for basket in two_basket:
                    temp_basket = data_array[basket]
                    for item in temp_basket:
                        target_basket = basket
                        print(f"目标篮子是 {target_basket}")
                        break
            elif zero_basket.__le__ != 0:
                target_basket = zero_basket[0]
                print(f"目标篮子是 {target_basket}")
            elif one_basket.__le__ != 0:
                target_basket = one_basket[0]
                for basket in one_basket:
                    temp_basket = data_array[basket]
                    if temp_basket[0]["class"] == myTeam:
                        target_basket = basket
                        print(f"目标篮子是 {target_basket}")
                        break


if __name__ == "__main__":
    main()
