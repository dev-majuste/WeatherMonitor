[English](README.md) | [Português (Brasil)](README.pt-BR.md)

# WeatherMonitor

WeatherMonitor é um projeto IoT de monitoramento ambiental que utiliza um ESP32-S3 para coletar dados de sensores e enviá-los para um backend FastAPI conectado a um banco de dados MySQL.

O projeto tem como objetivo fornecer um sistema simples e completo de monitoramento, utilizando hardware embarcado, uma API REST, armazenamento de dados e um exemplo de frontend leve.

## Estrutura do Projeto

```text
WeatherMonitor/
├── api/
├── firmware/
├── frontend/
├── README.md
└── LICENSE
```

- `api/` — Backend FastAPI e integração com o banco de dados
- `firmware/` — Firmware do ESP32 e gerenciamento dos sensores
- `frontend/` — Exemplo simples de frontend para exibir os dados da API

## Como Funciona

O ESP32-S3 lê os dados dos sensores conectados e envia uma nova medição para o backend a cada 10 minutos utilizando a API REST.

As medições são enviadas para:

```text
POST /measurements
```

O ESP32 utiliza uma `Device Key` para autenticar as requisições antes que as medições sejam armazenadas no banco de dados MySQL.

As medições armazenadas podem ser recuperadas através da API utilizando os endpoints `GET` disponíveis. Essas requisições exigem uma API Key e estão sujeitas ao limite de requisições configurado para essa chave.

O diretório `frontend/` contém um exemplo simples de uma aplicação que consome esses endpoints e exibe as medições armazenadas.

## Hardware

- ESP32-S3 N16R8
- BME280 — temperatura, umidade e pressão atmosférica
- Sensor LDR — luminosidade
- Sensor de chuva — detecção de chuva

## API

O backend fornece uma API REST responsável por receber, armazenar e recuperar as medições ambientais coletadas pelo ESP32-S3.

As medições são armazenadas no banco de dados e retornadas pela API no formato JSON.

Uma única medição segue este formato:

```json
{
  "id": 57,
  "temperature": 20.78,
  "humidity": 74.03,
  "pressure": 949.47,
  "luminosity": 0,
  "raindrop": 2285,
  "timestamp": "2026-09-10T21:54:41"
}
```

Endpoints que retornam mais de uma medição retornam um array JSON contendo vários objetos no mesmo formato.

A API utiliza três tipos diferentes de chaves para diferentes finalidades.

A `Device Key` é utilizada pelo ESP32 ao enviar novas medições para o servidor. Ela é incluída no cabeçalho HTTP `X-Device-Key` e é utilizada para garantir que apenas um dispositivo autorizado possa enviar dados para a API.

A `Admin Key` é utilizada para operações administrativas, principalmente para criar e gerenciar API Keys. Ela é incluída no cabeçalho HTTP `X-Admin-Key`.

As `API Keys` são as chaves fornecidas aos usuários que precisam consultar os dados das medições. Elas são incluídas no cabeçalho HTTP `X-API-Key`.

Cada `API Key` pode ter seu próprio limite de requisições por minuto e também pode ser ativada ou desativada individualmente. Isso permite que o servidor controle quantas requisições cada chave pode realizar e ajuda a evitar o uso excessivo da API.

## Endpoints

`POST /measurements`

Utilizado pelo ESP32 para enviar uma nova medição ao servidor.

A requisição deve incluir a `Device Key` no cabeçalho `X-Device-Key`.

O corpo da requisição deve conter os dados dos sensores no formato JSON:

```json
{
  "temperature": 20.78,
  "humidity": 74.03,
  "pressure": 949.47,
  "luminosity": 0,
  "raindrop": 2285
}
```

`GET /measurements/latest`

Retorna a medição mais recente armazenada no banco de dados.

`GET /measurements/day`

Retorna as medições do dia atual quando nenhum parâmetro é informado.

Também é possível consultar uma data específica:

```text
/measurements/day?date=2026-09-10
```

A data deve utilizar o formato:

```text
YYYY-MM-DD
```

`GET /measurements/week`

Retorna as medições dos últimos 7 dias.

`GET /measurements/month`

Retorna as medições dos últimos 30 dias quando nenhum parâmetro é informado.

Também é possível consultar um mês e ano específicos:

```text
/measurements/month?month=9&year=2026
```

Todos os endpoints de consulta de medições exigem uma `API Key` válida no cabeçalho `X-API-Key`.

## Frontend

O diretório `frontend/` contém um exemplo simples de como os dados retornados pela API podem ser exibidos utilizando HTML, CSS e JavaScript.

## Licença

Este projeto é licenciado sob a licença MIT.

Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
