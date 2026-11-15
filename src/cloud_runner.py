"""
Autonomous Cloud Runner & Queue Consumer for Comic Panels
Executes on GitHub Actions (10 times daily) to publish scheduled comic panels.
"""

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

# Force UTF-8 stdout
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr:
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.publisher import publish_comic_photo

LEDGER_PATH = PROJECT_ROOT / "published_ledger.json"
QUEUE_DIR = PROJECT_ROOT / "scheduled_queue"

def load_env_file():
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env_file()


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] [CloudRunner] {msg}", flush=True)


def load_ledger() -> list[dict]:
    if LEDGER_PATH.exists():
        try:
            with open(LEDGER_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log(f"Aviso al cargar ledger: {e}")
    return []


def save_ledger(ledger: list[dict]):
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)


def format_full_caption(meta: dict) -> str:
    """Combines hook, comic context, CTA question, and hashtags into a viral caption."""
    hook = meta.get("hook") or meta.get("title") or "¡Momento épico de cómic!"
    story = meta.get("story") or meta.get("caption") or ""
    comic = meta.get("comic_source") or meta.get("comic") or ""
    cta = meta.get("debate_question") or meta.get("cta") or "¿Qué opinas de este momento? Déjalo en los comentarios 👇"
    tags = meta.get("hashtags") or "#ComicsEnEspañol #Comics #Marvel #DCComics"

    parts = [f"🔥 {hook}"]
    if story:
        parts.append(story)
    if comic:
        parts.append(f"📖 Cómic: {comic}")
    parts.append(f"💬 {cta}")
    parts.append(f"\n{tags}")

    return "\n\n".join(parts)


def run_cloud_step(dry_run: bool = False, draft: bool = False):
    log("===========================================================")
    log("🌟 INICIANDO EJECUCIÓN DEL MOTOR AUTÓNOMO DE PANELES DE CÓMIC")
    log("===========================================================")

    if not QUEUE_DIR.exists():
        QUEUE_DIR.mkdir(parents=True, exist_ok=True)

    pending_items = sorted([
        d for d in QUEUE_DIR.iterdir()
        if d.is_dir() and any((d / f).exists() for f in ["image.jpg", "image.png", "panel.jpg", "panel.png"])
    ])

    if not pending_items:
        log("⚠️ No hay paneles pendientes en scheduled_queue. Cola vacía.")
        return

    target_item = pending_items[0]
    log(f"🎯 Panel seleccionado para despacho: '{target_item.name}'")

    meta_file = target_item / "metadata.json"
    meta = {}
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as mf:
                meta = json.load(mf)
        except Exception as me:
            log(f"Error leyendo metadata.json: {me}")

    # Find image file
    image_file = None
    for cand in ["image.jpg", "image.png", "panel.jpg", "panel.png"]:
        if (target_item / cand).exists():
            image_file = target_item / cand
            break

    if not image_file:
        log(f"❌ No se encontró imagen en '{target_item.name}'. Omitiendo...")
        return

    full_caption = format_full_caption(meta)
    title = meta.get("title", target_item.name)

    repo_owner = os.environ.get("GITHUB_REPO_OWNER", "Lorecomicvault")
    repo_name = os.environ.get("GITHUB_REPO_NAME", "comics-paneles-espanol")
    rel_img_path = image_file.relative_to(PROJECT_ROOT).as_posix()
    raw_github_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{rel_img_path}"

    log(f"   Título: {title}")
    log(f"   Archivo: {image_file.name} ({image_file.stat().st_size / 1024:.1f} KB)")
    log(f"   URL pública prevista: {raw_github_url}")

    if dry_run:
        log("[DRY-RUN] Simulación completa. Caption:")
        print("-" * 50)
        print(full_caption)
        print("-" * 50)
        return

    # Execute publication exclusively on Facebook Page
    pub_results = publish_comic_photo(
        image_path=image_file,
        caption=full_caption,
        image_url=raw_github_url,
        platforms=["facebook"],
        draft_only=draft
    )

    # Record in ledger
    ledger = load_ledger()
    ledger_entry = {
        "id": meta.get("id") or target_item.name,
        "title": title,
        "character": meta.get("character", ""),
        "comic_source": meta.get("comic_source", ""),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "social_links": {
            "facebook": pub_results.get("facebook", {}).get("permalink")
        },
        "status": "published",
        "platform": "facebook",
        "caption": full_caption
    }
    ledger.append(ledger_entry)
    save_ledger(ledger)

    # Remove consumed folder from queue
    try:
        shutil.rmtree(target_item, ignore_errors=True)
        log(f"✅ Panel '{target_item.name}' consumido y removido de scheduled_queue.")
    except Exception as re:
        log(f"Advertencia eliminando carpeta de cola: {re}")

    log(f"🎉 ¡Despacho exitoso de '{target_item.name}' completado!")


def main():
    parser = argparse.ArgumentParser(description="Despachador autónomo de paneles de cómic")
    parser.add_argument("--dry-run", action="store_true", help="Simular sin publicar")
    parser.add_argument("--draft", action="store_true", help="Guardar como borrador")
    args = parser.parse_args()

    run_cloud_step(dry_run=args.dry_run, draft=args.draft)


if __name__ == "__main__":
    main()
