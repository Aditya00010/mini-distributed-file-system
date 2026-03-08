# mini-distributed-file-system
A simplified implementation of a distributed file system inspired by Google File System (GFS) using Python, TCP sockets, chunk storage, and metadata management.
# Distributed File Storage System (MiniGFS)

## Overview
This project is a simplified implementation of a distributed file storage system inspired by the Google File System (GFS). It demonstrates how large files can be split into chunks and stored across multiple servers with replication and metadata management.

The system consists of one master server, multiple chunk servers, and a client. Communication between components is implemented using TCP sockets in Python.

## Architecture

Client → Master Server → Chunk Servers

- Client sends file operations
- Master manages metadata and chunk allocation
- Chunk servers store actual file chunks

## Components

### Master Server
Responsible for:
- Metadata management
- File chunk allocation
- Chunk server coordination

### Chunk Servers
Responsible for:
- Storing file chunks
- Handling read/write requests

### Client
Responsible for:
- Sending commands to the master server
- Fetching file chunks from servers

## Features

- Distributed file storage
- File chunking (64 byte chunks)
- Metadata management
- Chunk replication
- Fault tolerance
- TCP socket communication

## Technologies Used

- Python
- Socket Programming
- Distributed Systems Concepts
- File Chunking
- Replication

## Project Structure
MiniGFS
│
├── master.py
├── client.py
├── chunk_server.py
├── metadata.json
└── chunk_storage/
