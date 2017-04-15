from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    desc = models.CharField(null=True, blank=True, max_length=250)
    avatar = models.ImageField(upload_to='avatars', default='/avatars/default.png')
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(null=True, blank=True, max_length=14)
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Question(models.Model):
    author = models.ForeignKey(to=UserProfile, related_name='question_author')
    title = models.CharField(null=True, blank=True, max_length=100)
    desc = models.TextField(null=True, blank=True, max_length=1000)
    topics = models.ForeignKey(to=Topic, related_name='question', null=True)
    answer_counts = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(to=Question, related_name='question_answer')
    author = models.ForeignKey(to=UserProfile, related_name='answer_author')
    user_vote = models.ManyToManyField(to=UserProfile, related_name='user_vote_answer', blank=True)
    content = models.TextField(null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    like_counts = models.IntegerField(default=0)
    dislike_counts = models.IntegerField(default=0)
    comment_counts = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.author.name


# 取答案前200字符做摘要
@receiver(post_save, sender=Answer)
def create_answer_abstract(sender, instance, created, **kwargs):
    if created:
        content = instance.content
        instance.abstract = content[:200]
        instance.save()


class Comment(models.Model):
    comment_user = models.ForeignKey(to=UserProfile, related_name='comment_author')
    user_ip = models.CharField(null=True, blank=True, max_length=30)
    belong_to = models.ForeignKey(to=Answer, related_name='answer_comments')
    # 父评论
    parent = models.ForeignKey(to='self', related_name='child_comments', null=True, blank=True)
    # 回复对象
    reply_to = models.ForeignKey(to='self', related_name='who_reply', null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment_user.name


class Vote(models.Model):
    owner = models.ForeignKey(to=UserProfile, related_name='user_vote')
    give_to = models.ForeignKey(to=Answer, related_name='vote')
    # 1是未作选择，2是赞同，3是反对
    vote = models.IntegerField(default=1)
    create_time = models.DateTimeField(default=timezone.now)

