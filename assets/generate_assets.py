import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = Path(__file__).resolve().parent / "images"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def create_case_image(filename: str, title: str, subtitle_before: str, subtitle_after: str, left_color: tuple, right_color: tuple):
    width, height = 1000, 600
    img = Image.new("RGB", (width, height), color=(18, 18, 20))
    draw = ImageDraw.Draw(img)

    # Левая половина (ДО)
    for x in range(0, width // 2):
        # Градиент / фактура
        ratio = x / (width // 2)
        r = int(left_color[0] * (0.8 + 0.2 * ratio))
        g = int(left_color[1] * (0.8 + 0.2 * ratio))
        b = int(left_color[2] * (0.8 + 0.2 * ratio))
        draw.line([(x, 80), (x, height - 80)], fill=(r, g, b))

    # Рисуем имитацию дефектов слева (паутинка/потертости)
    for i in range(15):
        cx = 80 + (i * 25) % (width // 2 - 160)
        cy = 150 + (i * 27) % (height - 300)
        draw.arc([cx - 40, cy - 40, cx + 40, cy + 40], start=0, end=270, fill=(160, 160, 160), width=1)
        draw.line([cx - 30, cy - 20, cx + 50, cy + 30], fill=(140, 140, 140), width=1)

    # Правая половина (ПОСЛЕ)
    for x in range(width // 2, width):
        ratio = (x - width // 2) / (width // 2)
        r = int(right_color[0] * (0.9 + 0.3 * (1 - ratio)))
        g = int(right_color[1] * (0.9 + 0.3 * (1 - ratio)))
        b = int(right_color[2] * (0.9 + 0.3 * (1 - ratio)))
        draw.line([(x, 80), (x, height - 80)], fill=(r, g, b))

    # Рисуем глянец / блики справа
    draw.polygon([(width // 2 + 50, 80), (width // 2 + 180, 80), (width // 2 + 100, height - 80), (width // 2 - 30, height - 80)], fill=(right_color[0] + 30, right_color[1] + 30, right_color[2] + 30))
    draw.polygon([(width // 2 + 130, 80), (width // 2 + 160, 80), (width // 2 + 80, height - 80), (width // 2 + 50, height - 80)], fill=(255, 255, 255))

    # Разделительная линия
    draw.line([(width // 2, 70), (width // 2, height - 70)], fill=(255, 215, 0), width=4)

    # Верхний заголовок
    draw.rectangle([(0, 0), (width, 80)], fill=(24, 25, 28))
    draw.text((30, 26), f"APEX DETAIL | {title.upper()}", fill=(240, 240, 240))

    # Бейджи ДО и ПОСЛЕ
    # ДО
    draw.rectangle([(40, 100), (140, 140)], fill=(200, 40, 40))
    draw.text((65, 112), "ДО", fill=(255, 255, 255))
    draw.text((45, 150), subtitle_before, fill=(210, 210, 210))

    # ПОСЛЕ
    draw.rectangle([(width // 2 + 40, 100), (width // 2 + 170, 140)], fill=(40, 170, 70))
    draw.text((width // 2 + 65, 112), "ПОСЛЕ", fill=(255, 255, 255))
    draw.text((width // 2 + 45, 150), subtitle_after, fill=(255, 255, 255))

    # Нижняя плашка
    draw.rectangle([(0, height - 80), (width, height)], fill=(24, 25, 28))
    draw.text((30, height - 52), "Гарантия на все виды работ • Премиальная автохимия", fill=(170, 170, 170))
    draw.text((width - 280, height - 52), "Apex Detail • Москва", fill=(255, 215, 0))

    img.save(ASSETS_DIR / filename, quality=92)
    print(f"Generated: {filename}")


def main():
    create_case_image(
        "case_polishing.jpg",
        "Глубокая восстановительная полировка",
        "Паутинка, голограммы, матовость",
        "Идеальное зеркало, глубина цвета 100%",
        (45, 45, 48),
        (10, 12, 15),
    )
    create_case_image(
        "case_dry_cleaning.jpg",
        "Детейлинг-химчистка светлой кожи",
        "Въевшаяся грязь, затертости от джинсов",
        "Оригинальный матовый оттенок + защита",
        (110, 95, 75),
        (215, 195, 160),
    )
    create_case_image(
        "case_ceramic.jpg",
        "Защитное керамическое покрытие 9H",
        "Без защиты: пленка воды, грязь на ЛКП",
        "Мощный гидрофоб: самоочищение кузова",
        (60, 70, 80),
        (20, 50, 90),
    )


if __name__ == "__main__":
    main()
