from django.db import models
import uuid
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.hashers import make_password, check_password as django_check_password

class Funcionario(models.Model):
    rf = models.CharField(max_length=10, unique=True, primary_key=True, blank=False, null=False)
    nome = models.CharField(max_length=255, blank=False, null=False)
    cpf = models.CharField(max_length=11, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    senha = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return f"RF{self.rf} - {self.nome}"

    def check_password(self, raw_password):
        """
        Verifica se a senha em texto puro corresponde à senha hash armazenada.
        """
        return django_check_password(raw_password, self.senha)
    
    def save(self, *args, **kwargs):
        # Hash da senha antes de salvar
        if self.senha:
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs) 

class FuncionarioToken(models.Model):
    funcionario = models.ForeignKey('Funcionario', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Exemplo de expiração após 24 horas
        return timezone.now() < self.created_at + timezone.timedelta(hours=24)

    def __str__(self):
        return f"Token for {self.funcionario.nome}"

class Aluno(models.Model):
    rm = models.CharField(max_length=5, primary_key=True, unique=True, blank=False, null=False)
    turma = models.CharField(max_length=6, blank=False, null=False)
    data_nasc = models.DateField(max_length=10, blank=False, null=False)
    nome = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    senha = models.CharField(max_length=255, blank=False, null=False)
    cpf = models.CharField(max_length=11, blank=False, null=False)

    def delete(self, using=None, keep_parents=False):
        Sugestao.objects.filter(content_type=ContentType.objects.get_for_model(Aluno), object_id=self.rm).delete()
        ProjetoVoluntario.objects.filter(content_type=ContentType.objects.get_for_model(Aluno), object_id=self.rm).delete()
        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f"RM{self.rm} - {self.nome}"

class AlunoToken(models.Model):
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timezone.timedelta(hours=24)

    def __str__(self):
        return f"Token for {self.aluno.nome}"

class Responsavel(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, unique=True, editable=False)
    nome = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    senha = models.CharField(max_length=255, blank=False, null=False)
    cpf = models.CharField(max_length=11, blank=False, null=False)

    def delete(self, using=None, keep_parents=False):
        Sugestao.objects.filter(content_type=ContentType.objects.get_for_model(Responsavel), object_id=self.id).delete()
        ProjetoVoluntario.objects.filter(content_type=ContentType.objects.get_for_model(Responsavel), object_id=self.id).delete()
        super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        verbose_name_plural = "Responsáveis"

    def __str__(self):
        return self.nome

class ResponsavelToken(models.Model):
    responsavel = models.ForeignKey('Responsavel', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timezone.timedelta(hours=24)

    def __str__(self):
        return f"Token for {self.responsavel.nome}"
    
class ResponsavelDependente(models.Model):
    responsavel = models.ForeignKey(Responsavel, related_name="dependentes", on_delete=models.CASCADE)
    dependente = models.ForeignKey(Aluno, related_name="dependentes_responsavel", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('responsavel', 'dependente')

    def __str__(self):
        return f"{self.responsavel} - {self.dependente}"

class Doacao(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, unique=True, editable=False)
    data_envio = models.DateField(max_length=10, blank=False, null=False)
    cpf_autor = models.CharField(max_length=11, blank=False, null=False)
    valor = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Doações"

    def __str__(self):
        return self.id

class Projeto(models.Model):
    STATUS_CHOICE = {
        "NI" : "Não Iniciado",
        "EA" : "Em Andamento",
        "FI" : "Finalizado"
    }
    id = models.AutoField(auto_created=True, primary_key=True, unique=True, editable=False)
    titulo = models.CharField(max_length=255, blank=False, null=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOICE, default="NI", blank=False, null=False)
    desc = models.CharField(max_length=255, blank=False, null=False)
    foto = models.ImageField(upload_to="", blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.titulo}"
       
class ProjetoVoluntario(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='voluntarios')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    voluntario = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('projeto', 'content_type', 'object_id')
    
    def __str__(self):
        return f"{self.id} - {self.voluntario}"

class Sugestao(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, unique=True, editable=False)
    foto = models.ImageField(upload_to="images/", blank=True, null=True)
    data_envio = models.DateField(max_length=10, blank=False, null=False)
    conteudo = models.CharField(max_length=255, blank=False, null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    autor = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name_plural = "Sugestões"

    def __str__(self):
        return str(self.id)
