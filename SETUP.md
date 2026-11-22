# Guide d'installation (Mac et Windows)

À suivre dans l'ordre. Durée : environ 15 minutes.

**Versions à utiliser :** Python **3.12** (3.10 minimum, la 3.9 plante) et pygame 2.6.1 (installé automatiquement).

---

## 1. Installer Git

| Mac | Windows |
|---|---|
| `brew install git` (ou accepter l'installation des Command Line Tools si le Mac la propose) | `winget install Git.Git` (ou installateur sur git-scm.com, options par défaut) |

Vérification :
```bash
git --version
```

## 2. Configurer Git (une seule fois)

Utilise **le même email que ton compte GitHub**, sinon tes commits ne seront pas rattachés à ton profil.

```bash
git config --global user.name "Prénom Nom"
git config --global user.email "email-github@exemple.com"
```

## 3. Installer Python 3.12

| Mac | Windows |
|---|---|
| `brew install python@3.12` | `winget install Python.Python.3.12` (ou installateur sur python.org en **cochant « Add python.exe to PATH »**) |

Vérification :

| Mac | Windows |
|---|---|
| `python3.12 --version` | `py -3.12 --version` |

Le Python 3.9 fourni avec le Mac peut rester installé, on appelle simplement `python3.12`.

## 4. Accéder au dépôt GitHub

1. **Accepter l'invitation** de collaborateur reçue par email (sinon impossible de pousser).
2. Se connecter à GitHub depuis le terminal (le mot de passe n'est plus accepté) :

| Mac | Windows |
|---|---|
| `brew install gh` | `winget install GitHub.cli` |

Puis, sur les deux :
```bash
gh auth login
```
Choisir : GitHub.com, puis HTTPS, puis connexion par le navigateur.

## 5. Récupérer le projet

```bash
git clone https://github.com/valeriiarybalka18/kart_racing_2d.git
cd kart_racing_2d
```

Ce dossier est la **racine du projet** : toutes les commandes se lancent d'ici.

## 6. Créer l'environnement virtuel

Chacun crée le sien en local. Il n'est jamais envoyé sur GitHub.

| Mac | Windows (PowerShell) |
|---|---|
| `python3.12 -m venv .venv` | `py -3.12 -m venv .venv` |
| `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |

Le prompt doit commencer par `(.venv)`. Vérification :
```bash
python --version
```
Doit afficher `3.12.x`.

> Windows : si PowerShell refuse d'activer le venv, lancer une fois
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, puis recommencer.

Le venv se **réactive à chaque nouveau terminal**. Pour en sortir : `deactivate`.

## 7. Installer les dépendances

Venv activé :
```bash
pip install --upgrade pip
pip install -r requirements-dev.txt
```

## 8. Lancer le jeu et les tests

```bash
python main.py
python -m pytest
```

Utiliser `python -m pytest` (et non `pytest` seul), sinon les imports du projet peuvent échouer.

**VS Code :** ouvrir le dossier racine, puis `Cmd/Ctrl + Shift + P`, puis **Python: Select Interpreter**, et choisir celui de `.venv`.

---

## Travailler au quotidien

**Avant de commencer, toujours :**
```bash
git pull
```

**Après un changement cohérent :**
```bash
git status
git add .
git commit -m "Message précis"
git push
```

**Messages de commit** : dire ce qui a été fait.
- Bon : `Ajoute le freinage et la marche arrière à la classe Car`
- Mauvais : `update`, `fix`, `modif`

**Règles du groupe :**
- Plusieurs petits commits par séance, pas un énorme à la fin.
- Ne jamais commiter `.venv/`, `__pycache__/`, ni de mots de passe.
- Ne jamais faire `git push --force`.
- Si `git push` est refusé (`rejected` / `fetch first`) : `git pull`, puis `git push`. En cas de conflit, le résoudre à plusieurs.
- Pas de `print` de debug dans les commits.
- Se mettre d'accord sur les noms et paramètres des méthodes qui se parlent entre vos parties.

**Option : une branche par fonctionnalité**
```bash
git switch -c feature/nom-de-la-fonctionnalite
git push -u origin feature/nom-de-la-fonctionnalite
```
Puis une Pull Request vers `main`, relue par un autre membre.

## Structure du projet

```
model/        règles du jeu (voiture, circuit, terrains, blocs)
view/         affichage pygame (lecture seule du modèle)
controller/   touches, boucle de jeu, états
tests/        tests sans fenêtre pygame
docs/         diagramme UML
```

## Utilisation de l'IA (obligatoire)

Le README doit déclarer si une IA a été utilisée pour : traduire ou expliquer le sujet, la conception, écrire du code, le débogage, les commentaires et docstrings, le diagramme UML.

Tout code généré doit être **relu et compris** (l'oral peut porter sur n'importe quelle partie), et les commentaires adressés à l'utilisateur de l'IA doivent être supprimés ou réécrits.

## Problèmes fréquents

| Problème | Solution |
|---|---|
| `TypeError` sur `X \| None` | Python trop ancien : vérifier `python --version` (3.10 minimum) |
| `ModuleNotFoundError: pygame` | Venv non activé, ou `pip install -r requirements-dev.txt` oublié |
| `ModuleNotFoundError` dans les tests | Utiliser `python -m pytest` depuis la racine |
| `Authentication failed` au push | Refaire `gh auth login` et vérifier l'invitation GitHub |
| Le prompt n'affiche pas `(.venv)` | Réactiver le venv |
