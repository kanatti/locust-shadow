# Simulations with Toxiproxy

Toxiproxy is a tool for simulating network conditions, particularly useful for testing S3 interactions in this project. This guide focuses on using Toxiproxy to simulate network delays with jitter, which is crucial for testing minute_batches and evaluating the effectiveness of prefetching minute_batches.

## Setting up Toxiproxy

1. Run Toxiproxy in a Docker container:

   ```sh
   docker run -d --name toxiproxy \
     -p 8474:8474 \
     -p 9000:9000 \
     -p 9001:9001 \
     shopify/toxiproxy
   ```

2. Create proxies for Minio:

   ```sh
   toxiproxy-cli create minio -l 0.0.0.0:9000 -u minio:9000
   toxiproxy-cli create minio-console -l 0.0.0.0:9001 -u minio:9001
   ```

## Simulating Network Delays with Jitter

To simulate realistic network conditions, we can add latency with jitter to the Minio proxy:

```sh
toxiproxy-cli toxic add minio -t latency -a latency=100 -a jitter=50
```

This adds a 100ms delay with ±50ms jitter to all requests going through the Minio proxy.

## Testing minute_batches with Network Delays

When testing minute_batches, we can simulate scenarios where fetching each batch experiences variable latency:

```sh
# Add base latency with jitter
toxiproxy-cli toxic add minio -t latency -a latency=50 -a jitter=25

# Simulate a spike in latency for a specific period
toxiproxy-cli toxic update minio -n latency -a latency=500 -a jitter=100
sleep 60
toxiproxy-cli toxic update minio -n latency -a latency=50 -a jitter=25
```

## Testing Prefetch Effectiveness

Once the prefetch feature for minute_batches is implemented, we can evaluate its effectiveness:

1. Run the application without prefetching:

   ```sh
   toxiproxy-cli toxic add minio -t latency -a latency=200 -a jitter=50
   # Run the application and measure performance
   ```

2. Enable prefetching and run the same test:

   ```sh
   toxiproxy-cli toxic update minio -n latency -a latency=200 -a jitter=50
   # Run the application with prefetching and measure performance
   ```

By comparing the performance metrics between these scenarios, we can quantify the benefits of prefetching minute_batches under realistic network conditions.

Remember to remove or update toxics as needed:

```sh
toxiproxy-cli toxic remove minio -n latency
```

Using Toxiproxy in this manner allows for comprehensive testing of S3 interactions in this project, especially in the context of minute_batches and prefetching, ensuring the application performs well under various network conditions.
