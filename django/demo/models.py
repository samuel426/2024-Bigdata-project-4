from django.conf import settings
from django.db import models
from django.utils import timezone

from hdfs import InsecureClient


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    

class Show():
    def __init__(self, input_1, input_2):
        self.input_1 = input_1
        self.input_2 = input_2

    def getDataFromHDFS(self):
        # HDFS Namenode IP addr
        client = InsecureClient("http://192.168.0.48:50070", user="hadoop")
        with client.read("/user/hadoop/strawberry_avg.csv", encoding='utf-8') as f:
            return f.read()

