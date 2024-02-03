import java.io.Serializable;

class TransferRequest implements Serializable {
    public int from;
    public int to;
    public int amount;

    public TransferRequest(int from, int to, int amount) {
        this.from = from;
        this.to = to;
        this.amount = amount;
    }

    @Override
    public String toString(){
        return "TransferRequest from " + from + " to " + to + " (" + amount +" euro)";
    }
}