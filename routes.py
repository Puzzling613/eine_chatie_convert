import json
import uuid
from flask import Flask, render_template, request, send_file
import os
import pathlib
from werkzeug.utils import secure_filename
from uploads import PtoJ
from uploads import modifyJson

app = Flask(__name__)


# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #파일 업로드 용량 제한 단위:바이트

# 에러 핸들러
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


# 홈 HTML 렌더링
@app.route('/')
def home_page():
    return render_template('home.html')


# 업로드 HTML 렌더링
@app.route('/upload')
def upload_page():
    return render_template('upload.html')


# 파일 업로드 처리
@app.route('/fileUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        file_name = f.filename
        if file_name[-3:] != "txt":
            return render_template('page_not_found.html')
        else:
            f.save('./uploads/' + secure_filename(file_name))
            os.rename('./uploads/' + secure_filename(file_name), "./uploads/prompt.txt")
            return render_template('check.html')


# json 파일 수정
@app.route('/modify')
def modify():
    return render_template("modify.html")


@app.route('/modifyjson', methods=['POST'])
def modify_json():
    if request.method == 'POST':
        title = request.form['title']
        characterstring = request.form['characters']
        characterlist = characterstring.split(",")
        for i in range(0, len(characterlist)):
            characterlist[i] = characterlist[i].strip()
        mainchara = request.form['mainchara']
        modifyJson.modifyjson(title, characterlist, mainchara)
        return render_template("modify.html", title=title, characters=characterstring, mainchara=mainchara)


# 파일 변환 및 다운로드
@app.route('/convert')
def convert():
    prompt_path = pathlib.Path("./uploads/prompt.txt")
    chatinfo_path = pathlib.Path("./uploads/ChatInfo.json")
    if prompt_path.exists() and chatinfo_path.exists():
        path = "./uploads/"
        PtoJ.ctoj(path + "prompt.txt", path + "ChatInfo.json")
        return send_file(path + "chatie.json", download_name="chatie.json", as_attachment=True)
    else:
        return render_template('page_not_found.html')

    # return render_template('convert.html')


if __name__ == '__main__':
    # 서버 실행
    app.run(host='0.0.0.0', port=614, debug=True)
