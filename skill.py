import os
import sys
from dotenv import load_dotenv

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

    candidates_folder = os.path.join("inputs", "candidates")
    jobs_folder = os.path.join("inputs", "jobs")

    print("\n📄 Leyendo descripciones de puesto...")
    jobs = read_pdfs_from_folder(jobs_folder)

    if len(jobs) < 2:
        print("❌ Se necesitan exactamente 2 descripciones de puesto en inputs/jobs/")
        sys.exit(1)

    job_files = sorted(jobs.keys())
    job_a_name = job_files[0].replace(".pdf", "").replace("-", " ").title()
    job_b_name = job_files[1].replace(".pdf", "").replace("-", " ").title()
    job_a_text = jobs[job_files[0]]
    job_b_text = jobs[job_files[1]]

    print("  ✓ Puesto A: " + job_a_name)
    print("  ✓ Puesto B: " + job_b_name)

    print("\n👥 Leyendo perfiles de candidatos...")
    candidates = read_pdfs_from_folder(candidates_folder)
    print("  ✓ Total candidatos encontrados: " + str(len(candidates)))

    print("\n🤖 Evaluando candidatos con IA...")
    evaluations = evaluate_all_candidates(candidates, job_a_text, job_b_text, job_a_name, job_b_name)
    print("  ✓ Evaluaciones completadas: " + str(len(evaluations)))

    print("\n📊 Construyendo reporte...")
    report = build_report(evaluations, job_a_name, job_b_name)
    print("  ✓ Reporte construido")
    print("  → Para Puesto A: " + str(report["stats"]["para_puesto_a"]) + " candidatos")
    print("  → Para Puesto B: " + str(report["stats"]["para_puesto_b"]) + " candidatos")
    print("  → Para ambos:    " + str(report["stats"]["para_ambos"]) + " candidatos")
    print("  → No recomendados: " + str(report["stats"]["no_recomendados"]) + " candidatos")

    print("\n🚀 Publicando reporte en Notion...")
    page_url = publish_report(report)

    print("\n" + "=" * 50)
    print("  ✅ Skill completado exitosamente")
    print("  🔗 " + page_url)
    print("=" * 50)

if __name__ == "__main__":
    main()