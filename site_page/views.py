#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from site_page.models import UserProfile, Answer, Topic, Question
from site_page.forms import VoteForm, ProfileForm
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


def search(request):
    context = {}
    q = request.GET.get("q", "").strip()
    if not q:
        return redirect(to="home")
    context["q"] = q
    answers = Answer.objects.filter(content__contains=q)
    context["answers"] = answers
    return render(request, "search.html", context)


def edit_profile(request, user_id):
    user = get_object_or_404(UserProfile, belong_to_id=user_id)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        info = form.save()
        info.save()
    context = {'form': form}
    return render(request, 'edit_profile.html', context)