from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from main.views import *

router = routers.DefaultRouter()
router.register("funcionarios", FuncionarioViewSet, basename="funcionarios")
router.register("alunos", AlunoViewSet, basename="alunos")
router.register("responsaveis", ResponsavelViewSet, basename="responsaveis")
router.register("doacoes", DoacaoViewSet, basename="doacoes")
router.register("projetos", ProjetoViewSet, basename="projetos")
router.register("projetovoluntarios", ProjetoVoluntarioViewSet, basename="projetovoluntario")
router.register("sugestoes", SugestaoViewSet, basename="sugestoes")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls))
]
