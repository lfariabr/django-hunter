from rest_framework import serializers
from .models import ServedAppointments
from procedures.models import Procedure

# Serializers are used to convert
# Django models into JSON to be rendered in APIs

class ServedAppointmentsSerializer(serializers.ModelSerializer):
    procedure = serializers.SlugRelatedField(slug_field='name', queryset=Procedure.objects.all(), many=True)
    
    class Meta:
        model = ServedAppointments
        fields = '__all__'

    def create(self, validated_data):
        procedures_data = validated_data.pop('procedure')
        user = self.context['request'].user
        served_appointment = ServedAppointments.objects.create(user=user, **validated_data)
        served_appointment.procedure.set(procedures_data)
        return served_appointment