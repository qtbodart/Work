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

uint8_t nbits(uint32_t n) {
    uint8_t output = 0;
    for (int i = 0; i < 32; i++){
        output += n%2;
        n = n>>1;
    }
    return output;
}

int main(){
    uint32_t x = 0b11011;
    uint8_t a = nbits(x);
    printf("%u\n", a);
}