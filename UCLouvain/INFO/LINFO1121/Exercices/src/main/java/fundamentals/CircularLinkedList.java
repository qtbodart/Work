package fundamentals;

import java.util.ConcurrentModificationException;
import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * Author Pierre Schaus
 * _
 * We are interested in the implementation of a circular simply linked list,
 * i.e. a list for which the last position of the list refers, as the next position,
 * to the first position of the list.
 * _
 * The addition of a new element (enqueue method) is done at the end of the list and
 * the removal (remove method) is done at a particular index of the list.
 * _
 * A (single) reference to the end of the list (last) is necessary to perform all operations on this queue.
 * _
 * You are therefore asked to implement this circular simply linked list by completing the class see (TODO's)
 * Most important methods are:
 * _
 * - the enqueue to add an element;
 * - the remove method [The exception IndexOutOfBoundsException is thrown when the index value is not between 0 and size()-1];
 * - the iterator (ListIterator) used to browse the list in FIFO.
 *
 * @param <Item>
 */
public class CircularLinkedList<Item> implements Iterable<Item> {

    private long nOp = 0; // count the number of operations
    private int n;          // size of the stack
    private Node last;   // trailer of the list

    // helper linked list class
    private class Node {
        private Item item;
        private Node next;
    }

    public CircularLinkedList() {
        this.n = 0;
        this.last = null;
    }

    public boolean isEmpty() {
        return this.n == 0;
    }

    public int size() {
        return this.n;
    }

    private long nOp() {
        return this.nOp;
    }


    /**
     * Append an item at the end of the list
     * @param item the item to append
     */
    public void enqueue(Item item) {
        System.out.println("Enqueued " + item.toString());
        if (this.isEmpty()){
            last = new Node();
            last.item = item;
            last.next = last;
            n++;
            nOp++;
            return;
        }
        Node newNode = new Node();
        newNode.item = item;
        newNode.next = last.next;
        last.next = newNode;
        last = newNode;
        n++;
        nOp++;
    }

    /**
     * Removes the element at the specified position in this list.
     * Shifts any subsequent elements to the left (subtracts one from their indices).
     * Returns the element that was removed from the list.
     */
    public Item remove(int index) {
        if (this.isEmpty()){
            throw new NoSuchElementException();
        }
        if (index < 0 || index >= n){
            throw new IndexOutOfBoundsException();
        }

        Node cur = last;
        for (int i = 0; i < index; i++) {
            cur = cur.next;
        }
        Item output = cur.next.item;
        cur.next = cur.next.next;
        n--;
        nOp++;
        System.out.println("Removed " + output.toString());
        return output;
    }


    /**
     * Returns an iterator that iterates through the items in FIFO order.
     * @return an iterator that iterates through the items in FIFO order.
     */
    public Iterator<Item> iterator() {
        return new ListIterator();
    }

    /**
     * Implementation of an iterator that iterates through the items in FIFO order.
     * The iterator should implement a fail-fast strategy, that is ConcurrentModificationException
     * is thrown whenever the list is modified while iterating on it.
     * This can be achieved by counting the number of operations (nOp) in the list and
     * updating it everytime a method modifying the list is called.
     * Whenever it gets the next value (i.e. using next() method), and if it finds that the
     * nOp has been modified after this iterator has been created, it throws ConcurrentModificationException.
     */
    private class ListIterator implements Iterator<Item> {

        Node current = last.next;
        long oldnOp = nOp();


        @Override
        public boolean hasNext() {
            return true;
        }

        @Override
        public Item next() {
            if (!hasNext()){
                throw new NoSuchElementException();
            }
            if (oldnOp != nOp()) {
                throw new ConcurrentModificationException();
            }
            Item item = current.item;
            current = current.next;
            System.out.println("item " + item.toString() + " iterated");
            return item;
        }

    }

}