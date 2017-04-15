from django.conf.urls import url
from site_page.views import question_detail, home, profile, answer_detail,\
    edit_profile, question, topic_page, search, profile_answer, profile_ask
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^topic$', topic_page, name="topic"),
    url(r'^question/$', question, name="question"),
    url(r'^question/(?P<question_id>\d+)/$', question_detail, name="question_detail"),
    url(r'^question/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/$', answer_detail, name='answer_detail'),
    url(r'^profile/(?P<user_id>\d+)/$', profile, name="profile"),
    url(r'^profile/(?P<user_id>\d+)/ask/$', profile_ask, name="profile_ask"),
    url(r'^profile/(?P<user_id>\d+)/answer/$', profile_answer, name="profile_answer"),
    url(r'^profile/(?P<user_id>\d+)/edit/$', edit_profile, name="edit_profile"),
    url(r'^search/$', search, name='search'),
    url(r'^user/$', TemplateView.as_view(template_name='login_register.html'))
]

