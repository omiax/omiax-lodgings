from rest_framework import serializers

from payments import models


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        # fields = "__all__"
        fields = [
            'payment_image',
            'tenant',
            'room',
            'lodge',
            'transaction_id',
            'payment_ref',
            'status',
            'currency',
            'amount',
            'payment_plan',
            'manual_pay',
            'rent_start_date',
            'rent_end_date',
            'verified',
            'room',
            'lodge_name'
        ]
