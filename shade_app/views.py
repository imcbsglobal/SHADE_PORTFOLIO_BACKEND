from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User as DjangoUser
from .models import User, Smile, OurClient, Ceremonial, LoginHistory, Demonstration
from .serializers import (
    UserSerializer,
    SmileSerializer,
    OurClientSerializer,
    CeremonialSerializer,
    LoginHistorySerializer,
    DemonstrationSerializer,
)
import requests


# -------------------------------------------------------------------------
# Helper: Get IP
# -------------------------------------------------------------------------
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


# -------------------------------------------------------------------------
# WhatsApp API Credentials
# -------------------------------------------------------------------------
WHATSAPP_API_URL = "https://app.dxing.in/api/send/whatsapp"
SECRET = "7b8ae820ecb39f8d173d57b51e1fce4c023e359e"
ACCOUNT = "1761365422812b4ba287f5ee0bc9d43bbf5bbe87fb68fc4daea92d8"
ADMIN_PHONE = "919072791379"


# -------------------------------------------------------------------------
# VISITOR REGISTRATION (Auto Login if Existing)
# -------------------------------------------------------------------------
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def register_visitor(request):
    data = request.data
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()

    if not name or not phone:
        return Response({"error": "Name and phone are required"}, status=400)

    # Auto Login if phone exists
    existing = User.objects.filter(phone=phone).first()
    if existing:
        request.session["visitor_id"] = existing.id
        request.session["visitor_name"] = existing.name

        return Response(
            {
                "message": "Login successful",
                "user": {
                    "id": existing.id,
                    "name": existing.name,
                    "phone": existing.phone,
                    "email": existing.email,
                },
            },
            status=200,
        )

    try:
        # Create new user
        user = User.objects.create(name=name, phone=phone, email=email)

        # WhatsApp Notification
        message = (
            f"📢 New User Registered - Shade 💚!\n\n"
            f"👤 Name: {name}\n"
            f"📞 Phone: {phone}\n"
            f"📧 Email: {email if email else 'Not provided'}"
        )

        params = {
            "secret": SECRET,
            "account": ACCOUNT,
            "recipient": ADMIN_PHONE,
            "type": "text",
            "message": message,
            "priority": 1,
        }

        try:
            requests.post(WHATSAPP_API_URL, params=params, timeout=5)
        except Exception as e:
            print("WhatsApp Error:", e)

        # Store in session
        request.session["visitor_id"] = user.id
        request.session["visitor_name"] = user.name

        return Response(
            {
                "message": "Registration successful",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "phone": user.phone,
                    "email": user.email,
                },
            },
            status=201,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# -------------------------------------------------------------------------
# VISITOR LOGIN
# -------------------------------------------------------------------------
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    phone = request.data.get("phone", "").strip()

    if not phone:
        return Response({"error": "Phone number is required"}, status=400)

    try:
        user = User.objects.get(phone=phone)

        request.session["visitor_id"] = user.id
        request.session["visitor_name"] = user.name

        return Response(
            {
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "phone": user.phone,
                    "email": user.email,
                },
            },
            status=200,
        )

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


# -------------------------------------------------------------------------
# ADMIN LOGIN
# -------------------------------------------------------------------------
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def admin_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    ip_address = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")

    if username == "imcbs" and password == "1234":
        user, created = DjangoUser.objects.get_or_create(
            username="imcbs", defaults={"is_staff": True, "is_superuser": True}
        )

        LoginHistory.objects.create(
            user=user,
            username="imcbs",
            ip_address=ip_address,
            user_agent=user_agent,
            status="success",
        )

        request.session["user_id"] = user.id
        request.session["username"] = "imcbs"

        return Response(
            {"message": "Admin login successful", "user": {"id": user.id, "username": "imcbs"}},
            status=200,
        )

    LoginHistory.objects.create(
        user=None,
        username=username or "unknown",
        ip_address=ip_address,
        user_agent=user_agent,
        status="failed",
    )

    return Response({"error": "Invalid admin credentials"}, status=401)


# -------------------------------------------------------------------------
# SMILES API
# -------------------------------------------------------------------------
@csrf_exempt
@api_view(["GET", "POST"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([AllowAny])
def smile_list(request):
    if request.method == "GET":
        smiles = Smile.objects.all()
        return Response(SmileSerializer(smiles, many=True).data)

    serializer = SmileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([AllowAny])
def smile_detail(request, pk):
    try:
        smile = Smile.objects.get(pk=pk)
    except Smile.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.method == "GET":
        return Response(SmileSerializer(smile).data)

    if request.method in ["PUT", "PATCH"]:
        serializer = SmileSerializer(smile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    smile.delete()
    return Response({"message": "Deleted"}, status=204)


# -------------------------------------------------------------------------
# OUR CLIENTS API
# -------------------------------------------------------------------------
@csrf_exempt
@api_view(["GET", "POST"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([AllowAny])
def client_list(request):
    if request.method == "GET":
        clients = OurClient.objects.all()
        return Response(OurClientSerializer(clients, many=True).data)

    serializer = OurClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([AllowAny])
def client_detail(request, pk):
    try:
        client = OurClient.objects.get(pk=pk)
    except OurClient.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.method == "GET":
        return Response(OurClientSerializer(client).data)

    if request.method in ["PUT", "PATCH"]:
        serializer = OurClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    client.delete()
    return Response({"message": "Deleted"}, status=204)


# -------------------------------------------------------------------------
# CEREMONIAL API
# -------------------------------------------------------------------------
@csrf_exempt
@api_view(["GET", "POST"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([AllowAny])
def ceremonial_list(request):
    if request.method == "GET":
        ceremonials = Ceremonial.objects.all()
        return Response(CeremonialSerializer(ceremonials, many=True).data)

    serializer = CeremonialSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([AllowAny])
def ceremonial_detail(request, pk):
    try:
        ceremonial = Ceremonial.objects.get(pk=pk)
    except Ceremonial.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.method == "GET":
        return Response(CeremonialSerializer(ceremonial).data)

    if request.method in ["PUT", "PATCH"]:
        serializer = CeremonialSerializer(ceremonial, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    ceremonial.delete()
    return Response({"message": "Deleted"}, status=204)


# -------------------------------------------------------------------------
# DEMONSTRATIONS API
# -------------------------------------------------------------------------
@csrf_exempt
@api_view(["GET", "POST"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([AllowAny])
def demonstration_list(request):
    if request.method == "GET":
        demonstrations = Demonstration.objects.all()
        return Response(DemonstrationSerializer(demonstrations, many=True).data)

    serializer = DemonstrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([AllowAny])
def demonstration_detail(request, pk):
    try:
        demonstration = Demonstration.objects.get(pk=pk)
    except Demonstration.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.method == "GET":
        return Response(DemonstrationSerializer(demonstration).data)

    if request.method in ["PUT", "PATCH"]:
        serializer = DemonstrationSerializer(demonstration, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    demonstration.delete()
    return Response({"message": "Deleted"}, status=204)


# -------------------------------------------------------------------------
# DASHBOARD DATA
# -------------------------------------------------------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def dashboard_data(request):
    visitors = User.objects.all().order_by("-created_at").values(
        "id", "name", "phone", "email", "created_at"
    )

    return Response(
        {
            "total_visitors": User.objects.count(),
            "visitors": list(visitors),
            "smiles": Smile.objects.count(),
            "clients": OurClient.objects.count(),
            "ceremonials": Ceremonial.objects.count(),
            "demonstrations": Demonstration.objects.count(),
            "login_history": LoginHistorySerializer(LoginHistory.objects.all()[:20], many=True).data,
        }
    )
