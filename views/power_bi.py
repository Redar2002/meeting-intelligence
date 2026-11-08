import os

import streamlit as st

import ui

# Lien d'intégration du rapport (Power BI → Fichier → Intégrer le rapport), à mettre dans .env
REPORT_URL = os.getenv("POWERBI_URL", "").strip()

ui.page_header(
    "Power BI",
    "Tableau de bord commercial alimenté par les données SQL Server.",
    eyebrow="Reporting",
)

if not REPORT_URL:
    ui.empty_state(
        "Aucun rapport configuré",
        "Ajoutez le lien d'intégration de votre rapport Power BI dans .env (POWERBI_URL=...), puis relancez l'application.",
    )
    st.stop()

st.markdown(
    f'<div class="mi-embed"><iframe title="Rapport Power BI" src="{REPORT_URL}" allowfullscreen="true"></iframe></div>',
    unsafe_allow_html=True,
)

st.caption(
    "Utilisez les filtres directement dans le rapport. Si le rapport ne s'affiche pas, "
    "vérifiez que votre compte Microsoft a accès au rapport."
)
st.link_button("Ouvrir dans Power BI", REPORT_URL, icon=":material/open_in_new:")
