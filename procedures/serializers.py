from rest_framework import serializers
from .models import Procedure, Favorite

# Why Use Serializers?

# • Convert Django Models to JSON: 
#  It allows you to render Django models into 
# a JSON format that can be transmitted over HTTP.

# • Validation: 
# Serializers validate the incoming data, 
# ensuring that the data conforms to model fields.

# • Deserialization: 
# It converts JSON data from an API request into a format 
# that can be saved in the database.

class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

