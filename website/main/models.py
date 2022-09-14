from django.db import models

# Create your models here.

class Student(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return "Student: " + str(self.id)

class Question(models.Model):
    question = models.TextField(blank=True, null=True, verbose_name = "Question")
    context = models.TextField(blank=True, null=True, verbose_name = "Context")
    ref_answer = models.TextField(blank=True, null=True, verbose_name = "Reference Answer")
    stu_answer = models.TextField(blank=True, null=True, verbose_name="Student Answer")
    auto_score_1 = models.FloatField(null=True, blank=True, verbose_name="Automatic score 1")
    auto_score_2 = models.FloatField(null=True, blank=True, verbose_name="Automatic score 2")
    auto_score_3 = models.FloatField(null=True, blank=True, verbose_name="Automatic score 3")
    marked_score = models.FloatField(null=True, blank=True, verbose_name="Marked Score")
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    is_answered = models.BooleanField(default=False, verbose_name="Answered")
    is_marked = models.BooleanField(default=False, verbose_name="Marked")

    def __str__(self):
        return "Question: " + self.question

