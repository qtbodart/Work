#include <stdint.h>
#include <stdio.h>

void printBinary(uint32_t x){
    char bin[32] = {"0"};
    for (int i = 0; i < 32; i++){
        bin[31-i] = 48+(x%2);
        x = x >> 1;
    }
    printf("%s\n", bin);
}

uint32_t reset_highestorder_strong_bit(uint32_t x) {
    uint32_t cur = 0b10000000000000000000000000000000;
    while ((x & cur) == 0 && cur != 0)
    {
        cur /= 2;
    }
    if (cur != 0){
        return x-cur;
    }
    return x;
}

int main(){
    uint32_t x = 0b1011;
    uint32_t a = reset_highestorder_strong_bit(x);
    printBinary(a);
}