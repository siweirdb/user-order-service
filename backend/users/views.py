from django.views.generic import View
from .models import User
from django.http import JsonResponse, HttpResponseNotAllowed, Http404
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")

        if user_id:
            user = User.objects.filter(id=user_id).values().first()
            if user:
                return JsonResponse({'user': user})
            return JsonResponse({'error': 'User not found'}, status=404)
        else:
            return JsonResponse({'users': list(User.objects.values())})

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        age = data.get("age")

        if not name:
            return JsonResponse({"error": "Name is required"}, status=400)
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)
        try:
            age = int(age)
            if age < 0:
                return JsonResponse({"error": "Age cannot be less than 0"}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({"error": "Age must be a valid integer"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        User.objects.create(name=name, email=email, age=age)
        return JsonResponse({"message": "User successfully created"}, status=201)

    def patch(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        if not user_id:
            return HttpResponseNotAllowed(['PATCH'])

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        name = data.get("name")
        email = data.get("email")
        age = data.get("age")

        if name is not None:
            name = name.strip()
            if not name:
                return JsonResponse({"error": "Name cannot be empty"}, status=400)
            user.name = name

        if email is not None:
            email = email.strip()
            if not email:
                return JsonResponse({"error": "Email cannot be empty"}, status=400)
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return JsonResponse({"error": "Email already in use"}, status=400)
            user.email = email

        if age is not None:
            try:
                age = int(age)
                if age < 0:
                    return JsonResponse({"error": "Age must be non-negative"}, status=400)
                user.age = age
            except (ValueError, TypeError):
                return JsonResponse({"error": "Age must be a valid integer"}, status=400)

        user.save()
        return JsonResponse({"message": "User successfully updated"})



