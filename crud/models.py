from django.db import models

class Funcionario(models.Model):
    rf = models.CharField(max_length=10, editable=False, unique=True, blank=False, null=False)
    nome = models.CharField(max_length=255, blank=False, null=False)
    cpf = models.CharField(max_length=11, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    senha = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Funcionários"

class Aluno(models.Model):
    rm = models.CharField(max_length=5, editable=False, unique=True, blank=False, null=False)
    turma = models.CharField(max_length=6, blank=False, null=False)
    data_nasc = models.DateField(max_length=10, blank=False, null=False)
    nome = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    senha = models.CharField(max_length=255, blank=False, null=False)
    cpf = models.CharField(max_length=11, blank=False, null=False)

class Responsavel(models.Model):
    nome = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    senha = models.CharField(max_length=255, blank=False, null=False)
    cpf = models.CharField(max_length=11, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Responsáveis"

class Doacao(models.Model):
    data_envio = models.DateField(max_length=10, blank=False, null=False)
    cpf_autor = models.CharField(max_length=11, blank=False, null=False)
    valor = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Doações"

class NotaFiscal(models.Model):
    valor_gasto = models.DecimalField(decimal_places=2, max_digits=10, blank=False, null=False)
    destino_valor = models.CharField(max_length=255, blank=False, null=False)
    
    class Meta:
        verbose_name_plural = "Notas Fiscais"

class Projeto(models.Model):
    STATUS_CHOICE = {
        "NI" : "Não Iniciado",
        "EA" : "Em Andamento",
        "FI" : "Finalizado"
    }
    status = models.CharField(max_length=2, choices=STATUS_CHOICE, default="NI", blank=False, null=False)
    desc = models.CharField(max_length=255, blank=False, null=False)
    foto = models.ImageField(upload_to="images/", blank=True, null=True)

class Sugestao(models.Model):
    foto = models.ImageField(upload_to="images/", blank=True, null=True)
    data_envio = models.DateField(max_length=10, blank=False, null=False)
    cpf_autor = models.CharField(max_length=11, blank=False, null=False)
    conteudo = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Sugestões"
