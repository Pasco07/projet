
from django.shortcuts import render, redirect
from .forms import AmortissementForm
from .forms import AmortissementFormdif
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from scipy.optimize import newton



def accueil(request):
    return render(request, 'accueil.html')

def a_propos(request):
    return render(request, 'a_propos.html')

def contact(request):
    return render(request, 'contact.html')

def tableau_amortissement(request):
    # Rediriger en fonction du choix de l'utilisateur
    type_amortissement = request.GET.get('type_amortissement')
    if type_amortissement == "differe":
        return redirect('differe')
    elif type_amortissement == "non_differe":
        return redirect('non_differe')
    return render(request, 'tableau_amortissement.html')

def differe(request):
    return render(request, 'differe.html')

def non_differe(request):
    return render(request, 'non_differe.html')

def Nouvelle_page(request):
    return render(request, 'Nouvelle_page.html')

from datetime import timedelta
from scipy.optimize import newton

def calculer_tableau_amortissement(nominal, taux_facial, date_valeur, maturite, prix_pondere):
    # Validation des paramètres
    if any([nominal <= 0, taux_facial <= 0, maturite <= 0]):
        raise ValueError("Les valeurs de nominal, taux facial et maturité doivent être positives.")

    tableau = []
    cash_flows = []
    dates = []
    taux_periodique = taux_facial / 100  # Convertir le taux en décimal
    amortissement_const = nominal / maturite  # Amortissement constant
    montant_restant = nominal

    # Première période (Investissement initial)
    tableau.append({
        'periode': 1,
        'date': date_valeur.strftime('%d/%m/%Y'),
        'montant_debut': '-',
        'interet': '-',
        'amortissement': '-',
        'annuite': -prix_pondere,  # Annuité = -prix_pondere
        'montant_fin': '-',
    })
    cash_flows.append(-prix_pondere)  # Simplification
    dates.append(date_valeur)

    # Périodes suivantes
    for periode in range(2, maturite + 2):
        interet = montant_restant * taux_periodique 
        annuite = interet + amortissement_const
        montant_fin_periode = montant_restant - amortissement_const

        # Calculer la date en années
        date_periode = date_valeur + timedelta(days=365 * (periode - 1))

        tableau.append({
            'periode': periode,
            'date': date_periode.strftime('%d/%m/%Y'),
            'montant_debut': round(montant_restant, 2),
            'interet': round(interet, 2),
            'amortissement': round(amortissement_const, 2),
            'annuite': round(annuite, 2),
            'montant_fin': round(montant_fin_periode, 2),
        })
        cash_flows.append(round(annuite, 2))  # Simplification
        dates.append(date_periode)

        montant_restant = montant_fin_periode

    return tableau, cash_flows, dates

def xirr(cash_flows, dates, guess=0.01):
    def npv(rate):
        return sum(cf / (1 + rate) ** ((date - dates[0]).days / 365) for cf, date in zip(cash_flows, dates))
    
    try:
        return newton(npv, guess)
    except Exception as e:
        raise ValueError(f"Erreur lors du calcul du XIRR : {str(e)}")


def non_differe(request):
    if request.method == 'POST':
        form = AmortissementForm(request.POST)
        if form.is_valid():
            try:
                # Récupération des données
                data = form.cleaned_data
                nominal = data['nominal']
                taux_facial = data['taux_facial']
                date_valeur = data['date_valeur']
                maturite = data['maturite']
                prix_pondere = data['prix_pondere']

                # Validation
                if not (nominal > 0 and taux_facial > 0 and maturite > 0):
                    raise ValueError("Les valeurs de nominal, taux facial et maturité doivent être positives.")

                # Calculs
                tableau, cash_flows, dates = calculer_tableau_amortissement(nominal, taux_facial, date_valeur, maturite, prix_pondere)

                # Calcul du rendement
                try:
                    rendement = round(xirr(cash_flows, dates) * 100, 2)
                except Exception as e:
                    rendement = f"Erreur de calcul : {str(e)}"

                context = {
                    'form': form,
                    'tableau': tableau,
                    'rendement': rendement,
                    **data
                }
                return render(request, 'non_differe.html', context)

            except ValueError as e:
                form.add_error(None, f"Erreur de validation : {str(e)}")
                return render(request, 'non_differe.html', {'form': form})
            except Exception as e:
                form.add_error(None, f"Erreur inattendue : {str(e)}")
                return render(request, 'non_differe.html', {'form': form})

    else:
        form = AmortissementForm()

    return render(request, 'non_differe.html', {'form': form})




