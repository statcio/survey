from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from .models import Question, Option, Poll, Reply
from .serializers import OptionSerializer, ReplySerializer, QuestionSerializer, PollSerializer


@csrf_exempt
@api_view(["GET"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please enter username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Wrong data'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def polls_view(request):
    serializer = PollSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        poll = serializer.save()
        return Response(PollSerializer(poll).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def poll_detail_view(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'PATCH':
        serializer = PollSerializer(poll, data=request.data, partial=True)
        if serializer.is_valid():
            poll = serializer.save()
            return Response(PollSerializer(poll).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        poll.delete()
        return Response("Poll deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def current_poll_view(request):
    polls = Poll.objects.filter(end_date__gte=timezone.now()).filter(start_date__lte=timezone.now())
    serializer = PollSerializer(polls, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def poll_view(request):
    poll = Poll.objects.all()
    serializer = PollSerializer(poll, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def questions_view(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            Question.objects.create(**serializer.validated_data)
            return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def question_detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def options_view(request):
    serializer = OptionSerializer(data=request.data)
    if serializer.is_valid():
        option = serializer.save()
        return Response(OptionSerializer(option).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def option_detail_view(request, option_id):
    option = get_object_or_404(Option, pk=option_id)
    if request.method == 'PATCH':
        serializer = OptionSerializer(option, data=request.data, partial=True)
        if serializer.is_valid():
            option = serializer.save()
            return Response(OptionSerializer(option).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        option.delete()
        return Response("Option deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def reply_create(request):
    serializer = ReplySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        reply = serializer.save()
        return Response(ReplySerializer(reply).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def reply_view(request, user_id):
    replies = Reply.objects.filter(user_id=user_id)
    serializer = ReplySerializer(replies, many=True)
    return Response(serializer.data)


@api_view(['PATCH', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def reply_update(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.method == 'PATCH':
        serializer = ReplySerializer(reply, data=request.data, partial=True)
        if serializer.is_valid():
            reply = serializer.save()
            return Response(ReplySerializer(reply).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        reply.delete()
        return Response("Reply deleted", status=status.HTTP_204_NO_CONTENT)
