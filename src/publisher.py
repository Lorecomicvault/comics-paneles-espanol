"""
Comic Panels Social Publisher (Facebook & Instagram)
Multi-platform publisher for high-impact comic panels & splash pages.
Brand: Multiverso Comic
- Facebook Page (ID: 1289410784257454)
- Instagram Business (ID: 17841427017671758)
"""

import os
import re
import sys
import time
from pathlib import Path
import requests

from .image_optimizer import optimize_comic_image

DEFAULT_PAGE_ID = "1289410784257454"
DEFAULT_IG_USER_ID = "17841427017671758"
DEFAULT_ACCESS_TOKEN = "EAAduw9ZBIaysBSVYGkNZCmRYBKHwiPpwlkZBiFxM5SNCWCBnmMLhl7SDSvUNFJXzn6xSYQBeKDNseZA3bM5cwCxcIV7L4bim7nlIU5CtgsB8gZCy82iew2MZB72Q13ODT8yBKcFrdRHXhUziR7DwOqMCoZBOcTd4whcwZByMWR4xQfqWJEl7gHZCRT3HOtZA73OMBCaZCzi"
GRAPH_API_VERSION = "v20.0"


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] [PhotoPublisher] {msg}", flush=True)


def upload_to_temporary_public_url(image_path: str | Path) -> str:
    """
    Uploads the local image to a temporary public HTTPS host (tmpfiles.org)
    and extracts the direct link for Meta's Instagram container builder.
    """
    ipath = Path(image_path)
    if not ipath.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    log(f"Subiendo imagen temporalmente a host público ({ipath.name})...")
    upload_url = "https://tmpfiles.org/api/v1/upload"

    with open(ipath, "rb") as f:
        r = requests.post(upload_url, files={"file": f}, timeout=60)

    if r.status_code != 200:
        raise RuntimeError(f"Error subiendo imagen temporal ({r.status_code}): {r.text}")

    data = r.json()
    raw_url = data.get("data", {}).get("url")
    if not raw_url:
        raise RuntimeError(f"Respuesta inesperada de host temporal: {data}")

    direct_url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
    log(f"URL pública directa obtenida: {direct_url}")
    return direct_url


def publish_to_facebook_photo(
    image_path: str | Path,
    caption: str,
    page_id: str | None = None,
    page_token: str | None = None
) -> dict:
    """Publishes a high-resolution photo directly to Facebook Page timeline."""
    pid = page_id or os.environ.get("FB_PAGE_ID", DEFAULT_PAGE_ID)
    token = page_token or os.environ.get("FB_PAGE_TOKEN", DEFAULT_ACCESS_TOKEN)
    ipath = Path(image_path)

    if not ipath.exists():
        return {"success": False, "error": f"Image not found: {image_path}"}

    log(f"Publicando foto en Facebook Page '{pid}'...")
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{pid}/photos"
    payload = {
        "caption": caption,
        "access_token": token,
        "published": "true"
    }

    mime = "image/png" if ipath.suffix.lower() == ".png" else "image/jpeg"
    try:
        with open(ipath, "rb") as f:
            files = {"source": (ipath.name, f, mime)}
            res = requests.post(url, data=payload, files=files, timeout=90).json()

        if "id" in res:
            photo_id = res["id"]
            post_id = res.get("post_id", photo_id)
            fb_link = f"https://facebook.com/{post_id}"
            log(f"✅ Foto publicada exitosamente en Facebook: {fb_link} (ID: {photo_id})")
            return {"success": True, "photo_id": photo_id, "post_id": post_id, "permalink": fb_link}
        else:
            log(f"❌ Error publicando en Facebook: {res}")
            return {"success": False, "error": res}
    except Exception as e:
        log(f"❌ Excepción publicando en Facebook: {e}")
        return {"success": False, "error": str(e)}


