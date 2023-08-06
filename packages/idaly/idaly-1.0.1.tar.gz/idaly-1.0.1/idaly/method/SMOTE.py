import random
from sklearn.neighbors import NearestNeighbors
import numpy as np


class Smote(object):
    def __init__(self, N=100, k=10, r=2):
        self.N = N
        self.k = k
        self.r = r
        self.newindex = 0

    def fit(self, samples):
        T = samples.shape[0]
        numattrs = samples.shape[1]
        self.synthetic = np.zeros((self.N, numattrs))
        neighbors = NearestNeighbors(n_neighbors=self.k + 1,
                                     algorithm='ball_tree',
                                     p=self.r).fit(samples)
        repeats = int(self.N / T)
        yu = self.N % T
        if repeats > 0:
            for i in range(T):
                nnarray = neighbors.kneighbors(samples[i].reshape((1, -1)),
                                               return_distance=False)[0][1:]
                self._populate(repeats, i, nnarray, samples)

        samples_shuffle = samples
        np.random.shuffle(samples_shuffle)
        neighbors_1 = NearestNeighbors(n_neighbors=self.k + 1,
                                       algorithm='ball_tree',
                                       p=self.r).fit(samples_shuffle)
        for j in range(yu):
            nnarray_1 = neighbors_1.kneighbors(samples_shuffle[j].reshape((1, -1)),
                                               return_distance=False)[0][1:]
            self._populate(1, j, nnarray_1, samples_shuffle)
        return self.synthetic

    def _populate(self, N, i, nnarray, samples):
        for j in range(N):
            nn = random.randint(0, self.k - 1)
            diff = samples[nnarray[nn]] - samples[i]
            gap = random.uniform(0, 1)
            self.synthetic[self.newindex] = samples[i] + gap * diff
            self.newindex += 1


def smote_execute(original_data, num_gen, para):
    smote = Smote(N=num_gen, k=para[0], r=2)
    smote_gen = smote.fit(original_data)
    return smote_gen



def main():
    samples = np.array([[3, 1, 2], [4, 3, 3], [1, 3, 4],
                        [3, 3, 2], [2, 2, 1], [1, 4, 3]])

    smote = Smote(N=10, k=3, r=2)

    gen_data = smote.fit(samples)

    print(gen_data)


if __name__ == '__main__':
    main()
