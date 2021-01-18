from django.core import management


def flush_expired_tokens():
    """
    Flush expired access and refresh tokens from database
    should run daily

    command
    -------
    python manage.py shell
    from django_q.models import Schedule
    Schedule.objects.create(
        name='expired_tokens'
        func='user.tasks.delete_expired_tokens',
        schedule_type=Schedule.DAILY,
        repeats=-1
    )
    """

    management.call_command('flushexpiredtokens')
