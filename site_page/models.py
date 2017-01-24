from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(null=True)
    desc = models.CharField(null=True, blank=True, max_length=250)
    avatar = models.ImageField(upload_to='avatars', default='/avatars/default.png')
    create_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(null=True, blank=True, max_length=14)
    create_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    author = models.ForeignKey(to=UserProfile, related_name='question_author')
    title = models.CharField(null=True, blank=True, max_length=100)
    desc = models.TextField(null=True, blank=True, max_length=1000)
    topics = models.ForeignKey(to=Topic, related_name='question', null=True)
    answer_counts = models.IntegerField(default=0)
    create_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(to=Question, related_name='question_answer')
    author = models.ForeignKey(to=UserProfile, related_name='answer_author')
    user_vote = models.ManyToManyField(to=UserProfile, related_name='user_vote_answer', blank=True)
    content = models.TextField(null=True, blank=True)
    like_counts = models.IntegerField(default=0)
    dislike_counts = models.IntegerField(default=0)
    comment_counts = models.IntegerField(default=0)
    create_time = models.DateField(auto_now=True)
    show_all_content = models.BooleanField(default=False)
    like_or = models.CharField(max_length=10, default='normal')

    def __str__(self):
        return self.author.name


class Comment(models.Model):
    author = models.ForeignKey(to=UserProfile, related_name='comment_author')
    answer = models.ForeignKey(to=Answer, related_name='answer_comments')
    content = models.TextField(null=True, blank=True)
    create_time = models.DateField(auto_now=True)
    comment_reply_input = models.BooleanField(default=False)

    def __str__(self):
        return self.author.name


class Vote(models.Model):
    owner = models.ForeignKey(to=UserProfile)
    give_to = models.ForeignKey(to=Answer)
    create_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.owner.name
