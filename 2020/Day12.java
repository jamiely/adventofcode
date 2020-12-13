import java.io.*;

public class Day12 {
    public static double getAnswerB(String filepath) throws IOException {
        try(BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            double x = 0;
            double y = 0;
            double waypointX = 10;
            double waypointY = 1;
            while(line != null) {
                char instruction = line.charAt(0);
                int arg1 = Integer.valueOf(line.substring(1, line.length()));

                switch(instruction) {
                    case 'E':
                        waypointX += arg1;
                        break;
                    case 'W':
                        waypointX -= arg1;
                        break;
                    case 'S':
                        waypointY -= arg1;
                        break;
                    case 'N':
                        waypointY += arg1;
                        break;
                    case 'L':
                        double[] newPtY = rotateInDir(waypointX, waypointY, arg1);
                        waypointX = newPtY[0];
                        waypointY = newPtY[1];
                        break;
                    case 'R':
                        double[] newPtR = rotateInDir(waypointX, waypointY, -arg1);
                        waypointX = newPtR[0];
                        waypointY = newPtR[1];
                        break;
                    case 'F':
                        x += waypointX * arg1;
                        y += waypointY * arg1;
                        break;
                }

                System.out.println(String.format("Instruction %s (%f, %f) waypoint (%f, %f)", line, x, y, waypointX, waypointY));

                line = reader.readLine();
            }
            return Math.abs(x) + Math.abs(y);
        }
    }
    static double[] rotateInDir(double x, double y, double dir) {
        double rads = Math.toRadians(dir);
        double sin = Math.sin(rads);
        double cos = Math.cos(rads);
        double newX = x * cos - y * sin;
        double newY = x * sin + y * cos;

        return new double[]{newX, newY};
    }
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
            "A. the Manhattan distance between the ships ending location and the ship's starting position is %f",
            getAnswerA(args[0])
        ));
        System.out.println(String.format(
            "B. the Manhattan distance between the ships ending location and the ship's starting position is %f",
            getAnswerB(args[0])
        ));
    }
    
}
