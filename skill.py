import os
import sys
from dotenv import load_dotenv

# Agregar modules al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))

from pdf_reader import read_pdfs_from_folder
from evaluator import evaluate_all_candidates
from report_builder import build_report
from notion_publisher import publish_report

load_dotenv()

def main():
    print("=" * 50)
    print("  BetterWay ATS Skill")
    print("=" * 50)

    # --- RUTAS DE INPUT ---
    candidates_folder = os.path.join("inputs", "candidates")
    jobs_folder = os.path.join("inputs", "jobs")

    # --- LEER DESCRIPCIONES DE PUESTO ---
    print("\n📄 Leyendo descripciones de puesto...")
    jobs = read_pdfs_from_folder(jobs_folder)

    if len(jobs) < 2:
        print("❌ Se necesitan exactamente 2 descripciones de puesto en inputs/jobs/")
        sys.exit(1)

    job_files = sorted(jobs.keys())
    job_a_name = "Integration Developer — Oracle EBS"
    job_b_name = "Business Systems Analyst — Oracle EBS"
    job_a_text = jobs[job_files[0]]
    job_b_text = jobs[job_files[1]]

    print(f"  ✓ Puesto A: {job_a_name}")
    print(f"  ✓ Puesto B: {job_b_name}")

    # --- LEER CANDIDATOS ---
    print("\n👥 Leyendo perfiles de candidatos...")
    candidates = read_pdfs_from_folder(candidates_folder)
    print(f"  ✓ Total candidatos encontrados: {len(candidates)}")

    # --- EVALUAR CANDIDATOS ---
    print("\n🤖 Evaluando candidatos con IA...")
    evaluations = evaluate_all_candidates(candidates, job_a_text, job_b_text)
    print(f"  ✓ Evaluaciones completadas: {len(evaluations)}")

    # --- CONSTRUIR REPORTE ---
    print("\n📊 Construyendo reporte...")
    report = build_report(evaluations, job_a_name, job_b_name)
    print(f"  ✓ Reporte construido")
    print(f"  → Para Puesto A: {report['stats']['para_puesto_a']} candidatos")
    print(f"  → Para Puesto B: {report['stats']['para_puesto_b']} candidatos")
    print(f"  → Para ambos:    {report['stats']['para_ambos']} candidatos")
    print(f"  → No recomendados: {report['stats']['no_recomendados']} candidatos")

    # --- PUBLICAR EN NOTION ---
    print("\n🚀 Publicando reporte en Notion...")
    page_url = publish_report(report)

    print("\n" + "=" * 50)
    print("  ✅ Skill completado exitosamente")
    print(f"  🔗 {page_url}")
    print("=" * 50)

if __name__ == "__main__":
    main()