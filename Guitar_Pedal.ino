int ID = 2;
int padle_pin_1 = 2;
int timeout = 1 * 100;
unsigned long delay_between_presses = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);
  pinMode(padle_pin_1, INPUT);
  Serial.begin(9600);

  
}

void do_blink() {
  digitalWrite(13,1);
  delay(1000);
  digitalWrite(13,0);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  //do_blink();
  if(digitalRead(padle_pin_1)) {
    millis();
    digitalWrite(13,1);
    Serial.print(padle_pin_1);//ID
    delay(timeout);
  } else {
    digitalWrite(13,0);
  }
}
