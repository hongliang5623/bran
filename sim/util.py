# -*-coding:utf-8-*-


def cos_distance(vector1, vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA * normB) ** 0.5)


# 计算皮尔逊相关度：
def pearson(p, q):
    # 只计算两者共同有的
    same = 0
    for i in p:
        if i in q:
            same +=1

    n = same
    # 分别求p，q的和
    sumx = sum([p[i] for i in range(n)])
    sumy = sum([q[i] for i in range(n)])
    # 分别求出p，q的平方和
    sumxsq = sum([p[i]**2 for i in range(n)])
    sumysq = sum([q[i]**2 for i in range(n)])
    # 求出p，q的乘积和
    sumxy = sum([p[i]*q[i] for i in range(n)])
    # print sumxy
    # 求出pearson相关系数
    up = sumxy - sumx*sumy/n
    down = ((sumxsq - pow(sumxsq,2)/n)*(sumysq - pow(sumysq,2)/n))**.5
    # 若down为零则不能计算，return 0
    if down == 0 :return 0
    r = up/down
    return r


# 计算欧几里德距离：
def euclidean(p,q):
    # 如果两数据集数目不同，计算两者之间都对应有的数
    same = 0
    for i in p:
        if i in q:
            same += 1

    # 计算欧几里德距离,并将其标准化
    e = sum([(p[i] - q[i])**2 for i in range(same)])
    return 1/(1+e**.5)


# 计算曼哈顿距离：
def manhattan(p,q):
    # 只计算两者共同有的
    same = 0
    for i in p:
        if i in q:
            same += 1
    # 计算曼哈顿距离
    n = same
    vals = range(n)
    distance = sum(abs(p[i] - q[i]) for i in vals)
    return distance


# 计算jaccard系数
def jaccard(p, q):
    return 0


if __name__ == '__main__':
    user1_score = (1, 2, 1)
    user2_score = (2, 4, 5)
    print cos_distance(user1_score, user2_score)

    v1 = (1, 1)
    v2 = (-1, -1)
    print cos_distance(v1, v2)

    v3 = (1, 2, 2)
    v4 = (2, 4, 4)
    print cos_distance(v3, v4)
    list1 = [1, 3, 2, 3, 4, 3]
    list2 = [1, 3, 4, 3, 2, 3, 4, 3]
    print pearson(list1, list1)


