''' RESTfull service implementation '''
from flask import jsonify, request

from ..service.crud import get_doctors, create_doctor
from ..service.crud import update_doctor, receive_doctor, delete_doctor
from ..service.crud import get_patients, create_patient
from ..service.crud import update_patient, receive_patient, delete_patient
from ..service.helper import parse_request_doctor, parse_request_patient, parse_search_criterias
from ..config import app


# ========= DOCTORS ========
@app.route('/api/')
@app.route('/api/doctors/')
def api_doctors():
    ''' API to get list of doctors'''
    app.logger.debug('List of doctors')
    return jsonify(get_doctors()), 200

@app.route("/api/create_doctor/", methods=["POST"])
def api_create_doctor():
    '''api for add new doctor'''
    data = parse_request_doctor(request)
    feedback = create_doctor(data)
    app.logger.debug(f'email = {data.get("email")}. {feedback}')
    if feedback == 'success':
        return jsonify(message='Doctor ' + data['last_name'] + ' have been added'), 201
    return jsonify(message=feedback), 409

@app.route('/api/receive_doctor/', methods=['GET'])
def api_receive_doctor():
    '''API to get a doctor data be id or by email
    usage: /api/doctor/?id=<unic id number or unic email>'''
    key = request.args.get('id')
    app.logger.debug(f'key = {key}')
    feedback = receive_doctor(key)
    if feedback:
        app.logger.debug('found')
        return jsonify(feedback), 200
    app.logger.debug('absent')
    return jsonify(message='There is no such doctor in database'), 204

@app.route("/api/update_doctor/", methods=['PUT'])
def api_update_doctor():
    '''API to update a doctor data if email exist in records'''
    data = parse_request_doctor(request)
    feedback = update_doctor(data)
    app.logger.debug(f'key = {data.get("email")}, {feedback}')
    if feedback == 'success':
        return jsonify(message='Doctor ' + data['last_name'] + ' have been updated'), 201
    return jsonify(message=feedback), 409

@app.route("/api/delete_doctor/", methods=["DELETE"])
def api_delete_doctor():
    '''API to delete a doctor data be id or by email
    parameter in body is id=<unic id number or unic email>'''
    key = request.form.get('id')
    feedback = delete_doctor(key)
    app.logger.debug(f'key = {key}, {feedback}')
    if feedback == 'success':
        return jsonify(message='Doctor with id/email = ' + key + ' have been deleted'), 200
    return jsonify(message=feedback), 409

# ======== PATIENTS ==============
@app.route("/api/patients/",  methods=['GET', 'POST'])
def api_patients():
    '''API to get list of patients'''
    # GET. Return whole list of patients
    if request.method == "GET":
        app.logger.debug('Whole list')
        return jsonify(get_patients()), 200
    # POST. Return filtered list
    search_criterias = parse_search_criterias(request)
    app.logger.debug(
        f"""List of Patients. Filters:
        birthday_since = {search_criterias['birthday_since']}, 
        sbirthday_till = {search_criterias['birthday_till']},
        doctor_id = {search_criterias['doctor_id']}""")
    return jsonify(get_patients(**search_criterias)), 200

@app.route('/api/create_patient/', methods=["POST"])
def api_create_patient():
    '''API for creating new patient'''
    data = parse_request_patient(request)
    feedback = create_patient(data)
    app.logger.debug(f'email = {data.get("email")}. {feedback}')
    if feedback == 'success':
        return jsonify(message='Patient ' + data['last_name'] + ' have been added'), 201
    return jsonify(message=feedback), 409

@app.route('/api/receive_patient/', methods=['GET'])
def api_receive_patient():
    '''API to get a patient data be id or by email
    usage: /api/doctor/?id=<unic id number or unic email>'''
    key = request.args.get('id')
    feedback = receive_patient(key)
    if feedback:
        app.logger.debug(f'id = {key}. found')
        return jsonify(feedback), 200
    app.logger.debug(f'id = {key}. absent')
    return jsonify(message='There is no such patient in database'), 204

@app.route('/api/update_patient/', methods=['PUT'])
def api_update_patient():
    '''API for updating existing patient record'''
    data = parse_request_patient(request)
    feedback = update_patient(data)
    app.logger.debug(f'email = {data.get("email")}. {feedback}')
    if feedback == 'success':
        return jsonify(message='Patient ' + data['last_name'] + ' have been updated'), 201
    return jsonify(message=feedback), 409

@app.route('/api/delete_patient/', methods=["DELETE"])
def api_delete_patient():
    '''API for delete patient'''
    key = request.form.get('id')
    feedback = delete_patient(key)
    app.logger.debug(f'key = {key}. {feedback}')
    if feedback == 'success':
        return jsonify(message='PAtient with id/email = ' + key + ' have been deleted'), 200
    return jsonify(message=feedback), 409
