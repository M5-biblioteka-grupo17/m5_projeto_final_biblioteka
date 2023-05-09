from rest_framework import serializers

from .models import Copy
from .models import Loan

from users.serializers import UserSerializer

from datetime import date, timedelta


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = ["id", "book_id", "available"]
        read_only_fields = ["available"]


class LoanSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ["id", "user", "copy", "start_date", "return_date", "is_returned"]
        read_only_fields = ["id", "user", "copy", "start_date", "return_date", "is_returned"]

    def create(self, validated_data):
        return_date = date.today() + timedelta(days=2)

        if return_date.strftime("%a") == "Sat":
            return_date = return_date + timedelta(days=2)
        if return_date.strftime("%a") == "Sun":
            return_date = return_date + timedelta(days=1)

        return Loan.objects.create(**validated_data, return_date=return_date)

    def update(self, instance: Loan, validated_data):
        instance.copy.available = True
        instance.copy.save()

        instance.is_returned = True
        instance.save()
        return_date = instance.return_date
        if return_date < date.today():
            instance.user.have_permission = date.today() + timedelta(days=2)
            instance.user.save()

        return instance
