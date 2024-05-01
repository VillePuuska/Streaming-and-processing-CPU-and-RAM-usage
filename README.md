# Streaming and processing CPU and RAM usage; <br/> Learning Kafka and Flink

Initial idea and planned outline:
- Stream CPU and RAM usage measurements with one or more Python scripts to a Kafka topic.
- Multiple measurements per second.
- Process the stream with Flink to get aggregates per second (tumbling windows).
- Stream the window aggregate data from Flink to a Postgres table/Timescale hypertable.
- Visualize live and historical data with Streamlit.

