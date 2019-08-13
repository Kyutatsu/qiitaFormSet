from django.contrib import admin

from first.models import TestModel, Author, Book


admin.site.register(TestModel)
admin.site.register(Author)
admin.site.register(Book)
