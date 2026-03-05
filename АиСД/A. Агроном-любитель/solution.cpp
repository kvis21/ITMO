#include <cstdio>
#include <iostream>
#include <utility>

using namespace std;

int main() {
  freopen("agro.in", "r", stdin);
  freopen("agro.out", "w", stdout);

  int n, a;
  int left = 0, right = 0;
  int max_length = -1;
  pair<int, int> best_slice = {left, right};
  int current_flower = -1;
  int sequence = 0;

  cin >> n;
  for (int i = 0; i < n; i++) {
    cin >> a;

    if (current_flower != a) {
      current_flower = a;
      sequence = 1;
    } else {
      sequence++;
    }

    if (sequence == 3) {
      if (max_length < right - left) {
        max_length = right - left;
        best_slice = {left + 1, right};
      }
      left = i - 1;
      sequence--;
    }
    right++;
  }
  if (max_length < right - left) {
    max_length = right - left;
    best_slice = {left + 1, right};
  }
  cout << best_slice.first << " " << best_slice.second;
  return 0;
}