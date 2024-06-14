from django import forms
from .models import estados, municipios, paises

class EstadoForm(forms.ModelForm):
    class Meta:
        model = estados
        fields = ['nombreEstado', 'idPais_id']

class MunicipioForm(forms.ModelForm):
    class Meta:
        model = municipios
        fields = ['nombreMunicipio', 'idEstado_id']

class PaisesForm(forms.ModelForm):
    class Meta:
        model = paises
        fields = ['nombre']
