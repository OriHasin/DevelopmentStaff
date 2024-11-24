// Generics.java

/*
 * Generics in Java
 * Generics add type safety to classes and methods, allowing reusability.
 *
 * Key Concepts:
 * - Bounded Types: Restrict type parameters using `extends` or `super`.
 * - Wildcards: Use `?`, `? extends T`, `? super T` for flexible type handling.
 * - Type Erasure: Type parameters are replaced with their bounds (or Object) at runtime.
 */



// --- Custom Generic Class ---
class Box<T> {
    private T value;

    public Box(T value) {
        this.value = value;
    }

    public T getValue() {
        return value;
    }
}



// --- Bounded Types ---
class Utils {
    public static <T extends Comparable<T>> T findMax(T a, T b) {
        return a.compareTo(b) > 0 ? a : b;
    }
}

class GenericsExample {
    public static void main(String[] args) {
        Box<Integer> intBox = new Box<>(42);
        System.out.println("Boxed Value: " + intBox.getValue());

        System.out.println("Max Value: " + Utils.findMax(10, 20));
    }
}
