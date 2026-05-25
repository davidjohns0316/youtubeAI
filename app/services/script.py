import anthropic
from app.config import settings

STYLE_NOTES = {
    "Finance": "authoritative, alarming hooks, specific numbers, urgency",
    "AI News": "futuristic, slightly ominous, thought-provoking, technical-but-accessible",
    "Sports Drama": "emotional, narrative-driven, rise-and-fall arc, personal stakes",
}


def generate_script(
    topic: str,
    category: str = "Finance",
    duration_seconds: int = 60,
    articles: list[dict] | None = None,
) -> str:
    """Generate a voiceover script using Claude Haiku, grounded in real news articles when available."""
    if not settings.anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in .env — needed for script generation.")

    style = STYLE_NOTES.get(category, "engaging, punchy, optimized for social media")
    word_target = int(duration_seconds * 2.2)  # ~130 words/min speaking pace

    # Build news context block
    news_context = ""
    if articles:
        news_context = "\n\nReal news articles to base your script on (use these facts — do NOT invent numbers or events):\n"
        for i, a in enumerate(articles[:3], 1):
            date_str = f" — {a['date'][:16]}" if a.get("date") else ""
            news_context += (
                f"\n[Source {i}] {a['source']}{date_str}\n"
                f"Headline: {a['title']}\n"
            )
            if a.get("summary"):
                news_context += f"Summary: {a['summary']}\n"
        news_context += (
            "\nCite the source(s) naturally in the script — e.g. 'According to [Source]...' "
            "or 'As [Source] reported...' — at least once."
        )

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        messages=[{
            "role": "user",
            "content": (
                f"Write a {duration_seconds}-second voiceover script for a faceless YouTube/TikTok video.\n\n"
                f"Topic: {topic}\n"
                f"Category: {category}\n"
                f"Style: {style}\n"
                f"Target word count: ~{word_target} words\n"
                f"{news_context}\n\n"
                "Rules:\n"
                "- Open with a hook that stops the scroll in the first 3 seconds\n"
                "- Use short punchy sentences. Vary the rhythm.\n"
                "- Include specific facts, numbers, and names from the sources above\n"
                "- Build tension or curiosity throughout\n"
                "- End with a strong call-to-action (like, subscribe, comment)\n"
                "- No hashtags, no stage directions, no section labels — just the spoken words\n"
                "- Write it exactly as it should be read aloud"
            ),
        }],
    )

    return message.content[0].text.strip()
