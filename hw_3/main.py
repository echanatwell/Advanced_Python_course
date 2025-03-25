import numpy as np
from matrixlib import MyMatrix, HashableMatrix
from matrixlib.numpyMixin import ExtendedArray

if __name__ == '__main__':
    np.random.seed(0)

    a = np.random.randint(0, 10, (10, 10))
    b = np.random.randint(0, 10, (10, 10))

    a_matrix = MyMatrix(a)
    b_matrix = MyMatrix(b)

    ab_sum = a_matrix + b_matrix
    ab_mul = a_matrix * b_matrix
    ab_matmul = a_matrix @ b_matrix

    with open('artifacts/matrix+.txt', 'w') as f:
        f.write(str(ab_sum))
    with open('artifacts/matrix_mul.txt', 'w') as f: # matrix*.txt - invalid filename
        f.write(str(ab_mul))
    with open('artifacts/matrix@.txt', 'w') as f:
        f.write(str(ab_matmul))

    a_mixin = ExtendedArray(a)
    b_mixin = ExtendedArray(b)

    mixin_sum = a_mixin + b_mixin
    mixin_mul = a_mixin * b_mixin
    mixin_matmul = a_mixin @ b_mixin

    mixin_sum.save('artifacts/mixin_matrix+.txt')
    mixin_mul.save('artifacts/mixin_matrix_mul.txt')
    mixin_matmul.save('artifacts/mixin_matrix@.txt')

    A = HashableMatrix([[1, 0],
                        [0, 2]])

    B = D = HashableMatrix([[3, 0],
                            [0, 3]])

    C = HashableMatrix([[2, 0],
                        [0, 1]])

    assert hash(A) == hash(C)
    assert A != C

    with open('artifacts/A.txt', 'w') as f:
        f.write(str(A))
    with open('artifacts/B.txt', 'w') as f:
        f.write(str(B))
    with open('artifacts/C.txt', 'w') as f:
        f.write(str(C))
    with open('artifacts/D.txt', 'w') as f:
        f.write(str(D))
    
    AB = A @ B
    CD = C @ D

    with open('artifacts/hash.txt', 'w') as f:
        f.write(f'{str(hash(AB))} {str(hash(CD))}')

    A = MyMatrix(A.value)
    B = D = MyMatrix(B.value)
    C = MyMatrix(C.value)

    with open('artifacts/AB.txt', 'w') as f:
        f.write(str(A @ B))
    with open('artifacts/CD.txt', 'w') as f:
        f.write(str(C @ D))