from rest_framework import viewsets, response, status

from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from rest_framework.views import APIView
import json

from datetime import date

class FuncionarioViewSet(viewsets.ModelViewSet):
    serializer_class = FuncionarioSerializer
    queryset = Funcionario.objects.all()

class AlunoViewSet(viewsets.ModelViewSet):
    serializer_class = AlunoSerializer
    queryset = Aluno.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        rm = self.request.query_params.get('rm')
        if rm:
            queryset = queryset.filter(rm=rm)
        return queryset

    def list(self, request, *args, **kwargs):
        rm = request.query_params.get('rm')

        # Se tiver RM, faz a verificação de idade
        if rm:
            try:
                aluno = Aluno.objects.get(rm=rm)
                serializer = self.get_serializer(aluno)

                # Cálculo da idade (assumindo campo data_nascimento)
                hoje = date.today()
                idade = (
                    hoje.year - aluno.data_nasc.year
                    - ((hoje.month, hoje.day) < (aluno.data_nasc.month, aluno.data_nasc.day))
                )

                return Response({
                    "aluno": serializer.data,
                    "maior_de_idade": idade >= 18
                })

            except Aluno.DoesNotExist:
                return Response({"erro": "Aluno não encontrado."}, status=404)

        # Se não tiver RM, retorna lista normal
        return super().list(request, *args, **kwargs)

class AlunoTokenView(APIView):

    def post(self, request, *args, **kwargs):
        rm = request.data.get('rm')
        senha = request.data.get('senha')

        try:
            aluno = Aluno.objects.get(rm=rm)
            if aluno.check_password(senha):
                token, created = AlunoToken.objects.get_or_create(aluno=aluno)
                
                return Response({
                    'token': str(token.token),
                    'message': 'Autenticação bem-sucedida'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        except Aluno.DoesNotExist:
            return Response({'error': 'Aluno não encontrado'}, status=status.HTTP_404_NOT_FOUND)

class ResponsavelViewSet(viewsets.ModelViewSet):
    serializer_class = ResponsavelSerializer
    queryset = Responsavel.objects.prefetch_related('dependentes').all()

    def get_queryset(self):
        queryset = super().get_queryset()
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(email=email)
        return queryset

class ResponsavelTokenView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        senha = request.data.get('senha')

        try:
            responsavel = Responsavel.objects.get(email=email)
            if responsavel.check_password(senha):
                token, created = ResponsavelToken.objects.get_or_create(responsavel=responsavel)
                
                return Response({
                    'token': str(token.token),
                    'message': 'Autenticação bem-sucedida'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        except Responsavel.DoesNotExist:
            return Response({'error': 'Responsável não encontrado'}, status=status.HTTP_404_NOT_FOUND)

class ResponsavelDependenteViewSet(viewsets.ModelViewSet):
    serializer_class = ResponsavelDependenteSerializer

    def get_queryset(self):
        queryset = ResponsavelDependente.objects.all()
        responsavel_id = self.request.query_params.get('responsavel')
        if responsavel_id:
            queryset = queryset.filter(responsavel=responsavel_id)
        return queryset
    
    def create(self, request):
        dependentes = request.data.getlist("dependente")
        responsavel = request.data.get("responsavel")

        for dependente_id in dependentes:
            new_dependente = ResponsavelDependente(
                responsavel=Responsavel.objects.get(id=responsavel),
                dependente=Aluno.objects.get(rm=dependente_id)
            )
            new_dependente.save()
        
        return response.Response("Dependentes salvos", status=status.HTTP_201_CREATED)
                


class DoacaoViewSet(viewsets.ModelViewSet):
    serializer_class = DoacaoSerializer
    queryset = Doacao.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        cpf = self.request.query_params.get('cpf')
        
        if cpf:
            alunos_com_cpf = Aluno.objects.filter(cpf=cpf)
            responsaveis_com_cpf = Responsavel.objects.filter(cpf=cpf)

            doacoes_de_alunos = Doacao.objects.filter(aluno__in=alunos_com_cpf)

            doacoes_de_responsaveis = Doacao.objects.filter(responsavel__in=responsaveis_com_cpf)

            queryset = doacoes_de_alunos | doacoes_de_responsaveis

        return queryset

class SomaDoacoesAPIView(APIView):

    def get(self, request, *args, **kwargs):
        total_doacoes = Doacao.objects.aggregate(total=models.Sum('valor'))['total']
        
        if total_doacoes is None:
            total_doacoes = 0.0
        
        return Response({"total_doacoes": total_doacoes}, status=status.HTTP_200_OK)

class ProjetoViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ProjetoSerializer
    queryset = Projeto.objects.prefetch_related('voluntarios').all()

class ProjetoVoluntarioViewSet(viewsets.ModelViewSet):
    serializer_class = ProjetoVoluntarioSerializer

    def get_queryset(self):
        queryset = ProjetoVoluntario.objects.all()
        projeto_id = self.request.query_params.get('projeto')
        if projeto_id:
            queryset = queryset.filter(projeto_id=projeto_id)
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
        
        return response.Response("Voluntários salvos", status=status.HTTP_201_CREATED)

class SugestaoViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = SugestaoSerializer
    queryset = Sugestao.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        content_type = self.request.query_params.get("content_type")
        object_id = self.request.query_params.get("object_id")
 
        if content_type and object_id:
            try:
                ct = ContentType.objects.get(model=content_type)
                queryset = queryset.filter(content_type=ct, object_id=object_id)
            except ContentType.DoesNotExist:
                queryset = queryset.none()

        return queryset

    def create(self, request, *args, **kwargs):
        content_type = request.data.get("content_type")
        foto = request.data.get("foto")
        object_id = request.data.get("object_id")
        conteudo = request.data.get("conteudo")
        data_envio = date.today()

        sugestao = Sugestao(
            foto = foto,
            content_type = ContentType.objects.get(model=content_type),
            object_id = object_id,
            conteudo = conteudo,
            data_envio = data_envio
        )

        sugestao.save()
        
        return response.Response(status=status.HTTP_201_CREATED)

class FuncionarioTokenView(APIView):

    def post(self, request, *args, **kwargs):
        rf = request.data.get('rf')
        senha = request.data.get('senha')

        try:
            funcionario = Funcionario.objects.get(rf=rf)
            if funcionario.check_password(senha):
                token, created = FuncionarioToken.objects.get_or_create(funcionario=funcionario)
                
                return Response({
                    'token': str(token.token),
                    'message': 'Autenticação bem-sucedida'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        except Funcionario.DoesNotExist:
            return Response({'error': 'Funcionário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

class FuncionarioLogoutView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization')
        if token:
            try:
                if token.startswith("Bearer "):
                    token = token[7:]
                funcionario_token = FuncionarioToken.objects.get(token=token)
                funcionario_token.delete()
                return Response({'message': 'Logout bem-sucedido'}, status=status.HTTP_200_OK)
            except FuncionarioToken.DoesNotExist:
                return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Token não encontrado'}, status=status.HTTP_400_BAD_REQUEST)


class verifyToken(APIView):
    def get(self, request):
        return Response({},status=200)