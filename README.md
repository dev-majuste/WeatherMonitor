<p align="right">
  <a href="README.md">English</a> |
  <a href="README.pt-BR.md">Português (Brasil)</a>
</p>

# WeatherMonitor

WeatherMonitor is an IoT environmental monitoring project that uses an ESP32-S3 to collect sensor data and send it to a FastAPI backend connected to a MySQL database.

The project is intended to provide a simple end-to-end monitoring system with embedded hardware, a REST API, data storage and a lightweight frontend example.

## Project Structure

```text
WeatherMonitor/
├── api/
├── firmware/
├── frontend/
├── README.md
└── LICENSE
```

- `api/` — FastAPI backend and database integration
- `firmware/` — ESP32 firmware and sensor handling
- `frontend/` — Simple example frontend for displaying API data

## How It Works

The ESP32-S3 reads data from the connected sensors and sends a new measurement to the backend every 10 minutes using the REST API.

Measurements are sent to:

```text
POST /measurements
```

The ESP32 uses a `Device Key` to authenticate requests before measurements are stored in the MySQL database.

Stored measurements can then be retrieved through the API using the available `GET` endpoints. These requests require an API key and are subject to the request limit configured for that key.

The `frontend/` directory contains a simple example of an application that consumes these endpoints and displays the stored measurements.

## Hardware

- ESP32-S3 N16R8
- BME280 — temperature, humidity and atmospheric pressure
- LDR sensor — luminosity
- Raindrop sensor — rain detection

## API

The backend provides a REST API responsible for receiving, storing and retrieving environmental measurements collected by the ESP32-S3.

Measurements are stored in the database and returned by the API in JSON format.

A single measurement follows this format:

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

Endpoints that return more than one measurement return a JSON array containing multiple objects in the same format.

The API uses three different types of keys for different purposes.

The `Device Key` is used by the ESP32 when sending new measurements to the server. It is included in the `X-Device-Key` HTTP header and is used to make sure that only an authorized device can send data to the API.

The `Admin Key` is used for administrative operations, mainly for creating and managing API keys. It is included in the `X-Admin-Key` HTTP header.

The `API Keys` are the keys provided to users who need to retrieve measurement data. They are included in the `X-API-Key` HTTP header.

Each `API Key` can have its own request-per-minute limit and can also be enabled or disabled individually. This allows the server to control how many requests each key can make and helps prevent excessive API usage.

## Endpoints

`POST /measurements`

Used by the ESP32 to send a new measurement to the server.

The request must include the `Device Key` in the `X-Device-Key` header.

The request body must contain the sensor data in JSON format:

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

Returns the latest measurement stored in the database.

`GET /measurements/day`

Returns the measurements from the current day when no parameter is provided.

A specific date can also be requested:

```text
/measurements/day?date=2026-09-10
```

The date must use the format:

```text
YYYY-MM-DD
```

`GET /measurements/week`

Returns the measurements from the last 7 days.

`GET /measurements/month`

Returns the measurements from the last 30 days when no parameters are provided.

A specific month and year can also be requested:

```text
/measurements/month?month=9&year=2026
```

All measurement retrieval endpoints require a valid `API Key` in the `X-API-Key` header.

## Frontend

The `frontend/` directory contains a simple example of how data returned by the API can be displayed using HTML, CSS and JavaScript.

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
