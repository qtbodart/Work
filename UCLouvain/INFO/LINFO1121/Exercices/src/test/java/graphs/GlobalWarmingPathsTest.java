package graphs;

import org.javagrader.ConditionalOrderingExtension;
import org.javagrader.Grade;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.junit.jupiter.api.Assertions.assertTrue;


import java.util.List;
import java.util.Random;

@ExtendWith(ConditionalOrderingExtension.class)
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
@Grade
public class GlobalWarmingPathsTest {

    final int [] seeds = new int[]{0,7,13};

    Random rand = new Random(seeds[new java.util.Random().nextInt(3)]);

    public int [][] getSimpleMatrix() {
        int[][] matrix = new int[][]{
                {0, 0, 0, 0, 0, 1, 1, 1, 0, 0},
                {0, 1, 0, 0, 0, 1, 0, 1, 1, 1},
                {0, 0, 0, 0, 0, 1, 0, 0, 1, 0},
                {0, 1, 0, 0, 0, 1, 0, 1, 1, 0},
                {0, 1, 0, 0, 0, 1, 1, 1, 1, 1},
                {0, 1, 0, 0, 0, 0, 0, 0, 0, 0},
                {0, 0, 1, 1, 1, 0, 0, 0, 0, 0},
                {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
        };
        return matrix;
    }

    public int [][] getExamMatrix() {
        int [][] tab = new int[][] {{1,3,3,1,3},
                {4,2,2,4,5},
                {4,4,1,4,2},
                {1,4,2,3,6},
                {1,1,1,6,3}};
        return tab;
    }


    @Test
    @Grade(value= 1)
    @Order(1)
    public void testShortestPathExam() {
        List<GlobalWarmingPaths.Point> path = new GlobalWarmingPaths(getExamMatrix(), 3).shortestPath(new GlobalWarmingPaths.Point(1, 0), new GlobalWarmingPaths.Point(3, 1));
        assertTrue( path != null && path.size() == 4 && validPath(getExamMatrix(),3,point(1,0),point(3,1),path) );
    }


    public int [][] getRandomMatrix(int n,int bound) {
        int[][] matrix = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                matrix[i][j] = rand.nextInt(bound);
            }
        }
        return matrix;
    }


    public static GlobalWarmingPaths.Point point(int x, int y) {
        return new GlobalWarmingPaths.Point(x,y);
    }

    @Test
    @Grade(value= 1)
    @Order(2)
    public void testSimpleAll() {
        assertTrue(simpleAll());
    }

    public boolean simpleAll() {
        int [][] matrix = getSimpleMatrix();
        GlobalWarmingPaths warming = new GlobalWarmingPaths(matrix,0);

        List<GlobalWarmingPaths.Point> path1 = warming.shortestPath(point(1,1),point(1,1));

        if (!validPath(matrix, 0, point(1, 1), point(1, 1), path1)) {
            return false;
        }

        if (warming.shortestPath(point(9, 9), point(9, 9)) != null) {
            if (!warming.shortestPath(point(9, 9), point(9, 9)).isEmpty()) {
                return false;
            }
        }

        if (warming.shortestPath(point(0, 9), point(9, 9)) != null) {
            if (!warming.shortestPath(point(0, 9), point(9, 9)).isEmpty()) {
                return false;
            }
        }

        List<GlobalWarmingPaths.Point> path2 = warming.shortestPath(point(4, 5), point(1, 7));
        if (!validPath(matrix, 0, point(4, 5), point(1, 7), path2)) {
            return false;
        }

        if (path2.size() != 8) {
            System.out.println(path2.size());
            return false;
        }
        return true;
    }



    public boolean validPath(int [][] matrix, int level, GlobalWarmingPaths.Point p1, GlobalWarmingPaths.Point p2, List<GlobalWarmingPaths.Point> path) {
        for (GlobalWarmingPaths.Point p: path) {
            if (matrix[p.getX()][p.getY()] <= level) return false;
        }
        for (int i = 0; i < path.size()-1; i++) {
            if (!neighbors(path.get(i),path.get(i+1))) {
                return false;
            }
        }
        if (matrix[p1.getX()][p1.getY()] <= level && !path.isEmpty()) return false;
        if (matrix[p2.getX()][p2.getY()] <= level && !path.isEmpty()) return false;

        return !path.isEmpty() && path.get(0).equals(p1) && path.get(path.size()-1).equals(p2);
    }


    public boolean neighbors(GlobalWarmingPaths.Point p1,GlobalWarmingPaths.Point p2) {
        return Math.abs(p1.getX() - p2.getX()) + Math.abs(p1.getY() - p2.getY()) == 1;
    }


}

