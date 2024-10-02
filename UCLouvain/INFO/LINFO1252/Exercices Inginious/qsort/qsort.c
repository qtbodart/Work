#include <stdio.h>

void sort(void *base, size_t nel, size_t width, int (*compar)(const void *, const void *))
{
    return;
}

int compare(const void* a, const void* b){
    const char* s1 = a;
    const char* s2 = b;
    while(*s1 && (*s1 == *s2)){
        s1++;
        s2++;
    }
    return *s1 - *s2;
}