import numpy as np
array_3d = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                     [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
                     [[19, 20, 21], [22, 23, 24], [25, 26, 27]]])

# Create 3x3 array
array_2d = np.array([[100, 200, 300],
                     [400, 500, 600],
                     [700, 800, 900]])

# Stack along the third axis (axis=2) to create 3x3x4 array
result = np.dstack([array_3d, array_2d[:, :, np.newaxis]])
result = result.reshape(3, 3, 4)
print(result)