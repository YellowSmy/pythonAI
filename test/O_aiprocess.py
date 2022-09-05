from test.mlforkids import MLforKidsImageProject

# treat this key like a password and keep it secret!
key = "501df280-2c27-11ed-97fe-07e5aeb69d43c7de2caa-e94e-4c28-bfe4-af5b2a583a9c"
indicateResult = ['A', 'B', 'C'];



def _ai_process(trust):
    # this will train your model and might take a little while
    myproject = MLforKidsImageProject(key)
    myproject.train_model()

    # CHANGE THIS to the image file you want to recognize
    demo = myproject.prediction("static/img/result/exchange.png")

    label = demo["class_name"]
    confidence = demo["confidence"]

    #indicate
    #상수함수 = 유지
    #증가 & 정확도 60% = 상승
    #증가 but 신뢰도 설정값 미만 = 
    #감소 = 감소

    if(label == "increase" and confidence >= trust):
        indicate = '상승'
        reason = '환율이 오를 것으로 예측됩니다.'
    elif(label == 'increase' and confidence < trust):
        indicate = '몰?루'
        reason = '환율이 오를 것으로 예측되나 정확도가' + str(trust) + '% 미만입니다.'
    elif(label == 'constant' and confidence >=trust):
        indicate = '유지'
        reason = '환율이 지금 추세를 유지할 것으로 보입니다.'
    elif(label == 'constant' and confidence < trust):
        indicate = '몰?루'
        reason = '환율이 유지 될 것으로 예측되나 정확도가' + str(trust) + '% 미만입니다.'
    else:
        indicate = '하락'
        reason = '환율이 하락 할 것으로 예측됩니다. 주의하세요!'

    indicateResult[0] = indicate
    indicateResult[1] = str(round(confidence, 2)) + '%'
    indicateResult[2] = reason

    # console check
    # print(indicateResult)

    return indicateResult
    
