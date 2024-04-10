#include "fem.h"

//
// Ici, vous pouvez définir votre géométrie :-)
//  (1) Raffiner intelligemment.... (yes )
//  (2) Construire la geometrie avec OpenCascade
//  (3) Construire la geometrie avec les outils de GMSH
//  (4) Obtenir la geometrie en lisant un fichier .geo de GMSH

double geoSize(double x, double y) {

  femGeo *theGeometry = geoGetGeometry();
  return theGeometry->h * (1.0 - 0.5 * x);
}

void geoMeshGenerate(void) {
  femGeo *theGeometry = geoGetGeometry();
  double Lx = 1.0;
  double Ly = 1.0;
  theGeometry->LxPlate = Lx;
  theGeometry->LyPlate = Ly;
  theGeometry->h = Lx * 0.05;
  theGeometry->elementType = FEM_QUAD;

  geoSetSizeCallback(geoSize);

  double w = theGeometry->LxPlate;
  double h = theGeometry->LyPlate;

  int ierr;
  double r = w / 4;
  int idRect = gmshModelOccAddRectangle(0.0, 0.0, 0.0, w, h, -1, 0.0, &ierr);
  int idDisk = gmshModelOccAddDisk(w / 2.0, h / 2.0, 0.0, r, r, -1, NULL, 0, NULL, 0, &ierr);
  int idSlit = gmshModelOccAddRectangle(w / 2.0, h / 2.0 - r, 0.0, w, 2.0 * r, -1, 0.0, &ierr);
  int rect[] = {2, idRect};
  int disk[] = {2, idDisk};
  int slit[] = {2, idSlit};

  gmshModelOccCut(rect, 2, disk, 2, NULL, NULL, NULL, NULL, NULL, -1, 1, 1, &ierr);
  gmshModelOccCut(rect, 2, slit, 2, NULL, NULL, NULL, NULL, NULL, -1, 1, 1, &ierr);
  gmshModelOccSynchronize(&ierr);

  if (theGeometry->elementType == FEM_QUAD) {
    gmshOptionSetNumber("Mesh.SaveAll", 1, &ierr);
    gmshOptionSetNumber("Mesh.RecombineAll", 1, &ierr);
    gmshOptionSetNumber("Mesh.Algorithm", 8, &ierr);
    gmshOptionSetNumber("Mesh.RecombinationAlgorithm", 1.0, &ierr);
    gmshModelGeoMeshSetRecombine(2, 1, 45, &ierr);
    gmshModelMeshGenerate(2, &ierr);
  }

  if (theGeometry->elementType == FEM_TRIANGLE) {
    gmshOptionSetNumber("Mesh.SaveAll", 1, &ierr);
    gmshModelMeshGenerate(2, &ierr);
  }

  return;
}

