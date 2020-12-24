# https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
# modify -> "__init__.py and app.py" for signals to work


from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

from django.http import HttpResponse


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

from smtplib import SMTPException


import os
import datetime
import requests
from environ import Env

from lodge.models import Room
from payments.models import Payment

env = Env()
User = get_user_model()

file_path = os.path.join(settings.STATIC_ROOT, "logo/OmiaxLogo-x2.png")


def createReceiptPDF(name, lodge, amount, transaction_id, start_date, end_date):
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
                name="Date", fontName="Times-Italic", fontSize=12, alignment=TA_RIGHT
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


@receiver(pre_save, sender=Payment, dispatch_uid="verfiy_payment")
def verify_payment(sender, instance, **kwargs):
    instance.rent_start_date = datetime.date.today()
    instance.rent_end_date = datetime.date.today() + datetime.timedelta(weeks=52)
    instance.terms_agreed = True

    if instance.manual_pay:
        pass
    else:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + env("SECK"),
        }
        payload = {"tx_ref": instance.transaction_id}
        # payload = {'tx_ref': '99ddc860-3939-11eb-a50a-092a1a8aa8bc'}
        r = requests.get(env("TRANSAC_URL"), headers=headers, params=payload)

        transac = r.json()
        # print(env("SECK"))

        if transac["data"]:
            # some maybe useful data
            instance.ip_address = transac["data"][0]["ip"]
            instance.created_at = transac["data"][0]["created_at"]
            instance.amount_settled = transac["data"][0]["amount_settled"]
            instance.payment_type = transac["data"][0]["payment_type"]
            instance.customer_id = transac["data"][0]["customer"]["id"]
            instance.account_id = transac["data"][0]["account_id"]
            instance.app_fee = transac["data"][0]["app_fee"]
            instance.merchant_fee = transac["data"][0]["merchant_fee"]
            instance.tenant_name = transac["data"][0]["customer"]["name"]

            if transac["data"][0]["flw_ref"] == instance.payment_ref:
                if transac["data"][0]["status"] == instance.status:
                    if transac["data"][0]["currency"] == instance.currency:
                        if transac["data"][0]["charged_amount"] == instance.amount:
                            instance.verified = "verified"


@receiver(post_save, sender=Payment, dispatch_uid="book_room")
def book_room(sender, instance, created, **kwargs):
    # Actually Book the room
    if created:
        if instance.verified == "verified":
            Room.objects.filter(pk=instance.room_id, lodge=instance.lodge_id).update(
                tenant=instance.tenant_id,
                rent_start_date=instance.rent_start_date,
                rent_end_date=instance.rent_end_date,
                transaction_id=instance.transaction_id,
                terms_agreed=instance.terms_agreed,
                occupied=True,
            )

            # send receipt email here
            # name, lodge, amount, transaction_id, start_date, end_date
            user = User.objects.get(id=instance.tenant_id)
            user_full_name = f"{user.first_name} {user.last_name}"

            subject = "Omiax Apartments [Receipt]"
            message = "The receipt of your recent payment is attached below"
            emails = [user.email]

            mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, emails)
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
