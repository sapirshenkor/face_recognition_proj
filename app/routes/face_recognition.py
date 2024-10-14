
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import upload_image, recognize_faces

bp=Blueprint('face_recognition',__name__)

@bp.route('/upload',methods=['POST'])
@jwt_required()
def upload():
    if 'image' not in request.files:
        return ({"error":"No image file provided"}),400

    file=request.files['image']
    is_target=request.form.get('is_target','false').lower()=='true'
    username=get_jwt_identity()

    result=upload_image(file,is_target,username)
    return jsonify(result),201

@bp.route('/recognize', methods=['POST'])
@jwt_required()
def recognize():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    results = recognize_faces(file)
    return jsonify({"faces": results})