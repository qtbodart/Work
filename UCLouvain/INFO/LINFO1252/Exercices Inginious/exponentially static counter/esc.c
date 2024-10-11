#include<stdio.h>

unsigned int stexp() {
    static unsigned int count = 1;

    if (count == 8192){
        count = 1;
    }

    count *= 2;
    return count/2;
}

void main(){
    for (int i = 0; i < 30; i++){
        printf("%u\n", stexp());
    }
}