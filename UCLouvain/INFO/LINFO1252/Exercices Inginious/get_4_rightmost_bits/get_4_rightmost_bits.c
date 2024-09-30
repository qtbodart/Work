#include <stdint.h>
#include <stdio.h>

uint8_t get_4_rightmost_bits(uint32_t x) {
    return (uint8_t) (x & 0b1111);
}

int main(){
    uint32_t x = 0b11011001010010100101010110101111;
    uint8_t a = get_4_rightmost_bits(x);
    printf("%u\n", a);
}