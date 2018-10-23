import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    title = models.CharField('question title', max_length=100)
    content = models.TextField('question content')
    author = models.CharField('author', max_length=50)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
