import numpy as np
import matplotlib.pyplot as plt

# Define the learned filter (weights and biases)
filter = np.array([
    [[-1, -1, 0], [-1, 8, -1], [0, -1, -1]],
    [[-1, -1, -1], [8, -1, -1], [-1, -1, 0]],
    [[0, -1, -1], [-1, -1, 8], [-1, 0, -1]]
])

# Define the input image (a 3x3 matrix)
input_image = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
])

# Deconvolve the input image using the learned filter
def naive_deconvolution(feature_maps, filter):
    # Get the shape of the input data
    input_shape = feature_maps.shape
    
    # Initialize the reconstructed image
    reconstructed_image = np.zeros(input_shape)
    
    # Deconvolve each feature map
    for i in range(feature_maps.shape[0]):
        reconstructed_image += feature_maps[i] * filter
    
    return reconstructed_image

# Deconvolve the input image
deconvolved_image = naive_deconvolution(input_image, filter)

# Visualize the deconvolved image
plt.imshow(deconvolved_image, cmap='gray')
plt.show()

###########################################

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import zoom

# Define the learned filter (weights and biases)
filter = np.array([
    [[-1, -1, 0], [-1, 8, -1], [0, -1, -1]],
    [[-1, -1, -1], [8, -1, -1], [-1, -1, 0]],
    [[0, -1, -1], [-1, -1, 8], [-1, 0, -1]]
])

# Define the input image (a 3x3 matrix)
input_image = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
])

# Deconvolve the input image using upsampling
def upsampling_deconvolution(feature_maps, filter):
    # Get the shape of the input data
    input_shape = feature_maps.shape
    
    # Initialize the reconstructed image
    reconstructed_image = np.zeros((input_shape[0]*2, input_shape[1]*2))
    
    # Upsample the feature maps
    upsampled_feature_maps = zoom(feature_maps, 2, order=0)
    
    # Deconvolve the upsampled feature maps
    for i in range(upsampled_feature_maps.shape[0]):
        reconstructed_image += upsampled_feature_maps[i] * filter
    
    return reconstructed_image

# Deconvolve the input image
deconvolved_image = upsampling_deconvolution(input_image, filter)

# Visualize the deconvolved image
plt.imshow(deconvolved_image, cmap='gray')
plt.show()
