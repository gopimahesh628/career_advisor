import json
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.conf import settings

from .utils import CustomSignUpForm
from .models import ChatSession, ChatMessage, UserProfile, QuizQuestion, QuizResult
from openai import OpenAI 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # set your API key in .env

@csrf_exempt
def ask_gpt(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            # GPT call
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # fast & cheap
                messages=[
                    {"role": "system", "content": "You are a helpful career guidance assistant."},
                    {"role": "user", "content": user_message}
                ]
            )

            reply = response.choices[0].message.content
            return JsonResponse({"reply": reply, "session_id": data.get("session_id", "new")})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required(login_url="auth")
def home(request):
    return render(request, "home.html")

def user_profile(request):
    # You can add logic here to pass user data to the template
    return render(request, 'user_profile.html')

def career_guide(request):
    return render(request, "career_guide.html")

def quiz_page(request):
    return render(request, "quiz.html")

def auth_page(request):
    login_form = AuthenticationForm()
    signup_form = CustomSignUpForm()

    if request.method == "POST":
        if "login_submit" in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("home")   # ✅ go to home after login
        elif "signup_submit" in request.POST:
            signup_form = CustomSignUpForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                return redirect("home")   # ✅ go to home after signup

    return render(request, "auth_page.html", {
        "login_form": login_form,
        "signup_form": signup_form
    })


def recommend_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("message", "").lower()
        session_id = data.get("session_id")

        # Find or create chat session
        if session_id:
            session = ChatSession.objects.filter(id=session_id).first()
        else:
            session = ChatSession.objects.create(title="New Chat")

        # Store user message
        ChatMessage.objects.create(session=session, sender="user", text=user_input)

        # --- Rule-based logic ---
        if "10th" in user_input or "ssc" in user_input:
            reply = "After 10th, you can choose: Intermediate (Science/Commerce/Arts), Diploma, or ITI."
        elif "inter" in user_input or "12th" in user_input:
            reply = "After Inter, you can go for Undergraduate degrees like B.Tech, B.Sc, B.Com, or BA."
        elif "ug" in user_input or "degree" in user_input:
            reply = "After UG, you can pursue PG (M.Tech, M.Sc, MBA, etc.)."
        elif "pg" in user_input or "masters" in user_input:
            reply = "After PG, you can aim for Research (PhD), Competitive Exams, or Jobs."
        else:
            reply = "I can help! Please tell me your current class or education stage."

        # Store bot message
        ChatMessage.objects.create(session=session, sender="bot", text=reply)

        return JsonResponse({"reply": reply, "session_id": session.id})

    return JsonResponse({"error": "Invalid request"}, status=400)


def get_chat_history(request, session_id):
    session = ChatSession.objects.get(id=session_id)
    messages = session.messages.all().order_by("timestamp")
    data = [{"sender": m.sender, "text": m.text} for m in messages]
    return JsonResponse({"messages": data, "title": session.title})


def list_chats(request):
    sessions = ChatSession.objects.all().order_by("-created_at")
    data = [{"id": s.id, "title": s.title} for s in sessions]
    return JsonResponse({"sessions": data})

def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Simple rule-based bot (expand later with ML)
        if "10th" in user_message.lower():
            reply = "After 10th, you can choose Inter, Diploma, or ITI."
        elif "inter" in user_message.lower():
            reply = "After Inter, you can choose UG courses like B.Sc, B.Com, or B.Tech."
        elif "ug" in user_message.lower():
            reply = "After UG, you can go for PG like MBA, M.Tech, or M.Sc."
        elif "pg" in user_message.lower():
            reply = "After PG, you can pursue PhD, research, or government exams."
        else:
            reply = "Tell me more about your education stage so I can guide you."

        return JsonResponse({"reply": reply})
    return JsonResponse({"error": "Invalid request"}, status=400)

def chat_sessions(request):
    sessions = ChatSession.objects.all().order_by("-created_at")
    return JsonResponse({
        "sessions": [{"id": s.id, "title": s.title or f"Chat {s.id}"} for s in sessions]
    })

# Get messages of a session
def chat_messages(request, session_id):
    messages = ChatMessage.objects.filter(session_id=session_id).order_by("timestamp")
    return JsonResponse({
        "messages": [
            {"id": m.id, "text": m.text, "sender": m.sender}
            for m in messages
        ]
    })

# Create a new chat session
@csrf_exempt
def new_chat(request):
    if request.method == "POST":
        session = ChatSession.objects.create(title="New Chat")
        return JsonResponse({"session_id": session.id})
    
@csrf_exempt
def recommend(request):
    import json
    from django.views.decorators.csrf import csrf_exempt

    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message")
        session_id = data.get("session_id")

        # Get or create chat session
        if session_id:
            session = ChatSession.objects.get(id=session_id)
        else:
            session = ChatSession.objects.create(title="New Chat")

        # Save user message
        ChatMessage.objects.create(session=session, sender="user", text=message)

        # If this is the first message → set it as the title
        if session.title == "New Chat":
            session.title = message[:30]  # limit length to 30 chars
            session.save()

        # Dummy bot reply for now
        reply = "I can help! Please tell me your current class or education stage."

        # Save bot reply
        ChatMessage.objects.create(session=session, sender="bot", text=reply)

        return JsonResponse({
            "session_id": session.id,
            "reply": reply
        })

@csrf_exempt
def delete_chat(request, session_id):
    if request.method == "DELETE":
        try:
            session = ChatSession.objects.get(id=session_id)
            session.delete()
            return JsonResponse({"success": True})
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Chat not found"}, status=404)
        
def save_chatbot_data(request):
    if request.method == "POST":
        data = request.POST
        profile = UserProfile.objects.create(
            age=data.get("age"),
            study=data.get("study"),
            interests=data.get("interests"),
            goal=data.get("goal"),
            project=data.get("project"),
        )
        return redirect("quiz", user_id=profile.id)  # Pass profile id

@csrf_exempt
def submit_quiz(request, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_profile = UserProfile.objects.get(id=user_id)

            result = QuizResult.objects.create(
                user_profile=user_profile,
                answers=data.get("answers"),
                recommended_field=data.get("recommended"),
            )

            return JsonResponse({"status": "success", "recommended": result.recommended_field})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})