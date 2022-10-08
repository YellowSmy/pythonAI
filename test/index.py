import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

indicateResult = ['A', 'B', 'C'];

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
# Load the model
model = tensorflow.keras.models.load_model('/workspace/j/tensor/keras_model.h5')
# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array IsADirectoryError
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
# Replace this with the path to your image
image = Image.open('/workspace/j/tensor/dddecrease.jpg')
#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
image = ImageOps.fit(image, size, Image.ANTIALIAS)
#turn the image into a numpy array
image_array = np.asarray(image)
# Normalize the Image
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
# Load the image into the array
data[0] = normalized_image_array
# run the inferencepip i9n

prediction = model.predict(data)

if(prediction[0,0] > prediction[0,1]) :
    if(prediction[0,0] > prediction[0,2]) :
        print("increase")
    else :
        print("constant")

elif(prediction[0,1] > prediction[0,2]) :
    if(prediction[0,1] > prediction[0,0]) :
        print("decrease")
    else :
        print("increase")
    
elif(prediction[0,0] < prediction[0,2]) :
    if(prediction[0,2] > prediction[0,1]) :
        print("constant")
    else :
        print("decrease")



print(prediction)
    

