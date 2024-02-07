package org.betriebssysteme;

import java.util.Arrays;

public class BankServer extends Thread{
    private int[] accounts;
    private int[] accountsStartconfig;

    public BankServer(int numAccounts, int seed, int minStartBalance, int maxStartBalance) {
        accounts = new int[numAccounts];
        LCG randomGenerator = new LCG(String.valueOf(seed));

        // Initialisiere Konten mit positiven Zufallswerten
        for (int i = 0; i < numAccounts; i++) {
            accounts[i] = randomGenerator.getNextNumberBetween(minStartBalance, maxStartBalance);
        }

        // Copy startconfig
        accountsStartconfig = Arrays.copyOf(accounts, accounts.length);
    }

    public synchronized void transfer(int fromAccount, int toAccount, int amount) {
        // Überprüfe, ob die Kontonummern gültig sind
        if (isValidAccount(fromAccount) && isValidAccount(toAccount)) {
            if (accounts[fromAccount - 1] >= amount) {
                accounts[fromAccount - 1] -= amount;
                accounts[toAccount - 1] += amount;
            }
        }
    }

    private boolean isValidAccount(int accountNumber) {
        return accountNumber >= 1 && accountNumber <= accounts.length;
    }

    @Override
    public void run() {
        // Der Server reagiert nur auf Anfragen der Clients, initiert jedoch keine Überweisungen
    }


    public int countTotalMoney(int[] accounts){
        int totalMoney = 0;
        for (int i = 0; i < accounts.length; i++) {
            totalMoney += accounts[i];
        }
        return totalMoney;
    }


    public String accountToString(){
        int totalMoneyStart = countTotalMoney(accountsStartconfig);
        int totalMoneyEnd = countTotalMoney(accounts);

        String accountsToString = "[" + totalMoneyStart + ", " + totalMoneyEnd;

        for (int i = 0; i < accountsStartconfig.length; i++) {
            accountsToString += ", " + accountsStartconfig[i] + ", " + accounts[i];
        }

        accountsToString += "]";
        return accountsToString;
    }
}
