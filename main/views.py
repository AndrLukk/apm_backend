from rest_framework import viewsets
from .serializers import *

class FuncionarioViewSet(viewsets.ModelViewSet):
    serializer_class = FuncionarioSerializer
    queryset = Funcionario.objects.all()

class AlunoViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    serializer_class = AlunoSerializer
    queryset = Aluno.objects.all()

class ResponsavelViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    serializer_class = ResponsavelSerializer
    queryset = Responsavel.objects.all()

class DoacaoViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    serializer_class = DoacaoSerializer
    queryset = Doacao.objects.all()

class ProjetoViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    serializer_class = ProjetoSerializer
    queryset = Projeto.objects.all()

class SugestaoViewSet(EnablePartialUpdateMixin, viewsets.ModelViewSet):
    serializer_class = SugestaoSerializer
    queryset = Sugestao.objects.all()