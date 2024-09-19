package graphs;

import java.util.LinkedList;
import java.util.Queue;


/**
 * Let's consider a forest represented as a 2D grid.
 * Each cell of the grid can be in one of three states:
 *
 * 0 representing an empty spot.
 * 1 representing a tree.
 * 2 representing a burning tree (indicating a wildfire).
 *
 * The fire spreads from a burning tree to its four neighboring cells (up, down, left, and right) if there's a tree there.
 * Each minute, the trees in the neighboring cells of burning tree catch on fire.
 *
 * Your task is to calculate how many minutes it would take for the fire to spread throughout the forest i.e. to burn all the trees.
 *
 * If there are trees that cannot be reached by the fire (for example, isolated trees with no adjacent burning trees),
 * we consider that the fire will never reach them and -1 is returned.
 *
 * The time-complexity of your algorithm must be O(n) with n the number of cells in the forest.
 */
public class Wildfire {

    static final int EMPTY = 0;
    static final int TREE = 1;
    static final int BURNING = 2;


    /**
     * This method calculates how many minutes it would take for the fire to spread throughout the forest.
     *
     * @param forest
     * @return the number of minutes it would take for the fire to spread throughout the forest,
     *         -1 if the forest cannot be completely burned.
     */
    public int burnForest(int [][] forest) {
        if (forest == null || forest.length == 0 || forest[0].length == 0) return -1;

        int rows = forest.length;
        int cols = forest[0].length;
        int minutes = 0;

        // Initializing a queue with burning trees and count total trees
        Queue<int[]> queue = new LinkedList<>();
        int totalTrees = 0;
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (forest[i][j] == TREE) {
                    totalTrees++;
                } else if (forest[i][j] == BURNING) {
                    queue.add(new int[]{i, j});
                }
            }
        }

        if (totalTrees == 0) return -1; // No trees to burn from the start

        int[][] directions = {{0,1},{-1,0},{0,-1},{1,0}};
        while (!queue.isEmpty()) {
            int size = queue.size();
            boolean fireSpread = false;

            for (int i = 0; i < size; i++) {
                int[] cur = queue.poll();
                int x = cur[0];
                int y = cur[1];

                for (int[] direction : directions) {
                    int newX = x + direction[0];
                    int newY = y + direction[1];

                    if (newX >= 0 && newX < rows && newY >= 0 && newY < cols && forest[newX][newY] == TREE) {
                        queue.add(new int[]{newX, newY});
                        totalTrees--;
                        fireSpread = true;
                    }
                }
            }
            if (fireSpread) {
                minutes++;
            }
        }
        return totalTrees == 0 ? minutes : -1;
    }
}