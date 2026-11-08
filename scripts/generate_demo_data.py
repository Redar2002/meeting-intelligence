"""
generate_demo_data.py — Crée demo/meetings_demo.json : réunions FICTIVES pour le mode démo.
Entreprises, personnes et chiffres sont inventés ; aucune donnée réelle.

Thème : un intégrateur qui vend et déploie le CRM Kommo (pipeline, WhatsApp, Salesbot…).
Chaque réunion est assemblée à partir de phases (ouverture, découverte, démonstration,
objections, prix, intégration, formation, prochaines étapes…) tirées au hasard avec une graine fixe :
le fichier généré est toujours le même.

Usage :
    python scripts/generate_demo_data.py
"""
import json
import os
import random
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "demo", "meetings_demo.json")

# ─── Acteurs fictifs ──────────────────────────────────────────────────────────

SELLERS = ["Sara", "Youssef", "Amine", "Léa"]
CLIENTS = [
    # (entreprise, secteur, interlocuteur, rôle, décideur)
    ("Retail Plus", "la distribution", "Claire", "directrice des opérations", "Marc, le directeur financier"),
    ("NovaSaaS", "l'édition de logiciels RH", "Thomas", "head of sales", "Julie, la directrice commerciale"),
    ("Atlas Logistique", "le transport et la logistique", "Paul", "directeur des achats", "le comité de direction"),
    ("BioSanté", "la santé", "Inès", "responsable de l'innovation", "le directeur général"),
    ("Immo Horizon", "l'immobilier", "Karim", "directeur d'agence", "les associés"),
    ("EduNext", "la formation en ligne", "Sophie", "directrice commerciale", "le CEO"),
    ("AgriVerte", "l'agroalimentaire", "Hamza", "responsable commercial export", "la direction générale"),
    ("FinConseil", "le conseil financier", "Nora", "associée", "le comité des associés"),
    ("Hôtels Azur", "l'hôtellerie", "David", "directeur des ventes", "le directeur régional"),
    ("TechParts", "l'industrie", "Mehdi", "responsable grands comptes", "le directeur industriel"),
]
COMPETITORS = ["un autre CRM généraliste", "un outil développé en interne", "une solution de ticketing"]
PROJECT_TEAM = [("Nadia", "Chef de projet"), ("Karim", "Développeur"), ("Lina", "Data analyst"), ("Hugo", "Marketing")]

# ─── Phases d'une réunion commerciale ─────────────────────────────────────────
# Chaque phase est une liste d'échanges ; un échange est une liste de (rôle, texte).
# Rôles : "V" = commercial (vendeur), "C" = client.

OPENING = [
    [("V", "Bonjour {contact}, merci d'avoir pris ce temps. Comme convenu, on fait le point sur votre projet CRM chez {client} et sur ce que Kommo peut vous apporter."),
     ("C", "Bonjour, merci à vous. On a environ une heure, ça devrait suffire.")],
    [("V", "Avant de commencer, êtes-vous d'accord pour que la réunion soit enregistrée ? Cela nous permet de vous envoyer un compte rendu fidèle."),
     ("C", "Oui, pas de problème."),
     ("V", "Merci. Je vous propose dix minutes sur votre contexte, puis on passe directement dans Kommo.")],
    [("V", "Pour cadrer : votre contexte commercial, une démonstration de Kommo sur vos cas d'usage, puis les prochaines étapes. Ça vous convient ?"),
     ("C", "Parfait, c'est exactement ce dont on a besoin.")],
]

DISCOVERY = [
    [("V", "Comment gérez-vous vos prospects aujourd'hui ?"),
     ("C", "Sur des fichiers Excel partagés et dans les messageries des commerciaux. On perd des contacts, surtout ceux qui arrivent par WhatsApp.")],
    [("V", "D'où viennent principalement vos demandes clients ?"),
     ("C", "À {pct} % de WhatsApp et d'Instagram, le reste par le formulaire du site et le téléphone. Les réponses tardent parce que personne ne sait qui doit répondre.")],
    [("V", "Combien de commerciaux utiliseraient le CRM ?"),
     ("C", "{team} personnes au départ, réparties entre {city} et le télétravail. Peut-être plus si l'équipe support suit.")],
    [("V", "Quelles sont les grandes étapes de votre cycle de vente ?"),
     ("C", "Premier contact, qualification, envoi du devis, négociation, puis signature. Mais aujourd'hui on ne voit pas où les affaires bloquent.")],
    [("V", "Combien de temps vos commerciaux passent-ils sur les relances ?"),
     ("C", "Au moins {hours} heures par semaine chacun, et beaucoup de relances sont tout simplement oubliées.")],
    [("V", "Avez-vous déjà utilisé un CRM ?"),
     ("C", "On a testé {competitor}, mais il n'était pas adapté aux messageries. Les commerciaux sont vite revenus à WhatsApp sur leur téléphone personnel.")],
    [("V", "Qui suit les résultats commerciaux et comment ?"),
     ("C", "Le directeur commercial, chaque lundi, à partir de tableaux Excel consolidés à la main. Les chiffres arrivent toujours en retard.")],
    [("V", "Qu'est-ce qui se passerait si rien ne changeait cette année ?"),
     ("C", "On ne tiendrait pas l'objectif de croissance de {growth} %. On perd déjà des clients qui attendent trop longtemps une réponse.")],
]

