class TransactionProcessor {
    private final Map<String, Account> accounts = new HashMap<>();
    private final ExecutorService executor = Executors.newFixedThreadPool(4);

    public void addAccount(String accountId, double initialBalance) {
        accounts.put(accountId, new Account(initialBalance));
    }

    public CompletableFuture<Void> processDeposit(String accountId, double amount) {
        return CompletableFuture.runAsync(() -> {
            Account account = accounts.get(accountId);
            if (account != null) {
                account.deposit(amount);
            } else {
                System.out.println("Account not found: " + accountId);
            }
        }, executor);
    }

    public CompletableFuture<Void> processWithdrawal(String accountId, double amount) {
        return CompletableFuture.runAsync(() -> {
            Account account = accounts.get(accountId);
            if (account != null) {
                try {
                    account.withdraw(amount);
                } catch (InsufficientFundsException e) {
                    System.out.println("Error processing withdrawal: " + e.getMessage());
                }
            } else {
                System.out.println("Account not found: " + accountId);
            }
        }, executor);
    }

    public void shutdown() {
        executor.shutdown();
    }

    public double getAccountBalance(String accountId) {
        Account account = accounts.get(accountId);
        return account != null ? account.getBalance() : 0;
    }
}