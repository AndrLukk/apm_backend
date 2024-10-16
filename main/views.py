from rest_framework import viewsets, response, status
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import authenticate

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

        if not voluntarios:
            return Response({"error": "Voluntários não fornecidos"}, status=status.HTTP_400_BAD_REQUEST)

    # Processar voluntários
        try:
            for voluntario in voluntarios:
            # Aqui você deve processar o voluntário, por exemplo, validá-lo ou salvá-lo
            print(voluntario)  # Verifique se você está recebendo os dados corretamente

            return Response({"message": "Voluntários processados com sucesso"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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