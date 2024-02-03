import java.util.Random;

class BankClient extends Thread {
    private BankServer server;
    private int numTransactions;

    private int numAccounts;
    public BankClient(BankServer server, int numTransactions, int numAccounts) {
        this.server = server;
        this.numTransactions = numTransactions;
        this.numAccounts = numAccounts;
    }

    @Override
    public void run() {
        Random rand = new Random();

        for (int i = 0; i < numTransactions; i++) {
            int from = rand.nextInt(numAccounts);
            int to = rand.nextInt(numAccounts);
            int amount = rand.nextInt(100) + 1; // Zufälliger Betrag zwischen 1 und 100

            server.transfer(from, to, amount);
        }
    }
}