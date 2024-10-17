// mp:
//   subl $8, %esp
//   movl 16(%esp), %edx
//   movl 12(%esp), %ecx
//   movl %ecx,%eax
//   addl %ecx,%ecx
//   addl %eax,%ecx
//   cmpl %edx,%ecx
//   jle m1
//   movl %edx, %eax
//   addl $8, %esp
//   ret
// m1:
//   movl %ecx, %eax
//   addl $8, %esp
//   ret

int mp(int a, int c, int d){
    a -= 8;
    a = c;
    c += c;
    c += a;
    if (d > c){
        
    }
}