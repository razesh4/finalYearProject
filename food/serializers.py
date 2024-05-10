from rest_framework import serializers
from .models import person_details,nutrition_details,namaste
# Create your serializers here

class serializer_person_details(serializers.ModelSerializer):
    class Meta:
        model = person_details
        fields = '__all__'

class serializer_nutrition_details(serializers.ModelSerializer):
    class Meta:
        model = nutrition_details
        fields = '__all__'

class serializer_namaste(serializers.ModelSerializer):
    class Meta:
        model = namaste
        fields = '__all__'