#include <cctype>
#include <cstring>
#include <iostream>

using namespace std;

int main() {
  freopen("chaos.in", "r", stdin);
  freopen("chaos.out", "w", stdout);

  int a, b, c, d, k;
  cin >> a >> b >> c >> d >> k;

  for (int i = 0; i < k; ++i) {
    int prev_a = a;

    a = a * b - c;

    if (a <= 0) {
      a = 0;
      break;
    }
    if (a > d) {
      a = d;
    }
    if (a == prev_a) {
      break;
    }
  }
  cout << a << endl;
  return 0;
}