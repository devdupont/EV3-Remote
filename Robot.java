import java.io.*;
import java.net.Socket;
import java.net.ServerSocket;
import java.util.Scanner;
import lejos.nxt.Button;
import lejos.nxt.LCD;
import lejos.nxt.Motor;
import lejos.nxt.Sound;
import lejos.nxt.LocalBattery;
import lejos.util.Delay;


/*
 * Michael duPont - flyinactor91.com
 * EV3-Remote - https://github.com/flyinactor91/EV3-Remote
 * Generic robot client
 * Lejos 0.4.0-alpha running on EV3
 * 
 * 2013-12-28
 * 
 * Commands recieved from Controller
 *     jrun Robot (-c)
 * Commands recieved from terminal
 *     jrun Robot -t
 * 
 * Commands separated by ';'
 * Available Commands:
 * 		Motors
 * 			Forward: 	F distance<int> (serial<def=Y /N>)
 * 			Backward: 	B distance<int> (serial<def=Y /N>)
 * 			Left:		L degree<int> (serial< def=Y /N>)
 * 			Right:		R degree<int> (serial< def=Y /N>)
 * 			Servo:		S degree<int +/->
 * 			MotorSpd:	MS motor<M/S> speed<int>				#Main (A and B) / Servo (C)
 *		Sound
 * 			Volume:		VOL percent<int 0-100>					#Buzzer/TONE doesn't work if volume less than 8%
 * 			Tone:		TONE freq-Hz<int> duration-ms<int>
 * 			Beep:		BEEP pattern<int 1-5>
 * 			Song:		WAV song<*.wav>							#Song.wav location
 *		Utils
 * 			Pause:		P duration-ms<int>
 * 			LED Disp:	LED pattern<int 0-9>
 * 			Battery:	BAT										#Displays the battery level (terminal/LCD)
 * 			Quit:		QUIT
 * 
 * Example: F 1000 N;LED 8;S 300;P 2000;L 220;B 300;S -300;BEEP 5;QUIT
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
	
	static Boolean toLCD = true;
	
	public static void printToLCD(String txt) {
		LCD.clear();
		LCD.drawString(txt , 0 , 0);
	}
	
	//Controls main/movement motors. Direction = "Forward" || "Backward" || "Left" || "Right"
	//New positions are both calculated early to minimize lag time between motor A init and motor B init
	public static void Move(String direction , int unit , boolean serial) {
		System.out.println(direction + " " + Integer.toString(unit) + " units. !Serial: " + Boolean.toString(serial));
		if (toLCD) printToLCD(direction);
		int APos = Motor.A.getTachoCount();
		int BPos = Motor.B.getTachoCount();
		int newAPos , newBPos;
		if ((direction.equals("Forward")) || (direction.equals("Right"))) newAPos = APos + unit;
		else newAPos = APos - unit;
		if ((direction.equals("Forward")) || (direction.equals("Left"))) newBPos = BPos + unit;
		else newBPos = BPos - unit;
		Motor.A.rotateTo(newAPos , true);
		Motor.B.rotateTo(newBPos , serial);
	}
	
	//Controls non-movement motor. Unit can be + or -
	public static void Servo(int unit , boolean serial) {
		System.out.println("Servo " + Integer.toString(unit) + " units. Serial: " + Boolean.toString(serial));
		if (toLCD) printToLCD("Servo");
		int CPos = Motor.C.getTachoCount();
		Motor.C.rotateTo(CPos + unit , serial);
	}
	
    public static void main(String args[]) throws IOException {
        String stringIn;
        String[] commands , subCommand;
        int port = 5678;
        boolean fromClient = true;
        //If recieving commands from Controller
        if ((args.length == 0) || ((args.length == 1) && (args[0].equals("-c")))) {
			fromClient = true;
		}
        //If recieving commands from terminal
        else if ((args.length == 1) && (args[0].equals("-t"))) {
			fromClient = false;
		}
        else {
			System.out.println("Usage: java Robot (-c/-t)");
			System.exit(0);
		}
        
        //Init Robot
        System.out.println("Running...");
		LCD.drawString("EV3-Remote", 0, 0);
		Motor.A.setSpeed(360);
		Motor.B.setSpeed(360);
		Motor.C.setSpeed(360);
		
		ServerSocket server = new ServerSocket(port); //Server is always init'd because compile will throw errors if only declared
		if (fromClient) {
			System.out.println("Wait for connection on port " + Integer.toString(port));
        }
        
        
        boolean run = true;
        while (run) {
			if (fromClient) {
				//Accept and init new connection
				Socket client = server.accept();
				System.out.println("Got connection on port " + Integer.toString(port));
				BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
				PrintWriter out = new PrintWriter(client.getOutputStream(),true);
				stringIn = in.readLine();
				System.out.println("\nreceived: " + stringIn);
				out.println("Executing: " + stringIn + "\n");
			}
			else {
				System.out.print("\nCommand: ");
				stringIn = new Scanner (System.in).nextLine();
			}
			//Trim and get commands
            stringIn = stringIn.trim();
            commands = stringIn.split(";");
            
            //Run swith for each command
            for (int i = 0; i < commands.length ; i++) {
				subCommand = commands[i].trim().split(" ");
				switch (subCommand[0]) {
					
					//Forward
					case "F":
						//if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Forward(Integer.parseInt(subCommand[1]) , true);
						//else Forward(Integer.parseInt(subCommand[1]) , false);
						if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Move("Forward" , Integer.parseInt(subCommand[1]) , true);
						else Move("Forward" , Integer.parseInt(subCommand[1]) , false);
						break;
					
					//Backwards
					case "B":
						//if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Backward(Integer.parseInt(subCommand[1]) , true);
						//else Backward(Integer.parseInt(subCommand[1]) , false);
						if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Move("Backward" , Integer.parseInt(subCommand[1]) , true);
						else Move("Backward" , Integer.parseInt(subCommand[1]) , false);
						break;
					
					//Left
					case "L":
						//if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Left(Integer.parseInt(subCommand[1]) , true);
						//else Left(Integer.parseInt(subCommand[1]) , false);
						if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Move("Left" , Integer.parseInt(subCommand[1]) , true);
						else Move("Left" , Integer.parseInt(subCommand[1]) , false);
						break;
					
					//Right
					case "R":
						//if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Right(Integer.parseInt(subCommand[1]) , true);
						//else Right(Integer.parseInt(subCommand[1]) , false);
						if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Move("Right" , Integer.parseInt(subCommand[1]) , true);
						else Move("Right" , Integer.parseInt(subCommand[1]) , false);
						break;
					
					//Servo
					case "S":
						if ((subCommand.length > 2) && (subCommand[2].equals("N"))) Servo(Integer.parseInt(subCommand[1]) , true);
						else Servo(Integer.parseInt(subCommand[1]) , false);
						break;
					
					//Set Motor Speed
					case "MS":
						System.out.println("Set motor " + subCommand[1] + " to " + subCommand[2]);
						if (toLCD) printToLCD("Motor " + subCommand[1] + " " + subCommand[2]);
						if (subCommand[1].equals("M")) {
							Motor.A.setSpeed(Integer.parseInt(subCommand[2]));
							Motor.B.setSpeed(Integer.parseInt(subCommand[2]));
						}
						if (subCommand[1].equals("S")) Motor.C.setSpeed(Integer.parseInt(subCommand[2]));
						break;
					
					//Pause
					case "P":
						System.out.println("Pause " + subCommand[1] + " ms");
						if (toLCD) printToLCD("Pause");
						Delay.msDelay(Long.parseLong(subCommand[1]));
						break;
					
					//LED
					case "LED":
						System.out.println("LED pattern " + subCommand[1]);
						if (toLCD) printToLCD("LED " + subCommand[1]);
						Button.LEDPattern(Integer.parseInt(subCommand[1]));
						break;
					
					//Set Master Volume
					case "VOL":
						System.out.println("Set volume: " + subCommand[1]);
						if (toLCD) printToLCD("Volume " + subCommand[1]);
						Sound.setVolume(Integer.parseInt(subCommand[1]));
						break;
					
					//Tone
					case "TONE":
						System.out.println("Tone Freq: " + subCommand[1] + " Duration: " + subCommand[2]);
						if (toLCD) printToLCD("Tone " + subCommand[1]);
						Sound.playTone(Integer.parseInt(subCommand[1]) , Integer.parseInt(subCommand[2]));
						break;
					
					//Beep
					case "BEEP":
						System.out.println("Beep Type: " + subCommand[1]);
						if (toLCD) printToLCD("Beep " + subCommand[1]);
						if (subCommand[1].equals("1")) Sound.beep();
						else if (subCommand[1].equals("2")) Sound.twoBeeps();
						else if (subCommand[1].equals("3")) Sound.buzz();
						else if (subCommand[1].equals("4")) Sound.beepSequenceUp();
						else if (subCommand[1].equals("5")) Sound.beepSequence();
						else System.out.println("Invalid BEEP value");
						break;
					
					//Song
					case "WAV":
						System.out.println("Song: " + subCommand[1]);
						if (toLCD) printToLCD("Song " + subCommand[1]);
						File song = new File(subCommand[1]);
						if(song.exists()) {Sound.playSample(song);}
						//Sound.playSample(new File("halsorry.wav"));
						else System.out.println("File not found " + subCommand[1]);
						break;
					
					//Get battery voltage
					case "BAT":
						LocalBattery battery = new LocalBattery();
						String percent = Integer.toString((int)Math.round(battery.getVoltage() / 8.4 * 100)); //8.4 is the highest I could charge my battery. YMMV
						System.out.println("Battery: " + percent + "%");
						if (toLCD) printToLCD("Battery " + percent + "%");
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
