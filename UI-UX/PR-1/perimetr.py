import math

WIDTH = 60
LINE = "=" * WIDTH
THIN = "-" * WIDTH


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


def show_result(formula, calculation, name="Периметр P", value=None):
    print(THIN)
    print(f"Формула:     {formula}")
    print(f"Розрахунок:  {calculation}")
    if value is not None:
        print(f"Відповідь:   {name} = {fmt(value)} од.")
    print(THIN)


def side(prompt, what="Сторона"):
    return read_number(prompt, what, positive=True)


def calc_rect_sides():
    a = side("Довжина a: ", "Довжина")
    b = side("Ширина b: ", "Ширина")
    p = 2 * (a + b)
    show_result("P = 2 · (a + b)", f"P = 2 · ({fmt(a)} + {fmt(b)}) = {fmt(p)}", value=p)


def calc_square():
    a = side("Сторона квадрата a: ")
    p = 4 * a
    show_result("P = 4 · a", f"P = 4 · {fmt(a)} = {fmt(p)}", value=p)


def calc_rect_diagonal():
    a = side("Відома сторона a: ")
    while True:
        d = side("Діагональ d: ", "Діагональ")
        if d > a:
            break
        print("  [Помилка] Діагональ прямокутника має бути більшою за сторону (d > a).")
    b = math.sqrt(d ** 2 - a ** 2)
    p = 2 * (a + b)
    print(f"\nДруга сторона: b = √(d² − a²) = √({fmt(d)}² − {fmt(a)}²) = {fmt(b)}")
    show_result("P = 2 · (a + b)", f"P = 2 · ({fmt(a)} + {fmt(b)}) = {fmt(p)}", value=p)


def calc_tri_three_sides():
    while True:
        a = side("Сторона a: ")
        b = side("Сторона b: ")
        c = side("Сторона c: ")
        if a + b > c and a + c > b and b + c > a:
            break
        print("  [Помилка] Трикутник з такими сторонами не існує: сума будь-яких двох\n"
              "            сторін має бути більшою за третю. Введіть сторони ще раз.")
    p = a + b + c
    show_result("P = a + b + c", f"P = {fmt(a)} + {fmt(b)} + {fmt(c)} = {fmt(p)}", value=p)


def calc_tri_equilateral():
    a = side("Сторона рівностороннього трикутника a: ")
    p = 3 * a
    show_result("P = 3 · a", f"P = 3 · {fmt(a)} = {fmt(p)}", value=p)


def calc_tri_isosceles():
    a = side("Основа a: ", "Основа")
    while True:
        b = side("Бічна сторона b: ", "Бічна сторона")
        if 2 * b > a:
            break
        print("  [Помилка] Трикутник не існує: дві бічні сторони разом мають бути\n"
              "            більшими за основу (2b > a).")
    p = a + 2 * b
    show_result("P = a + 2 · b", f"P = {fmt(a)} + 2 · {fmt(b)} = {fmt(p)}", value=p)


def calc_tri_two_sides_angle():
    a = side("Сторона a: ")
    b = side("Сторона b: ")
    while True:
        g = read_number("Кут γ між ними (у градусах): ", "Кут", positive=True)
        if g < 180:
            break
        print("  [Помилка] Кут трикутника має бути в межах 0° < γ < 180°.")
    c = math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(math.radians(g)))
    p = a + b + c
    print(f"\nТретя сторона (теорема косинусів): c = √(a² + b² − 2ab·cos γ) = {fmt(c)}")
    show_result("P = a + b + c", f"P = {fmt(a)} + {fmt(b)} + {fmt(c)} = {fmt(p)}", value=p)


def calc_circle_radius():
    r = side("Радіус r: ", "Радіус")
    c = 2 * math.pi * r
    show_result("C = 2 · π · r", f"C = 2 · π · {fmt(r)} = {fmt(c)}", "Довжина кола C", c)


def calc_circle_diameter():
    d = side("Діаметр d: ", "Діаметр")
    c = math.pi * d
    show_result("C = π · d", f"C = π · {fmt(d)} = {fmt(c)}", "Довжина кола C", c)


def calc_circle_area():
    s = side("Площа круга S: ", "Площа")
    r = math.sqrt(s / math.pi)
    c = 2 * math.pi * r
    print(f"\nРадіус: r = √(S / π) = √({fmt(s)} / π) = {fmt(r)}")
    show_result("C = 2 · π · r", f"C = 2 · π · {fmt(r)} = {fmt(c)}", "Довжина кола C", c)


