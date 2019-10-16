from django.test import TestCase
import backend.settings.authentication as auth
from django.contrib.auth.models import User

# Create your tests here.
class ServisPeopleTestCase(TestCase):
    def setUp(self):
        adamif = User(username="adamif")
    def test_get_user(self):
        be = auth.MyBackend()
        self.assertEqual(be.get_user("adamif"), 0)
    def test_auth_user(self):
        be = auth.MyBackend()
        self.assertEqual(be.authenticate("adamif", "", 0)
