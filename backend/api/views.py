from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets, status
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
#from django.views.decorators.csrf import csrf_exempt

from rest_framework import serializers

from .models import TeachingAssistant, TeachingAssistantSerializer
from .models import Lecture, LectureSerializer
from .models import Session, SessionSerializer
from .models import Question, QuestionSerializer
from .models import Vote, VoteSerializer

import pandas as pd
import numpy as np

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))

#@csrf_exempt
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class TeachingAssistantViewSet(viewsets.ModelViewSet):
    queryset = TeachingAssistant.objects.all()
    serializer_class = TeachingAssistantSerializer

class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#            handle_uploaded_file(request.FILES['file']) 
#            return Response("ok", status=status.HTTP_200_OK)
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})
# 
class Csv(object):
    def __init__(self, **kwargs):
        for field in ('id', 'name', 'data'):
            setattr(self, field, kwargs.get(field, None))


class CSVSerializer(serializers.Serializer):
    # name = serializers.CharField(max_length=256)
    data = serializers.FileField()

    def create(self, validated_data):
        return Csv(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance

class CSVViewSet(viewsets.ViewSet):
        # Required for the Browsable API renderer to have a nice form.
    serializer_class = CSVSerializer

    def list(self, request):
        return Response("can't list csv_files", status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        
        serializer = CSVSerializer(data=request.data)
        if serializer.is_valid():
            csv_obj = serializer.save()
            err = handle_csv(csv_obj.data)
            if not err is None:
                return Response("Error reading csv: " + err, status=status.HTTP_400_BAD_REQUEST)
            else :
                return Response("Lectures and Teaching Assistants added.", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response("can't retrieve csv_files", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        self.create(request)

    def partial_update(self, request, pk=None):
        self.create(request)

    def destroy(self, request, pk=None):
        return Response("can't destroy csv_files", status=status.HTTP_400_BAD_REQUEST)

def handle_csv(f):
    try:
        df = pd.read_csv(f, sep="%")
    except Exception as e:
        return str(e)
    
    if df.shape[0]<1:
        return "File is empty or malformed"
    correct_header = "lecture_name, lecture_semester, lecture_professors, lecture_year, ta_name, session_language"
    if df.shape[1] != 6:
        return "found " + str(df.shape[1]) + "cols, Wrong header, we want: " + correct_header
    
    df = df.applymap(lambda s: str(s).strip())

    for i, line in df.iterrows():
        lecture_name, lecture_semester, lecture_professors, lecture_year, ta_name, session_language = line

        lec_exists = Lecture.objects.filter(name=lecture_name, year=lecture_year, semester=lecture_semester).exists()
        if not lec_exists:
            lec = Lecture(name=lecture_name, semester=lecture_semester, professors=lecture_professors, year=lecture_year)
            lec.save()
        else:
            lec = Lecture.objects.filter(name=lecture_name, year=lecture_year, semester=lecture_semester)[0]
        
        ta_exists = TeachingAssistant.objects.filter(name=ta_name).exists()
        if not ta_exists:
            ta = TeachingAssistant(name=ta_name)
            ta.save()
        else: 
            ta = TeachingAssistant.objects.filter(name=ta_name)[0]
            
        se_exists = Session.objects.filter(assistant=ta.id, lecture=lec.id).exists()
        if not se_exists:
            se = Session(language=session_language, assistant=ta, lecture=lec)
            se.save()
        

        
        
from django.contrib.auth import authenticate, login
from backend.settings.authentication import MyBackend
from django.http import JsonResponse

def login_view(request):
    be = MyBackend()
    if request.method == 'GET':
        username = request.GET['username']
        password = request.GET['password']
        user = be.authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'success'}, status=status.HTTP_200_OK)
        else:
            # Return an 'invalid login' error message.
            return JsonResponse({'message': 'invalid login'}, status=status.HTTP_401_UNAUTHORIZED)
        



    
    

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
