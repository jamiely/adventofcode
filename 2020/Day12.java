import java.io.*;

public class Day12 {
    public static double getAnswerA(String filepath) throws IOException {
        try(BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            double x = 0;
            double y = 0;
            int direction = 0;
            while(line != null) {
                char instruction = line.charAt(0);
                int arg1 = Integer.valueOf(line.substring(1, line.length()));

                switch(instruction) {
                    case 'E':
                        x += arg1;
                        break;
                    case 'W':
                        x -= arg1;
                        break;
                    case 'S':
                        y -= arg1;
                        break;
                    case 'N':
                        y += arg1;
                        break;
                    case 'L':
                        direction += arg1;
                        break;
                    case 'R':
                        direction -= arg1;
                        break;
                    case 'F':
                        double rads = Math.toRadians(direction);
                        double sin = Math.sin(rads);
                        double cos = Math.cos(rads);
                        double dy = sin * arg1;
                        double dx = cos * arg1;

                        x += dx;
                        y += dy;
                        System.out.println(String.format("dx=%f dy=%f", dx, dy));
                        break;
                }

                System.out.println(String.format("Instruction %s (%f, %f) dir=%d", line, x, y, direction));

                line = reader.readLine();
            }
            return Math.abs(x) + Math.abs(y);
        }
    }
    public static void main(String[] args) throws IOException {
        System.out.println(String.format(
            "the Manhattan distance between the ships ending location and the ship's starting position is %f",
            getAnswerA(args[0])
        ));
    }
    
}
