import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

def features(row):
    return [row['mass_kg'],row['melt'],row['drift']]

def calculate(data):
    archive=data['pool']
    train,held=archive[:-8],archive[-8:]
    scale=StandardScaler().fit([features(row) for row in train])
    knn=NearestNeighbors(n_neighbors=4).fit(scale.transform([features(row) for row in train]))
    def density(rows):
        distances=knn.kneighbors(scale.transform([features(row) for row in rows]))[0]
        return 1/(1+distances.mean(axis=1))
    source=density([data['source']])[0]
    cutoff=np.quantile(density(held),.15)
    return {'density':round(float(source),5),'threshold':round(float(cutoff),5),
            'train':len(train),'held':len(held)}
