import numpy as np

class MyMatrix:
    def __init__(self, value):
        self._check_input(value)
        self.value = value

    @property
    def shape(self):
        return len(self.value), len(self.value[0])
    
    def _check_input(self, value):
        if not all([len(row) == len(value[0]) for row in value]):
            raise ValueError('Invalid matrix shape')
        
    def __add__(self, right):
        if isinstance(right, MyMatrix):
            if self.shape != right.shape:
                raise ValueError(f'Shape a: {self.shape} does not match shape b: {right.shape}')
            result = []
            for i in range(len(self.value)):
                new_row = []
                for j in range(self.shape[1]):
                    new_row.append(self.value[i][j] + right.value[i][j])
                result.append(new_row)

            return MyMatrix(result)
        else: # int/float
            result = []
            for i in range(len(self.value)):
                new_row = []
                for j in range(self.shape[1]):
                    new_row.append(self.value[i][j] + right)
                result.append(new_row)
            
            return MyMatrix(result)
        
    def __mul__(self, right):
        if isinstance(right, MyMatrix):
            if self.shape != right.shape:
                raise ValueError(f'Shape a: {self.shape} does not match shape b: {right.shape}')
            result = []
            for i in range(len(self.value)):
                new_row = []
                for j in range(self.shape[1]):
                    new_row.append(self.value[i][j] * right.value[i][j])
                result.append(new_row)

            return MyMatrix(result)
        else: # int/float
            result = []
            for i in range(len(self.value)):
                new_row = []
                for j in range(self.shape[1]):
                    new_row.append(self.value[i][j] * right)
                result.append(new_row)
            
            return MyMatrix(result)
    
    def __matmul__(self, right):
        if isinstance(right, MyMatrix):
            if self.shape[1] != right.shape[0]:
                raise ValueError(
                    f'Cannot perform matmul between shapes {self.shape} and {right.shape} ({self.shape[1]} != {right.shape[0]})'
                )

            result = []

            for i in range(len(self.value)):
                new_row = []
                for j in range(right.shape[1]):
                    c = 0
                    for k in range(self.shape[1]):
                        c += self.value[i][k]*right.value[k][j]
                    new_row.append(c)
                result.append(new_row)
            
            result = MyMatrix(result)
            
            return result
        else:
            raise ValueError('Operand must be "MyMatrix" instance')
        
    def __str__(self):
        return np.array(self.value).__str__()
    
    def __eq__(self, right):
        return self.value == right.value
    

class HashMixin:
    def __hash__(self):
        """Computes production of matrix's main diagonal elements"""
        n_elements = min(self.shape[0], self.shape[1])
        prod = 1
        for i in range(n_elements):
            prod *= self.value[i][i]
        return prod
    

class HashableMatrix(HashMixin, MyMatrix):
    _cache = {}
    
    @classmethod
    def clear_cache(cls):
        cls._cache = {}

    def __matmul__(self, right):
        if isinstance(right, MyMatrix):
            if self.shape[1] != right.shape[0]:
                raise ValueError(
                    f'Cannot perform matmul between shapes {self.shape} and {right.shape} ({self.shape[1]} != {right.shape[0]})'
                )
            
            mul_hash = hash(self), hash(right)
            if mul_hash not in self._cache:
                result = []

                for i in range(len(self.value)):
                    new_row = []
                    for j in range(right.shape[1]):
                        c = 0
                        for k in range(self.shape[1]):
                            c += self.value[i][k]*right.value[k][j]
                        new_row.append(c)
                    result.append(new_row)
                
                result = HashableMatrix(result)
                self._cache[mul_hash] = result
                
                return result
            return self._cache[mul_hash]
        else:
            raise ValueError('Operand must be "MyMatrix" instance')