def calculer_tableau_amortissement_differe(nominal, taux_facial, date_valeur, maturite, prix_pondere, annees_differe):
    # Validation des paramètres
    if any([nominal <= 0, taux_facial <= 0, maturite <= 0, annees_differe < 0]):
        raise ValueError("Les paramètres doivent être positifs")
    if annees_differe >= maturite:
        raise ValueError("La période de différé doit être inférieure à la maturité")

    tableau = []
    cash_flows = []
    dates = []
    taux_periodique = taux_facial / 100
    duree_amortissement = maturite - annees_differe
    amortissement_const = nominal / duree_amortissement if duree_amortissement > 0 else 0
    montant_restant = nominal

    # Période initiale (Investissement)
    tableau.append({
        'periode': 1,
        'date': date_valeur.strftime('%d/%m/%Y'),
        'montant_debut': '-',
        'interet': '-',
        'amortissement': '-',
        'annuite': -prix_pondere,
        'montant_fin': '-',
    })
    cash_flows.append(-prix_pondere)
    dates.append(date_valeur)

    # Période de différé (Paiement des intérêts seulement)
    for periode in range(2, annees_differe + 2):
        date_periode = date_valeur + timedelta(days=365*(periode-1))
        interet = montant_restant * taux_periodique
        
        tableau.append({
            'periode': periode,
            'date': date_periode.strftime('%d/%m/%Y'),
            'montant_debut': round(montant_restant, 2),
            'interet': round(interet, 2),
            'amortissement': 0.00,
            'annuite': round(interet, 2),
            'montant_fin': round(montant_restant, 2)
        })
        cash_flows.append(round(interet, 2))
        dates.append(date_periode)

    # Période d'amortissement
    for periode in range(annees_differe + 2, maturite + 2):
        date_periode = date_valeur + timedelta(days=365*(periode-1))
        interet = montant_restant * taux_periodique
        annuite = interet + amortissement_const
        montant_fin_periode = montant_restant - amortissement_const

        tableau.append({
            'periode': periode,
            'date': date_periode.strftime('%d/%m/%Y'),
            'montant_debut': round(montant_restant, 2),
            'interet': round(interet, 2),
            'amortissement': round(amortissement_const, 2),
            'annuite': round(annuite, 2),
            'montant_fin': round(montant_fin_periode, 2)
        })
        cash_flows.append(round(annuite, 2))
        dates.append(date_periode)
        montant_restant = montant_fin_periode

    return tableau, cash_flows, dates

def xirr(cash_flows, dates, guess=0.01, max_iter=1000):
    """Calcul du taux de rendement interne avec gestion d'erreur améliorée"""
    def npv(rate):
        return sum(
            cf / (1 + rate) ** ((date - dates[0]).days / 365)
            for cf, date in zip(cash_flows, dates)
        )
    
    try:
        return newton(npv, guess, maxiter=max_iter)
    except RuntimeError:
        raise ValueError("Impossible de converger vers une solution")


def differe(request):
    if request.method == 'POST':
        form = AmortissementFormdif(request.POST)
        if form.is_valid():
            try:
                # Récupération des données
                data = form.cleaned_data
                nominal = data['nominal']
                taux_facial = data['taux_facial']
                date_valeur = data['date_valeur']
                maturite = data['maturite']
                prix_pondere = data['prix_pondere']
                annees_differe = data['annees_differe']

                # Validation
                if not (nominal > 0 and taux_facial > 0 and maturite > 0 and annees_differe >= 0):
                    raise ValueError("Les valeurs de nominal, taux facial et maturité doivent être positives.")
                if annees_differe >= maturite:
                    raise ValueError("La période de différé doit être inférieure à la maturité.")

                # Calculs
                tableau, cash_flows, dates = calculer_tableau_amortissement_differe(
                    nominal, taux_facial, date_valeur, maturite, prix_pondere, annees_differe
                )

                # Calcul du rendement
                try:
                    rendement = round(xirr(cash_flows, dates) * 100, 2)
                except Exception as e:
                    rendement = f"Erreur de calcul : {str(e)}"

                context = {
                    'form': form,
                    'tableau': tableau,
                    'rendement': rendement,
                    **data
                }
                return render(request, 'differe.html', context)

            except ValueError as e:
                form.add_error(None, f"Erreur de validation : {str(e)}")
                return render(request, 'differe.html', {'form': form})
            except Exception as e:
                form.add_error(None, f"Erreur inattendue : {str(e)}")
                return render(request, 'differe.html', {'form': form})

    else:
        form = AmortissementFormdif()

    return render(request, 'differe.html', {'form': form})

