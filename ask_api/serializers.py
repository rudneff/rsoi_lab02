from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField

from ask_api.models import Question, Answer, CustomUser


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')


class UserDetailSerializer(serializers.ModelSerializer):
    questions = HyperlinkedRelatedField(many=True, read_only=True, view_name='questions-list')

    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number', 'email', 'questions')


class AnswerSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ('body', 'author', 'question', 'date')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    author = UserShortSerializer()

    class Meta:
        model = Question
        fields = ('title', 'body', 'author', 'date', 'answers')
