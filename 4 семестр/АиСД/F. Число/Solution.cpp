#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

bool compareStrings(const string a, const string b) {
  return (a + b) > (b + a);
}

int main() {
  freopen("number.in", "r", stdin);
  freopen("number.out", "w", stdout);

  vector<string> numbers;
  string number;

  while (cin >> number) {
    numbers.push_back(number);
  }

  sort(numbers.begin(), numbers.end(), compareStrings);

  for (int i = 0; i < (int)numbers.size(); ++i) {
    cout << numbers[i];
  }

  return 0;
}