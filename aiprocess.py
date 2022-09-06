from mlforkids import MLforKidsImageProject

# treat this key like a password and keep it secret!
key = "501df280-2c27-11ed-97fe-07e5aeb69d43c7de2caa-e94e-4c28-bfe4-af5b2a583a9c"
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
    elif(label == 'constant' and confidence >= trust):
        indicate = '유지'
        reason = '적기가 비행궤도를 유지할 것으로 보입니다.'
    elif(confidence < trust):
        indicate = '몰?루'
        reason = '정확도가' + str(trust) + '% 미만입니다. AI 신뢰 한계를 낮추거나 데이터를 추가하세요.'      
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
    elif(label == 'constant' and confidence >= trust):
        indicate = '유지'
        reason = '적기가 속도를 유지할 것으로 보입니다.'
    elif(confidence < trust):
        indicate = '몰?루'
        reason = '정확도가' + str(trust) + '% 미만입니다. AI 신뢰 한계를 낮추거나 데이터를 추가하세요.'       
    else:
        indicate = '감속'
        reason = '적기가 감속 할것으로 예측됨.'

    velocityResult[0] = indicate
    velocityResult[1] = str(round(confidence, 2)) + '%'
    velocityResult[2] = reason

    # console check
    # print(indicateResult)

    return [moveResult, velocityResult]
    
#console    
#print(_ai_process(50))