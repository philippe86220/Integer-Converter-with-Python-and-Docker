# 1. On part d'une image Python déjà prête
FROM python:3.12-slim

# 2. On définit le dossier de travail dans le conteneur
WORKDIR /app

# 3. On copie uniquement le fichier des dépendances d'abord
COPY convert.py .

# 4. On définit une commande fixe, tout ce qui est ajouté après le nom de l'image au "docker run" 
# est passé en argument à cette commande

ENTRYPOINT ["python", "convert.py"]
