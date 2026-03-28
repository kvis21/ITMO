from math import sqrt, exp

def f(x):
    return sqrt(1 + x**2) - exp(-2 * x)

def quadratic_approximation(x1, h, eps):
    iteration = 1

    x2 = x1 + h
    f1, f2 = f(x1), f(x2)
    
    if f1 > f2:
        x3 = x1 + 2 * h
    else:
        x3 = x1 - h
    f3 = f(x3)

    print(f"{'Ит.':<4} | {'x1':<8} | {'x2':<8} | {'x3':<8}  | {'x_bar':<8} | {'f(x_bar)':<8} | {'x_min':<8} | {'f(x_min)':<8}")
    print("-" * 100)

    while True:
        f1, f2, f3 = f(x1), f(x2), f(x3)
        
        points = [(x1, f1), (x2, f2), (x3, f3)]
        x_min_pt, f_min = min(points, key=lambda p: p[1])
 
        num = (x2**2 - x3**2)*f1 + (x3**2 - x1**2)*f2 + (x1**2 - x2**2)*f3
        den = (x2 - x3)*f1 + (x3 - x1)*f2 + (x1 - x2)*f3
        
        if den < eps:
            x1 = x_min_pt
            x2 = x1 + h
            f2 = f(x2)
            if f1 > f2:
                x3 = x1 + 2*h
            else:
                x3 = x1 - h
            continue

        x_bar = 0.5 * (num / den)
        f_bar = f(x_bar)

        print(f"{iteration:<4} | {x1:<8.3f} | {x2:<8.3f} | {x3:<8.3f} | {x_bar:<8.3f} | {f_bar:<8.3f} | {x_min_pt:<8.3f} | {f_min:<8.3f}")

        if abs((f_min - f_bar) / f_bar) < eps and abs((x_min_pt - x_bar) / x_bar) < eps:
            print("-" * 70)
            print(f"Минимум найден: x = {x_bar}, f(x) = {f_bar}")
            break
        
        
        if  x1 <= x_bar <= x3:
            all_points = [(x1, f1), (x2, f2), (x3, f3), (x_bar, f_bar)]
            best_points = sorted(all_points, key=lambda p: p[0])[:3]
            
            x1, x2, x3 = best_points[0][0], best_points[1][0], best_points[2][0]
        else:
            x1 = x_min_pt
            x2 = x1 + h
            if f(x1) > f(x2):
                x3 = x1 + 2 * h
            else:
                x3 = x1 - h
        
        iteration += 1
        if iteration > 100: 
            break

quadratic_approximation(x1=0.5, h=0.1, eps=0.0001)