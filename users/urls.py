from users.views import UserSerializerClass 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/user', UserSerializerClass)
#LLamo las urlpatterns para que esta ruta pueda estar disponible para usarla en el url global del proyecto
urlpatterns = router.urls