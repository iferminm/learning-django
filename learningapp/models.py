from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from mailer import Mailer
import os

class ProfessorType(models.Model):
    """
    Models the professor's grade in the institute
    """
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name


class ProfessorDegree(models.Model):
    """
    Models the professor's academic degree
    """
    name = models.CharField(max_length=16)
    
    def __unicode__(self):
        return self.name


class Course(models.Model):
    """
    Models the distinct courses that the institute offers
    """
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class CourseCategory(models.Model):
    """
    Models a hierarchical categories structure to classify the courses
    """
    name = models.CharField(max_length=64)
    courses = models.ManyToManyField(Course)
    parent = models.ForeignKey('CourseCategory', null=True, blank=True)

    def __unicode__(self):
        return self.name

class Professor(models.Model):
    """
    Models the information about the professors
    """
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
    """
    Stores information about the guides for the courses
    """
    name = models.CharField(max_length=128)
    description = models.TextField()
    week = models.IntegerField()
    course = models.ForeignKey(Course)
    author = models.ForeignKey(Professor)

    def __unicode__(self):
        return self.name


class GuideTheme(models.Model):
    """
    Content for the guides
    """
    title = models.CharField(max_length=128)
    content = models.TextField()
    guide = models.ForeignKey(CourseGuide)

    def __unicode__(self):
        return self.title


class Student(models.Model):
    """
    Models information about the students
    """
    picture = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT, 'student_pictures'), blank=True, null=True)
    first_name = models.CharField(max_length=32)
    last_names = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    gender = models.CharField(max_length=2, choices=settings.GENDER_CHOICES)
    enroled = models.ManyToManyField(Course)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_names)


class Session(models.Model):
    """
    Class sessions on the courses.
    """
    begin = models.DateTimeField()
    end = models.DateTimeField()
    course = models.ForeignKey(Course)
    themes = models.ManyToManyField(GuideTheme)
    ended = models.BooleanField(default=False)
    mail_sent = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s: %s -- %s" % (self.course.name, self.begin, self.end)

def session_ended(sender, instance, created, *args, **kwargs):
    if not created and instance.ended and not instance.mail_sent:
        students = instance.course.student_set.all()
        content = ", ".join(t.title for t in instance.themes.all())
        print content
        mailer = Mailer()
        for s in students:
            name = "%s %s" % (s.first_name, s.last_names)
            text = u"""
Estimado/a %s

Su clase ha finalizado, el contenido visto fue:

%s

Se le recomienda ampliamente revisar el contenido.
""" % (name, content)
            mail = s.email
            mailer.send_mail(name, mail, u"Contenidos de la clase de hoy", text)

        instance.mail_sent = True
        instance.save()

post_save.connect(session_ended, sender=Session)
