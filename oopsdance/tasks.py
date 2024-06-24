from celery import shared_task
from django.core.management import call_command

@shared_task
def update_attendance():
    from io import StringIO
    from django.core.management import get_commands, load_command_class

    # Load the command
    app_name = get_commands()['update_attendance']
    command = load_command_class(app_name, 'update_attendance')

    # Capture output
    out = StringIO()
    command.stdout = out

    # Call the command
    messages = command.handle()
    
    # Print to log
    out.seek(0)
    print(out.read())

    return messages
    
@shared_task
def update_student_attendance():
    call_command('update_student_attendance')
    print("Student attendance updated for today")