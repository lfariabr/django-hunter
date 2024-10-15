# recommendations/views.py

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from recommendations.algorithm import prepare_data_and_similarity, get_recommendations_multi  # Import algorithm
from recommendations.models import RequestLog

class RecommendationsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    @action(detail=False, methods=['POST'])
    def recommend(self, request):
        # Extract the 'procedures' from the request body
        procedures = request.data.get('procedures', [])

        # Extra fields
        procedures = request.data.get('procedures', [])
        client_id = request.data.get('client_id', None)
        client_name = request.data.get('client_name', None)
        most_recent_appointment = request.data.get('most_recent_appointment', None)
        most_recent_purchase = request.data.get('most_recent_purchase', None)

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
            procedures=procedures,
            recommended_procedures=recommended_procedures  # Log the recommendations
        )

        # Send back the recommended procedures
        return Response(recommended_df.to_dict(orient='records'), status=status.HTTP_200_OK)