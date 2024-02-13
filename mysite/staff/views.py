from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.response import Response
from .models import Profile

# Create your views here.
@require_POST
@csrf_exempt
def creatUser(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    is_staff = request.POST.get('is_staff')
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username, email, password, is_staff=is_staff, is_active=True)
        if is_staff:
            return creatStaff(request, u)
        return JsonResponse(u, status=201)
    else:
        return HttpResponse("Username already exists.", status=400)
@require_POST
@csrf_exempt
def creatStaff(request, user):
    staff = Profile(user=user)
    staff.save()
    return Response({'user':user, 'staff': staff}, status=201)