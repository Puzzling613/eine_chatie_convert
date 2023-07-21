import json
import uuid
from flask import Flask, render_template, request, send_file
import os
try:
	from werkzeug.utils import secure_filename
except:
	from werkzeug import secure_filename
import PtoJ

app = Flask(__name__)
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #파일 업로드 용량 제한 단위:바이트

#에러 핸들러
@app.errorhandler(404)
def page_not_found(error):
     return render_template('page_not_found.html'), 404

#홈 HTML 렌더링
@app.route('/')
def home_page():
	return render_template('home.html')

# 파일 리스트
@app.route('/list')
def list_page():
	file_list = os.listdir("./uploads")
	html = """<center><a href="/">홈페이지</a><br><br>""" 
	html += "file_list: {}".format(file_list) + "</center>"
	return html

#업로드 HTML 렌더링
@app.route('/upload')
def upload_page():
	return render_template('upload.html')

#파일 업로드 처리
@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		#저장할 경로 + 파일명
		f.save('./uploads/' + secure_filename(f.filename))
		return render_template('check.html')

#파일 변환 및 다운로드
@app.route('/convert')
def convert():
    PtoJ.CtoJ("prompt.txt","ChatInfo.json")
    path = "./uploads/" 
    send_file(path + "chatie.json",as_attachment=True)
    return render_template('convert.html')

if __name__ == '__main__':
	#서버 실행
	app.run(host='0.0.0.0', port = 614, debug = True)