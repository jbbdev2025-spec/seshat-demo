"""
SESHAT PoC v0.1 — Scaffolding Generator (Mock)

This is a MOCK implementation.

It returns pre-written scaffolding suggestions instead of calling an LLM.
Later, this file will contain the real LLM call.
The interface will NOT need to change.
"""

from core.models import ScaffoldingSet, ScaffoldingSuggestion, Situation, AnalysisResult


def generate_scaffolding(
    situation: Situation = None,
    analysis: AnalysisResult = None,
) -> ScaffoldingSet:
    """
    Generate ordered scaffolding suggestions for the teacher.

    MOCK VERSION: returns fixed suggestions.
    REAL VERSION (later): will call an LLM.

    The scaffolding can be based on:
    - A situation (to prepare support in advance)
    - An analysis of student work (to respond to observed difficulties)
    - Both

    Args:
        situation: Optional. The learning situation.
        analysis: Optional. The analysis of student productions.

    Returns:
        A ScaffoldingSet with 2-3 ordered suggestions.
        NEVER contains the solution.
    """
    # Determine context for the teacher
    if analysis and analysis.difficulties:
        context = (
            "Basé sur l'analyse des productions : difficulté majeure "
            "sur le calcul du pourcentage."
        )
    elif situation:
        context = (
            "Basé sur la situation proposée : problème de réduction "
            "de prix."
        )
    else:
        context = "Contexte non spécifié."

    # Three levels of support, from lightest to strongest
    # NONE of these contain the solution (6000 FCFA)
    return ScaffoldingSet(
        suggestions=[
            ScaffoldingSuggestion(
                level=1,
                text=(
                    "« Que représente 25 % d'une quantité ? "
                    "Peux-tu l'exprimer d'une autre façon ? »"
                ),
            ),
            ScaffoldingSuggestion(
                level=2,
                text=(
                    "« 25 %, c'est un quart. "
                    "Si tu devais partager cette somme en 4 parts égales, "
                    "combien ferait une part ? »"
                ),
            ),
            ScaffoldingSuggestion(
                level=3,
                text=(
                    "« Essaie de calculer un quart de 8 000. "
                    "Ensuite, soustrais ce que tu obtiens "
                    "du prix initial. »"
                ),
            ),
        ],
        context=context,
    )