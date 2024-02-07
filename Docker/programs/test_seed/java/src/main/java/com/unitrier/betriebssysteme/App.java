package com.unitrier.betriebssysteme;
import java.util.Arrays;
import java.util.StringJoiner;


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


public class App {
    public static void main (String [] args) {
	if (args.length != 1) {
            System.out.println("Usage:  <seed>");
            System.exit(1);
	}

	String seedString = args[0];
	LCG generator = new LCG(seedString);
	long[] numbers = new long[5];

	for (int i = 0; i < 5; i++) {
            numbers[i] = generator.getNextNumber(100);
	}

	StringJoiner joiner = new StringJoiner(", ");
	for (long number : numbers) {
	    joiner.add(String.valueOf(number));
	}

	System.out.println(joiner.toString());
    }
}


