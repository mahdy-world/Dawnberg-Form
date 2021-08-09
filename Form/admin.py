from django.contrib import admin
from .models import Form , Question , QuestionOption
# Register your modeladmion
admin.site.register(Form)
admin.site.register(Question)
admin.site.register(QuestionOption)