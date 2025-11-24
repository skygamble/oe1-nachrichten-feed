import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

# Offizieller Ö1-Journale-RSS-Feed (alle Journale des Tages)
SRC_URL = "https://podcast.orf.at/podcast/oe1/oe1_journale/oe1_journale.xml"
DEST_PATH = Path("docs/feed.xml")


def main():
    # RSS vom ORF laden
    with urllib.request.urlopen(SRC_URL, timeout=20) as resp:
        data = resp.read()

    # XML parsen
    root = ET.fromstring(data)
    channel = root.find("channel")
    if channel is None:
        raise RuntimeError("Kein <channel> im RSS gefunden")

    items = channel.findall("item")
    if not items:
        raise RuntimeError("Keine <item>-Einträge im RSS gefunden")

    # Nur die neueste Episode behalten (erstes Item)
    for i, item in enumerate(items):
        if i > 0:
            channel.remove(item)

    # Zielordner anlegen
    DEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Feed schreiben
    tree = ET.ElementTree(root)
    tree.write(DEST_PATH, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
