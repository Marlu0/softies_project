#include <iostream>
#include <vector>
using namespace std;

template <typename T>
T sum(const vector<T>& v) {
    T total = 0;
    for (auto& e : v) total += e;
    return total;
}

int main() {
    vector<int> nums = {1, 2, 3, 4};
    cout << sum(nums) << endl;
}