void geoMeshGenerateGeo(void) {
  
    int ierr;
    int base = gmshModelOccAddRectangle(0, 0, 0, 40, 82, -1, 0,&ierr);
    ErrorGmsh(ierr);
    int based[] = {2,base};

    double rec_point[14][2][2] = {
        {{0 ,59},{5 ,82}},
        {{40,59},{35,82}},
        {{0 ,0 },{5 ,52}},
        {{40,0 },{35,52}},
        {{5 ,77},{15,82}},
        {{35,77},{25,82}},
        {{5 ,70},{15,59}},
        {{35,70},{25,59}},
        {{5 ,41},{15,52}},
        {{35,41},{25,52}},
        {{5 ,28},{15,34}},
        {{35,28},{25,34}},
        {{5 ,0 },{8 ,28}},
        {{35,0 },{32,28}}
    };

    for (int i = 0; i < sizeof(rec_point)/sizeof(rec_point[0]); i++){
        int temp_rec = gmshModelOccAddRectangle(rec_point[i][0][0], rec_point[i][0][1], 0, rec_point[i][1][0]-rec_point[i][0][0], rec_point[i][1][1]-rec_point[i][0][1], -1, 0,&ierr);
        ErrorGmsh(ierr);
        int temp[] = {2, temp_rec};
        gmshModelOccCut(based, 2, temp, 2, NULL, NULL, NULL, NULL, NULL, -1, 1, 1, &ierr);
        ErrorGmsh(ierr);
    }
    
    double trian_point[63][3][2] = {
        {{5 ,71},{5 ,77},{15,77}},
        {{15,77},{15,82},{20,82}},
        {{0 ,53},{0 ,59},{15,59}},
        {{5 ,35},{5 ,41},{15,41}},
        {{8 ,0 },{8 ,28},{15,28}},
        {{7 ,71},{15,71},{15,76}},
        {{3 ,53},{15,53},{15,58}},
        {{7 ,35},{15,35},{15,40}},
        {{35,71},{35,77},{25,77}},
        {{25,77},{25,82},{20,82}},
        {{40,53},{40,59},{25,59}},
        {{35,35},{35,41},{25,41}},
        {{32,0 },{32,28},{25,28}},
        {{33,71},{25,71},{25,76}},
        {{37,53},{25,53},{25,58}},
        {{33,35},{25,35},{25,40}},
        {{16.0 , 77.0},{20.0 , 81.0},{24.0 , 77.0}},
        {{16.0 , 76.0},{20.0 , 74.0},{24.0 , 76.0}},
        {{16.0 , 75.0},{16.0 , 72.0},{19.0 , 73.5}},
        {{16.0 , 71.0},{20.0 , 73.0},{24.0 , 71.0}},
        {{24.0 , 75.0},{24.0 , 72.0},{21.0 , 73.5}},
        {{16.0 , 70.0},{20.0 , 68.0},{24.0 , 70.0}},
        {{16.0 , 66.0},{16.0 , 69.0},{19.0 , 67.5}},
        {{16.0 , 65.0},{20.0 , 67.0},{24.0 , 65.0}},
        {{24.0 , 66.0},{24.0 , 69.0},{21.0 , 67.5}},
        {{16.0 , 64.0},{20.0 , 62.0},{24.0 , 64.0}},
        {{16.0 , 63.0},{16.0 , 60.0},{19.0 , 61.5}},
        {{16.0 , 59.0},{20.0 , 61.0},{24.0 , 59.0}},
        {{24.0 , 63.0},{24.0 , 60.0},{21.0 , 61.5}},
        {{16.0 , 58.0},{20.0 , 56.0},{24.0 , 58.0}},
        {{16.0 , 57.0},{16.0 , 54.0},{19.0 , 55.5}},
        {{16.0 , 53.0},{20.0 , 55.0},{24.0 , 53.0}},
        {{24.0 , 57.0},{24.0 , 54.0},{21.0 , 55.5}},
        {{16.0 , 52.0},{20.0 , 50.0},{24.0 , 52.0}},
        {{16.0 , 51.0},{16.0 , 48.0},{19.0 , 49.5}},
        {{16.0 , 47.0},{20.0 , 49.0},{24.0 , 47.0}},
        {{24.0 , 51.0},{24.0 , 48.0},{21.0 , 49.5}},
        {{16.0 , 46.0},{20.0 , 44.0},{24.0 , 46.0}},
        {{16.0 , 45.0},{16.0 , 42.0},{19.0 , 43.5}},
        {{16.0 , 41.0},{20.0 , 43.0},{24.0 , 41.0}},
        {{24.0 , 45.0},{24.0 , 42.0},{21.0 , 43.5}},
        {{16.0 , 40.0},{20.0 , 38.0},{24.0 , 40.0}},
        {{16.0 , 39.0},{16.0 , 36.0},{19.0 , 37.5}},
        {{16.0 , 35.0},{20.0 , 37.0},{24.0 , 35.0}},
        {{24.0 , 39.0},{24.0 , 36.0},{21.0 , 37.5}},
        {{16.0 , 34.0},{20.0 , 32.0},{24.0 , 34.0}},
        {{16.0 , 33.0},{16.0 , 30.0},{19.0 , 31.5}},
        {{16.0 , 29.0},{20.0 , 31.0},{24.0 , 29.0}},
        {{24.0 , 33.0},{24.0 , 30.0},{21.0 , 31.5}},
        {{16.0 , 28.0},{20.0 , 24.0},{24.0 , 28.0}},
        {{15.75 , 27.0},{14.25 , 21.0},{19.0 , 23.5}},
        {{24.25 , 27.0},{25.75 , 21.0},{21.0 , 23.5}},
        {{20.0 , 23.0},{14.0 , 20.0},{26.0 , 20.0}},
        {{20.0 , 16.0},{14.0 , 20.0},{26.0 , 20.0}},
        {{13.75 , 19.0},{19.0 , 15.5},{12.25 , 13.0}},
        {{26.25 , 19.0},{21.0 , 15.5},{27.75 , 13.0}},
        {{20.0 , 15.0},{12.0 , 12.0},{28.0 , 12.0}},
        {{20.0 , 8.0},{12.0 , 12.0},{28.0 , 12.0}},
        {{11.75 , 11.0},{19.0 , 7.5},{10.25 , 5.0}},
        {{28.25 , 11.0},{21.0 , 7.5},{29.75 , 5.0}},
        {{20.0 , 7.0},{10.0 , 4.0},{30.0 , 4.0}},
        {{9.0 , 0.0},{10.0 , 4.0},{30.0 , 4.0}},
        {{9.0 , 0.0},{31.0 , 0.0},{30.0 , 4.0}}
    };

    for (int i = 0; i < sizeof(trian_point)/sizeof(trian_point[0]); i++){
        int P1 = gmshModelOccAddPoint(trian_point[i][0][0], trian_point[i][0][1], 0, 0, -1, &ierr);
        ErrorGmsh(ierr);
        int P2 = gmshModelOccAddPoint(trian_point[i][1][0], trian_point[i][1][1], 0, 0, -1, &ierr);
        ErrorGmsh(ierr);
        int P3 = gmshModelOccAddPoint(trian_point[i][2][0], trian_point[i][2][1], 0, 0, -1, &ierr);
        ErrorGmsh(ierr);
        int L1 = gmshModelOccAddLine(P1, P2, -1, &ierr);
        ErrorGmsh(ierr);
        int L2 = gmshModelOccAddLine(P2, P3, -1, &ierr);
        ErrorGmsh(ierr);
        int L3 = gmshModelOccAddLine(P3, P1, -1, &ierr);
        ErrorGmsh(ierr);
        int l[] = {L1, L2, L3};
        int C1 = gmshModelOccAddCurveLoop(l,3, -1, &ierr);
        ErrorGmsh(ierr);
        int s[] = {C1};
        int S1 = gmshModelOccAddPlaneSurface(s,1, -1, &ierr);
        ErrorGmsh(ierr);
        int trou[] = {2,S1};
        gmshModelOccCut(based,2,trou,2,NULL,NULL,NULL,NULL,NULL,-1,1,1,&ierr);
        ErrorGmsh(ierr);
    }
    
    double penta_point[0][5][2] = {
        
    };

    for (int i = 0; i < sizeof(penta_point)/sizeof(penta_point[0]); i++){
        int P1 = gmshModelOccAddPoint(penta_point[i][0][0], penta_point[i][0][1], 0, 0, -1, &ierr);
        ErrorGmsh(ierr);
        int P2 = gmshModelOccAddPoint(penta_point[i][1][0], penta_point[i][1][1], 0, 0, -1, &ierr);
        ErrorGmsh(ierr);
        int P3 = gmshModelOccAddPoint(penta_point[i][2][0], penta_point[i][2][1], 0, 0, -1, &ierr);
        ErrorGmsh(ierr);
        int P4 = gmshModelOccAddPoint(penta_point[i][3][0], penta_point[i][3][1], 0, 0, -1, &ierr);
        ErrorGmsh(ierr);
        int P5 = gmshModelOccAddPoint(penta_point[i][4][0], penta_point[i][4][1], 0, 0, -1, &ierr);
        ErrorGmsh(ierr);
        int L1 = gmshModelOccAddLine(P1, P2, -1, &ierr);
        ErrorGmsh(ierr);
        int L2 = gmshModelOccAddLine(P2, P3, -1, &ierr);
        ErrorGmsh(ierr);
        int L3 = gmshModelOccAddLine(P3, P4, -1, &ierr);
        ErrorGmsh(ierr);
        int L4 = gmshModelOccAddLine(P4, P5, -1, &ierr);
        ErrorGmsh(ierr);
        int L5 = gmshModelOccAddLine(P5, P1, -1, &ierr);
        ErrorGmsh(ierr);
        int l[] = {L1, L2, L3, L4, L5};
        int C2 = gmshModelOccAddCurveLoop(l,5, -1, &ierr);
        ErrorGmsh(ierr);
        int s[] = {C2};
        int S2 = gmshModelOccAddPlaneSurface(s,1, -1, &ierr);
        ErrorGmsh(ierr);
        int trou2[] = {2,S2};
        gmshModelOccCut(based,2,trou2,2,NULL,NULL,NULL,NULL,NULL,-1,1,1,&ierr); 
        ErrorGmsh(ierr);
    }


//
//  -2- Définition de la fonction callback pour la taille de référence
//      Synchronisation de OpenCascade avec gmsh
//      Génération du maillage (avec l'option Mesh.SaveAll :-)
                  
   
    geoSetSizeCallback(geoSize);      
    gmshModelOccSynchronize(&ierr);   
    gmshOptionSetNumber("Mesh.SaveAll", 1, &ierr);
    gmshModelMeshGenerate(2, &ierr);
    
       
//
//  Generation de quads :-)
//
//    gmshOptionSetNumber("Mesh.SaveAll", 1, &ierr);
//    gmshOptionSetNumber("Mesh.RecombineAll", 1, &ierr);
//    gmshOptionSetNumber("Mesh.Algorithm", 8, &ierr);  
//    gmshOptionSetNumber("Mesh.RecombinationAlgorithm", 1.0, &ierr);  
//    gmshModelGeoMeshSetRecombine(2,1,45,&ierr);  
//    gmshModelMeshGenerate(2, &ierr);  
   
 
//
//  Plot of Fltk
//
    gmshModelGeoSynchronize(&ierr);
    gmshFltkInitialize(&ierr);
    gmshFltkRun(&ierr); 
//
}

void geoMeshGenerateGeoFile(const char *filename) {
  femGeo *theGeometry = geoGetGeometry();
  int ierr;
  gmshOpen(filename, &ierr);
  ErrorGmsh(ierr);
  if (theGeometry->elementType == FEM_QUAD) {
    gmshOptionSetNumber("Mesh.SaveAll", 1, &ierr);
    gmshOptionSetNumber("Mesh.RecombineAll", 1, &ierr);
    gmshOptionSetNumber("Mesh.Algorithm", 8, &ierr);
    gmshOptionSetNumber("Mesh.RecombinationAlgorithm", 1.0, &ierr);
    gmshModelGeoMeshSetRecombine(2, 1, 45, &ierr);
    gmshModelMeshGenerate(2, &ierr);
  }

  if (theGeometry->elementType == FEM_TRIANGLE) {
    gmshOptionSetNumber("Mesh.SaveAll", 1, &ierr);
    gmshModelMeshGenerate(2, &ierr);
  }
  return;
}

void geoMeshGenerateMshFile(const char *filename) {
  int ierr;
  gmshOpen(filename, &ierr);
  ErrorGmsh(ierr);
  return;
}
