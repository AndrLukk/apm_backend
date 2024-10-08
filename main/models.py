from django.db import models

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

class Aluno(models.Model):
    rm = models.CharField(max_length=5, primary_key=True, unique=True, blank=False, null=False)
    turma = models.CharField(max_length=6, blank=False, null=False)
    data_nasc = models.DateField(max_length=10, blank=False, null=False)
    nome = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    senha = models.CharField(max_length=255, blank=False, null=False)
    cpf = models.CharField(max_length=11, blank=False, null=False)

    def __str__(self):
        return f"RM{self.rm} - {self.nome}"

class Responsavel(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, unique=True, editable=False)
    nome = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    senha = models.CharField(max_length=255, blank=False, null=False)
    cpf = models.CharField(max_length=11, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Responsáveis"

    def __str__(self):
        return self.nome

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
    foto = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.titulo}"

class Sugestao(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, unique=True, editable=False)
    foto = models.ImageField(upload_to="images/", blank=True, null=True)
    data_envio = models.DateField(max_length=10, blank=False, null=False)
    cpf_autor = models.CharField(max_length=11, blank=False, null=False)
    conteudo = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Sugestões"

    def __str__(self):
        return self.id
