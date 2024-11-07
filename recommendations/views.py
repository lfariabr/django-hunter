# recommendations/views.py

from django.shortcuts import render
from recommendations.algorithm import prepare_data_and_similarity, get_recommendations_multi  # Import algorithm
from recommendations.models import RequestLog
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RecommendationsViewSet(viewsets.ViewSet):
    # Ensuring only authenticated users can access
    permission_classes = [IsAuthenticated]  
    throtthle_classes = [UserRateThrottle]

    @swagger_auto_schema(
            method='POST',
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'procedures': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
                    'client_id': openapi.Schema(type=openapi.TYPE_STRING),
                    'client_name': openapi.Schema(type=openapi.TYPE_STRING),
                    'most_recent_appointment': openapi.Schema(type=openapi.TYPE_STRING),
                    'most_recent_purchase': openapi.Schema(type=openapi.TYPE_STRING),
                    'reference_code': openapi.Schema(type=openapi.TYPE_STRING),
                },
                required=['procedures'],
            ),
            responses={200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'status': openapi.Schema(type=openapi.TYPE_STRING)})},
    )

    # Using @action to use a custom endpoint
    @action(detail=False, methods=['POST'])
    def recommend(self, request):
        
        # Extracting the 'procedures' from the request body
        procedures = request.data.get('procedures', [])

        # Extra fields
        client_id = request.data.get('client_id', None)
        client_name = request.data.get('client_name', None)
        most_recent_appointment = request.data.get('most_recent_appointment', None)
        most_recent_purchase = request.data.get('most_recent_purchase', None)
        
        # Procedure ID, for example
        reference_code = request.data.get('reference_code', None)

        if not procedures:
            return Response({'status': 'No procedures provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare data and calculate similarities
        df, cosine_sim, indices = prepare_data_and_similarity()

        # Get the recommendations using the updated multi-procedure algorithm
        recommended_df = get_recommendations_multi(
            procedures=procedures,
            cosine_sim=cosine_sim,
            df=df,
            indices=indices,
            peso_similaridade=0.0,
            peso_custo=0.5,
            peso_queixa=0.5
        )

        recommended_procedures = recommended_df[['name', 'complaint']].to_dict(orient='records')

        # Log the incoming request and the recommendations
        log_entry = RequestLog.objects.create(
            client_id=client_id,
            client_name=client_name,
            most_recent_appointment=most_recent_appointment,
            most_recent_purchase=most_recent_purchase,
            reference_code=reference_code,
            procedures=procedures,
            recommended_procedures=recommended_procedures
        )

        # Send back the recommended procedures
        return Response(recommended_df.to_dict(orient='records'), status=status.HTTP_200_OK)