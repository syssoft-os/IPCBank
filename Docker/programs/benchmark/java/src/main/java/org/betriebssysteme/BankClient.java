package org.betriebssysteme;

public class BankClient extends Thread{

    private BankServer server;
    private int numTransfersPerClient;
    private LCG randomGenerator;
    private int numAccounts;
    private int minTransferAmount;
    private int maxTransferAmount;

    public BankClient(BankServer server, int numTransfersPerClient, int seed, int numAccounts, int minTransferAmount, int maxTransferAmount) {
        this.server = server;
        this.numTransfersPerClient = numTransfersPerClient;
        this.randomGenerator = new LCG(String.valueOf(seed));
        this.numAccounts = numAccounts;
        this.minTransferAmount = minTransferAmount;
        this.maxTransferAmount = maxTransferAmount;

    }

    @Override
    public void run() {
        for (int i = 0; i < numTransfersPerClient; i++) {
            int fromAccount = randomGenerator.getNextNumber(numAccounts) + 1;
            int toAccount = randomGenerator.getNextNumber(numAccounts) + 1;
            int amount = randomGenerator.getNextNumberBetween(minTransferAmount, maxTransferAmount);

            server.transfer(fromAccount, toAccount, amount);
        }
    }
}
