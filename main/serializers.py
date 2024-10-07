from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

class FuncionarioSerializer(serializers.ModelSerializer):
    rf = serializers.CharField(read_only=False)
    senha = serializers.CharField(write_only=True)

    class Meta:
        model = Funcionario
        fields = "__all__"

    def create(self, validated_data):
        validated_data['senha'] = make_password(validated_data['senha'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'senha' in validated_data:
            validated_data['senha'] = make_password(validated_data['senha'])
        return super().update(instance, validated_data)

class AlunoSerializer(serializers.ModelSerializer):
    rm = serializers.CharField(read_only=False)
    senha = serializers.CharField(write_only=True)

    class Meta:
        model = Aluno
        fields = "__all__"

    def create(self, validated_data):
        validated_data['senha'] = make_password(validated_data['senha'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'senha' in validated_data:
            validated_data['senha'] = make_password(validated_data['senha'])
        return super().update(instance, validated_data)

class ResponsavelSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=False)
    senha = serializers.CharField(write_only=True)

    class Meta:
        model = Responsavel
        fields = "__all__"

    def create(self, validated_data):
        validated_data['senha'] = make_password(validated_data['senha'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'senha' in validated_data:
            validated_data['senha'] = make_password(validated_data['senha'])
        return super().update(instance, validated_data)

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