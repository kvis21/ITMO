#include <stdio.h>

#ifdef _WIN32
    #define DLLEXPORT __declspec(dllexport)
#else
    #define DLLEXPORT
#endif


typedef struct {
    int x;
    int y;
} Point;

DLLEXPORT void process_point(Point* p) {
    printf("[C] Получена структура. x = %d, y = %d\n", p->x, p->y);
    p->x = p->x * 10;
    p->y = p->y * 10;
    printf("[C] Значения модифицированы.\n");
}


DLLEXPORT long long fib_c(int n) {
    if (n <= 1) {
        return n;
    } else {
        return fib_c(n - 1) + fib_c(n - 2);
    }
}

DLLEXPORT long long fib_c_iterative(int n) {
    if (n <= 1) return n;
    
    long long a = 0;
    long long b = 1;
    long long temp;
    
    for (int i = 2; i <= n; i++) {
        temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}