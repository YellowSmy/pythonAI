from flask import Flask, render_template, request

from process import _pandas_processI, _pandas_processII
from aiprocess import _ai_process

app = Flask(__name__)

###upload Part

# 업로드 HTML 렌더링
@app.route('/')
def upload_main():
    return render_template('upload.html')

@app.route('/upload2')
def upload_2():
    return render_template('upload2.html')

# 파일 업로드 처리

#upload1
@app.route('/process', methods = ['GET', 'POST'])
def file_process():
    if request.method == 'POST':
        
        ##information upload
        drugName = request.form['drugName']
        shape = request.form['shape']
        color= request.form['color'] 
        drugForm = request.form['drugForm']
        text = request.form['text']
        trust = float(request.form['trust']) #for ai 연동, float change
        
        inputDrugInfo = [text, '', color, '', shape, drugForm]
        
        #processing part
        result = _pandas_processI(drugName, inputDrugInfo)
        url = result[0] #약품 정보 URL
        sideEffect = result[1]

        #ai process
        aiResult = _ai_process(sideEffect, trust)

        return render_template('complete.html', url=url, aiResult=aiResult)
         
        
#upload2
@app.route('/process2', methods = ['GET', 'POST'])
def file_processII():
    if request.method == 'POST':
        
        ##information upload
        shape = request.form['shape']
        color= request.form['color'] 
        dosageForm = request.form['dosageForm']
        divisionLine = request.form['divisionLine']
        text = request.form['text']
        trust = float(request.form['trust']) #for ai 연동, float change
        
        #processing part
        inputDrugInfo = [shape, color, dosageForm, divisionLine, text]
        result = _pandas_processII(inputDrugInfo)
        url = result[0]
        sideEffect = result[1]

        #ai process
        aiResult = _ai_process(sideEffect, trust)
        

        return render_template('complete.html', url=url, aiResult=aiResult)
         
 




if __name__ == '__main__':
    app.secret_key = "wnsdn"
    app.run(debug = True)