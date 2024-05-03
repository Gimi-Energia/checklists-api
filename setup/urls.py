from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenRefreshView

from apps.checklists.views import ChecklistViewSet, ProductViewSet
from apps.checklistsA.views import ChecklistAViewSet
from apps.checklistsB.views import ChecklistBViewSet
from apps.checklistsC.views import ChecklistCViewSet
from apps.checklistsD.views import ChecklistDViewSet
from apps.checklistsE.views import ChecklistEViewSet
from apps.checklistsF.views import ChecklistFViewSet
from apps.checklistsG.views import ChecklistGViewSet
from apps.registrations.views import RegistrationViewSet
from utils.token import CustomTokenObtainPairView

schema_view = get_schema_view(
    openapi.Info(
        title="Checklists API",
        default_version="v1",
        description="API Rest",
        terms_of_service="#",
        contact=openapi.Contact(email="dev2@engenhadev.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r"api/checklists", ChecklistViewSet, basename="checklist")
router.register(r"api/products", ProductViewSet, basename="product")
router.register(r"api/registrations", RegistrationViewSet, basename="registration")
router.register(r"api/checklist/a", ChecklistAViewSet, basename="checklists-a")
router.register(r"api/checklist/b", ChecklistBViewSet, basename="checklists-b")
router.register(r"api/checklist/c", ChecklistCViewSet, basename="checklists-c")
router.register(r"api/checklist/d", ChecklistDViewSet, basename="checklists-d")
router.register(r"api/checklist/e", ChecklistEViewSet, basename="checklists-e")
router.register(r"api/checklist/f", ChecklistFViewSet, basename="checklists-f")
router.register(r"api/checklist/g", ChecklistGViewSet, basename="checklists-g")

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("", include("apps.users.urls")),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token-obtain"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
