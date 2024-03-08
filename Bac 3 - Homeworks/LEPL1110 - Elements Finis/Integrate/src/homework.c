#include <stdio.h>
#include <math.h>
#include "glfem.h"


double integrate(double x[3], double y[3], double (*f) (double, double))
{
    double I = 0;
    double xLoc[3];
    double yLoc[3];

    double w[3] = {1.0/6.0, 1.0/6.0, 1.0/6.0};
    double xi[3] = {1.0/6.0, 2.0/3.0, 1.0/6.0};
    double eta[3] = {1.0/6.0, 1.0/6.0, 2.0/3.0};

    // double HitTheRoadJac = (x[1]-x[0])*(y[2]-y[0])-(y[1]-y[0])*(x[2]-x[0]);

    for (int i = 0; i < 3; i++)
    {
        xLoc[i] = x[0] + xi[i]*(x[1]-x[0]) + eta[i]*(x[2]-x[0]);
        yLoc[i] = y[0] + xi[i]*(y[1]-y[0]) + eta[i]*(y[2]-y[0]);
        I += w[i]*f(xLoc[i],yLoc[i]);
    }
    
    glfemSetColor(GLFEM_BLACK); glfemDrawElement(x,y,3);
    glfemSetColor(GLFEM_BLUE);  glfemDrawNodes(x,y,3);
    glfemSetColor(GLFEM_RED);   glfemDrawNodes(xLoc,yLoc,3);

    return I;
}


/*
On considère un triangle dont l'angle droit se situe en bas à gauche, avec
(x1,y1) le coin inférieur gauche, (x2,y2) le coin inférieur droit et (x3,y3) le coin supérieur.
A chaque récursion, soit on renvoit l'intégrale approximée si n=0, soit on applique la récursion
sur les 4 sous-triangle obtenus en divisant les côtés par 2 si n>0
*/
double integrateRecursive(double x[3], double y[3], double (*f)(double,double), int n)
{   
    // printf("Entered with values : (%f,%f), (%f,%f), (%f,%f) and depth %d\n",x[0],y[0],x[1],y[1],x[2],y[2],n);
    double I = 0;

    if (n == 0){
        return integrate(x,y,f);
    }
    else if (n > 0){
        double newx[3];
        double newy[3];

        // triangle 1 (down-left)
        newx[0] = x[0];
        newx[1] = (x[1]-x[0])/2;
        newx[2] = x[2];
        
        newy[0] = y[0];
        newy[1] = y[1];
        newy[2] = (y[2]-y[0])/2;

        I += integrateRecursive(newx,newy,f,n-1)/4;

        // triangle 2 (up-left)
        newx[0] = x[0];
        newx[1] = (x[1]-x[0])/2;
        newx[2] = x[2];
        
        newy[0] = (y[2]-y[0])/2;
        newy[1] = (y[2]-y[0])/2;
        newy[2] = y[2];

        I += integrateRecursive(newx,newy,f,n-1)/4;

        // triangle 3 (down-right)
        newx[0] = (x[1]-x[0])/2;
        newx[1] = x[1];
        newx[2] = (x[1]-x[0])/2;
        
        newy[0] = y[0];
        newy[1] = y[1];
        newy[2] = (y[2]-y[0])/2;

        I += integrateRecursive(newx,newy,f,n-1)/4;

        // triangle 4 (center)
        newx[0] = (x[1]-x[0])/2;
        newx[1] = x[0];
        newx[2] = (x[1]-x[0])/2;
        
        newy[0] = (y[2]-y[0])/2;
        newy[1] = (y[2]-y[0])/2;
        newy[2] = y[0];

        I += integrateRecursive(newx,newy,f,n-1)/4;
        // printf("Evaluated interal to %f\n",I);
        return I;
    }
    return 0;
}
