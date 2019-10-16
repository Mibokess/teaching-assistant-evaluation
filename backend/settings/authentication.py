import people_pb2
import people_pb2_grpc
import grpc
import urllib
import os
from django.contrib.auth.models import User


class MyBackend:
    def __init__(self):
        API_SERVER = os.environ["RUNTIME_SERVIS_PEOPLE_API_SERVER"]
        API_PORT = os.environ["RUNTIME_SERVIS_PEOPLE_API_PORT"]
        API_KEY = os.environ["RUNTIME_SERVIS_PEOPLE_API_KEY"]
        self.grpc_channel = grpc.insecure_channel("{}:{}".format(API_SERVER, API_PORT))
        self.people_api = people_pb2_grpc.PeopleStub(self.grpc_channel)
        self.people_api_auth_metadata = [('authorization', API_KEY)]

    def get_create_user(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username)
            user.save()
        return user
 
    def authenticate(self, request, username=None, password=None):
        authPersonRequest = people_pb2.AuthPersonRequest(username=username, password=password)
        try:
            #authPersonResponse = self.people_api.AuthEthPerson(authPersonRequest, metadata=self.people_api_auth_metadata)
            if True: #authPersonRequest:
                return self.get_create_user(username) 
            else:
                return None
        except grpc._channel._Rendezvous:
            return None



    def get_user(self, username=None):
        getPersonRequest = people_pb2.GetPersonRequest(username=username)
        try:
            #getPersonResponse = self.people_api.GetEthPerson(getPersonRequest, metadata=self.people_api_auth_metadata)
            return self.get_create_user(username)
        except grpc._channel._Rendezvous:
            return None