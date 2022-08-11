from mlforkids import MLforKidsImageProject

# treat this key like a password and keep it secret!
key = "3e7871f0-09a8-11ed-a0b4-7b73eb924b025c485045-7cbe-4e1d-9476-dd2a6b91d346"
indicateResult = ['A', 'B', 'C'];



def _ai_process(trust):
    # this will train your model and might take a little while
    myproject = MLforKidsImageProject(key)
    myproject.train_model()

    # CHANGE THIS to the image file you want to recognize
    demo = myproject.prediction("static/img/result/Yield.png")

    label = demo["class_name"]
    confidence = demo["confidence"]

    #indicate
    #상수함수 = 안정적 양산 가능 #일정 수율 미만 상수함수는 process.py의 1st indicate 에서 처리
    #증가 & 정확도 60% = 양산 가능
    #증가 but 정확도 60% 미만 = 위험
    #감소 = 양산 불가

    if(label == "increase" and confidence >= trust):
        indicate = '양산 가능'
        reason = '수율이 증가하고 있습니다.'
    elif(label == 'increase' and confidence < trust):
        indicate = '위험'
        reason = '수율이 증가하나 AI판단의 정확도가 60% 미만입니다.'
    else:
        indicate = '양산 불가'
        reason = '수율이 감소하고 있습니다.'

    indicateResult[0] = indicate
    indicateResult[1] = str(round(confidence, 2)) + '%'
    indicateResult[2] = reason

    # console check
    # print(indicateResult)

    return indicateResult
    
