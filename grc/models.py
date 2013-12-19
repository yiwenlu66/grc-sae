import time
from django.db import models


class Group(models.Model):
    name_en = models.CharField(max_length=20)
    name_ch = models.CharField(max_length=20)
    enabled = models.BooleanField()

    def __str__(self):
        return self.name_en


class Question(models.Model):
    q_class = models.IntegerField()
    # Currently Supported:
    #    0 - Random Blanks
    #    1 - Strict Blanks
    group = models.ForeignKey(Group)
    title = models.CharField(max_length=20, default=" ")
    question = models.TextField()
    answer = models.TextField(blank=True)
    # Converted from Python list, not required for q_class 0
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.group) + "_" + str(self.id)
