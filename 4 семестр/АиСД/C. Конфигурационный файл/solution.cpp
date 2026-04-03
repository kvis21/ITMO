#include <cctype>
#include <cstddef>
#include <cstring>
#include <iostream>
#include <map>
#include <stack>
#include <string>

using namespace std;

int main() {
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);

  stack<map<string, int>> stack_calls;
  map<string, int> current_values;

  string line;
  while (cin >> line) {
    if (line == "{") {
      stack_calls.push(map<string, int>());
      continue;
    }
    if (line == "}") {
      for (auto [var, old_value] : stack_calls.top()) {
        current_values[var] = old_value;
      }
      stack_calls.pop();
      continue;
    }

    size_t pos = line.find("=");

    string variable = line.substr(0, pos);
    string value = line.substr(pos + 1);

    if (!stack_calls.empty() && stack_calls.top().count(variable) == 0) {
      stack_calls.top()[variable] = current_values[variable];
    }

    if (isdigit(value[0]) || value[0] == '-') {
      current_values[variable] = stoi(value);
    } else {
      current_values[variable] = current_values[value];
      cout << current_values[variable] << "\n";
    }
  }

  return 0;
}