THEORY_GENERAL = """\
Периметр (P) — сума довжин усіх сторін многокутника, тобто довжина
його межі. Для кола аналогом периметра є довжина кола (C).
Периметр вимірюється в одиницях довжини (мм, см, м, км) — у тих самих,
в яких задано сторони. Програма виводить результат в «од.» — тобто
в тих одиницях, в яких введено дані."""

THEORY_RECT = """\
Прямокутник — чотирикутник, у якого всі кути прямі, а протилежні
сторони рівні.
  P = 2 · (a + b),   a — довжина, b — ширина
Квадрат — прямокутник з рівними сторонами:
  P = 4 · a
Якщо відомі сторона a і діагональ d (теорема Піфагора):
  b = √(d² − a²),    P = 2 · (a + b)
Приклад: a = 5, b = 3  →  P = 2 · (5 + 3) = 16"""

THEORY_TRIANGLE = """\
Трикутник — многокутник з трьома сторонами.
  P = a + b + c
Умова існування (нерівність трикутника): a + b > c, a + c > b, b + c > a.
Рівносторонній трикутник:  P = 3 · a
Рівнобедрений (основа a, бічна сторона b):  P = a + 2 · b,  умова 2b > a
Дві сторони і кут γ між ними (теорема косинусів):
  c = √(a² + b² − 2 · a · b · cos γ),   P = a + b + c
Приклад: a = 3, b = 4, γ = 90°  →  c = 5,  P = 12"""

THEORY_CIRCLE = """\
Коло — множина точок площини, рівновіддалених від центра.
  C = 2 · π · r = π · d,    π ≈ 3,14159
Якщо відома площа круга S:
  r = √(S / π),   C = 2 · π · r
Приклад: r = 5  →  C = 2 · π · 5 ≈ 31,4159"""

AUTHOR_INFO = """\
Автор:        Мельник Дмитро
Група:        ПД-21
Робота:       Практична робота №1
              «Багаторівневі інтерфейси-меню консольних застосунків»
Варіант:      Калькулятор периметрів (прямокутник, трикутник, коло)
Мова:         Python 3"""


def rect_menu():
    submenu("ПРЯМОКУТНИК І КВАДРАТ", [
        calc_item("Прямокутник за двома сторонами", calc_rect_sides),
        calc_item("Квадрат за стороною", calc_square),
        calc_item("Прямокутник за стороною і діагоналлю", calc_rect_diagonal),
    ])


def triangle_menu():
    submenu("ТРИКУТНИК", [
        calc_item("За трьома сторонами", calc_tri_three_sides),
        calc_item("Рівносторонній трикутник", calc_tri_equilateral),
        calc_item("Рівнобедрений трикутник", calc_tri_isosceles),
        calc_item("За двома сторонами і кутом між ними", calc_tri_two_sides_angle),
    ])


def circle_menu():
    submenu("КОЛО", [
        calc_item("Довжина кола за радіусом", calc_circle_radius),
        calc_item("Довжина кола за діаметром", calc_circle_diameter),
        calc_item("Довжина кола за площею круга", calc_circle_area),
    ])


def theory_menu():
    submenu("ТЕОРЕТИЧНИЙ МАТЕРІАЛ", [
        text_item("Що таке периметр", THEORY_GENERAL),
        text_item("Прямокутник і квадрат", THEORY_RECT),
        text_item("Трикутник", THEORY_TRIANGLE),
        text_item("Коло", THEORY_CIRCLE),
    ])


def author_menu():
    header("ПРО АВТОРА")
    print(AUTHOR_INFO)
    pause()


def main():
    print("Автор: Мельник Дмитро ПД-21")
    items = [
        ("1", "Прямокутник і квадрат"),
        ("2", "Трикутник"),
        ("3", "Коло"),
        ("4", "Теоретичний матеріал"),
        ("5", "Про автора"),
    ]
    actions = {"1": rect_menu, "2": triangle_menu, "3": circle_menu,
               "4": theory_menu, "5": author_menu}
    while True:
        choice = menu("КАЛЬКУЛЯТОР ПЕРИМЕТРІВ — ГОЛОВНЕ МЕНЮ", items, "Вихід з програми")
        if choice == "0":
            print("\nДякуємо за використання програми. До побачення!")
            return
        actions[choice]()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nРоботу програми перервано користувачем. До побачення!")