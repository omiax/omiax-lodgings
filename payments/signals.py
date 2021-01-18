# https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
# modify -> "__init__.py and app.py" for signals to work


from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from django_q.tasks import async_task


import datetime
import requests
from environ import Env

from lodge.models import Room
from payments.models import Payment

env = Env()


@receiver(pre_save, sender=Payment, dispatch_uid="verfiy_payment")
def verify_payment(sender, instance, **kwargs):
    instance.rent_start_date = datetime.date.today()
    instance.rent_end_date = datetime.date.today() + datetime.timedelta(weeks=52)  # 47.9
    instance.terms_agreed = True
    instance.lodge_name = instance.lodge.name

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

    if instance.verified == "verified":

        Room.objects.filter(pk=instance.room_id, lodge=instance.lodge_id).update(
            tenant=instance.tenant_id,
            rent_start_date=instance.rent_start_date,
            rent_end_date=instance.rent_end_date,
            transaction_id=instance.transaction_id,
            terms_agreed=instance.terms_agreed,
            occupied=True,
        )

        async_task("payments.services.send_payment_sms", instance)

        async_task("payments.services.send_receipt", instance)
