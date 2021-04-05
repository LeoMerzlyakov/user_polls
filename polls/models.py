from django.contrib.auth.models import User
from django.db import models


class Poll(models.Model):
    text = models.CharField(max_length=200)
    time_start = models.DateTimeField('date published')
    time_end = models.DateTimeField('date passed', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField()

    class Meta:
        ordering = ['time_start']

    def __str__(self):
        return str(self.pk)


class Question(models.Model):
    CHOICES = (
        ('TXT', 'Ответ текстом'),
        ('CH1', 'Выбор одгого'),
        ('CHM', 'Выбор нескольких'),
    )

    text = models.CharField(max_length=200)
    type = models.CharField(max_length=300, choices=CHOICES)
    poll = models.ManyToManyField(Poll, related_name='questions')

    class Meta:
        ordering = ['text']

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.TextField(null=True, blank=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,
                                 on_delete=models.SET_NULL,
                                 null=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)

    def __str__(self):
        return self.text
