#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define FALSE 0 
#define TRUE  1
#define MAXNAME 256


typedef enum {FEM_TRIANGLE,FEM_QUAD} ElementType;
typedef enum {FEM_FULL,FEM_BAND,FEM_ITER} SolverType;
typedef enum {FEM_NO,FEM_XNUM,FEM_YNUM, FEM_PROPNUM} RenumType;

typedef struct {
    int nNodes;
    double *X;
    double *Y;
    int *number;
} Nodes;

typedef struct {
    int nLocalNode;
    int nElem;
    int* elem;
    Nodes* nodes;
} Mesh;

typedef struct {
    Mesh* mesh;
    int nElem;
    int* elem;
    char name[MAXNAME];
} Domain;