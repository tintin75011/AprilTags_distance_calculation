
# AprilTag Vision

Détection d'AprilTags avec estimation de pose en temps réel via une webcam. Le programme utilise OpenCV, NumPy et la bibliothèque `pupil_apriltags` pour identifier plusieurs tags, afficher leur position (x, y, z), leur rotation autour de l’axe Z, et la distance entre eux.
![Capture d'écran de l'application](images\Capture.PNG)

## 🔧 Prérequis

- Python 3.10 ou supérieur
- [Poetry](https://python-poetry.org/) (gestionnaire de dépendances)

## 📦 Installation

1. Clone ce dépôt :

```bash
git clone https://github.com/tintin75011/apriltag-vision.git
cd apriltag-vision 
```

2. Installe les dépendances avec Poetry :

```bash
pip install poetry
poetry install
```

3. Lance le script principal :
```bash
poetry run python main.py
```

## 📷 Fonctionnalités

- 🎯 Détection d’AprilTags via webcam
- 📍 Estimation de la position `(x, y, z)` pour chaque tag détecté
- 📏 Affichage de la distance et des décalages entre les tags `0`, `1` et `2`
- 🔄 Affichage de la rotation autour de l'axe **Z**
- 🧵 Trait visuel entre les centres des tags

---

## 🛠 Technologies utilisées

- `opencv-python`
- `numpy`
- `pupil-apriltags`

---

## 📄 Exemple de sortie visuelle

L’application affiche une fenêtre avec :

- L’image de la webcam
- Les coins et ID de chaque tag
- Leur position `(x, y, z)`
- Les distances entre les tags
- Leur orientation (rotation autour de Z)

---

## 📜 Licence

**MIT License** – libre à toi de modifier, partager ou intégrer ce projet dans le tien !
