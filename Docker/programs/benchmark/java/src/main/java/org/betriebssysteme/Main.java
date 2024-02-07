package org.betriebssysteme;

public class Main {

    static int numAccounts; // Anzahl der Konten
    static int numClients; // Anzahl der Clients
    static int numTransfersPerClient; // Anzahl der Anfragen pro Client
    static String seed; // Seed zur Generierung der Zufallszahlen
    static int minStartBalance; // Minimale Startbetrag für Konten
    static int maxStartBalance; // Maximale Startbetrag für Konten
    static int minTransferAmount; // Minimaler Betrag pro Überweisung
    static int maxTransferAmount; // Maximaler Betrag pro Überweisung


    public static void main(String[] args) {
        if(args.length != 8){
            System.out.println("Wrong number of arguments!");
            System.exit(1);
        }


        numAccounts = Integer.parseInt(args[1]); // Anzahl der Konten
        numClients = Integer.parseInt(args[6]); // Anzahl der Clients
        numTransfersPerClient = Integer.parseInt(args[7]); // Anzahl der Anfragen pro Client
        seed = args[0]; // Seed zur Generierung der Zufallszahlen
        minStartBalance = Integer.parseInt(args[2]); // Minimale Startbetrag für Konten
        maxStartBalance = Integer.parseInt(args[3]); // Maximale Startbetrag für Konten
        minTransferAmount = Integer.parseInt(args[4]); // Minimaler Betrag pro Überweisung
        maxTransferAmount = Integer.parseInt(args[5]); // Maximaler Betrag pro Überweisung


        LCG randomSeedGenerator = new LCG(seed);

        BankServer server = new BankServer(numAccounts, randomSeedGenerator.getNextNumber(1000), minStartBalance, maxStartBalance);

        Thread serverThread = new Thread(server);
        serverThread.start();

        Thread[] clientThreads = new Thread[numClients];
        for (int i = 0; i < clientThreads.length; i++) {
            BankClient client = new BankClient(server, numTransfersPerClient, randomSeedGenerator.getNextNumber(1000), numAccounts, minTransferAmount, maxTransferAmount);
            clientThreads[i] = new Thread(client);
            clientThreads[i].start();
        }

        for (Thread clientThread : clientThreads) {
            try {
                clientThread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

	serverThread.interrupt();
        System.out.println(server.accountToString());
        
    }
}
