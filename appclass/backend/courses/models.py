from django.db import models
from users.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    user = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
class Question(models.Model):
    course = models.ForeignKey(Course, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.course.title} - {self.text[:50]}"


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'✔️' if self.is_correct else '✖️'})"


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.FloatField()
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Certificado - {self.user.username} - {self.course.title}"
