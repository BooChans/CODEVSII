#include <SPI.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>
#include "arduino_secrets.h" 
///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = SECRET_SSID;        // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0; 
char  ReplyBuffer[] = "reconnu";


#include <Keypad.h>

#define L1 8
#define L2 7
#define L3 6
#define L4 5
#define C1 4
#define C2 3
#define C3 2

const byte lignes = 4;
const byte colonnes = 3;

char code[lignes][colonnes] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};

byte pin_lignes[lignes] = {L1, L2, L3, L4};
byte pin_colonnes[colonnes] = {C1, C2, C3};

Keypad clavier = Keypad(makeKeymap(code), pin_lignes, pin_colonnes, lignes, colonnes);

String input_password;

                // your network key index number (needed only for WEP)

int status = WL_IDLE_STATUS;
unsigned int localPort = 2390;
int openPin = 2; 
char packetBuffer[256];
char stringBuffer[256];
String clear = "clear";
IPAddress ip;

WiFiUDP Udp;
WiFiClient client;
IPAddress serveur(192,168,43,84);

void setup() {
  Serial.begin(9600);   
  Serial1.begin(9600);   // initialize serial communication
  pinMode(openPin, OUTPUT);      // set the LED pin mode


  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true);
  }

  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }

  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);                   // print the network name (SSID);

    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);
    // wait 10 seconds for connection:
    delay(10000);
  }
  Serial.print("You are now connected to the network");
  Udp.begin(localPort);
                        // you're connected now, so print out the status
}


void loop() {
  char actionBuffer[16];
  if (WiFi.status() != status) {
    Serial.println("\nConnexion lost");
    NVIC_SystemReset();
    }
    int packetSize = Udp.parsePacket();
  if (packetSize) {
    Serial.print("Received packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    IPAddress remoteIp = Udp.remoteIP();
    Serial.print(remoteIp);
    Serial.print(", port ");
    Serial.println(Udp.remotePort());

    // read the packet into packetBufffer
    int len = Udp.read(packetBuffer, 255);
    if (len > 0) {
      packetBuffer[len] = 0;
    }
    Serial.println("Contents:");
    Serial.println(packetBuffer);


    Udp.beginPacket(serveur, localPort);
    char buf[30];
    strcpy(buf,ReplyBuffer);
    strcat(buf," ");
    strcat(buf, packetBuffer);


    
    Udp.write(buf);
    Serial.write(buf);


    
    Udp.endPacket();
    delay(2000);
    Serial1.write("C");
    Serial1.write(packetBuffer);
    }

  char touche = clavier.getKey();
  if (touche != NO_KEY)
  {
    Serial.println(touche);

      if(touche == '*') {
      input_password = ""; // clear input password
      Serial1.write("D");
      clear.toCharArray(actionBuffer, 16);
      Serial1.write(actionBuffer);
    } else if(touche == '#') {
      Serial1.write("D");
      clear.toCharArray(actionBuffer, 16);
      Serial1.write(actionBuffer);
      input_password.toCharArray(stringBuffer,256);
      Serial.write(stringBuffer);
      Udp.beginPacket(serveur, localPort);
      Udp.write(stringBuffer);
      Udp.endPacket();

      input_password = ""; // clear input password
    } else {
      input_password += touche;
      Serial1.write("D");
      input_password.toCharArray(actionBuffer,16);
      Serial1.write(actionBuffer); // append new character to input password string
    }
  }

    
  }
  

  
