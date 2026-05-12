#include <iostream>
#include <list>

using namespace std;

int main() {
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);

  int n;
  if (!(cin >> n))
    return 0;

  list<int> q;
  auto mid = q.end();

  for (int i = 0; i < n; ++i) {
    char op;
    cin >> op;

    if (op == '+') {
      int id;
      cin >> id;
      q.push_back(id);

      if (q.size() == 1) {
        mid = q.begin();
      } else if (q.size() % 2 == 1) {
        mid++;
      }
    } else if (op == '*') {
      int id;
      cin >> id;

      if (q.empty()) {
        q.push_back(id);
        mid = q.begin();
      } else {
        auto pos = mid;
        pos++;
        q.insert(pos, id);

        if (q.size() % 2 == 1) {
          mid++;
        }
      }
    } else if (op == '-') {
      cout << q.front() << "\n";

      if (q.size() == 1) {
        q.pop_front();
        mid = q.end();
      } else {
        if (q.size() % 2 == 0) {
          mid++;
        }
        q.pop_front();
      }
    }
  }

  return 0;
}