def publish_to_instagram_photo(
    image_path: str | Path,
    caption: str,
    image_url: str | None = None,
    ig_user_id: str | None = None,
    page_token: str | None = None,
    max_wait_seconds: int = 120
) -> dict:
    """Publishes a single photo post to Instagram Business feed via Graph API."""
    ig_id = ig_user_id or os.environ.get("IG_USER_ID", DEFAULT_IG_USER_ID)
    token = page_token or os.environ.get("FB_PAGE_TOKEN", DEFAULT_ACCESS_TOKEN)
    ipath = Path(image_path)

    log(f"Iniciando publicación en Instagram Business '{ig_id}'...")

    # Ensure image is optimized and within Instagram aspect ratio (4:5 to 1.91:1)
    opt_image = optimize_comic_image(ipath, for_instagram=True)

    # Resolve public image URL (GitHub raw link or temporary upload)
    pub_url = image_url
    if not pub_url:
        try:
            pub_url = upload_to_temporary_public_url(opt_image)
        except Exception as e:
            log(f"Advertencia subiendo imagen temporal: {e}")

    if not pub_url:
        return {"success": False, "error": "No se pudo obtener URL pública para Instagram"}

    # Step 1: Create Container
    create_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_id}/media"
    payload = {
        "image_url": pub_url,
        "caption": caption,
        "access_token": token
    }

    try:
        r = requests.post(create_url, data=payload, timeout=60)
        res = r.json()
        if "id" not in res:
            log(f"❌ Error creando contenedor de Instagram: {res}")
            return {"success": False, "error": res}

        creation_id = res["id"]
        log(f"Contenedor creado en Instagram (ID: {creation_id}). Esperando procesamiento...")

        # Step 2: Poll container status
        status_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{creation_id}"
        start_time = time.time()
        while time.time() - start_time < max_wait_seconds:
            s_res = requests.get(status_url, params={"fields": "status_code", "access_token": token}, timeout=15).json()
            code = s_res.get("status_code")
            if code == "FINISHED":
                log("Contenedor listo para publicar.")
                break
            elif code == "ERROR":
                log(f"❌ Error en procesamiento de contenedor: {s_res}")
                return {"success": False, "error": s_res}
            time.sleep(3)

        # Step 3: Publish container
        pub_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_id}/media_publish"
        pub_res = requests.post(pub_url, data={"creation_id": creation_id, "access_token": token}, timeout=60).json()

        if "id" in pub_res:
            media_id = pub_res["id"]
            # Fetch post permalink
            perm_res = requests.get(
                f"https://graph.facebook.com/{GRAPH_API_VERSION}/{media_id}",
                params={"fields": "permalink", "access_token": token},
                timeout=15
            ).json()
            permalink = perm_res.get("permalink", f"https://instagram.com/p/{media_id}")
            log(f"✅ Foto publicada exitosamente en Instagram: {permalink} (Media ID: {media_id})")
            return {"success": True, "media_id": media_id, "permalink": permalink}
        else:
            log(f"❌ Error al publicar contenedor en Instagram: {pub_res}")
            return {"success": False, "error": pub_res}

    except Exception as e:
        log(f"❌ Excepción publicando en Instagram: {e}")
        return {"success": False, "error": str(e)}


def publish_comic_photo(
    image_path: str | Path,
    caption: str,
    image_url: str | None = None,
    platforms: list[str] | None = None,
    draft_only: bool = False
) -> dict:
    """Orchestrates publishing of a comic panel across Facebook and Instagram."""
    if platforms is None:
        platforms = ["facebook", "instagram"]

    log("===========================================================")
    log("🚀 PUBLICADOR MULTIPLATAFORMA DE PANELES DE CÓMIC")
    log(f"   Archivo: {image_path}")
    log(f"   Plataformas: {platforms} | Modo Borrador: {draft_only}")
    log("===========================================================")

    results = {}

    if draft_only:
        log("[MODO BORRADOR] Simulación completada sin enviar a redes.")
        return {"draft": True, "facebook": {"success": True}, "instagram": {"success": True}}

    if "facebook" in platforms:
        fb_res = publish_to_facebook_photo(image_path=image_path, caption=caption)
        results["facebook"] = fb_res

    if "instagram" in platforms:
        ig_res = publish_to_instagram_photo(image_path=image_path, caption=caption, image_url=image_url)
        results["instagram"] = ig_res

    return results
