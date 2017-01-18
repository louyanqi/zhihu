from django.conf.urls import url
from .views import user_info, question, answer, topic, \
    comment, UserLoginAPIView, UserCreateAPIView, user_now, question_answer_home,\
    only_question, user_vote, edit_profile, user_info_detail


urlpatterns = [
    url(r'^api/users/$', user_info),
    url(r'^api/user/(?P<user_id>\d+)/$', user_info_detail),
    url(r'^api/users/now/$', user_now),
    url(r'^api/questions/$', question),
    url(r'^api/only_questions/$', only_question),
    url(r'^api/questions/(?P<id>\d+)/$', question_answer_home),
    url(r'^api/answers/$', answer),
    url(r'^api/topics/$', topic),
    url(r'^api/user_vote/(?P<answer_id>\d+)/(?P<user_id>\d+)/$', user_vote),
    url(r'^api/comments/$', comment),
    url(r'^api/edit_profile/(?P<user_id>\d+)/$', edit_profile),
    url(r'^api/login/$', UserLoginAPIView.as_view()),
    url(r'^api/register/$', UserCreateAPIView.as_view()),
]

