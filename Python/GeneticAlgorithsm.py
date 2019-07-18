# Genetic Algorithm 基因算法

# 父代： 生成一个24位的二进制数
# 通过crossover, mutation操作后生成子代

# crossover： 父母最后两位数交换；  产生 子代1 和子代2
# mutation: 对子代最后一位数进行处理; 0 --> 1, 1 --> 0； 产生 子代3 子代4

# 在子代中找到最优的两个： 二进制转换成十进制，数字大的入选。
# 最优的两个子代作为新的父母， 经过同样的操作生成下一代 .......


# 在博弈论中的运用： 重复博弈， 找到最优策略 --> 我们称作纳什均衡（Nash equilibrium）
# 假设两个玩家， player 1 和 player 2

#                    p2
#             合作       背叛
#     合作  （6， 6）  （0， 8）
#  p1
#     背叛  （8， 0）  （3 ，3） <-- 这个例子里，博弈只进行一次，它是纳什均衡


# 加入基因算法：
# 假设很多个玩家，每个人都由24位的二进制数表示，1 表示背叛， 0 表示合作
# 24位： 游戏进行24次，每位玩家的payoff分别累加
# 24次结束后， payoff最高的两位成为父代，生成下一代娃
# 娃之间重复以上操作， 选出最高的两位成为父代
# .......(循环)
# 期望看到的结果： 玩家的策略（由24位的二进制数表示）会逐渐向 1111 1111 1111 1111 1111 1111 收敛


import random

# 设置初始的父代，随机生成两个24位的二进制数
def set_player():
    player = bin(random.randint(8388608, 16777215))
    print(player)
    # print(len(str(player)))
    # print(type(player))

    return player


# 进行crossover 操作，最后两位交换位置
def cross_over(player1, player2):
    print('------------------------------')
    print('cross_over 被调用了')
    p1 = str(player1)[24:]
    p2 = str(player2)[24:]
    print(p1)
    print(p2)
    new_p1 = str(player1[:23]) + str(player2[23:])
    new_p2 = str(player2[:23]) + str(player1[23:])
    return new_p1, new_p2

# 进行变异操作：子代的最后一位 0变1 1变0
def mutation(player):
    print('------------------------------')
    print('mutation 被调用了')
    if str(player)[-1] == '1':
        player = str(player)[:25] + str(0)

    else:
        player = str(player)[:25] + str(1)
    print(player)
    return player

# 产生下一代的函数， 会调用cross_over和mutation
def next_genertion(player1, player2):
    print('------------------------------')
    print('next_generation 被调用了')
    player1, player2 = cross_over(player1, player2)
    print('p1 is: {}'.format(player1))
    print('p2 is: {}'.format(player2))

    player3 = mutation(player1)
    player4 = mutation(player2)
    print('p3 is: {}'.format(player3))
    print('p4 is: {}'.format(player4))
    return player1, player2, player3, player4

# 计算子代的payoff； 传入子代1和子代2的二进制数和payoff
# 返回他俩的payoff / value
def value_accumulation(p1_value, player1, p2_value, player2):

    print('value_accumulation被调用了')

    player1 = int(player1, 2)
    player2 = int(player2, 2)

    result = player1 & player2
    for i in str(result):
        if i == '1':
            p1_value += 6
            p2_value += 6

    digit = 2
    for x in str(player1)[2:]:
        if x == 0 and str(player2)[digit] == 0:
            p1_value += 3
            p2_value += 3

        if x == 0 and str(player2)[digit] == 1:
            p1_value += 0
            p2_value += 8

        if x == 1 and str(player2)[digit] == 0:
            p1_value += 8
            p2_value += 0

        digit += 1
    return p1_value, p2_value

# 让四个子代互相进行游戏，调用上面的函数，返回一个字典（储存四个娃的二进制数串和payoff）
def cal_value(p1, p2, p3, p4):
    print('------------------------------')
    print('cal_value 被调用了')
    p1_v = p2_v = p3_v = p4_v = 0
    p1_v, p2_v = value_accumulation(p1_v, p1, p2_v, p2)
    # print(p1_v)
    p1_v, p3_v = value_accumulation(p1_v, p1, p3_v, p3)
    # print(p1_v)
    p1_v, p4_v = value_accumulation(p1_v, p1, p4_v, p4)
    # print(p1_v)

    p2_v, p3_v = value_accumulation(p2_v, p2, p3_v, p3)
    p2_v, p4_v = value_accumulation(p2_v, p2, p4_v, p4)

    p3_v, p4_v = value_accumulation(p3_v, p3, p4_v, p4)
    print(p1_v)
    print(p2_v)
    print(p3_v)
    print(p4_v)
    value_dict = {p1: p1_v, p2: p2_v, p3: p3_v, p4: p4_v}
    # return p1_v, p2_v, p3_v, p4_v
    return value_dict

# 传入上面的字典，得出新的爸爸们
# 返回最优的两个
def get_parents(value_dict):
    print('------------------------------')
    print('get_parents被调用了')
    value_list = sorted(value_dict.items(), key=lambda e: e[1], reverse=True)
    print(value_list)

    return value_list[0][0], value_list[1][0]




# player1 = set_player()
# player2 = set_player()
# print('p1 is: {}'.format(player1))
# print('p2 is: {}'.format(player2))


# 主程序： 先设置第一代爸妈，再调用do_action
def do_action(parent1, parent2):

    p1, p2, p3, p4 = next_genertion(parent1, parent2)
    value_dict = cal_value(p1, p2, p3, p4)
    parent1, parent2 = get_parents(value_dict)
    print('-----运行结束-----')
    print('parent1: {}'.format(int(parent1, 2)))
    print('parent2: {}'.format(int(parent2, 2)))
    return parent1, parent2


# 手动操作： 我用来debug的
p1 = set_player()
p2 = set_player()
print('p1 is: {}'.format(p1))
print('p2 is: {}'.format(p2))
p3, p4 = do_action(p1, p2)
p5, p6 = do_action(p3, p4)
p7, p8 = do_action(p5, p6)


# 一个自动调用的循环
# count = 0

# def main(p1, p2):
#     global count
#     if count < 3:
#         count += 1
#         # 第一次调用do_action，用生成的p1, p2
#         p3, p4 = do_action(p1, p2)
#         print(p3, p4)
#         # 第二次调用do_action,用上一次生成的parent1 parent2
#         main(p3, p4)
#
#     # .....依次循环n次.....
#
# count = 0
# main(p1,p2)



# a = bin(10000002)
# print(a)
# print(len(str(a)))

# a = str(100000000000000000000000)  # 24位二进制
# b = str(111111111111111111111111)  # 24位二进制
# print(int(a, 2))
# print(int(b, 2))
# print(len(str(a)))
# print(len(str(b)))
