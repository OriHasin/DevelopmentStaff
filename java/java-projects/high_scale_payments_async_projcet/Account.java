package high_scale_payments_async_projcet;
class Account {
    private double balance;
    private final Object lock = new Object(); // Lock for synchronizing account balance changes

    public Account(double initialBalance) {
        this.balance = initialBalance;
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        synchronized (lock) {
            balance += amount;
        }
    }

    public void withdraw(double amount) throws InsufficientFundsException {
        synchronized (lock) {
            if (amount > balance) {
                throw new InsufficientFundsException("Insufficient funds for withdrawal");
            }
            balance -= amount;
        }
    }
}