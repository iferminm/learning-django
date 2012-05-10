from django.db import models
from django.conf import settings
import os

class ProfessorType(models.Model):
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name


class ProfessorDegree(models.Model):
    name = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class CourseCategory(models.Model):
    name = models.CharField(max_length=64)
    courses = models.ManyToManyField(Course)

    def __unicode__(self):
        return self.name

class Professor(models.Model):
    picture = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT, 'professor_pictures'), blank=True, null=True)
    first_name = models.CharField(max_length=32)
    last_names = models.CharField(max_length=64)
    gender = models.CharField(max_length=2, choices=settings.GENDER_CHOICES)
    prof_type = models.ForeignKey(ProfessorType)
    degree = models.ForeignKey(ProfessorDegree)
    date_begin = models.DateField()
    date_retired = models.DateField(blank=True, null=True)
    teaches = models.ManyToManyField(Course)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_names)


class CourseGuide(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    week = models.IntegerField()
    course = models.ForeignKey(Course)
    author = models.ForeignKey(Professor)

    def __unicode__(self):
        return self.name


class GuideTheme(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    guide = models.ForeignKey(CourseGuide)

    def __unicode__(self):
        return self.name


class Student(models.Model):
    picture = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT, 'professor_pictures'), blank=True, null=True)
    first_name = models.CharField(max_length=32)
    last_names = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    gender = models.CharField(max_length=2, choices=settings.GENDER_CHOICES)
    enroled = models.ManyToManyField(Course)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_names)


class Session(models.Model):
    begin = models.DateTimeField()
    end = models.DateTimeField()
    course = models.ForeignKey(Course)
    themes = models.ManyToManyField(GuideTheme)
