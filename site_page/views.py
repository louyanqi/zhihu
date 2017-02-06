#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Q
from site_page.models import UserProfile, Answer, Question, User, Topic
from site_page.forms import ProfileForm
from django.shortcuts import get_object_or_404


def question(request):
    question_list = Question.objects.all()
    context = {
        'question_list': question_list
    }

    return render(request, 'question.html', context)


def answer_detail(request, question_id, answer_id):
    question_info = Question.objects.get(id=question_id)
    answer_info = Answer.objects.get(id=answer_id)

    context = {
        'answer': answer_info,
        'question': question_info
    }

    return render(request, "answer_detail.html", context)


def question_detail(request, question_id):
    question_info = Question.objects.get(id=question_id)

    context = {
        'question': question_info
    }

    return render(request, "question_detail.html", context)


def home(request):
    context = {}
    return render(request, "home.html", context)


def topic_page(request):
    topic_name = request.GET.get('t')

    context = {'topic_name': topic_name}
    return render(request, "topic.html", context)


def index_login(request):
    context = {}

    return render(request, "login.html", context)


def profile(request, user_id):

    context = {
        'user_id': user_id
    }

    return render(request, 'profile.html', context)


def register(request):
    context = {}

    return render(request, "register.html", context)


def edit_profile(request, user_id):
    user = get_object_or_404(UserProfile, belong_to_id=user_id)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        info = form.save()
        info.save()
    context = {'form': form}
    return render(request, 'edit_profile.html', context)


def search(request):
    q = request.GET.get('q')
    search_type = request.GET.get('type')
    if not search_type:
        search_type = 'content'
    user_list = topic_list = answer_list = []
    if search_type == 'people':
        user_list = User.objects.filter(Q(username__icontains=q))
    elif search_type == 'topic':
        topic_list = Topic.objects.filter(Q(name__icontains=q))
    else:
        answer_list = Answer.objects.filter(Q(question__title__icontains=q) |
                                            Q(question__desc__icontains=q) |
                                            Q(content__icontains=q))
    print(answer_list)
    context = {
        'q': q,
        'user_list': user_list,
        'topic_list': topic_list,
        'answer_list': answer_list,
        'search_type': search_type
    }
    return render(request, 'search.html', context)
