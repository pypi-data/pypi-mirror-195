''' WEB controller '''
from flask import render_template, redirect, request, flash

from ..service.crud import get_doctors, get_patients, create_doctor, create_patient
from ..service.crud import receive_doctor, receive_patient, update_doctor, update_patient
from ..service.crud import delete_doctor, delete_patient
from ..service.helper import parse_request_doctor, parse_request_patient, parse_search_criterias
from ..config import app

# ========= DOCTORS ==========
@app.route('/')
@app.route('/doctors/')
def doctors():
    '''list of doctors'''
    data = get_doctors()
    app.logger.debug("list of doctors")
    return render_template("doctor_list.html", data=data)

@app.route('/new_doctor/', methods=['GET', 'POST'])
def new_doctor():
    '''add new doctor'''
    if request.method == "POST":
        data = parse_request_doctor(request)
        feedback = create_doctor(data)
        app.logger.debug(f'email = {data.get("email")}. {feedback}')
        if feedback == 'success':
            flash('New doctor record created!',  category='message')
        else:
            flash(feedback, category='error')
        return redirect("/")
    app.logger.debug("method GET. rendering new_doctor.html")
    return render_template("new_doctor.html")

@app.route('/doctor/', methods=['GET'])
def get_doctor():
    '''Show a doctor data by id or by email '''
    doctor_id = request.args.get('id')
    app.logger.debug(f"get doctor. id = {doctor_id}")
    doctor_list = receive_doctor(doctor_id)
    return render_template("doctor.html", data=doctor_list)

@app.route('/edit_doctor/', methods=['GET', 'POST'])
def edit_doctor():
    '''Edit doctor record'''
    # GET
    if request.method == "GET":
        key = request.args.get('id')
        app.logger.debug(f"GET. key = {key}")
        doctor = receive_doctor(key)
        return render_template("edit_doctor.html", data=doctor)
    # POST
    data = parse_request_doctor(request)
    feedback = update_doctor(data)
    app.logger.debug(f"POST. edit doctor {data.get('email')} : {feedback}")
    if feedback == 'success':
        flash('Doctor record updated!',  category='message')
    else:
        flash(feedback, category='error')
    return redirect("/")

@app.route('/remove_doctor/', methods=['POST'])
def remove_doctor():
    ''' deleting doctor record '''
    # key = request.args.get('id') # for GET
    key = request.form.get('id')
    app.logger.debug(f"key = {key}")
    feedback = delete_doctor(key)
    if feedback == 'success':
        app.logger.debug("deleting doctor. flash SUCSESS MESSAGE ")
        flash('Doctor record deleted!',  category='message')
    else:
        app.logger.debug("deleting doctor. flash ERROR MESSAGE ")
        flash(feedback, category='error')
    return redirect("/")

# ========= PATIENTS =======
@app.route('/patients/', methods=['GET', 'POST'])
def patients():
    '''list of patients with search block'''
    # GET. Return whole list of patients
    if request.method == "GET":
        app.logger.debug('whole list')
        return render_template("patient_list.html", patients=get_patients(), doctors=get_doctors())
     # POST. Return filtered list
    search_criterias = parse_search_criterias(request)
    app.logger.debug(
        f"""Filtered list of Patients. :
        birthday_since = {search_criterias.get('birthday_since')}, 
        sbirthday_till = {search_criterias.get('birthday_till')},
        doctor_id = {search_criterias.get('doctor_id')}""")

    return render_template("patient_list.html",
                           patients=get_patients(**search_criterias),
                           doctors=get_doctors())

@app.route('/new_patient/', methods=['GET', 'POST'])
def new_patient():
    ''' creating new patient'''
    if request.method == "GET":
        doctor_id = request.args.get('doctor_id')
        app.logger.debug(f'GET. doctor id ={doctor_id}')
        if doctor_id:
            doctor = receive_doctor(doctor_id)
            return render_template('new_patient.html', doctor=doctor)
        return redirect('/')
    # POST
    data = parse_request_patient(request)
    feedback = create_patient(data)
    app.logger.debug(f'creating patient. {feedback}')
    if feedback == 'success':
        flash('New patient created!',  category='message')
    else:
        flash(feedback, category='error')
    return redirect("/doctor/?id=" + str(data['doctor_id']))

@app.route('/patient/', methods=['GET'])
def patient():
    '''Show a patient data by id or by email'''
    key = request.args.get('id')
    app.logger.debug(f'show patient key ={key}')
    patient_list = receive_patient(key)
    return render_template("patient.html", data=patient_list)

@app.route('/edit_patient/', methods=['GET', 'POST'])
def edit_patient():
    ''' edit patient '''
    if request.method == "GET":
        key = request.args.get('id')
        app.logger.debug(f'GET. key ={key}')
        return render_template("edit_patient.html",
                               data=receive_patient(key),
                               doctors=get_doctors())
    # POST
    data = parse_request_patient(request)
    feedback = update_patient(data)
    app.logger.debug(feedback)
    if feedback == 'success':
        flash('Patient record updated!',  category='message')
    else:
        flash(feedback, category='error')
    return redirect("/patients")

@app.route('/remove_patient/', methods=['POST'])
def remove_patient():
    ''' deleting patiend by id'''
    key = request.form.get('id')
    app.logger.debug(f'key = {key}')
    feedback = delete_patient(key)
    if feedback == "success":
        flash('Patient record deleted', category='message')
    else:
        flash(feedback, category='error')
    return redirect('/patients')
