from micropeutist_app.views.web_view import app

class TestHomeRoute():
    ''' Testing home route'''
    def test_route_home(self):
        responce = app.test_client().get('/')
        assert responce.status_code == 200
        assert b'List of Doctors' in responce.data

class TestDoctorCRUD():
    ''' Testing routes for doctors'''
    def test_route_doctors(self):
        responce = app.test_client().get('/doctors/')
        assert responce.status_code == 200
        assert b'List of Doctors' in responce.data

    def test_route_new_doctor(self):
        responce = app.test_client().get('/new_doctor/')
        assert responce.status_code == 200
        assert b'Creating new doctor record' in responce.data

    def test_route_get_doctor(self):
        responce = app.test_client().get('/doctor/?id=1')
        assert responce.status_code == 200
        assert b'Doctor record' in responce.data

    def test_route_edit_doctor(self):
        responce = app.test_client().get('/edit_doctor/?id=1')
        assert responce.status_code == 200
        assert b'Editing doctor record' in responce.data

    def test_route_remove_doctor(self):
        test_data = {'id': 'notexistedid',}
        responce = app.test_client().post('/remove_doctor/', data=test_data)
        assert responce.status_code == 302
        assert b'redirected' in responce.data

class TestPatientCRUD():
    ''' Testing routes for patients'''
    def test_route_patients(self):
        responce = app.test_client().get('/patients/')
        assert responce.status_code == 200
        assert b'List of Patients' in responce.data

    def test_route_new_patient(self):
        responce = app.test_client().get('/new_patient/?doctor_id=4')
        assert responce.status_code == 200
        assert b'Creating new patient record' in responce.data

    def test_route_get_patient(self):
        responce = app.test_client().get('/patient/?id=1')
        assert responce.status_code == 200
        assert b'Patient record' in responce.data

    def test_route_edit_patient(self):
        responce = app.test_client().get('/edit_patient/?id=1')
        assert responce.status_code == 200
        assert b'Editing patient record' in responce.data

    def test_route_remove_patient(self):
        test_data = {'id': 'notexistedid',}
        responce = app.test_client().post('/remove_patient/', data=test_data)
        assert responce.status_code == 302
        assert b'redirected' in responce.data
