#include <cstdio>
#include <iostream>
#include <vector>

using namespace std;

int main() {
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);
  int n, k;

  cin >> n >> k;

  int distance;
  vector<int> distances(n);

  for (int i = 0; i < n; ++i) {
    cin >> distance;
    distances[i] = distance;
  }

  return 0;
}