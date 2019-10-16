from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import Lecture
from .models import Question
from .models import Session
from .models import TeachingAssistant
from .models import Vote

admin.site.register(Lecture)
admin.site.register(Question)
admin.site.register(Session)
admin.site.register(TeachingAssistant)
admin.site.register(Vote)

# TODO : Find a way to make sure that we don't add the admin every single time that we run the app.
try:
    User.objects.create_superuser(username='admin', email='admin@example.org', password='visdev4funandjoy')
except Exception as e:
    print("Error adding admin: " + str(e))