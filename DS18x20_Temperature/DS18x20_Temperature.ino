#include <OneWire.h>
#include <SPI.h>
#include <Ethernet.h>
#include <DHT.h>;
// OneWire DS18S20, DS18B20, DS1822 Temperature Example
//
// http://www.pjrc.com/teensy/td_libs_OneWire.html
//
// The DallasTemperature library can do all this work for you!
// http://milesburton.com/Dallas_Temperature_Control_Library

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
char jinni_server[] = "192.168.2.7";    // name address for Google (using DNS)
char server[] = "192.168.2.7";    // name address for Google (using DNS)
IPAddress ip(192, 168, 2, 223);
EthernetClient client;

OneWire  ds(2);  // on pin 10 (a 4.7K resistor is necessary)
float last_celsius = 0;
float last_celsius2 = 0;
float last_humid2 = 0;
unsigned long last_update = 0;

#define DHTPIN 7     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino

void note_temp_jinni(char sensor_name[], float value) {
	// if you get a connection, report back via serial:
    if (client.connect(jinni_server,42042)) {
      Serial.println("connected");
      // Make a HTTP request:
      client.print("GET /hq/temperature/note/");
      client.print(sensor_name);
      client.print("/");
      client.print(value);
      client.println("/ HTTP/1.1");
      client.println();
      while (!client.available());
      while (client.available()){
        char c = client.read();
        Serial.write(c);
      }
      client.stop();
    } else {
      // if you didn't get a connection to the jinni_server:
      Serial.println("connection failed");
    }
}


void setup(void) {
  Serial.begin(9600);
  dht.begin();

  // start the Ethernet connection:
  //if (Ethernet.begin(mac) == 0) {
  //  Serial.println("Failed to configure Ethernet using DHCP");
    // try to congifure using IP address instead of DHCP:
    Ethernet.begin(mac, ip);
  //}
  // give the Ethernet shield a second to initialize:
  delay(1000);
  Serial.println("connecting...");
}


void loop(void) {

  if(last_update == 0 || millis() - last_update >= 60000)
  {
    last_update = millis();
    Serial.println(">>>>>>UPDATING ALIVENESS");
    // if you get a connection, report back via serial:
    if (client.connect(server,42042)) {
      Serial.println("connected");
      // Make a HTTP request:
      client.println("GET /hq/alive/uno HTTP/1.1");
      client.println();
      while (!client.available());
      while (client.available()){
        char c = client.read();
        Serial.write(c);
      }
      client.stop();
    } else {
      // if you didn't get a connection to the server:
      Serial.println("connection failed");
    }
  }
  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
  byte addr[8];
  float celsius, celsius2, humid2, fahrenheit;
  
  if ( !ds.search(addr)) {
    Serial.println("No more addresses.");
    Serial.println();
    ds.reset_search();
    delay(250);
    return;
  }
  
  Serial.print("ROM =");
  for( i = 0; i < 8; i++) {
    Serial.write(' ');
    Serial.print(addr[i], HEX);
  }

  if (OneWire::crc8(addr, 7) != addr[7]) {
      Serial.println("CRC is not valid!");
      return;
  }
  Serial.println();
 
  // the first ROM byte indicates which chip
  switch (addr[0]) {
    case 0x10:
      Serial.println("  Chip = DS18S20");  // or old DS1820
      type_s = 1;
      break;
    case 0x28:
      Serial.println("  Chip = DS18B20");
      type_s = 0;
      break;
    case 0x22:
      Serial.println("  Chip = DS1822");
      type_s = 0;
      break;
    default:
      Serial.println("Device is not a DS18x20 family device.");
      return;
  } 

  ds.reset();
  ds.select(addr);
  ds.write(0x44, 1);        // start conversion, with parasite power on at the end
  
  //delay(5000);     // maybe 750ms is enough, maybe not
  // we might do a ds.depower() here, but the reset will take care of it.
  
  present = ds.reset();
  ds.select(addr);    
  ds.write(0xBE);         // Read Scratchpad

  Serial.print("  Data = ");
  Serial.print(present, HEX);
  Serial.print(" ");
  for ( i = 0; i < 9; i++) {           // we need 9 bytes
    data[i] = ds.read();
    Serial.print(data[i], HEX);
    Serial.print(" ");
  }
  Serial.print(" CRC=");
  Serial.print(OneWire::crc8(data, 8), HEX);
  Serial.println();

  // Convert the data to actual temperature
  // because the result is a 16 bit signed integer, it should
  // be stored to an "int16_t" type, which is always 16 bits
  // even when compiled on a 32 bit processor.
  int16_t raw = (data[1] << 8) | data[0];
  if (type_s) {
    raw = raw << 3; // 9 bit resolution default
    if (data[7] == 0x10) {
      // "count remain" gives full 12 bit resolution
      raw = (raw & 0xFFF0) + 12 - data[6];
    }
  } else {
    byte cfg = (data[4] & 0x60);
    // at lower res, the low bits are undefined, so let's zero them
    if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
    else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
    else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
    //// default is 12 bit resolution, 750 ms conversion time
  }
  celsius = (float)raw / 16.0;
  fahrenheit = celsius * 1.8 + 32.0;
  celsius2 = dht.readTemperature();
  humid2 = dht.readHumidity();
  Serial.print(millis());
  Serial.print("  Temperature = ");
  Serial.print(celsius);
  Serial.print(" Celsius, ");
  Serial.print(fahrenheit);
  Serial.print(" Fahrenheit, ");
  Serial.print(last_celsius);
  Serial.println(" last Celsius");
  
  Serial.print("Humidity: ");
  Serial.print(humid2);
  Serial.print(" %, Temp: ");
  Serial.print(celsius2);
  Serial.print(" Celsius2,");
  Serial.print(last_celsius2);
  Serial.print(" last Celsius2,");
  Serial.print(last_humid2);
  Serial.println(" last Humid2");

  if(abs(last_celsius - celsius) > 0.15)
  {
    last_celsius = celsius;
    Serial.println(">>>>>>UPDATING TEMP");
	note_temp_jinni("ch.eric",celsius);
  }
  
  if(abs(last_celsius2 - celsius2) > 0.15)
  {
    last_celsius2 = celsius2;
    Serial.println(">>>>>>UPDATING TEMP2");
	note_temp_jinni("ch.eric2",celsius2);
  }
  
  if(abs(last_humid2 - humid2) > 0.15)
  {
    last_humid2 = humid2;
    Serial.println(">>>>>>UPDATING HUMID");
	note_temp_jinni("ch.eric.humid2",humid2);
  }
  
  
  delay(1000);     // maybe 750ms is enough, maybe not
}
