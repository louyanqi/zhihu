from rest_framework.serializers import ModelSerializer
from site_page.models import (User, UserProfile, Topic, Question, Answer, Comment)


# 只序列化answer的id
class AnswerForCommentSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id']


class UserProfileSerializer(ModelSerializer):

    user_vote_answer = AnswerForCommentSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


# 只有question下级没有answer
class OnlyQuestionSerializer(ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'
        depth = 1


class AnswerSerializer(ModelSerializer):
    author = UserProfileSerializer()
    question = OnlyQuestionSerializer()

    class Meta:
        model = Answer
        fields = ['id', 'question', 'author', 'user_vote', 'abstract', 'like_counts'
                  , 'answer_comments', 'comment_counts', 'create_time']


class AnswerDetailSerializer(ModelSerializer):
    author = UserProfileSerializer()
    question = OnlyQuestionSerializer()

    class Meta:
        model = Answer
        fields = ['id', 'question', 'author', 'user_vote', 'content', 'like_counts'
                  , 'answer_comments', 'comment_counts', 'create_time']


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


class CommentUserSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'avatar']


class ReplyCommentSerializer(ModelSerializer):
    comment_user = CommentUserSerializer()
    parent = CommentUserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_ip', 'comment_user', 'create_time', 'parent']
        depth = 1


class ChildCommentSerializer(ModelSerializer):
    comment_user = CommentUserSerializer()
    reply_to = ReplyCommentSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_ip', 'comment_user', 'create_time', 'parent', 'reply_to']
        depth = 1


class CommentSerializer(ModelSerializer):
    comment_user = CommentUserSerializer()
    belong_to = AnswerForCommentSerializer()
    child_comments = ChildCommentSerializer(many=2, )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_ip', 'comment_user', 'create_time', 'belong_to', 'child_comments']
        depth = 1


class QuestionSerializer(ModelSerializer):
    question_answer = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


