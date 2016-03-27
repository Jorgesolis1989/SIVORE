from candidatos.models import Candidato
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required("usuarios.Administrador", login_url="/")
def registro_candidato(request):
    candidato = Candidato()
    return render(request, 'registro_candidato.html', {'candidato': candidato})

