import json
import uuid
from flask import Flask, render_template, request, send_file
import os
import pathlib
from werkzeug.utils import secure_filename
import PtoJ

app = Flask(__name__)


# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #파일 업로드 용량 제한 단위:바이트

# 에러 핸들러
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


# 홈 HTML 렌더링
@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        f = request.files['file']
        file_name = f.filename
        prompt = f.read()
        prompt = prompt.decode('utf-8')
        if file_name[-3:] != "txt":
            return render_template('page_not_found.html')
        else:
            PtoJ.ctoj(prompt)
            return send_file("chatie.json", download_name="chatie.json", as_attachment=True)
    return render_template('home.html')


if __name__ == '__main__':
    # 서버 실행
    app.run(host='0.0.0.0', port=614, debug=True)
