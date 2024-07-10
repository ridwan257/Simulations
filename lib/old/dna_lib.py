import random

class DNA:
    def __init__(self):
        self.dna = "acgt"
        self.length = 4
        self.__neucleotide = "acgt"
        self.f = 0

    def get(self):
        return self.dna

    def get_fitness(self):
        return self.f

    def load_neucleotide(self, txt):
        self.__neucleotide = txt

    def show_neucleotide(self):
        return self.__neucleotide

    def load(self, txt):
        self.dna = txt
        self.length = len(self.dna)

    def copy(self, other):
        self.dna = other.dna
        self.__neucleotide = other.__neucleotide
        self.length = other.length
        self.f = other.f

    def random_dna(self,l):
        self.dna = ""
        for i in range(l):
            ch = random.choice(self.__neucleotide)
            self.dna += ch
        self.length = l

    def cross(self, other, middle=0):
        child_dna = DNA()
        if self.length == other.length:
            middle = self.length // 2 if middle == 0 else middle
            dna_seq = self.dna[:middle] + other.dna[middle:]
            child_dna.load(dna_seq)
            child_dna.load_neucleotide(self.__neucleotide)
        return child_dna

    def fitness(self, func, *args):
        self.f = func(args)
        return self.f

    def mutate(self, rate):
        n = round((rate * self.length) / 100)
        for i in range(n):
            index = random.randint(0,self.length-1)
            nt = random.choice(self.__neucleotide)
            self.dna = self.dna[:index] + nt + self.dna[index+1:]






def to_dna(dna_seq):
    new_dna = DNA()
    new_dna.load(dna_seq)
    return new_dna


def smart_slice(pops, st_pos=0, init_pos=0):
    new_arr = []
    init_pos = len(pops) // 2 if init_pos == 0 else init_pos
    count = 0
    for i in range(st_pos, init_pos+1):
        new_arr.append(pops[i])
        count += pops[i].dna.f

    return [new_arr, count]




def fitness_sort(pops):
    # this function also returns the total fitness of the population 
    total_fitness = 0
    for i in range(len(pops)):
        total_fitness += pops[i].dna.f
        lowest_value_index = i
        
        for j in range(i + 1, len(pops)):
            if pops[j].dna.f > pops[lowest_value_index].dna.f:
                lowest_value_index = j
        pops[i], pops[lowest_value_index] = pops[lowest_value_index], pops[i]
    return total_fitness


def random_mates(pops, total_fitness):
    new_pops = []
    for p in pops:
        n = round((p.dna.f * 100) / total_fitness)
        for i in range(n):
            new_pops.append(p)
    mate1 = random.choice(new_pops)
    mate2 = random.choice(new_pops)
    return (mate1, mate2)


if __name__ == "__main__":
    pass


