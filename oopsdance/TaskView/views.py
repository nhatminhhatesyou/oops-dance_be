from django.http import JsonResponse
from ..tasks import update_attendance, update_student_attendance

def run_update_attendance_task(request):
    # Trigger the Celery task
    result = update_attendance.delay()

    # Wait for the task to complete
    result.wait()  # This will block until the task finishes
    
    # Fetch the result (messages)
    messages = result.result
    
    return JsonResponse({'status': 'Task completed', 'messages': messages, 'task_id': result.id})

def update_student_attendance_view(request):
    update_student_attendance.delay()  # Call the Celery task with .delay()
    return JsonResponse({"status": "Student attendance update task started for today."})