DEMO = [
    [("V", "Voici le pipeline de vente dans Kommo. Chaque colonne correspond à une étape de votre cycle, et vous déplacez les affaires d'une étape à l'autre par glisser-déposer."),
     ("C", "On peut adapter les étapes à notre processus ?"),
     ("V", "Oui, entièrement : on reprendra vos cinq étapes, de la qualification à la signature.")],
    [("V", "Ici, l'intégration WhatsApp. Les messages arrivent directement dans la fiche du prospect, et toute l'équipe voit l'historique de la conversation."),
     ("C", "Donc si un commercial est absent, un collègue peut reprendre la discussion ?"),
     ("V", "Exactement, et le prospect garde le même numéro de contact.")],
    [("V", "Le Salesbot permet d'automatiser les premières réponses : accueil, questions de qualification, prise de rendez-vous."),
     ("C", "C'est ce qui nous manque le soir et le week-end, quand personne ne répond.")],
    [("V", "Les tâches et relances sont créées automatiquement à chaque étape du pipeline. Le commercial reçoit un rappel s'il n'a pas recontacté le prospect à temps."),
     ("C", "Ça réglerait notre problème de relances oubliées.")],
    [("V", "Côté pilotage, les rapports montrent le taux de conversion par étape, le délai de réponse et l'activité de chaque commercial."),
     ("C", "On pourrait exporter ces données vers Power BI ?"),
     ("V", "Oui, via l'API de Kommo ou un export planifié. C'est ce qu'on met en place pour plusieurs clients.")],
    [("V", "On peut aussi connecter Instagram, Facebook Messenger et le formulaire de votre site : tous les leads arrivent dans le même pipeline."),
     ("C", "Ça nous éviterait de jongler entre quatre applications.")],
]

OBJECTIONS = [
    [("C", "Le coût des licences s'ajoute à notre budget informatique, qui est déjà serré."),
     ("V", "Je comprends. On peut commencer avec une partie de l'équipe et un plan d'entrée de gamme. Si Kommo vous fait récupérer quelques affaires par mois grâce aux relances, il est rentabilisé.")],
    [("C", "Mes commerciaux sont habitués à WhatsApp sur leur téléphone, ils risquent de ne pas adopter le CRM."),
     ("V", "C'est justement l'intérêt de Kommo : ils continuent à discuter sur WhatsApp, mais les conversations sont centralisées. L'application mobile reprend la même interface.")],
    [("C", "On a peu de temps pour un projet de migration ce trimestre."),
     ("V", "Le déploiement prend environ {weeks} semaines : import de vos contacts depuis Excel, paramétrage du pipeline, puis une formation d'une demi-journée.")],
    [("C", "Et nos données clients ? On ne veut pas les perdre pendant la migration."),
     ("V", "On fait d'abord un import test sur un échantillon, vous validez, puis on importe l'ensemble. Vos fichiers d'origine restent intacts.")],
    [("C", "On hésite encore avec {competitor}."),
     ("V", "C'est une bonne solution, mais Kommo a été conçu autour des messageries. Pour une activité où {pct} % des demandes arrivent par WhatsApp, c'est un vrai avantage.")],
]

PRICING = [
    [("C", "Concrètement, combien ça coûterait pour une équipe comme la nôtre ?"),
     ("V", "Le prix des licences dépend du plan Kommo choisi ; je vous enverrai la grille officielle. Pour notre accompagnement, paramétrage, intégrations et formation, on serait autour de {price} euros."),
     ("C", "C'est raisonnable, mais il faudra le valider avec {decider}.")],
    [("C", "Est-ce qu'on peut tester avant de s'engager ?"),
     ("V", "Oui, Kommo propose une période d'essai. On peut la configurer avec votre vrai pipeline pour que le test soit représentatif."),
     ("C", "Ça rassurerait tout le monde en interne.")],
    [("C", "Si on s'engage sur l'année, il y a un geste possible sur l'accompagnement ?"),
     ("V", "Avec un engagement annuel, on peut réduire l'accompagnement de {discount} % et inclure une deuxième session de formation.")],
]

