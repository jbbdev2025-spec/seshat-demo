import sys
from pathlib import Path

# Add project root to Python path so core/ can be found
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

"""
SESHAT PoC v0.1 — Main Interface
"""

import streamlit as st

from core.models import (
    ApproachType,
    SituationRequest,
    AnalysisRequest,
)
from core.situation_generator import generate_situation, generate_variants
from core.analyzer import analyze_productions
from core.scaffolder import generate_scaffolding

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="SESHAT — PoC v0.1",
    page_icon="📚",
    layout="wide"
)

st.image(
    "assets/logo_seshat.png",
    width=120
)

st.title("SESHAT — PoC v0.1")
st.caption("Assistant de conception et d'observation pédagogique")

# US-05: Teacher decision marker — always visible
st.info("SESHAT propose, l'enseignant décide.")

st.markdown("---")

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────

tab_design, tab_analysis, tab_scaffold = st.tabs([
    "🎨 Conception de situation",
    "🔍 Analyse de productions",
    "🪜 Étayage"
])

# ─────────────────────────────────────────────
# TAB 1: SITUATION DESIGN (US-01, US-02)
# ─────────────────────────────────────────────

with tab_design:
    st.header("Concevoir une situation d'apprentissage actif")

    with st.form("situation_form"):

        col1, col2 = st.columns(2)

        with col1:
            st.text_input(
                label="Niveau des élèves",
                placeholder="Ex : 4ème, Terminale S, L1...",
                key="level",
                help="Le niveau scolaire ou académique"
            )

            st.selectbox(
                label="Type d'approche active",
                options=[e.value for e in ApproachType],
                key="approach_type",
                help="Choisissez la famille d'approche pédagogique"
            )

        with col2:
            st.text_input(
                label="Discipline",
                placeholder="Ex : Mathématiques, SVT, Français...",
                key="discipline"
            )

            st.text_input(
                label="Durée souhaitée",
                value="50 min",
                key="duration",
                help="Durée indicative de l'activité"
            )

        st.text_area(
            label="Objectifs d'apprentissage",
            placeholder="Ex : Savoir calculer un pourcentage de réduction...",
            height=100,
            key="objectives",
            help="Que les élèves doivent-ils savoir ou savoir faire ?"
        )

        st.text_area(
            label="Contraintes supplémentaires (optionnel)",
            placeholder="Ex : Travail en groupes de 4, matériel limité...",
            height=80,
            key="constraints",
            help="Toute contrainte pertinente : matériel, contexte, effectif..."
        )

        submitted = st.form_submit_button("Générer une situation")

    if submitted:
        request = SituationRequest(
            objectives=st.session_state.objectives,
            level=st.session_state.level,
            discipline=st.session_state.discipline,
            approach_type=ApproachType(st.session_state.approach_type),
            duration=st.session_state.duration,
            constraints=st.session_state.constraints,
        )

        with st.spinner("Génération en cours..."):
            situation = generate_situation(request)

        st.session_state.current_situation = situation

    if "current_situation" in st.session_state:
        st.success("Situation générée — vous pouvez modifier chaque champ ci-dessous.")

        situation = st.session_state.current_situation

        st.session_state.current_situation.context = st.text_area(
            label="Contexte / Situation",
            value=situation.context,
            height=120,
            key="edit_context"
        )

        st.session_state.current_situation.task = st.text_area(
            label="Consigne donnée aux élèves",
            value=situation.task,
            height=120,
            key="edit_task"
        )

        st.session_state.current_situation.deliverable = st.text_area(
            label="Livrable attendu",
            value=situation.deliverable,
            height=80,
            key="edit_deliverable"
        )

        st.session_state.current_situation.duration = st.text_input(
            label="Durée estimée",
            value=situation.duration,
            key="edit_duration"
        )

        st.session_state.current_situation.alignment_note = st.text_area(
            label="Alignement avec les objectifs",
            value=situation.alignment_note,
            height=100,
            key="edit_alignment"
        )

        st.markdown("---")
        st.subheader("Demander des variantes")

        col_v1, col_v2 = st.columns([1, 1])

        with col_v1:
            variant_type = st.text_input(
                label="Type de variante souhaité",
                placeholder="Ex : plus guidée, plus ouverte, plus courte, autre contexte...",
                key="variant_type"
            )

        with col_v2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Générer des variantes"):
                with st.spinner("Génération des variantes..."):
                    variant_set = generate_variants(
                        st.session_state.current_situation,
                        variant_type
                    )
                st.session_state.current_variants = variant_set

    if "current_variants" in st.session_state:
        variants = st.session_state.current_variants

        for i, (variant, description) in enumerate(
            zip(variants.variants, variants.variant_descriptions), 1
        ):
            with st.expander(f"Variante {i} — {description}", expanded=False):
                st.text_area(
                    label="Contexte",
                    value=variant.context,
                    height=100,
                    key=f"variant_{i}_context"
                )
                st.text_area(
                    label="Consigne",
                    value=variant.task,
                    height=100,
                    key=f"variant_{i}_task"
                )
                st.text_area(
                    label="Livrable",
                    value=variant.deliverable,
                    height=80,
                    key=f"variant_{i}_deliverable"
                )


