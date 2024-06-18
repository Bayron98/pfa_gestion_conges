from django.core.exceptions import ValidationError
from django.utils import timezone
from django import forms
from .models import DemandeConge, TypeConge
class DemandeCongeForm(forms.ModelForm):
    class Meta:
        model = DemandeConge
        fields = ['date_debut', 'date_fin', 'type_conge', 'raison']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'type_conge': forms.Select(choices=TypeConge.objects.all()),
            'raison': forms.Textarea,
        }

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')

        if date_fin and date_debut and date_fin < date_debut:
            raise ValidationError("La date de fin doit être après la date de début.")

        if date_debut and date_debut < timezone.now().date():
            raise ValidationError("La demande de congé doit être pour des dates futures.")

        return cleaned_data