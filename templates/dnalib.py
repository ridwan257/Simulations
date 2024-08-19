from abc import ABC, abstractmethod
from copy import deepcopy
import numpy as np

from lib import shape


class DNA(ABC):
    counter = 0

    def __init__(self, length=1, dtype='S1'):
        self.seq = np.zeros(length, dtype=dtype)
        self.length = self.seq.size
        self.__neucleotide = np.array(['a', 'g', 'c', 't'], dtype=dtype)
        self.fitness = 0

    @property
    def neucleotide(self):
        return self.__neucleotide
    @neucleotide.setter
    def neucleotide(self, txt):
        self.__neucleotide = np.fromstring(txt, dtype='S1')

  
    def get(self):
        return self.seq.tostring().decode('ascii')

    def get_fitness(self):
        return self.f

    def load(self, txt):
        self.seq = np.fromstring(txt, dtype='S1')
        self.length = self.seq.size

    def copy(self, other):
        self.__dict__ = deepcopy(other)

    def random(self,length, p=None):
        if not p:
            self.seq = np.random.choice(self.__neucleotide, length)
        else:
            self.seq = np.random.choice(self.__neucleotide, length, p=p)
        self.length = self.seq.size

    def mutate(self, rate):
        n = round((rate * self.length) / 100)
        indices = np.random.randint(0, self.length, n)
        nts = np.random.choice(self.__neucleotide, n)
        self.seq[indices] = nts
    
    def shuffle(self):
        np.random.shuffle(self.seq)

    @staticmethod
    @abstractmethod
    def cross():
        pass
        # child_dna = DNA()
        # if self.length == other.length:
        #     middle = self.length // 2 if middle == 0 else middle
        #     dna_seq = self.dna[:middle] + other.dna[middle:]
        #     child_dna.load(dna_seq)
        #     child_dna.load_neucleotide(self.__neucleotide)
        # return child_dna

    @abstractmethod
    def phenotype_mapper(self):
        pass










# def to_dna(dna_seq):
#     new_dna = DNA()
#     new_dna.load(dna_seq)
#     return new_dna


# def smart_slice(pops, st_pos=0, init_pos=0):
#     new_arr = []
#     init_pos = len(pops) // 2 if init_pos == 0 else init_pos
#     count = 0
#     for i in range(st_pos, init_pos+1):
#         new_arr.append(pops[i])
#         count += pops[i].dna.f

#     return [new_arr, count]




# def fitness_sort(pops):
#     # this function also returns the total fitness of the population 
#     total_fitness = 0
#     for i in range(len(pops)):
#         total_fitness += pops[i].dna.f
#         lowest_value_index = i
        
#         for j in range(i + 1, len(pops)):
#             if pops[j].dna.f > pops[lowest_value_index].dna.f:
#                 lowest_value_index = j
#         pops[i], pops[lowest_value_index] = pops[lowest_value_index], pops[i]
#     return total_fitness


def random_mates(number_of_parent, total, replace=False):
    weights = np.arange(1, number_of_parent+1, dtype=np.float64)**2
    weights /= np.sum(weights)
    parents = np.arange(0, number_of_parent)
    pairs = np.zeros((total, 2))
    for i in range(total):
        pairs[i,] = np.random.choice(parents, 2, replace=replace, p=weights)

    return pairs.astype(np.int32)

if __name__ == "__main__":
    pass


