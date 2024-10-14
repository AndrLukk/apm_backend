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

class ProjetoVoluntarioSerializer(serializers.ModelSerializer):
    voluntario_info = serializers.SerializerMethodField()

    class Meta:
        model = ProjetoVoluntario
        fields = ['id', 'projeto', 'voluntario_info']

    def get_voluntario_info(self, obj):
        if obj.content_type.model == 'funcionario':
            return FuncionarioSerializer(obj.voluntario).data
        elif obj.content_type.model == 'aluno':
            return AlunoSerializer(obj.voluntario).data
        return None

class ProjetoSerializer(serializers.ModelSerializer):
    voluntarios = ProjetoVoluntarioSerializer(many=True, read_only=True)
    
    class Meta:
        model = Projeto
        fields = "__all__"

class SugestaoSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False)

    class Meta:
        model = Sugestao
        fields = "__all__"