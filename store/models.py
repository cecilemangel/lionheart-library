from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)
    picture = models.URLField()
    about = models.CharField(max_length=2000, null=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    email = models.EmailField(max_length=100)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    synopsis = models.CharField(max_length=2000)
    picture = models.URLField()
    author = models.ManyToManyField(Author, related_name='books', blank=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    contacted = models.BooleanField(default=False)
    book = models.OneToOneField(Book, on_delete=models.CASCADE, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    def __str__(self):
        return self.contact.name