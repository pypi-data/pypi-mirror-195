''' CRUD operations '''
from ..config import db
from ..models.model import Doctor, doctor_schema, doctors_schema
from ..models.model import Patient, patient_schema, patients_schema
from .helper import where_is_photo, get_age, delete_photo, save_photo

# ======= DOCTORS ======
def get_doctors() -> list:
    ''' select all records from doctors and add patient count to each record
    return type is list of dicts'''
    doctors = Doctor.query.all()
    doctor_list = doctors_schema.dump(doctors)
    # add to each doctor number of related patients
    for doctor in doctor_list:
        key = doctor["id"]
        doctor["patient_count"] = Patient.query.filter_by(doctor_id = key).count()
    return doctor_list

def create_doctor(data: dict) -> str:
    '''creating new doctor record
    return either "success" or error description '''
    is_exist = Doctor.query.filter_by(email=data.get('email')).first()
    if is_exist:
        return "Error. This email already exist in Doctor records"

    if data.get('file'):
        save_photo(data)

    # creating record
    with db.session() as session:
        new_doctor = Doctor(**data)
        session.add(new_doctor)
        session.commit()
    return "success"

def receive_doctor(tag: str) -> list:
    '''get doctor info by id or by email'''
    # define what is tag and select doctor data
    if tag.isdigit():
        doctor = Doctor.query.filter_by(id=int(tag)).first()
    else:
        doctor = Doctor.query.filter_by(email=tag).first()

    if doctor:
        doctor_dict = doctor_schema.dump(doctor)
        doctor_dict['image_url'] = where_is_photo(doctor_dict.get('email'))

        # add list of related patients
        patients = Patient.query.filter_by(doctor_id=doctor_dict['id']).all()
        if patients:
            doctor_dict["patients"] = patients_schema.dump(patients)

            # add age for each patient
            for patient in doctor_dict["patients"]:
                patient['age'] = get_age(patient['id'])
        return doctor_dict
    return None

def update_doctor(data: dict) -> str:
    '''updating existing doctor record
    return either "success" or error description '''
    if data.get('id'):
        doctor = Doctor.query.filter_by(id=data.get('id')).first()
    else:
        doctor = Doctor.query.filter_by(email=data.get('email')).first()

    if doctor:
        if data.get('file'):
            save_photo(data)

        doctor.first_name = data.get('first_name')
        doctor.last_name = data.get('last_name')
        doctor.grade = data.get('grade')
        doctor.specialization = data.get('specialization')
        doctor.email = data['email']

        db.session.commit()
        return 'success'
    return 'Error. No record with such key'

def delete_doctor(tag: str) -> str:
    '''delete doctor selected by id or by email'''
    # define what is tag and delete doctor data
    if tag.isdigit():
        doctor = Doctor.query.filter_by(id=int(tag)).first()
    else:
        doctor = Doctor.query.filter_by(email=tag).first()

    if doctor:
        email = doctor_schema.dump(doctor).get('email')
        delete_photo(email)
        with db.session() as session:
            session.delete(doctor)
            session.commit()
        return "success"
    return "No such doctor record in the database"

# ====== PATIENTS =======
def get_patients(**criterias: dict) -> list:
    ''' filter records from patients '''
    if not criterias:
        patients = Patient.query.all()
    elif criterias.get('doctor_id'):
        patients = Patient.query.\
            filter(Patient.birthday.between(criterias['birthday_since'],
                                            criterias['birthday_till'])).\
            filter(Patient.doctor_id == criterias['doctor_id']).\
            all()
    else:
        patients = Patient.query.\
            filter(Patient.birthday.between(criterias['birthday_since'],
                                            criterias['birthday_till'])).\
            all()

    patient_list = patients_schema.dump(patients)
    # add patient age and related doctor info
    for patient_dict in patient_list:
        # add age
        patient_dict['age'] = get_age(patient_dict['id'])
        # add related doctor
        doctor = Doctor.query.filter_by(id=patient_dict["doctor_id"]).first()
        if doctor:
            patient_dict["doctor"] = doctor_schema.dump(doctor)
        else:
            patient_dict["doctor"] = None
    return patient_list

def create_patient(data: dict) ->str:
    ''' creating new doctor record
    return either "success" or error description '''
    is_exist = Patient.query.filter_by(email=data.get('email')).first()
    if is_exist:
        return "Error. This email already exist in Patient records"

    if data.get('file'):
        save_photo(data)

    # creating record
    with db.session() as session:
        new_patient = Patient(**data)
        session.add(new_patient)
        session.commit()
    return "success"

def receive_patient(tag: str) -> list:
    '''get patient info by id or by email'''
    # define what is tag and select patient data
    if tag.isdigit():
        patient = Patient.query.filter_by(id=int(tag)).first()
    else:
        patient = Patient.query.filter_by(email=tag).first()

    if patient:
        patient_dict = patient_schema.dump(patient)
        patient_dict['image_url'] = where_is_photo(patient_dict.get('email'))


        # add relative doctor
        doctor = Doctor.query.filter_by(id=patient_dict['doctor_id']).first()
        doctor_dict = doctor_schema.dump(doctor)
        patient_dict['doctor'] = doctor_dict
        return patient_dict
    return None

def update_patient(data: dict) -> str:
    '''updating existing patient record'''
    if data.get('id'):
        patient = Patient.query.filter_by(id=data.get('id')).first()
    else:
        patient = Patient.query.filter_by(email=data.get('email')).first()

    if patient:
        if data.get('file'):
            save_photo(data)

        patient.first_name = data.get('first_name')
        patient.last_name = data.get('last_name')
        patient.gender = data.get('gender')
        patient.birthday = data.get('birthday')
        patient.health_state = data['health_state']
        patient.email = data['email']
        patient.doctor_id = data['doctor_id']
        db.session.commit()
        return 'success'
    return 'Error. No record with such key'

def delete_patient(tag: str) -> str:
    '''delete patient selected by id or by email'''
    # define what is tag and delete doctor data
    if tag.isdigit():
        patient = Patient.query.filter_by(id=int(tag)).first()
    else:
        patient = Patient.query.filter_by(email=tag).first()

    if patient:
        with db.session() as session:
            session.delete(patient)
            session.commit()
        return "success"
    return "No such patient record in the database"
