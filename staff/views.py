from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, ProfileSerializer
from .models import Profile
from django.contrib.auth import login, authenticate

# Create your views here.
@csrf_exempt
@api_view(['POST'])
def creatUser(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    is_staff = request.POST.get('is_staff')
    item_start = request.POST.get('item_start')
    item_end = request.POST.get('item_end')
    item_version = request.POST.get('item_version')
    last_issued_number = request.POST.get('last_issued_number')
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username, email, password, is_staff=is_staff, is_active=True)
        if is_staff:
            return creatStaff(request._request, u, {
                "item_start": item_start,
                "item_end": item_end,
                "item_version": item_version,
                "last_issued_number": last_issued_number,
            })
        return JsonResponse(u, status=201)
    else:
        return HttpResponse("Username already exists.", status=400)
@csrf_exempt
@api_view(['POST'])
def creatStaff(request, user, data):
    staff = Profile(user=user, item_start=data['item_start'], item_end=data['item_end'],item_version=data['item_version'],last_issued_number=data['last_issued_number'],)
    print('staff', staff)
    staff.save()
    print('here')
    serializer_user = UserSerializer(user)
    serializer_staff = ProfileSerializer(staff)
    return Response({'user': serializer_user.data, 'staff': serializer_staff.data}, status=201)


@csrf_exempt
@api_view(['POST'])
def loginUser(request):
    json_data = request.data
    user = authenticate(request, username=json_data.get('username'), password=json_data.get('password'))
    if user is not None:
        staff = None
        if user.is_staff:
            staff = Profile.objects.get(user_id=user.id)
        # login(request, user)
            return Response({'status': 'success', 'user_id': user.id, 'staff_id': staff.id}, status=200)
        else:
            return Response({'status': 'success', 'user_id': user.id}, status=200)
    else:
        print('here')
        return Response('login failed.', status=403)
