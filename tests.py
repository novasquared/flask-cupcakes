from unittest import TestCase

from werkzeug.wrappers import response

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        # "**" means "pass this dictionary as individual named params"
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id'] #TODO: This shouldn't work but our test passed. Why is that?

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    # test wrong id = 404
    def test_update_cupcake_id_not_there(self):
        with app.test_client() as client:
            url = "/api/cupcakes/9999"
            resp = client.patch(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 404)

    # test 0 changes = stays the same
    def test_update_cupcake_id_not_there(self):
        with app.test_client() as client:
            # before db variable
            url = url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.patch(url, json={})
            # after db variable
            # before = after
            data = resp.json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data,{"cupcake":{"id":self.cupcake.id,"flavor":,"size":,"rating":,"image":}})
            # test 1 change
            # test changing all

            # test sending incorrect data input e.g. price

            # url = f"/api/cupcakes/{self.cupcake.id}"
            # resp = client.patch(url, json=CUPCAKE_DATA_2)

            # cupcake = Cupcake.query.get_or_404(self.cupcake.id)


            # self.assertEqual(resp.status_code, 200)

            # data = resp.json

            # # don't know what ID we'll get, make sure it's an int & normalize
            # self.assertIsInstance(data['cupcake']['id'], int)
            # del data['cupcake']['id'] 

            # self.assertEqual(data, {
            #     "cupcake": {
            #         "flavor": "TestFlavor2",
            #         "size": "TestSize2",
            #         "rating": 10,
            #         "image": "http://test.com/cupcake2.jpg"
            #     }
            # })

            # self.assertEqual(Cupcake.query.count(), 2)

            

    def test_delete_cupcake_not_there(self):
        with app.test_client() as client:
            url = "/api/cupcakes/9999"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 404)


    def test_delete_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)

            data = resp.json  

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, {"deleted": self.cupcake.id})
            self.assertEqual(Cupcake.query.count(), 0)