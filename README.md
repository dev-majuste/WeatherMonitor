# WeatherMonitor

WeatherMonitor is an IoT environmental monitoring project that uses an ESP32-S3 to collect sensor data and send it to a FastAPI backend connected to a MySQL database.

The project is intended to provide a simple end-to-end monitoring system with embedded hardware, a REST API, data storage. A lightweight frontend is planned as a future addition.

## Project Structure

```text
WeatherMonitor/
├── api/
├── firmware/
├── README.md
└── LICENSE
```

- `api/` — FastAPI backend and database integration
- `firmware/` — ESP32 firmware and sensor handling

## Hardware

- ESP32-S3 N16R8
- BME280 — temperature, humidity and atmospheric pressure
- LDR sensor — luminosity
- Raindrop sensor — rain detection

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
