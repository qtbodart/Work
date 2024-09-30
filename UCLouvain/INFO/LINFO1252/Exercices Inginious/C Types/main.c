int main(){
    int z = 0;
    static int* x = &z;
    *x = 0;
}