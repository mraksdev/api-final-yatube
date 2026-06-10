from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)

from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet)
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')
router_v1.register('groups', GroupViewSet)
router_v1.register('follow', FollowViewSet)

jwt_patterns = [
    path('create/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(),
         name='token_verify'),
]

v1_patterns = [
    path('', include(router_v1.urls)),
    path('jwt/', include(jwt_patterns)),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]
