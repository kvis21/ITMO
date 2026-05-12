#include <cstddef>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;

const int INF = 1e9;

int main() {
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);

  int n, k, p;
  if (!(cin >> n >> k >> p))
    return 0;

  vector<int> queries(p);
  vector<vector<int>> pos(n + 1);
  for (int i = 0; i < p; ++i) {
    cin >> queries[i];
    pos[queries[i]].push_back(i);
  }

  vector<int> pos_idx(n + 1, 0);
  vector<bool> on_floor(n + 1, false);
  int floor_count = 0;
  int operations = 0;

  priority_queue<pair<int, int>> pq;

  for (int i = 0; i < p; ++i) {
    int c = queries[i];
    pos_idx[c]++;

    int next_use = ((size_t)pos_idx[c] < pos[c].size()) ? pos[c][pos_idx[c]] : INF;

    if (on_floor[c]) {
      pq.push({next_use, c});
    } else {
      operations++;

      if (floor_count == k) {
        while (!pq.empty()) {
          int evict_c = pq.top().second;
          pq.pop();

          if (on_floor[evict_c]) {
            on_floor[evict_c] = false;
            floor_count--;
            break;
          }
        }
      }

      on_floor[c] = true;
      floor_count++;
      pq.push({next_use, c});
    }
  }

  cout << operations;
  return 0;
}