from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from main.views import *

router = routers.DefaultRouter()
router.register("funcionarios", FuncionarioViewSet, basename="funcionarios")
router.register("alunos", AlunoViewSet, basename="alunos")
router.register("responsaveis", ResponsavelViewSet, basename="responsaveis")
router.register("dependentes", ResponsavelDependenteViewSet, basename="dependentes")
router.register("doacoes", DoacaoViewSet, basename="doacoes")
router.register("soma-doacoes", SomaDoacoesAPIView.as_view(), basename="soma-doacoes")
router.register("projetos", ProjetoViewSet, basename="projetos")
router.register("voluntarios", ProjetoVoluntarioViewSet, basename="voluntarios")
router.register("sugestoes", SugestaoViewSet, basename="sugestoes")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path('login-funcionario', FuncionarioTokenView.as_view(), name='custom_token_obtain_pair'),
    path('login-responsavel', ResponsavelTokenView.as_view(), name='custom_token_obtain_pair'),
    path('login-aluno', AlunoTokenView.as_view(), name='custom_token_obtain_pair'),
    path('logout/', FuncionarioLogoutView.as_view(), name ='token_delet'),
    path('verify/', verifyToken.as_view(), name='verify')
]
