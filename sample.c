// LED-Cube_3x3x3 ver.1.21 2020.10.17 meyon
// Pattern cycle (ms)
unsigned long pcycle = 360;
// Pattern data
int ptn[][3] = {
//{LayerA,LayerB,LayerC},
// LayerA
  {01,0,0},{03,0,0},{07,0,0},
  {017,0,0},{037,0,0},{077,0,0},
  {0177,0,0},{0377,0,0},{0777,0,0},
// LayerB
  {0,01,0},{0,03,0},{0,07,0},
  {0,017,0},{0,037,0},{0,077,0},
  {0,0177,0},{0,0377,0},{0,0777,0},
// LayerC
  {0,0,01},{0,0,03},{0,0,07},
  {0,0,017},{0,0,037},{0,0,077},
  {0,0,0177},{0,0,0377},{0,0,0777},
// Sample
  {0111,0111,0111},{0222,0222,0222},{0444,0444,0444},
  {07,07,07},{070,070,070},{0700,0700,0700},
  {0,0,0777},{0,0777,0},{0777,0,0},
  {0505,0,0505},{020,0252,020},{0777,0777,0777},
};
int colpin[9] = {2,3,4,5,6,7,8,12,13}; // Column output pin
int laypin[3] = {9,10,11}; // Layer output pin
void setup() {
  for (int i=0; i<9; i++){
    pinMode (colpin[i], OUTPUT);
  }
  for (int i=0; i<3; i++){
    pinMode (laypin[i], OUTPUT);
  }
}
void loop() {
  int nptn = sizeof(ptn) / sizeof(ptn[0]);
  for (int k=0; k < nptn; k++){
    unsigned long ctime = millis();
    while (millis() - ctime < pcycle){
      for (int j=0; j<3; j++){
        for(int i=0; i<9; i++){
          digitalWrite (colpin[i], ptn[k][j]>>i&1);
        }
        digitalWrite (laypin[j], HIGH);
        delay(5);
        digitalWrite (laypin[j], LOW);
      }
    }
  }
}