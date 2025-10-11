from django.http import JsonResponse
from django.urls import resolve, Resolver404
from django.utils.deprecation import MiddlewareMixin
from .models import FuncionarioToken, ResponsavelToken, AlunoToken

class FuncionarioTokenMiddleware(MiddlewareMixin):
    # URLs de login isentas de autenticação
    exempt_urls = ['/login-funcionario', '/login-responsavel', '/login-aluno']

    def process_request(self, request):
        # Se a URL for uma das URLs de login, não realiza autenticação
        if request.path in self.exempt_urls or request.path.startswith('/admin/'):
            return None
        
        try:
            resolve(request.path)  # Verifica se a URL existe
        except Resolver404:
            return JsonResponse({'error': 'Rota não encontrada'}, status=404)
        
        # Verificar o token de autenticação
        token = request.headers.get('Authorization')
        if token:
            try:
                if token.startswith("Bearer "):
                    token = token[7:]  # Remove o prefixo "Bearer "

                # Verifica se o token é de Funcionario
                if request.path == '/login-funcionario':  
                    funcionario_token = FuncionarioToken.objects.get(token=token)
                    if funcionario_token.is_valid():
                        request.funcionario = funcionario_token.funcionario
                    else:
                        return JsonResponse({'error': 'Token expirado'}, status=401)

                # Verifica se o token é de Responsavel
                elif request.path == '/login-responsavel':
                    responsavel_token = ResponsavelToken.objects.get(token=token)
                    if responsavel_token.is_valid():
                        request.responsavel = responsavel_token.responsavel
                    else:
                        return JsonResponse({'error': 'Token expirado'}, status=401)

                # Verifica se o token é de Aluno
                elif request.path == '/login-aluno':
                    aluno_token = AlunoToken.objects.get(token=token)
                    if aluno_token.is_valid():
                        request.aluno = aluno_token.aluno
                    else:
                        return JsonResponse({'error': 'Token expirado'}, status=401)

            except (FuncionarioToken.DoesNotExist, ResponsavelToken.DoesNotExist, AlunoToken.DoesNotExist):
                return JsonResponse({'error': 'Token inválido'}, status=401)
        else:
            return JsonResponse({'error': 'Autorização necessária'}, status=401)