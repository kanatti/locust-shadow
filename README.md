# On-Demand Traffic Shadow System

## Project Overview
This project aims to create an on-demand traffic shadow system based on production logs using Locust. The system will replay traffic patterns from production environments in a controlled manner, allowing for testing and analysis of application behavior under realistic load conditions.

## Key Components

1. **Minute-Batches**: 
   - Minutely traffic data extracted from production logs
   - Named as `minute_0`, `minute_1`, etc., for flexible start times

2. **Locust-based Executor**:
   - Utilizes Locust for load generation
   - Executes traffic patterns based on minute-batch data

3. **Synchronization Mechanism**:
   - Manages distributed workers
   - Potential use of Redis or other sync providers

## High-Level Architecture

```
[Production Logs] -> [Log Processor] -> [Minute-Batches]
                                              |
                                              v
[Redis/Sync Provider] <-> [Locust Master] <-> [Locust Workers]
                                              |
                                              v
                                        [Target System]
```

## Getting Started
(To be added: installation instructions, configuration details, and usage examples)

## Development Roadmap
1. Implement log processing and minute-batch generation
2. Develop Locust-based executor for replaying traffic
3. Implement synchronization mechanism for distributed workers
4. Create configuration system for flexible deployment
5. Develop monitoring and reporting features

## Contributing
(To be added: guidelines for contributing to the project)

## License
This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.
