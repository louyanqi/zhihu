from django.contrib import admin
from site_page.models import UserProfile, Topic, Question, Answer, Comment, Vote
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Vote)


