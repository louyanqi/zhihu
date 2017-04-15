from django.conf.urls import url
from .views import user_info, question, answer, topic, \
    comment, user_now, question_answer_home,\
    only_question, user_vote, edit_profile, user_info_detail,\
    register, user_login, answer_detail, child_comments, profile_answer_like, profile_answer, search


urlpatterns = [
    url(r'^api/users/$', user_info),
    url(r'^api/user/(?P<user_id>\d+)/$', user_info_detail),
    url(r'^api/users/now/$', user_now),
    url(r'^api/questions/$', question),
    url(r'^api/only_questions/$', only_question),
    url(r'^api/questions/(?P<id>\d+)/$', question_answer_home),  #问题页
    url(r'^api/answers/$', answer),
    url(r'^api/answer/(?P<answer_id>\d+)/$', answer_detail),
    url(r'^api/topics/$', topic),
    url(r'^api/user_vote/$', user_vote),
    url(r'^api/comments/$', comment),
    url(r'^api/child_comments/(?P<comment_id>\d+)/$', child_comments),
    url(r'^api/edit_profile/(?P<user_id>\d+)/$', edit_profile),
    url(r'^api/register/$', register),
    url(r'^api/login/$', user_login),
    url(r'^api/profile/answers/like/$', profile_answer_like),
    url(r'^api/profile/answers/$', profile_answer),
    url(r'^api/search/', search)
]

