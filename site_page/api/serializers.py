from rest_framework.serializers import (ModelSerializer, EmailField, ValidationError)
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from site_page.models import (User, UserProfile, Topic,
                              Question, Answer, Comment)

from rest_framework.response import Response
from rest_framework import status


class UserCreateSerializer(ModelSerializer):
    email = EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email'
        ]
        extra_kwargs = {'password': {
            'write_only': True
        }}

    def validate(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        username_exist = User.objects.filter(username=username).exists()
        password_length = len(password)
        email_exist = User.objects.filter(email=email).exists()
        if username_exist:
            raise ValidationError({'username_err': '姓名已存在'})
        if password_length < 6:
            raise ValidationError({'password_err': '请输入六位以上密码'})
        if email_exist:
            raise ValidationError({'email_err': '邮箱已被注册'})
        return validated_data

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']

        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        user_profile = UserProfile(belong_to=user_obj, name=username, email=email)
        user_profile.save()
        Response(status=status.HTTP_200_OK)
        return validated_data


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
    email = serializers.EmailField()
    username = serializers.CharField(required=False)

    def validate(self, attrs):
        email = attrs.get('email')
        username = User.objects.filter(email=email).first()
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user or not username:
            raise ValidationError({'login_err': '用户名或密码错误'})

        attrs['user'] = user
        return attrs


class AnswerSerializer(ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'
        depth = 1


# 只序列化answer的id
class AnswerForCommentSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id']


class UserProfileSerializer(ModelSerializer):
    many = True
    user_vote_answer = AnswerForCommentSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'profile',
        ]


class TopicSerializer(ModelSerializer):

    class Meta:
        model = Topic
        fields = '__all__'
        depth = 1


class CommentParentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author']
        depth = 1


class CommentSerializer(ModelSerializer):
    answer = AnswerForCommentSerializer()
    parent = CommentParentSerializer()

    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'create_time', 'comment_reply_input', 'author', 'answer', 'parent'
        ]
        depth = 1


class QuestionSerializer(ModelSerializer):
    question_answer = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


# 只有question下级没有answer
class OnlyQuestionSerializer(ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'
        depth = 1