# ─────────────────────────────────────────────
# TAB 2: ANALYSIS (US-03, US-05)
# ─────────────────────────────────────────────

with tab_analysis:
    st.header("Analyse de productions d'élèves")
    st.caption(
        "Collez une ou plusieurs productions d'élèves pour obtenir "
        "une analyse formatrice adressée à vous, l'enseignant."
    )

    with st.form("analysis_form"):

        st.text_area(
            label="Consigne ou tâche donnée aux élèves",
            placeholder="Ex : Un article coûte 8 000 FCFA. Après une réduction de 25 %, quel est le nouveau prix ?",
            height=80,
            key="analysis_task",
            help="La tâche ou la question que les élèves devaient traiter"
        )

        st.text_area(
            label="Objectifs d'apprentissage visés",
            placeholder="Ex : Savoir calculer un pourcentage de réduction...",
            height=60,
            key="analysis_objectives"
        )

        st.markdown("**Productions des élèves**")

        num_productions = st.number_input(
            label="Nombre de productions à analyser",
            min_value=1,
            max_value=10,
            value=1,
            key="num_productions",
            help="Vous pouvez coller plusieurs productions pour obtenir une synthèse collective"
        )

        productions = []
        for i in range(num_productions):
            production = st.text_area(
                label=f"Production {i + 1}",
                placeholder=f"Collez ici la production de l'élève {i + 1}...",
                height=100,
                key=f"production_{i}"
            )
            productions.append(production)

        submitted_analysis = st.form_submit_button("Analyser")

    if submitted_analysis:
        valid_productions = [p for p in productions if p.strip()]

        if not valid_productions:
            st.warning("Veuillez coller au moins une production d'élève.")
        else:
            request = AnalysisRequest(
                original_task=st.session_state.analysis_task,
                objectives=st.session_state.analysis_objectives,
                productions=valid_productions,
            )

            with st.spinner("Analyse en cours..."):
                result = analyze_productions(request)

            st.session_state.current_analysis = result

    if "current_analysis" in st.session_state:
        result = st.session_state.current_analysis

        st.success("Analyse terminée — destinée à l'enseignant, pas aux élèves.")

        confidence_color = {
            "high": "🟢",
            "moderate": "🟡",
            "low": "🔴"
        }
        confidence_icon = confidence_color.get(result.confidence, "🟡")

        st.caption(
            f"{confidence_icon} Niveau de confiance de l'analyse : "
            f"**{result.confidence}**"
        )

        st.markdown("---")

        st.subheader("✅ Points forts observés")
        for strength in result.strengths:
            st.markdown(f"- {strength}")

        st.subheader("⚠️ Difficultés ou points de blocage")
        for difficulty in result.difficulties:
            st.markdown(f"- {difficulty}")

        if result.collective_patterns:
            st.subheader("📊 Tendances collectives")
            for pattern in result.collective_patterns:
                st.markdown(f"- {pattern}")

        st.subheader("📎 Éléments de preuve cités")
        for evidence in result.evidence:
            st.markdown(f"> *{evidence}*")

        st.markdown("---")
        st.info(
            "Cette analyse est une proposition. "
            "Vous pouvez l'utiliser, la modifier ou l'ignorer."
        )


