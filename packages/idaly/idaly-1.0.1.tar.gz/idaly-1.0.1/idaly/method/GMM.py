from sklearn.mixture import GaussianMixture as GMM
import numpy as np


class Gmm(object):
    def __init__(self, num_gen=50, n_components=2):
        self.num_gen = num_gen
        self.n_components = n_components

    def fit(self, samples):
        gmm = GMM(n_components=self.n_components)
        gmm.fit(samples)
        self.synthetic = gmm.sample(self.num_gen)[0]

        return self.synthetic


def gmm_execute(original_data, para):
    gmm = Gmm(num_gen=para[0], n_components=para[1])
    gmm_gen = gmm.fit(original_data)
    return gmm_gen


