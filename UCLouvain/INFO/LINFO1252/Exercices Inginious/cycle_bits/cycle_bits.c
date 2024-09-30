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

uint32_t cycle_bits(uint32_t x, uint8_t n) {
    for (int i = 0; i < n; i++){
        printBinary(x);
        uint8_t last = (x % 2);
        x = (x >> 1) + (0b10000000000000000000000000000000 * last);
    }
    printf("\n");
    printBinary(x);
    return x;
}

int main(){
    uint32_t x = 0b110;
    uint32_t a = cycle_bits(x, 4);
    printf("%u\n", a);
}