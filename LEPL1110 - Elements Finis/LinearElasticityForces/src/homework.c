#include "fem.h"

double** A_copie_non_contrain;
double* B_copie_non_contrain;

void femElasticityAssembleElements(femProblem *theProblem){
    femFullSystem  *theSystem = theProblem->system;
    femIntegration *theRule = theProblem->rule;
    femDiscrete    *theSpace = theProblem->space;
    femGeo         *theGeometry = theProblem->geometry;
    femNodes       *theNodes = theGeometry->theNodes;
    femMesh        *theMesh = theGeometry->theElements;
    femMesh        *theEdges = theGeometry->theEdges;
    double x[4],y[4],phi[4],dphidxsi[4],dphideta[4],dphidx[4],dphidy[4];
    int iElem,iInteg,iEdge,i,j,d,map[4],mapX[4],mapY[4];
    int nLocal = theMesh->nLocalNode;
    double a   = theProblem->A;
    double b   = theProblem->B;
    double c   = theProblem->C;      
    double rho = theProblem->rho;
    double g   = theProblem->g;
    double **A = theSystem->A;
    double *B  = theSystem->B;
    
    
    for (iElem = 0; iElem < theMesh->nElem; iElem++) {
        for (j=0; j < nLocal; j++) {
            map[j]  = theMesh->elem[iElem*nLocal+j];
            mapX[j] = 2*map[j];
            mapY[j] = 2*map[j] + 1;
            x[j]    = theNodes->X[map[j]];
            y[j]    = theNodes->Y[map[j]];} 
        
        for (iInteg=0; iInteg < theRule->n; iInteg++) {    
            double xsi    = theRule->xsi[iInteg];
            double eta    = theRule->eta[iInteg];
            double weight = theRule->weight[iInteg];  
            femDiscretePhi2(theSpace,xsi,eta,phi);
            femDiscreteDphi2(theSpace,xsi,eta,dphidxsi,dphideta);
            
            double dxdxsi = 0.0;
            double dxdeta = 0.0;
            double dydxsi = 0.0; 
            double dydeta = 0.0;
            for (i = 0; i < theSpace->n; i++) {  
                dxdxsi += x[i]*dphidxsi[i];       
                dxdeta += x[i]*dphideta[i];   
                dydxsi += y[i]*dphidxsi[i];   
                dydeta += y[i]*dphideta[i]; }
            double jac = fabs(dxdxsi * dydeta - dxdeta * dydxsi);
            
            for (i = 0; i < theSpace->n; i++) {    
                dphidx[i] = (dphidxsi[i] * dydeta - dphideta[i] * dydxsi) / jac;       
                dphidy[i] = (dphideta[i] * dxdxsi - dphidxsi[i] * dxdeta) / jac; }            
            for (i = 0; i < theSpace->n; i++) { 
                for(j = 0; j < theSpace->n; j++) {
                    A[mapX[i]][mapX[j]] += (dphidx[i] * a * dphidx[j] + 
                                            dphidy[i] * c * dphidy[j]) * jac * weight;                                                                                            
                    A[mapX[i]][mapY[j]] += (dphidx[i] * b * dphidy[j] + 
                                            dphidy[i] * c * dphidx[j]) * jac * weight;                                                                                           
                    A[mapY[i]][mapX[j]] += (dphidy[i] * b * dphidx[j] + 
                                            dphidx[i] * c * dphidy[j]) * jac * weight;                                                                                            
                    A[mapY[i]][mapY[j]] += (dphidy[i] * a * dphidy[j] + 
                                            dphidx[i] * c * dphidx[j]) * jac * weight; }}
             for (i = 0; i < theSpace->n; i++) {
                B[mapY[i]] -= phi[i] * g * rho * jac * weight; }}} 

}


