#include <stdio.h>

void sort(void *base, size_t nel, size_t width, int (*compar)(const void *, const void *))
{
    return;
}

int compare(const void* a, const void* b){
    char s1 = *(char*) a;
    char s2 = *(char*) b;
    if (s1 >= 65 && s1 <= 91){
        s1 += 32;
    }
    if (s2 >= 65 && s2 <= 91){
        s2 += 32;
    }
    while(s1 && (s1 == s2)){
        s1++;
        s2++;
        if (s1 >= 65 && s1 <= 91){
            s1 += 32;
        }
        if (s2 >= 65 && s2 <= 91){
            s2 += 32;
        }
    }
    return s1 - s2;
}