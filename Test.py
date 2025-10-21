import numpy as np
from Layer import Layer
def test_overlay():
    a = Layer(2,2)
    b = Layer(2,2)
    
    a.content = np.array([
        [ [1,10,100], [1,10,100] ],
        [ [1,10,100], [1,10,100] ]
        ])

    b.content = np.array([
        [ [1,10,100], [1,10,100] ],
        [ [1,10,180], [1,10,120] ]
        ])
    
    print(a.normal(b.content))

def test():
    large_array = np.ones((100, 100, 3))
    vector = np.array([0.5, 1.2, 0.8])


    result = np.multiply(large_array, vector)

    print(f"Result shape: {result.shape}")
    print(result)
test()