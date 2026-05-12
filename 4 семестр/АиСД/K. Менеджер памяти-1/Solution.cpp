#include <algorithm>
#include <iostream>
#include <random>
#include <vector>

using namespace std;

typedef long long ll;

mt19937 rng(1337);

struct Node {
  ll L, R, size;
  bool is_free;
  ll max_free;
  int priority;
  Node* left;
  Node* right;

  Node(ll l_pos, ll r_pos, bool free)
      : L(l_pos)
      , R(r_pos)
      , size(r_pos - l_pos + 1)
      , is_free(free)
      , priority(rng())
      , left(nullptr)
      , right(nullptr) {
    update();
  }

  void update() {
    max_free = is_free ? size : 0;
    if (left) {
      max_free = max(max_free, left->max_free);
    }
    if (right) {
      max_free = max(max_free, right->max_free);
    }
  }
};

vector<Node*> req_nodes;
Node* root = nullptr;

void split(Node* t, ll L, Node*& l, Node*& r) {
  if (!t) {
    l = r = nullptr;
    return;
  }
  if (t->L < L) {
    split(t->right, L, t->right, r);
    l = t;
  } else {
    split(t->left, L, l, t->left);
    r = t;
  }
  if (l) {
    l->update();
  }
  if (r) {
    r->update();
  }
}

Node* merge(Node* l, Node* r) {
  if (!l || !r) {
    return l ? l : r;
  }
  if (l->priority > r->priority) {
    l->right = merge(l->right, r);
    l->update();
    return l;
  } else {
    r->left = merge(l, r->left);
    r->update();
    return r;
  }
}

Node* find_first_fit(Node* t, ll K) {
  if (!t || t->max_free < K) {
    return nullptr;
  }
  if (t->left && t->left->max_free >= K) {
    return find_first_fit(t->left, K);
  }
  if (t->is_free && t->size >= K) {
    return t;
  }
  return find_first_fit(t->right, K);
}

void free_block(int request_id) {
  if (request_id >= (int)req_nodes.size()) {
    return;
  }
  Node* to_free = req_nodes[request_id];
  if (!to_free) {
    return;
  }

  ll curL = to_free->L;
  ll curR = to_free->R;

  Node* l;
  Node* mid;
  Node* r;
  split(root, curL, l, r);
  split(r, curR + 1, mid, r);

  delete mid;

  if (l) {
    Node* prev = l;
    while (prev->right) {
      prev = prev->right;
    }
    if (prev->is_free) {
      curL = prev->L;
      Node* l1;
      Node* l2;
      split(l, prev->L, l1, l2);
      l = l1;
      delete l2;
    }
  }

  if (r) {
    Node* next = r;
    while (next->left) {
      next = next->left;
    }
    if (next->is_free) {
      curR = next->R;
      Node* r1;
      Node* r2;
      split(r, next->R + 1, r1, r2);
      r = r2;
      delete r1;
    }
  }

  Node* combined = new Node(curL, curR, true);
  root = merge(l, merge(combined, r));
  req_nodes[request_id] = nullptr;
}

int main() {
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);

  ll n;
  int m;
  if (!(cin >> n >> m)) {
    return 0;
  }
  req_nodes.resize(m + 1, nullptr);

  root = new Node(1, n, true);

  for (int i = 1; i <= m; ++i) {
    ll x;
    cin >> x;
    if (x > 0) {
      Node* target = find_first_fit(root, x);
      if (!target) {
        cout << "-1\n";
      } else {
        ll L = target->L;
        ll oldR = target->R;
        cout << L << "\n";

        Node* l;
        Node* mid;
        Node* r;
        split(root, L, l, r);
        split(r, oldR + 1, mid, r);

        req_nodes[i] = new Node(L, L + x - 1, false);
        Node* new_tree = merge(l, req_nodes[i]);

        if (mid->size > x) {
          new_tree = merge(new_tree, new Node(L + x, oldR, true));
        }
        root = merge(new_tree, r);
        delete mid;
      }
    } else {
      free_block(-x);
    }
  }
  return 0;
}