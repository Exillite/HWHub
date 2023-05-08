import sympy


def calculate_mark(hw_points, sub_points, formula, fine) -> float:
    points_count = len(hw_points)  # CNT
    done_count = sum([1 if p != 0 else 0 for p in sub_points])  # C
    total_points = [hw_points[i] * sub_points[i] for i in range(points_count)]
    sum_total_points = sum(total_points)  # K

    CNT = sympy.Symbol('CNT')
    C = sympy.Symbol('C')
    K = sympy.Symbol('K')

    expr = sympy.sympify(formula)
    calc = expr.subs(
        [(CNT, points_count), (C, done_count), (K, sum_total_points)])

    mark = calc + fine
    mark = round(mark, 2)
    return float(mark)
