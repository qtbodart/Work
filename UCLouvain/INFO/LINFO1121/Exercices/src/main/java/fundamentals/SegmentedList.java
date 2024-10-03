package fundamentals;

import java.util.*;

/**
 * Author Pierre Schaus
 *
 * The SegmentedList is a linear structure that consists of several segments (or groups) of elements,
 * where each segment can have its own size.
 * It is like a list of lists, but the user interacts with it as a single linear sequence.
 * The iterator will need to traverse each segment in order, element by element,
 * seamlessly presenting the entire structure as a single flat sequence.
 *
 * Be careful with the iterator, it should implement the fail-fast behavior.
 * A fail-fast iterator detects illegal concurrent modification during iteration (see the tests).
 *
 * Example:
 *
 *         SegmentedList<Integer> segmentedList = create();
 *
 *         // Add segments
 *         List<Integer> segment1 = new ArrayList<>();
 *         segment1.add(1); segment1.add(2); segment1.add(3);
 *         segmentedList.addSegment(segment1); // add [1,2,3]
 *
 *         List<Integer> segment2 = new ArrayList<>();
 *         segment2.add(4); segment2.add(5);
 *         segmentedList.addSegment(segment2); // add [4,5]
 *
 *         List<Integer> segment3 = new ArrayList<>();
 *         segment3.add(6); segment3.add(7); segment3.add(8); segment3.add(9);
 *         segmentedList.addSegment(segment3); // add [6,7,8,9]
 *
 *         segmentedList.removeSegment(1); // remove [4,5], the segment in second position
 *
 *         // Iterate through the SegmentedList that is elements 1,2,3,6,7,8,9
 *         for (Integer value : segmentedList) {
 *             System.out.println(value);
 *         }
 *
 *         // Example of using get()
 *         System.out.println("Element at global index 4: " + segmentedList.get(4)); // Should print 5
 *
 * @param <T>
 */
public interface SegmentedList<T> extends Iterable<T> {

    // Add a new segment (list) to the SegmentedList.
    void addSegment(List<T> segment);

    // Remove a segment by its index.
    void removeSegment(int index);

    // Get the total size of the segmented list (across all segments).
    int size();

    // Retrieve an element at a global index (spanning all segments).
    T get(int globalIndex);

    // Static method inside the interface
    static <T> SegmentedList<T> create() {
        return new SegmentedListImpl<>();
    }

}

class SegmentedListImpl<T> implements SegmentedList<T> {

    int n_segment;
    int n_elements;
    int nOp;
    ArrayList<ArrayList<T>> segments;

    public SegmentedListImpl() {
        n_segment = 0;
        n_elements = 0;
        nOp = 0;
        segments = new ArrayList<>();
    }


    // Add a new segment (list) to the SegmentedList.
    public void addSegment(List<T> segment) {
        segments.add(new ArrayList<>(segment));
        n_segment++;
        n_elements += segment.size();
        nOp++;
    }

    // Remove a segment by its index.
    public void removeSegment(int index) {
        n_elements -= segments.get(index).size();
        segments.remove(index);
        n_segment--;
        nOp++;
    }

    // Get the total size of the segmented list (across all segments).
    public int size() {
         return n_elements;
    }

    // Retrieve an element at a global index (spanning all segments).
    public T get(int globalIndex) {
         int elements_checked = 0;
         for (List<T> segment : segments) {
             if (globalIndex < elements_checked+segment.size()) {
                 return segment.get(globalIndex-elements_checked);
             }
             elements_checked+=segment.size();
         }
         throw new IndexOutOfBoundsException();
    }



    // Return an iterator for the segmented list.
    @Override
    public Iterator<T> iterator() {
         return new SegListIterator<T>();
    }

    private class SegListIterator<T> implements Iterator<T> {

        private int elementIndex = 0;
        private int segmentIndex = 0;
        private int enOps;

        @Override
        public boolean hasNext() {
            return true;
        }

        @Override
        public T next() {
            return null;
        }

        @Override
        public void remove() {
            Iterator.super.remove();
        }
    }


}
