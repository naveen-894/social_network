from django.contrib.auth.hashers import check_password
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import User, FriendRequest
from .serializers import UserSerializer, UserSignupSerializer, FriendRequestSerializer
from .throttles import FriendRequestThrottle
from .utils import generate_token
from .authentications import CryptoJWTAuthentication
from .permissions import IsUser
from .paginations import StandardResultsSetPagination
class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT token
        token=generate_token({'id':str(user.id)})
        response_data = {
            "token": token,
            "user": {
                "id": user.id,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                # Generate JWT token
                token=generate_token({'id':str(user.id)})
                response_data = {
                    "token": token,
                    "user": {
                        "id": user.id,
                    }
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes=[CryptoJWTAuthentication]
    permission_classes=[IsUser]

    def get_queryset(self):
        keyword = self.request.query_params.get('search', '').strip().lower()
        if '@' in keyword:
            return User.objects.filter(email__iexact=keyword).exclude(email=self.request.user.email)
        else:
            return User.objects.filter(Q(name__icontains=keyword)).exclude(name__iexact=self.request.user.name)

class FriendRequestViewSet(viewsets.ViewSet):
    pagination_class = StandardResultsSetPagination
    authentication_classes = [CryptoJWTAuthentication]
    
    def send_request(self, request, pk=None):
        throttler=FriendRequestThrottle()
        if not throttler.allow_request(request, view=None):
            return Response({'details': 'Too Many Requests'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        from_user = request.user
        to_user = User.objects.get(pk=pk)
        if from_user != to_user:
            friend_request, created = FriendRequest.objects.get_or_create(
                from_user=from_user, to_user=to_user, defaults={'status': 'pending'})
            if created:
                return Response({'status': 'Request Sent'})
            else:
                return Response({'status': 'Request Already Sent'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Cannot send request to yourself'}, status=status.HTTP_400_BAD_REQUEST)

    
    def respond_request(self, request, pk=None):
        response = request.data.get('response')
        try:
            friend_request = FriendRequest.objects.get(from_user=request.user,to_user=pk, status='pending')
            if friend_request.to_user != request.user:
                if response == 'accept':
                    friend_request.status = 'accepted'
                elif response == 'reject':
                    friend_request.status = 'rejected'
                else:
                    return Response({'error': 'Not a valid action'}, status=status.HTTP_400_BAD_REQUEST)
                friend_request.save()
                return Response(FriendRequestSerializer(friend_request).data)
            else:
                return Response({'error': 'Not authorized to respond to this request'}, status=status.HTTP_403_FORBIDDEN)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend Request Not Found'}, status=status.HTTP_404_NOT_FOUND)


  
    def list_friends(self, request):
        friends = FriendRequest.objects.filter(
            Q(from_user=request.user,status='accepted')
        )
        return Response(FriendRequestSerializer(friends, many=True).data)

    def pending_requests(self, request):
        pending_requests = FriendRequest.objects.filter(from_user=request.user, status='pending')
        return Response(FriendRequestSerializer(pending_requests, many=True).data)