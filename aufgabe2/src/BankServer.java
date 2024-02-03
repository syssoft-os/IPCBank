import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.Random;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicInteger;

class BankServer {
    private final boolean fast = false;
    private final boolean log = false && !fast;
    private int[] accounts;
    private long totalTransactions;
    private TransferExecutor[] transferExecutors;
    private BlockingQueue<TransferRequest> transferQueue;

    public BankServer(int numAccounts, long totalTransactions) {
        this.totalTransactions = totalTransactions;
        accounts = new int[numAccounts];
        Random rand = new Random();
        transferQueue = new LinkedBlockingQueue<>();

        for (int i = 0; i < numAccounts; i++) {
            accounts[i] = rand.nextInt(1000) + 1; // Initialisierung mit positiven Zufallswerten
        }

        this.init();
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

    private void executeTransfer(TransferRequest request) {
        int from = request.from;
        int to = request.to;
        int amount = request.amount;

        synchronized (this){
            if (accounts[from] >= amount) {
                accounts[from] -= amount;
                accounts[to] += amount;
            }
        }
    }
    private void init(){

        try{
            String pipePathString = "data_pipe";
            Path pipePath = FileSystems.getDefault().getPath(pipePathString);

            if(!Files.exists(pipePath)){
                // Create a named pipe using the mkfifo command
                ProcessBuilder processBuilder = new ProcessBuilder("/bin/bash", "-c", "mkfifo " + pipePathString);
                Process process = processBuilder.start();

                // Wait for the process to complete
                int exitCode = process.waitFor();

                if (exitCode == 0) {
                    System.out.println("Named pipe created successfully");
                } else {
                    System.out.println("Error creating named pipe");
                }
            }

            this.printSum();

            FileChannel dataPipeChannel = FileChannel.open(pipePath, StandardOpenOption.READ);

            System.out.println("Server started, receiving transactions...");

            this.startTransferExecutors();

            this.receiveTransactions(dataPipeChannel);

            dataPipeChannel.close();

            for (TransferExecutor t : transferExecutors)
                t.join();

            System.out.println("Received and processed " + transactionsExecuted.get() + " transactions. Stopping.");
            this.printSum();

        } catch (IOException e){
            System.err.println("An error occured when trying to send a transfer request.");
            e.printStackTrace();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    private void startTransferExecutors () {
        final int numExecutors = 4;
        transferExecutors = new TransferExecutor[numExecutors];
        for(int i = 0; i < numExecutors; i++){
            transferExecutors[i] = new TransferExecutor();
            transferExecutors[i].start();
        }
    }

    private void receiveTransactions(FileChannel dataPipeChannel){
        try{
            final int numReceivers = 8;
            TransferReceiver[] transferReceivers = new TransferReceiver[numReceivers];
            for(int i = 0; i < numReceivers; i++){
                transferReceivers[i] = new TransferReceiver(dataPipeChannel);
                transferReceivers[i].start();
            }
            for(int i = 0; i < numReceivers; i++){
                transferReceivers[i].join();
            }
        } catch (Exception e){
            System.err.println("An error occured while trying to receive a transfer request.");
            e.printStackTrace();
        }
    }


    private AtomicInteger transactionsExecuted = new AtomicInteger(1);


    private class TransferReceiver extends Thread {
        private FileChannel pipe;
        public TransferReceiver(FileChannel pipe){
            this.pipe = pipe;
        }
        @Override
        public void run() {
            try {
                this.receive(pipe);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        private void receive(FileChannel dataPipeChannel) throws IOException {
            ByteBuffer buffer = ByteBuffer.allocate(1536); // 128 * 3 * 4 ( 128 transactions )
            while(transactionsExecuted.get() < totalTransactions){
                buffer.clear();

                // Read data from the named pipe
                int bytesRead = dataPipeChannel.read(buffer);

                if(bytesRead == -1){
                    continue;
                }
                buffer.flip();

                int bytesProcessed = 0;
                // System.out.println("Received " + bytesRead + " bytes.");
                while(bytesProcessed < bytesRead){
                    int from = buffer.getInt();
                    int to = buffer.getInt();
                    int amount = buffer.getInt();

                    transfer(from, to, amount);
                    bytesProcessed += 12;
                }
                // this.printSum();
            }
        }
    }

    private class TransferExecutor extends Thread{
        @Override
        public void run() {
            try {
                executeWithCounter();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        private void execute() throws InterruptedException {
            while (true) {
                TransferRequest request = transferQueue.take();
                executeTransfer(request);
            }
        }

        private void executeWithCounter () throws InterruptedException{
            while (true) {
                if(transactionsExecuted.incrementAndGet() > totalTransactions){
                    transactionsExecuted.decrementAndGet();
                    break;
                }
                TransferRequest request = transferQueue.take();
                executeTransfer(request);
            }
        }
    }


    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();
        // Lesen der Umgebungsvariablen oder Standardwerte verwenden
        int numAccounts = Integer.parseInt(System.getenv("NUM_ACCOUNTS") != null ? System.getenv("NUM_ACCOUNTS") : "1000");
        int numTransactions = Integer.parseInt(System.getenv("TRANSACTIONS_PER_CLIENT") != null ? System.getenv("TRANSACTIONS_PER_CLIENT") : "1000");
        int numClients = Integer.parseInt(System.getenv("NUM_CLIENTS") != null ? System.getenv("NUM_CLIENTS") : "1000");
        long totalTransactions = numTransactions * numClients;

        BankServer server = new BankServer(numAccounts, totalTransactions);

        long endTime = System.currentTimeMillis();
        long totalTime = endTime - startTime;
        System.out.println("Total Execution Time: " + totalTime + " milliseconds");
    }

}