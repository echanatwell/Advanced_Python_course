import numpy as np
import numbers

class ArrayLike(np.lib.mixins.NDArrayOperatorsMixin):
    def __init__(self, value):
        self.value = np.asarray(value)

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (ArrayLike, )):
                return NotImplemented
            
        inputs = tuple(x.value if isinstance(x, ArrayLike) else x
                    for x in inputs)
        
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, ArrayLike) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)
        
class ArraLikeExtension:
    def __str__(self):
        return str(self.array)
    
    def save(self, path):
        with open(path, 'w') as f:
            f.write(str(self.array))
    
    @property
    def array(self):
        return self.value
    
    @array.setter
    def array(self, value):
        self.value = np.asarray(value)

class ExtendedArray(ArrayLike, ArraLikeExtension):
    pass