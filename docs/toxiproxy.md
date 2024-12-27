# Simulations with Toxiproxy

Toxiproxy is a powerful tool for simulating network conditions, particularly useful for testing S3 interactions in this project. This guide focuses on using Toxiproxy to simulate network delays with jitter, which is crucial for testing minute_batches and evaluating the effectiveness of prefetching minute_batches.

## Setting up Toxiproxy

1. Install Toxiproxy:
```sh
brew tap shopify/shopify
brew install toxiproxy
```

2. Install Toxiproxy CLI:
```sh
wget https://github.com/Shopify/toxiproxy/releases/download/v2.11.0/toxiproxy-cli-darwin-arm64 -O toxiproxy-cli
chmod +x toxiproxy-cli
```

3. Create a proxy for Minio:
```sh
toxiproxy-cli create -l localhost:29000 -u localhost:9000 minio
```

Now you can access Minio through port 29000. Test it with:
```sh
aws --endpoint-url http://localhost:29000 --profile minio s3 ls
```

## Simulating Network Delays with Jitter

To simulate realistic network conditions:

1. Add latency with jitter to the Minio proxy:
```sh
toxiproxy-cli toxic add -t latency -a latency=500 -a jitter=50 minio
```
This adds a 500ms delay with ±50ms jitter to all requests.

2. Verify the configuration:
```sh
toxiproxy-cli ls
toxiproxy-cli inspect minio
```

Example output:
```
❯ toxiproxy-cli ls
Name            Listen          Upstream        Enabled     Toxics
======================================================================================
minio           127.0.0.1:29000 localhost:9000   enabled     1

❯ toxiproxy-cli inspect minio
Name: minio    Listen: 127.0.0.1:29000    Upstream: localhost:9000
======================================================================
Upstream toxics:
Proxy has no Upstream toxics enabled.

Downstream toxics:
latency_downstream:    type=latency    stream=downstream    toxicity=1.00    attributes=[    jitter=50    latency=500    ]
```

3. Remove the delay when done:
```sh
toxiproxy-cli toxic remove -n latency_downstream minio
```

## Troubleshooting

If you encounter issues:
- Ensure Toxiproxy is running (`toxiproxy-server`)
- Check proxy status with `toxiproxy-cli list`
- Restart Toxiproxy if needed

For more advanced configurations, refer to the [Toxiproxy documentation](https://github.com/Shopify/toxiproxy).
