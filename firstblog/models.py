from django.db import models
from django.contrib.postgres.fields import JSONField

class Compound(models.Model):
    """Химическое соединение для анализа"""
    name = models.CharField(max_length=200, verbose_name='Название соединения')
    formula = models.CharField(max_length=100, verbose_name='Химическая формула')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Соединение'
        verbose_name_plural = 'Соединения'

class ModelTraining(models.Model):
    """Результаты обучения модели"""
    model_type = models.CharField(max_length=100, verbose_name='Тип модели')
    training_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата обучения')
    metrics = models.JSONField(verbose_name='Метрики модели')  # Store metrics like accuracy, loss
    dataset_info = models.TextField(verbose_name='Информация о наборе данных')

    def __str__(self):
        return f"{self.model_type} - {self.training_date}"

    class Meta:
        verbose_name = 'Обучение модели'
        verbose_name_plural = 'Обучения модели'