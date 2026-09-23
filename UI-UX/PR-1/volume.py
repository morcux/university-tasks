import math

WIDTH = 60
LINE = "=" * WIDTH
THIN = "-" * WIDTH

UNITS = {
    "1": ("мл", "мілілітр", 0.001),
    "2": ("л", "літр", 1.0),
    "3": ("м³", "кубічний метр", 1000.0),
}


def header(title):
    print("\n" + LINE)
    print(title.center(WIDTH))
    print(LINE)


def fmt(x):
    if x == 0:
        return "0"
    if 1e-4 <= abs(x) < 1e15:
        text = f"{x:,.10f}".rstrip("0").rstrip(".")
        return text.replace(",", " ")
    return f"{x:.6g}"


def read_choice(valid):
    while True:
        choice = input(">>> Ваш вибір: ").strip()
        if choice in valid:
            return choice
        if choice == "":
            print("  [Помилка] Ви нічого не ввели. Введіть номер пункту меню.")
        else:
            print(f"  [Помилка] Пункту «{choice}» немає. "
                  f"Допустимі значення: {', '.join(valid)}.")


def read_number(prompt, what="Значення", positive=False):
    while True:
        raw = input(prompt).strip().replace(",", ".").replace(" ", "")
        if raw == "":
            print("  [Помилка] Порожнє введення. Введіть число, наприклад 12.5")
            continue
        try:
            value = float(raw)
        except ValueError:
            print(f"  [Помилка] «{raw}» не є числом. Приклад правильного введення: 12.5")
            continue
        if not math.isfinite(value):
            print("  [Помилка] Допускаються лише скінченні числа.")
            continue
        if value < 0:
            print(f"  [Помилка] {what}: значення не може бути від'ємним. Введіть число ≥ 0.")
            continue
        if positive and value == 0:
            print(f"  [Помилка] {what}: значення має бути більшим за нуль.")
            continue
        return value


def ask_again():
    while True:
        ans = input("\nВиконати ще раз з іншими даними? (т — так / н — ні): ").strip().lower()
        if ans in ("т", "так", "y", "yes"):
            return True
        if ans in ("н", "ні", "n", "no"):
            return False
        print("  [Помилка] Введіть «т» (так) або «н» (ні).")


def pause():
    input("\nНатисніть Enter, щоб повернутися до меню...")


def menu(title, items, zero_label):
    header(title)
    for key, text in items:
        print(f"  {key}. {text}")
    print(f"  0. {zero_label}")
    print(THIN)
    keys = [key for key, _ in items]
    print(f"Введіть номер пункту ({keys[0]}–{keys[-1]}) і натисніть Enter; "
          f"0 — {zero_label.lower()}.")
    return read_choice(keys + ["0"])


def submenu(title, entries):
    items = [(str(i), name) for i, (name, _) in enumerate(entries, 1)]
    while True:
        choice = menu(title, items, "Назад")
        if choice == "0":
            return
        entries[int(choice) - 1][1]()


def run_calc(title, calc):
    while True:
        header(title)
        calc()
        if not ask_again():
            return


def calc_item(name, calc):
    return name, lambda: run_calc(name, calc)


def text_item(name, text):
    def show():
        header(name)
        print(text)
        pause()
    return name, show


def choose_unit(prompt):
    print(prompt)
    for key, (short, name, _) in UNITS.items():
        print(f"    {key}. {short} ({name})")
    return UNITS[read_choice(list(UNITS))]


def read_volume(label):
    value = read_number(f"{label} — числове значення: ", "Об'єм")
    unit = choose_unit(f"{label} — одиниця вимірювання:")
    return value, unit


def print_in_all_units(litres):
    for short, _, factor in UNITS.values():
        print(f"  {fmt(litres / factor):>25} {short}")


def make_convert(unit_key):
    short, _, factor = UNITS[unit_key]

    def calc():
        value = read_number(f"Введіть об'єм в {short}: ", "Об'єм")
        litres = value * factor
        print(THIN)
        print(f"Результат: {fmt(value)} {short} дорівнює")
        for s2, _, f2 in UNITS.values():
            if s2 != short:
                print(f"  {fmt(litres / f2):>25} {s2}")
        print(THIN)
    return calc


def calc_sum():
    v1, u1 = read_volume("Перший об'єм")
    v2, u2 = read_volume("Другий об'єм")
    total = v1 * u1[2] + v2 * u2[2]
    print(THIN)
    print(f"Сума: {fmt(v1)} {u1[0]} + {fmt(v2)} {u2[0]} =")
    print_in_all_units(total)
    print(THIN)


