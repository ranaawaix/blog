from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.


class Category(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            self.slug + slugify(self.id)
        return super().save(*args, **kwargs)


def validate_future_date(value):
    if value < timezone.now().date():
        raise ValidationError('Date must be today or in the future.')


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=250)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    publish_date = models.DateField(null=True, blank=True, validators=[validate_future_date])
    publish = models.BooleanField(null=True, blank=True)
    draft = models.BooleanField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True, upload_to='media')
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        else:
            self.slug + slugify(self.updated_on)
        return super().save(*args, **kwargs)

    def get_upvote_count(self):
        return Vote.objects.filter(post=self, vote=True).count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='main')
    comment = models.CharField(max_length=250, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    vote = models.BooleanField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return f'User: {self.user} Vote: {self.post}'

    def validate_unique_vote(self):
        existing_votes = Vote.objects.filter(user=self.user, post=self.post)
        if existing_votes.exists():
            raise ValidationError("You have already voted on this post.")

    def save(self, *args, **kwargs):
        self.validate_unique_vote()
        super().save(*args, **kwargs)


class ContactUs(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.PositiveIntegerField(validators=[MaxValueValidator(99999999999)])
    message = models.TextField()
    file = models.FileField(null=True, blank=True, upload_to='media')

    def __str__(self):
        return self.name
