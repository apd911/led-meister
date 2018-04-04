#include <EEPROM.h>

#define RED_PIN 6
#define GREEN_PIN 5
#define BLUE_PIN 3

int redb = 0;
int greenb = 0;
int blueb = 0;

long c[4];

int UPDATES_PER_SECOND = EEPROM.read(8);

int redc = EEPROM.read(11);
int greenc = EEPROM.read(13);
int bluec = EEPROM.read(15);

int paletteCounter = EEPROM.read(5);
int brightnessCounter = EEPROM.read(6);
int dir = 9; // sets strip type (non-addressable)

String type = "arduino";
String id = "DeskStrip";

void setup() {
  Serial.begin(9600);
  delay(100);
  
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
}

void loop() {
  if (Serial.available() >= 4) {
    for (int i = 0; i < 4; i++) {
      c[i] = Serial.read();
    }
    Serial.flush();
    if (c[0] == 9 && c[1] == 1) {
      Serial.println(String(paletteCounter) + ' ' + String(brightnessCounter) + ' ' + String(UPDATES_PER_SECOND) + ' ' + String(dir) + ' ' + String(type) + ' ' + String(id));
    }
    else if (c[0] == 1 && c[1] == 2) {
      brightnessCounter=c[2];
    }
    else if (c[0] == 1 && c[1] == 3) {
      if (dir == 0) {
        dir = 1;
      }
      else {
        dir = 0; //invert direction
      }
    }
    else if (c[0] == 1 && c[1] == 4) {
      UPDATES_PER_SECOND=c[2];
    }
    
    else if (c[0] == 2 && c[1] == 1) {
      paletteCounter = 1; //rainbow
    }
    else if (c[0] == 2 && c[1] == 2) {
      paletteCounter = 2; //blackwhite
    }
    else if (c[0] == 2 && c[1] == 3) {
      paletteCounter = 3; //fire1
    }
    else if (c[0] == 2 && c[1] == 4) {
      paletteCounter = 4; //ocean
    }
    else if (c[0] == 2 && c[1] == 5) {
      paletteCounter = 5; //lava
    }
    else if (c[0] == 2 && c[1] == 6) {
      paletteCounter = 6; //forest
    }
    else if (c[0] == 2 && c[1] == 7) {
      paletteCounter = 7; //fire2
    }
    else if (c[0] == 2 && c[1] == 8) {
      paletteCounter = 8; //police
    }
    else if (c[0] == 2 && c[1] == 9) {
      paletteCounter = 9; //party
    }
    else if (c[0] == 2 && c[1] == 0) {
      paletteCounter = 10; //blackout
    }
    else if (c[0] == 3 && c[1] == 0) {
      EEPROM.write(5, paletteCounter);
      EEPROM.write(6, brightnessCounter);
      EEPROM.write(8, UPDATES_PER_SECOND);
      EEPROM.write(11, redc);
      EEPROM.write(13, greenc);
      EEPROM.write(15, bluec); //save settings
    }
    else if (c[0] == 4){
      paletteCounter = 11; //custom color
      redc = c[1];
      greenc = c[2];
      bluec = c[3];
    }
    
  }
  ChangePalette();
}

void solid(){
  redb = (redc * brightnessCounter) / 255;
  greenb = (greenc * brightnessCounter) / 255;
  blueb = (bluec * brightnessCounter) / 255;
  
  analogWrite(RED_PIN, redb);
  analogWrite(GREEN_PIN, greenb);
  analogWrite(BLUE_PIN, blueb);
}

void ChangePalette(){   
    if( paletteCounter == 10)  { Black();}
    if( paletteCounter == 11)  { solid();}
}

void Black(){
  analogWrite(RED_PIN, 0);
  analogWrite(GREEN_PIN, 0);
  analogWrite(BLUE_PIN, 0);
}

