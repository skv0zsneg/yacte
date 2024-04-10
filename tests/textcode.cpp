#include <iostream>


void say_hello(std::string user_name) {
    std::cout << "Hello, " << user_name << std::endl;
}

int main() {
    say_hello("User");
    return 0;
}
