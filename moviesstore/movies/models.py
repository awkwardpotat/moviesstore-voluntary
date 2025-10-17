from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def like_ratio(self):
        total_reviews = self.review_set.count()
        if total_reviews == 0:
            return 0
        likes = self.review_set.filter(is_like=True).count()
        return int((likes / total_reviews) * 100)

    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField(default=None)  # True for upvote, False for downvote

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name