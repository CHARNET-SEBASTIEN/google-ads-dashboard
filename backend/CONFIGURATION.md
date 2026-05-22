# ⚙️ Guide de Configuration Backend

## Variables d'environnement (.env)

Le fichier `backend/.env` contient toute la configuration. Les ports CORS sont maintenant **configurés par défaut** dans `settings.py`.

## 🌐 CORS - Ports supportés par défaut

✅ Les ports suivants fonctionnent directement :
- `http://localhost:4200` - Angular défaut
- `http://localhost:4201` - Angular alternatif  
- `http://localhost:4300` - Angular alternatif
- `http://localhost:5000` - Flask/alternatif
- `http://localhost:3000` - React/Next.js

**Aucune configuration nécessaire pour ces ports !**

## 🔧 Personnaliser CORS (optionnel)

### Option 1 : Modifier settings.py

```python
# backend/app/config/settings.py
CORS_ORIGINS: List[str] = Field(
    default=[
        "http://localhost:4200",
        "https://votre-domaine.com",  # Ajoutez ici
    ]
)
```

### Option 2 : Variable d'environnement (Format JSON)

```bash
export CORS_ORIGINS='["http://localhost:4200","https://monsite.com"]'
```

## 🔐 JWT & Sécurité

Générer une clé secrète :
```bash
openssl rand -hex 32
```

## 📚 Documentation complète

Voir `backend/README.md` pour plus de détails.
