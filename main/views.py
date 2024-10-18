from rest_framework import viewsets, response, status
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.hashers import check_password
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
    
    def get_queryset(self):
        queryset = ProjetoVoluntario.objects.all()
        projeto_id = self.request.query_params.get('project')  # Obtém o parâmetro 'project' da URL
        if projeto_id:
            queryset = queryset.filter(projeto_id=projeto_id)  # Filtra pelo 'projeto_id' se for fornecido
        return queryset

    def create(self, request, *args, **kwargs):
        voluntarios = request.data.getlist("voluntario")
        projeto = request.data.get("projeto")

        for voluntario in voluntarios:
            voluntario_dict = json.loads(voluntario)
            content_type_str = voluntario_dict["content_type"]
            if content_type_str == "aluno":
                rm = voluntario_dict["id"]
                projeto_voluntario = ProjetoVoluntario(
                    projeto=Projeto.objects.get(id=projeto),
                    content_type=ContentType.objects.get(model=content_type_str),
                    object_id=rm
                )
            else:
                id = int(voluntario_dict["id"])
                projeto_voluntario = ProjetoVoluntario(
                    projeto=Projeto.objects.get(id=projeto),
                    content_type=ContentType.objects.get(model=content_type_str),
                    object_id=id)
            projeto_voluntario.save()
        
        return response.Response("escreveu nãoleu pau comeu", status=status.HTTP_201_CREATED)


            
                

    

class SugestaoViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = SugestaoSerializer
    queryset = Sugestao.objects.all()

    def create(self, request, *args, **kwargs):
        content_type = request.data.get("content_type")
        foto = request.data.get("foto")
        object_id = request.data.get("object_id")
        conteudo = request.data.get("conteudo")
        data_envio = request.data.get("data_envio")

        sugestao = Sugestao(
            foto = foto,
            content_type = ContentType.objects.get(model=content_type),
            object_id = object_id,
            conteudo = conteudo,
            data_envio = data_envio
        )

        sugestao.save()
        
        return response.Response(status=status.HTTP_201_CREATED)

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