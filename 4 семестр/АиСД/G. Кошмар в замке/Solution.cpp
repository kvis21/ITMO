#include <algorithm>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

using namespace std;

int main() {
  freopen("aurora.in", "r", stdin);
  freopen("aurora.out", "w", stdout);

  string word;
  if (!(cin >> word)) {
    return 0;
  }

  int counts[26] = {0};
  for (char c : word) {
    counts[c - 'a']++;
  }

  vector<pair<long long, char>> char_weights;
  for (int i = 0; i < 26; ++i) {
    long long w;
    cin >> w;
    char_weights.push_back({w, (char)('a' + i)});
  }

  sort(char_weights.rbegin(), char_weights.rend());

  int n = (int)word.size();
  string result(n, ' ');
  int left = 0;
  int right = n - 1;

  for (auto cw : char_weights) {
    char ch = cw.second;
    int idx = ch - 'a';
    if (counts[idx] >= 2) {
      result[left] = ch;
      result[right] = ch;
      left++;
      right--;
      counts[idx] -= 2;
    }
  }

  int mid_ptr = left;
  for (int i = 0; i < 26; ++i) {
    while (counts[i] > 0) {
      result[mid_ptr] = (char)('a' + i);
      mid_ptr++;
      counts[i]--;
    }
  }

  cout << result;

  return 0;
}