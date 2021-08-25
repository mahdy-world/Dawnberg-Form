from django.contrib import admin
from .models import *

# Register your modeladmion
admin.site.register(Form)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(Answer)
admin.site.register(Instance)
admin.site.register(InstanceCall)
admin.site.register(InstanceComment)
