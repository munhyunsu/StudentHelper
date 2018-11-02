import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    title = models.CharField('question title', max_length=100)
    content = models.TextField('question content')
    author = models.CharField('author', max_length=50)
    pub_date = models.DateTimeField('date published')
    is_done = models.BooleanField('is solved')

    def __str__(self):
        return self.title


class Reply(models.Model):
    author = models.CharField('author', max_length=50)
    to = models.IntegerField('question id')
    content = models.TextField('reply content')
    pub_date = models.DateTimeField('date published')
    is_selected = models.BooleanField('is selected')
    # rate = models.FloatField('rate')

    def __str__(self):
        return '{0} to {1} at {2}'.format(self.author, self.to, self.pub_date)
