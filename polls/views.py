from datetime import datetime

from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Answer, Poll, Question

from .serializers import (ActivePollsSerializer,
                          AnswersQuestionsSerializer,
                          AnswerSerializer,
                          PutAnswerSerializer,
                          PollAllSerializer,
                          PollPatchSerializer,
                          PollSerializer,
                          QuestionSerializer,
                          )


class PollViewSet(viewsets.ModelViewSet):
    """
    Возвращает полный список опросов вне зависимости от активности
    для редактирования/удаления ответа необходимо указать ../poll/poll_id/
    В момент создания опроса:
    - время старта - задается текущее время 
    - дата окончания - Null.
    Доступен только Администратору.
    """
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
        """ 
        Эндпоинт для завершения опроса.
        Эедпоинт закрывает опрос по текущему времени.
        Доступен только Администратору.
        """
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
            'End poll by PATCH command',
            status=status.HTTP_405_METHOD_NOT_ALLOWED
            )


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Полный список вопросов.
    При создании вопроса необходимо в теле запроса передать id опроса,
    в который будет включен этот вопрос.
    При создании/редактировании необходимо указать тип запроса 'type':
    TXT - Ответ текстом
    CH1 - Выбор одного
    CHM - Выбор нескольких
    Доступен только Администратору.
    """

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = QuestionSerializer


class QwestionsByPollViewSet(viewsets.ModelViewSet):
    """
    Список вопросов конкретного проса.
    В url необходимо прописать id опроса.
    При создании вопроса автоматически проставится id опроса.
    При создании/редактировании необходимо указать тип запроса 'type':
    TXT - Ответ текстом
    CH1 - Выбор одного
    CHM - Выбор нескольких
    Доступен только Администратору.
    """

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
    """
    Эндпоит списка ответов. Просмотр, создание, редактирование всех ответов.
    Доступен только Администратору.
    Для создания необходимо передать в теле запроса:
        - 'poll' id опроса
        - 'question' id вопроса
        - 'text' ответ в текстовом формате
    для редактирования/удаления ответа необходимо указать ../answer/answer_id/
    Пользователь проставится автоматически.
    Если неавторизованный пользователь, то значение Null
    """

    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = [permissions.IsAdminUser]


class AnswerByPollViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin):
    """
    Возвращает список ответов по вопросу конкретного опроса.
    Доступен Администратору
    """

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
    """ Возвращает список активных вопросов. Доступен каждому """
    serializer_class = ActivePollsSerializer
    queryset = Poll.objects.filter(is_active=True)
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
def answer_question(request):
    """
    Эндпоинт для ответа.
    Для ответа необходимо передать в теле запроса:
        - 'poll' id опроса
        - 'question' id вопроса
        - 'text' ответ в текстовом формате
    Пользователь проставится автоматически.
    Если неавторизованный пользователь, то значение Null
    """
    if request.method == 'POST':
        serializer = PutAnswerSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.pk:
                serializer.save()
            else:
                serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GetPollsByUserView(viewsets.GenericViewSet,
                         mixins.ListModelMixin):
    """ 
    Возвращает список ответов текущего пользователя.
    Только для авторизованных пользователей
     """
    serializer_class = AnswersQuestionsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        answers = Answer.objects.filter(user=user)
        return answers
