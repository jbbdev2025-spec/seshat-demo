"""
SESHAT PoC v0.1 — Production Analyzer (Mock)

This is a MOCK implementation.

It returns a pre-written analysis instead of calling an LLM.
Later, this file will contain the real LLM call.
The interface will NOT need to change.
"""

from core.models import AnalysisRequest, AnalysisResult


def analyze_productions(request: AnalysisRequest) -> AnalysisResult:
    """
    Analyze one or more student productions for the teacher.

    MOCK VERSION: returns a fixed analysis.
    REAL VERSION (later): will call an LLM with a structured prompt.

    Args:
        request: An AnalysisRequest containing the task,
                 objectives, and student productions.

    Returns:
        An AnalysisResult addressed to the teacher.
    """
    # The mock adapts slightly based on number of productions
    # to show that the single vs. multiple logic works

    production_count = len(request.productions)

    if production_count == 1:
        # Single production analysis
        return AnalysisResult(
            strengths=[
                "L'élève identifie correctement qu'il faut calculer "
                "la réduction avant de la soustraire.",
                "La démarche est structurée : l'élève passe par "
                "une étape de calcul intermédiaire."
            ],
            difficulties=[
                "Le calcul du pourcentage est incorrect : l'élève "
                "obtient 1 000 au lieu de 2 000. Il semble diviser "
                "par 8 au lieu de multiplier par 0,25 (ou confondre "
                "25 % avec 1/8).",
                "L'élève ne vérifie pas la cohérence de son résultat "
                "intermédiaire (1 000 FCFA de réduction sur un article "
                "de 8 000 FCFA semble faible)."
            ],
            collective_patterns=[],
            evidence=[
                "« 25 % de 8000 = 1000 » — erreur sur le calcul "
                "du pourcentage",
                "« 8000 - 1000 = 7000 » — soustraction correcte "
                "mais appliquée à un résultat intermédiaire faux"
            ],
            confidence="high",
        )

    else:
        # Multiple productions analysis
        return AnalysisResult(
            strengths=[
                "La majorité des élèves (4 sur 5) identifient "
                "qu'il faut calculer la réduction avant de soustraire.",
                "Deux élèves utilisent spontanément la méthode "
                "multiplicative (× 0,75) plutôt que la méthode "
                "en deux étapes, montrant une bonne compréhension "
                "de la notion de pourcentage."
            ],
            difficulties=[
                "3 élèves sur 5 font une erreur de calcul du "
                "pourcentage : ils obtiennent 1 000 au lieu de 2 000.",
                "2 élèves confondent la réduction avec le prix final : "
                "ils répondent 2 000 au lieu de 6 000.",
                "Aucun élève ne justifie oralement son résultat "
                "ou ne vérifie la plausibilité du montant obtenu."
            ],
            collective_patterns=[
                "Erreur majoritaire sur le calcul de 25 % d'un nombre : "
                "la division par un entier semble privilégiée à tort "
                "(diviser par 4 donne 2 000, mais certains divisent par 8).",
                "Conception récurrente : « la réduction C'est le nouveau prix » "
                "— confusion entre le montant de la réduction et le prix après réduction.",
                "Absence généralisée de vérification / métacognition : "
                "aucun élève ne commente la vraisemblance de son résultat."
            ],
            evidence=[
                "Élève A : « 25 % de 8000 = 1000, donc 7000 »",
                "Élève B : « 8000 × 25 % = 2000, donc le nouveau prix est 2000 »",
                "Élève C : « 8000 - 25 = 7975 »",
                "Élève D : « 8000 × 0,75 = 6000 »",
                "Élève E : « 25 % de 8000 = 1000 »"
            ],
            confidence="moderate",
        )