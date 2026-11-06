#!/usr/bin/env python3
"""Genera branding/locales/es/messages.json: el español del front con "caja fuerte" -> "gestor de claves".

El texto "Cajas fuertes" no está en el CSS sino en el archivo de idiomas del front (traducción de Bitwarden).
Hay que partir del archivo de la versión que corre en el servidor, así que se genera desde la imagen:

  docker run --rm --entrypoint cat vaultwarden/server:latest /web-vault/locales/es/messages.json \
    | python3 branding/tools/generar-locale-es.py > branding/locales/es/messages.json

Ejecutar de nuevo después de actualizar Vaultwarden.
"""
import json, re, sys

G = "gestor de claves"
# Orden importa: lo más específico primero. Se cuida el género (la caja -> el gestor).
REGLAS = [
    (r"\bTodas las cajas fuertes\b", "Todos los gestores de claves"),
    (r"\bCajas fuertes\b", "Gestor de claves"),
    (r"\bcajas fuertes\b", "gestores de claves"),
    (r"\b([Uu])na caja fuerte\b", r"\1n " + G),
    (r"\bde la caja fuerte\b", "del " + G),
    (r"\ba la caja fuerte\b", "al " + G),
    (r"\bla caja fuerte\b", "el " + G),
    (r"\bLa caja fuerte\b", "El " + G),
    (r"\bCaja fuerte Web\b", "Gestor de claves"),
    (r"\bcaja fuerte web\b", G),
    (r"\bCaja fuerte\b", "Gestor de claves"),
    (r"\bcaja fuerte\b", G),
]
# Concordancia: participios/adjetivos que quedaron en femenino
CONCORDANCIA = [
    (r"([Gg]estor de claves)( de organización| de la organización)? (bloquead|desbloquead|purgad|exportad|importad)a\b", r"\1\2 \3o"),
    (r"([Gg]estor de claves) a la que\b", r"\1 al que"),
    (r"\bsu propia (gestor de claves)", r"su propio \1"),
    (r"\b(está|estar) desbloqueada\b", r"\1 desbloqueado"),
    (r"\b(está|estar) bloqueada\b", r"\1 bloqueado"),
    (r"\bha sido purgada\b", "ha sido purgado"),
    (r"(gestor de claves) máximo\b", r"\1 máximo"),
]

def conv(t):
    if not re.search(r"caja[s]? fuerte", t, re.I):
        return t
    for pat, rep in REGLAS + CONCORDANCIA:
        t = re.sub(pat, rep, t)
    return t

d = json.load(sys.stdin)
for v in d.values():
    if isinstance(v, dict) and isinstance(v.get("message"), str):
        v["message"] = conv(v["message"])
json.dump(d, sys.stdout, ensure_ascii=False, indent=2)
print()
