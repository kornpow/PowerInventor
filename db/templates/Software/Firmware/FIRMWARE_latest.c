// This #include statement was automatically added by the Particle IDE.
#include "PietteTech_DHT/PietteTech_DHT.h"

#include "string.h"

#define NUM_RELAYS 4

// system defines
#define DHTTYPE  DHT22              // Sensor type DHT11/21/22/AM2301/AM2302
#define DHTPIN   7         	    // Digital pin for communications
#define DHT_SAMPLE_INTERVAL   2000  // Sample every two seconds

#define NUM_RELAYS 4


int relayNum[NUM_RELAYS] = {D6,D5,D4,D3};

int switchTemp[NUM_RELAYS] = {-69,-69,95,-69};
int switchDir[NUM_RELAYS] = {1, 1,0, 1,};
// #endif

//Particle Variables
int relayStatus[4] = {0};
int relaypack = 0;
int tempf = -1;
int humidity = -1;
int light = -1;


//DHTlib declarations
//declaration
void dht_wrapper(); // must be declared before the lib initialization

// Lib instantiate
PietteTech_DHT DHT(DHTPIN, DHTTYPE, dht_wrapper);

// globals
unsigned int DHTnextSampleTime;	    // Next time we want to start sample
bool bDHTstarted;		    // flag to indicate we started acquisition
int n;                              // counter


int sched[16];

int scheduler(String data);

// This wrapper is in charge of calling
// must be defined like this for the lib work
void dht_wrapper() {
    DHT.isrCallback();
}

void on_handler(const char *event, const char *data)
{
    int io = atoi(data);
    switch(io) {
        case 1: 
        {
            digitalWrite(relayNum[0],HIGH);
            relayStatus[0] = 1;
            break;
        }
        case 2:
        {
            digitalWrite(relayNum[1],HIGH);
            relayStatus[1] = 1;
            break;
        }
        case 3: 
        {
            digitalWrite(relayNum[2],HIGH);
            relayStatus[2] = 1;
            break;
        }
        case 4:
        {
            digitalWrite(relayNum[3],HIGH);
            relayStatus[3] = 1;
            break;
        }
    }
        
        return;
}
void off_handler(const char *event, const char *data)
{
    int io = atoi(data);
    switch(io) {
        case 1: 
        {
            digitalWrite(relayNum[0],LOW);
            relayStatus[0] = 0;
            break;
        }
        case 2:
        {
            digitalWrite(relayNum[1],LOW);
            relayStatus[1] = 0;
            break;
        }
        case 3: 
        {
            digitalWrite(relayNum[2],LOW);
            relayStatus[2] = 0;
            break;
        }
        case 4:
        {
            digitalWrite(relayNum[3],LOW);
            relayStatus[3] = 0;
            break;
        }
    }
        
        return;
}

void GetRelayStatus(const char *event, const char *data) {
    char buffer[20];
    for(int i = 0; i < NUM_RELAYS; i++) {
        sprintf(buffer, "Status %d = %d", i, relayStatus[i]);
        Particle.publish("skorn_stderr",buffer);
    }
}

void SetRelay(int val);

// int scheduler(String data) {
    // Particle.publish("skorn_stderr","Current 24 hourly schedule:");
    // Particle.publish("skorn_stderr","hour: status");
    // char buffer[20];
    // for(int i = 0; i < 24; i++) {
    //     for(int j = 0; j < 4; j++) {
    //         if(slots[i][j]) {
    //             sprintf(buffer,"hour: %d, minute: %d, task: %d",i,j,slots[i][j]);
    //             Particle.publish("skorn_stderr",buffer);
    //         }
    //     }
    // }
// }

//TODO: Write Scheduling Functions
// int addEvent(String data) {
//     if(strlen(data) != 6) {
//         Particle.publish("skorn_stderr","Usage (No Spaces)(6 chars): (hr)(min)(bitpack)");
//         return -1;
//     }
    
//     String hour = data.substring(0,2);
//     String min = data.substring(2,4);
//     String bp = data.substring(4,6);
    
//     Particle.publish("skorn_stderr",hour);
//     Particle.publish("skorn_stderr",min);
//     Particle.publish("skorn_stderr",bp);
    
//     int h, m;
    
//     return 0;
// }



int water_time = 10;
int cycle_time = 20;
int last_time = 0;