# ─────────────────────────────────────────────
# TAB 3: SCAFFOLDING (US-04, US-05)
# ─────────────────────────────────────────────

with tab_scaffold:
    st.header("Suggestions d'étayage")
    st.caption(
        "Obtenez des niveaux d'aide progressifs que vous pouvez "
        "choisir de donner aux élèves. Aucune suggestion ne contient "
        "la solution."
    )

    # Show what's available as basis for scaffolding
    has_situation = "current_situation" in st.session_state
    has_analysis = "current_analysis" in st.session_state

    if not has_situation and not has_analysis:
        st.warning(
            "Générez d'abord une situation (onglet 1) ou "
            "analysez des productions (onglet 2) pour obtenir "
            "des suggestions d'étayage contextualisées."
        )
        st.stop()

    # Show available context
    st.subheader("Contexte disponible")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        if has_situation:
            st.markdown("✅ Situation générée")
        else:
            st.markdown("⚪ Aucune situation")

    with col_c2:
        if has_analysis:
            st.markdown("✅ Analyse réalisée")
        else:
            st.markdown("⚪ Aucune analyse")

    st.markdown("---")

    # Generate button
    if st.button("Générer des suggestions d'étayage"):
        situation = st.session_state.get("current_situation")
        analysis = st.session_state.get("current_analysis")

        with st.spinner("Génération des suggestions..."):
            scaffold_set = generate_scaffolding(
                situation=situation,
                analysis=analysis,
            )

        st.session_state.current_scaffolding = scaffold_set

    # Display scaffolding
    if "current_scaffolding" in st.session_state:
        scaffold_set = st.session_state.current_scaffolding

        st.success("Suggestions générées — choisissez celles que vous souhaitez utiliser.")

        st.caption(f"*{scaffold_set.context}*")

        st.markdown("---")

        for suggestion in scaffold_set.suggestions:
            level_label = {
                1: "🟢 Niveau 1 — Question légère",
                2: "🟡 Niveau 2 — Guidage plus explicite",
                3: "🟠 Niveau 3 — Étayage renforcé",
            }

            with st.expander(
                level_label.get(suggestion.level, f"Niveau {suggestion.level}"),
                expanded=(suggestion.level == 1),
            ):
                st.markdown(f"> {suggestion.text}")

                # Teacher can accept or edit each suggestion
                edited = st.text_area(
                    label="Modifier si souhaité",
                    value=suggestion.text,
                    height=80,
                    key=f"scaffold_edit_{suggestion.level}"
                )

                col_a1, col_a2 = st.columns(2)

                with col_a1:
                    if st.button(
                        "Copier",
                        key=f"scaffold_copy_{suggestion.level}"
                    ):
                        st.toast("Texte copié dans le presse-papiers (fonctionnalité navigateur)")

                with col_a2:
                    if st.button(
                        "J'utilise celle-ci",
                        key=f"scaffold_use_{suggestion.level}",
                        type="primary"
                    ):
                        st.toast("Marqué comme sélectionné")

        # US-05 reminder
        st.markdown("---")
        st.info(
            "Ces suggestions sont des propositions. "
            "Vous pouvez les utiliser, les modifier ou les ignorer. "
            "Aucune n'a été envoyée aux élèves."
        )