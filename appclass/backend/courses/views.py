from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Course
from .models import Question, Certificate, Option, Enrollment
from django.utils import timezone
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from .serializers import CourseSerializer, QuestionSerializer
from .serializers import QuestionSerializer
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def course_list(request):
    courses = Course.objects.filter(is_active=True)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk, is_active=True)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response({"error": "Curso no encontrado."}, status=404)
    
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def course_quiz(request, pk):
    try:
        course = Course.objects.get(pk=pk)
        questions = course.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response({"error": "Curso no encontrado."}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def submit_quiz(request, pk):
    user = request.user
    answers = request.data.get('answers', {})

    try:
        course = Course.objects.get(pk=pk)
        questions = course.questions.all()

        correct = 0
        for question in questions:
            selected_id = answers.get(str(question.id))
            if selected_id:
                option = Option.objects.filter(id=selected_id, question=question).first()
                if option and option.is_correct:
                    correct += 1

        grade = round((correct / len(questions)) * 10, 2)

        # Verifica si ya tiene certificado previo
        cert_exists = Certificate.objects.filter(user=user, course=course).exists()
        if cert_exists:
            return Response({"message": "Ya tienes un certificado para este curso."}, status=400)

        # Si aprueba (nota >=7)
        if grade >= 7:
            cert = Certificate.objects.create(user=user, course=course, grade=grade)
            Enrollment.objects.filter(user=user, course=course).update(is_completed=True)
            return Response({"message": f"Aprobado con {grade}/10. Certificado generado."}, status=200)
        else:
            return Response({"message": f"Reprobado con {grade}/10. Debes obtener 7 o más."}, status=200)

    except Course.DoesNotExist:
        return Response({"error": "Curso no encontrado."}, status=404)
    
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def question_list(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)
