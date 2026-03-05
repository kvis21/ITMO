#include <iostream>

using namespace std;

int main() {
  int t;
  string s;
  size_t left, right;
  cin >> t;

  for (int i = 0; i < t; i++) {
    cin >> s;
    bool is_square_string = true;
    left = 0;
    right = s.size() / 2;
    while (right < s.size()) {
      if (s[left] != s[right] || s.size() % 2 != 0) {
        is_square_string = false;
        break;
      }
      left++;
      right++;
    }

    if (is_square_string) {
      cout << "YES" << endl;
    } else {
      cout << "NO" << endl;
    }
  }
  return 0;
}