public class Main {
    public static void main(String[] args) throws InterruptedException {
        // Initialize the TransactionProcessor and create some accounts
        TransactionProcessor processor = new TransactionProcessor();
        processor.addAccount("user1", 1000);
        processor.addAccount("user2", 500);

        // Submit multiple asynchronous transactions (both deposits and withdrawals)
        List<CompletableFuture<Void>> futures = new ArrayList<>();
        futures.add(processor.processDeposit("user1", 200));
        futures.add(processor.processWithdrawal("user1", 150));
        futures.add(processor.processDeposit("user2", 100));
        futures.add(processor.processWithdrawal("user2", 700)); // This will fail due to insufficient funds

        // Wait for all transactions to finish
        CompletableFuture<Void> allOf = CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]));
        allOf.join();

        // Print final account balances
        System.out.println("Final balance of user1: " + processor.getAccountBalance("user1"));
        System.out.println("Final balance of user2: " + processor.getAccountBalance("user2"));

        // Shut down the executor service
        processor.shutdown();
    }
}