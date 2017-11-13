# coding:utf8

from collections import OrderedDict

RECORDS = (
    ('10001', '120001', '文艺 爱情'),
    ('10002', '120001', '文艺 青春'),
    ('10003', '120001', '战争 爱情'),
    ('10004', '120001', '战争 亲情'),
    ('10005', '120001', '生活 爱情'),
    ('10006', '120001', '文艺 浪漫'),
    ('10007', '120001', '犯罪 爱情'),
    ('10008', '120001', '犯罪 悬疑'),
    ('10009', '120001', '科幻 惊悚'),
    ('10009', '120001', '文艺 战争'),
    ('10001', '120002', '文艺 爱情'),
    ('10001', '120003', '文艺 青春'),
    ('10001', '120004', '战争 爱情'),
    ('10001', '120005', '战争 亲情'),
    ('10001', '120006', '生活 爱情'),
    ('10001', '120007', '文艺 浪漫'),
    ('10001', '120008', '犯罪 爱情'),
    ('10001', '120009', '犯罪 悬疑'),
    ('10001', '1200010', '科幻 惊悚'),
)
# item_id, user_id, tags


def calculate_item_weight():
    tag_weight = OrderedDict()
    for item_id, user, tags in RECORDS:
        tags = tags.split()
        for tag in tags:
            if (item_id, tag) in tag_weight:
                tag_weight[item_id, tag] += 1
            else:
                tag_weight[item_id, tag] = 1
    return tag_weight


def get_all_user_tag():
    tag_weight = OrderedDict()
    for item_id, user, tags in RECORDS:
        tags = tags.split()
        for tag in tags:
            if (user, tag) in tag_weight:
                tag_weight[user, tag] += 1
            else:
                tag_weight[user, tag] = 1
    return tag_weight


def get_top_user_tags(user_id, limit=5):
    result = []
    user_weight = get_all_user_tag()
    for user_tag, weight in user_weight.items():
        if user_tag[0] == user_id:
            result.append((user_tag[1], weight))
    result = sorted(result, key=lambda tag_weight: tag_weight[1], reverse=True)
    result = [tag for tag, weight in result]
    return result[:limit]


def get_item_tag_weight(user_id, limit=5):
    result = []
    user_weight = get_all_user_tag()
    for user_tag, weight in user_weight.items():
        if user_tag[0] == user_id:
            result.append((user_tag[1], weight))
    result = sorted(result, key=lambda tag_weight: tag_weight[1], reverse=True)
    result = [tag for tag, weight in result]
    return result[:limit]


def get_movie_by_tag(tag_name, count=2):
    result = []
    item_weight = calculate_item_weight()
    for item_tag, weight in item_weight.items():
        if item_tag[1] == tag_name:
            item_id = item_weight[0]
            total_weight = get_item_tag_weight(item_id, type='item')
            if not total_weight:
                continue
            result.append(item_id, weight / total_weight)
    return result[:count]


def recommend_by_tag(user_id, limit=10):
    result = []
    user_tags = get_top_user_tags(user_id=user_id)
    for tag in user_tags:
        items_with_weight = get_movie_by_tag(tag, count=2)
        result.extend(items_with_weight)
    result = sorted(
        result, key=lambda item_weight: item_weight[1], reverse=True)
    result = [item for item, weight in result]
    return result[:limit]


if __name__ == '__main__':
    item_weight = calculate_item_weight(RECORDS)
    user_tags = get_top_user_tags('120001')
    # print item_weight
    print user_tags
    for tag in user_tags:
        print tag
    print '---->>>'
