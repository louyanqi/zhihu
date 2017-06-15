from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from site_page.models import User, UserProfile, Topic, Question, Answer, Comment, Vote
from .serializers import (UserSerializer, UserProfileSerializer, QuestionSerializer,
                          AnswerSerializer, TopicSerializer, CommentSerializer, OnlyQuestionSerializer,
                          AnswerDetailSerializer, ChildCommentSerializer)
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from site_page.paginator import get_page_list
from django.db.models import Q
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def user_info(request):
    if request.method == 'GET':
        if request.GET.get('type') == 'people':
            q = request.GET.get('q')
            user_list = User.objects.filter(Q(username__icontains=q))
        else:
            user_list = User.objects.all()
        serializer = UserSerializer(user_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_info_detail(request, user_id):
    if request.method == 'GET':
        user_list = User.objects.get(id=user_id)
        serializer = UserSerializer(user_list)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 用来判断当前用户身份，返回其信息
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


# 下级没有answer的question，为节约加载
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


# 问题页，问题为主导
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
    print(request.auth)
    print(request.user)
    the_topic = request.GET.get('topic')
    p = request.GET.get('p')
    user_answer_id = request.GET.get('user_answer_id')
    q = request.GET.get('q')
    if p:
        start = int(p)
        end = int(p)+5
    else:
        start = 0
        end = 10
    if request.method == 'GET':
        if user_answer_id:    #回答列表页
            answer_list = UserProfile.objects.get(belong_to_id=user_answer_id).answer_author.all()
            serializer = AnswerSerializer(answer_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif the_topic:    #话题页
            answer_list = Answer.objects.filter(question__topics__name=the_topic)[:end]
            serializer = AnswerSerializer(answer_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif q:  #搜索
            answer_list = Answer.objects.filter(Q(question__title__icontains=q) |
                                                Q(question__desc__icontains=q) |
                                                Q(content__icontains=q))
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
@authentication_classes((TokenAuthentication, ))
def answer_detail(request, answer_id):
    if request.method == 'GET':
        # 已登录用户判断是否对答案点赞
        if request.auth:
            user_id = request.user.profile.id
            vote_exist = Vote.objects.filter(owner_id=user_id, give_to_id=answer_id).exists()
            if vote_exist:
                vote_info = Vote.objects.get(owner_id=user_id, give_to_id=answer_id).vote
            else:
                vote_info = 1
        else:
            vote_info = 1
        answer_info = get_object_or_404(Answer, id=answer_id)
        serializer = AnswerDetailSerializer(answer_info)

        data = {
            'answer': serializer.data,
            'vote': vote_info
        }
        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def comment(request):
    if request.method == 'GET':
        answer_id = request.GET.get('answer_id')
        now_page = request.GET.get('page')
        comment_list_num = Comment.objects.all().filter(belong_to_id=answer_id, parent=None).count()

        if int(comment_list_num) % 5 != 0:
            num_pages = int(int(comment_list_num) / 5 + 1)
        else:
            num_pages = int(int(comment_list_num) / 5)

        if not now_page:
            now_page = 1
            start = 0
        else:
            start = (int(now_page)-1)*5

        if comment_list_num <= start+5:
            have_next = False
        else:
            have_next = True

        comment_list = Comment.objects.all().filter(belong_to_id=answer_id, parent=None).order_by('-id')[start:start+5]
        page_list = get_page_list(current_page=int(now_page), left=3, right=4, page_number=num_pages)
        serializer = CommentSerializer(comment_list, many=True)
        data = {
            'data': serializer.data,
            'page_list': page_list,
            'now_page': now_page,
            'have_next':  have_next
        }
        return Response(data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        data = request.data
        parent_id = data.get('parent_id')
        content = data.get('content')
        reply_id = data.get('reply_id')
        answer_id = data.get('answer_id')
        answer_info = Answer.objects.get(id=answer_id)
        user = request.user.profile

        new_comment = Comment.objects.create(comment_user=user, belong_to_id=answer_id,
                                             content=content, parent_id=parent_id, reply_to_id=reply_id)
        new_comment.save()

        comment_counts = Comment.objects.filter(belong_to_id=answer_id).count()
        answer_info.comment_counts = comment_counts
        answer_info.save()

        return Response({'comment_counts': comment_counts}, status=status.HTTP_200_OK)


@api_view(['GET'])
def child_comments(request, comment_id):
    if request.method == 'GET':
        comment_info = Comment.objects.get(id=comment_id)
        child_comments_list = comment_info.child_comments
        serializer = ChildCommentSerializer(child_comments_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def topic(request):
    if request.method == 'GET':
        if request.GET.get('type') == 'topic':
            q = request.GET.get('q')
            topic_list = Topic.objects.filter(Q(name__icontains=q))
        else:
            topic_list = Topic.objects.all()
        serializer = TopicSerializer(topic_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def user_vote(request):
    if request.method == 'POST':

        data = request.data
        vote = int(data['vote'])
        user_id = request.user.profile.id
        answer_id = data['answer_id']
        answer_info = Answer.objects.get(id=answer_id)
        exists = Vote.objects.filter(owner_id=user_id, give_to_id=answer_id).exists()
        if exists:
            vote_info = Vote.objects.get(owner_id=user_id, give_to_id=answer_id)
            # 如果已经点赞或反对，再次点击则取消
            if vote == vote_info.vote:

                Vote.delete(vote_info)
                if vote == 2:
                    answer_info.like_counts -= 1
                if vote == 3:
                    answer_info.dislike_counts -= 1
                answer_info.save()

            # 把赞同改为反对或相反
            else:
                vote_info.vote = vote
                vote_info.save()
                if vote == 2:
                    answer_info.like_counts += 1
                    answer_info.dislike_counts -= 1
                if vote == 3:
                    answer_info.like_counts -= 1
                    answer_info.dislike_counts += 1
                answer_info.save()
        else:
            Vote.objects.create(owner_id=user_id, give_to_id=answer_id, vote=vote)
            if vote == 2:
                answer_info.like_counts += 1
            if vote == 3:
                answer_info.dislike_counts += 1
            answer_info.save()

        # 把赞同反对数保存到数据库，测试发现这种用时间多一点
        # vote_like_count = Vote.objects.filter(give_to_id=answer_id, vote=2).count()
        # vote_dislike_count = Vote.objects.filter(give_to_id=answer_id, vote=3).count()
        # answer_info = Answer.objects.get(id=answer_id)
        # answer_info.like_counts = vote_like_count
        # answer_info.dislike_counts = vote_dislike_count
        # answer_info.save()
        return Response(status=status.HTTP_200_OK)


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


@api_view(['GET', 'POST'])
def register(request):
    if request.method == "POST":
        data = request.data
        name = data.get('name')
        passwd = data.get('password')

        # 手机注册用户
        if 'phone' in data:
            phone = data.get('phone')
            user_exist = User.objects.filter(username=phone).exists()
            # 手机号被注册
            if user_exist:
                return Response({'msg': '手机号已被注册'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_info = User(username=phone)
                user_info.set_password(passwd)
                user_info.save()
                UserProfile.objects.create(belong_to=user_info, name=name, phone=phone)

                return Response({"msg": '注册成功'}, status=status.HTTP_200_OK)

        # 邮箱注册用户
        elif 'email' in data:
            email = data.get('email')
            user_exist = User.objects.filter(username=email).exists()
            # 邮箱被注册
            if user_exist:
                return Response({'msg': '邮箱已被注册'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_info = User(username=email)
                user_info.set_password(passwd)
                user_info.save()
                UserProfile.objects.create(belong_to=user_info, name=name, email=email)

                return Response({"msg": '注册成功'}, status=status.HTTP_200_OK)
        else:

            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    if request.method == "POST":
        data = request.data
        print(data)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        # 判断用户信息是否正确
        if not user or not username:
            return Response({'msg': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 用户信息正确生成token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def profile_answer_like(request):
    user_id = request.user.profile.id
    answer_list = Answer.objects.filter(vote__owner_id=user_id, vote__vote=2).all()
    serializer = AnswerSerializer(answer_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def profile_answer(request):
    user_id = request.user.profile.id
    answer_list = Answer.objects.filter(author_id=user_id).all()
    serializer = AnswerSerializer(answer_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def search(request):
    search_type = request.GET.get('type')
    q = request.GET.get('q')

    if search_type == 'content':
        answer_list = Answer.objects.filter(Q(question__title__icontains=q) |
                                            Q(question__desc__icontains=q) |
                                            Q(content__icontains=q))
        serializer = AnswerSerializer(answer_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if search_type == 'topic':
        topic_list = Topic.objects.filter(Q(name__icontains=q))
        serializer = TopicSerializer(topic_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if search_type == 'people':
        user_list = UserProfile.objects.filter(Q(name__icontains=q) | Q(desc__icontains=q))
        serializer = UserProfileSerializer(user_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

