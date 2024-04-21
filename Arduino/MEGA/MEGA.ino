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

} 
void loop() {
  if (Serial.available() > 0){
    int hi=Serial.read();
    Serial.println(hi);
  if (hi==53){Serial.println("hi6");   digitalWrite(Relay2, HIGH);           
  delay(2000);
  digitalWrite(Relay2,LOW);
  } 
  if (hi==54){Serial.println("hi7");
  digitalWrite(Relay, HIGH);           

  delay(2000);
  digitalWrite(Relay, LOW);  
           
  }
  if (hi==55){Serial.println("hi8");   digitalWrite(Relay3, HIGH);           
  delay(2000);
  digitalWrite(Relay3,LOW);
  } 
    if (hi==56){Serial.println("hi9");   digitalWrite(Relay4, HIGH);           
  delay(2000);
  digitalWrite(Relay4,LOW);
  } 
  }
} 