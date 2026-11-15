# Multiverso Comic - Motor Autónomo de Paneles e Imágenes de Cómic 📖📸

Sistema 100% automatizado para la curación, optimización y publicación autónoma de **paneles y momentos legendarios de cómics** en Facebook e Instagram, diseñado para maximizar el alcance orgánico, retención de lectura y debate en comentarios.

---

## 🚀 Características Principales

- **Frecuencia Autónoma:** **10 publicaciones al día** en las horas de mayor tráfico e interacción en redes sociales (de 08:00 AM a 09:30 PM).
- **Multiplataforma Nativo:** Publicación simultánea en:
  - **Página de Facebook** (`Multiverso Comic` / ID: `1289410784257454`) vía Graph API con resolución fotográfica completa.
  - **Feed de Instagram** (`@multiversoocomic` / ID: `17841427017671758`) vía Graph API Container publishing.
- **Copywriting Hipnótico:** Cada panel cuenta con:
  - 🎣 **Hook de alto impacto** para detener el *scroll*.
  - 📖 **Micro-narrativa** del contexto del cómic, número y año exacto.
  - 💬 **Llamada a la acción (CTA)** provocativa para desatar debates en comentarios.
  - 🏷️ **Hashtags optimizados** de alto volumen y nicho.
- **Optimización Visual Automática:** Gradación cinemática de color, contraste y adaptación de bordes con desenfoque suave para cumplir estrictamente con los límites de aspecto de Instagram (4:5 a 1.91:1).
- **Despacho Autónomo:** GitHub Actions gestiona la cola en `scheduled_queue/`, publica el siguiente panel, lo archiva en `published_ledger.json` y commitea los cambios sin intervención manual.

---

## ⏰ Programación Diaria (10 Horarios Pico)

| Post # | Hora Local (UTC-5) | Horario UTC | Objetivo de Contenido |
| :---: | :---: | :---: | :--- |
| **01** | `08:00 AM` | `13:00 UTC` | Apertura matutina: Momento heroico inspirador |
| **02** | `09:30 AM` | `14:30 UTC` | Curiosidad o revelación impactante |
| **03** | `11:00 AM` | `16:00 UTC` | Batalla brutal / Pelea épica |
| **04** | `12:30 PM` | `17:30 UTC` | Hora de almuerzo: Gran debate clásico |
| **05** | `02:00 PM` | `19:00 UTC` | Momento oscuro o perturbador |
| **06** | `03:30 PM` | `20:30 UTC` | Splash page de arte monumental |
| **07** | `05:00 PM` | `22:00 UTC` | Giro de trama o traición inolvidable |
| **08** | `06:30 PM` | `23:30 UTC` | Muerte legendaria o sacrificio |
| **09** | `08:00 PM` | `01:00 UTC` | Prime Time: El momento más viral del día |
| **10** | `09:30 PM` | `02:30 UTC` | Cierre nocturno: Reflexión o final épico |

---

## 📂 Estructura del Proyecto

```text
comics-paneles-espanol/
├── .github/
│   └── workflows/
│       └── publish_panels.yml       # Cronjobs y workflow de publicación
├── scheduled_queue/                 # Cola FIFO de paneles pendientes
│   ├── 001_wolverine_muerte.../
│   │   ├── image.jpg                # Imagen en alta resolución optimizada
│   │   └── metadata.json            # Título, contexto, hook, CTA y hashtags
│   └── ...
├── src/
│   ├── cloud_runner.py              # Despachador principal que consume la cola
│   ├── publisher.py                 # Conectores Meta Graph API (FB + IG)
│   └── image_optimizer.py           # Gradación de color y ajuste 4:5
├── scripts/
│   └── populate_panels_queue.py     # Creador de lotes de paneles masivos
├── published_ledger.json            # Historial inmutable de publicaciones realizadas
├── requirements.txt
└── .env                             # Claves y credenciales locales
```

---

## 🔑 Configuración de Secretos en GitHub

En el repositorio de GitHub, añade los siguientes secretos en **Settings -> Secrets and variables -> Actions**:

| Secreto | Descripción | Valor |
| :--- | :--- | :--- |
| `FB_PAGE_TOKEN` | Token de acceso de la Página de Meta | Token de Graph API |
| `FB_PAGE_ID` | ID de la Página de Facebook | `1289410784257454` |
| `IG_USER_ID` | ID de la Cuenta de Instagram Business | `17841427017671758` |
| `GEMINI_API_KEY` | Clave de API de Gemini | Clave de Google AI Studio |

---

## 🛠️ Comandos de Utilidad

### 1. Poblar la cola con nuevos paneles
```powershell
python scripts/populate_panels_queue.py
```

### 2. Probar el despachador en modo simulación (Dry Run)
```powershell
python src/cloud_runner.py --dry-run
```

### 3. Publicar manualmente el siguiente panel ahora mismo
```powershell
python src/cloud_runner.py
```
