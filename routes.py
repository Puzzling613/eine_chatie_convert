import json
import uuid
from flask import Flask, Response, render_template, request, send_file
import os
import pathlib
from werkzeug.utils import secure_filename
import Converter

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

        if file_name[-4:] == "json":
            messages = json.loads(f.read().decode('utf-8'))
            conversation_file = Converter.json2text(messages)
            return Response(conversation_file, content_type='text/plain', headers={'Content-Disposition': 'attachment; filename=conversation.txt'})
        elif file_name[-3:] == "txt":
            text = f.read()
            text = text.decode('utf-8')
            chatie_file = Converter.text2json(text)
            return Response(chatie_file, content_type='application/json', headers={'Content-Disposition': 'attachment; filename=chatie.json'})

        else:
            return render_template("page_not_found.html")
    return render_template('home.html')


if __name__ == '__main__':
    # 서버 실행
    app.run(host='0.0.0.0', port=614, debug=True)
