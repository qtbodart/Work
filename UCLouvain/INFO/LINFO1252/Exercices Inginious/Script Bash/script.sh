#!bin/bash

# Vérification du nombre d'arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 chemin_du_dossier_de_code"
    exit 1
fi

CHEMIN_DOSSIER=$1
NOM_DOSSIER=$(basename "$CHEMIN_DOSSIER")
DATE_GENERATION=$(date --rfc-3339=seconds)
USER_HOST=$(whoami)@$(hostname)
MANIFEST_FILE="manifest.txt"

if [ ! -d "$CHEMIN_DOSSIER" ]; then
    echo "Le dossier spécifié n'existe pas."
    exit 1
fi

if [ -f "$CHEMIN_DOSSIER/Makefile" ]; then
    echo "Makefile détecté, exécution de 'make clean'..."
    (cd "$CHEMIN_DOSSIER" && make clean)
fi

LIGNES_TOTAL=$(find "$CHEMIN_DOSSIER" \( -name "*.c" -o -name "*.h" -o -name "*.py" \) -type f | xargs wc -l | tail -n 1 | awk '{print $1}')

# Création du fichier manifest.txt
echo "$DATE_GENERATION" > "$MANIFEST_FILE"
echo "$LIGNES_TOTAL" >> "$MANIFEST_FILE"
echo "$USER_HOST" >> "$MANIFEST_FILE"

# Création de l'archive .tar.xz
ARCHIVE_NAME="${NOM_DOSSIER}.tar.xz"
tar -cJf "$ARCHIVE_NAME" -C "$(dirname "$CHEMIN_DOSSIER")" "$NOM_DOSSIER" "$MANIFEST_FILE"

rm "$MANIFEST_FILE"
