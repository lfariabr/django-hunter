from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Procedure, Favorite
from .serializers import ProcedureSerializer
from .recommendation.recommendation_engine import prepare_data_and_similarity, get_recommendations_multi


# Create your views here.

class ProcedureViewSet(viewsets.ModelViewSet):
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Route for favoriting a procedure
    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk=None):
        procedure = self.get_object()
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            procedure=procedure,
        )
        if created:
            return Response({'status': 'Procedure added to favorites'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Procedure already in favorites'}, status=status.HTTP_200_OK)
    
    # Route for unfavoriting a procedure
    @action(detail=True, methods=['DELETE'])
    def unfavorite(self, request, pk=None):
        procedure = self.get_object()
        favorite = Favorite.objects.filter(
            user=request.user,
            procedure=procedure,
        ).first()
        if favorite:
            favorite.delete()
            return Response({'status': 'Procedure removed from favorites'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Procedure not found in favorites'}, status=status.HTTP_404_NOT_FOUND)

    # Route for listing user favorites
    @action(detail=False, methods=['GET'])
    def favorites(self, request):
        favorites = Favorite.objects.filter(user=request.user).values_list('procedure', flat=True)
        procedures = Procedure.objects.filter(id__in=favorites)
        serializer = ProcedureSerializer(procedures, many=True)
        return Response(serializer.data)
    
    # Route for retrieving recommended procedures
    @action(detail=False, methods=['GET'])
    def recommended(self, request):
        
        # user_favorites = Favorite.objects.filter(user=request.user).values_list('procedure', flat=True)
        # if not user_favorites:
        #     return Response({'status': 'No favorites found'}, status=status.HTTP_404_NOT_FOUND)

        # # Fetch the favorite procedures
        # favorite_procedures = Procedure.objects.filter(id__in=user_favorites)
    
        # # Call the recommendation logic
        # recommended = calculate_recommendations(favorite_procedures)
    
        # serializer = ProcedureSerializer(recommended, many=True)
        # return Response(serializer.data)
        
        # Prepare the data for recommendations
        df, cosine_sim, indices = prepare_data_and_similarity()
        
        # Get the user's favorite procedures
        user_favorites = Favorite.objects.filter(user=request.user).values_list('procedure__name', flat=True)
        if not user_favorites:
            return Response({'status': 'No favorites found'}, status=status.HTTP_404_NOT_FOUND)

        # Call the recommendation logic
        recommended_df = get_recommendations_multi(
            procedimentos=user_favorites,
            cosine_sim=cosine_sim,
            df=df,
            indices=indices,
            peso_similaridade=0.3,
            peso_custo=0.5,
            peso_queixa=0.2
        )

        # Retrieve Procedure objects for the recommended IDs
        recommended_procedure_ids = recommended_df['id'].tolist()
        recommended_procedures = Procedure.objects.filter(id__in=recommended_procedure_ids)
        serializer = ProcedureSerializer(recommended_procedures, many=True)
        
        return Response(serializer.data)