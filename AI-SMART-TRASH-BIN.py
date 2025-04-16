# Data training (jarak dan label)
training_data = [
    (5, 'tangan'),
    (6, 'tangan'),
    (7, 'tangan'),
    (15, 'sampah'),
    (18, 'sampah'),
    (19, 'sampah'),
    (30, 'kosong'),
    (32, 'kosong'),
    (35, 'kosong'),
]

def knn_predict(distance):
    min_dist = 999
    label = None
    for data_point in training_data:
        d, l = data_point
        diff = abs(distance - d)
        if diff < min_dist:
            min_dist = diff
            label = l
    return label