void femElasticityAssembleNeumann(femProblem *theProblem){
    femFullSystem  *theSystem = theProblem->system;
    femIntegration *theRule = theProblem->ruleEdge;
    femDiscrete    *theSpace = theProblem->spaceEdge;
    femGeo         *theGeometry = theProblem->geometry;
    femNodes       *theNodes = theGeometry->theNodes;
    femMesh        *theEdges = theGeometry->theEdges;
    double x[2],y[2],phi[2];
    int iBnd,iElem,iInteg,iEdge,i,j,d,map[2],mapU[2];
    int nLocal = 2;
    double *B  = theSystem->B;

    for(iBnd=0; iBnd < theProblem->nBoundaryConditions; iBnd++){
        femBoundaryCondition *theCondition = theProblem->conditions[iBnd];
        femBoundaryType type = theCondition->type;
        double value = theCondition->value;
        // Seulement si c'est une condition de Neumann
        if(type == NEUMANN_X || type == NEUMANN_Y){
            // On parcourt les éléments de bord où il y a la condition
            for (iElem = 0; iElem < theCondition->domain->nElem; iElem++) {
                iEdge = theCondition->domain->elem[iElem]; // Car la condition ne doit être appliquée que sur les bords concernés. 
                for (j=0; j < nLocal; j++) {
                    map[j]  = theEdges->elem[iEdge*nLocal+j];
                    if(type == NEUMANN_X){
                        mapU[j] = 2*map[j];
                    }
                    if(type == NEUMANN_Y){
                        mapU[j] = 2*map[j] + 1;
                    }
                    x[j]    = theNodes->X[map[j]];
                    y[j]    = theNodes->Y[map[j]];
                    }

                // On fait l'intégration numérique
                for (iInteg=0; iInteg < theRule->n; iInteg++) {    
                    double jacobien = sqrt((x[1]-x[0])*(x[1]-x[0]) + (y[1]-y[0])*(y[1]-y[0]))/2; // h/2
                    double xsi    = theRule->xsi[iInteg];
                    double weight = theRule->weight[iInteg];  
                    femDiscretePhi(theSpace,xsi,phi);
                    for (i = 0; i < theSpace->n; i++) {
                        B[mapU[i]] += phi[i] * value * weight*jacobien; 
                    }
                }
            }
        }
    }
}


double *femElasticitySolve(femProblem *theProblem){
    femFullSystem  *theSystem = theProblem->system;

    femElasticityAssembleElements(theProblem);
    femElasticityAssembleNeumann(theProblem);

    // Pour pouvoir garder la matrice en copie pour la dernière fonction. 
    A_copie_non_contrain = malloc(theSystem->size * sizeof(double*));
    for (int i = 0; i < theSystem->size; i++) {
        A_copie_non_contrain[i] = malloc(theSystem->size * sizeof(double));
        memcpy(A_copie_non_contrain[i], theProblem->system->A[i], theProblem->system->size * sizeof(double));
    }

    B_copie_non_contrain = malloc(theSystem->size * sizeof(double));
    memcpy(B_copie_non_contrain, theProblem->system->B, theProblem->system->size * sizeof(double));
  
    int *theConstrainedNodes = theProblem->constrainedNodes; // Liste des numéros de la contrainte associé à un noeud.
    for (int i=0; i < theSystem->size; i++) { // i = le numéro du noeud.    
        if (theConstrainedNodes[i] != -1) { // Si une condition est appliquée sur le noeud. 
            //printf("Constrained Nodes : %d\n", theConstrainedNodes[i]);
            //printf("Condition : %s\n", theProblem->conditions[theConstrainedNodes[i]]->domain->name);
            // Via les prints, on voit que la numéro d'une condition est bien liée sur un domaine précis.

            double value = theProblem->conditions[theConstrainedNodes[i]]->value;
            femFullSystemConstrain(theSystem,i,value); 
        }
    }

    femFullSystemEliminate(theSystem);

    for(int i = 0; i<theSystem->size; i++){
        theProblem->soluce[i] = theSystem->B[i];}  

    return theProblem->soluce; 
}

double * femElasticityForces(femProblem *theProblem){        
           
    double *soluce = theProblem->soluce;
    femFullSystem *sys = theProblem->system;

    for (int i = 0; i < sys -> size; i++) {
        double AU = 0.0;
        for (int j = 0; j < sys -> size; j++) {
            AU += A_copie_non_contrain[i][j]*soluce[j];
        }
        theProblem->residuals[i] += AU - B_copie_non_contrain[i];
    }
    for(int i = 0; i<sys->size; i++){
        free(A_copie_non_contrain[i]);
    }
    free(A_copie_non_contrain);
    free(B_copie_non_contrain);
    return theProblem->residuals;
}