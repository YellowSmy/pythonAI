from flask import Flask, render_template, request

from process import _pandas_exchange_processing
from aiprocess import _ai_process

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
        selectRate = request.form['selectRate']
        period = request.form['period'] # 'yyyy-mm-dd ~ yyyy-mm-dd'
        selectTime = request.form['selectTime'] 
        trust = float(request.form['trust']) #ai 연동, float change
        
        # date slicing
        start_date = period[0:10]
        end_date = period[13:23]

        #processing part
        _pandas_exchange_processing(selectRate, start_date, end_date, selectTime)

        #ai process
        result = _ai_process(trust)
        indicate = result[0]
        confidence = result[1]
        reason = result[2]
        return render_template('complete.html', image_file='img/result/exchange.png', indicate=indicate, confidence=confidence, reason=reason)
        
        

        
    
        


if __name__ == '__main__':
    app.secret_key = "wnsdn"
    app.run(debug = True)


