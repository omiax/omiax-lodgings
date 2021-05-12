from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

from django.http import HttpResponse
from smtplib import SMTPException


# from PIL import Image
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

import os
import datetime
import requests
from environ import Env

from notification.models import Notification

env = Env()

User = get_user_model()

# https://www.bulksmsnigeria.com/api/v1/sms/create?api_token=1LyRVE2FndEpDpNOzuamaTrc02pP5wEoHXK4T8ne4ciM37VSjSVu1Xpkyjk1&from=BulkSMS.ng&to=2348071501239&body=Welcome&dnd=2
file_path = os.path.join(settings.STATIC_ROOT, "logo/OmiaxLogo-x2.png")


def createReceiptPDF(name, lodge, amount, transaction_id, start_date, end_date):
    # Generate transaction Receipt in memory and email to tenant
    buffer = BytesIO()

    date = datetime.date.today()
    # end_date = datetime.date.today() + datetime.timedelta(weeks=52)

    info = """
    Remember not to sublet or transfer your room, shop or any portion of the
    premises to any one without the consent of the Landloard or Collector.
    When leaving, the keys must be submitted to the Landlord or Collector
    incharge.
    """

    data = [
        ["Received from:", name.title()],
        ["Property:", lodge.title()],
        ["Paid:", str(amount) + " Naira"],
        ["Transaction Ref:", transaction_id],
        ["Start Date:", start_date.strftime("%d-%m-%Y")],
        ["End Date:", end_date.strftime("%d-%m-%Y")],
    ]

    pdf = SimpleDocTemplate(
        buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=20, bottomMargin=6
    )

    table = Table(data)

    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
            ("LINEABOVE", (0, 0), (2, 0), 2, colors.purple),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("ALIGN", (0, 0), (0, -1), "RIGHT"),
            ("ALIGN", (1, 0), (1, -1), "LEFT"),
            ("SIZE", (0, 0), (-1, -1), 14),
            ("FACE", (0, 0), (0, -1), "Helvetica-Bold"),
        ]
    )
    table.setStyle(style)

    elems = []

    elems.append(Image(file_path, 4 * cm, 2 * cm, hAlign="CENTER"))

    elems.append(
        Paragraph(
            "Omiax Accommodations",
            ParagraphStyle(
                name="Omiax",
                fontName="Times-Bold",
                fontSize=30,
                alignment=TA_CENTER,
                textColor=colors.purple,
            ),
        )
    )

    elems.append(Spacer(1, 40))

    elems.append(
        Paragraph(
            "Rent Receipt",
            ParagraphStyle(
                name="Rent",
                fontName="Times-BoldItalic",
                fontSize=20,
                alignment=TA_CENTER,
            ),
        )
    )

    elems.append(
        Paragraph(
            "Date: " + date.strftime("%d-%m-%Y"),
            ParagraphStyle(
                name="Date",
                fontName="Times-Italic",
                fontSize=12,
                alignment=TA_RIGHT
            ),
        )
    )

    elems.append(Spacer(2, 40))
    elems.append(table)
    elems.append(Spacer(1, 35))

    elems.append(
        Paragraph(
            info,
            ParagraphStyle(
                name="Omiax",
                fontName="Courier-Bold",
                fontSize=12,
                alignment=TA_CENTER,
                rightIndent=0,
                textColor=colors.red,
            ),
        )
    )

    pdf.build(elems)

    res = buffer.getvalue()
    buffer.close()
    return res


def send_payment_sms(instance):
    '''Send text message to tenant for verified payments to tenant'''
    # send confirmation of sms

    body = f"Your payment of {instance.amount} for {instance.lodge.name} \
    from {instance.rent_start_date} to {instance.rent_end_date} is confirmed"

    payload = {"api_token": env("BULKSMS_TK"),
               "from": "omiaxapartments.com",
               "to": instance.tenant.phone_number,
               "body": body,
               "dnd": "2"}

    requests.get("https://www.bulksmsnigeria.com/api/v1/sms/create", params=payload)


def send_receipt(instance):
    '''
    send email with receipt attached for verified payments to tenant

    Parameters
    ----------
    instance : object
        payment instance
    '''
    # send receipt in notification

    n = Notification(receiver=instance.tenant,
                     topic="Payment Verification",
                     message=f"Your payment for {instance.lodge.name} of {instance.amount} Naira is confirmed")
    n.save()

    # send receipt in email
    if "@temp-email.com" not in instance.tenant.email:
        # user = User.objects.get(id=instance.tenant_id)
        user_full_name = f"{instance.tenant.first_name} {instance.tenant.last_name}"

        subject = "Omiax Apartments [Receipt]"
        message = "The receipt of your recent payment is attached below"
        emails = [instance.tenant.email]

        mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, emails)
        # name, lodge, amount, transaction_id, start_date, end_date
        pdf = createReceiptPDF(
            user_full_name,
            instance.lodge.name,
            instance.amount,
            instance.transaction_id,
            instance.rent_start_date,
            instance.rent_end_date,
        )

        mail.attach("Receipt.pdf", pdf, "application/pdf")
        try:
            mail.send(fail_silently=False)
        except SMTPException:
            return HttpResponse("Mail Not Sent")
