from __future__ import annotations
from typing import TypeVar, Generic, List, Sequence
from copy import deepcopy
from functools import partial
from random import uniform, choices
from statistics import mean, pstdev
from dataclasses import dataclass
from data_point import DataPoint


def zscores(original: Sequence[float]) -> List[float]:
    avg: float = mean(original)
    std: float = pstdev(original)
    if std == 0: # return all zeros if there is no variation
        return [0] * len(original)
    return [(x - avg) / std for x in original]


Point = TypeVar('Point', bound=DataPoint)

class KMeans(Generic[Point]):
    @dataclass
    class Cluster:
        points: List[Point]
        centroid: DataPoint

    def __init__(self, k: int, points: List[Point], init:str="k-means++") -> None:
        if k < 1: # k-means can't do negative or zero clusters
            raise ValueError("k must be >= 1")
        self._points: List[Point] = points
        self._zscore_normalize()
        # initialize empty clusters with random centroids
        self._clusters: List[KMeans.Cluster] = []
        if init == "k-means++":
            self._kmeans_plusplus(k)
        else:
            self._random_assign(k)
    
    def _random_assign(self, k:int) -> None:
        for _ in range(k):
            rand_point: DataPoint = self._random_point()
            cluster: KMeans.Cluster = KMeans.Cluster([], rand_point)
            self._clusters.append(cluster)

    def _kmeans_plusplus(self, k:int) -> None:
        sq_distances = [1] * len(self._points)
        for i in range(k):
            if i == 0:
                point: DataPoint = self._random_point()
            else:
                point: DataPoint = choices(self._points, weights=sq_distances, k=1).pop()
            
            cluster: KMeans.Cluster = KMeans.Cluster([], point)
            self._clusters.append(cluster)
            
            fn_distance = partial(DataPoint.distance, point)
            sq_distances = [fn_distance(p)**2 for p in self._points]

    @property
    def _centroids(self) -> List[DataPoint]:
        return [x.centroid for x in self._clusters]

    def _dimension_slice(self, dimension:int) -> List[float]:
        return [p.dimensions[dimension] for p in self._points]

    def _zscore_normalize(self)-> None:
        zscored: List[List[float]] = [[] for _ in range(len(self._points))]
        for dimension in range(self._points[0].num_dimensions):
            dimension_slice: List[float] = self._dimension_slice(dimension)
            for index, zscore in enumerate(zscores(dimension_slice)):
                zscored[index].append(zscore)
        for i in range(len(self._points)):
            self._points[i].dimensions = tuple(zscored[i])

    def _random_point(self) -> DataPoint:
        rand_dimensions: List[float] = []
        for dimension in range(self._points[0].num_dimensions):
            values: List[float] = self._dimension_slice(dimension)
            rand_value: float = uniform(min(values), max(values))
            rand_dimensions.append(rand_value)
        return DataPoint(rand_dimensions)

    def _assign_cluster(self) -> None:
        for point in self._points:
            closest: DataPoint = min(self._centroids, key=partial(DataPoint.distance, point))
            idx: int = self._centroids.index(closest)
            cluster: KMeans.Cluster = self._clusters[idx]
            cluster.points.append(point)

    def _generate_centroids(self) -> None:
        for cluster in self._clusters:
            if len(cluster.points) == 0: # mantem o mesmo centroid se não houver pontos
                continue
            means: List[float] = []
            for dimension in range(cluster.points[0].num_dimensions):
                dimension_slice: List[float] = [
                    p.dimensions[dimension]
                    for p in cluster.points
                ]
                means.append(mean(dimension_slice))
            cluster.centroid = DataPoint(means)

    def run(self, max_iterations:int=100) -> List[KMeans.Cluster]:
        for iteration in range(max_iterations):
            for cluster in self._clusters: # limpa todos os clusters
                cluster.points.clear()
            self._assign_cluster() # encontra o cluster do qual o ponto está mais próximo
            old_centroids: List[DataPoint] = deepcopy(self._centroids)
            self._generate_centroids()
            if old_centroids == self._centroids:
                print(f"Converged after {iteration} iterations")
                return self._clusters
        return self._clusters


if __name__ == '__main__':
    point1: DataPoint = DataPoint([2.0, 1.0, 1.0])
    point2: DataPoint = DataPoint([2.0, 2.0, 5.0])
    point3: DataPoint = DataPoint([3.0, 1.5, 2.5])

    kmeans_test: KMeans[DataPoint] = KMeans(2, [point1, point2, point3])
    test_cluster: List[KMeans.Cluster] = kmeans_test.run()
    for index, cluster in enumerate(test_cluster):
        print(f"Cluster {index}:{cluster.points}")
