# Warm-up Stage

## Overview

For high-volume shadow testing, it might be required to prepare the system with a warm-up stage before moving to the detailed minute-batch traffic patterns. This document outlines the warm-up configuration and behavior.

## Warm-up Configuration

The warm-up stage is defined in a separate configuration file, typically named `warmup-config.yml`. This separation allows for independent execution of the warm-up phase when needed. Here's an example structure:

```yaml
host: http://example.com
start_rps: 10
rps_increment: 20
step_duration: 60  # seconds
end_rps: 100
request_files:
  - ./warmup/requests1.jsonl
  - ./warmup/requests2.jsonl
```

### Configuration Parameters

- `host`: The target host for the warm-up requests.
- `start_rps`: Initial requests per second at the beginning of warm-up.
- `rps_increment`: How much to increase the RPS after each step.
- `step_duration`: Duration of each step in the warm-up phase, in seconds.
- `end_rps`: Target RPS to reach or exceed, which will end the warm-up phase.
- `request_files`: List of JSONL files containing sample requests for warm-up.

## Warm-up Behavior

1. **Request Selection**: 
   - Requests are randomly selected from the provided `request_files`.
   - Each file should be in JSONL format, with each line representing a single request.

2. **RPS Ramping**:
   - The RPS will start at `start_rps` and increase by `rps_increment` after each step.
   - Each step will last for `step_duration` seconds.
   - The warm-up phase will continue until the RPS reaches or exceeds `end_rps`.
   - The actual end RPS might be higher than `end_rps` if the last increment pushes it over.

3. **Duration**:
   - The total warm-up phase duration will depend on how many steps are needed to reach `end_rps`.
   - It can be calculated as: ceil((end_rps - start_rps) / rps_increment) * step_duration

## Usage

The warm-up phase can be run independently of the shadow testing using a separate command or script. This allows for flexibility in when and how often the warm-up is performed.

## Calculation Example

Given the configuration:
- start_rps: 10
- rps_increment: 20
- step_duration: 60 seconds
- end_rps: 100

The warm-up will proceed as follows:
1. Step 1: 10 RPS for 60 seconds
2. Step 2: 30 RPS for 60 seconds
3. Step 3: 50 RPS for 60 seconds
4. Step 4: 70 RPS for 60 seconds
5. Step 5: 90 RPS for 60 seconds
6. Step 6: 110 RPS for 60 seconds (exceeds end_rps, so this is the final step)

Total duration: 6 * 60 = 360 seconds
Final RPS: 110

This warm-up mechanism ensures that the system under test is properly prepared for high-volume traffic, improving the accuracy and reliability of subsequent shadow tests.
