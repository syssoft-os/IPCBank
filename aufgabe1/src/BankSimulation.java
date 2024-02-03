public class BankSimulation {
    public static void main(String[] args) {

        long startTime = System.currentTimeMillis();
        // Lesen der Umgebungsvariablen oder Standardwerte verwenden
        int numAccounts = Integer.parseInt(System.getenv("NUM_ACCOUNTS") != null ? System.getenv("NUM_ACCOUNTS") : "1000");
        int numClients = Integer.parseInt(System.getenv("NUM_CLIENTS") != null ? System.getenv("NUM_CLIENTS") : "100");
        int transactionsPerClient = Integer.parseInt(System.getenv("TRANSACTIONS_PER_CLIENT") != null ? System.getenv("TRANSACTIONS_PER_CLIENT") : "1000");

        BankServer server = new BankServer(numAccounts);
        server.start();
        server.printSum();

        BankClient[] clients = new BankClient[numClients];
        for (int i = 0; i < numClients; i++) {
            clients[i] = new BankClient(server, transactionsPerClient, numAccounts);
            clients[i].start();
        }

        try {
            for (int i = 0; i < numClients; i++) {
                clients[i].join();
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        long endTime = System.currentTimeMillis();
        long totalTime = endTime - startTime;
        System.out.println("Total Execution Time: " + totalTime + " milliseconds");
        server.printSum();

    }
}
