from django.contrib import admin
from site_page.models import UserProfile, Topic, Question, Answer, Comment, Vote


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['belong_to', 'name', 'email', 'create_time']
    search_fields = ['belong_to', 'name', 'email', 'create_time']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'answer_counts', 'create_time']
    search_fields = ['author', 'title', 'answer_counts', 'create_time']


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'author', 'like_counts', 'create_time']
    search_fields = ['question', 'author', 'like_counts', 'create_time']


class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_time']
    search_fields = ['name', 'create_time']


class VoteAdmin(admin.ModelAdmin):
    list_display = ['owner', 'give_to', 'vote', 'create_time']
    search_fields = ['owner', 'give_to', 'create_time']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['belong_to', 'comment_user', 'parent', 'create_time']
    search_fields = ['belong_to', 'comment_user', 'parent', 'create_time']

admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote,)


