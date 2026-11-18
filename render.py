from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
PAPER = "#F5F0E5"
INK = "#171A1C"
RED = "#A12A2A"
MUTED = "#656761"
BLUE = "#B7D5D8"
DEEP_BLUE = "#376C78"
WHITE = "#FFFDF7"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

image = Image.new("RGB", (SIZE, SIZE), PAPER)
draw = ImageDraw.Draw(image)


def font(size: int, bold: bool = False, serif: bool = False) -> ImageFont.FreeTypeFont:
    path = SERIF_BOLD if serif else (SANS_BOLD if bold else SANS)
    return ImageFont.truetype(path, size)


def text(x: int, y: int, value: str, size: int, fill: str = INK,
         bold: bool = False, serif: bool = False) -> None:
    draw.text((x, y), value, font=font(size, bold, serif), fill=fill)


def wrap(value: str, face: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in value.split():
        candidate = f"{current} {word}".strip()
        if current and draw.textlength(candidate, font=face) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def paragraph(x: int, y: int, value: str, width: int, size: int = 19,
              fill: str = INK, bold: bool = False, leading: int = 6) -> int:
    face = font(size, bold)
    lines = wrap(value, face, width)
    line_height = size + leading
    for index, line in enumerate(lines):
        draw.text((x, y + index * line_height), line, font=face, fill=fill)
    return y + len(lines) * line_height


def panel(bounds: tuple[int, int, int, int], fill: str = WHITE) -> None:
    draw.rounded_rectangle(bounds, radius=8, fill=fill, outline="#C9C2B5", width=2)


def drone(cx: int, cy: int, scale: int = 1) -> None:
    color = RED
    draw.line((cx - 15 * scale, cy, cx + 15 * scale, cy), fill=color, width=2 * scale)
    draw.line((cx, cy - 9 * scale, cx, cy + 6 * scale), fill=color, width=2 * scale)
    draw.ellipse((cx - 4 * scale, cy - 3 * scale, cx + 4 * scale, cy + 4 * scale), fill=color)
    for dx in (-15, 15):
        draw.ellipse((cx + dx * scale - 5 * scale, cy - 3 * scale,
                      cx + dx * scale + 5 * scale, cy + 3 * scale), outline=color, width=2)
    draw.line((cx - 3 * scale, cy + 4 * scale, cx - 7 * scale, cy + 9 * scale),
              fill=color, width=2)
    draw.line((cx + 3 * scale, cy + 4 * scale, cx + 7 * scale, cy + 9 * scale),
              fill=color, width=2)


def bridge_art() -> None:
    draw.rounded_rectangle((54, 305, 592, 492), radius=9, fill="#E5ECE7")
    text(70, 318, "BLACK SEA", 14, DEEP_BLUE, bold=True)
    text(492, 318, "CRIMEA", 14, DEEP_BLUE, bold=True)

    draw.rectangle((55, 418, 591, 492), fill=BLUE)
    for x, y, width in ((72, 437, 67), (171, 458, 79), (290, 440, 61),
                        (383, 465, 92), (493, 440, 60)):
        draw.arc((x, y, x + width, y + 18), start=190, end=350, fill=DEEP_BLUE, width=3)
    draw.line((55, 418, 591, 418), fill="#759DA0", width=2)

    deck = "#30383A"
    draw.polygon(((77, 389), (267, 389), (286, 402), (272, 415), (77, 415)), fill=deck)
    draw.polygon(((359, 409), (375, 397), (552, 397), (552, 423), (370, 423)), fill=deck)
    draw.line((82, 389, 266, 389), fill="#F2EDE1", width=3)
    draw.line((376, 397, 548, 397), fill="#F2EDE1", width=3)

    for px, top in ((183, 344), (452, 344)):
        draw.rectangle((px - 8, top, px + 8, 391), fill=INK)
        draw.rectangle((px - 19, 389, px + 19, 397), fill=INK)
        for anchor in range(px - 76, px + 79, 19):
            if anchor < px:
                target = max(83, anchor - 2)
            else:
                target = min(548, anchor + 2)
            draw.line((px, top + 8, target, 388 if px == 183 else 396),
                      fill="#50595A", width=2)

    draw.line((280, 394, 294, 402), fill=RED, width=4)
    draw.line((355, 410, 366, 403), fill=RED, width=4)
    drone(310, 346)
    drone(388, 332, 1)


def news_panel(bounds: tuple[int, int, int, int], label: str,
               heading: str, summary: str) -> None:
    panel(bounds)
    x, y, right, bottom = bounds
    text(x + 16, y + 12, label, 14, RED, bold=True)
    head_y = y + 34
    head_end = paragraph(x + 16, head_y, heading, right - x - 32, 18, INK, True, 2)
    paragraph(x + 16, head_end + 5, summary, right - x - 32, 18, INK, False, 4)


text(42, 27, "THE WORLD  /  WEDNESDAY EDITION", 17, RED, bold=True)
text(38, 48, "WORLD NEWS", 70, INK, bold=True, serif=True)
text(44, 132, "WEDNESDAY 18 NOVEMBER 2026", 23, INK, bold=True)
draw.line((42, 173, 982, 173), fill=INK, width=3)

text(44, 191, "LEAD  •  UKRAINE–CRIMEA", 17, RED, bold=True)
text(42, 214, "KERCH BRIDGE HIT — AGAIN", 32, INK, bold=True, serif=True)
text(44, 261, "2nd day  •  Russia calls it the war's biggest drone attack", 17, MUTED, bold=True)
bridge_art()

lead_y = 500
lead_y = paragraph(
    48, lead_y,
    "Russia said 1,441 drones crossed 22 regions overnight, its biggest drone attack of the war.",
    535, 17, INK, True, 4
) + 4
lead_y = paragraph(
    48, lead_y,
    "A road arch and span collapsed into the Kerch Strait; road traffic was suspended.",
    535, 17, INK, False, 4
) + 4
lead_y = paragraph(
    48, lead_y,
    "Crimea's Russian-installed governor Aksyonov said two died.",
    535, 17, INK, False, 4
) + 4
lead_y = paragraph(
    48, lead_y,
    "Zelenskyy called it “unprecedented”; he said it was phase seven, with Flamingo delivering the final blow.",
    535, 17, RED, True, 4
) + 4
paragraph(
    48, lead_y,
    "The Kremlin linked the timing to the planned Trump–Xi–Putin meeting in Shenzhen.",
    535, 17, INK, False, 4
)

news_panel((620, 191, 982, 360), "GULF  •  IRAN–U.S.",
           "DRONES OVER BAHRAIN",
           "Iranian drones at a U.S. radar site were intercepted; the U.S. struck an IRGC missile site on Qeshm. Kuwait also reported interceptions.")
news_panel((620, 374, 982, 537), "ASIA  •  MANILA",
           "TRUMP AT ASEAN",
           "Trump met ASEAN leaders and held Quad talks. A Trump–Xi–Putin meeting is due in Shenzhen on the APEC sidelines.")
news_panel((620, 551, 982, 720), "BUSINESS  •  NVIDIA",
           "REVENUE DOUBLES",
           "$115.84bn quarterly revenue, twice a year ago. The board says it will not reinstate Jensen Huang.")

cards = (
    (42, 744, 345, 889, "TECH  •  OUTAGE & CYBER",
     "Apple services outage. Reported supply-chain attack exposed CNN, BBC and Zoom visitors to malware; 178 firms hit."),
    (356, 744, 668, 889, "TRADE  •  CANADA–CHINA",
     "Japan offered ASEAN access to crude reserves. Canada and China extended trade deals as Xi met Mark Carney ahead of APEC."),
    (679, 744, 982, 889, "SPORT  •  DHONI RETIRES",
     "MS Dhoni ended his IPL playing career and will mentor Chennai Super Kings.")
)
for x1, y1, x2, y2, heading, summary in cards:
    panel((x1, y1, x2, y2))
    text(x1 + 13, y1 + 13, heading, 15, RED, bold=True)
    paragraph(x1 + 13, y1 + 43, summary, x2 - x1 - 26, 17, INK, False, 4)

draw.rectangle((42, 903, 982, 974), fill=INK)
text(58, 912, "MORE  •  TRUMP–BBC SUIT: DEPOSITION DEADLINE EXTENDED TO 22 JAN", 15, WHITE, bold=True)
text(58, 937, "DEUTSCHE BANK  •  leaked-file report says warnings ignored   |   CYCLONE AKVAN  •  expected to strengthen", 14, WHITE)
text(44, 983, "18 NOV 2026", 14, INK, bold=True)
text(345, 983, "SOURCES: BBC  •  REUTERS  •  AP  •  AL JAZEERA", 13, MUTED, bold=True)
text(896, 983, "WORLD BRIEF", 14, RED, bold=True)

image.save(Path(__file__).with_name("entry.png"), format="PNG", optimize=True)
