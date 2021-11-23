import com.opencsv.CSVWriter;

import java.io.*;

class DeploymentTime {
    public static void main(String[] args) throws IOException {
        // Initialize the times to 0
        double avDeploymentTime = 0;
        double avgColdStartTime = 0;
        double avgWarmStartTime = 0;
        // fetch the current directory
        String spath = System.getProperty("user.dir");
        // directory which contains all the logs
        System.out.println(spath);
        String requiredPath = spath+"\\..\\cold_warm_start_AB";
        //create a .csv file for storing final deployment times
        File finalCsv = new File(requiredPath + "\\deployment_times_nano.csv");
        // create FileWriter object with file as parameter
        FileWriter outputfile = new FileWriter(finalCsv);
        // create CSVWriter object filewriter object as parameter
        CSVWriter writer = new CSVWriter(outputfile);
        // temporary array to store each applications value in required csv's format
        String[] temp;
        // Write the headers to the file.
        temp = new String[]{"AppName", "Nano"};
//        temp = new String[]{"AppName", "Nano", "Rpi"};
        writer.writeNext(temp);
//        temp[2] = "";
        //get all the subdirectories of present directory
        File dir = new File(requiredPath);
        System.out.println("dir :" +dir );//remove
        String childs[] = dir.list();
        for (String appname : childs) {
            //first column value is application name
            temp[0] = appname;
            // below directory contains all the required logs
//            String appsLogFilePath = appname + "\\NANO\\";
            // name of the required log file
            String appsLogFile = appname + "_ab_NANO_cold_warm_reading.csv";
            System.out.println(requiredPath +"\\"+ appname +"\\"+ appsLogFile);
//            File f = new File(requiredPath + "\\" + appsLogFilePath + appsLogFile);
            File f = new File(requiredPath +"\\"+ appname +"\\"+ appsLogFile);
            // Proceed if the logfile is present
            if (f.isFile()) {
                // line and splitBy to traverse the csv file
                String line = "";
                String splitBy = ",";
                try {
                    //parsing a CSV file into BufferedReader class constructor
                    BufferedReader br = new BufferedReader(new FileReader(f));
                    while ((line = br.readLine()) != null) {  //returns a Boolean value
                        String[] readings = line.split(splitBy);    // use comma as separator
                        // Calculate Deployment time
                        if (readings[0].equals("1")){
                            avgColdStartTime = Double.parseDouble(readings[1]);
                            System.out.println(temp[0]);
                            System.out.println(readings[0]);
                        } else
                        if(readings[0].equals("2") || readings[0].equals("3") || readings[0].equals("4") || readings[0].equals("5")){
                            avgWarmStartTime = avgWarmStartTime + Double.parseDouble(readings[1]);
                        }
                    }
                    System.out.println("avg cold start "+avgColdStartTime);
                    System.out.println("avg warm start " +avgWarmStartTime);
                    avDeploymentTime = avgColdStartTime - (avgWarmStartTime/4);
                    System.out.println("avg deploy time "+avDeploymentTime);
                    // Add the final values to the finalCSV file.
                    // TODO : add a check to see if its a nano log or a rpi log
                    temp[1] = Double.toString(avDeploymentTime);
//                    temp[2] = Double.toString(avDeploymentTime);
                    // resetting the values for the next iteration
                    avgColdStartTime = 0;
                    avgWarmStartTime =0;
                    avDeploymentTime = 0;
                    writer.writeNext(temp);
                    temp[1]="";
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }



//            // below directory contains all the required logs
//            // name of the required log file
//            appsLogFile = appname + "_ab_RPI_cold_warm_reading.csv";
//            System.out.println(requiredPath +"\\"+ appname +"\\"+ appsLogFile);
//            f = new File(requiredPath +"\\"+ appname +"\\"+ appsLogFile);
////            f = new File(requiredPath + "\\" + appsLogFilePath + appsLogFile);
//            // Proceed if the logfile is present
//            if (f.isFile()) {
//                // line and splitBy to traverse the csv file
//                String line = "";
//                String splitBy = ",";
//                try {
//                    //parsing a CSV file into BufferedReader class constructor
//                    BufferedReader br = new BufferedReader(new FileReader(f));
//                    while ((line = br.readLine()) != null) {  //returns a Boolean value
//                        String[] readings = line.split(splitBy);    // use comma as separator
//                        // Calculate Deployment time
//                        if (readings[0].equals("1")){
//                            avgColdStartTime = Double.parseDouble(readings[1]);
//                            System.out.println(temp[0]);
//                            System.out.println(readings[0]);
//                        } else
//                        if(readings[0].equals("2") || readings[0].equals("3") || readings[0].equals("4") || readings[0].equals("5")){
//                            System.out.println("val - "+readings[1]);
//                            avgWarmStartTime = avgWarmStartTime + Double.parseDouble(readings[1]);
//                        }
//                    }
//                    System.out.println("avg cold start "+avgColdStartTime);
//                    System.out.println("avg warm start " +avgWarmStartTime);
//                    avDeploymentTime = avgColdStartTime - (avgWarmStartTime/4);
//                    System.out.println("avg deploy time "+avDeploymentTime);
//                    // Add the final values to the finalCSV file.
//                    // TODO : add a check to see if its a nano log or a rpi log
//                    temp[2] = Double.toString(avDeploymentTime);
////                    temp[2] = Double.toString(avDeploymentTime);
//                    // resetting the values for the next iteration
//                    avgColdStartTime = 0;
//                    avgWarmStartTime =0;
//                    avDeploymentTime = 0;
//                    writer.writeNext(temp);
//                    temp[2]= "";
//                } catch (IOException e) {
//                    e.printStackTrace();
//                }
//            }
        }
        writer.close();
    }
}
