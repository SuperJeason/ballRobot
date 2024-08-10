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
    返回目标target篮子,以及权重

功能：
    根据读取的 JSON 文件中的数据，判断游戏的胜负情况。
    首先，根据读取的 JSON 文件中的分类数据，统计每个篮子中物品的数量，并将篮子按照物品数量分类。
    然后，遍历有三个物品的篮子，判断其中是否包含至少两个自己阵营的球，并且第三个球也是自己阵营的，如果是，则胜利桶数量加一。
    最后，根据胜利桶的数量判断游戏的胜负情况，如果胜利桶数量大于等于3，则打印"游戏胜利"，否则根据篮子的优先级选择目标篮子。

"""


def find_victory_basket(data_array, third_basket, myTeam):
    victory_basket_count = 0
    for basket in third_basket:
        temp_basket = data_array[basket]
        team_ball_count = sum(item["name"] == myTeam for item in temp_basket)
        if team_ball_count >= 2 and temp_basket[2]["name"] == myTeam:
            victory_basket_count += 1
    return victory_basket_count


def calculate_target(
    basket_lists, level, ball_data, myTeam, victory_basket_count, baskets_by_count
):
    """
    根据给定的篮子列表、等级和球数据计算目标值。

    Args:
        basket_list (list): 这里传进来的是目标篮子列表。(从这几种选一个)
        level (int): 等级，取值范围为0, 1, 2。
        ball_data (dict): 这里是球与篮子的映射关系。

    Returns:
        返回最终选择结果，以及优先级。

    Raises:
        ValueError: 如果传入的等级未定义（不在 1, 2, 3 范围内）。

    """

    def handle_level_0():
        # 选择没有球的篮子
        return basket_lists[0], 3

    def handle_level_1():
        # 只有一个球，挑选本方球
        for l in basket_lists:
            if ball_data[l][0]["name"] == myTeam:
                return l, 2
        # 只有一个球，挑选对方球
        return basket_lists[0], 1

    def handle_level_2():
        # 有两个球的篮子，有三种情况
        # 1. 两个球都是本方
        # 2. 两个球都是对方
        # 3. 一个球是本方，一个球是对方
        baskets = {1: [], 2: [], 3: []}
        for l in basket_lists:
            if ball_data[l][0]["name"] == myTeam and ball_data[l][1]["name"] == myTeam:
                baskets[1].append(l)
            elif (
                ball_data[l][0]["name"] != myTeam and ball_data[l][1]["name"] != myTeam
            ):
                baskets[2].append(l)
            else:
                baskets[3].append(l)
        # 如果本方大胜桶少于对方，优先放置至少一个球是对方的桶
        if 2 * victory_basket_count < len(baskets_by_count[3]):
            if baskets[3]:
                return baskets[3][0], 5
            elif baskets[2]:
                return baskets[2][0], 4
            else:
                return baskets[1][0], 4
        else:
            if baskets[3]:
                return baskets[3][0], 5
            elif baskets[1]:
                return baskets[1][0], 4
            else:
                return baskets[2][0], 4

    actions = {0: handle_level_0, 1: handle_level_1, 2: handle_level_2}
    action = actions.get(level)
    if action:
        return action()
    else:
        raise ValueError(f"未定义的 level: {level}")


def choose_target_basket(data_array, basket_item_count, myTeam):
    baskets_by_count = {0: [], 1: [], 2: [], 3: []}

    # 分类篮子数量
    for basket, num in basket_item_count.items():
        if num in baskets_by_count:
            baskets_by_count[num].append(basket)

    if len(baskets_by_count[3]) == len(basket_item_count):
        print("游戏结束，所有桶已经满了")
        return 5, 10

    # 检查是否有胜利条件
    victory_basket_count = find_victory_basket(data_array, baskets_by_count[3], myTeam)
    if victory_basket_count >= 3:
        print("游戏胜利")
        return 5, 9

    # 选择目标篮子
    # 优先级: 2 -> 0 -> 1
    if baskets_by_count[2]:
        target_basket, priority = calculate_target(
            basket_lists=baskets_by_count[2],
            level=2,
            ball_data=data_array,
            myTeam=myTeam,
            victory_basket_count=victory_basket_count,
            baskets_by_count=baskets_by_count,
        )
    elif baskets_by_count[0]:
        target_basket, priority = calculate_target(
            basket_lists=baskets_by_count[0],
            level=0,
            ball_data=data_array,
            myTeam=myTeam,
            victory_basket_count=victory_basket_count,
            baskets_by_count=baskets_by_count,
        )
    elif baskets_by_count[1]:
        target_basket, priority = calculate_target(
            basket_lists=baskets_by_count[1],
            level=1,
            ball_data=data_array,
            myTeam=myTeam,
            victory_basket_count=victory_basket_count,
            baskets_by_count=baskets_by_count,
        )
    else:
        target_basket = 5
        priority = 10
    return target_basket, priority


def main():

    # 定义自己阵营
    myTeam = "red"

    # 读取 JSON 文件
    with open("resultBall/data_classified.json", "r") as file:
        data_array = json.load(file)

    basket_item_count = showBasket(data_array)
    task_id, priority = choose_target_basket(data_array, basket_item_count, myTeam)
    print(f"篮子 ID: {task_id}, 优先级: {priority}")

if __name__ == "__main__":
    main()
