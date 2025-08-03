from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Order
from users.models import User
import json



@method_decorator(csrf_exempt, name='dispatch')
class OrderView(View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")

        if order_id:
            order = Order.objects.filter(id=order_id).values().first()
            if order:
                return JsonResponse({'order': order})
            return JsonResponse({'error': 'Order not found'}, status=404)
        else:
            return JsonResponse({'orders': list(Order.objects.values())})

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        user_id = data.get("user_id")
        name = data.get("name", "").strip()
        description = data.get("description", "").strip()

        if not user_id or not name or not description:
            return JsonResponse({"error": "user_id, name and description are required"}, status=400)

        if User.objects.filter(id=user_id).exists():
            user = User.objects.get(id=user_id)
        else:
            return JsonResponse({"error": "User not found"}, status=404)

        Order.objects.create(user=user, name=name, description=description)
        return JsonResponse({ "message": "Order created"}, status=201)

    def patch(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")
        if not order_id:
            return JsonResponse({"error": "Order_id is required"}, status=400)

        if Order.objects.filter(id=order_id).exists():
            order = Order.objects.get(id=order_id)
        else:
            return JsonResponse({"error": "Order not found"}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


        name = data.get("name")
        description = data.get("description")

        if name is not None:
            order.name = name.strip()
        if description is not None:
            order.description = description.strip()

        order.save()
        return JsonResponse({"message": "Order updated"})
