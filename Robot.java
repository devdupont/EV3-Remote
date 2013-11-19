import java.io.*;
import java.net.*;
import lejos.nxt.Button;
import lejos.nxt.LCD;
import lejos.nxt.Motor;
import lejos.nxt.Sound;
import lejos.util.Delay;


/*
 * Michael duPont - flyinactor91.com
 * Generic robot client
 * Lejos 0.4.0-alpha running on EV3
 * 
 * Connects to controller via socket
 * Commands separated by ';'
 * Available Commands:
 * 		Forward: 	F distance<int> (serial<def=Y /N>)
 * 		Backward: 	B distance<int> (serial<def=Y /N>)
 * 		Left:		L degree<int> (serial< def=Y/N>)
 * 		Right:		R degree<int> (serial< def=Y/N>)
 * 		Pause:		P duration-ms<int>
 * 		LED Disp:	LED pattern<int 0-9>
 * 		Volume:		VOL percent<int 0-100>					#Buzzer/TONE doesn't work if volume less than 8%
 * 		Tone:		TONE freq-Hz<int> duration-ms<int>
 * 		Beep:		BEEP pattern<int 1-5>
 * 		Quit:		QUIT
 * 
 * Example: F 1000 N;R 90 N;P 2000;L 90 N;B 1000 N;QUIT
 * 
 * Notes:
 * 		LED patterns:
 * 			0 = Off , 1 = Green , 2 = Red , 3 = Orange
 * 			4-6 = Even pulses , 7-9 Heartbeat pulses
 * 		Beep patterns:
 * 			1 = beep , 2 = two beeps , 3 = buzzer
 * 			4 = ascending beeps , 5 = descending beeps
 */


class Robot {
	
	public static void Forward(int unit , boolean serial) {
		System.out.println("Forward " + Integer.toString(unit) + " units. Serial: " + Boolean.toString(serial));
		LCD.clear();
		LCD.drawString("Forward", 0, 0);
		int APos = Motor.A.getTachoCount();
		int BPos = Motor.B.getTachoCount();
		Motor.A.rotateTo(APos + unit , true);
		Motor.B.rotateTo(BPos + unit , serial);
	}
	
	public static void Backward(int unit , boolean serial) {
		System.out.println("Backward " + Integer.toString(unit) + " units. Serial: " + Boolean.toString(serial));
		LCD.clear();
		LCD.drawString("Backward", 0, 0);
		int APos = Motor.A.getTachoCount();
		int BPos = Motor.B.getTachoCount();
		Motor.A.rotateTo(APos - unit , true);
		Motor.B.rotateTo(BPos - unit , serial);
	}
	
	public static void Left(int unit , boolean serial) {
		System.out.println("Left " + Integer.toString(unit) + " units. Serial: " + Boolean.toString(serial));
		LCD.clear();
		LCD.drawString("Left", 0, 0);
		int APos = Motor.A.getTachoCount();
		int BPos = Motor.B.getTachoCount();
		Motor.A.rotateTo(APos - unit , true);
		Motor.B.rotateTo(BPos + unit , serial);
	}
	
	public static void Right(int unit , boolean serial) {
		System.out.println("Right " + Integer.toString(unit) + " units. Serial: " + Boolean.toString(serial));
		LCD.clear();
		LCD.drawString("Right", 0, 0);
		int APos = Motor.A.getTachoCount();
		int BPos = Motor.B.getTachoCount();
		Motor.A.rotateTo(APos + unit , true);
		Motor.B.rotateTo(BPos - unit , serial);
	}
	
    public static void main(String args[]) throws Exception {
        String stringIn;
        String[] commands , subCommand;
        int APos , BPos;
        int port = 5678;
        
        //Init Robot
        System.out.println("Running...");
		LCD.drawString("Robot Slave", 0, 0);
		Motor.A.setSpeed(360);
		Motor.B.setSpeed(360);        
        ServerSocket server = new ServerSocket(port);
        System.out.println("Wait for connection on port " + Integer.toString(port));
        
        boolean run = true;
        while(run) {
			//Accept and init new connection
            Socket client = server.accept();
            System.out.println("Got connection on port " + Integer.toString(port));
            BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
            PrintWriter out = new PrintWriter(client.getOutputStream(),true);
            
            //Read in and split command line
            stringIn = in.readLine();
            System.out.println("received: " + stringIn);
            out.println("Executing: " + stringIn);
            commands = stringIn.split(";");
            
            //Run swith for each command
            for (int i = 0; i < commands.length ; i++) {
				subCommand = commands[i].trim().split(" ");
				switch (subCommand[0]) {
					
					//Forward
					case "F":
						if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Forward(Integer.parseInt(subCommand[1]) , true);
						else Forward(Integer.parseInt(subCommand[1]) , false);
						break;
					
					//Backwards
					case "B":
						if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Backward(Integer.parseInt(subCommand[1]) , true);
						else Backward(Integer.parseInt(subCommand[1]) , false);
						break;
					
					//Left
					case "L":
						if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Left(Integer.parseInt(subCommand[1]) , true);
						else Left(Integer.parseInt(subCommand[1]) , false);
						break;
					
					//Right
					case "R":
						if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Right(Integer.parseInt(subCommand[1]) , true);
						else Right(Integer.parseInt(subCommand[1]) , false);
						break;
					
					//Pause
					case "P":
						System.out.println("Pause " + subCommand[1] + " ms");
						LCD.clear();
						LCD.drawString("Pause", 0, 0);
						Delay.msDelay(Long.parseLong(subCommand[1]));
						break;
					
					//LED
					case "LED":
						System.out.println("LED pattern " + subCommand[1]);
						LCD.clear();
						LCD.drawString("LED " + subCommand[1] , 0, 0);
						Button.LEDPattern(Integer.parseInt(subCommand[1]));
						break;
					
					//Set Master Volume
					case "VOL":
						System.out.println("Set volume: " + subCommand[1]);
						LCD.clear();
						LCD.drawString("Volume " + subCommand[1] , 0, 0);
						Sound.setVolume(Integer.parseInt(subCommand[1]));
						break;
					
					//Tone
					case "TONE":
						System.out.println("Tone Freq: " + subCommand[1] + " Duration: " + subCommand[2]);
						LCD.clear();
						LCD.drawString("Tone " + subCommand[1] , 0, 0);
						Sound.playTone(Integer.parseInt(subCommand[1]) , Integer.parseInt(subCommand[2]));
						break;
					
					//Beep
					case "BEEP":
						System.out.println("Beep Type: " + subCommand[1]);
						LCD.clear();
						LCD.drawString("Beep " + subCommand[1] , 0, 0);
						if (subCommand[1].equals("1")) Sound.beep();
						else if (subCommand[1].equals("2")) Sound.twoBeeps();
						else if (subCommand[1].equals("3")) Sound.buzz();
						else if (subCommand[1].equals("4")) Sound.beepSequenceUp();
						else if (subCommand[1].equals("5")) Sound.beepSequence();
						break;
					
					//Quit program
					case "QUIT":
						System.out.println("End Program");
						LCD.clear();
						LCD.drawString("End Program" , 0 , 0);
						Delay.msDelay(1000);
						run = false;
						break;
					
					//Unknown Command
					default:
						System.out.println("Command not recognised");
						break;
				}
			}
        }
        
        
        //Shutdown Program
        Button.LEDPattern(0);
        System.exit(0);
    }
}
