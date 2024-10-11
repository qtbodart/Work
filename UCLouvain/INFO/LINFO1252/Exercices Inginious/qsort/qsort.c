#include <stdio.h>

void sort(void *base, size_t nel, size_t width, int (*compar)(const void *, const void *)) {
    // Selection sort
    size_t i, j, min_idx;
    char *arr = (char *)base;

    for (i = 0; i < nel - 1; i++) {
        min_idx = i;

        // Find the index of the minimum element in the unsorted portion
        for (j = i + 1; j < nel; j++) {
            if (compar(arr + j * width, arr + min_idx * width) < 0) {
                min_idx = j;
            }
        }

        // Swap the minimum element with the new minimum, if found
        if (min_idx != i) {
            size_t k;
            for (k = 0; k < width; k++) {
                char temp = arr[i * width + k];
                arr[i * width + k] = arr[min_idx * width + k];
                arr[min_idx * width + k] = temp;
            }
        }
    }
}


int compare(const void* a, const void* b){
    char* p_a = (char*) a;
    char* p_b = (char*) b;
    char char_a;
    char char_b;

    while(1){
        char_a = *p_a;
        char_b = *p_b;
        // To lowercase
        if (char_a >= 65 && char_a <= 90){
            char_a += 32;
        }
        if (char_b >= 65 && char_b <= 90){
            char_b += 32;
        }

        // Return 0 if no difference found
        if (!char_a && !char_b){
            return 0;
        }

        // Return if difference found
        if (char_a != char_b){
            return (unsigned char) char_a- (unsigned char) char_b;
        }


        p_a++;
        p_b++;
    }

    return 0;
}

void main(){
    char* A = "aBc";
    char* a = "Ab";
    printf("Compare \"A\" and \"a\" : %i\n", compare(A,a));
}