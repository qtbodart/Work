#include"fem.h"

#define MIN(a,b) ((a) < (b) ? (a) : (b))
#ifndef NORENUMBER 

void femIsort(int *positions, double *xy, int xy_size){
    int i, j, key;
    double cmpvalue;
    for (i = 1; i < xy_size; i++){
        key = positions[i];
        cmpvalue = xy[positions[i]];
        j = i-1;

        while (j>=0 && xy[positions[j]] > cmpvalue){
            positions[j+1] = positions[j];
            j -= 1;
        }
        positions[j+1] = key;
    }
}

void femMeshRenumber(femMesh *theMesh, femRenumType renumType)
{
    int positions[theMesh->nodes->nNodes], *ptr;

    switch (renumType) {
        case FEM_NO :
            for (int i = 0; i < theMesh->nodes->nNodes; i++) 
                theMesh->nodes->number[i] = i;
            break;
// 
// A modifier :-)
// debut
//
        case FEM_XNUM :
            for (int i = 0; i < theMesh->nodes->nNodes; i++){
                positions[i] = i;
            }
            ptr = (int *)positions;
            femIsort(ptr, theMesh->nodes->X, theMesh->nodes->nNodes);
            for (int i = 0; i < theMesh->nodes->nNodes; i++){
                theMesh->nodes->number[positions[i]] = i;
            }
            break;

        case FEM_YNUM : 
            for (int i = 0; i < theMesh->nodes->nNodes; i++){
                positions[i] = i;
            }
            ptr = (int *)positions;
            femIsort(ptr, theMesh->nodes->Y, theMesh->nodes->nNodes);
            for (int i = 0; i < theMesh->nodes->nNodes; i++){
                theMesh->nodes->number[positions[i]] = i;
            }
            break;
// 
// end
//

        default : Error("Unexpected renumbering option"); }
}

#endif
#ifndef NOBAND 

int femMeshComputeBand(femMesh *theMesh)
{
    int myBand = theMesh->nodes->nNodes;
    
    // A completer :-)
    // calcul de la largeur de bande de la matrice

    myBand = 0;
    for (int i = 0; i < theMesh->nElem; i++) {
        for (int j = 0; j < theMesh->nLocalNode; j++) {
            for (int k = 0; k < theMesh->nLocalNode; k++) {
                int diff = fabs(theMesh->nodes->number[theMesh->elem[theMesh->nLocalNode * i + j]] - theMesh->nodes->number[theMesh->elem[theMesh->nLocalNode * i + k]]);
                if (diff > myBand) {
                    myBand = diff;
                }
            }
        }
    }
    myBand++;

    // for(int i = 0; i < theMesh->nElem; i++){
    //     int *elem = theMesh->elem;
    //     for(int j = 0; j < 3; j++){
    //         for(int k = 0; k < 3; k++){
    //             int diff = abs(theMesh->nodes->number[elem[j]] - theMesh->nodes->number[elem[k]]);
    //             if(diff < myBand){
    //                 myBand = diff;
    //             }
    //         }
    //     }
    // }
    
    return(myBand);
}


#endif
#ifndef NOBANDASSEMBLE


void femBandSystemAssemble(femBandSystem* myBandSystem, double *Aloc, double *Bloc, int *map, int nLoc)
{
    // A Ecrire :-)
    for (int i = 0; i < nLoc; i++) {
        int row = map[i];
        for (int j = 0; j < nLoc; j++) {
            int col = map[j];
            if (col >= row) {
                myBandSystem->A[row][col] += Aloc[i * nLoc + j];
            }
            myBandSystem->B[row] += Bloc[i];
        }
    }
}


#endif
#ifndef NOBANDELIMINATE


double  *femBandSystemEliminate(femBandSystem *myBand)
{
    double  **A, *B, factor;
    int     i, j, k, jend, size, band;
    A    = myBand->A;
    B    = myBand->B;
    size = myBand->size;
    band = myBand->band;
    
    // A completer :-)
    // élémination de Gauss pour une matrice bande
    for (k = 0; k < size-1; k++) {
        jend = MIN(size-1,k+band);
        for (j = k+1; j <= jend; j++) {
            factor = A[j][k]/A[k][k];
            for (i = k; i <= jend; i++) {
                A[j][i] -= factor*A[k][i];
            }
            B[j] -= factor*B[k];
        }
    }

    return(myBand->B);
}


#endif