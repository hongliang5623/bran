# -*-coding:utf-8-*-

import math


class ItemBasedCF:
    def __init__(self, train_file):
        self.train_file = train_file
        self.readData()

    def readData(self):
        # 读取文件，并生成用户-物品的评分表和测试集
        self.records = dict()  # 用户-物品的评分表
        for line in open(self.train_file):
            user, score, item = line.strip().split(",")
            self.records.setdefault(user, {})
            self.records[user][item] = int(float(score))

    def ItemSimilarity(self):
        # 建立物品-物品的同现矩阵
        item_item = dict()  # 物品-物品的共现矩阵
        item_count = dict()  # 电影被多少个不同用户观看
        for user, items in self.records.items():
            for i in items.keys():
                item_count.setdefault(i, 0)
                item_count[i] += 1
                item_item.setdefault(i, {})
                for j in items.keys():
                    if i == j: continue
                    item_item[i].setdefault(j, 0)
                    item_item[i][j] += 1
        # 计算相似度矩阵
        self.sim = dict()
        for i, related_items in item_item.items():
            self.sim.setdefault(i, {})
            for j, cij in related_items.items():
                self.sim[i][j] = cij / (math.sqrt(item_count[i] * item_count[j]))
        return self.sim

    # 给用户user推荐，前K个相似相关物品
    def RecommendByItemFC(self, user, K=3, N=10):
        rec_dict = dict()
        action_item = self.records[user]  # 用户user产生过行为的item和评分
        for item, rating in action_item.items():
            for sim_item, sim_score in sorted(
                    self.sim[item].items(), key=lambda x: x[1], reverse=True)[0:K]:
                if sim_item in action_item.keys():
                    continue
                rec_dict.setdefault(sim_item, 0)
                rec_dict[sim_item] += rating * sim_score
        return sorted(rec_dict.items(), key=lambda x: x[1], reverse=True)[0:N]


# 声明一个ItemBased推荐的对象
Item = ItemBasedCF("G:\Datas\uid_score_bid")
Item.ItemSimilarity()
recommedDic = Item.Recommend("xiyuweilan")
for k, v in recommedDic:
    print k, "\t", v