from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, render, redirect

def mostrar_tarjeton(request):
    return render(request, 'mostrar_tarjeton.html')

def mostrar_corporaciones(request):
    return render(request, 'mostrar_corporaciones.html')

