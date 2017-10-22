# coding:utf8

from math import sqrt

users_item_score = {
    "David": {"Imagine Dragons": 3, "Daft Punk": 5, "Lorde": 4, "Fall Out Boy": 1},
    "Matt": {"Imagine Dragons": 3, "Daft Punk": 4, "Lorde": 4, "Fall Out Boy": 1},
    "Ben": {"Kacey Musgraves": 4, "Imagine Dragons": 3, "Lorde": 3, "Fall Out Boy": 1},
    "Chris": {"Kacey Musgraves": 4, "Imagine Dragons": 4, "Daft Punk": 4, "Lorde": 3, "Fall Out Boy": 1},
    "Tori": {"Kacey Musgraves": 5, "Imagine Dragons": 4, "Daft Punk": 5, "Fall Out Boy": 3}
}


def computeSimilarity(band1, band2, userRatings):
    user_average = {}
    # 求出每一个user评价物品的均值
    for (user, item_scores) in userRatings.items():
        user_average[user] = (
            float(sum(item_scores.values())) / len(item_scores.values())
        )

    print user_average

    num = 0  # 分子
    dem1 = 0  # 分母一部分
    dem2 = 0  # 分母另一部分
    for (user, item_scores) in userRatings.items():
        if band1 in item_scores and band2 in item_scores:
            avg = user_average[user]
            num += (item_scores[band1] - avg) * (item_scores[band2] - avg)
            dem1 += (item_scores[band1] - avg) ** 2
            dem2 += (item_scores[band2] - avg) ** 2
    return num / (sqrt(dem1) * sqrt(dem2))


if __name__ == '__main__':

    print computeSimilarity('Kacey Musgraves', 'Lorde', users_item_score)
    print computeSimilarity('Imagine Dragons', 'Lorde', users_item_score)
    print computeSimilarity('Daft Punk', 'Lorde', users_item_score)
