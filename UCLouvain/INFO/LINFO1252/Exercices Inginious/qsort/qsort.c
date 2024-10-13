#include <stdio.h>
#include <stdlib.h>
#include <ctype.h> 

void sort(void *base, size_t nel, size_t width, int (*compar)(const void *, const void *)) {
    // Handle special cases
    if (nel <= 1 || base == NULL || compar == NULL || width == 0) {
        // Nothing to sort
        return;
    }

    char *arr = (char *)base;
    // Allocate a temporary buffer to hold one element of size width
    char *temp = (char *)malloc(width);
    if (temp == NULL) {
        exit(EXIT_FAILURE);
    }

    for (size_t i = 1; i < nel; i++) {
        memcpy(temp, arr + i * width, width);

        size_t j = i;
        while (j > 0 && compar(temp, arr + (j - 1) * width) < 0) {
            memcpy(arr + j * width, arr + (j - 1) * width, width);
            j--;
        }
        memcpy(arr + j * width, temp, width);
    }
    free(temp);
}


void lower(void* s){
    char* s_p = (char*) s;
    while (*s_p != '\0'){
        if (*s_p >= 65 && *s_p <= 90){
            *s_p += 32;
        }
        s_p++;
    }
    return;
}

int compare(const void* a, const void* b) {
    const char* str1 = *(const char**)a;
    const char* str2 = *(const char**)b;

    while (*str1 && *str2) {
        // Convert both characters to lowercase for case-insensitive comparison
        char c1 = tolower((unsigned char)*str1);
        char c2 = tolower((unsigned char)*str2);

        if (c1 != c2) {
            return c1 - c2;
        }
        str1++;
        str2++;
    }

    // If both strings have reached the end, they are equal
    if (*str1 == '\0' && *str2 == '\0') {
        return 0;
    }

    // If one string has ended, the shorter string is considered smaller
    return (*str1 == '\0') ? -1 : 1;
}

void main(){
    char* A = "Ab[]A";
    char* a = "ab[]b";
    printf("Compare \"A\" and \"a\" : %i\n", compare(A,a));
}