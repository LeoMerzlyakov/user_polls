from rest_framework import serializers

from .models import Poll, Question, Answer


class PollSerializer(serializers.ModelSerializer):
    """Serializer for list Poll model."""
    class Meta:
        model = Poll
        exclude = ('time_start', 'time_end',)

class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model with default
       functional of ModelSerializer."""

    class Meta:
        model = Question
        fields = '__all__'

class PollAllSerializer(serializers.ModelSerializer):
    """Serializer for Poll model with default
       functional of ModelSerializer."""
    question_list = QuestionSerializer(required=False, many=True, source='questions')
    class Meta:
        model = Poll
        fields = '__all__'


class PollPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['is_active', 'time_end']


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for Question model with default
       functional of ModelSerializer."""

    poll = serializers.CharField(max_length=200, read_only=True)
    question = serializers.CharField(max_length=200, read_only=True)
    user = serializers.CharField(max_length=200, read_only=True)

    class Meta:
        model = Answer
        exclude = ('id',)

class PutAnswerSerializer(serializers.ModelSerializer):
    """Serializer for Question model with default
       functional of ModelSerializer."""

    class Meta:
        model = Answer
        exclude = ('id',)

class ActivePollsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['time_start', 'text']


class AnswersQuestionsSerializer(serializers.ModelSerializer):
    questios = QuestionSerializer(required=False,
                                       many=True)
    pool = QuestionSerializer(required=False,
                                       many=True)
                                       
    class Meta:
        model = Answer
        fields = '__all__'