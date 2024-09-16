#include "functions.h"

Mesh* parseFile(const char* filename){
    Mesh* output = malloc(sizeof(Mesh));
    FILE* file = fopen(filename, "r");
    if (file == NULL) {printf("Unable to open file while parsing\n"); exit(-1);}
    char elementType[MAXNAME];
    char line[MAXNAME];

    // Extracting all nodes
    fgets(line, MAXNAME, file);
    sscanf(line, "Number of nodes %d ", &output->nNodes);
    output->X = malloc(output->nNodes * sizeof(double));
    output->Y = malloc(output->nNodes * sizeof(double));
    output->num = malloc(output->nNodes  * sizeof(int));
    for (int i = 0; i < output->nNodes; i++){
        fgets(line, MAXNAME, file);
        sscanf(line, "%d : %le %le", &output->num[i], &output->X[i], &output->Y[i]);
    }

    // Extracting all edges
    fgets(line, MAXNAME, file);
    sscanf(line, "Number of edges %d ", &output->nEdges);
    output->edges = malloc(2 * output->nEdges * sizeof(int));
    for (int i = 0; i < output->nEdges; i++){
        fgets(line, MAXNAME, file);
        sscanf(line, "%*d : %d %d", &output->edges[2*i], &output->edges[2*i+1]);
    }

    // Extracting all finite elements
    fgets(line, MAXNAME, file);
    sscanf(line, "Number of %s %d ", elementType, &output->nElements);
    if (strncasecmp(elementType, "triangles", MAXNAME) == 0){output->elementNodes=3;}else{output->elementNodes=4;}
    output->elements = malloc(output->nElements * output->elementNodes * sizeof(int));
    for (int i = 0; i < output->nElements; i++){
        fgets(line, MAXNAME, file);
        if (output->elementNodes == 3){
            sscanf(line, "%*d : %d %d %d", &output->elements[3*i], &output->elements[3*i+1], &output->elements[3*i+2]);
        } else if (output->elementNodes == 4){
            sscanf(line, "%*d : %d %d %d %d", &output->elements[4*i], &output->elements[4*i+1], &output->elements[4*i+2], &output->elements[4*i+3]);
        }
    }

    // Extracting all domains
    fgets(line, MAXNAME, file);
    sscanf(line, "Number of domains %d", &output->nDomains);
    int nDomains = output->nDomains;
    output->domains = malloc(sizeof(Domain *) * nDomains);
    for (int iDomain = 0; iDomain < nDomains; iDomain++) {
        Domain *theDomain = malloc(sizeof(Domain));
        output->domains[iDomain] = theDomain;
        fgets(line, MAXNAME, file);
        sscanf(line, "  Domain : %*d \n");
        fgets(line, MAXNAME, file);
        sscanf(line, "  Name : %s \n", (char *)&theDomain->name);
        fgets(line, MAXNAME, file);
        sscanf(line, "  Number of elements : %6d\n", &theDomain->nElements);
        theDomain->elements = malloc(sizeof(int) * theDomain->nElements);
        const char s[2] = " ";
        int j = 0;
        do{
            fgets(line, MAXNAME, file);
            char* token = strtok(line,s);
            while ( token != NULL) {
                theDomain->elements[j] = atoi(token);
                token = strtok(NULL, s);
                j++;
            }
        } while (j == theDomain->nElements-1);
    }

    fclose(file);
    return output;
}

void freeMesh(Mesh* fmesh){
    free(fmesh->num);
    free(fmesh->X);
    free(fmesh->Y);
    free(fmesh->edges);
    free(fmesh->elements);
    for (int i = 0; i < fmesh->nDomains; i++){
        free(fmesh->domains[i]->elements);
        free(fmesh->domains[i]);
    }
    free(fmesh->domains);
    free(fmesh);
}