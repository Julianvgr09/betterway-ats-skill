import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

def evaluate_candidate(candidate_name: str, candidate_text: str, job_a: str, job_b: str) -> dict:
    """
    Evalúa un candidato contra dos descripciones de puesto usando Claude.
    Retorna un diccionario con scores, razones y recomendación.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""Eres un experto en reclutamiento técnico especializado en Oracle EBS y tecnología empresarial.

Analiza este perfil de candidato y evalúalo contra dos descripciones de puesto.

=== PERFIL DEL CANDIDATO ===
{candidate_text}

=== PUESTO A: Integration Developer — Oracle EBS ===
{job_a}

=== PUESTO B: Business Systems Analyst — Oracle EBS ===
{job_b}

Responde ÚNICAMENTE con un objeto JSON válido, sin texto adicional, sin markdown, sin explicaciones fuera del JSON:

{{
  "nombre": "nombre completo del candidato",
  "puesto_a": {{
    "score": 0,
    "nivel": "NO_FIT | POSIBLE | BUENO | EXCELENTE",
    "razones_positivas": ["razón 1", "razón 2"],
    "alertas": ["alerta 1"],
    "resumen": "una línea"
  }},
  "puesto_b": {{
    "score": 0,
    "nivel": "NO_FIT | POSIBLE | BUENO | EXCELENTE",
    "razones_positivas": ["razón 1", "razón 2"],
    "alertas": ["alerta 1"],
    "resumen": "una línea"
  }},
  "recomendacion": "SOLO_A | SOLO_B | AMBOS | NINGUNO",
  "prioridad": 0,
  "nota_reclutador": "observación clave en una línea"
}}

Reglas para los scores:
- score: número entero del 0 al 100
- prioridad: número entero del 1 al 3 (1=contactar primero, 2=contactar después, 3=no prioritario)
- Si el candidato tiene experiencia técnica relevante aunque no sea exactamente Oracle EBS, puede tener score hasta 60
- Evalúa potencial y transferibilidad de skills, no solo match exacto
- Sé estricto: un score 80+ significa que cumple casi todos los requisitos del puesto"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # Si Claude no retorna JSON limpio, intentar extraerlo
        start = raw.find("{")
        end = raw.rfind("}") + 1
        result = json.loads(raw[start:end])

    result["archivo"] = candidate_name
    return result


def evaluate_all_candidates(candidates: dict, job_a: str, job_b: str) -> list:
    """
    Evalúa todos los candidatos y retorna lista ordenada por prioridad y score.
    """
    results = []
    total = len(candidates)

    for i, (filename, text) in enumerate(candidates.items(), 1):
        print(f"  Evaluando {i}/{total}: {filename}")
        try:
            result = evaluate_candidate(filename, text, job_a, job_b)
            results.append(result)
        except Exception as e:
            print(f"  ✗ Error evaluando {filename}: {e}")

    # Ordenar por prioridad (1 primero) y luego por score más alto
    results.sort(key=lambda x: (x.get("prioridad", 99), -max(
        x.get("puesto_a", {}).get("score", 0),
        x.get("puesto_b", {}).get("score", 0)
    )))

    return results