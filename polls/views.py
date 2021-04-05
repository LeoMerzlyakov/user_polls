from django.contrib.auth.models import AnonymousUser

from datetime import datetime

from rest_framework import viewsets, status, permissions, mixins, views
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from django.contrib.auth.models import User


from .models import Poll, Question, Answer

from .serializers import (PollAllSerializer,
                          QuestionSerializer,
                          PollSerializer,
                          PollPatchSerializer,
                          AnswerSerializer,
                          ActivePollsSerializer,
                          PutAnswerSerializer,
                          AnswersQuestionsSerializer
                          )

class PollViewSet(viewsets.ModelViewSet):
    """List/create/updete/delete/  all polls"""
    queryset = Poll.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(time_start=datetime.now())
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PollSerializer
        return PollAllSerializer 

    
    @action(methods=['PATCH'],
            detail=True,
            permission_classes=[permissions.IsAdminUser],
            url_path='end_poll',
            url_name='end_poll')
    def end_poll(self, request, pk=None):
        """ End the poll comand """
        if request.method == 'PATCH':
            poll = get_object_or_404(Poll, pk=pk)
            poll_serializer = PollPatchSerializer(
                poll,
                data=request.data,
                partial=True
            )
            if poll_serializer.is_valid(raise_exception=True):
                poll = poll_serializer.save(time_end=datetime.now(),
                                            is_active=False
                                            )
                return Response(
                    poll_serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                poll_serializer.data,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'End poll by PATCH command', status=status.HTTP_405_METHOD_NOT_ALLOWED
            )


class QuestionViewSet(viewsets.ModelViewSet):
    """List/create/updete/delete/ questions"""

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = QuestionSerializer


class QwestionsByPollViewSet(viewsets.ModelViewSet):
    """List/create/updete/delete/ questions"""

    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        poll_id = self.kwargs['poll_id']
        if get_object_or_404(Poll, pk=poll_id):
            queryset = Question.objects.filter(poll=poll_id)
            return queryset

    def perform_create(self, serializer):
        poll_id = self.kwargs['poll_id']
        serializer.save(poll=poll_id)


class AnswerViewSet(viewsets.ModelViewSet):
    """List/create/updete/delete/ all Answer"""

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAdminUser]

class AnswerByPollViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin):
    """List of Answers"""

    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        poll_id = self.kwargs['poll_id']
        question_id = self.kwargs['question_id']
        if get_object_or_404(Poll, pk=poll_id):
            if Poll.objects.filter(questions__pk=question_id).exists():
                queryset = Answer.objects.filter(poll=poll_id,
                                                 question=question_id)
                return queryset


class ActivePollsViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin):
    serializer_class = ActivePollsSerializer
    queryset = Poll.objects.filter(is_active=True)
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
def answer_question(request):
    if request.method == 'POST':
        serializer = PutAnswerSerializer(data=request.data) 
        if serializer.is_valid():
            if request.user.pk == None:
                serializer.save()
            else:
                serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class GetPollsByUserView(viewsets.GenericViewSet,
                         mixins.ListModelMixin):
    serializer_class = AnswersQuestionsSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        answers = Answer.objects.filter(user=user)
        return answers

