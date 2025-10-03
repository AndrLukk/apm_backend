from django.http import JsonResponse
from django.urls import resolve, Resolver404, reverse
from django.utils.deprecation import MiddlewareMixin
from .models import FuncionarioToken

class FuncionarioTokenMiddleware(MiddlewareMixin):
    exempt_urls = ['/login-funcionario', '/login-responsavel']

    def process_request(self, request):

        if request.path in self.exempt_urls or request.path.startswith('/admin/'):
            return None
        
        try:
            resolve(request.path)
        except Resolver404:
            return JsonResponse({'error': 'Rota não encontrada'}, status=404)
        
        token = request.headers.get('Authorization')
        if token:
            try:
                if token.startswith("Bearer "):
                    token = token[7:]
                funcionario_token = FuncionarioToken.objects.get(token=token)
                if funcionario_token.is_valid():
                    request.funcionario = funcionario_token.funcionario
                else:
                    return JsonResponse({'error': 'Token expirado'}, status=401)
            except FuncionarioToken.DoesNotExist:
                return JsonResponse({'error': 'Token inválido'}, status=401)
        else:
            return JsonResponse({'error': 'Autorização necessária'}, status=401)
