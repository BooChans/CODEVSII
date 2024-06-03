#include <Keypad.h>

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

char array1[] = "Code";
char vide[] = "               ";

LiquidCrystal_I2C lcd(0x27, 16, 2);



String input_password = "code ";
char stringBuffer[256];

int Relay = 23;  
int Relay1 = 25;    
int Relay2 = 27; 
int Relay3 = 29;
int Relay4 = 31;
int Relay5 = 33;  
int Relay6 = 35;    
int Relay7 = 37; 
int Relay8 = 39;
int Relay9 = 41;

String velo0 = "0";
String velo1 = "1";
String velo2 = "2";
String velo3 = "3";
String velo4 = "4"; 
String velo5 = "5";
String velo6 = "6";
String velo7 = "7";
String velo8 = "8";
String velo9 = "9"; 

void setup() {
  Serial.begin(9600);   
  pinMode(Relay, OUTPUT);   
    pinMode(Relay1,OUTPUT) ; 
  pinMode(Relay2,OUTPUT) ;
  pinMode(Relay3,OUTPUT);
    pinMode(Relay4,OUTPUT);
    pinMode(Relay5,OUTPUT);
    pinMode(Relay6, OUTPUT);    
  pinMode(Relay7,OUTPUT) ;
  pinMode(Relay8,OUTPUT);
    pinMode(Relay9,OUTPUT);
  lcd.init();
  lcd.backlight();

  lcd.print(array1);
  lcd.setCursor(0, 1);
  lcd.print(vide);

} 
void loop() {
  if (Serial.available() > 0){
    char initial=Serial.read();
    Serial.println(initial);
    char buf[16];

    if (initial=='D'){
      String action = Serial.readString();
      if (action == "clear"){
        lcd.setCursor(0, 1);
        lcd.print(vide);
      }
      else{
        action.toCharArray(buf,16);
        lcd.setCursor(0, 1);
        lcd.print(buf);
      }}

  

  else{
    char Buffer[4];
    String initial = Serial.readString();
  if (initial == velo0){Serial.println("hi6");   digitalWrite(Relay, HIGH);           
  delay(2000);
  digitalWrite(Relay,LOW);
  } 
  if (initial== velo1){Serial.println("hi7");
  digitalWrite(Relay1, HIGH);           

  delay(2000);
  digitalWrite(Relay1, LOW);  
           
  }
  if (initial== velo2){Serial.println("hi8");   digitalWrite(Relay2, HIGH);           
  delay(2000);
  digitalWrite(Relay2,LOW);
  } 
    if (initial==velo3){Serial.println("hi9");   digitalWrite(Relay3, HIGH);           
  delay(2000);
  digitalWrite(Relay3,LOW);
  }
  if (initial == velo4){Serial.println("hi10"); digitalWrite(Relay4,HIGH);
  delay(2000);
  digitalWrite(Relay4,LOW);} 

    if (initial == velo5){Serial.println("hi6");   digitalWrite(Relay5, HIGH);           
  delay(2000);
  digitalWrite(Relay5,LOW);
  } 
  if (initial== velo6){Serial.println("hi7");
  digitalWrite(Relay6, HIGH);           

  delay(2000);
  digitalWrite(Relay6, LOW);  
           
  }
  if (initial== velo7){Serial.println("hi8");   digitalWrite(Relay7, HIGH);           
  delay(2000);
  digitalWrite(Relay7,LOW);
  } 
    if (initial==velo8){Serial.println("hi9");   digitalWrite(Relay8, HIGH);           
  delay(2000);
  digitalWrite(Relay8,LOW);
  }
  if (initial == velo9){Serial.println("hi10"); digitalWrite(Relay9,HIGH);
  delay(2000);
  digitalWrite(Relay9,LOW);} 
  }
} }