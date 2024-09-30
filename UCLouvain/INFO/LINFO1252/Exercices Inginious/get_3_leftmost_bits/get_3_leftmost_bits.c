#include <stdint.h>
#include <stdio.h>

uint8_t get_3_leftmost_bits(uint32_t x) {
    uint32_t only_3_leftmost = x & 0b11100000000000000000000000000000;
    only_3_leftmost /= 0b00100000000000000000000000000000;
    return (uint8_t) only_3_leftmost;
}

int main(){
    uint32_t x = 0b11011001010010100101010110100100;
    uint8_t a = get_3_leftmost_bits(x);
    printf("%u\n", a);
}