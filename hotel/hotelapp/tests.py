from django.test import TestCase

# Create your tests here.
class HotelBookingApiTest(TestCase):

    def test_01_post_owner_success(self):
        data = [
            {"name": "willian", "email": "willian1@gmail.com", "password": "pass1"},
            {"name": "Joe", "email": "joe341@gmail.com", "password": "pass2"},
            {"name": "Lancy", "email": "lancy76@gmail.com", "password": "pass3"}
        ]
        for i in data:
            res = self.client.post('/hotelapp/owner/', data=i)
            assert res.status_code == 201
            assert res.json()['name'] == i['name']

    def test_02_post_owner_error(self):
        data = {"name": "willian", "email": "willian1@gmail.com", "password": "pass1"}
        res = self.client.post('/hotelapp/owner/', data=data)
        data = {"name": "Charlie", "email": "willian1@gmail.com", "password": "pass5"}
        res = self.client.post('/hotelapp/owner/', data=data)
        assert res.status_code == 400
        assert b'email already exists' in res.content

    def test_03_post_hotel_success(self):
        data = {"name": "willian", "email": "willian1@gmail.com", "password": "pass1"}
        res = self.client.post('/hotelapp/owner/', data=data)
        data = [
            {"hotel_name": "ABC Hotels", "address": "No:23, North Cross, New York, US", "owner_id": 1},
            {"hotel_name": "Aswins Hotels", "address": "No:23, West Cross, New York, US", "owner_id": 1}
        ]
        for i in data:
            res = self.client.post('/hotelapp/hotel/', data=i)
            assert res.status_code == 201
            assert res.json()['hotel_name'] == i['hotel_name']

    def test_04_post_hotel_error(self):
        data = {"name": "willian", "email": "willian1@gmail.com", "password": "pass1"}
        res = self.client.post('/hotelapp/owner/', data=data)
        res = self.client.post('/hotelapp/hotel/', data={"hotel_name": "ABC Hotels", "address": "No:23, North Cross, New York, US"})
        assert res.status_code == 400
        assert b'This field is required' in res.content

    def test_05_post_room_success(self):
        res = self.client.post('/hotelapp/owner/', data={"name": "willian", "email": "willian1@gmail.com", "password": "pass1"})
        res = self.client.post('/hotelapp/hotel/', data={"hotel_name": "ABC Hotels", "address": "No:23, North Cross, New York, US", "owner_id": 1})
        res = self.client.post('/hotelapp/room/', data={"room_no": "A101", "rent": 2500, "is_occupied": "true", "hotel_id": 1})
        assert res.status_code == 201
        assert res.json()['room_no'] == "A101"

    def test_06_post_room_error(self):
        res = self.client.post('/hotelapp/owner/', data={"name": "willian", "email": "willian1@gmail.com", "password": "pass1"})
        res = self.client.post('/hotelapp/hotel/', data={"hotel_name": "ABC Hotels", "address": "No:23, North Cross, New York, US", "owner_id": 1})
        res = self.client.post('/hotelapp/room/', data={"room_no": "A101", "is_occupied": "true", "hotel_id": 1})
        print(res.content)
        assert res.status_code == 400
        assert b'This field is required' in res.content

    def test_07_get_id_room_success(self):
        res = self.client.post('/hotelapp/owner/', data={"name": "willian", "email": "willian1@gmail.com", "password": "pass1"})
        res = self.client.post('/hotelapp/hotel/', data={"hotel_name": "ABC Hotels", "address": "No:23, North Cross, New York, US", "owner_id": 1})
        res = self.client.post('/hotelapp/room/', data={"room_no": "A101", "rent": 2500, "is_occupied": "true", "hotel_id": 1})
        res = self.client.get('/hotelapp/room/1/')
        assert res.status_code == 200
        assert res.json()['room_no'] == "A101"

    def test_08_get_id_room_error(self):
        res = self.client.post('/hotelapp/owner/', data={"name": "willian", "email": "willian1@gmail.com", "password": "pass1"})
        res = self.client.post('/hotelapp/hotel/', data={"hotel_name": "ABC Hotels", "address": "No:23, North Cross, New York, US", "owner_id": 1})
        res = self.client.post('/hotelapp/room/', data={"room_no": "A101", "rent": 2500, "is_occupied": "true", "hotel_id": 1})
        res = self.client.get('/hotelapp/room/2/')
        assert res.status_code == 404
        assert b'Not found' in res.content
    def test_09_patch_id_room_success(self):
        res = self.client.post('/hotelapp/owner/', data={"name": "willian", "email": "willian1@gmail.com", "password": "pass1"})
        res = self.client.post('/hotelapp/hotel/', data={"hotel_name": "ABC Hotels", "address": "No:23, North Cross, New York, US", "owner_id": 1})
        res = self.client.post('/hotelapp/room/', data={"room_no": "A101", "rent": 2500, "is_occupied": "false", "hotel_id": 1})
        res = self.client.patch('/hotelapp/room/1/', data={"is_occupied": "true"}, content_type="application/json")
        print(res.content)
        assert res.status_code == 200
        assert res.json()['is_occupied'] == 1

    def test_10_patch_id_room_error(self):
        res = self.client.post('/hotelapp/owner/', data={"name": "willian", "email": "willian1@gmail.com", "password": "pass1"})
        res = self.client.post('/hotelapp/hotel/', data={"hotel_name": "ABC Hotels", "address": "No:23, North Cross, New York, US", "owner_id": 1})
        res = self.client.post('/hotelapp/room/', data={"room_no": "A101", "rent": 2500, "is_occupied": "false", "hotel_id": 1})
        res = self.client.patch('/hotelapp/room/2/', data={"is_occupied": "true"}, content_type="application/json")
        assert res.status_code == 404
        assert b'Not found' in res.content

    def test_11_delete_id_room_success(self):
        res = self.client.post('/hotelapp/owner/', data={"name": "willian", "email": "willian1@gmail.com", "password": "pass1"})
        res = self.client.post('/hotelapp/hotel/', data={"hotel_name": "ABC Hotels", "address": "No:23, North Cross, New York, US", "owner_id": 1})
        res = self.client.post('/hotelapp/room/', data={"room_no": "A101", "rent": 2500, "is_occupied": "false", "hotel_id": 1})
        res = self.client.delete('/hotelapp/room/1/')
        print(res.content)
        assert res.status_code == 204

    def test_12_delete_id_room_error(self):
        res = self.client.post('/hotelapp/owner/', data={"name": "willian", "email": "willian1@gmail.com", "password": "pass1"})
        res = self.client.post('/hotelapp/hotel/', data={"hotel_name": "ABC Hotels", "address": "No:23, North Cross, New York, US", "owner_id": 1})
        res = self.client.post('/hotelapp/room/', data={"room_no": "A101", "rent": 2500, "is_occupied": "false", "hotel_id": 1})
        res = self.client.delete('/hotelapp/room/2/')
        assert res.status_code == 404
        assert b'Not found' in res.content
