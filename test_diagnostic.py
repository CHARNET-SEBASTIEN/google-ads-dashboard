#!/usr/bin/env python3
"""
Script de diagnostic complet pour le dashboard Google Ads
"""

import sys
import os

print("="*60)
print("DIAGNOSTIC DU DASHBOARD GOOGLE ADS")
print("="*60)

# Test 1: Imports
print("\n1. Test des imports...")
try:
    import streamlit as st
    print("   ✅ streamlit")
except Exception as e:
    print(f"   ❌ streamlit: {e}")
    sys.exit(1)

try:
    from config.settings import STREAMLIT_CONFIG
    print("   ✅ config.settings")
except Exception as e:
    print(f"   ❌ config.settings: {e}")

try:
    from config.i18n import t, init_language
    print("   ✅ config.i18n")
except Exception as e:
    print(f"   ❌ config.i18n: {e}")

try:
    from utils.ui_helpers import load_custom_css, init_theme
    print("   ✅ utils.ui_helpers")
except Exception as e:
    print(f"   ❌ utils.ui_helpers: {e}")

try:
    from components.sidebar import render_custom_sidebar, hide_default_navigation
    print("   ✅ components.sidebar")
except Exception as e:
    print(f"   ❌ components.sidebar: {e}")

try:
    from components.topbar import render_topbar, TOPBAR_CSS
    print("   ✅ components.topbar")
except Exception as e:
    print(f"   ❌ components.topbar: {e}")

try:
    from utils.preferences import user_prefs
    print("   ✅ utils.preferences")
except Exception as e:
    print(f"   ❌ utils.preferences: {e}")

# Test 2: Fichiers CSS
print("\n2. Vérification des fichiers CSS...")
css_files = [
    "assets/custom.css",
    "assets/custom-dark-rafo.css",
    "assets/google-ads-logo.svg"
]

for f in css_files:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"   ✅ {f} ({size} bytes)")
    else:
        print(f"   ❌ {f} - INTROUVABLE")

# Test 3: Préférences utilisateur
print("\n3. Test des préférences...")
try:
    from utils.preferences import user_prefs
    lang = user_prefs.get_language()
    dark = user_prefs.is_dark_mode()
    print(f"   Langue: {lang}")
    print(f"   Mode sombre: {dark}")
    print("   ✅ Préférences OK")
except Exception as e:
    print(f"   ❌ Erreur préférences: {e}")

# Test 4: Modules script_data_loader
print("\n4. Test script_data_loader...")
try:
    from modules.script_data_loader import script_loader
    exists = script_loader.data_exists()
    print(f"   Données existent: {exists}")
    if exists:
        account = script_loader.get_account_info()
        print(f"   Compte: {account.get('name') if account else 'N/A'}")
    print("   ✅ script_loader OK")
except Exception as e:
    print(f"   ❌ script_loader: {e}")

# Test 5: Traductions
print("\n5. Test des traductions...")
try:
    from config.i18n import t
    tests = ["home", "config", "overview", "connected"]
    for key in tests:
        translation = t(key)
        print(f"   {key} -> {translation}")
    print("   ✅ Traductions OK")
except Exception as e:
    print(f"   ❌ Traductions: {e}")

print("\n" + "="*60)
print("DIAGNOSTIC TERMINÉ")
print("="*60)
