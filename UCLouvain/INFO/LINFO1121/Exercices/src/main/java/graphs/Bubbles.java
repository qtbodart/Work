package graphs;

import java.util.*;

/**
 * Sophie and Marc want to reduce the bubbles
 * of contacts in the belgian population
 * to contain an evil virus (weird idea but
 * nevertheless inspired by a true belgian
 * story in 2020, don't ask ...).
 *
 * Help them!
 *
 * The Belgian government has imposed on the
 * population to limit the number of contacts, via "bubbles".
 *
 * The principle is quite simple:
 * If you have a (close) contact with someone,
 * You are then in his bubble, and he is in yours.
 *
 * Let's say the following contacts have taken place: [
 * [Alice, Bob], [Alice, Carol], [Carol, Alice], [Eve, Alice], [Alice, Frank],
 * [Bob, Carole], [Bob, Eve], [Bob, Frank], [Bob, Carole], [Eve, Frank]
 * ].
 *
 * Note that the contacts are two-by-two and
 * can occur several times. The order within
 * of a contact does not matter.
 *
 * The resulting bubbles are :
 *
 * - Alice's bubble = [Bob, Carol, Eve, Frank]
 * - Bob's bubble = [Bob, Carol, Eve, Frank]
 * - Bob's bubble = [Alice, Carol, Eve, Frank]
 * - Carole's bubble = [Alice, Bob]
 * - Frank's Bubble = [Alice, Bob, Eve]
 *
 * Note that the relationship is symmetric
 * (if Alice is in Bob's bubble, then Bob is in Alice's bubble)
 * but not transitive (if Bob is in Alice's bubble,
 * then Bob is in Alice's bubble)
 * and Carol is in Bob's bubble, Carol is
 * not necessarily in Alice's.
 *
 * Since at most n people can be in someone's
 * bubble without him being outlaw
 * given a list of contacts, select pairs of people
 * that you will forbid to meet, so that eventually
 * each person has a bubble of NO MORE than n people
 * (not counting themselves).
 * You need to ban AS FEW AS POSSIBLE (pairs of) people to meet.
 *
 * For example, if n = 3, in the example above,
 * you could forbid Alice and Carol to see each other, but also
 * Bob and Carol. This removes 2 links
 * (even though Alice and Carol appear twice in the contacts!).
 * But there is a better solution: prevent Alice and Bob
 * from seeing each other, which only removes one link.
 * Finding an algorithm that solves this problem is complex,
 * that's why we give you a rather vague idea of an algorithm:
 *
 * - As long as there are links between two bubbles
 *   each "too big", remove one of these links;
 * - Then, as long as there are bubbles that are too big,
 *   remove any link connected to one of these bubbles
 *   (removing is equivalent to "adding the link
 *   to the list of forbidden relationships")
 *
 * Implementing this algorithm as it is a bad idea.
 * Think of an optimal way to implement it in the
 * method {@code cleanBubbles}
 *
 * You CANNOT modify the `contacts` list directly (nor the lists inside)
 * If you try, you will receive an UnsupportedOperationException.
 *
 */
public class Bubbles {

