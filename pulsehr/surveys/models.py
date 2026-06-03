from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    """Опрос"""
    title = models.CharField(max_length=200, verbose_name='Название опроса')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_anonymous = models.BooleanField(default=True, verbose_name='Анонимный опрос')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    """Вопрос"""
    QUESTION_TYPES = [
        ('rating', 'Оценка 1-5'),
        ('text', 'Текстовый ответ'),
        ('choice', 'Выбор одного варианта'),
    ]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions', verbose_name='Опрос')
    text = models.CharField(max_length=500, verbose_name='Текст вопроса')
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='text', verbose_name='Тип вопроса')
    order = models.IntegerField(default=0, verbose_name='Порядок')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['order']


class Choice(models.Model):
    """Вариант ответа (для типа choice)"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name='Вопрос')
    text = models.CharField(max_length=200, verbose_name='Текст варианта')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'


class Answer(models.Model):
    """Ответ сотрудника"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Сотрудник')
    session_key = models.CharField(max_length=40, blank=True, verbose_name='Ключ сессии')

    # Для rating: значение 1-5
    rating_value = models.IntegerField(null=True, blank=True, verbose_name='Оценка')

    # Для text: текст ответа
    text_value = models.TextField(blank=True, verbose_name='Текстовый ответ')

    # Для choice: выбранный вариант
    choice_value = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='Выбранный вариант')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата ответа')

    def __str__(self):
        return f'Ответ на "{self.question}"'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'