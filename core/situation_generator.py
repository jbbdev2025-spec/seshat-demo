"""
SESHAT PoC v0.1 — Situation Generator (Mock)

This is a MOCK implementation.

It returns a pre-written situation instead of calling an LLM.
This allows us to build and test the interface without
any external dependency.

Later, this file will contain the real LLM call.
The interface (app/main.py) will NOT need to change.
"""

from core.models import Situation, VariantSet


def generate_situation(request) -> Situation:
    """
    Generate an active learning situation from a teacher's request.

    MOCK VERSION: returns a fixed situation regardless of input.
    REAL VERSION (later): will call an LLM with a structured prompt.

    Args:
        request: A SituationRequest object from the teacher.

    Returns:
        A Situation object ready to display.
    """
    # This is the mock response
    # It ignores the input and always returns the same situation
    return Situation(
        context=(
            "Une commune rurale de 5 000 habitants envisage de "
            "construire un marché couvert. Le maire dispose d'un "
            "budget de 15 millions de FCFA. Différents groupes "
            "(commerçants, éleveurs, agriculteurs, femmes "
            "transformatrices) ont des besoins différents."
        ),
        task=(
            "En groupes de 4, élaborez une proposition de plan "
            "du marché qui tient compte des contraintes budgétaires "
            "et des besoins de chaque groupe. Justifiez vos choix "
            "de surface, d'emplacement et d'équipement."
        ),
        deliverable="Un plan schématique du marché avec justifications écrites (1 page)",
        duration="1h30",
        alignment_note=(
            "Cette situation mobilise la capacité à analyser un "
            "problème concret impliquant des contraintes multiples "
            "(budgétaires, spatiales, sociales) et à formuler une "
            "proposition argumentée. Elle requiert de mobiliser "
            "des savoirs en géométrie (surfaces), en proportionnalité "
            "(répartition du budget) et en raisonnement logique "
            "(arbitrage entre besoins contradictoires)."
        ),
    )


def generate_variants(original_situation, variant_type: str) -> VariantSet:
    """
    Generate variants of an existing situation.

    MOCK VERSION: returns fixed variants.
    REAL VERSION (later): will call an LLM.

    Args:
        original_situation: The Situation to create variants from.
        variant_type: Description of the desired variant type.

    Returns:
        A VariantSet with 2-3 differentiated variants.
    """
    return VariantSet(
        variants=[
            Situation(
                context=(
                    "Une commune rurale de 5 000 habitants envisage de "
                    "construire un marché couvert. Le maire dispose d'un "
                    "budget de 15 millions de FCFA. Différents groupes "
                    "ont des besoins différents."
                ),
                task=(
                    "Voici les étapes à suivre :\n"
                    "1. Listez les besoins de chaque groupe.\n"
                    "2. Calculez la surface nécessaire par groupe.\n"
                    "3. Vérifiez que le total respecte le budget.\n"
                    "4. Dessinez le plan du marché."
                ),
                deliverable="Un plan schématique avec étapes de calcul détaillées",
                duration="1h30",
                alignment_note="Même objectif, mais avec un guidage étape par étape.",
            ),
            Situation(
                context=(
                    "Votre école veut aménager un espace multimédia "
                    "de 40 m² avec un budget de 2 millions de FCFA. "
                    "Les élèves, les enseignants et l'administration "
                    "ont des attentes différentes."
                ),
                task=(
                    "Proposez un aménagement de cet espace qui "
                    "satisfasse les besoins de chacun tout en "
                    "respectant le budget et la surface disponible."
                ),
                deliverable="Un plan détaillé avec devis simplifié",
                duration="1h30",
                alignment_note="Même compétence (arbitrage sous contraintes) dans un contexte différent.",
            ),
        ],
        variant_descriptions=[
            "Version plus guidée : étapes explicites fournies aux élèves",
            "Même structure dans un contexte différent (école au lieu de marché)",
        ],
    )