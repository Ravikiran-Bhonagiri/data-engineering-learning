# aggregator.py
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

def main():
    # 1. Setup Environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    t_env = StreamTableEnvironment.create(env)

    # 2. Define Source Table (Kafka)
    # We use Flink SQL to define the schema and connection to Kafka
    t_env.execute_sql("""
        CREATE TABLE trades (
            symbol STRING,
            price DOUBLE,
            quantity INT,
            ts TIMESTAMP(3),
            WATERMARK FOR ts AS ts - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'trades',
            'properties.bootstrap.servers' = 'broker:29092',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
    """)

    # 3. Define Sink Table (Print to Console/Logs for demo)
    t_env.execute_sql("""
        CREATE TABLE print_sink (
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            symbol STRING,
            total_volume INT
        ) WITH (
            'connector' = 'print'
        )
    """)

    # 4. Define Logic (Tumbling Window Aggregation)
    # "Group by Symbol and 10-second Window, calculate Sum(Quantity)"
    t_env.execute_sql("""
        INSERT INTO print_sink
        SELECT
            TUMBLE_START(ts, INTERVAL '10' SECOND) as window_start,
            TUMBLE_END(ts, INTERVAL '10' SECOND) as window_end,
            symbol,
            SUM(quantity) as total_volume
        FROM trades
        GROUP BY
            TUMBLE(ts, INTERVAL '10' SECOND),
            symbol
    """)

if __name__ == '__main__':
    main()
