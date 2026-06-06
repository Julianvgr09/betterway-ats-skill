from datetime import datetime

def build_report(evaluations: list, job_a_name: str, job_b_name: str) -> dict:
    """
    Toma la lista de evaluaciones y construye la estructura del reporte.
    """

    # Separar candidatos por recomendación
    solo_a = [e for e in evaluations if e.get("recomendacion") == "SOLO_A"]
    solo_b = [e for e in evaluations if e.get("recomendacion") == "SOLO_B"]
    ambos = [e for e in evaluations if e.get("recomendacion") == "AMBOS"]
    ninguno = [e for e in evaluations if e.get("recomendacion") == "NINGUNO"]

    # Candidatos para Puesto A (SOLO_A + AMBOS), ordenados por score
    candidatos_a = sorted(
        [e for e in evaluations if e.get("recomendacion") in ["SOLO_A", "AMBOS"]],
        key=lambda x: x.get("puesto_a", {}).get("score", 0),
        reverse=True
    )

    # Candidatos para Puesto B (SOLO_B + AMBOS), ordenados por score
    candidatos_b = sorted(
        [e for e in evaluations if e.get("recomendacion") in ["SOLO_B", "AMBOS"]],
        key=lambda x: x.get("puesto_b", {}).get("score", 0),
        reverse=True
    )

    # Estadísticas generales
    stats = {
        "total": len(evaluations),
        "para_puesto_a": len(solo_a) + len(ambos),
        "para_puesto_b": len(solo_b) + len(ambos),
        "para_ambos": len(ambos),
        "no_recomendados": len(ninguno),
        "prioridad_1": len([e for e in evaluations if e.get("prioridad") == 1]),
        "prioridad_2": len([e for e in evaluations if e.get("prioridad") == 2]),
    }

    # Score promedio del pool
    scores_a = [e.get("puesto_a", {}).get("score", 0) for e in evaluations]
    scores_b = [e.get("puesto_b", {}).get("score", 0) for e in evaluations]
    stats["score_promedio_a"] = round(sum(scores_a) / len(scores_a), 1) if scores_a else 0
    stats["score_promedio_b"] = round(sum(scores_b) / len(scores_b), 1) if scores_b else 0

    return {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "job_a_name": job_a_name,
        "job_b_name": job_b_name,
        "stats": stats,
        "candidatos_a": candidatos_a,
        "candidatos_b": candidatos_b,
        "ambos": ambos,
        "ninguno": ninguno,
        "todos": evaluations
    }


def get_nivel_emoji(nivel: str) -> str:
    """Retorna emoji según el nivel de fit."""
    return {
        "EXCELENTE": "🟢",
        "BUENO": "🟡",
        "POSIBLE": "🟠",
        "NO_FIT": "🔴"
    }.get(nivel, "⚪")


def get_prioridad_emoji(prioridad: int) -> str:
    """Retorna emoji según la prioridad."""
    return {
        1: "🔥",
        2: "👍",
        3: "👀"
    }.get(prioridad, "⚪")