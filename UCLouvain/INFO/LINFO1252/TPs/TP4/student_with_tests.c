#include <stdio.h>

static inline void my_inline_func(int *a, int b, int c){
    /* if(*a > 10) 
     *   *a = b + 3;
     * else 
     *   *a = c - 4;
     */
    __asm__(
        // ASM Template
        "cmpl $10,%0\n"
        "jg if\n"
        "subl $4,%2\n"
        "movl %2,%0\n"
        "jmp end\n"
        "if:\n"
        "addl $3,%1\n"
        "mov %1,%0\n"
        "end:"
        //outputs : + means read and write, m means location in memory
        :"+m"(*a)
        //inputs : r means register
        :"r"(b), "r"(c)
    );
}

int main(){
int a = 11, b = 2, c = 3;
    my_inline_func(&a, b, c);
    printf("Basic test: a = %d ; expected : %d \n", a, 5);

    a = 8, b = 2, c = 3;
    my_inline_func(&a, b, c);
    printf("Basic test: a = %d ; expected : %d \n", a, -1);

    a = 42, b = 12, c = 50;
    my_inline_func(&a, b, c);
    printf("Basic test: a = %d ; expected : %d \n", a, 15);

    a = 0, b = 12, c = 50;
    my_inline_func(&a, b, c);
    printf("Basic test: a = %d ; expected : %d \n", a, 46); 
    return 0;
}
