#include <cctype>
#include <cstddef>
#include <cstdio>
#include <iostream>
#include <stack>
#include <string>
#include <vector>

using namespace std;

int main() {
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);

  string data;
  cin >> data;

  vector<int> trap_to_animal(data.size() / 2 + 1);
  stack<pair<char, int>> traps_animals;

  int current_id = 0;
  int animal_cnt = 0;
  int trap_cnt = 0;

  for (char trap_animal : data) {
    if (isupper(trap_animal)) {
      current_id = ++trap_cnt;
    } else {
      current_id = ++animal_cnt;
    }

    if (!traps_animals.empty()) {
      auto top_element = traps_animals.top();
      if (tolower(top_element.first) == tolower(trap_animal) &&
          islower(top_element.first) != islower(trap_animal)) {
        if (isupper(trap_animal)) {
          trap_to_animal[current_id] = top_element.second;
        } else {
          trap_to_animal[top_element.second] = current_id;
        }
        traps_animals.pop();
        continue;
      }
    }
    traps_animals.push({trap_animal, current_id});
  }

  if (traps_animals.empty()) {
    cout << "Possible" << endl;
    for (size_t i = 1; i < trap_to_animal.size(); ++i) {
      cout << trap_to_animal[i] << " ";
    }
    cout << endl;
  } else {
    cout << "Impossible" << endl;
  }

  return 0;
}