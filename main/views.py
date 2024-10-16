from rest_framework import viewsets, response, status
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import authenticate
import json

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
    queryset = Projeto.objects.prefetch_related('voluntarios').all()

class ProjetoVoluntarioViewSet(viewsets.ModelViewSet):
    serializer_class = ProjetoVoluntarioSerializer
    queryset = ProjetoVoluntario.objects.all()

    def create(self, request, *args, **kwargs):
        voluntarios = request.data.getlist("voluntario")
        projeto = request.data.get("projeto")

        for voluntario in voluntarios:
            voluntario_dict = json.loads(voluntario)
            rm = voluntario_dict["rm"]
            content_type_str = voluntario_dict["content_type"]

            projeto_voluntario = ProjetoVoluntario(
                projeto=Projeto.objects.get(id=projeto),
                content_type=ContentType.objects.get(model=content_type_str),
                object_id=rm,
            )
            projeto_voluntario.save()
        
        return response


            
                

    

class SugestaoViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = SugestaoSerializer
    queryset = Sugestao.objects.all()

class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        nome = request.data.get('nome')
        senha = request.data.get('senha')
        try:
            funcionario = Funcionario.objects.get(nome=nome)
            if check_password(senha, funcionario.senha):
                return response.Response({"message": "Login bem-sucedido!"}, status=status.HTTP_200_OK)
            else:
                return response.Response({"error": "Credenciais inválidas!"}, status=status.HTTP_401_UNAUTHORIZED)
        except Funcionario.DoesNotExist:
            return response.Response({"error": "Credenciais inválidas!"}, status=status.HTTP_401_UNAUTHORIZED)