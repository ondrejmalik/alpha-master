class HeapPermutationGenerator:
    # zdroje: Chat-GPT
    #         https://en.wikipedia.org/wiki/Heap%27s_algorithm
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self.indices = [0] * self.size
        self.permutation_count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.permutation_count == 0:
            self.permutation_count += 1
            return self.data.copy()

        while self.permutation_count < self.size:
            if self.indices[self.permutation_count] < self.permutation_count:
                if self.permutation_count % 2 == 0:
                    self.data[0], self.data[self.permutation_count] = (
                        self.data[self.permutation_count],
                        self.data[0],
                    )
                else:
                    self.data[
                        self.indices[self.permutation_count]
                    ], self.data[self.permutation_count] = (
                        self.data[self.permutation_count],
                        self.data[self.indices[self.permutation_count]],
                    )
                self.indices[self.permutation_count] += 1
                #print(str(self.indices[self.permutation_count])+ " " + str(self.permutation_count))
                self.permutation_count = 0
                return self.data.copy()
            else:
                self.indices[self.permutation_count] = 0
                self.permutation_count += 1

        return None  # No more permutations
