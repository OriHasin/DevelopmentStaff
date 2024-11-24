// Reflection.java

/*
 * Reflection in Java
 * Reflection allows runtime inspection and manipulation of classes, methods, fields, and constructors.
 *
 * Use Cases:
 * - Frameworks (e.g., Spring, Hibernate).
 * - Testing and dynamic invocation.
 *
 * Key Methods:
 * - getConstructor(): Gets a Constructor object.
 * - getMethod(): Retrieves public methods.
 * - getDeclaredMethod(): Retrieves methods, including private.
 * - setAccessible(true): Bypasses Java's access control checks.
 */



import java.lang.reflect.*;


class Person {
    private String name;

    public Person(String name) {
        this.name = name;
    }

    public String greet() {
        return "Hello, " + name;
    }

    private void secretMethod() {
        System.out.println("Secret Method Invoked!");
    }
}



class ReflectionExample {
    public static void main(String[] args) throws Exception {
        // Obtain the class object.
        Class<?> clazz = Person.class;

        // --- Access Constructor ---
        Constructor<?> constructor = clazz.getConstructor(String.class); // Retrieves public constructor.
        Person person = (Person) constructor.newInstance("John"); // Creates instance dynamically.

        // --- Access Public Method ---
        Method greetMethod = clazz.getMethod("greet");
        System.out.println("Result of greet(): " + greetMethod.invoke(person));

        // --- Access Private Method ---
        Method secretMethod = clazz.getDeclaredMethod("secretMethod");
        secretMethod.setAccessible(true); // Bypass visibility restrictions.
        secretMethod.invoke(person);

        // --- Access and Modify Field ---
        Field nameField = clazz.getDeclaredField("name");
        nameField.setAccessible(true); // Access private fields.
        nameField.set(person, "Jane"); // Modify field value.

        System.out.println("Modified greet(): " + greetMethod.invoke(person));
    }
}
