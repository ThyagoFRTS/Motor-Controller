#define sensor A0
#define potency A1

const int led1 = 8;
const int led2 = 9;
const int led3 = 10;
const int motor = 11;
const int left = 12;
const int right = 13;

int input = 0;

bool controller_led1 = false;
bool controller_led2 = false;
bool controller_led3 = false;

void setup()
{
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);

  pinMode(motor, OUTPUT);
  pinMode(left, OUTPUT);
  pinMode(right, OUTPUT);

  pinMode(sensor, INPUT);
  pinMode(potency, INPUT);

  clear_leds();
  Serial.begin(9600);
}

void loop() {
  while (Serial.available())
  {
    input = Serial.read();
  }
  switch (input) {
    case '1':
      manage_leds(led1, &controller_led1);
      input = 0;
      break;
    case '2':
      manage_leds(led2, &controller_led2);
      input = 0;
      break;
    case '3':
      manage_leds(led3, &controller_led3);
      input = 0;
      break;
    case '4': // ESQUERDA
      digitalWrite(motor,HIGH);
      digitalWrite(left,HIGH);
      digitalWrite(right,LOW);
      input = 0;
      break;
    case '5': // DIREITA
      digitalWrite(motor,HIGH);
      digitalWrite(right,HIGH);
      digitalWrite(left,LOW);
      input = 0;
    break;  
    case '6':
      // desligar
      digitalWrite(motor,LOW);
      digitalWrite(right,LOW);
      digitalWrite(left,LOW);
      input = 0;
      break;
    case '7':
      Serial.print(analogRead(sensor) * 0.488);
      input = 0;
      break;
    case '8':
      Serial.print(analogRead(potency));
      input = 0;
      break;
    case '9':
      String message = String(analogRead(potency)) +" "+ String(analogRead(sensor) * 0.488); 
      Serial.print(message);
      input = 0;
      break;
    
  }
  input = 0;
}

void manage_leds(int led, bool* controller_led) {
  if (*controller_led) {
    digitalWrite(led, LOW); switch_bool(controller_led);
  } else {
    digitalWrite(led, HIGH); switch_bool(controller_led);
  }
}

void switch_bool(bool *led) {
  *led ? *led = false : *led = true;
}

void clear_leds() {
  digitalWrite (led1, LOW);
  digitalWrite (led2, LOW);
  digitalWrite (led3, LOW);
}
