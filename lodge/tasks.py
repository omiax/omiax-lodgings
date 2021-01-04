from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


from lodge.models import Room

# https://mattsegal.dev/simple-scheduled-tasks.html


def check_expired_rooms():
    """
    Check for rooms with three months to expiry dates
    should run monthly
    """

    print("I room every minute..!")
    # tenants_list = []

    # within_three_months = Room.objects.filter(rent_end_date__month__lte=3)

    # if within_three_months:
    #     for room in within_three_months:
    #         tenants_list.append(f'{room.lodge.name}, room {room.room_number} - \
    #                             {room.tenant.username}, {room.tenant.email} - {room.tenant.phone_number}')

    #         subject = "Omiax Apartments [Rent Reminder]"
    #         message = f"Your Rent for room: {room.room_number} at {room.lodge.name} is due to expire!"
    #         emails = [room.tenant.email]

    #         send_mail(subject, message, settings.EMAIL_HOST_USER, emails)

    # if tenants_list:
    #     subject = "Omiax Apartments [Rent Reminder]"
    #     message = '\n'.join(map(str, tenants_list))
    #     emails = ['idy@idudoh.com']
    #     send_mail(subject, message, settings.EMAIL_HOST_USER, emails)
