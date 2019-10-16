from django.db import models
from rest_framework import serializers


# --- QUESTIONS ---


class Question(models.Model):
    label = models.TextField()
    positive = models.TextField()
    negative = models.TextField()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'label', 'positive', 'negative')


# --- TEACHING ASSISTANTS ---


class TeachingAssistant(models.Model):
    name = models.TextField()

class TeachingAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingAssistant
        fields = ('id', 'name',)


# --- LECTURES ---


class Lecture(models.Model):
    HERBST_SEMESTER     = "HS"
    FRUHLINGS_SEMESTER  = "FS"
    SEMESTER_CHOICES    = [
        (HERBST_SEMESTER, "Herbstsemester"),
        (FRUHLINGS_SEMESTER, "Fruhlingsemester"),
    ]
    name = models.TextField()
    semester = models.CharField(
        max_length=2,
        choices = SEMESTER_CHOICES,
        default=HERBST_SEMESTER
    )
    professors = models.TextField()
    year = models.IntegerField()


    def is_upperclass(self):
        return self.semester in (self.HERBST_SEMESTER, self.FRUHLINGS_SEMESTER)

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('id', 'name', 'semester', 'professors', 'year')


# --- SESSIONS ---


class Session(models.Model):
    LANGUAGE_ENGLISH    = "EN"
    LANGUAGE_GERMAN     = "DE"
    LANGUAGE_ITALIAN    = "IT"
    LANGUAGE_FRENCH     = "FR"
    LANGUAGE_CHOICES    = [
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_GERMAN, "German"),
        (LANGUAGE_ITALIAN, "Italian"),
        (LANGUAGE_FRENCH, "French"),
    ]
    language = models.CharField(
        max_length=2,
        choices = LANGUAGE_CHOICES,
        default = LANGUAGE_GERMAN
    )
    assistant = models.ForeignKey(TeachingAssistant, on_delete = models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    def is_upperclass(self):
        return self.language in (self.LANGUAGE_ENGLISH, self.LANGUAGE_GERMAN, self.LANGUAGE_ITALIAN, self.LANGUAGE_FRENCH)

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'language', 'assistant', 'lecture')
        

# --- VOTES ---


class Vote(models.Model):
    VOTE_POSITIVE   = "P"
    VOTE_NEGATIVE   = "N"
    VOTE_CHOICES    = [
        (VOTE_POSITIVE, "Positive"),
        (VOTE_NEGATIVE, "Negative"),
    ]
    opinion = models.CharField(
        max_length=1,
        choices = VOTE_CHOICES,
        default = VOTE_NEGATIVE
    )
    session         = models.ForeignKey(Session, on_delete=models.CASCADE)
    question        = models.ForeignKey(Question, on_delete=models.CASCADE)

    def is_upperclass(self):
        return self.opinion in (self.VOTE_NEGATIVE, self.VOTE_POSITIVE)

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'session', 'question', 'opinion')