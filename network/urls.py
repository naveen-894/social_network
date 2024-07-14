from django.urls import path
from .views import UserSignupView, UserSearchView, FriendRequestViewSet,UserLoginView


urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('friend-requests/<uuid:pk>', FriendRequestViewSet.as_view({'post': 'send_request'}), name='friend-request'),
    path('friends/', FriendRequestViewSet.as_view({'get': 'list_friends',}), name='friend-request-list'),
    path('friend-requests/pending/', FriendRequestViewSet.as_view({'get': 'pending_requests',}), name='pending-requests'),
    path('friend-requests/<uuid:pk>/respond/', FriendRequestViewSet.as_view({'post': 'respond_request',}), name='respond-request'),
]
