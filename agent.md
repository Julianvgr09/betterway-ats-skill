# BetterWay ATS Skill — Agent Instructions

## ¿Qué hace este skill?
Evalúa N perfiles de candidatos contra M descripciones de puesto usando IA,
y publica un reporte priorizado en Notion indicando a quién contactar primero.

## Requisitos
- Python 3.10+
- Node.js 18+
- Cuenta de Anthropic con créditos (mínimo $5 USD)
- Cuenta de Notion (gratuita)

## Instalación

### 1 — Clonar el repositorio
```bash
git clone https://github.com/Julianvgr09/betterway-ats-skill.git
cd betterway-ats-skill
```

### 2 — Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3 — Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4 — Configurar Notion MCP
1. Ve a https://www.notion.so/profile/integrations
2. Click "New integration" → nombre: `betterway-ats-skill`
3. Método de autenticación: Token de acceso
4. Copia el token (empieza con `ntn_...`)
5. Crea una página en Notion llamada `ATS Reports`
6. Dentro de esa página click `...` → "Connect to" → selecciona `betterway-ats-skill`
7. Copia el Page ID del URL (últimos 32 caracteres antes del `?`)

### 5 — Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto:

ANTHROPIC_API_KEY=sk-ant-tu-api-key
NOTION_TOKEN=ntn_tu-token-de-notion
NOTION_PARENT_PAGE_ID=tu-page-id-de-32-caracteres

## Preparar inputs

Coloca los archivos en estas carpetas:

inputs/
├── candidates/    ← PDFs de candidatos 
└── jobs/          ← PDFs de descripciones de puesto

## Ejecutar el skill
```bash
python skill.py
```

## Output
Al finalizar verás en la terminal:

✅ Skill completado exitosamente
🔗 https://notion.so/...

El reporte en Notion incluye:
- Resumen ejecutivo con estadísticas del pool
- Top candidatos por puesto ordenados por score
- Candidatos aptos para ambos puestos
- Candidatos no recomendados con razones
- Notas del analista

## Estructura del proyecto
betterway-ats-skill/
├── skill.py                  ← Punto de entrada principal
├── agent.md                  ← Este archivo
├── requirements.txt          ← Dependencias
├── modules/
│   ├── pdf_reader.py         ← Lee PDFs
│   ├── evaluator.py          ← Evalúa con IA
│   ├── report_builder.py     ← Construye reporte
│   └── notion_publisher.py   ← Publica en Notion
└── inputs/
├── candidates/           ← PDFs de candidatos
└── jobs/                 ← PDFs de descripciones

## Notas importantes
- El skill es completamente reutilizable con cualquier vacante
- Los PDFs de inputs NO se suben al repositorio
- Nunca subas el archivo `.env` al repositorio
- El costo estimado por ejecución completa (30 candidatos) es ~$0.16 USD en Claude