from django import forms

class AmortissementForm(forms.Form):
    nominal = forms.FloatField(label="Nominal", initial=10000)
    taux_facial = forms.FloatField(label="Taux facial (%)", initial=5.0)
    date_valeur = forms.DateField(label="Date de valeur",widget=forms.DateInput(attrs={'type': 'date'}))
    maturite = forms.IntegerField(label="Maturité (année)", initial=5)
    prix_pondere = forms.FloatField(label="Prix pondéré")


   
class AmortissementFormdif(forms.Form):
    nominal = forms.FloatField(label="Nominal",initial=10000)
    taux_facial = forms.FloatField(label="Taux facial (%)")
    date_valeur = forms.DateField(label="Date de valeur", widget=forms.DateInput(attrs={'type': 'date'}))
    maturite = forms.IntegerField(label="Maturité (année)")
    prix_pondere = forms.FloatField(label="Prix pondéré")
    annees_differe = forms.IntegerField(label="Nombre d'années de différé")  # Nouveau champ

