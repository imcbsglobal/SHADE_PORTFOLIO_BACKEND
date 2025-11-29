from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Visitor, Smile, OurClient, Ceremonial, Demonstration  # ✅ Only these models
from .serializers import (
    VisitorSerializer,
    SmileSerializer,
    OurClientSerializer,
    CeremonialSerializer,
    DemonstrationSerializer,
)
import requests


# -------------------------------------------------------------------------
# WhatsApp API Helper
# -------------------------------------------------------------------------
def send_whatsapp_message(phone, message):
    url = "https://app.dxing.in/api/send/whatsapp"
    params = {
        "secret": "7b8ae820ecb39f8d173d57b51e1fce4c023e359e",
        "account": "1761365422812b4ba287f5ee0bc9d43bbf5bbe87fb68fc4daea92d8",
        "recipient": phone,
        "type": "text",
        "message": message,
        "priority": 1,
    }

    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print("WhatsApp Error:", e)
        return None


# -------------------------------------------------------------------------
# VISITOR REGISTRATION (Simple like Starstay)
# -------------------------------------------------------------------------
@csrf_exempt
@api_view(["POST", "GET"])
@permission_classes([AllowAny])
def visitor_list(request):
    if request.method == "GET":
        visitors = Visitor.objects.all().order_by("-id")
        return Response(VisitorSerializer(visitors, many=True).data)

    elif request.method == "POST":
        serializer = VisitorSerializer(data=request.data)
        if serializer.is_valid():
            visitor = serializer.save()

            # Send WhatsApp to Admin
            admin_number = "919072791379"
            message = (
                f"🔔 New Visitor - Shade 💚!\n\n"
                f"👤 Name: {visitor.name}\n"
                f"📱 Phone: {visitor.phone}\n"
                f"📧 Email: {visitor.email or 'Not provided'}\n\n"
                f"✅ Time: {visitor.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            )

            # Send WhatsApp notification
            whatsapp_response = send_whatsapp_message(admin_number, message)
            if whatsapp_response:
                print("✅ WhatsApp sent successfully:", whatsapp_response)
            else:
                print("❌ WhatsApp sending failed")

            # Store in session
            request.session["visitor_id"] = visitor.id
            request.session["visitor_name"] = visitor.name

            return Response(
                {"message": "Visitor registered successfully!", "visitor": VisitorSerializer(visitor).data},
                status=201
            )

        return Response(serializer.errors, status=400)


# -------------------------------------------------------------------------
# ADMIN LOGIN
# -------------------------------------------------------------------------
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def admin_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    ADMIN_USER = "imcbs"
    ADMIN_PASS = "1234"

    if username == ADMIN_USER and password == ADMIN_PASS:
        request.session["admin_logged_in"] = True
        return Response(
            {"message": "Admin login successful!", "token": "admin123token"},
            status=200
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
    visitors = Visitor.objects.all().order_by("-created_at").values(
        "id", "name", "phone", "email", "created_at"
    )

    return Response(
        {
            "total_visitors": Visitor.objects.count(),
            "visitors": list(visitors),
            "smiles": Smile.objects.count(),
            "clients": OurClient.objects.count(),
            "ceremonials": Ceremonial.objects.count(),
            "demonstrations": Demonstration.objects.count(),
        }
    )