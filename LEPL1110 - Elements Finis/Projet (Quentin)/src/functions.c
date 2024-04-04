#include <functions.h>

Mesh* parseFile(const char* filename){
    Mesh* output = malloc(sizeof(Mesh));
    FILE* file = fopen(filename, "r");
    if (file == NULL) {printf("Unable to open file while parsing\n"); exit(-1);}
    char elementType[MAXNAME];

    // Scans for information about the number of nodes, edges, shapes and domains there is in the file
    fscanf(file, "Number of nodes %d \n", output->nNodes);
    fscanf(file, "Number of edges %d \n", output->nEdges);
    fscanf(file, "Number of %s %d \n", elementType, output->nElements);
    fscanf(file, "Number of domains %d\n", &output->nDomains);

    // Sets the type of element we'll be working with (either triangles or quads)
    if (strcasecmp(elementType,"triangles") == 0) {output->elementNodes = 3;}else{output->elementNodes = 4;}

    // Gets the position of each node and gives them a numerotation
    output->X = malloc(output->nNodes * sizeof(double));
    output->Y = malloc(output->nNodes * sizeof(double));
    for (int i = 0; i < output->nNodes; i++){
        fscanf(file, "%*d : %le %le \n", &output->X[i], &output->Y[i]);
        output->num[i] = i;
    }

    // Gets the edges between the nodes
    output->edges = malloc(output->nEdges*sizeof(int)*2);
    for (int i = 0; i < output->nEdges; i++){
        fscanf(file, "%*d : %6d %6d \n", &output->edges[2*i], &output->edges[2*i+1]);
    }

    // Gets the elements
    output->elements = malloc(output->nElements * output->elementNodes * sizeof(int));
    for (int i = 0; i < output->nElements; i++){
        if (output->elementNodes == 3){
            fscanf(file, "%*d : %6d %6d %6d \n", &output->elements[3*i], &output->elements[3*i+1], &output->elements[3*i+2]);
        } else {
            fscanf(file, "%*d : %6d %6d %6d %6d \n", &output->elements[4*i], &output->elements[4*i+1], &output->elements[4*i+2], &output->elements[4*i+3]);
        }
    }

    // Gets the domains
    output->domains = malloc(output->nDomains*sizeof(Domain));
    for (int iDomain = 0; iDomain < output->nDomains; iDomain++) {
        Domain* newDomain = malloc(sizeof(Domain));
        fscanf(file, "  Domain : %*d \n");
        fscanf(file, "  Name : %[^\n]s \n", (char *)&newDomain->name);
        fscanf(file, "  Number of elements : %6d\n", &newDomain->nElements);
        newDomain->elements = malloc(sizeof(int) * 2 * newDomain->nElements);
        for (int i = 0; i < newDomain->nElements; i++) {
            fscanf(file, "%6d", &newDomain->elements[i]);
            if ((i + 1) != newDomain->nElements && (i + 1) % 10 == 0){
                fscanf(file, "\n");
            }
        }
    }

    return output;
}