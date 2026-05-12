#include <deque>
#include <iostream>
#include <vector>

using namespace std;

int main() {
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);

  int n, k;
  if (!(cin >> n >> k)) {
    return 0;
  }

  vector<int> a(n);
  for (int i = 0; i < n; ++i) {
    cin >> a[i];
  }

  deque<int> dq;
  for (int i = 0; i < n; ++i) {
    if (!dq.empty() && dq.front() <= i - k) {
      dq.pop_front();
    }

    while (!dq.empty() && a[dq.back()] >= a[i]) {
      dq.pop_back();
    }

    dq.push_back(i);

    if (i >= k - 1) {
      cout << a[dq.front()] << " ";
    }
  }

  return 0;
}