''' ORM Models '''
from sqlalchemy import ForeignKey, String, Date, Column, Integer
from sqlalchemy.orm import relationship

from ..config import db, ma


# ============== DOCTOR ===============
class Doctor(db.Model): #pylint: disable=too-few-public-methods
    '''class Doctor declares Model Doctor.
    It has attributes: first_name, last_name, grade, specialization, email'''
    __tablename__ = 'doctors'
    id              = Column(Integer, primary_key=True)
    first_name      = Column(String(50), nullable=False)
    last_name       = Column(String(50), nullable=False)
    grade           = Column(String(50))
    specialization  = Column(String(50))
    email           = Column(String(50), unique=True)

    patient = relationship("Patient", back_populates="doctor")

    def __init__(self, **kwargs):
        ''' Doctor object constructor.
        Usage example: new_doctor = Doctor({'first_name': <text>,
        'last_name': <text>, 'grade': <text>,'specialization': <text>, 'email':<text>})'''
        for key in kwargs:
            setattr(self, key, kwargs.get(key))

class DoctorSchema(ma.Schema):
    '''Schema of Doctor class'''
    class Meta: #pylint: disable=missing-class-docstring disable=too-few-public-methods
        fields = ('id', 'first_name', 'last_name', 'grade', 'specialization',
                  'email', 'img_data')


# ========== PATIENT ================
class Patient(db.Model): #pylint: disable=too-few-public-methods
    '''class Patient declares Model Patient.
    It has attributes: first_name, last_name, gender, birthday, health_state, email, doctor_id.
    Attribute doctor_id used as foreign key to Doctor class'''
    __tablename__ = 'patients'
    id              = Column(Integer, primary_key=True)
    first_name      = Column(String(50), nullable=False)
    last_name       = Column(String(50), nullable=False)
    gender          = Column(String(6))
    birthday        = Column(Date)
    health_state    = Column(String(255), nullable=True)
    email           = Column(String(50), unique=True)
    doctor_id       = Column(Integer, ForeignKey("doctors.id"))

    doctor = relationship("Doctor", back_populates="patient")

    def __init__(self, **kwargs):
        ''' Patient object constructor. usage:
        new_patient = Patient(<first_name>, <last_name>, <gender>, <birthday>,
                             <health_state>, <email>, <doctor_id>)'''
        for key in kwargs:
            setattr(self, key, kwargs.get(key))

class PatientSchema(ma.Schema):
    '''Schema of Patient class'''
    class Meta: #pylint: disable=missing-class-docstring disable=too-few-public-methods
        fields = ('id', 'first_name', 'last_name', 'gender','birthday', 'health_state',
                  'email', 'doctor_id')

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)

patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)
