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


if __name__ == '__main__':
    user1_score = (5, 5, 5)
    user2_score = (2, 5, 5)
    print cos_distance(user1_score, user2_score)

    v1 = (1, 1)
    v2 = (-1, -1)
    print cos_distance(v1, v2)

    v3 = (1, 2, 2)
    v4 = (2, 4, 4)
    print cos_distance(v3, v4)

