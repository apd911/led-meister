#include <FastLED.h>
#include <EEPROM.h>
 
#define LED_PIN 5
#define NUM_LEDS 95
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
#define SPARKING 120
#define COOLING  55

bool gReverseDirection = true; // Invert direction of fire

int redc = EEPROM.read(11);
int greenc = EEPROM.read(13);
int bluec = EEPROM.read(15);

long c[4];
 
CRGB leds[NUM_LEDS];

int UPDATES_PER_SECOND = EEPROM.read(8);

CRGBPalette32 currentPalette;
TBlendType    currentBlending;

int paletteCounter = EEPROM.read(5);
int brightnessCounter = EEPROM.read(6);
int dir = EEPROM.read(10);
 
void setup() {

  Serial.begin(9600);
 
  delay( 1000 );
 
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness(255);
}
 
void loop() {

  if (Serial.available() >= 4) {
    for (int i = 0; i < 4; i++) {
      c[i] = Serial.read();
    }
    Serial.flush();
    if (c[0] == 9 && c[1] == 1) {
      Serial.println(String(paletteCounter) + ' ' + String(brightnessCounter) + ' ' + String(UPDATES_PER_SECOND) + ' ' + String(dir));
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
      paletteCounter = 3; //fire
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
      paletteCounter = 7; //greenpurple
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
      EEPROM.write(10, dir);
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
  if (paletteCounter == 3){
    Fire();
    FastLED.show();
    FastLED.delay(1000 / UPDATES_PER_SECOND); 
  }
  else {
    ChangePalette();
    static uint8_t startIndex = 0;

    startIndex = startIndex + 1;
   
    FillLEDsFromPaletteColors(startIndex);
    FastLED.show();
    FastLED.delay(800 / UPDATES_PER_SECOND); 
  }
}

void fillSolid(uint32_t colour) {      
  fill_solid(leds, NUM_LEDS, colour);
}
 
void FillLEDsFromPaletteColors( uint8_t colorIndex)
{
  
  for( int i = 0; i < NUM_LEDS; i++) {
    leds[i] = ColorFromPalette( currentPalette, colorIndex, brightnessCounter, currentBlending);
    if (dir == 0) {
      colorIndex += 3;
    }
    else {
      colorIndex -= 3;
    }
  }
}
 
void ChangePalette()
{   
    if( paletteCounter == 1)  { currentPalette = RainbowColors_p;         currentBlending = LINEARBLEND;}
    if( paletteCounter == 2)  { SetupBlackAndWhiteStripedPalette();       currentBlending = LINEARBLEND;}
    if( paletteCounter == 4)  { currentPalette = OceanColors_p;           currentBlending = LINEARBLEND;}
    if( paletteCounter == 5)  { currentPalette = LavaColors_p;            currentBlending = LINEARBLEND;}
    if( paletteCounter == 6)  { currentPalette = ForestColors_p;          currentBlending = LINEARBLEND;}
    if( paletteCounter == 7)  { SetupPurpleAndGreenPalette();             currentBlending = LINEARBLEND;}
    if( paletteCounter == 8)  { SetupPolicePalette();                     currentBlending = LINEARBLEND;}
    if( paletteCounter == 9)  { currentPalette = PartyColors_p;           currentBlending = LINEARBLEND;}
    if( paletteCounter == 10)  { Black();                                 currentBlending = LINEARBLEND;}
    if( paletteCounter == 11)  { fill_solid( currentPalette, 32, CRGB(redc, greenc, bluec)); currentBlending = LINEARBLEND;}
}

void SetupBlackAndWhiteStripedPalette()
{
  fill_solid( currentPalette, 16, CRGB::White);
  currentPalette[7] = CRGB::Black;
  currentPalette[8] = CRGB::Black;
  currentPalette[9] = CRGB::Black;
  currentPalette[22] = CRGB::White;
  currentPalette[23] = CRGB::White;
  currentPalette[24] = CRGB::White;
}

void SetupPolicePalette()
{
  fill_solid( currentPalette, 32, CRGB::Black);
  currentPalette[0] = CRGB::Red;
  currentPalette[1] = CRGB::Red;
  currentPalette[2] = CRGB::Black;
  currentPalette[3] = CRGB::Blue;
  currentPalette[4] = CRGB::Blue;
  currentPalette[5] = CRGB::Black;
  currentPalette[6] = CRGB::Red;
  currentPalette[7] = CRGB::Red;
  currentPalette[8] = CRGB::Black;
  currentPalette[9] = CRGB::Blue;
  currentPalette[10] = CRGB::Blue;
  currentPalette[11] = CRGB::Black;
  currentPalette[12] = CRGB::Red;
  currentPalette[13] = CRGB::Red;
  currentPalette[14] = CRGB::Red;
  currentPalette[15] = CRGB::Red;
  currentPalette[16] = CRGB::Black;
  currentPalette[17] = CRGB::Blue;
  currentPalette[18] = CRGB::Blue;
  currentPalette[19] = CRGB::Blue;
  currentPalette[20] = CRGB::Blue;
  currentPalette[21] = CRGB::Black;
  currentPalette[22] = CRGB::Red;
  currentPalette[23] = CRGB::Red;
  currentPalette[24] = CRGB::Red;
  currentPalette[25] = CRGB::Red;
  currentPalette[26] = CRGB::Black;
  currentPalette[27] = CRGB::Blue;
  currentPalette[28] = CRGB::Blue;
  currentPalette[29] = CRGB::Blue;
  currentPalette[30] = CRGB::Blue;
  currentPalette[31] = CRGB::Black;
}

void Fire()
{
  static byte heat[NUM_LEDS];

  for( int i = 0; i < NUM_LEDS; i++) {
    heat[i] = qsub8( heat[i],  random8(0, ((COOLING * 10) / NUM_LEDS) + 2));
  }
  
  for( int k= NUM_LEDS - 1; k >= 2; k--) {
    heat[k] = (heat[k - 1] + heat[k - 2] + heat[k - 2] ) / 3;
  }
    
  if( random8() < SPARKING ) {
    int y = random8(7);
    heat[y] = qadd8( heat[y], random8(160,255) );
  }

  for( int j = 0; j < NUM_LEDS; j++) {
    CRGB color = HeatColor( heat[j]);
    int pixelnumber;
    if( gReverseDirection ) {
      pixelnumber = (NUM_LEDS-1) - j;
    } else {
      pixelnumber = j;
    }
    leds[pixelnumber] = color;
  }
}

void Black()
{
  CRGB black = CRGB::Black;

  currentPalette = CRGBPalette16(
    black, black, black, black,
    black, black, black, black,
    black, black, black, black,
    black, black, black, black);
}

void SetupPurpleAndGreenPalette()
{
  CRGB purple = CHSV( HUE_PURPLE, 255, 255);
  CRGB green  = CHSV( HUE_GREEN, 255, 255);
  CRGB black  = CRGB::Black;
 
  currentPalette = CRGBPalette16(
    green,  green,  black,  black,
    purple, purple, black,  black,
    green,  green,  black,  black,
    purple, purple, black,  black );
}


