from django.db import models
from django.urls import reverse


# formset, modelformset解説用-> TestModel, Book
class TestModel(models.Model):
    text = models.CharField(max_length=20)

    def __str__(self):
        return self.text

class Author(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('first:author', args=[str(self.pk),])

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

