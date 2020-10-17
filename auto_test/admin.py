from django.contrib import admin
from . import models

admin.site.register(models.Project,models.ProjectAdmin)
admin.site.register(models.Module,models.ModuleAdmin)
admin.site.register(models.TestCase,models.TestCaseAdmin)
admin.site.register(models.KeyWord,models.KeyWordAdmin)
admin.site.register(models.CaseStep,models.CaseStepAdmin)
