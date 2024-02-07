package org.betriebssysteme;

class LCG {
    private long state;
    private final int a = 1664525;
    private final int c = 1013904223;
    private final long m = 1294967296;

    public LCG(String seed) {
        this.state = hashSeed(seed);
    }

    private long hashSeed(String inputStr) {
        int prime = 31;
        long checksum = 0;

        for (char ch : inputStr.toCharArray()) {
            checksum = (checksum * prime + (int) ch) & 0xFFFFFFFFL;
        }
        return checksum;
    }

    private long next() {
        state = (a * state + c) % m;
        return state;
    }

    public double random() {
        return (double) next() / m;
    }

    public int getNextNumber(int n) {
        return  (int)Math.round(Math.floor(random() * n));
    }

    public int getNextNumberBetween(int n, int m) {
        return  (int)Math.round(Math.floor(random() * (m - n)) + n);
    }
}