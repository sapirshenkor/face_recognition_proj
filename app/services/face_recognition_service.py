import face_recognition
import numpy as np
from PIL import Image
import io
import os
import uuid



from app import mongo
from app.models import User

def upload_image(file,is_target,username):
    img=Image.open(io.BytesIO(file.read()))
    img_arry=np.array(img)

    face_encodings=face_recognition.face_encodings(img_arry)

    if len(face_encodings)==0:
        return {"error":"No face detected in the image"},400

    filename=str(uuid.uuid4())+'.jpg'
    img.save(os.path.join('uploads',filename))

    user=User.find_by_username(username)

    new_image={
        "filename": filename,
        "user_id": user['_id'],
        "is_target": is_target,
        "encoding": face_encodings[0].tolist()
    }

    result=mongo.db.images.insert_one(new_image)

    return {"msg": "Image uploaded successfuly","id":str(result.inserted_id)}


def recognize_faces(file):
    img=Image.open(io.BytesIO(file.read()))
    img_array=np.array(img)

    face_location=face_recognition.face_locations(img_array)
    face_encodings=face_recognition.face_encodings(img_array,face_location)

    target_images=list(mongo.db.images.find({"is target": True}))
    known_face_encodings=[np.array(img['encoding'])for img in target_images]
    known_face_ids=[str(img['_id'])for img in target_images]

    results = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        image_id = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            image_id = known_face_ids[first_match_index]

        results.append({"image_id": image_id})

    return results