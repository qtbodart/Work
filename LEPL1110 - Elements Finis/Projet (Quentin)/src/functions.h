#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define FALSE 0 
#define TRUE  1
#define MAXNAME 256

typedef struct{
    char name[MAXNAME];
    int nElements;
    int* elements;
} Domain;

typedef struct{
    int nNodes;
    int* num;
    double* X;
    double* Y;

    int nEdges;
    int* edges;

    int nElements;
    int elementNodes;
    int* elements;

    int nDomains;
    Domain** domains;
} Mesh;

/*
Frees all memory allocated to `fmesh`
*/
void freeMesh();

/*
Converts the `.txt` file into a "Mesh" structure so that it can be used directly in the code.
*/
Mesh* parseFile();