void setup() {
    //Set IO Pin directions
    for (int i = 0; i < NUM_RELAYS; i++) {
        pinMode(relayNum[i],OUTPUT);
    }
    pinMode(D7,OUTPUT);
    //Register Status Variables
    Particle.variable("relay1", relayStatus[0]);
    Particle.variable("relay2", relayStatus[1]);
    Particle.variable("relay3", relayStatus[2]);
    Particle.variable("relay4", relayStatus[3]);
    Particle.variable("tempf", tempf);
    Particle.variable("humidity", humidity);
    Particle.variable("rpack", relaypack);
    Particle.variable("light",light);

    Particle.subscribe("skorn_on",on_handler);
    Particle.subscribe("skorn_off",off_handler);
    Particle.subscribe("skorn_status", GetRelayStatus);
    
    
    //Setup Light Sensor
    light = analogRead(A1);
    



    
    bool success = Particle.function("set", WebSetRelay);
    success = Particle.function("schedule", scheduler);
    success = Particle.function("ps", printEEPROM);
 
    
    if(!success) {
        Particle.publish("skorn_stderr","failed to register a cloud function.");
    }
    
    
    char buffer[20];
    sprintf(buffer,"hour: %d",(int) Time.hour());
    Particle.publish("skorn_stderr",buffer);
    sprintf(buffer,"minute: %d",(int) Time.minute());
    Particle.publish("skorn_stderr",buffer);
    
    
    int min = Time.minute();
    
    Time.zone(-6); //Boulder Colorado Time!
    
    DHTnextSampleTime = 0;
}

void loop() {
    checkSchedule();
    GetWeather();
    relaypack = RelayStatusPack();
    light = analogRead(A0);
    // CheckTemp();
    
    delay(500);
}

void CheckTemp() {
    for(int i = 0; i < NUM_RELAYS; i++) {
        if(switchDir[i]) {
            if(tempf >= switchTemp[i]) {
                SetRelay(i, 1);
            }
            else if(tempf < switchTemp[i]) {
                SetRelay(i, 0);
            }
        }
        else {
            if(tempf < switchTemp[i]) {
                SetRelay(i, 1);
            }
            if(tempf >= switchTemp[i]) {
                SetRelay(i, 0);
            }
        }
    }
}

void SetRelay(int relay, int val) {
    digitalWrite(relayNum[relay-1],val);
    relayStatus[relay-1] = val;
}

int WebSetRelay(String extra) {
    int relay = extra.toInt();
    if (relay < 10) {
        SetRelay(relay,HIGH);
    }
    else if (relay > 10) {
        SetRelay(relay-10,LOW);
    }
        
    
    return RelayStatusPack();
}

int printEEPROM(String data) {
    int test[16];
    EEPROM.get(0,test);
    int index = 0;
    Particle.publish("skorn_stderr",String::format("Outputting EEPROM"));
    delay(1000);
    for(index = 0 ; index < 16 ; index++) {
        Particle.publish("skorn_stderr",String::format("%d:%d",index,test[index]));
        delay(1000);
    }
    
}

int scheduler(String data) {
    //Looking for relaynum:onHour:onminute:offhour:offminute
    int line[5];
    int index = 0;
    char buff[20];
    data.toCharArray(buff,20);
    const char s[2] = ":";
    char * token;
    
    token = strtok(buff, s);
    
    
    while(token != NULL) {
        line[index] = atoi(token);
        index++;
        token = strtok(NULL, s); 
        
    }
    
    Particle.publish("skorn_stderr",String::format("Parsing Bullshit %d %d %d %d %d", line[0],line[1],line[2],line[3],line[4]));
    
    int relayNum = line[0];
    int hourOn = line[1];
    int minuteOn = line[2];
    int hourOff = line[3];
    int minuteOff = line[4];
    
    sched[(relayNum-1)*4] = hourOn;
    sched[(relayNum-1)*4+1] = minuteOn;
    sched[(relayNum-1)*4+2] = hourOff;
    sched[(relayNum-1)*4+3] = minuteOff;
    
    
    EEPROM.put(0,sched);
    
}

void checkSchedule() {
    int current[16];
    EEPROM.get(0,current);
    int relay = 0;
    for(relay; relay < 4; relay++) {
        if(current[relay*4+0] == Time.hour() ) {
            if(current[relay*4+1] == Time.minute() ) {
                SetRelay(relay+1,HIGH);
            }
        }
        if(current[relay*4+2] == Time.hour() ) {
            if(current[relay*4+3] == Time.minute() ) {
                SetRelay(relay+1,LOW);
            }
        }
    }
}
int RelayStatusPack() {
    int pack = 0;
    for(int i = 0; i < NUM_RELAYS; i++) {
        pack |= relayStatus[i] << i;
    }
    return pack;
}



void GetWeather() {
  if (millis() > DHTnextSampleTime) {
	if (!bDHTstarted) {		// start the sample
	    Serial.print("\n");
	    Serial.print(n);
	    Serial.print(": Retrieving information from sensor: ");
	    DHT.acquire();
	    bDHTstarted = true;
	}
    if (!DHT.acquiring()) {		// has sample completed?

	// get DHT status
	int result = DHT.getStatus();

    humidity = DHT.getHumidity();
    Particle.publish("skorn_stderr",String::format("Humidity: %d",humidity));
	    
	tempf = DHT.getFahrenheit();
	Particle.publish("skorn_stderr",String::format("Temperature F: %d",tempf));
	    
    n++;  // increment counter
    bDHTstarted = false;  // reset the sample flag so we can take another
    DHTnextSampleTime = millis() + DHT_SAMPLE_INTERVAL;  // set the time for next sample
	}
  }
}
int WebRelayPack(String extra) {
    return RelayStatusPack();
}