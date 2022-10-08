import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

indicateResult = ['A', 'B', 'C'];



def _ai_process(trust):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = tensorflow.keras.models.load_model('static/model/keras_model.h5')

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open('static/img/result/exchange.jpg')

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)

    
    ## AI PROCESS ##

    if(prediction[0,0] > prediction[0,1]) :
        if(prediction[0,0] > prediction[0,2]) :
            #increase
            confidence = round(prediction[0,0]*100)

            indicate = '상승'
            reason  = '환율이 오를 것으로 예측됩니다.'

            if(confidence < trust):
                indicate = '몰?루'
                reason = '환율이 상승할 것으로 예측되나 정확도가 ' + str(trust) + '% 미만입니다.'
       
        else :
            #constant
            confidence = round(prediction[0,2]*100)

            indicate = '유지'
            reason = '환율이 지금 추세를 유지할 것으로 보입니다.'

            if(confidence < trust):
                indicate = '몰?루'
                reason = '환율이 유지될 것으로 예측되나 정확도가 ' + str(trust) + '% 미만입니다.'

    elif(prediction[0,1] > prediction[0,2]) :
        if(prediction[0,1] > prediction[0,0]) :
            #decrease
            confidence = round(prediction[0,1]*100)

            indicate = '하락'
            reason = '환율이 하락 할 것으로 예측됩니다. 주의하세요!'

            if(confidence < trust):
                indicate = '몰?루'
                reason = '환율이 하락할 것으로 예측되나 정확도가 ' + str(trust) + '% 미만입니다.'
        
        else :
            #increase
            confidence = round(prediction[0,0]*100)

            indicate = '상승'
            reason  = '환율이 오를 것으로 예측됩니다.'
            
            if(confidence < trust):
                indicate = '몰?루'
                reason = '환율이 상승할 것으로 예측되나 정확도가 ' + str(trust) + '% 미만입니다.'
        
    elif(prediction[0,0] < prediction[0,2]) :
        if(prediction[0,2] > prediction[0,1]) :
            #constant
            confidence = round(prediction[0,2]*100)

            indicate = '유지'
            reason = '환율이 지금 추세를 유지할 것으로 보입니다.'

            if(confidence < trust):
                indicate = '몰?루'
                reason = '환율이 유지될 것으로 예측되나 정확도가 ' + str(trust) + '% 미만입니다.'

        else :
            #decrease
            confidence = round(prediction[0,1]*100)

            indicate = '하락'
            reason = '환율이 하락 할 것으로 예측됩니다. 주의하세요!'

            if(confidence < trust):
                indicate = '몰?루'
                reason = '환율이 하락할 것으로 예측되나 정확도가 ' + str(trust) + '% 미만입니다.'

    indicateResult[0] = indicate
    indicateResult[1] = str(confidence) + '%'
    indicateResult[2] = reason
    
    return indicateResult


'''
#console
result = _ai_process(100);
print(result)
'''