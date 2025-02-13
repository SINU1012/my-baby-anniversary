import os

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

# Flask 인스턴스 생성
app = Flask(__name__)

# --------------------
# 1) 업로드 폴더 설정
# --------------------
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# (선택) 업로드 최대 크기(예: 50MB)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024


# -------------------
# 2) 테스트 라우트
# -------------------
@app.route('/')
def hello_world():
    return "Hello from Flask Upload API!"


# ------------------------
# 3) 업로드 처리 라우트
# ------------------------
@app.route('/upload_images', methods=['POST'])
def upload_images():
    """
    - multipart/form-data로 "images"라는 필드 이름을 사용해 여러 파일을 업로드 받는다.
    - 서버가 uploads/ 폴더에 저장한다.
    - 성공 시, 업로드된 파일 경로 목록을 JSON으로 반환.
    """
    # 3.1) request.files.getlist('images')로 여러 파일을 가져옴
    files = request.files.getlist('images')
    
    # 3.2) 실제 저장 경로 목록
    saved_paths = []
    
    for file in files:
        if file:
            # 안전한 파일 이름 생성(특수문자 제거 등)
            filename = secure_filename(file.filename)
            
            # uploads/ 폴더 내부에 저장
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            
            saved_paths.append(save_path)
    
    # 3.3) 결과 JSON 리턴
    return jsonify({
        "message": "Upload success",
        "uploaded_files": saved_paths
    })


# ----------------------
# 4) 메인 실행 구문
# ----------------------
if __name__ == '__main__':
    # 개발 모드 실행
    app.run(host='0.0.0.0', port=5000, debug=True)
