from django.http import HttpResponse

def receber(request):
    return HttpResponse("Recebendo webhook...")
