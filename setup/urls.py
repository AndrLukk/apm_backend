from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from main.views import *

router = routers.DefaultRouter()
router.register("funcionarios", FuncionarioViewSet, basename="funcionarios")
router.register("alunos", AlunoViewSet, basename="alunos")
router.register("responsavel", ResponsavelViewSet, basename="responsavel")
router.register("doacao", DoacaoViewSet, basename="doacao")
router.register("projeto", ProjetoViewSet, basename="projeto")
router.register("sugestao", SugestaoViewSet, basename="sugestao")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls))
]
