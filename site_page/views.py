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

    context = {
        'answer_id': answer_id,
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


def profile(request, user_id):

    context = {
        'user_id': user_id
    }

    return render(request, 'profile.html', context)


def profile_ask(request, user_id):

    context = {
        'user_id': user_id
    }

    return render(request, 'peo_ask.html', context)


def profile_answer(request, user_id):

    context = {
        'user_id': user_id
    }

    return render(request, 'peo_answer.html', context)


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
    answer_list = Answer.objects.filter(Q(question__title__icontains=q) |
                                            Q(question__desc__icontains=q) |
                                            Q(content__icontains=q))
    print(answer_list)
    print('#'*65)
    context = {
        'q': q,
        'answer_list': answer_list,
    }
    return render(request, 'search.html', context)
