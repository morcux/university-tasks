import math

WIDTH = 60
LINE = "=" * WIDTH
THIN = "-" * WIDTH

UNITS = {
    "1": ("м²", "квадратний метр", 1.0),
    "2": ("га", "гектар", 10_000.0),
    "3": ("км²", "квадратний кілометр", 1_000_000.0),
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


def read_area(label):
    value = read_number(f"{label} — числове значення: ", "Площа")
    unit = choose_unit(f"{label} — одиниця вимірювання:")
    return value, unit


def print_in_all_units(m2):
    for short, _, factor in UNITS.values():
        print(f"  {fmt(m2 / factor):>25} {short}")


def make_convert(unit_key):
    short, _, factor = UNITS[unit_key]

    def calc():
        value = read_number(f"Введіть площу в {short}: ", "Площа")
        m2 = value * factor
        print(THIN)
        print(f"Результат: {fmt(value)} {short} дорівнює")
        for s2, _, f2 in UNITS.values():
            if s2 != short:
                print(f"  {fmt(m2 / f2):>25} {s2}")
        print(THIN)
    return calc


def calc_sum():
    v1, u1 = read_area("Перша площа")
    v2, u2 = read_area("Друга площа")
    total = v1 * u1[2] + v2 * u2[2]
    print(THIN)
    print(f"Сума: {fmt(v1)} {u1[0]} + {fmt(v2)} {u2[0]} =")
    print_in_all_units(total)
    print(THIN)


def calc_compare():
    v1, u1 = read_area("Перша площа")
    v2, u2 = read_area("Друга площа")
    a, b = v1 * u1[2], v2 * u2[2]
    first, second = f"{fmt(v1)} {u1[0]}", f"{fmt(v2)} {u2[0]}"
    print(THIN)
    if math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12):
        print(f"Площі рівні: {first} = {second}")
    else:
        sign = ">" if a > b else "<"
        print(f"Порівняння: {first} {sign} {second}")
        print("Різниця між площами:")
        print_in_all_units(abs(a - b))
        if min(a, b) > 0:
            print(f"Більша площа перевищує меншу в {fmt(max(a, b) / min(a, b))} раз(и).")
    print(THIN)


def calc_plot():
    length = read_number("Довжина ділянки, м: ", "Довжина", positive=True)
    width = read_number("Ширина ділянки, м: ", "Ширина", positive=True)
    m2 = length * width
    print(THIN)
    print(f"Площа ділянки S = {fmt(length)} м × {fmt(width)} м =")
    print_in_all_units(m2)
    print(THIN)


THEORY_UNITS = """\
Площа — величина, що характеризує розмір плоскої фігури або поверхні.

• Квадратний метр (м²) — основна одиниця площі в системі SI:
  площа квадрата зі стороною 1 м.
• Гектар (га) — позасистемна одиниця, площа квадрата зі стороною 100 м.
  Використовується для земельних ділянок, полів, лісів.
• Квадратний кілометр (км²) — площа квадрата зі стороною 1 км.
  Використовується для площ міст, областей, країн."""

THEORY_FORMULAS = """\
Основні співвідношення:
  1 га  = 100 м × 100 м   = 10 000 м²
  1 км² = 1000 м × 1000 м = 1 000 000 м²
  1 км² = 100 га

Формули переведення:
  м²  → га  :  S / 10 000        га  → м²  :  S × 10 000
  м²  → км² :  S / 1 000 000     км² → м²  :  S × 1 000 000
  га  → км² :  S / 100           км² → га  :  S × 100

Загальний принцип програми: значення спочатку переводиться в м²
(множенням на коефіцієнт одиниці), а потім ділиться на коефіцієнт
цільової одиниці."""

THEORY_EXAMPLES = """\
1) 2,5 га = 2,5 × 10 000 = 25 000 м²
2) 350 000 м² = 350 000 / 10 000 = 35 га = 0,35 км²
3) Ділянка 6 соток (1 сотка = 100 м²) = 600 м² = 0,06 га
4) Площа Києва ≈ 839 км² = 83 900 га = 839 000 000 м²"""

AUTHOR_INFO = """\
Автор:        Мельник Дмитро
Група:        ПД-21
Робота:       Практична робота №1
              «Багаторівневі інтерфейси-меню консольних застосунків»
Варіант:      Конвертер площ (м², га, км²)
Мова:         Python 3"""


def convert_menu():
    submenu("КОНВЕРТАЦІЯ ПЛОЩ", [
        calc_item(f"Перевести з {short} ({name}) в інші одиниці", make_convert(key))
        for key, (short, name, _) in UNITS.items()
    ])


def operations_menu():
    submenu("ОПЕРАЦІЇ З ПЛОЩАМИ", [
        calc_item("Сума двох площ у різних одиницях", calc_sum),
        calc_item("Порівняння двох площ", calc_compare),
        calc_item("Площа прямокутної ділянки (довжина × ширина)", calc_plot),
    ])


def theory_menu():
    submenu("ТЕОРЕТИЧНИЙ МАТЕРІАЛ", [
        text_item("Одиниці вимірювання площі", THEORY_UNITS),
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
        ("1", "Конвертація площ"),
        ("2", "Операції з площами"),
        ("3", "Теоретичний матеріал"),
        ("4", "Про автора"),
    ]
    actions = {"1": convert_menu, "2": operations_menu,
               "3": theory_menu, "4": author_menu}
    while True:
        choice = menu("КОНВЕРТЕР ПЛОЩ — ГОЛОВНЕ МЕНЮ", items, "Вихід з програми")
        if choice == "0":
            print("\nДякуємо за використання програми. До побачення!")
            return
        actions[choice]()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nРоботу програми перервано користувачем. До побачення!")