def calc_compare():
    v1, u1 = read_volume("Перший об'єм")
    v2, u2 = read_volume("Другий об'єм")
    a, b = v1 * u1[2], v2 * u2[2]
    first, second = f"{fmt(v1)} {u1[0]}", f"{fmt(v2)} {u2[0]}"
    print(THIN)
    if math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12):
        print(f"Об'єми рівні: {first} = {second}")
    else:
        sign = ">" if a > b else "<"
        print(f"Порівняння: {first} {sign} {second}")
        print("Різниця між об'ємами:")
        print_in_all_units(abs(a - b))
        if min(a, b) > 0:
            print(f"Більший об'єм перевищує менший в {fmt(max(a, b) / min(a, b))} раз(и).")
    print(THIN)


def calc_tank():
    a = read_number("Довжина ємності, см: ", "Довжина", positive=True)
    b = read_number("Ширина ємності, см: ", "Ширина", positive=True)
    h = read_number("Висота ємності, см: ", "Висота", positive=True)
    ml = a * b * h
    print(THIN)
    print(f"Об'єм V = {fmt(a)} × {fmt(b)} × {fmt(h)} = {fmt(ml)} см³, тобто")
    print_in_all_units(ml / 1000)
    print(THIN)


THEORY_UNITS = """\
Об'єм — величина, що характеризує місткість тіла або посудини
(кількість простору, який воно займає).

• Кубічний метр (м³) — основна одиниця об'єму в системі SI:
  об'єм куба з ребром 1 м. Використовується для води в лічильниках,
  газу, будматеріалів.
• Літр (л) — позасистемна одиниця, дорівнює 1 дм³ (куб з ребром 10 см).
  Використовується для напоїв, пального, місткості посуду.
• Мілілітр (мл) — тисячна частина літра, дорівнює 1 см³.
  Використовується в медицині, кулінарії, косметиці."""

THEORY_FORMULAS = """\
Основні співвідношення:
  1 л  = 1 дм³ = 1000 мл
  1 мл = 1 см³ = 0,001 л
  1 м³ = 1000 л = 1 000 000 мл

Формули переведення:
  мл → л  :  V / 1000            л  → мл :  V × 1000
  л  → м³ :  V / 1000            м³ → л  :  V × 1000
  мл → м³ :  V / 1 000 000       м³ → мл :  V × 1 000 000

Об'єм прямокутної ємності:  V = a × b × h
(якщо розміри в см, результат — у см³ = мл)."""

THEORY_EXAMPLES = """\
1) 2,5 л = 2,5 × 1000 = 2500 мл
2) 750 мл = 750 / 1000 = 0,75 л
3) 3,2 м³ води за місяць = 3200 л
4) Акваріум 60 × 30 × 40 см = 72 000 см³ = 72 л = 0,072 м³"""

AUTHOR_INFO = """\
Автор:        Мельник Дмитро
Група:        ПД-21
Робота:       Практична робота №1
              «Багаторівневі інтерфейси-меню консольних застосунків»
Варіант:      Конвертер об'ємів (л, мл, м³)
Мова:         Python 3"""


def convert_menu():
    submenu("КОНВЕРТАЦІЯ ОБ'ЄМІВ", [
        calc_item(f"Перевести з {short} ({name}) в інші одиниці", make_convert(key))
        for key, (short, name, _) in UNITS.items()
    ])


def operations_menu():
    submenu("ОПЕРАЦІЇ З ОБ'ЄМАМИ", [
        calc_item("Сума двох об'ємів у різних одиницях", calc_sum),
        calc_item("Порівняння двох об'ємів", calc_compare),
        calc_item("Об'єм прямокутної ємності (a × b × h, см)", calc_tank),
    ])


def theory_menu():
    submenu("ТЕОРЕТИЧНИЙ МАТЕРІАЛ", [
        text_item("Одиниці вимірювання об'єму", THEORY_UNITS),
        text_item("Формули переведення", THEORY_FORMULAS),
        text_item("Приклади розрахунків", THEORY_EXAMPLES),
    ])


def author_menu():
    header("ПРО АВТОРА")
    print(AUTHOR_INFO)
    pause()


def main():
    print("Автор: Мельник Дмитро ПД-21")
    items = [
        ("1", "Конвертація об'ємів"),
        ("2", "Операції з об'ємами"),
        ("3", "Теоретичний матеріал"),
        ("4", "Про автора"),
    ]
    actions = {"1": convert_menu, "2": operations_menu,
               "3": theory_menu, "4": author_menu}
    while True:
        choice = menu("КОНВЕРТЕР ОБ'ЄМІВ — ГОЛОВНЕ МЕНЮ", items, "Вихід з програми")
        if choice == "0":
            print("\nДякуємо за використання програми. До побачення!")
            return
        actions[choice]()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nРоботу програми перервано користувачем. До побачення!")