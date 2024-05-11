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
- `poetry install` (add `--with dev` to include dev dependencies which are just stubs)
- Download the JARs needed by Flink. The list of URLs to download from Maven Repository are in the file `flink/needed_jar_urls.txt`. The JARs should be placed in the directory `jars/`, but if you want to place them in a different directory, you can pass the directory path as the parameter `--jar-path` when running the Flink script `flink/process_stream.py`
- (optional) `docker compose --profile cc pull`

Running the project (note: the instructions assume you're running the commands from the root of this repository):
- If you DON'T want/need Control Center running: `docker compose up -d`
- If you DO want Control Center: `docker compose --profile cc up -d`
- Create the `measurements` topic (alternatively you can use the flag `--allow-new-topic` when starting the producer script to create the topic):
```
docker exec kafka1 /bin/bash -c "kafka-topics --create --topic measurements --bootstrap-server localhost:9092"
```
- Open _two_ shells and activate the virtual environment with the dependencies of this project in _both_ of the shells: `poetry shell`
- Start producing measurements in one of the shells: `python measurement_spammer/spam_measurements.py` (add `--help` to see info on parameters)
- In the other shell, start the Flink job that processes the stream and sinks to Postgres/Timescale: `python flink/process_stream.py` (add `--help` to see info on parameters)
- To run and view the Streamlit app, run `python -m streamlit run app/main.py` and open `localhost:8501` in your browser
