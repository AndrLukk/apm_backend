from rest_framework import viewsets
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser


class FuncionarioViewSet(viewsets.ModelViewSet):
    serializer_class = FuncionarioSerializer
    queryset = Funcionario.objects.all()

class AlunoViewSet(viewsets.ModelViewSet):
    serializer_class = AlunoSerializer
    queryset = Aluno.objects.all()

class ResponsavelViewSet(viewsets.ModelViewSet):
    serializer_class = ResponsavelSerializer
    queryset = Responsavel.objects.all()

class DoacaoViewSet(viewsets.ModelViewSet):
    serializer_class = DoacaoSerializer
    queryset = Doacao.objects.all()

class ProjetoViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ProjetoSerializer
    queryset = Projeto.objects.all()

class SugestaoViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = SugestaoSerializer
    queryset = Sugestao.objects.all()