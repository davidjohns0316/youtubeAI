import anthropic
from app.config import settings

STYLE_NOTES = {
    "Finance": "authoritative, alarming hooks, specific numbers, urgency",
    "AI News": "futuristic, slightly ominous, thought-provoking, technical-but-accessible",
    "Sports Drama": "emotional, narrative-driven, rise-and-fall arc, personal stakes",
}

VISUAL_STYLE_NOTES = {
    "Finance": "dramatic financial imagery — trading floors, skyscrapers, cash, stock charts, corporate boardrooms",
    "AI News": "futuristic tech — glowing neural networks, robot hands, data centers, holographic interfaces, cityscapes at night",
    "Sports Drama": "cinematic sports scenes — stadiums, athletes, trophies, crowds, dramatic lighting",
}


def generate_script(
    topic: str,
    category: str = "Finance",
    duration_seconds: int = 60,
    articles: list[dict] | None = None,
) -> dict:
    """
    Generate a voiceover script AND a matching Runway video prompt using Claude Haiku.
    Returns {"script": str, "video_prompt": str}
    """
    if not settings.anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in .env — needed for script generation.")

    style = STYLE_NOTES.get(category, "engaging, punchy, optimized for social media")
    visual_style = VISUAL_STYLE_NOTES.get(category, "cinematic, dramatic, high production value")
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
        max_tokens=900,
        messages=[{
            "role": "user",
            "content": (
                f"You are creating content for a faceless YouTube/TikTok video about: {topic}\n"
                f"Category: {category} | Style: {style}\n"
                f"{news_context}\n\n"
                f"Return EXACTLY this format with both sections:\n\n"
                f"SCRIPT:\n"
                f"[Write a {duration_seconds}-second voiceover (~{word_target} words). "
                f"Open with a scroll-stopping hook. Short punchy sentences. "
                f"Include specific facts/numbers from the sources. "
                f"Cite sources naturally (e.g. 'According to Reuters...'). "
                f"Build tension. End with a call-to-action. "
                f"No hashtags, no stage directions — spoken words only.]\n\n"
                f"VIDEO_PROMPT:\n"
                f"[Write a single Runway ML video prompt (2-4 sentences) that visually represents "
                f"the KEY STORY from the script above. "
                f"Be specific to the actual topic — reference the real subject matter. "
                f"Visual style: {visual_style}. "
                f"Cinematic, photorealistic, dramatic lighting, 16:9 landscape. "
                f"No text overlays, no people talking directly to camera.]"
            ),
        }],
    )

    raw = message.content[0].text.strip()

    # Parse the two sections
    script = ""
    video_prompt = ""

    if "VIDEO_PROMPT:" in raw:
        parts = raw.split("VIDEO_PROMPT:", 1)
        video_prompt = parts[1].strip()
        script_part = parts[0]
    else:
        script_part = raw

    if "SCRIPT:" in script_part:
        script = script_part.split("SCRIPT:", 1)[1].strip()
    else:
        script = script_part.strip()

    return {"script": script, "video_prompt": video_prompt}
