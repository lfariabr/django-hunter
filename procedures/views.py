from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Procedure
from .serializers import ProcedureSerializer
from recommendations.algorithm import prepare_data_and_similarity, get_recommendations_multi
from rest_framework.permissions import IsAuthenticated

# Create your views here.
    
class ProcedureViewSet(viewsets.ModelViewSet):
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated for these actions
    
    # # Route for retrieving recommended procedures based on appointments
    # @action(detail=False, methods=['POST'])
    # def recommended(self, request):
        
    #     # Log the incoming data to verify what is being received
    #     logging.info(f"Incoming request data: {request.data}")

    #     # Ensure we get the procedures from the request
    #     appointment_procedures = request.data.get('procedures', [])
        
    #     if not appointment_procedures:
    #         return Response({'status': 'No procedures provided'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Prepare the data for recommendations
    #     df, cosine_sim, indices = prepare_data_and_similarity()

    #     # Call the recommendation logic
    #     recommended_df = get_recommendations_multi(
    #         procedures=appointment_procedures,  # Pass the correct argument name
    #         cosine_sim=cosine_sim,
    #         df=df,
    #         indices=indices,
    #         peso_similaridade=0.3,
    #         peso_custo=0.5,
    #         peso_queixa=0.2
    #     )

    #     # Retrieve Procedure objects for the recommended IDs
    #     recommended_procedure_ids = recommended_df['id'].tolist()
    #     recommended_procedures = Procedure.objects.filter(id__in=recommended_procedure_ids)
    #     serializer = ProcedureSerializer(recommended_procedures, many=True)
        
    #     return Response(serializer.data, status=status.HTTP_200_OK)