#include <stdint.h>
#include <stdio.h>

void exchange_pointers(int** a, int** b) {
    int* temp = *a;
    printf("%p  %p  %p\n", a, b, temp);
    *a = *b;
    printf("%p  %p  %p\n", a, b, temp);
    *b = temp;
    printf("%p  %p  %p\n", a, b, temp);
    return;
}
    

int main(){
    int x = 2;
    int y = 3;
    int* c = &x;
    int* d = &y;
    int** a = &c;
    int** b = &d;
    printf("pointers before swap : %p   %p\n", *a, *b);
    exchange_pointers(a , b);
    printf("pointers after swap : %p   %p\n", *a, *b);
}