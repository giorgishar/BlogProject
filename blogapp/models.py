from django.db import models
from django.forms import CharField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile
from taggit.managers import TaggableManager



class Feedback(models.Model):
    STATUSES = (
        (0, 'Unlike'),
        (1, 'Like'),
        (2, 'None')
        )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('blogapp.Post', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUSES)

    class Meta:
        unique_together = ['user', 'post']
    



class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    feedbacks = models.ManyToManyField(User, related_name='feedbacks', through=Feedback)
    tags = TaggableManager()
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.name)