#include <cctype>
#include <cstdio>
#include <iostream>
#include <stack>
#include <string>

using namespace std;

char transform(char chr) {
  if (isupper(chr)) {
    return tolower(chr);
  } else {
    return toupper(chr);
  }
}

int main() {
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);

  string animals;
  stack<char> holder;

  cin >> animals;

  for (char &animal : animals) {
    if (!holder.empty() && transform(holder.top()) == animal) {
        holder.pop();
    }
    holder.push(animal);
  }
}