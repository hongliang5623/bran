# -*-coding=utf-8 -*-
import sys
import math
from texttable import Texttable
from collections import defaultdict

from util import cos_distance

reload(sys)
sys.setdefaultencoding('utf-8')

MOVIE_DATA_FILE = 'G:\Datas\ml-100k\u.item'
USER_RATING_FILE = 'G:\Datas\ml-100k\u.data'
TARGET_USER_ID = 100


# 算法流程：
# 1、建立电影-用户的倒排表，表示电影被那些用户看过
# 2、从目标用户看过的每一步电影开始遍历
# 3、寻找和目标用户有共同看过电影交集的所有用户作为初始邻居
# 4、对初始邻居里边的每一个邻居，计算和目标用户的余弦夹角相似度
# 5、建立相似度到用户的倒排表，相似度从高到低排列
# 6、根据相似度找出最近k邻居
# 7、从最近k邻看过的所有的电影开始遍历
#  这里的推荐思路是：对于最近k邻居看过的所有电影中的某一电影m
#  如果m仅仅被一个邻居看过，那么目标用户对此电影的的兴趣度就是目标用户和这个邻居的相似度
#  如果m被多个邻居看过，那么目标用户对此电影的相似度为目标用户与这些邻居相似度之和
# 8、建立目标用户兴趣度-电影id的倒排表
# 9、根据兴趣度由大到小进行推荐

# 计算余弦距离
# listUser2Score[2]=[(1,5),(4,2)].... 表示用户2对电影1的评分是5，对电影4的评分是2
# dist = getCosDist(listUser2Score[userId], listUser2Score[neighbor])
def getCosDist(user1_rate_datas, user2_rate_datas):
    # item_id, rate
    sum_x = 0.0
    sum_y = 0.0
    sum_xy = 0.0
    for item1_rate in user1_rate_datas:
        for item2_rate in user2_rate_datas:
            # key1[0]表示电影id，key1[1]表示对电影的评分
            # 如果是两个用户共同评价的一部电影
            if item1_rate[0] == item2_rate[0]:
                sum_x += item1_rate[1] * item1_rate[1]
                sum_y += item2_rate[1] * item2_rate[1]
                sum_xy += item1_rate[1] * item2_rate[1]
    if sum_xy == 0.0:
        return 0
    demo = math.sqrt(sum_x * sum_y)
    dis = sum_xy / demo
    return dis


def getCosDistNew(user1_rate_datas, user2_rate_datas):
    # item_id, rate
    user1_rating = []
    user2_rating = []
    for item1_rate in user1_rate_datas:
        for item2_rate in user2_rate_datas:
            # key1[0]表示电影id，key1[1]表示对电影的评分
            # 如果是两个用户共同评价的一部电影
            if item1_rate[0] == item2_rate[0]:
                user1_rating.append(item1_rate[1])
                user2_rating.append(item2_rate[1])
    if len(user1_rating) <= 2:
        return 0
    dis = cos_distance(user1_rating, user2_rating)
    # print 'user1, user2 mark same movie: %s, distance is: %s' % (len(user1_rating), dis)
    return dis


# 读取文件，读取以行为单位，每一行是列表里的一个元素
def readFile(filename):
    # contents = []
    f = open(filename, "r")
    contents = f.readlines()
    f.close()
    return contents


# 数据格式化为二维数组
def getRatingInfo(ratings):
    rates = []
    for line in ratings:
        rate = line.split("\t")
        #  u.data
        #  user id | item id | rating | timestamp.
        rates.append([int(rate[0]), int(rate[1]), int(rate[2])])
    return rates


# 生成用户评分数据结构
def getUserScoreDataStructure(rates):
    # listUser2Score[2]=[(1,5),(4,2)].... 表示用户2对电影1的评分是5，对电影4的评分是2
    listuser2score = defaultdict(list)
    # dictItem2Users{}, key=item id,value=user id list
    dictitem2users = defaultdict(list)
    for k in rates:
        #  u.data
        #  user id | item id | rating | timestamp.
        user_rank = (k[1], k[2])
        listuser2score[k[0]].append(user_rank)
        dictitem2users[k[1]].append(k[0])
    return listuser2score, dictitem2users


# 计算与目标用户
def getNearestNeighbor(userId, listUser2Score, dictItem2Users):
    neighbors = []
    # listUser2Score[2]=[(1,5),(4,2)].... 表示用户2对电影1的评分是5，对电影4的评分是2
    # 对于目标用户userId的每一个评价过的项目item
    for item in listUser2Score[userId]:
        # dictItem2Users{},key=item id,value=user id list
        # item[0]表示电影id，item[1]表示电影评分
        # dictItem2Users[item[0]]=dictItem2Users[电影id]=value=评价过这个电影的用户列表
        # 从评价过这个电影的用户列表里，计算目标用户和这个列表里边所有用户的相似度
        for neighbor in dictItem2Users[item[0]]:
            # 如果这个邻居不是目标用户并且这个邻居还没有被加入邻居集就加进来
            if neighbor != userId and neighbor not in neighbors:
                neighbors.append(neighbor)
    neighbors_dist = []
    # 存储的是[相似度，邻居id]
    for neighbor in neighbors:
        # listUser2Score[2]=[(1,5),(4,2)].... 表示用户2对电影1的评分是5，对电影4的评分是2
        dist = getCosDistNew(listUser2Score[userId], listUser2Score[neighbor])
        neighbors_dist.append([dist, neighbor])
    # 按照相似度倒排，相似度从道到低
    neighbors_dist.sort(reverse=True)
    return neighbors_dist