NEXT_STEPS = [
    [("V", "Pour la suite, je vous propose une réunion avec {decider} la semaine prochaine, avec la proposition chiffrée et le planning de déploiement."),
     ("C", "D'accord, je vous envoie ses disponibilités aujourd'hui.")],
    [("V", "Je vous envoie le compte rendu de la réunion et un accès d'essai à Kommo d'ici demain."),
     ("C", "Merci. On fait le point en interne et on revient vers vous d'ici {days} jours.")],
    [("V", "Si la proposition vous convient, on peut démarrer l'import des contacts dès le début du mois prochain."),
     ("C", "Ça me semble réaliste. Je confirme après validation par {decider}.")],
]

INTEGRATION = [
    [("V", "Aujourd'hui on se concentre sur la connexion de votre numéro WhatsApp Business à Kommo."),
     ("C", "Très bien. On a un seul numéro pour toute l'équipe, c'est un problème ?"),
     ("V", "Non, c'est même le cas idéal : les conversations sont réparties automatiquement entre les commerciaux.")],
    [("V", "On va aussi relier votre formulaire de contact : chaque demande crée une affaire dans la première étape du pipeline."),
     ("C", "Et on garde la source du lead ?"),
     ("V", "Oui, la source est enregistrée, ce qui vous permettra de mesurer le canal le plus rentable.")],
    [("V", "Pour Instagram, il faut un compte professionnel relié à une page Facebook. Vous l'avez déjà ?"),
     ("C", "Oui, c'est fait depuis l'an dernier.")],
    [("V", "On configure maintenant le Salesbot : message d'accueil, deux questions de qualification et proposition de rendez-vous."),
     ("C", "On peut écrire les messages en français et en arabe ?"),
     ("V", "Oui, on peut prévoir un message dans chaque langue selon la réponse du client.")],
]

TRAINING = [
    [("V", "Bienvenue à la formation Kommo. On commence par le pipeline : créer une affaire, la déplacer d'étape et ajouter une note."),
     ("C", "Est-ce qu'on peut retrouver toutes les affaires d'un même client ?"),
     ("V", "Oui, depuis la fiche contact, vous voyez toutes ses affaires et tout l'historique des échanges.")],
    [("V", "Deuxième point : les tâches. Chaque matin, vous ouvrez la liste des tâches du jour et vous traitez les relances en priorité."),
     ("C", "Et si une tâche est en retard ?"),
     ("V", "Elle passe en rouge et votre responsable la voit dans son tableau de bord.")],
    [("V", "Maintenant l'application mobile : vous recevez les messages WhatsApp des prospects directement dans Kommo."),
     ("C", "C'est plus simple que je pensais.")],
    [("V", "Pour finir, les modèles de messages : vous enregistrez vos réponses fréquentes et vous les envoyez en un clic."),
     ("C", "Ça va nous faire gagner beaucoup de temps sur les demandes de prix.")],
]

# ─── Réunions internes (point d'équipe sur les déploiements Kommo) ───────────

PROJECT = [
    ("Nadia", "Bonjour à tous. Point hebdomadaire sur les déploiements Kommo en cours et sur le connecteur Power BI, sprint {sprint}."),
    ("Karim", "L'import des contacts chez {c1} est terminé : plus de huit mille fiches, sans doublon après nettoyage."),
    ("Nadia", "Des blocages sur l'intégration WhatsApp chez {c2} ?"),
    ("Karim", "La validation du numéro WhatsApp Business a pris plus de temps que prévu. Ce sera connecté d'ici jeudi."),
    ("Lina", "Le connecteur entre l'API Kommo et Power BI est prêt. Il me manque juste les accès de production pour programmer le rafraîchissement quotidien."),
    ("Nadia", "Karim, tu peux lui transmettre les accès aujourd'hui ?"),
    ("Karim", "Oui, je m'en occupe juste après la réunion."),
    ("Hugo", "Côté marketing, deux nouveaux prospects sont arrivés via le webinaire sur Kommo et WhatsApp."),
    ("Lina", "Les rapports montrent que le délai moyen de réponse des clients déployés a nettement baissé depuis l'activation du Salesbot."),
    ("Nadia", "Très bon argument pour les prochaines démos. Hugo, tu peux en faire une étude de cas ?"),
    ("Hugo", "Oui, je la prépare pour la fin du mois."),
    ("Nadia", "Parfait. Prochain point même heure la semaine prochaine. Merci à tous."),
]


def _fill(text, ctx):
    return text.format(**ctx)


