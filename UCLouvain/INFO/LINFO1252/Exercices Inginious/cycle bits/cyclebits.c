#include<stdio.h>
#include<stdint.h>

uint32_t cycle_bits(uint32_t x, uint8_t n) {
    for (int i = 0; i < n; i++){
        int h_bit = x & 0b10000000000000000000000000000000;

        x *= 2;
        if (h_bit){
            x++;
        }
    }
    return x;
}

void main(){
    printf("%u\n", cycle_bits(0b1, 4));
}