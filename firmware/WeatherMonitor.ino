#include <Wire.h>
#include <WiFi.h>
#include <WiFiManager.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>

#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define PIN_SDA 8
#define PIN_SCL 9
#define PIN_LDR 5
#define PIN_CHUVA 4

const char* API_URL = "";

const char* DEVICE_API_KEY = "";

const unsigned long INTERVALO_ENVIO = 10UL * 60UL * 1000UL;

unsigned long ultimoEnvio = 0;

Adafruit_BME280 bme;
WiFiManager wifiManager;

void conectarWiFi() {
  Serial.println("Conectando ao Wi-Fi...");

  bool conectado = wifiManager.autoConnect(
    "WeatherMonitor-Setup"
  );

  if (!conectado) {
    Serial.println("Falha ao conectar ao Wi-Fi.");
    Serial.println("Reiniciando ESP32...");

    delay(3000);
    ESP.restart();
  }

  Serial.println("Wi-Fi conectado!");

  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}


void enviarMedicao() {
  float temperatura = bme.readTemperature();
  float umidade = bme.readHumidity();
  float pressao = bme.readPressure() / 100.0F;

  int luminosidade = digitalRead(PIN_LDR);
  int chuva = analogRead(PIN_CHUVA);


  if (
    isnan(temperatura) ||
    isnan(umidade) ||
    isnan(pressao)
  ) {
    Serial.println("Erro ao ler BME280.");
    return;
  }

  Serial.println("---------------------------------------");

  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println(" C");

  Serial.print("Umidade: ");
  Serial.print(umidade);
  Serial.println(" %");

  Serial.print("Pressao: ");
  Serial.print(pressao);
  Serial.println(" hPa");

  Serial.print("Luminosidade: ");
  Serial.println(luminosidade);

  Serial.print("Chuva: ");
  Serial.println(chuva);

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi desconectado.");

    WiFi.reconnect();

    unsigned long inicio = millis();

    while (
      WiFi.status() != WL_CONNECTED &&
      millis() - inicio < 10000
    ) {
      delay(500);
      Serial.print(".");
    }

    Serial.println();

    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("Nao foi possivel reconectar.");
      return;
    }
  }

  WiFiClientSecure client;
  client.setInsecure();

  HTTPClient http;

  if (!http.begin(client, API_URL)) {
    Serial.println("Erro ao iniciar requisicao HTTP.");
    return;
  }

  http.addHeader(
    "Content-Type",
    "application/json"
  );

  http.addHeader(
    "X-Device-Key",
    DEVICE_API_KEY
  );

  String json = "{";

  json += "\"temperature\":";
  json += String(temperatura, 2);

  json += ",\"humidity\":";
  json += String(umidade, 2);

  json += ",\"pressure\":";
  json += String(pressao, 2);

  json += ",\"luminosity\":";
  json += String(luminosidade);

  json += ",\"raindrop\":";
  json += String(chuva);

  json += "}";

  Serial.println("Enviando para API:");
  Serial.println(json);

  int httpCode = http.POST(json);

  Serial.print("HTTP Status: ");
  Serial.println(httpCode);

  if (httpCode > 0) {
    Serial.println("Resposta:");

    Serial.println(
      http.getString()
    );
  } else {
    Serial.println("Erro na requisicao:");

    Serial.println(
      http.errorToString(httpCode)
    );
  }

  http.end();

  Serial.println("---------------------------------------");
}

void setup() {
  Serial.begin(115200);

  delay(2000);


  Wire.begin(
    PIN_SDA,
    PIN_SCL
  );

  pinMode(
    PIN_LDR,
    INPUT
  );

  pinMode(
    PIN_CHUVA,
    INPUT
  );

  if (!bme.begin(0x76, &Wire)) {
    Serial.println("BME280 nao encontrado!");

    while (true) {
      delay(1000);
    }
  }

  Serial.println("BME280 detectado!");

  conectarWiFi();

  enviarMedicao();

  ultimoEnvio = millis();
}

void loop() {
  if (
    millis() - ultimoEnvio >= INTERVALO_ENVIO
  ) {
    enviarMedicao();

    ultimoEnvio = millis();
  }

  delay(100);
}
