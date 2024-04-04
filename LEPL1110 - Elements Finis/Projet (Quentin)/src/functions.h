#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define FALSE 0 
#define TRUE  1
#define MAXNAME 256

typedef struct{
    char* name;
    int nElements;
    int* elements;
} Domain;

typedef struct{
    int nNodes;
    int* num;
    double* X;
    double* Y;

    int nEdges;
    double* edges;

    int nElements;
    int elementNodes;
    double* elements;

    int nDomains;
    Domain* domains;
} Mesh;

/*
Converts the `.txt` file into a "Mesh" structure so that it can be used directly in the code.
*/
Mesh* parseFile(char* filename);