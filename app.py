"""
Gradio UI fuer Persona Marketing Agent
Demonstriert Google ADK Multi-Agent-Koordination.
"""

import gradio as gr
import asyncio
from dotenv import load_dotenv
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# Sub-Agenten direkt nutzen (zuverlaessig, immer beide Outputs)
from marketing_agent.agent import persona_agent, messaging_agent

load_dotenv()


# CSS Styling 


CSS = """
body {
    background: linear-gradient(135deg, #fafafa, #f8fafc);
}

.gradio-container {
    max-width: 1050px !important;
    margin: 0 auto;
}

.header h1 {
    font-weight: 600;
    font-size: 30px;
    color: #1f2937;
    margin-bottom: 6px;
}

.header p {
    color: #6b7280;
    font-size: 15px;
}

.card {
    padding: 10px 0;
    background: transparent;
    border: none;
    box-shadow: none;
}

textarea, input, select {
    border-radius: 12px !important;
    border: 1px solid #e5e7eb !important;
}

textarea {
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 14px !important;
}

button.primary {
    background-color: #fb923c !important;
    border: none !important;
    font-size: 15px !important;
    padding: 10px 16px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px rgba(251,146,60,0.25);
    transition: all 0.2s ease-in-out;
}

button.primary:hover {
    background-color: #f97316 !important;
    transform: translateY(-1px);
}
"""


# Runner Setup (zwei Runner, ein Session-Service)


session_service = InMemorySessionService()

persona_runner = Runner(
    agent=persona_agent,
    app_name="persona_marketing_agent",
    session_service=session_service,
)

messaging_runner = Runner(
    agent=messaging_agent,
    app_name="persona_marketing_agent",
    session_service=session_service,
)


# Helper: Agent ausfuehren und finalen Text holen


async def run_agent_once(runner: Runner, prompt: str) -> str:
    session = await session_service.create_session(
        user_id="user",
        app_name="persona_marketing_agent",
    )

    content = types.Content(role="user", parts=[types.Part(text=prompt)])

    events = runner.run_async(
        user_id="user",
        session_id=session.id,
        new_message=content
    )

    final_response = ""
    async for event in events:
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    return final_response.strip()


# Prompt Builder


def build_persona_prompt(product: str, audience: str, tone: str, extra: str, language: str) -> str:
    parts = [
        "Erstelle genau 3 unterschiedliche Marketing-Personas.",
        "",
        f"Produkt/Thema: {product}",
        f"Zielgruppe: {audience}",
        f"Ton: {tone}",
        f"Sprache: {language}",
    ]
    if extra.strip():
        parts.append(f"Zusatzinfos: {extra.strip()}")
    parts.append("")
    parts.append("Gib NUR die 3 Personas im vorgegebenen Persona-Format zurueck. Keine Erklaerungen.")
    return "\n".join(parts)


def build_messaging_prompt(
    product: str,
    audience: str,
    goal: str,
    tone: str,
    extra: str,
    language: str,
    personas_text: str
) -> str:
    parts = [
        "Erstelle Messaging fuer jede Persona (Value Proposition, CTA, Ad Copy, optional Keywords).",
        "",
        f"Produkt/Thema: {product}",
        f"Zielgruppe: {audience}",
        f"Marketingziel: {goal}",
        f"Ton: {tone}",
        f"Sprache: {language}",
    ]
    if extra.strip():
        parts.append(f"Zusatzinfos: {extra.strip()}")

    parts += [
        "",
        "Hier sind die Personas:",
        personas_text,
        "",
        "Gib NUR das Messaging im Messaging-Format zurueck (PERSONA 1/2/3 mit Value Proposition, CTA, Ad Copy, Keywords).",
        "Keine Erklaerungen, keine Meta-Kommentare."
    ]
    return "\n".join(parts)


def build_refinement_prompt(current_output: str, instruction: str) -> str:
    return (
        "Ueberarbeite den folgenden Text gemaess der Anweisung.\n"
        "Gib NUR den ueberarbeiteten Text zurueck.\n"
        "Keine Erklaerungen, keine Ueberschriften, kein Zusatztext.\n\n"
        "TEXT:\n"
        f"{current_output}\n\n"
        "ANWEISUNG:\n"
        f"{instruction}"
    )


