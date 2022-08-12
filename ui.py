from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from process import _pandas_processing
from aiprocess import _ai_process

saveFileName = 'God Save Us'
app = Flask(__name__)

###upload Part

# 업로드 HTML 렌더링
@app.route('/')
def upload_main():
    return render_template('upload.html')

# 파일 업로드 처리
@app.route('/process', methods = ['GET', 'POST'])
def file_process():
    if request.method == 'POST':
        ##information upload
        #excel file upload
        f = request.files['file']
        saveFileName = f.filename
        saveFileName = saveFileName.replace(' ', '_')
        f.save('./static/excel/' + secure_filename(saveFileName))

        trust = float(request.form['trust'])
    
        ##processing part
        _pandas_processing(saveFileName) #pandas
        result = _ai_process(trust) #ai

        moveResult = result[0]
        vResult = result[1]

        return render_template('complete.html', image_file = 'img/result/move.png', image_file2='img/result/velocity.png', moveResult=moveResult, vResult=vResult);
    
        
if __name__ == '__main__':
    app.secret_key = "wnsdn"
    app.run(debug = True)


