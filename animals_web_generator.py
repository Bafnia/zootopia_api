import html
from pathlib import Path
import data_fetcher

TEMPLATES_DIR = Path("templates")
OUTPUT_HTML = Path("animals.html")


def render_cards(animals: list, query: str) -> str:
    card_tpl = (TEMPLATES_DIR / "animal_card.html").read_text(encoding="utf-8")

    if not animals:
        return f'<h2>The animal "{query}" doesn\'t exist.</h2>'

    parts = []
    for a in animals:
        name = html.escape(a.get("name") or "Unknown")
        tax = a.get("taxonomy") or {}
        klass = html.escape(tax.get("class") or "-")
        family = html.escape(tax.get("family") or "-")
        locations = a.get("locations") or []
        loc_str = html.escape(", ".join(locations[:5]) or "-")
        diet = html.escape((a.get("characteristics") or {}).get("diet") or "-")

        parts.append(
            card_tpl.replace("{{NAME}}", name)
                    .replace("{{CLASS}}", klass)
                    .replace("{{FAMILY}}", family)
                    .replace("{{LOCATIONS}}", loc_str)
                    .replace("{{DIET}}", diet)
        )
    return "\n".join(parts)


def build_page(title: str, content_html: str) -> str:
    base_tpl = (TEMPLATES_DIR / "base.html").read_text(encoding="utf-8")
    return base_tpl.replace("{{TITLE}}", html.escape(title)).replace("{{CONTENT}}", content_html)


def main():
    query = input("Enter a name of an animal: ").strip()
    if not query:
        print("Bitte ein Tier eingeben (z. B. Fox).")
        return

    animals = data_fetcher.fetch_data(query)

    cards_html = render_cards(animals, query)
    page_html = build_page(f"Animals – Results for “{query}”", cards_html)

    OUTPUT_HTML.write_text(page_html, encoding="utf-8")
    print(f"Website was successfully generated → {OUTPUT_HTML.name}")


if __name__ == "__main__":
    main()
