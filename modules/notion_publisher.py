import os
from notion_client import Client
from dotenv import load_dotenv
from report_builder import get_nivel_emoji, get_prioridad_emoji

load_dotenv()

def get_notion_client():
    token = os.getenv("NOTION_TOKEN")
    if not token:
        raise ValueError("NOTION_TOKEN no encontrado en .env")
    return Client(auth=token)

def heading(text: str, level: int = 2) -> dict:
    types = {1: "heading_1", 2: "heading_2", 3: "heading_3"}
    return {
        "object": "block",
        "type": types.get(level, "heading_2"),
        types.get(level, "heading_2"): {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }

def paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }

def divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}

def build_candidate_row(candidate: dict, puesto_key: str) -> str:
    """Construye una línea de texto con la info clave del candidato."""
    nombre = candidate.get("nombre", candidate.get("archivo", "Sin nombre"))
    puesto = candidate.get(puesto_key, {})
    score = puesto.get("score", 0)
    nivel = puesto.get("nivel", "")
    resumen = puesto.get("resumen", "")
    alertas = puesto.get("alertas", [])
    prioridad = candidate.get("prioridad", 3)
    nota = candidate.get("nota_reclutador", "")

    emoji_nivel = get_nivel_emoji(nivel)
    emoji_prioridad = get_prioridad_emoji(prioridad)

    alerta_text = f" | ⚠️ {alertas[0]}" if alertas else ""
    return f"{emoji_prioridad} {emoji_nivel} [{score}/100] {nombre} — {resumen}{alerta_text} | 💬 {nota}"

def publish_report(report: dict) -> str:
    """
    Publica el reporte completo en Notion y retorna la URL de la página creada.
    """
    notion = get_notion_client()
    parent_id = os.getenv("NOTION_PARENT_PAGE_ID")

    if not parent_id:
        raise ValueError("NOTION_PARENT_PAGE_ID no encontrado en .env")

    fecha = report["fecha"]
    job_a = report["job_a_name"]
    job_b = report["job_b_name"]
    stats = report["stats"]

    blocks = []

    # --- RESUMEN EJECUTIVO ---
    blocks.append(heading("📊 Resumen Ejecutivo", 2))
    blocks.append(paragraph(
        f"Fecha: {fecha}\n"
        f"Total candidatos evaluados: {stats['total']}\n"
        f"Recomendados para {job_a}: {stats['para_puesto_a']}\n"
        f"Recomendados para {job_b}: {stats['para_puesto_b']}\n"
        f"Recomendados para ambos puestos: {stats['para_ambos']}\n"
        f"No recomendados: {stats['no_recomendados']}\n"
        f"Candidatos prioridad 🔥: {stats['prioridad_1']}\n"
        f"Candidatos prioridad 👍: {stats['prioridad_2']}\n"
        f"Score promedio del pool — {job_a}: {stats['score_promedio_a']}/100\n"
        f"Score promedio del pool — {job_b}: {stats['score_promedio_b']}/100"
    ))
    blocks.append(divider())

    # --- PUESTO A ---
    blocks.append(heading(f"🔧 Top Candidatos — {job_a}", 2))
    blocks.append(paragraph("Ordenados por score. 🔥 = contactar primero | 🟢 Excelente 🟡 Bueno 🟠 Posible"))

    if report["candidatos_a"]:
        for c in report["candidatos_a"]:
            blocks.append(paragraph(build_candidate_row(c, "puesto_a")))
    else:
        blocks.append(paragraph("No se encontraron candidatos recomendados para este puesto."))

    blocks.append(divider())

    # --- PUESTO B ---
    blocks.append(heading(f"📋 Top Candidatos — {job_b}", 2))
    blocks.append(paragraph("Ordenados por score. 🔥 = contactar primero | 🟢 Excelente 🟡 Bueno 🟠 Posible"))

    if report["candidatos_b"]:
        for c in report["candidatos_b"]:
            blocks.append(paragraph(build_candidate_row(c, "puesto_b")))
    else:
        blocks.append(paragraph("No se encontraron candidatos recomendados para este puesto."))

    blocks.append(divider())

    # --- AMBOS PUESTOS ---
    blocks.append(heading("⭐ Candidatos para Ambos Puestos", 2))

    if report["ambos"]:
        for c in report["ambos"]:
            score_a = c.get("puesto_a", {}).get("score", 0)
            score_b = c.get("puesto_b", {}).get("score", 0)
            nombre = c.get("nombre", c.get("archivo", "Sin nombre"))
            nota = c.get("nota_reclutador", "")
            emoji_p = get_prioridad_emoji(c.get("prioridad", 3))
            blocks.append(paragraph(
                f"{emoji_p} {nombre} | {job_a}: {score_a}/100 | {job_b}: {score_b}/100 | 💬 {nota}"
            ))
    else:
        blocks.append(paragraph("Ningún candidato califica para ambos puestos simultáneamente."))

    blocks.append(divider())

    # --- NO RECOMENDADOS ---
    blocks.append(heading("❌ No Recomendados", 2))
    blocks.append(paragraph("Candidatos que no cumplen los requisitos mínimos para ninguno de los dos puestos."))

    if report["ninguno"]:
        for c in report["ninguno"]:
            nombre = c.get("nombre", c.get("archivo", "Sin nombre"))
            nota = c.get("nota_reclutador", "")
            score_a = c.get("puesto_a", {}).get("score", 0)
            score_b = c.get("puesto_b", {}).get("score", 0)
            blocks.append(paragraph(
                f"🔴 {nombre} | Score A: {score_a}/100 | Score B: {score_b}/100 | {nota}"
            ))
    else:
        blocks.append(paragraph("Todos los candidatos tienen al menos un puesto recomendado."))

    blocks.append(divider())

    # --- NOTAS DEL ANALISTA ---
    blocks.append(heading("📝 Notas del Analista", 2))
    blocks.append(paragraph(
        f"Este reporte fue generado automáticamente por el BetterWay ATS Skill.\n"
        f"Evaluación realizada con IA (Claude Haiku) sobre {stats['total']} perfiles sintéticos.\n"
        f"Los scores reflejan el nivel de match técnico y funcional con cada descripción de puesto.\n"
        f"Se recomienda priorizar candidatos 🔥 con score superior a 70/100."
    ))

    # --- CREAR LA PÁGINA EN NOTION ---
    response = notion.pages.create(
        parent={"page_id": parent_id},
        properties={
            "title": {
                "title": [
                    {
                        "text": {
                            "content": f"📋 ATS Report — {job_a} & {job_b} — {fecha}"
                        }
                    }
                ]
            }
        },
        children=blocks
    )

    page_id = response["id"]
    page_url = response["url"]
    print(f"\n✅ Reporte publicado en Notion: {page_url}")
    return page_url
    