    /**
     *
     * @param contacts
     * @param n the number of persons in the population ranges from 0 to n-1 (included)
     * @return a list of people you are going to forbid to see each other.
     *         There MUST NOT be any duplicates.
     *         The order doesn't matter, both within the
     *         ForbiddenRelation and in the list.
     */
    public static List<ForbiddenRelation> cleanBubbles(List<Contact> contacts, int n) {
//        System.out.println("Cleaning bubbles at order "+n);
//        System.out.println("Contact list given : ");
//        for (Contact contact : contacts) {
//            System.out.println(contact.a + " <-> " + contact.b);
//        }

        Map<String, Integer> degreeMap = new HashMap<>(); // Map of degrees of nodes, each node representing a person
        Map<String, Set<String>> adjacencyMap = new HashMap<>(); // Map of contacts between people
        Set<ForbiddenRelation> forbiddenRelations = new HashSet<>(); // Return value, set of forbidden relations, allows to exclude duplicates

        // FIRST IDEA :
        // Initializing @degreeMap and @adjacencyMap while ignoring "high-priority" links
        // "High-priority" links are contacts given in @contacts which would increment both nodes' degree over the limit @n
        // Example : n=4, degreeMap.get(contact.a) = 4, degreeMap.get(contact.b) = 5
        // Then @contact is considered a "high-priority" link and is automatically put into @forbiddenRelations.
        // DOES NOT WORK -> Commented the "early pruning" part
        for (Contact contact : contacts) {
            String personA = contact.a;
            String personB = contact.b;

            // Checks if this @contact hasn't been already processed
            if (adjacencyMap.getOrDefault(personA, new HashSet<>()).contains(personB) || adjacencyMap.getOrDefault(personB, new HashSet<>()).contains(personA)) {
                continue;
            }

            int degreeA = degreeMap.getOrDefault(personA, 0);
            int degreeB = degreeMap.getOrDefault(personB, 0);

//            if (degreeA >= n && degreeB >= n) {
//                forbiddenRelations.add(new ForbiddenRelation(personA, personB));
//            } else {
                degreeMap.put(personA, degreeA + 1);
                degreeMap.put(personB, degreeB + 1);

                adjacencyMap.computeIfAbsent(personA, k -> new HashSet<>()).add(personB);
                adjacencyMap.computeIfAbsent(personB, k -> new HashSet<>()).add(personA);
//            }
        }

        System.out.println("Adjacency map : ");
        for (Map.Entry<String, Set<String>> entry : adjacencyMap.entrySet()) {
            System.out.println(entry.getKey() + " : " + entry.getValue());
        }
        System.out.println("Degree map : ");
        for (Map.Entry<String, Integer> entry : degreeMap.entrySet()) {
            System.out.println(entry.getKey() + " : " + entry.getValue());
        }
        System.out.println("\n");

        boolean changed;
        do{
            changed = false;
            for (String person : degreeMap.keySet()) {
                int degree = degreeMap.get(person);
                Set<String> toRemove = adjacencyMap.get(person);

                System.out.println("Removing links from " + person + ":");

                if (degree <= n || toRemove == null) {
                    continue;
                }

                // Remove "high priority" links first
                Iterator<String> itPrio = toRemove.iterator();
                while (itPrio.hasNext() && degree > n) {
                    String neighbor = itPrio.next();
                    if (degreeMap.getOrDefault(neighbor, 0) > n) {
                        System.out.println("Removing (Priority)" + person + "<->" + neighbor);
                        itPrio.remove();
                        adjacencyMap.get(neighbor).remove(person);
                        forbiddenRelations.add(new ForbiddenRelation(person, neighbor));

                        degreeMap.put(person, degreeMap.get(person) - 1);
                        degreeMap.put(neighbor, degreeMap.get(neighbor) - 1);

                        degree = degreeMap.get(neighbor);
                        changed = true;
                    }
                }

                // Then remove other links
                Iterator<String> it = toRemove.iterator();
                while (it.hasNext() && degree > n) {
                    String neighbor = it.next();
                    System.out.println(person + "<->" + neighbor);
                    it.remove();
                    adjacencyMap.get(neighbor).remove(person);
                    forbiddenRelations.add(new ForbiddenRelation(person, neighbor));

                    degreeMap.put(person, degreeMap.get(person) - 1);
                    degreeMap.put(neighbor, degreeMap.get(neighbor) - 1);

                    degree = degreeMap.get(neighbor);
                    changed = true;
                }
            }
        }while (changed);

        System.out.println("\nForbidden Relations: ");
        for (ForbiddenRelation forbiddenRelation : forbiddenRelations) {
            System.out.println(forbiddenRelation.a + " <-> " + forbiddenRelation.b);
        }
        System.out.println("\n");
        return new ArrayList<>(forbiddenRelations);
    }
}



class Contact {
    public final String a, b;

    public Contact(String a, String b) {
        // We always force a < b for simplicity.
        if(a.compareTo(b) > 0) {
            this.b = a;
            this.a = b;
        }
        else {
            this.a = a;
            this.b = b;
        }
    }
}

class ForbiddenRelation implements Comparable<ForbiddenRelation> {
    public final String a, b;

    public ForbiddenRelation(String a, String b) {
        // We always force a < b for simplicity.
        if(a.compareTo(b) > 0) {
            this.b = a;
            this.a = b;
        }
        else {
            this.a = a;
            this.b = b;
        }
    }

    @Override
    public boolean equals(Object obj) {
        if(obj instanceof ForbiddenRelation)
            return a.equals(((ForbiddenRelation) obj).a) && b.equals(((ForbiddenRelation) obj).b);
        return false;
    }

    @Override
    public int compareTo(ForbiddenRelation o) {
        if(a.equals(o.a))
            return b.compareTo(o.b);
        return a.compareTo(o.a);
    }
}