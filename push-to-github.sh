#!/bin/bash

echo "🚀 Configuration GitHub pour Google Ads Dashboard"
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📝 Étape 1: Créer le repo sur GitHub${NC}"
echo "   Allez sur: https://github.com/new"
echo "   - Nom du repo: google-ads-dashboard"
echo "   - Private ou Public"
echo "   - NE PAS cocher 'Initialize with README'"
echo ""
read -p "✓ Repo créé sur GitHub? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Créez d'abord le repo sur GitHub"
    exit 1
fi

echo -e "${YELLOW}🔗 Étape 2: URL du repo${NC}"
read -p "Entrez l'URL du repo (ex: https://github.com/username/google-ads-dashboard.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ URL requise"
    exit 1
fi

echo ""
echo -e "${YELLOW}📦 Étape 3: Commit initial${NC}"

# Vérifier si on est sur master ou main
BRANCH=$(git branch --show-current 2>/dev/null || echo "master")
echo "   Branche actuelle: $BRANCH"

# Changer pour main si on est sur master
if [ "$BRANCH" = "master" ]; then
    echo "   Passage de master à main..."
    git branch -M main
    BRANCH="main"
fi

# Add files
echo "   Ajout des fichiers..."
git add .

# Commit
echo "   Création du commit initial..."
git commit -m "🎨 Initial commit - Dashboard Google Ads avec design RAFO authentique

- Interface inspirée de rafo-chapters.com
- Mode clair (beige/stone) et mode sombre (bruns chauds)
- Multilingue: FR/EN/DE
- API Google Ads + Google Scripts
- Docker + Streamlit
- Design minimaliste et professionnel"

echo ""
echo -e "${YELLOW}🚀 Étape 4: Push vers GitHub${NC}"

# Add remote
echo "   Ajout du remote..."
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"

# Push
echo "   Push vers GitHub..."
git push -u origin $BRANCH

echo ""
echo -e "${GREEN}✅ TERMINÉ!${NC}"
echo ""
echo "🔗 Votre projet est maintenant sur GitHub:"
echo "   $REPO_URL"
echo ""
echo "📝 Pour les prochains commits:"
echo "   git add ."
echo "   git commit -m \"Description des changements\""
echo "   git push"
echo ""
