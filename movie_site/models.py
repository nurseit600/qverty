from django.db import models
import django.contrib.auth.models
from phonenumber_field.modelfields import PhoneNumberField

STATUS_CHOICES = (
    ('pro', 'PRO'),
    ('simple', 'SIMPLE'),
)


class Profile(django.contrib.auth.models.AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, region='KG')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return self.status


class Country(models.Model):
    country_name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=64)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField()
    director_image = models.ImageField(upload_to='director_image/')

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=16)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField()
    director_image = models.ImageField(upload_to='actor_image/')

    def __str__(self):
        return self.actor_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=64)
    year = models.DateField()
    country = models.ManyToManyField(Country, related_name='country_movies')
    director = models.ManyToManyField(Director, related_name='director_movies')
    actor = models.ManyToManyField(Actor, related_name='actor_movies')
    genre = models.ManyToManyField(Genre, related_name='genre_movies')
    TYPES_CHOICES = (
        ('144p', '144p'),
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
    )
    types = models.CharField(max_length=14, choices=TYPES_CHOICES, default='144')
    movie_time = models.PositiveSmallIntegerField()
    description = models.TextField()
    movie_trailer = models.FileField(upload_to='trailers/')
    movie_image = models.ImageField(upload_to='movie_images/')
    status_movie = models.CharField(max_length=16, choices=STATUS_CHOICES)

    def __str__(self):
        return self.movie_name


class MovieLanguages(models.Model):
    language = models.CharField(max_length=16)
    video = models.FileField(upload_to='movie_language/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_language')

    def __str__(self):
        return f'{self.movie}, {self.language}'


class Moments(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='moments')
    movie_moments = models.ImageField(upload_to='movie_moments')


class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.user}, {self.movie} '


class Favorite(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class History(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.user} - {self.movie} '




