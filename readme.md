# Python TCP Server Project

This project implements a TCP server in Python. It includes functionalities for handling markers and passings as per configured protocols for MyLaps TCP exporter.

## Getting Started

These instructions will get your copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Docker installed on your local system. You can download and install Docker from [Docker's official website](https://www.docker.com/get-started).

### Running the application with Docker

Build the Docker image:

```bash
docker build -t python-tcp-server .
```

Run the Docker container:

```bash
docker run --rm -it -p 3097:3097 python-tcp-server
```
