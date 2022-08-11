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
        f.save('./static/excelFile/' + secure_filename(saveFileName))

        #number(limit) upload
        chipLimit = float(request.form['chipLimit'])
        yieldLimit = float(request.form['yieldLimit'])

        #ai trust upload
        trust = float(request.form['trust'])

        #before indicate processing <- process.py
        result = _pandas_processing(saveFileName, chipLimit, yieldLimit);

        ##processing part
        #1st indicate: 수율 너무 낮은 wafer 과반수 이상 시 fail process <- process.py
        if(result == -1):
            result = '양산 실패'; reason = '공정 수율이 수율 한계보다 낮습니다';
            return render_template('complete.html', image_file = 'img/result/PF.png', image_file2='img/result/Yield.png', result=result, reason=reason);
        else:
            #2nd indicate: ai processing으로 증감 판단 <- aiprocess.py
            indicate = _ai_process(trust);
            result = indicate[0]; confidence = indicate[1]; reason = indicate[2];
            return render_template('complete.html', image_file = 'img/result/PF.png', image_file2='img/result/Yield.png', result=result, confidence = confidence, reason = reason);
    
        


if __name__ == '__main__':
    app.secret_key = "wnsdn"
    app.run(debug = True)


