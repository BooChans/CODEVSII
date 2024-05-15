#include <Keypad.h>

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

char array1[] = "Code";
char vide[] = "               ";

LiquidCrystal_I2C lcd(0x27, 16, 2);



String input_password = "code ";
char stringBuffer[256];

int Relay = 4;  
int Relay2 = 2;    
int Relay3= 3; 
int Relay4 = 5;


void setup() {
  Serial.begin(9600);   
  pinMode(Relay, OUTPUT);    
  pinMode(Relay2,OUTPUT) ;
  pinMode(Relay3,OUTPUT);
    pinMode(Relay4,OUTPUT);

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
    initial.toCharArray(Buffer,4);
  if (initial = '0'){Serial.println("hi6");   digitalWrite(Relay2, HIGH);           
  delay(2000);
  digitalWrite(Relay2,LOW);
  } 
  if (initial==54){Serial.println("hi7");
  digitalWrite(Relay, HIGH);           

  delay(2000);
  digitalWrite(Relay, LOW);  
           
  }
  if (initial==55){Serial.println("hi8");   digitalWrite(Relay3, HIGH);           
  delay(2000);
  digitalWrite(Relay3,LOW);
  } 
    if (initial==56){Serial.println("hi9");   digitalWrite(Relay4, HIGH);           
  delay(2000);
  digitalWrite(Relay4,LOW);
  } 
  }
} }