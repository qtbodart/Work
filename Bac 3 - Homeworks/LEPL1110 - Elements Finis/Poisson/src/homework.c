#include "fem.h"

# ifndef NOPOISSONCREATE

femPoissonProblem *femPoissonCreate(const char *filename)
{
    femGeo* theGeometry = geoMeshCreate(filename);
    femPoissonProblem *theProblem = malloc(sizeof(femPoissonProblem));
    theProblem->geo  = theGeometry;
    femMesh *theMesh = theGeometry->theElements;
    if (theMesh->nLocalNode == 4) {
        theProblem->space = femDiscreteCreate(4,FEM_QUAD);
        theProblem->rule = femIntegrationCreate(4,FEM_QUAD); }
    else if (theMesh->nLocalNode == 3) {
        theProblem->space = femDiscreteCreate(3,FEM_TRIANGLE);
        theProblem->rule = femIntegrationCreate(3,FEM_TRIANGLE); }
    theProblem->system = femFullSystemCreate(theMesh->nodes->nNodes);
    return theProblem;
}

# endif
# ifndef NOPOISSONBOUNDARY

void femPoissonFindBoundaryNodes(femPoissonProblem *theProblem)
{
    femGeo* theGeometry = theProblem->geo;  
    femMesh* theEdges = theGeometry->theEdges;
    int nBoundary = 0;

    int* raw = theEdges->elem;     
    
    int* seen = malloc(theGeometry->theNodes->nNodes*sizeof(int));
    for (int i = 0; i < theGeometry->theNodes->nNodes; i++){seen[i] = 0;}

    for (int i = 0; i < (2*theEdges->nElem); i++){
        if (seen[raw[i]] == 0){
            seen[raw[i]] = 1;
            nBoundary++;
        }
    }

    femDomain *theBoundary = malloc(sizeof(femDomain));
    theGeometry->nDomains++;
    theGeometry->theDomains = realloc(theGeometry->theDomains,theGeometry->nDomains*sizeof(femDomain*));
    theGeometry->theDomains[theGeometry->nDomains-1] = theBoundary;
    theBoundary->nElem = nBoundary;
    theBoundary->elem = malloc(nBoundary*sizeof(int));
    theBoundary->mesh = NULL;
    sprintf(theBoundary->name,"Boundary");
 
    int cur_elem = 0;
    for (int i = 0; i < theGeometry->theNodes->nNodes; i++){
        if (seen[i] == 1){
            theBoundary->elem[cur_elem] = i;
            cur_elem++;
        }
    }

    free(seen);
}
   
# endif
# ifndef NOPOISSONFREE

void femPoissonFree(femPoissonProblem *theProblem)
{
    geoMeshFree(theProblem->geo);           femDiscreteFree(theProblem->space);
    femIntegrationFree(theProblem->rule);   femFullSystemFree(theProblem->system);
    free(theProblem);
}
   
# endif
# ifndef NOPOISSONLOCAL

void femPoissonLocal(femPoissonProblem *theProblem, const int iElem, int *map, double *x, double *y)
{
    femMesh *theMesh = theProblem->geo->theElements;
    
    int geo_n = theMesh->nLocalNode;
    for (int i = 0; i < geo_n; i++){
        map[i] = theMesh->elem[iElem*geo_n+i];
        x[i] = theMesh->nodes->X[map[i]]; y[i] = theMesh->nodes->Y[map[i]];
    }
}

# endif
# ifndef NOPOISSONSOLVE

void femPoissonSolve(femPoissonProblem *theProblem)
{

    femMesh *theMesh = theProblem->geo->theElements;
    femDomain *theBoundary = geoGetDomain(theProblem->geo,"Boundary");
    femFullSystem *theSystem = theProblem->system;
    femIntegration *theRule = theProblem->rule;
    femDiscrete *theSpace = theProblem->space;
 
    if (theSpace->n > 4) Error("Unexpected discrete space size !");  
    double x[4],y[4],phi[4],dphidxsi[4],dphideta[4],dphidx[4],dphidy[4];
    int iElem,iInteg,iEdge,i,j,map[4];
    int nLocal = theMesh->nLocalNode;

    // A completer :-)
    for (iElem = 0; iElem < theMesh->nElem; iElem++) {
        femPoissonLocal(theProblem,iElem,map,x,y);
        for (i = 0; i < nLocal; i++){
            for (j = i; j < nLocal; j++){
                double I = 0.0;
                double I_b = 0.0;
                for (iInteg = 0; iInteg < theRule->n; iInteg++){
                    double xsi = theRule->xsi[iInteg];
                    double eta = theRule->eta[iInteg];
                    double weight = theRule->weight[iInteg];

                    theSpace->dphi2dx(xsi, eta, dphidxsi, dphideta);
                    theSpace->phi2(xsi, eta, phi);

                    double dxdxi  = 0.0;        double dydxi  = 0.0;
                    double dxdeta = 0.0;        double dydeta = 0.0;

                    for (int k = 0; k < theMesh->nLocalNode; k++){
                        dxdxi  += x[k]*dphidxsi[k];         dydxi  += y[k]*dphidxsi[k];
                        dxdeta += x[k]*dphideta[k];         dydeta += y[k]*dphideta[k];
                    }
                    double absHTRJack = fabs(dxdxi*dydeta - dydxi*dxdeta);
                    double dphi_i2dx = (dphidxsi[i]*dydeta - dphideta[i]*dydxi) / absHTRJack;
                    double dphi_i2dy = (dphideta[i]*dxdxi - dphidxsi[i]*dxdeta) / absHTRJack;
                    double dphi_j2dx = (dphidxsi[j]*dydeta - dphideta[j]*dydxi) / absHTRJack;
                    double dphi_j2dy = (dphideta[j]*dxdxi - dphidxsi[j]*dxdeta) / absHTRJack;
                    I += weight*(dphi_i2dx*dphi_j2dx + dphi_i2dy*dphi_j2dy) * absHTRJack;
                    if (i == j){
                        I_b += phi[i]*absHTRJack*weight;
                    }
                }
                theSystem->A[map[i]][map[j]] += I;

                if (i == j) {
                    theSystem->B[map[i]] += I_b;
                }
                else {
                    theSystem->A[map[j]][map[i]] += I;
                }
            }
        }
    }
    for (iEdge = 0; iEdge<theBoundary->nElem; iEdge++){
        femFullSystemConstrain(theSystem,theBoundary->elem[iEdge],0.0);
    }
    femFullSystemEliminate(theSystem);
    return;
}

# endif