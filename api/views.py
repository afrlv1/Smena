from rest_framework.views import APIView
from django.http import JsonResponse, FileResponse
from .models import Printer, Check
from .serializers import CheckSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
import json
import django_rq
from .tasks import make_pdf


class GetCheck(APIView):
	permission_classes = (IsAuthenticatedOrReadOnly,)

	def post(self, request):
		order = json.loads(request.body.decode())
		all_printers = Printer.objects.filter(point_id=order['point_id'])
		if not all_printers:
			return JsonResponse({'error': "Для данной точки не настроено ни одного принтера"}, status=400)
		if Check.objects.filter(order__id=order['id']).exists():
			return JsonResponse({'error': "Для данного заказа уже созданы чеки"}, status=400)
		for printer in all_printers:
			new_check = Check.objects.create(printer_id=printer.id, check_type=printer.check_type, order=order)
			django_rq.enqueue(make_pdf, new_check.id)
		return JsonResponse({'ok': "Чеки успешно созданы"}, status=201)


def get(request, api_key):
	printer = Printer.objects.get(api_key=api_key)
	if not printer:
		return JsonResponse({'error': "Не существует принтера с таким api_key"}, status=401)
	checks = printer.checks_set.filter(status=Check.rendered).order_by('id')
	list_check = CheckSerializer(checks, many=True).data
	return JsonResponse({'checks': list_check})


class NewCheck(APIView):
	permission_classes = (IsAuthenticatedOrReadOnly,)


class PdfCheck(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, api_key, check_id):
		if not Printer.objects.filter(api_key=api_key).exists():
			return JsonResponse({'error': "Не существует принтера с таким api_key"}, status=401)
		check = Check.object.filter(check_id=check_id).first()
		if not check:
			return JsonResponse({'error': "Данного чека не существует"}, status=400)
		if not check.pdf_file:
			return JsonResponse({'error': "Для данного чека не сгенерирован PDF-файл"}, status=400)
		check.status = Check.printed
		check.save()
		return FileResponse(open(check.pdf_file.path, 'rb'))
