int ch1; // Here's where we'll keep our channel values
int ch2;
int ch3;

void setup() {

  pinMode(5, INPUT); // Set our input pins as such
  pinMode(6, INPUT);
  pinMode(7, INPUT);

  Serial.begin(9600); // Pour a bowl of Serial

}

void loop() {

  ch1 = pulseIn(5, HIGH, 25000); // Read the pulse width of 
  ch2 = pulseIn(6, HIGH, 25000); // each channel
  ch3 = pulseIn(7, HIGH, 25000);

  Serial.print("A"); // Print the value of 
  Serial.print(ch1);        // each channel

  Serial.print("B");
  Serial.print(ch2);

  Serial.print("C");
  Serial.print(ch3);
  Serial.println("D");

//  delay(250); // I put this here just to make the terminal 
              // window happier
}
