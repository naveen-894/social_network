from rest_framework.throttling import UserRateThrottle
class UserBaseThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if request.user:
            ident = request.user.id
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

class FriendRequestThrottle(UserBaseThrottle):
    scope = "friend_request"
     
