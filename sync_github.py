import subprocess
import time
import os
from datetime import datetime

# --- CONFIGURATION ---
# Liste des fichiers à envoyer sur GitHub
FILES_TO_SYNC = ["user_cards.json", "atharine.json", "noms.json"]
# Intervalle de temps (3600 secondes = 1 heure)
INTERVAL = 3600

def push_to_github():
    try:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 Vérification des fichiers...")

        files_found = []
        for file in FILES_TO_SYNC:
            if os.path.exists(file):
                files_found.append(file)
            else:
                print(f"⚠️  Attention : {file} n'existe pas encore (attends que le bot le crée).")

        if not files_found:
            print("❌ Aucun fichier trouvé. Annulation du push.")
            return

        # 1. Ajouter les fichiers au "stage" Git
        subprocess.run(["git", "add"] + files_found, check=True)

        # 2. Créer le commit avec un message horodaté
        commit_message = f"Mise à jour auto : {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        # On utilise une petite astuce pour ne pas crash s'il n'y a rien de nouveau à commit
        subprocess.run(["git", "commit", "-m", commit_message], check=False)

        # 3. Envoyer vers GitHub
        # Note : Assure-toi que ton dossier est déjà lié à ton GitHub (git remote add origin ...)
        result = subprocess.run(["git", "push"], capture_output=True, text=True, check=True)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ GitHub mis à jour avec succès !")

    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Git : {e}")
    except Exception as e:
        print(f"❌ Erreur système : {e}")

if __name__ == "__main__":
    print("------------------------------------------")
    print("🚀 SCRIPT DE SYNCHRONISATION GITHUB LANCÉ")
    print(f"⏰ Fréquence : Toutes les heures")
    print("------------------------------------------")

    while True:
        push_to_github()
        print(f"⏳ Prochaine mise à jour à {datetime.now().hour + 1}h00...")
        time.sleep(INTERVAL)