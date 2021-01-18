from notification.models import Notification


def delete_expired_notifications():
    '''
    Check and delete every notification that was created one month ago!
    should run monthly

    command
    -------
    python manage.py shell
    from django_q.models import Schedule
    Schedule.objects.create(
        name='expired_notifications'
        func='notification.tasks.delete_expired_notifications',
        schedule_type=Schedule.MONTHLY,
        repeats=-1
    )
    '''

    expired_notifications = Notification.objects.filter(created_at__month__gt=1)
    expired_notifications.delete()
