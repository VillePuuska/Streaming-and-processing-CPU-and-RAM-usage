# Streaming and processing CPU and RAM usage; <br/> Learning Kafka and Flink

Initial idea and planned outline:
- Stream CPU and RAM usage measurements with one or more Python scripts to a Kafka topic.
- Multiple measurements per second.
- Process the stream with Flink to get aggregates per second (tumbling windows).
- Stream the window aggregate data from Flink to a Postgres table/Timescale hypertable.
- Visualize live and historical data with Streamlit.

![Project diagram](./diagram.png)

---

Setup before running the project:
- `poetry install`
- (optional) `docker compose --profile cc pull`

Running the project:
- If you don't want/need Control Center running: `docker compose up -d`
- If you DO want Control Center: `docker compose --profile cc up -d`
- Create the `measurements` topic:
```
docker exec kafka1 /bin/bash -c "kafka-topics --create --topic measurements --bootstrap-server localhost:9092"
```
- Activate the virtual environment with the dependencies of this project: `poetry shell`
- Start producing measurements: `python measurement_spammer/spam_measurements.py`
