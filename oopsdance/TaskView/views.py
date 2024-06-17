from django.http import JsonResponse
from ..tasks import update_attendance

def run_update_attendance_task(request):
    # Trigger the Celery task
    result = update_attendance.delay()
    return JsonResponse({'status': 'Task is being processed', 'task_id': result.id})