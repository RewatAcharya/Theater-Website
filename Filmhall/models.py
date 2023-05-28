from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=30)
    poster = models.ImageField(upload_to='media/poster/')
    details = models.TextField()
    stars = models.TextField()
    run_time = models.CharField(max_length=15)
    IMDB_rating = models.CharField(max_length=10)
    release = models.DateField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    review = models.TextField()
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.review
    
class Show(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.start_time)+" "+str(self.movie_id)
    
class Seat(models.Model):
    name = models.CharField(max_length=8)

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)