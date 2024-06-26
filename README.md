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
- `poetry install` (add `--with dev` to include dev dependencies which are just `mypy` and stubs)
- Download the JARs needed by Flink. The list of URLs to download from Maven Repository are in the file `flink/needed_jar_urls.txt`. The JARs should be placed in the directory `jars/`, but if you want to place them in a different directory, you can pass the directory path as the parameter `--jar-path` when running the PyFlink script `flink/process_stream.py`
- (optional) `docker compose --profile cc pull`

Running the project (note: the instructions assume you're running the commands from the root of this repository):
- If you DON'T want/need Control Center running: `docker compose up -d`
- If you DO want Control Center: `docker compose --profile cc up -d`
- Create the `measurements` topic (alternatively you can use the flag `--allow-new-topic` when starting the producer script to create the topic):
```
docker exec kafka1 /bin/bash -c "kafka-topics --create --topic measurements --bootstrap-server localhost:9092"
```
- Open _two_ shells and activate the virtual environment with the dependencies of this project in _both_ of the shells: `poetry shell`
- Start producing measurements in one of the shells: `python measurement_spammer/spam_measurements.py` (add `--help` to see info on parameters).
- In the other shell, start the Flink job that processes the stream and sinks to Postgres/Timescale: `python flink/process_stream.py` (add `--help` to see info on parameters).
- To run and view the Streamlit app, open yet another shell, open the virtual environment with `poetry shell`, and run `python -m streamlit run app/main.py` to start the app. Then you can access the app at `localhost:8501` in your browser.
- You can pass parameters to the app by running `python -m streamlit run app/main.py -- --param`; note the extra `--`. Currently the supported parameters are:
  - `--refresh-interval (float)`: Interval for how often data on the page is refreshed. Default: 1.0
  - `--pg-conn (text)`: Postgres connection string. Default: `postgresql://postgres:postgres@localhost:5432/`

---

Running static type checks with `mypy`:
- `poetry install --with dev` if you didn't install dev dependencies already.
- `poetry shell`
- To check the Streamlit app code: `python -m mypy app/`
- To check the PyFlink script: `python -m mypy flink/`
- To check the sciprt that sends measurements to Kafka: `python -m mypy measurement_spammer/`

*Note:* `python -m mypy .` fails with `Duplicate module named "utils"` since there are `utils` modules under `app/` and `measurement_spammer/`.
