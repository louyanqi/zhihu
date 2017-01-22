from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from site_page.models import User, UserProfile, Topic, Question, Answer, Comment, Vote
from .serializers import (UserSerializer, UserProfileSerializer, QuestionSerializer,
                          AnswerSerializer, TopicSerializer, CommentSerializer, OnlyQuestionSerializer,
                          UserLoginSerializer, UserCreateSerializer, )
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from  rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist


@api_view(['GET'])
def user_info(request):
    if request.method == 'GET':
        user_list = User.objects.all()
        serializer = UserSerializer(user_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_info_detail(request, user_id):
    if request.method == 'GET':
        user_list = User.objects.get(id=user_id)
        serializer = UserSerializer(user_list)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def user_now(request):
    if request.method == 'GET':
        if request.auth:
            request_user = request.user
            serializer = UserSerializer(request_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'user_now': 'not_login'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def question(request):
    if request.method == 'GET':
        question_list = Question.objects.all()
        serializer = QuestionSerializer(question_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = request.data
        question_topic = data.get('topic')
        question_desc = data.get('desc')
        question_title = data.get('title')
        user = request.user.profile
        topic_exist = Topic.objects.filter(name=question_topic).exists()
        if topic_exist:
            question_topic = Topic.objects.filter(name=question_topic)[0]
        else:
            Topic.objects.create(name=question_topic)
            question_topic = Topic.objects.filter(name=question_topic)[0]
        question_info = Question.objects.create(author=user, title=question_title, desc=question_desc, topics=question_topic)
        question_info.save()
        serializer = QuestionSerializer(question_info)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def only_question(request):
    p = request.GET.get('p')
    if p:
        start = int(p)
        end = int(p)+5
    else:
        start = 0
        end = 10
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        if user_id:
            question_list = UserProfile.objects.get(belong_to_id=user_id).question_author.all()[start:end]
        else:
            question_topic = request.GET.get('topic')
            topic_info = Topic.objects.filter(name=question_topic)
            if question_topic:
                question_list = Question.objects.filter(topics=topic_info)[start:end]
            else:
                question_list = Question.objects.all()[start:end]
        serializer = OnlyQuestionSerializer(question_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def question_answer_home(request, id):
    try:
        user = UserProfile.objects.get(belong_to_id=request.user.id)
    except ObjectDoesNotExist:
        user = None
    if request.method == 'GET':
        p = request.GET.get('p')
        if p:
            end = int(p) + 5
        else:
            end = 5
        question_info = Question.objects.get(id=id)
        answer_counts = question_info.question_answer.all().count()
        question_info.answer_counts = answer_counts
        question_info.save()
        answer_list = question_info.question_answer.all()[:end]
        if user:
            for answer in answer_list:
                vote = Vote.objects.filter(owner_id=user.id, give_to_id=answer.id).exists()
                if vote:
                    answer.like_or = 'like'
                else:
                    answer.like_or = 'normal'
        serializer = AnswerSerializer(answer_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def answer(request):
    the_topic = request.GET.get('topic')
    p = request.GET.get('p')
    user_id = request.GET.get('user_id')
    user_answer_id = request.GET.get('user_answer_id')
    answer_id = request.GET.get('answer_id')

    if p:
        start = int(p)
        end = int(p)+5
    else:
        start = 0
        end = 10
    if request.method == 'GET':
        if answer_id:    #答案详情页
            answer_info = Answer.objects.get(id=answer_id)
            serializer = AnswerSerializer(answer_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user_id:    #点赞列表页
            answer_list = UserProfile.objects.get(belong_to_id=user_id).user_vote_answer.all()
            serializer = AnswerSerializer(answer_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user_answer_id:    #回答列表页
            answer_list = UserProfile.objects.get(belong_to_id=user_answer_id).answer_author.all()
            serializer = AnswerSerializer(answer_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif the_topic:    #话题页
            answer_list = Answer.objects.filter(question__topics__name=the_topic)[:end]
            serializer = AnswerSerializer(answer_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:    #首页
            answer_list = Answer.objects.all()[start:end]
            serializer = AnswerSerializer(answer_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = request.data
        question_id = data.get('question_id')
        content = data.get('content')
        user = request.user
        new_answer = Answer.objects.create(question_id=question_id, author=user.profile, content=content)
        new_answer.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def comment(request):
    if request.method == 'GET':
        answer_id = request.GET.get('answer_id')
        comment_list = Comment.objects.all().filter(answer_id=answer_id)
        serializer = CommentSerializer(comment_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = request.data
        content = data.get('content')
        answer_id = data.get('answer_id')
        answer_info = Answer.objects.get(id=answer_id)
        user = request.user.profile
        new_comment = Comment.objects.create(author=user, answer_id=answer_id, content=content)
        new_comment.save()
        answer_info.comment_counts = Comment.objects.filter(answer_id=answer_id).count()
        answer_info.save()

        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def topic(request):
    if request.method == 'GET':
        topic_list = Topic.objects.all()
        serializer = TopicSerializer(topic_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def user_vote(request, answer_id, user_id, like_or='normal'):
    answer_info = Answer.objects.get(id=answer_id)
    user = UserProfile.objects.get(belong_to_id=user_id)
    if request.method == 'GET':
        vote = request.GET.get('vote')
        if vote == 'like':
            # exist = answer_info.user_vote.filter(belong_to=user_id).exists()
            exist = Vote.objects.filter(owner=user, give_to=answer_info).exists()
            if exist:
                Vote.objects.filter(owner=user, give_to=answer_info).delete()

                answer_info.user_vote.remove(user)
                like_or = 'normal'
            else:
                vote = Vote.objects.create(owner=user, give_to=answer_info)
                vote.save()
                answer_info.user_vote.add(user)
                like_or = 'like'
            answer_info.like_counts = answer_info.user_vote.all().count()
            answer_info.save()
    return Response({'like_counts': answer_info.like_counts, 'like_or': like_or}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def edit_profile(request, user_id):
    if int(request.user.id) == int(user_id):
        profile = UserProfile.objects.get(belong_to_id=user_id)
        user = profile.belong_to
        if request.method == 'POST':
            data = request.data
            new_name = data.get('name')
            new_desc = data.get('desc')
            if user.username == new_name:
                profile.desc = new_desc
                profile.save()
                return Response(status=status.HTTP_200_OK)
            else:
                exist = User.objects.filter(username=new_name)
                if not exist:
                    user.username = new_name
                    user.save()
                    profile.name = new_name
                    profile.desc = new_desc
                    profile.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({'msg': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'msg': '你没有权限'}, status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserLoginAPIView(APIView):
    permission_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)


