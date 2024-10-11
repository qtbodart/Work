#include<stdio.h>
#include<stdlib.h>

int fold(int* tab, size_t len, int res, int (*f)(int,int)){
    for (int i = 0; i<len; i++){
        res = f(tab[i], res);
    }
    return res;
}

int* map(int* tab, size_t len, int (*f)(int)){
    int* out = malloc(len*sizeof(int));
    for (int i = 0; i<len; i++){
        out[i] = f(tab[i]);
    }
    return out;
}

void main(){
    return;
}