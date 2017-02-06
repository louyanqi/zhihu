from django.conf.urls import url
from site_page.views import question_detail, home, index_login, profile, answer_detail,\
    edit_profile, register, question, topic_page, search


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^topic$', topic_page, name="topic"),
    url(r'^question/$', question, name="question"),
    url(r'^question/(?P<question_id>\d+)/$', question_detail, name="question_detail"),
    url(r'^question/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/$', answer_detail, name='answer_detail'),
    url(r'^login/$', index_login, name="login"),
    url(r'^profile/(?P<user_id>\d+)/$', profile, name="profile"),
    url(r'^profile/(?P<user_id>\d+)/edit/$', edit_profile, name="edit_profile"),
    url(r'^register/$', register, name="register"),
    url(r'^search/$', search, name='search')
]

