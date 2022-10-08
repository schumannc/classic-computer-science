from __future__ import annotations
from data_point import DataPoint
from kmeans import KMeans, zscores
from random import gauss, uniform


def make_blobs(
    n_samples: int = 100,
    n_features: int = 2,
    n_centers: int = 3,
    center_box: tuple[float] = (-10.0, 10.0),
    cluster_std=1.0,
):
    centers: list[DataPoint] = []
    for _ in range(n_centers):
        coords: list[float] = []
        for _ in range(n_features):
            coords.append(uniform(center_box[0], center_box[1]))
        centers.append(DataPoint(coords))

    n_samples_per_center: int = n_samples // n_centers
    points: list[DataPoint] = []
    for i in range(n_centers):
        for _ in range(n_samples_per_center):
            center: DataPoint = centers[i]
            coords: list[float] = []
            for d in range(n_features):
                 coords.append(gauss(center.dimensions[d], cluster_std))
            points.append(DataPoint(coords))
    return points, centers


if __name__ == "__main__":
    points: list[DataPoint] = None 
    centers: list[DataPoint]= None 
    points, centers = make_blobs()


    zscored: List[List[float]] = [[] for _ in range(len(centers))]
    for i in range(centers[0].num_dimensions):
        dimension_slice: list[float] = [
            p.dimensions[i]
            for p in centers
        ]
        for index, zscore in enumerate(zscores(dimension_slice)):
            zscored[index].append(zscore)
    
    for index in range(len(centers)):
        centers[index].dimensions = tuple(zscored[index])

    print("real centers:")
    for center in centers:
        print("\t", center.dimensions)

    print("k-means")
    kmeans: KMeans[Governor] = KMeans(3, points, init=None)
    clusters: list[KMeans.Cluster] = kmeans.run()

    for cluster in clusters:
        print("\t", cluster.centroid)


    print("k-means++")
    kmeans_plusplus: KMeans[Governor] = KMeans(3, points, init="k-means++")
    clusters_plusplus: list[KMeans.Cluster] = kmeans_plusplus.run()

    for cluster in clusters_plusplus:
        print("\t", cluster.centroid)
        


