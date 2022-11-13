from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from process import _pandas_processing
from aiprocess import _ai_process

saveFileName = ''
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

        A = int(request.form['A']);
        B = int(request.form['B']);
        C = int(request.form['C']);
        D = int(request.form['D']);
        E = int(request.form['E']);

        input = [A, B, C, D, E];
        trust = float(request.form['trust'])

        ##processing part
        _pandas_processing(input);
        result = _ai_process(trust) #ai

        print(result,input);

        return render_template('complete.html', image_file='img/result/LRresult.png', Result=result);
    
        
if __name__ == '__main__':
    app.secret_key = "wnsdn"
    app.run(debug = True)


