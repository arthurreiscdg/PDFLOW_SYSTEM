from django.shortcuts import render

def formularios(request):
    return render(request, 'formularios/formularios.html')