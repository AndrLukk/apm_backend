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
    
class ResponsavelDependenteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResponsavelDependente
        fields = "__all__"

class ResponsavelSerializer(serializers.ModelSerializer):
    dependentes = ResponsavelDependenteSerializer(many=True, read_only=True)
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
        if obj.voluntario is None:
            return {'error': 'Voluntário não encontrado'}

        if obj.content_type.model == 'responsavel':
            return {
                'id_obj': obj.voluntario.id,
                'nome': obj.voluntario.nome,
                'tipo': "Responsável"
            }
        elif obj.content_type.model == 'aluno':
            return {
                'id_obj': obj.voluntario.rm,
                'nome': obj.voluntario.nome,
                'tipo': "Aluno"
            }
        
        return {'error': 'Tipo de voluntário não reconhecido'}
    
class ProjetoSerializer(serializers.ModelSerializer):
    voluntarios = ProjetoVoluntarioSerializer(many=True, read_only=True)
    
    class Meta:
        model = Projeto
        fields = "__all__"

class SugestaoSerializer(serializers.ModelSerializer):
    tipo_Autor = serializers.SerializerMethodField()
    foto = serializers.ImageField(required=False)

    def get_tipo_Autor(self, obj):
        if obj.content_type.model == 'responsavel':
            return "Responsável"
        elif obj.content_type.model == 'aluno':
            return "Aluno"

    def create(self, validated_data):
        content_type_str = validated_data.pop("content_type")
        object_id = validated_data.pop("object_id")

        content_type=ContentType.objects.get(model=content_type_str)

        validated_data["content_type"] = content_type
        validated_data["object_id"] = object_id
        
        return super().create(validated_data)

    class Meta:
        model = Sugestao
        fields = ["id", "conteudo", "data_envio", "foto", "tipo_Autor", "object_id",]

class FuncionarioTokenObtainSerializer(serializers.Serializer):
    rf = serializers.CharField(max_length=10)
    senha = serializers.CharField(write_only=True)

    def validate(self, attrs):
        rf = attrs.get('rf')
        senha = attrs.get('senha')

        if rf and senha:
            try:
                funcionario = Funcionario.objects.get(rf=rf)
            except Funcionario.DoesNotExist:
                raise serializers.ValidationError('Credenciais inválidas.')

            if not funcionario.check_password(senha):
                raise serializers.ValidationError('Credenciais inválidas.')

            attrs['funcionario'] = funcionario
            return attrs
        else:
            raise serializers.ValidationError('Ambos os campos são necessários.')