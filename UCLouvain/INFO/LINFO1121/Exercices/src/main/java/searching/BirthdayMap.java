package searching;

import java.util.ArrayList;
import java.util.List;
import java.util.SortedMap;
import java.util.TreeMap;


/**
 * This class represents a map that maps birthdays to persons.
 * Your map should be able to handle multiple people born on the same day.
 * Your map should be able to query efficiently for
 * - people born on a specific date and
 * - people born in a specific year.
 * You can assume that the input is valid for dates (format 'YYYY-MM-DD') and years (format 'YYYY').
 * The years do not start with 0.
 * The time complexity of the operations should be in O(log n + k)
 * where k is the number of people born on the specified date or year
 * and n is the number of different birthdays in the map.
 *
 * Complete the class to make the tests in BirthdayMapTest pass.
 * Do not modify the signature of existing methods.
 * Feel free to add instance variables and new methods.
 * Also feel free to import and use existing java classes.
 */
class BirthdayMap {
    // Hint: feel free to use existing java classes from Java such as java.util.TreeMap

    BirthdayMap() {
        // TODO
    }

    /**
     * Adds a person to the map.
     * The key is the birthday of the person.
     * The time complexity of the method should be in O(log n)
     * where n is the number of different birthdays in the map.
     * @param person
     */
    void addPerson(Person person) {
        // TODO
    }

    /**
     * The function returns a list of Person objects in the map born on the specified date.
     * @param date a String input representing the date (in 'YYYY-MM-DD' format)
     *             for which we want to retrieve people born on.
     * @return A list of Person objects representing all people born on the specified date.
     *          An empty list is returned if no entries are found for the specified date.
     */
    List<Person> getPeopleBornOnDate(String date) {
        // TODO
         return null;
    }


    /**
     * The function returns a consolidated list of Person objects
     * in the map born in the specified year.
     * @param year A String input representing the year (in 'YYYY' format)
     *             for which we want to retrieve people born in.
     * @return A consolidated list of Person objects representing all people born in the specified year.
     *         If no entries are found for the specified year, the function returns an empty list.
     */
    List<Person> getPeopleBornInYear(String year) {
        // TODO
         return null;
    }


    /**
     * Example usage of the BirthdayMap class, feel free to modify.
     */
    public static void main(String[] args) {
        Person alice = new Person("Alice", "2000-07-17");
        Person bob = new Person("Bob", "2000-08-15");
        Person charlie = new Person("Charlie", "2001-06-06");

        BirthdayMap map = new BirthdayMap();
        map.addPerson(alice);
        map.addPerson(bob);
        map.addPerson(charlie);

        System.out.println(map.getPeopleBornOnDate("2000-07-17"));
        System.out.println(map.getPeopleBornInYear("2000"));
    }

}

class Person {
    String name;
    String birthday; // format: YYYY-MM-DD

    Person(String name, String birthday) {
        this.name = name;
        this.birthday = birthday;
    }

    @Override
    public String toString() {
        return this.name;
    }
}

