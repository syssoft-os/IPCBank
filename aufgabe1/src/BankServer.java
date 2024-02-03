import java.util.Random;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

class BankServer extends Thread {
    private int[] accounts;

    private BlockingQueue<TransferRequest> transferQueue;
    public BankServer(int numAccounts) {
        accounts = new int[numAccounts];
        Random rand = new Random();
        transferQueue = new LinkedBlockingQueue<>();

        for (int i = 0; i < numAccounts; i++) {
            accounts[i] = rand.nextInt(1000) + 1; // Initialisierung mit positiven Zufallswerten
        }
    }

    public void transfer(int from, int to, int amount) {
        transferQueue.offer(new TransferRequest(from, to, amount));
    }

    public void printAccountBalances() {
        for (int i = 0; i < accounts.length; i++) {
            System.out.println("Konto " + (i + 1) + ": " + accounts[i]);
        }
    }

    public void printSum() {
        int sum = 0;

        for (int i = 0; i < accounts.length; i++) {
            sum += accounts[i];
        }
        System.out.println("Total money: "+sum+ " euros");
    }

    @Override
    public void run() {
        try {
            while (true) {
                TransferRequest request = transferQueue.take();
                executeTransfer(request);
                //System.out.println(request);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private void executeTransfer(TransferRequest request) {
        int from = request.from;
        int to = request.to;
        int amount = request.amount;

        if (accounts[from] >= amount) {
            accounts[from] -= amount;
            accounts[to] += amount;
        }
    }

}