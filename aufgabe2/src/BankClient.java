import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.channels.FileLock;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.Random;

class BankClient {
    private final boolean log = false;
    private int numTransactions;

    private int numAccounts;
    public BankClient(int numTransactions, int numAccounts) {
        this.numTransactions = numTransactions;
        this.numAccounts = numAccounts;
        this.init();
    }

    private void init(){

        try{
            String pipePathString = "data_pipe";
            Path pipePath = FileSystems.getDefault().getPath(pipePathString);
            while(!Files.exists(pipePath)) {
                // waiting for pipe creation
                Thread.sleep(600);
            }

            FileChannel dataPipeChannel = FileChannel.open(pipePath, StandardOpenOption.WRITE);

            this.startTransactions(dataPipeChannel);

            dataPipeChannel.close();

        } catch (IOException | InterruptedException e){
            System.err.println("An error occured when trying to send a transfer request.");
            e.printStackTrace();
        }
    }

    private void startTransactions(FileChannel dataPipeChannel)
            throws IOException, InterruptedException {
        Random rand = new Random();

        final int transactionsPerIteration = 128;
        final int bufferSize = transactionsPerIteration*4*3;
        int counter;
        int numIterations = (int) Math.ceil(numTransactions / transactionsPerIteration);
        ByteBuffer buffer = ByteBuffer.allocate(bufferSize);
        for (int i = 0; i < numIterations; i++) {
            counter = 0;
            // Reset the position to the beginning of the ByteBuffer
            buffer.clear();
            while(counter < transactionsPerIteration) {
                int from = rand.nextInt(numAccounts);
                int to = rand.nextInt(numAccounts);
                int amount = rand.nextInt(100) + 1; // Zufälliger Betrag zwischen 1 und 100

                buffer.putInt(from);
                buffer.putInt(to);
                buffer.putInt(amount);

                counter++;
            }
            buffer.flip();
            int written_bytes = dataPipeChannel.write(buffer);
            //System.out.println("Written " + written_bytes + " bytes.");
        }

        // LAST ITERATION : BUFFER IS POSSIBLY NOT COMPLETELY FILLED

        int numSubIterationsInLastIteration = numTransactions % transactionsPerIteration;
        counter = 0;
        // Reset the position to the beginning of the ByteBuffer
        buffer.clear();
        while(counter < numSubIterationsInLastIteration) {
            int from = rand.nextInt(numAccounts);
            int to = rand.nextInt(numAccounts);
            int amount = rand.nextInt(100) + 1; // Zufälliger Betrag zwischen 1 und 100

            buffer.putInt(from);
            buffer.putInt(to);
            buffer.putInt(amount);

            counter++;
        }
        buffer.flip();
        int written_bytes = dataPipeChannel.write(buffer);
        //System.out.println("Client finished sending " + transactionsCounter + " transactions.");
    }

    public static void main(String[] args) {
        // Lesen der Umgebungsvariablen oder Standardwerte verwenden
        int numAccounts = Integer.parseInt(System.getenv("NUM_ACCOUNTS") != null ? System.getenv("NUM_ACCOUNTS") : "1000");
        int transactionsPerClient = Integer.parseInt(System.getenv("TRANSACTIONS_PER_CLIENT") != null ? System.getenv("TRANSACTIONS_PER_CLIENT") : "1000");

        BankClient client = new BankClient(transactionsPerClient, numAccounts);

    }
}