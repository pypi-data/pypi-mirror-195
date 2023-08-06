from micropeutist_app.rest.api_view import app

class TestApiGetPatients():
    ''' Testing route /api/patients/'''
    def test_get_api_patients(self):
        responce = app.test_client().get('/api/patients/')
        assert responce.status_code == 200

class TestApiPatientCRUD():
    ''' testing CRUP operations by API'''
    test_data = dict(first_name='Pedro', last_name='Sanches', gender='male', birthday='1333-08-15', email='test@email.com')
    filter_date = dict(birthday_since='1333-08-15', birthday_till='1333-08-15')
    update_data = dict(first_name='Rodrigo', last_name='Sanches', gender='male', birthday='2000-01-01', email='test@email.com')
    notexist_data = dict(first_name='a', last_name='b', gender='c', birthday='2000-01-01', email='no@email.com')
    
    # delete record with test data if exist
    app.test_client().delete('/api/delete_patient/', data={'id': test_data['email']})
    
    def test_api_create_patient(self):
        responce = app.test_client().post('/api/create_patient/',data=self.test_data)
        assert responce.status_code == 201
        assert b'have been added' in responce.data

    def test_api_create_patient_duble(self):
        responce = app.test_client().post('/api/create_patient/',data=self.test_data)
        assert responce.status_code == 409
        assert b'Error. This email already exist in Patient records' in responce.data

    def test_api_patient_filter_by_date(self):
        responce = app.test_client().post('/api/patients/', data=self.filter_date)
        assert responce.status_code == 200
        assert b'Sanches' in responce.data
        assert b'specialization' not in responce.data

    def test_api_receive_patient_by_email(self):
        responce = app.test_client().get('/api/receive_patient/?id=test@email.com')
        assert responce.status_code == 200  
        assert b'Sanches' in responce.data

    def test_api_receive_patient_by_id(self):
        responce = app.test_client().get('/api/receive_patient/?id=test@email.com')
        id = responce.get_json().get('id')
        responce = app.test_client().get('/api/receive_patient/?id=' + str(id))
        assert responce.status_code == 200  
        assert b'Sanches' in responce.data

    def test_api_update_patient(self):
        responce = app.test_client().put('/api/update_patient/', data=self.update_data)
        assert responce.status_code == 201
        assert b'have been updated' in responce.data

    def test_api_update_patient_not_existing(self):
        responce = app.test_client().put('/api/update_patient/', data=self.notexist_data)
        assert responce.status_code == 409
        assert b'Error. No record with such key' in responce.data

    def test_api_delete_patient(self):
        responce = app.test_client().delete('/api/delete_patient/', data={'id': self.test_data['email']})
        assert responce.status_code == 200
        assert b'have been deleted' in responce.data

    def test_api_delete_patient_not_existing(self):
        responce = app.test_client().delete('/api/delete_patient/', data={'id': self.notexist_data['email']})
        assert responce.status_code == 409
        assert b'No such patient record in the database' in responce.data
