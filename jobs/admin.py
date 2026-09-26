from django.contrib import admin
from .models import CandidateProfile, Job, Application

admin.site.register(CandidateProfile)
admin.site.register(Job)
admin.site.register(Application)
