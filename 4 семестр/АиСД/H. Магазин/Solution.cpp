#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

int main() {
  freopen("shop.in", "r", stdin);
  freopen("shop.out", "w", stdout);

  int n, k;
  cin >> n >> k;

  vector<int> a(n);
  for (int i = 0; i < n; ++i) {
    cin >> a[i];
  }

  sort(a.rbegin(), a.rend());

  long long total_cost = 0;
  for (int i = 0; i < n; ++i) {
    if ((i + 1) % k != 0) {
      total_cost += a[i];
    }
  }

  cout << total_cost << "\n";

  return 0;
}