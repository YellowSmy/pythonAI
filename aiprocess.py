from mlforkids import MLforKidsImageProject

# treat this key like a password and keep it secret!
key = "3e7871f0-09a8-11ed-a0b4-7b73eb924b025c485045-7cbe-4e1d-9476-dd2a6b91d346"
moveResult = ['A', 'B', 'C'];
velocityResult = ['A', 'B', 'C'];


def _ai_process(trust):
    # this will train your model and might take a little while
    myproject = MLforKidsImageProject(key)
    myproject.train_model()

    #move
    # CHANGE THIS to the image file you want to recognize
    demo = myproject.prediction("static/img/result/move.png")

    label = demo["class_name"]
    confidence = demo["confidence"]
    #indicate
    #상수함수 = 기동 단조로움, 속도 정보로 방향 indicate
    #상승: 상승 방향 check
    #하강: 하강 방향 check 
    #속도 정보 파악도.. 같이?

    if(label == "increase" and confidence >= trust):
        indicate = '상승'
        reason = '적기가 상승할 것으로 예측됩니다.'
    elif(label == 'increase' and confidence < trust):
        indicate = '(주의)상승'
        reason = '적기가 상승할 것으로 예측되나 정확도가' + str(trust) + '% 미만입니다.'      
    else:
        indicate = '하락'
        reason = '적기가 하강할 것으로 예측됨..'

    moveResult[0] = indicate
    moveResult[1] = str(round(confidence, 2)) + '%'
    moveResult[2] = reason

    #velocity
    velocity = myproject.prediction("static/img/result/move.png")

    Vlabel = velocity["class_name"]
    Vconfidence = velocity["confidence"]

    if(Vlabel == "increase" and Vconfidence >= trust):
        indicate = '가속'
        reason = '적기가 이동 방향으로 가속할 것으로 예상됩니다.'
    elif(Vlabel == 'increase' and Vconfidence < trust):
        indicate = '(주의)가속'
        reason = '적기가 가속할 것으로 예측되나 정확도가' + str(trust) + '% 미만입니다.'      
    else:
        indicate = '감속'
        reason = '적기가 감속 할것으로 예측됨..'

    velocityResult[0] = indicate
    velocityResult[1] = str(round(confidence, 2)) + '%'
    velocityResult[2] = reason

    # console check
    # print(indicateResult)

    return [moveResult, velocityResult]
    
#console    
#print(_ai_process(50))