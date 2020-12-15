public class GCD {
    public static class Result {
        public long a;
        public long b;
        public long gcd;
        public long bezoutCoefficientS;
        public long bezoutCoefficientT;
        public long quotientS;
        public long quotientT;

        // https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
        public long getInverse() {
            return (bezoutCoefficientS % b + b) % b;
        }

        public String toString() {
            return String.format(
                "{%d(%d)+%d(%d) = gcd(%d,%d) = %d, quotientsByGCD=(%d,%d), inverse=%d",
                a, bezoutCoefficientS,
                b, bezoutCoefficientT,
                a, b,
                gcd,
                quotientS, quotientT,
                getInverse()
            );
        }
    }

    // https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#See_also
    public static Result extendedGCD(long a, long b) {
        long oldR = a, r = b;
        long oldS = 1, s = 0;
        long oldT = 0, t = 1;

        while(r != 0) {
            long quotient = oldR / r;
            long tmp = r;
            r = oldR - quotient * r;
            oldR = tmp;

            tmp = s;
            s = oldS - quotient * s;
            oldS = tmp;

            tmp = t;
            t = oldT - quotient * t;
            oldT = tmp;
        }


        Result result = new Result();
        result.a = a;
        result.b = b;
        result.gcd = oldR;
        result.bezoutCoefficientS = oldS;
        result.bezoutCoefficientT = oldT;
        result.quotientS = s;
        result.quotientT = t;

        return result;
    }

    public static void main(String[] args) {
        long a = Long.valueOf(args[0]);
        long b = Long.valueOf(args[1]);

        System.out.println(GCD.extendedGCD(a, b));
    }
}