# 使用UserFC进行推荐，输入：文件名,用户ID,邻居数量
def recommendByUserFC(userId, listUser2Score, dictItem2Users, k=5):

    # 找出与k个指定user_id最相似的前五个邻居
    neighborsTopK = getNearestNeighbor(userId, listUser2Score, dictItem2Users)[:k]
    # neighborsTopK存储了相似度和邻居id的倒排表
    # 所以neighbor[1]表示邻居id，neighbor[0]表示相似度
    # 这里的推荐思路是：对于最近k邻居看过的所有电影中的某一电影m
    # 如果m仅仅被一个邻居看过，那么目标用户对此电影的的兴趣度就是目标用户和这个邻居的相似度
    # 如果m被多个邻居看过，那么目标用户对此电影的相似度为目标用户与这些邻居相似度之和
    # 建立推荐字典
    recommand_dict = {}
    for neighbor in neighborsTopK:
        neighbor_dist, neighbor_id = neighbor
        # 找出这个邻居看过的所有电影信息
        movie_scores = listUser2Score[neighbor_id]
        for movie_score in movie_scores:
            movie, _ = movie_score
            if movie not in recommand_dict:
                recommand_dict[movie] = neighbor_dist
            else:
                recommand_dict[movie] += neighbor_dist
                # 建立推荐列表
    recommand_list = []
    for movie_id in recommand_dict:
        # 建立目标用户兴趣度-电影id的倒排表
        recommand_list.append([recommand_dict[movie_id], movie_id])
    recommand_list.sort(reverse=True)
    # recommand_list存储的是目标用户兴趣度到电影id的倒排表
    # 所以这里的的k[1]表示的是电影id，k[0]表示的是兴趣度
    recommend_movies = [k[1] for k in recommand_list]
    neighbor_users = [k[1] for k in neighborsTopK]
    return recommend_movies, neighbor_users


# 获取电影的列表
def getMovieList(filename):
    contents = readFile(filename)
    movies_info = {}
    for movie in contents:
        single_info = movie.split("|")
        movies_info[int(single_info[0])] = single_info[1:]
        # print single_info, len(single_info)
    return movies_info


# 获取电影的列表
def getUserRatingData(filename):
    # 读取文件
    contents = readFile(filename)
    # 文件格式数据转化为二维数组
    rates = getRatingInfo(contents)
    # 格式化成字典数据
    listUser2Score, dictItem2Users = getUserScoreDataStructure(rates)
    return listUser2Score, dictItem2Users


def display_user_movie(user_id):
    dictMovieId2Info = getMovieList(MOVIE_DATA_FILE)
    listUser2Score, _ = getUserRatingData(USER_RATING_FILE)
    movie_scores = listUser2Score[user_id]
    for movie, rating in movie_scores:
        movie_title = dictMovieId2Info[movie][0]
        print '---------->>', user_id, movie_title, rating

def confirm_neighbors(user_id1, user_id2):
    print user_id1, user_id2
    dictMovieId2Info = getMovieList(MOVIE_DATA_FILE)
    listUser2Score, _ = getUserRatingData(USER_RATING_FILE)
    u1_movie_scores = listUser2Score[user_id1]
    u2_movie_scores = listUser2Score[user_id2]
    for u1_movie, u1_rating in u1_movie_scores:
        for u2_movie, u2_rating in u2_movie_scores:
            if u1_movie == u2_movie:
                movie_title = dictMovieId2Info[u1_movie][0]
                print 'they both mark movie:%s, and user1_rating:%s, user2_rating:%s' % (
                    movie_title, u1_rating, u2_rating)


if __name__ == '__main__':

    # 获取所有电影的列表,所有电影id到电影名字的键值对
    dictMovieId2Info = getMovieList(MOVIE_DATA_FILE)
    listUser2Score, dictItem2Users = getUserRatingData(USER_RATING_FILE)
    user_movies = [k[0] for k in listUser2Score[TARGET_USER_ID]]
    listRecommendMovieId, neighbors_id = recommendByUserFC(
        TARGET_USER_ID, listUser2Score, dictItem2Users, 80)
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t', 't', 't'])
    table.set_cols_align(["l", "l", "l"])
    rows = []
    rows.append([u"movie name", u"release time", u"from userid"])
    # 打印推荐列表的前20项数据，listRecommendMovieId里边存储的仅仅是id
    for movie_id in listRecommendMovieId[:20]:
        from_user = []
        for user_id in dictItem2Users[movie_id]:
            if user_id in neighbors_id:
                from_user.append(user_id)
                # dictMovieId2Info[movie_id][0]表示电影名 dictMovieId2Info[movie_id][1]表示时间
                movie_title = dictMovieId2Info[movie_id][0]
                create_time = dictMovieId2Info[movie_id][1]
        rows.append([movie_title, create_time, from_user])
    table.add_rows(rows)
    print table.draw()
