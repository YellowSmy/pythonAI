from flask import Flask, render_template, request
from process import process
from aiprocess import _ai_process

app = Flask(__name__)

###upload Part

# 업로드 HTML 렌더링
@app.route('/')
def upload_main():
    return render_template('upload.html')

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
    
        #pandas process
        inputDrugInfo = [shape, color, drugForm, text];
        result = process(drugName, inputDrugInfo)
        url = result[0];
        sideEffect = result[1];
        
        #ai process
        aiResult = _ai_process(sideEffect)
        length = len(aiResult)

        return render_template('complete.html', url=url, aiResult=aiResult, length=length)
         
 


if __name__ == '__main__':
    app.secret_key = "wnsdn"
    app.run(debug = True)