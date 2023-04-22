const int LINE[8] = {2,3,4,5,6,7,8,9};
const int ROW[8] = {10,11,12,13,14,15,16,17};

const int SHOW_DELAY = 2;
byte data[8] = {0,0,0,0,0,0,0,0};

byte cmd;
byte args[8];

int disconnectDelay = 10000;
unsigned long lastPacket;

void setup() {
    Serial.begin(115200);

    for(byte i = 0; i < 8; i++){
        pinMode(LINE[i], OUTPUT);
        pinMode(ROW[i], OUTPUT);

        digitalWrite(LINE[i], LOW);
        digitalWrite(ROW[i], HIGH);
    }

    lastPacket = millis();
}

void loop() {
    checkConnected();
    showData();
    recvCmd();
}

void showData() {
    for (byte i=0; i<8; i++) {
        if (data[i] != 0) {
            for (byte j=0; j<8; j++) {
                if (data[i] & (128>>j)) {
                    digitalWrite(ROW[j], LOW);
                } else {
                    digitalWrite(ROW[j], HIGH);
                }
            }
            digitalWrite(LINE[i], HIGH);
            delay(SHOW_DELAY);
            digitalWrite(LINE[i], LOW);
        } else {
            delay(SHOW_DELAY);
        }
    }
}

void recvCmd() {
    if (Serial.available() >= 9) {
        cmd = Serial.read();
        Serial.readBytes(args, 8);

        while (Serial.available()) {
            Serial.read();
        }

        switch (cmd) {
            case 80:  // Letter P
                ping();
                break;

            case 83:  // Letter S
                setData(args);
                break;

            case 71:  // Letter G
                getData();
                break;
        }
        lastPacket = millis();
    }
}

void checkConnected() {
    if (lastPacket + disconnectDelay < millis()) {
        for (byte i=0; i<8; i++) {
            data[i] = 0;
        }
        lastPacket = 4294967294;
        digitalWrite(13, LOW);
    }
}

void ping() {
    Serial.print("ACK");
}

void setData(byte arg[8]) {
    for (byte i=0; i<8; i++) {
        data[i] = arg[i];
    }

    byte nb = 0;
    for (byte i=0; i<8; i++) {
        for (byte j=0; j<8; j++) {
            if (data[i] & (128>>j)) {
                nb += 1;
            }
        }
    }

    Serial.write(nb);
}

void getData() {
    for (byte i=0; i<8; i++) {
        Serial.write(data[i]);
    }
}
