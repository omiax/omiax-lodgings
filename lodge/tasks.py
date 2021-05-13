from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

import datetime


from lodge.models import Room
from notification.models import Notification, StaffNotificationList

import requests
from environ import Env

env = Env()


# https://mattsegal.dev/simple-scheduled-tasks.html


def check_expired_rooms():
    """
    Check for rooms with three months to expiry dates
    should run monthly

    command
    -------
    python manage.py shell
    from django_q.models import Schedule
    Schedule.objects.create(
        name='expired_rooms'
        func='lodge.tasks.delete_expired_rooms',
        schedule_type=Schedule.MONTHLY,
        repeats=-1
    )

    """

    # print("I room every month..!")

    staff_list = StaffNotificationList.objects.all()
    tenants_list = []

    # within_three_months = Room.objects.filter(rent_end_date__month__lte=3)

    today_date = datetime.date.today()
    # three_from_today = datetime.date(today_date.year, today_date.month+3, 1)
    three_from_today = datetime.datetime.now() + datetime.timedelta(days=90)
    within_three_months = Room.objects.filter(rent_end_date__month__range=(today_date.month, three_from_today.month))

    if within_three_months:
        for room in within_three_months:

            # Generate Notification for each tenant
            n = Notification(receiver=room.tenant,
                             topic="Payment Verification",
                             message=f"Your Room is due to expire. Let us know, if you which to continue with us!")
            n.save()

            tenants_list.append(f'{room.lodge.name}, room {room.room_number} - \
                                {room.tenant.first_name} {room.tenant.last_name} - {room.tenant.phone_number} | \
                                    {room.rent_start_date} - {room.rent_end_date}.')

            # send receipt in email
            if "@temp-email.com" not in room.tenant.email:
                subject = "Omiax Apartments [Rent Reminder]"
                message = f"Your Rent for room: {room.room_number} at {room.lodge.name} is due to expire!"
                emails = [room.tenant.email]

                send_mail(subject, message, settings.EMAIL_HOST_USER, emails)

        if tenants_list:
            # SEND EMAIL
            # email tenants soon to expire details to staffs
            subject = "Omiax Apartments [Rent Reminder]"
            message = '\n'.join(map(str, tenants_list))
            emails = [s.email for s in staff_list]
            send_mail(subject, message, settings.EMAIL_HOST_USER, emails)

            # SEND SMS
            # send sms message of tenants soon to expire details to staffs
            payload = {"api_token": env("BULKSMS_TK"),
                       "from": "omiaxapartments.com",
                       "to": ','.join([s.phone_number for s in staff_list]),
                       "body": message,
                       "dnd": "2"}

            requests.get("https://www.bulksmsnigeria.com/api/v1/sms/create", params=payload)
