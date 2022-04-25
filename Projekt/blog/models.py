from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

#jakbyscie mieli problem z tagami to zobaczcie ten post
# https://stackoverflow.com/questions/70497294/get-extra-restriction-missing-1-required-positional-argument-related-alias
class Post(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length = 150, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                     related_name='blog_posts')
    image = models.ImageField(upload_to='images/')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.publish.year,
                                                 self.publish.strftime("%m"),
                                                 self.publish.strftime("%d"),
                                                 self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name = 'comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return "Komentarz dodany przez {} dla posta {}".format(self.name, self.post)