# Gradio Handlers 


async def process_request_async(
    product: str,
    audience: str,
    goal: str,
    tone: str,
    extra: str,
    language: str
) -> str:
    if not product.strip():
        return "Fehler: Bitte ein Produkt oder Thema eingeben."
    if not audience.strip():
        return "Fehler: Bitte eine Zielgruppe eingeben."

    # 1) Personas erzeugen
    persona_prompt = build_persona_prompt(product, audience, tone, extra, language)
    personas = await run_agent_once(persona_runner, persona_prompt)

    if not personas:
        return "Fehler: Keine Personas generiert."

    # 2) Messaging basierend auf Personas erzeugen
    messaging_prompt = build_messaging_prompt(product, audience, goal, tone, extra, language, personas)
    messaging = await run_agent_once(messaging_runner, messaging_prompt)

    if not messaging:
        return "Fehler: Kein Messaging generiert."

    # 3) Kombinierte Ausgabe
    return f"---\nPERSONAS\n{personas}\n\nMESSAGING\n{messaging}\n---"


async def refine_async(current_output: str, instruction: str) -> str:
    if not current_output.strip():
        return "Fehler: Bitte zuerst generieren."
    if not instruction.strip():
        return "Fehler: Bitte eine Verfeinerungs-Anweisung eingeben."

    # Refinement laeuft ueber den Messaging-Agent 
    prompt = build_refinement_prompt(current_output, instruction)
    refined = await run_agent_once(messaging_runner, prompt)

    return refined if refined else "Fehler: Keine ueberarbeitete Version generiert."


# Gradio UI


with gr.Blocks(
    title="Persona Marketing Agent",
    css=CSS,
    theme=gr.themes.Soft(primary_hue="orange")
) as demo:

    gr.HTML("""
    <div class="header">
        <h1>Persona Marketing Agent</h1>
        <p>
            Multi-Agent-System mit Google ADK zur Erstellung von Marketing-Personas und Messaging.
        </p>
    </div>
    """)

    with gr.Row():
        with gr.Column(elem_classes=["card"]):
            product = gr.Textbox(label="Produkt / Thema", lines=2)
            audience = gr.Textbox(label="Zielgruppe", lines=2)

            goal = gr.Dropdown(
                label="Marketingziel",
                choices=[
                    "Leads generieren",
                    "Kaufabschluesse steigern",
                    "Newsletter-Anmeldungen",
                    "App-Downloads",
                    "Event-Anmeldungen"
                ],
                value="Leads generieren",
                allow_custom_value=False,
            )

            tone = gr.Dropdown(
                label="Ton",
                choices=[
                    "Professionell",
                    "Locker",
                    "Motivierend",
                    "Humorvoll",
                    "Begeistert",
                    "Informativ",
                    "Serioes",
                    "Emotional"
                ],
                value="Informativ",
                allow_custom_value=False,
            )

            language = gr.Dropdown(
                label="Sprache",
                choices=["Deutsch", "Englisch"],
                value="Deutsch",
                allow_custom_value=False,
            )

            extra = gr.Textbox(label="Zusatzinformationen (optional)", lines=3)

            generate_btn = gr.Button("Generieren", variant="primary")

        with gr.Column(elem_classes=["card"]):
            output = gr.Textbox(label="Ergebnis", lines=28)

            gr.Markdown("### Ergebnis verfeinern")

            refinement_input = gr.Textbox(
                label="Verfeinerungs-Anweisung",
                placeholder="z.B. CTA direkter, Ad Copy kuerzer, Persona 2 preisfokussierter.",
                lines=3
            )

            refine_btn = gr.Button("Verfeinern", variant="secondary")

    generate_btn.click(
        fn=process_request_async,
        inputs=[product, audience, goal, tone, extra, language],
        outputs=output
    )

    refine_btn.click(
        fn=refine_async,
        inputs=[output, refinement_input],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()