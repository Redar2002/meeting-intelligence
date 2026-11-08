"""
utils_auth.py — Session et page de connexion de Meeting Intelligence
"""
import base64
import os
import sys

import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import auth
import ui

_SESSION_USER_KEY = "_auth_user"
_SESSION_LOGGEDIN = "_auth_logged_in"

_LOGIN_CSS = """
<style>
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="stHeader"] { display: none; }
.block-container { max-width: none; padding: 0 !important; }
.block-container > [data-testid="stVerticalBlock"] { gap: 0; }
[data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] { gap: 0; }
/* Panneau de droite : colonne centrée de 420 px, logo en haut, formulaire au milieu, pied en bas */
.st-key-login_panel {
    min-height: 100vh;
    padding: 2.5rem clamp(1.5rem, 5vw, 4rem);
    display: flex;
    flex-direction: column;
    align-items: center;
}
.st-key-login_panel > * { width: 100%; max-width: 420px; }
.st-key-login_panel > :has(.mi-login-heading) { margin-top: auto; }
.st-key-login_panel > :has(.mi-login-foot) { margin-top: auto; }
.st-key-login_panel [data-testid="stForm"] { border: none; padding: 0; }
.st-key-login_panel .stFormSubmitButton > button { height: 3rem; font-size: 1rem; }
@media (max-width: 640px) {
    .mi-login-visual { display: none; }
    .st-key-login_panel { min-height: 100vh; padding-top: 2rem; }
}
</style>
"""

# Visuel de gauche : photo assets/login.jpg si elle existe, sinon illustration (micro + halo ambré)
_MIC_SVG = (
    '<svg width="170" height="230" viewBox="0 0 34 46" fill="none" stroke="#E8ECF4" '
    'stroke-width="1.2" stroke-linecap="round"><rect x="10" y="2" width="14" height="26" rx="7"/>'
    '<path d="M10 10h5M10 15h5M10 20h5M19 10h5M19 15h5M19 20h5" stroke-opacity="0.45"/>'
    '<path d="M4 20a13 13 0 0 0 26 0M17 33v8M10 43h14"/></svg>'
)


def _login_visual_html() -> str:
    quote = (
        '<div class="mi-login-quote">Chaque réunion devient une décision.'
        "<span>Transcription · Analyse · Reporting</span></div>"
    )
    photo = ui.LOGIN_PHOTO_PATH
    if photo.exists():
        data = base64.b64encode(photo.read_bytes()).decode("ascii")
        # Dégradé sombre en bas pour garder le titre lisible sur la photo
        bg = (
            "background: linear-gradient(to top, rgba(8,14,27,0.95) 0%, rgba(8,14,27,0.55) 28%, rgba(8,14,27,0) 55%),"
            f" center / cover no-repeat url(data:image/jpeg;base64,{data});"
        )
        inner = quote
    else:
        bg = (
            "background: radial-gradient(circle at 70% 25%, rgba(242,169,34,0.55) 0%, rgba(242,169,34,0.08) 28%, transparent 45%),"
            " radial-gradient(circle at 15% 85%, rgba(220,38,38,0.35) 0%, transparent 40%),"
            " linear-gradient(160deg, #1B2540 0%, #0B1222 70%);"
        )
        inner = f'<div class="mi-login-mic">{_MIC_SVG}</div>{quote}'
    return f'<div class="mi-login-visual" style="{bg}">{inner}</div>'



def check_auth() -> bool:
    """Vérifie si l'utilisateur est connecté"""
    return st.session_state.get(_SESSION_LOGGEDIN, False)

def get_current_user() -> dict | None:
    """Récupère les données de l'utilisateur connecté"""
    if check_auth():
        return st.session_state.get(_SESSION_USER_KEY)
    return None

def logout():
    """Déconnexion de l'utilisateur"""
    for key in [_SESSION_USER_KEY, _SESSION_LOGGEDIN]:
        st.session_state.pop(key, None)
    st.rerun()

def render_user_sidebar():
    """Carte utilisateur + déconnexion, en bas de la barre latérale."""
    user = get_current_user()
    if not user:
        return
    ui.user_card(user)
    if st.button("Se déconnecter", icon=":material/logout:", width="stretch", key="_btn_logout_sidebar"):
        logout()


def _logo_b64() -> str:
    with open(ui.APP_LOGO_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def login_page():
    """Page de connexion."""
    auth.ensure_users_table()
    st.markdown(_LOGIN_CSS, unsafe_allow_html=True)

    visual_col, form_col = st.columns([1.15, 1])
    with visual_col:
        st.markdown(_login_visual_html(), unsafe_allow_html=True)
    panel = form_col.container(key="login_panel")
    panel.markdown(
        f'<div class="mi-login-brand"><img src="data:image/svg+xml;base64,{_logo_b64()}" alt="Meeting Intelligence"/></div>',
        unsafe_allow_html=True,
    )
    panel.markdown(
        '<div class="mi-login-heading"><div class="mi-login-title">Connexion</div>'
        "<div class=\"mi-login-subtitle\">Si vous n'avez pas de compte, contactez l'administrateur.</div></div>",
        unsafe_allow_html=True,
    )

    with panel.form("login_form", clear_on_submit=False, border=False):
        email = st.text_input("Adresse email", placeholder="prenom.nom@entreprise.com", key="login_email_field")
        password = st.text_input("Mot de passe", type="password", placeholder="Votre mot de passe", key="login_password_field")
        submitted = st.form_submit_button("Se connecter", type="primary", width="stretch")

    if submitted:
        if not email or not password:
            panel.error("Veuillez renseigner votre email et votre mot de passe.", icon=":material/error:")
        else:
            with panel, st.spinner("Vérification…"):
                result = auth.login_user(email=email, password=password)

            if not result["ok"]:
                panel.error(result["message"], icon=":material/error:")
            elif result["user"]["role"] != "admin":
                panel.error("Accès réservé aux administrateurs.", icon=":material/block:")
            else:
                st.session_state[_SESSION_LOGGEDIN] = True
                st.session_state[_SESSION_USER_KEY] = result["user"]
                st.rerun()

    panel.markdown('<div class="mi-login-foot">© Inspirigence Group · Meeting Intelligence</div>', unsafe_allow_html=True)


def require_auth() -> dict:
    """Affiche la page de connexion et arrête l'exécution si l'utilisateur n'est pas connecté."""
    if not check_auth():
        login_page()
        st.stop()
    return get_current_user()
