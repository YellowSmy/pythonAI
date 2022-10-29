#ai text 2000자까지 가능!

import requests

# This function will pass your text to the machine learning model
# and return the top result with the highest confidence
def classify(text):
    key = "986e6bf0-1633-11ed-a123-b3ac94355e4e8e751090-2802-4262-b967-ee582719dc6d"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.get(url, params={ "data" : text })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()

def _ai_process(input):
    indicateResult = ['','',''];
    finalResult = [];

    for countI in range(len(input)):
        demo = classify(input[countI])

        label = demo["class_name"]
        confidence = demo["confidence"]

        if(label  == 'safe'):
                indicateResult[0] = '추천'
                indicateResult[1] = str(round(confidence, 2)) + '%'
                indicateResult[2] = '부작용이 낮거나 경미합니다.'

        else:
                indicateResult[0] = '위험'
                indicateResult[1] = str(round(confidence, 2)) + '%'
                indicateResult[2] = '부작용이 치명적입니다. 주의하십시오.'

        finalResult.append(indicateResult)
    
    return finalResult


'''
#console
result = _ai_process(['심장마비', '경미한', '극심한'])
print(result[0][0])
'''