from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return (User.objects.create_superuser(**validated_data) if validated_data["library_collaborator"]
               else User.objects.create_user(**validated_data))
    
    def update(self, instance:User, validated_data:dict):
        for key, value in validated_data.items():
            if key== "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()   

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )        
    class Meta:
        model=User
        fields=[
            "id",
            "usernames",
            "email",
            "password",
            "first_name",
            "last_name",
            "created_at",
            "updated_at",
            "library_collaborator",
            "have_permission"
        ]
        extra_kwargs={
            "password":{"write_only": True}
        }