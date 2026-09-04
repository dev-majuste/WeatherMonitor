#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

// Define os pinos I2C padrão da ESP32-S3
#define PIN_SDA 8
#define PIN_SCL 9
#define PIN_LDR 5
#define PIN_CHUVA 4

Adafruit_BME280 bme; // Cria o objeto do sensor

void setup() {
  // Inicia a comunicação serial para exibir os dados no computador
  Serial.begin(115200);
  while(!Serial); // Aguarda a abertura do Monitor Serial
  Serial.println("--- Teste do Sensor BME280 com ESP32-S3 ---");

  // Inicializa o barramento I2C com os pinos corretos da ESP32-S3
  Wire.begin(PIN_SDA, PIN_SCL);
  pinMode(PIN_LDR, INPUT);
  pinMode(PIN_CHUVA, INPUT);

  // Inicializa o sensor BME280 no endereço padrão 0x76
  // Se não funcionar, mude o valor abaixo para 0x77
  if (!bme.begin(0x76, &Wire)) {
    Serial.println("Erro: Não foi possível encontrar o sensor BME280!");
    Serial.println("Verifique as conexões de fiação e alimentação (3.3V).");
    while (1); // Trava o programa se houver erro
  }

  Serial.println("Sensor BME280 detectado com sucesso!");
}

void loop() {
  // Realiza a leitura e armazena nas variáveis
  float temperatura = bme.readTemperature();
  float umidade = bme.readHumidity();
  float pressao = bme.readPressure() / 100.0F; // Converte de Pascal para hPa
  int estadoLuz = digitalRead(PIN_LDR);
  int chuva = analogRead(PIN_CHUVA);

  // Exibe os resultados no Monitor Serial
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println(" *C");

  Serial.print("Umidade:     ");
  Serial.print(umidade);
  Serial.println(" %");

  Serial.print("Pressão:     ");
  Serial.print(pressao);
  Serial.println(" hPa");

  Serial.print("Luz:          ");
  if (estadoLuz == HIGH) {
    Serial.println("Noite");
  } else {
    Serial.println("Dia");
  }
  Serial.print("Chuva:        ");
  Serial.println(chuva);
  Serial.println("---------------------------------------");

  // Aguarda 2 segundos antes da próxima leitura
  delay(2000);
}