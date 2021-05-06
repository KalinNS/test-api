from api import rnd

import pytest
import json

@pytest.fixture(scope="module")
def make_bear_record():
    yield rnd.random_bear()

def match_results(reference:dict, response:dict):
    assert reference['bear_name'].lower() == response['bear_name'].lower()
    assert reference['bear_type'].lower() == response['bear_type'].lower()
    assert float(reference['bear_age']) == float(response['bear_age'])

class TestSmoke:
    def test_create_new_bear(self, client, make_bear_record):
        #01: create new bear
        data = dict(make_bear_record)
        resp = client.create_bear(data)

        assert resp.status_code == 200
        assert resp.text.isdigit()

        result_id = resp.text

        #02: get data for a new bear
        resp = client.read_id(result_id)
        assert resp.status_code == 200

        result_data = json.loads(resp.text)

        assert resp.status_code == 200
        assert len(result_data) == 4

        #04: validate data for a new bear
        match_results(data, result_data)
    
    def test_update_bear_data(self, client, make_bear_record):
        #01: get one of the entries for any bear
        resp = client.read_all()

        assert resp.status_code == 200

        result_data = json.loads(resp.text)
        data = dict(result_data[-1])

        id = data['bear_id']
        
        #02: update data for bear
        reference_data = dict(make_bear_record)
        resp = client.update_bear_id(id, reference_data)
        assert resp.status_code == 200
        assert resp.text == 'OK'

        #03: get new data
        resp = client.read_id(id)

        assert resp.status_code == 200

        result_data = json.loads(resp.text)
        assert len(result_data) == 4

        #04: validate data for a new bear
        match_results(reference_data, result_data) 

    def test_update_bear_data_incorrect_id(self, client, make_bear_record):
        id = 999
        
        #01: update data for bear
        reference_data = dict(make_bear_record)
        resp = client.update_bear_id(id, reference_data)
        assert resp.status_code == 500



    def test_delete_bear(self, client):
        #01: get one of the entries for any bear
        resp = client.read_all()

        assert resp.status_code == 200

        result_data = json.loads(resp.text)
        data = dict(result_data[-1])

        id = data['bear_id']

        #02: delete by id
        resp = client.delete_id(id)   
        assert resp.status_code == 200
        assert resp.text == 'OK'  

        #03: try to get data
        resp = client.read_id(id)

        assert resp.status_code == 200
        assert resp.text == 'EMPTY'  

    def test_double_delete_bear(self, client):
        #01: get one of the entries for any bear
        resp = client.read_all()

        assert resp.status_code == 200

        result_data = json.loads(resp.text)
        data = dict(result_data[-1])

        id = data['bear_id']

        #02: delete by id
        resp = client.delete_id(id)   
        assert resp.status_code == 200
        assert resp.text == 'OK'  

        #03: try to get data
        resp = client.read_id(id)

        assert resp.status_code == 200
        assert resp.text == 'EMPTY'  

        #04: delete by id again
        resp = client.delete_id(id)   
        assert resp.status_code == 200
        assert resp.text == 'OK'  

#test cases for different
#"POLAR", "BROWN", "BLACK", "GUMMY"
    @pytest.mark.parametrize("bear_type, bear_name, bear_age, expected_result", [
        ("POLAR","NAME","10",200),
        ("BROWN","NAME","10.1",200),
        ("BLACK","NAME","10.2",200),
        ("GUMMY","NAME","10.3",200),        
        ("YELLOW","NAME","10.4",500),
        ("BROWN","","10.0",200),
        ("","NAME","10.0",500),
        ("BROWN","NAME","",500),
        ("","","",500),
        ("BROWN","NAME","-10.0",200),
        ("BROWN","NAME","0.0",200),
        ("BROWN","NAME","999",200),
        ("BROWN","NAME","1.11",200),
        ("BROWN","_!@#$RRRSSSsss","10.0",200),
        ("BROWN","МОЖНО ТАК?","10.0",200),
        ("POLAR","NAME","10",200),
        ])

    def test_validate_bear_type(self, client, bear_type, bear_name, bear_age, expected_result):
        #01: create new bear
        data = {"bear_type":bear_type, "bear_name": bear_name,"bear_age": bear_age}  
        resp = client.create_bear(data)

        assert resp.status_code == expected_result
        result_id = resp.text

        #02: get data for a new bear
        if (expected_result == 200):
            resp = client.read_id(result_id)

            print('\n ### Get Res: ' + resp.text)
            assert resp.status_code == 200

            result_data = json.loads(resp.text)
            assert len(result_data) != 0
            
            if (len(result_data) != 0):
                match_results(data, result_data)

    def test_wrong_get_ap(self, client):
        #01: send wrong req
        resp = client.wrong_ap()
        assert resp.status_code == 404


    def post_incomplete_body_no_bear_type(self, client):
        data = {"bear_name": "TEST_NAME","bear_age": 1.1}  
        resp = client.create_bear(data)

        assert resp.status_code == 500

    def post_incomplete_body_no_bear_name(self, client):
        data = {"bear_type": "POLAR","bear_age": 1.1}  
        resp = client.create_bear(data)

        assert resp.status_code == 500

    def post_incomplete_body_no_bear_age(self, client):
        data = {"bear_type": "POLAR","bear_name": "TEST_NAME"}  
        resp = client.create_bear(data)

        assert resp.status_code == 500

    def post_incomplete_body_no_body(self, client):
        data = {}  
        resp = client.create_bear(data)

        assert resp.status_code == 500
    
    def get_wrong_command(self, client):
        resp = client.get_wrong_command('test')

        assert resp.status_code == 404

    def _test_delete_all(self, client):
        #01: get one of the entries for any bear
        resp = client.read_all()

        assert resp.status_code == 200

        result_data = json.loads(resp.text)
        assert len(result_data) != 0

        #02: delete all entries
        resp = client.delete_all()
        assert resp.status_code == 200
        assert resp.text == 'OK'  

        #03: get one of the entries for any bear
        resp = client.read_all()

        assert resp.status_code == 200

        result_data = json.loads(resp.text)
        assert len(result_data) == 0
         
    
  
