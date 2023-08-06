'''helping functions '''
from datetime import datetime, timedelta
import re
import os
import numpy
import cv2

from ..models.model import Patient, patient_schema

YEAR = timedelta(days=365, hours=6)

def get_age(patient_id) -> int:
    ''' calculate age by id of patient'''
    patient = Patient.query.filter_by(id=patient_id).first()
    patient_dict = patient_schema.dump(patient)
    birthday = datetime.strptime(patient_dict['birthday'], '%Y-%m-%d')
    return int((datetime.today() - birthday)/YEAR)

def filename(email: str) -> str:
    ''' generate  name for jpg file based on email
    example: filename("john@face.photo") will return "john_face_photo.jpg" '''
    return re.sub(r"[.@+-]", "_", email) + ".jpg"

def url_for_save(email: str) -> str:
    r''' generate path for jpg file saving. Example:
    url_for_save('john@face.photo')
    will return "micropeutist\static\photo\john_face_photo.jpg" for Windows
    or 'micropeutist/static/photo/john_face_photo.jpg" for linux '''
    return os.path.join('micropeutist_app', 'static', 'photo', filename(email))

def where_is_photo(email: str) -> str:
    ''' generate path to photo siutable for usage in html. Example:
    where_is_photo('john@face.photo') will return '/static/photo/john_face_photo.jpg" '''
    return '/' + 'static' + '/' + 'photo' + '/' + filename(email)

def save_photo(data):
    ''' read bmp, png, jpg, jfif files from data transfered by html form and save it as jpg'''
    npimg = numpy.fromfile(data.get('file'), numpy.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR) # pylint: disable=no-member
    image_name = url_for_save(data.get('email'))
    cv2.imwrite(image_name, image) # pylint: disable=no-member

def delete_photo(email: str) -> None:
    ''' find photo related to email and delete it'''
    url = url_for_save(email)
    if os.path.exists(url):
        os.remove(url)

def parse_request_doctor(request) -> dict:
    ''' parse POST request to doctor data dict '''
    data = {}
    data['id'] = request.form.get("id")
    data['first_name'] = request.form.get("first_name")
    data['last_name'] = request.form.get("last_name")
    data['grade'] = request.form.get("grade")
    data['specialization'] = request.form.get("specialization")
    data['email'] = request.form.get("email")
    data['file'] = request.files.get('file')
    return data

def parse_request_patient(request) -> dict:
    ''' parse POST request to patient data dict '''
    data = {}
    data['id'] = request.form.get("id")
    data['first_name'] = request.form.get("first_name")
    data['last_name'] = request.form.get("last_name")
    data['gender'] = request.form.get("gender")
    data['birthday'] = request.form.get("birthday")
    data['health_state'] = request.form.get("health_state")
    data['email'] = request.form.get("email")
    data['doctor_id'] = request.form.get("doctor_id")
    data['file'] = request.files.get('file')
    return data

def parse_search_criterias(request) -> dict:
    ''' parse GET request to extract filtering criterias'''
    search_criterias = {}
    search_criterias['birthday_since'] = (request.form.get("birthday_since") or "0001-01-01")
    search_criterias['birthday_till'] = (request.form.get("birthday_till") or "9999-12-31")
    search_criterias['doctor_id'] = request.form.get("doctor_id")
    return search_criterias
