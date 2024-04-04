#include "functions.h"

/*
DEBUGGING : allows to print information about what's in the Mesh structure returned by `parseFile`.
*/
void checkParsedFile(verbose){
    Mesh* output = parseFile("./data/mesh.txt");
    printf("Info about mesh :\n");
    printf("Number of nodes : %d\n", output->nNodes);
    if(verbose){
        printf("Nodes :\n");
        for (int i = 0; i < output->nNodes; i++){
            printf("%d : %le %le\n", output->num[i], output->X[i], output->Y[i]);
        }
    }

    printf("Number of edges : %d\n", output->nEdges);

    if(verbose){
        for (int i = 0; i < output->nEdges; i++){
            printf("%d : %d %d\n", i, output->edges[2*i], output->edges[2*i+1]);
        }
    }
    
    printf("Number of elements : %d\n", output->nElements);
    if(verbose){
        if (output->elementNodes == 3){
            for (int i = 0; i < output->nElements; i++){
                printf("%d : %d %d %d\n", i, output->elements[3*i], output->elements[3*i+1], output->elements[3*i+2]);
            }
        }
        if (output->elementNodes == 4){
            for (int i = 0; i < output->nElements; i++){
                printf("%d : %d %d %d %d\n", i, output->elements[4*i], output->elements[4*i+1], output->elements[4*i+2], output->elements[4*i+3]);
            }
        }
    }
    
    printf("Number of domains : %d\n", output->nDomains);
    if(verbose){
        for (int i = 0; i < output->nDomains; i++){
            printf("%d : %s, number of elements : %d, first element : %d\n", i, output->domains[i]->name, output->domains[i]->nElements, output->domains[i]->elements[0]);
        }
    }
    printf("Number of nodes per element : %d\n",output->elementNodes);
    freeMesh(output);
}

int main(void){
    checkParsedFile(TRUE);
    return 0;
}