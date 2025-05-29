from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse  # ✅ Use this, not django.urls.reverse
from .models import Choice  # import Choice model
from .serializers import ChoiceSerializer  # import the serializer
from .models import Question, PollComment
from .serializers import QuestionSerializer, PollCommentSerializer

class ChoiceList(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = []

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PollCommentList(generics.ListCreateAPIView):
    queryset = PollComment.objects.all()
    serializer_class = PollCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'questions': reverse('polls_api:question-list', request=request, format=format),
        'choices': reverse('polls_api:choice-list', request=request, format=format),
        'comments': reverse('polls_api:comment-list', request=request, format=format),
    })
