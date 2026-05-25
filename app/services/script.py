import anthropic
from app.config import settings

STYLE_NOTES = {
    "Finance": "authoritative, alarming hooks, specific numbers, urgency",
    "AI News": "futuristic, slightly ominous, thought-provoking, technical-but-accessible",
    "Sports Drama": "emotional, narrative-driven, rise-and-fall arc, personal stakes",
}


def generate_script(topic: str, category: str = "Finance", duration_seconds: int = 60) -> str:
    """Generate a voiceover script using Claude claude-haiku-4-5."""
    if not settings.anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in .env — needed for script generation.")

    style = STYLE_NOTES.get(category, "engaging, punchy, optimized for social media")
    word_target = int(duration_seconds * 2.2)  # ~130 words/min speaking pace

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": (
                f"Write a {duration_seconds}-second voiceover script for a faceless YouTube/TikTok video.\n\n"
                f"Topic: {topic}\n"
                f"Category: {category}\n"
                f"Style: {style}\n"
                f"Target word count: ~{word_target} words\n\n"
                "Rules:\n"
                "- Open with a hook that stops the scroll in the first 3 seconds\n"
                "- Use short punchy sentences. Vary the rhythm.\n"
                "- Build tension or curiosity throughout\n"
                "- End with a strong call-to-action (like, subscribe, comment)\n"
                "- No hashtags, no stage directions, no section labels — just the spoken words\n"
                "- Write it exactly as it should be read aloud"
            ),
        }],
    )

    return message.content[0].text.strip()
