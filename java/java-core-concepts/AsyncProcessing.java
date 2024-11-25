// AsyncProgramming.java

/*
 * Asynchronous Programming in Java.
 * Java provides multithreading and asynchronous capabilities through Thread, ExecutorService, and CompletableFuture.
 * Key Concepts:
 * 1. **Threads and Thread Pools**: Threads are lightweight processes, and thread pools manage multiple threads efficiently.
 * 2. **Synchronization and Locks**: Prevent data inconsistency when multiple threads access shared resources.
 * 3. **CompletableFuture**: A modern API for non-blocking async programming.
 *
 * Key Differences from Python:
 * - Python uses `await` with an event loop (single-threaded concurrency).
 * - Java uses native threads managed by the OS, supporting true parallelism.
 */

import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.CompletableFuture;

// --- Basic Threads ---
class BasicThreadExample {
    public static void main(String[] args) {
        Thread t1 = new Thread(() -> System.out.println("Thread 1 is running"));
        Thread t2 = new Thread(() -> System.out.println("Thread 2 is running"));

        // Starting threads
        t1.start();
        t2.start();
        // Note: start() creates a new thread. If run() is called directly, it runs in the main thread.
    }
}



// --- Synchronization and Monitors ---
/*
 * Every Java object has an **intrinsic monitor lock**.
 * The `synchronized` keyword ensures that a thread must acquire the object's lock before executing a critical section.
 *
 * Scenarios:
 * 1. synchronized(this): Locks the current object instance.
 * 2. synchronized(ClassName.class): Locks the class's monitor, affecting all instances of the class.
 *
 * Example:
 * - If a thread holds a lock on an object, other threads attempting to acquire the same lock are blocked.
 */

class Counter {
    private int count = 0;

    // Locks the current instance (this) for thread-safe access.
    public synchronized void increment() {
        count++;
    }

    public int getCount() {
        return count;
    }
}

class SyncExample {
    public static void main(String[] args) throws InterruptedException {
        Counter counter = new Counter();

        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) counter.increment();
        });
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) counter.increment();
        });

        t1.start();
        t2.start();

        // Wait for threads to finish using join().
        t1.join();
        t2.join();

        System.out.println("Final Count: " + counter.getCount());
    }
}



// --- ReentrantLock ---
/*
 * **ReentrantLock** provides finer-grained control over locks compared to `synchronized`.
 * Advantages:
 * 1. Ability to try acquiring a lock (`tryLock`).
 * 2. Explicit locking/unlocking with more control.
 * 3. Avoid deadlocks with timed locks.
 */

class ReentrantLockExample {
    private final ReentrantLock lock = new ReentrantLock();

    public void performTask() {
        if (lock.tryLock()) { // Attempts to acquire the lock immediately.
            try {
                System.out.println(Thread.currentThread().getName() + " acquired the lock.");
            } finally {
                lock.unlock(); // Always release the lock to avoid deadlocks.
            }
        } else {
            System.out.println(Thread.currentThread().getName() + " could not acquire the lock.");
        }
    }
}




// --- ExecutorService ---
/*
 * ExecutorService simplifies thread management.
 * Key Methods:
 * - execute(): Submits a task for execution.
 * - submit(): Similar to execute, but returns a Future for task results.
 */


class ThreadPoolExample {
    public static void main(String[] args) {
        ExecutorService executor = Executors.newFixedThreadPool(2);

        Runnable task = () -> System.out.println(Thread.currentThread().getName() + " is executing a task");

        executor.execute(task);
        executor.execute(task);

        executor.shutdown(); // Gracefully shuts down the thread pool.
    }
}




// --- CompletableFuture ---
/*
 * CompletableFuture supports non-blocking, async workflows.
 * Great for non-blocking waiting for threads finish their work.
 * The key part here is that CompletableFuture allows you to decouple tasks.
 * Even if they run in the same thread, the calling thread can continue executing while waiting for the result.
 * This is a form of asynchronous behavior.
 * We can provide an ExecutorService to run the tasks in coordination of a managed thread pool.
 *
 * Key Methods:
 * - runAsync(): Executes a task asynchronously in a different thread.
 * - supplyAsync(): Executes a task that returns a value in  different thread.
 * - allOf(): Waits for multiple CompletableFutures to complete without blocking.
 * - join(): Waits for the result of a CompletableFuture, with block the execution flow.
 */

class CompletableFutureExample {
    public static void main(String[] args) {
        CompletableFuture<Void> future1 = CompletableFuture.runAsync(() -> {
            System.out.println("Task 1 running");
        });

        CompletableFuture<Void> future2 = CompletableFuture.runAsync(() -> {
            System.out.println("Task 2 running");
        });

        CompletableFuture<Void> combined = CompletableFuture.allOf(future1, future2);

        // Ensures both tasks complete before moving forward.
        combined.join(); // Blocks until all futures are complete.

        System.out.println("All tasks completed!");
    }
}
