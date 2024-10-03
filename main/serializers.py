from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

class FuncionarioSerializer(serializers.ModelSerializer):
    rf = serializers.CharField(read_only=True)

    class Meta:
        model = Funcionario
        fields = "__all__"

    def create(self, cleanedData):
        cleanedData['senha'] = make_password(cleanedData['senha'])
        return super().create(cleanedData)

    def update(self, instance, cleanedData):
        if 'senha' in cleanedData:
            cleanedData['senha'] = make_password(cleanedData['senha'])
        return super().update(instance, cleanedData)

class AlunoSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)

    class Meta:
        model = Aluno
        fields = "__all__"

    def create(self, cleanedData):
        cleanedData['senha'] = make_password(cleanedData['senha'])
        return super().create(cleanedData)

    def update(self, instance, cleanedData):
        if 'senha' in cleanedData:
            cleanedData['senha'] = make_password(cleanedData['senha'])
        return super().update(instance, cleanedData)

class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = "__all__"

    def create(self, cleanedData):
        cleanedData['senha'] = make_password(cleanedData['senha'])
        return super().create(cleanedData)

    def update(self, instance, cleanedData):
        if 'senha' in cleanedData:
            cleanedData['senha'] = make_password(cleanedData['senha'])
        return super().update(instance, cleanedData)

class DoacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doacao
        fields = "__all__"

class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = "__all__"

class SugestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sugestao
        fields = "__all__"