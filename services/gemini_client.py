def map_interest_to_tags(user_input):
    if not user_input.strip():
        return []
    
    prompt = INTEREST_MAPPING_PROMPT.format(user_input=user_input)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are an assistant that maps user interests to relevant tags. Output only a clean, comma-separated list of tags "
                "matching the user's text. Do not include any extra text, closing periods, or quotes. If no relevant tags are found, return an empty string."
            ),
            temperature=0.1
        )
    )

    raw_text = response.text or ""

    tags = []
    for tag in raw_text.split(","):
        if tag.strip():
            tags.append(tag.strip().lower())

    return tags
def rank_destinations(user_inputs, options_data):
    options_lines=[]
    for data in options_data:
        if "error" in data or not data:
            continue
        line = (
            f"- {data.get('city')}: "
            f"High: {data.get('avg_high')}°F, "
            f"Low: {data.get('avg_low')}°F, "
            f"Daily Rain: {data.get('avg_daily_rain_mm')}mm"
        )
        options_lines.append(line)
    formatted_options = "\n".join(options_lines)

    if not formatted_options:
        return "No valid options to be ranked."

    prompt = RANKING_PROMPT.format(
        budget=user_inputs.get("budget", "N/A"),
        climate=user_inputs.get("climate", "N/A"),
        interests=user_inputs.get("interests", "Any"),
        options_data=formatted_options
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7
        )
    )
    return response.text or "System failed to generate a ranking."