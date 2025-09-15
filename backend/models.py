from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # Data from chatbot
    age = models.CharField(max_length=10, blank=True, null=True)
    study = models.CharField(max_length=100, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    goal = models.CharField(max_length=200, blank=True, null=True)
    project = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"UserProfile {self.id} - {self.study}"


class QuizQuestion(models.Model):
    question_text = models.TextField()
    options = models.JSONField()  # Store as ["opt1","opt2","opt3"]
    fields = models.JSONField()   # Store mapped fields like ["Data Science","AI","Cybersecurity"]

    def __str__(self):
        return self.question_text[:50]

class QuizResult(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="quiz_results")
    answers = models.JSONField()  # Store user choices { "Q1": "AI", "Q2": "Management" }
    recommended_field = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for User {self.user_profile.id} - {self.recommended_field}"


class ChatSession(models.Model):
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    session = models.ForeignKey("ChatSession", related_name="messages", on_delete=models.CASCADE)
    sender = models.CharField(max_length=10, choices=[("user", "User"), ("bot", "Bot")])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 