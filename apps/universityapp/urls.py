from rest_framework import routers
from .views import UniversityViewSet

router = routers.DefaultRouter()
router.register('university', UniversityViewSet)

urlpatterns = []
urlpatterns += router.urls