def _sales_meeting(rng, client, seller, kind):
    company, sector, contact, role, decider = client
    ctx = {
        "client": company, "contact": contact, "decider": decider, "competitor": rng.choice(COMPETITORS),
        "team": rng.choice([8, 12, 15, 20, 25, 40]), "city": rng.choice(["Casablanca", "Rabat", "Marrakech", "Tanger", "Agadir"]),
        "hours": rng.choice([2, 3, 4]), "growth": rng.choice([15, 20, 25, 30]), "weeks": rng.choice([3, 4, 6]),
        "price": rng.choice([1500, 2500, 3500, 4800]), "discount": rng.choice([10, 15]), "days": rng.choice([5, 7, 10]),
        "pct": rng.choice([60, 70, 80]),
    }
    # Phases selon le type de réunion
    plan = {
        "Découverte": [(OPENING, 2), (DISCOVERY, 6), (DEMO, 1), (NEXT_STEPS, 2)],
        "Démo": [(OPENING, 1), (DISCOVERY, 3), (DEMO, 5), (OBJECTIONS, 2), (NEXT_STEPS, 2)],
        "Négociation": [(OPENING, 1), (OBJECTIONS, 4), (PRICING, 3), (NEXT_STEPS, 2)],
        "Intégration": [(OPENING, 1), (INTEGRATION, 4), (DEMO, 2), (NEXT_STEPS, 1)],
        "Formation": [(OPENING, 1), (TRAINING, 4), (DEMO, 2), (NEXT_STEPS, 1)],
        "Suivi": [(OPENING, 1), (DISCOVERY, 2), (DEMO, 2), (OBJECTIONS, 2), (PRICING, 1), (NEXT_STEPS, 2)],
    }[kind]
    lines = []
    for phase, count in plan:
        for exchange in rng.sample(phase, min(count, len(phase))):
            for who, text in exchange:
                speaker = f"{seller} (Commercial)" if who == "V" else f"{contact} ({company})"
                lines.append((speaker, _fill(text, ctx)))
    title = {
        "Découverte": f"Découverte besoins CRM — {company}",
        "Démo": f"Démo Kommo CRM — {company}",
        "Négociation": f"Négociation licences Kommo — {company}",
        "Intégration": f"Intégration WhatsApp × Kommo — {company}",
        "Formation": f"Formation équipe Kommo — {company}",
        "Suivi": f"Suivi déploiement Kommo — {company}",
    }[kind]
    return title, lines


def _build(title, lines, when, filename):
    segments, raw = [], []
    t = 0
    for speaker, text in lines:
        duration = max(4, round(len(text.split()) / 2.4))  # ~145 mots/minute
        segments.append({"start": float(t), "end": float(t + duration), "text": text, "speaker": speaker})
        raw.append(f"[{t // 60:02d}:{t % 60:02d}] {speaker} : {text}")
        t += duration + 1
    return {
        "title": title,
        "meeting_id": when.strftime("%Y%m%d_%H%M%S"),
        "filename": filename,
        "segments": segments,
        "transcript": " ".join(s["text"] for s in segments),
        "transcript_clean": "\n".join(raw),
        "segments_clean": segments,
    }


def main():
    rng = random.Random(2026)
    meetings = []
    start = datetime(2026, 7, 6, 9, 30)
    kinds = ["Découverte", "Démo", "Négociation", "Intégration", "Formation", "Suivi"]
    deployed = []  # clients déjà en intégration / formation / suivi, cités dans les points d'équipe
    for i, client in enumerate(CLIENTS):
        seller = SELLERS[i % len(SELLERS)]
        # 2 réunions par client, dans l'ordre logique du cycle (découverte → … → suivi)
        chosen = sorted(rng.sample(kinds, 2), key=kinds.index)
        for j, kind in enumerate(chosen):
            when = start + timedelta(days=i * 9 + j * 17, hours=rng.choice([0, 2, 4, 6]))
            title, lines = _sales_meeting(rng, client, seller, kind)
            slug = title.split(" — ")[0].lower().replace(" ", "_").replace("×", "x")
            meetings.append(_build(title, lines, when, f"{slug}_{client[0].lower().replace(' ', '_')}.mp3"))
            if kind in ("Intégration", "Formation", "Suivi"):
                deployed.append(client[0])
    deployed = deployed or [c[0] for c in CLIENTS]
    for k, sprint in enumerate([12, 14, 16]):
        when = start + timedelta(days=20 + k * 35, hours=1)
        ctx = {"sprint": sprint, "c1": deployed[k % len(deployed)], "c2": deployed[(k + 1) % len(deployed)]}
        lines = [(f"{name} ({next(r for n, r in PROJECT_TEAM if n == name)})", _fill(text, ctx)) for name, text in PROJECT]
        meetings.append(_build(f"Point équipe déploiements Kommo — Sprint {sprint}", lines, when, f"point_equipe_kommo_sprint_{sprint}.mp3"))

    meetings.sort(key=lambda m: m["meeting_id"], reverse=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf8") as f:
        json.dump(meetings, f, indent=2, ensure_ascii=False)
    words = sum(len(m["transcript"].split()) for m in meetings)
    print(f"{len(meetings)} réunions fictives, {words} mots, écrites dans {OUT}")


if __name__ == "__main__":
    main()
