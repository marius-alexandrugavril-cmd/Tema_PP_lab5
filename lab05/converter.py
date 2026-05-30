def text_to_html(text: str) -> str:
    """
    Convertește un text simplu în format HTML.
    Prima linie este considerată titlu (<h1>), iar restul paragrafelor (<p>).
    """
    lines = text.strip().split('\n')
    if not lines:
        return ""

    
    title = lines[0].strip()

    html_parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        f"    <title>{title}</title>",
        "</head>",
        "<body>",
        f"    <h1>{title}</h1>"
    ]


    for line in lines[1:]:
        clean_line = line.strip()
        if clean_line:
            html_parts.append(f"    <p>{clean_line}</p>")

    html_parts.append("</body>")
    html_parts.append("</html>")

    return "\n".join(html_parts)