# Tema del Ministerio para Vaultwarden

Mismo lenguaje visual que la Wiki (Brandbook 2024): verdes institucionales, beige, rosa del lapacho, Oak Sans,
botones en píldora. Funciona en tema claro y oscuro.

| Carpeta | Qué es | Dónde se monta en el contenedor |
|---|---|---|
| `scss/user.vaultwarden.scss.hbs` | El CSS. Vaultwarden lo mezcla en su `/css/vaultwarden.css` (mecanismo oficial, no toca la imagen). | `/data/templates/scss` |
| `fonts/` | Oak Sans (licencia OFL, ver `OFL.txt`). | `/web-vault/fonts/ministerio` |
| `images/flor-lapacho.svg` | Logo (flor). | `/web-vault/images/ministerio` |
| `favicon/` | Favicon, apple-touch, íconos android. Reemplazan los de Vaultwarden. | archivo por archivo, ver `docker-compose.yml` |
| `tools/generar-iconos.py` | Regenera `favicon/` desde la flor (`pip install pillow`). | — |

## Aplicar cambios en el servidor

```bash
cd ~/vaultwarden
git pull
docker compose up -d --force-recreate vaultwarden
```

`--force-recreate` hace falta: Vaultwarden cachea el CSS al arrancar y los favicon son montajes de archivo.
Después, en el navegador, Ctrl+Shift+R.

## Cómo se diseña

El front de Bitwarden pinta todo con variables CSS: tríos RGB (`--color-primary-600: 62 108 81`) y paletas hex
(`--color-gray-*`, `--color-brand-*`). Casi todo el rediseño es reasignar esas variables en `:root` / `.theme_light`
y `.theme_dark`. Los retoques de forma (píldoras, esquinas) y el logo están al final del archivo.

Reglas del archivo: es SCSS compilado por Vaultwarden (`grass`), así que un error de sintaxis hace que Vaultwarden
ignore el archivo y muestre el tema original (avisa en `docker logs vaultwarden`). No usar `{{` (Handlebars).

## Limitaciones

- El color de la barra del navegador en móviles (`theme-color`) y el nombre en el manifest vienen del `index.html`
  del web vault; no se cambian desde CSS.
- Si se actualiza Vaultwarden y cambia el front, algún selector fino (logo, ilustración) podría necesitar ajuste.
