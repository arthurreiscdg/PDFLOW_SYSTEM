from django.db import models

class Webhook(models.Model):
    evento = models.CharField(max_length=50)
    payload = models.TextField()
    recebido_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Webhook - {self.evento}"
