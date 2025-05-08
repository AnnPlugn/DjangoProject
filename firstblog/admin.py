from django.contrib import admin
from .models import Compound, ModelTraining

@admin.register(Compound)
class CompoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'formula', 'created_at')
    search_fields = ('name', 'formula')

@admin.register(ModelTraining)
class ModelTrainingAdmin(admin.ModelAdmin):
    list_display = ('model_type', 'training_date')
    list_filter = ('model_type',)