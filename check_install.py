#!/usr/bin/env python3
"""
Script de vérification de l'installation Google Ads Dashboard
"""

import sys
from pathlib import Path

def check_python_version():
    """Vérifie la version de Python"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} détecté — Python 3.11+ requis")
        return False


def check_dependencies():
    """Vérifie que les dépendances sont installées"""
    required_packages = [
        "streamlit",
        "google-ads",
        "pandas",
        "plotly",
        "cryptography",
        "diskcache",
    ]

    all_installed = True

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} non installé")
            all_installed = False

    return all_installed


def check_file_structure():
    """Vérifie la structure des fichiers"""
    base_dir = Path(__file__).parent

    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        "Dockerfile",
        "docker-compose.yml",
        ".env.example",
        ".gitignore",
        "config/settings.py",
        "modules/auth.py",
        "modules/storage.py",
        "modules/cache.py",
        "modules/google_ads_client.py",
        "modules/queries.py",
        "modules/diagnostics.py",
        "pages/1_🔧_Configuration.py",
        "pages/2_📊_Vue_Ensemble.py",
        "pages/3_🎯_Detail_Campagne.py",
        "pages/4_🔍_Termes_Recherche.py",
        "pages/5_⚕️_Diagnostic.py",
    ]

    all_exist = True

    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} manquant")
            all_exist = False

    return all_exist


def check_directories():
    """Vérifie et crée les répertoires nécessaires"""
    base_dir = Path(__file__).parent

    required_dirs = [
        ".credentials",
        ".cache",
        "exports",
    ]

    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name}/")
        else:
            dir_path.mkdir(exist_ok=True)
            print(f"✨ {dir_name}/ créé")

    return True


def check_client_secret():
    """Vérifie si client_secret.json existe"""
    base_dir = Path(__file__).parent
    client_secret_path = base_dir / "client_secret.json"

    if client_secret_path.exists():
        print(f"✅ client_secret.json présent")
        return True
    else:
        print(f"⚠️ client_secret.json manquant (à télécharger depuis Google Cloud Console)")
        return False


def main():
    """Lance toutes les vérifications"""
    print("=" * 60)
    print("🔍 Vérification de l'installation Google Ads Dashboard")
    print("=" * 60)

    print("\n📦 Version Python")
    python_ok = check_python_version()

    print("\n📚 Dépendances Python")
    deps_ok = check_dependencies()

    print("\n📁 Structure des fichiers")
    files_ok = check_file_structure()

    print("\n📂 Répertoires")
    dirs_ok = check_directories()

    print("\n🔐 Credentials OAuth")
    client_secret_ok = check_client_secret()

    print("\n" + "=" * 60)

    if all([python_ok, deps_ok, files_ok, dirs_ok]):
        print("✅ Installation complète !")

        if not client_secret_ok:
            print("\n⚠️ Action requise :")
            print("   Téléchargez client_secret.json depuis Google Cloud Console")
            print("   et placez-le à la racine du projet.")
            print("\n📖 Voir : QUICKSTART.md")
        else:
            print("\n🚀 Vous pouvez lancer l'application :")
            print("   streamlit run app.py")
            print("\n   ou avec Docker :")
            print("   docker-compose up")

        return 0
    else:
        print("❌ Installation incomplète")

        if not deps_ok:
            print("\n💡 Pour installer les dépendances :")
            print("   pip install -r requirements.txt")

        return 1


if __name__ == "__main__":
    sys.exit(main())
