# Mini Distributed File System (MiniGFS)

## Execution Guide

This document explains how to run and test the **Mini Distributed File
System** project. The system simulates a simplified version of the
**Google File System (GFS)** using Python.

------------------------------------------------------------------------

# 1. Project Overview

The system consists of three main components:

1.  **Master Server**
    -   Maintains metadata
    -   Tracks chunk locations
    -   Coordinates client requests
2.  **Chunk Servers**
    -   Store file chunks
    -   Handle read/write requests
3.  **Client**
    -   Sends commands to the master server
    -   Retrieves file chunks from servers

------------------------------------------------------------------------

# 2. System Architecture

Client → Master Server → Chunk Servers

Components:

-   1 Master Server
-   5 Chunk Servers
-   1 Client

Communication is implemented using **TCP sockets**.

------------------------------------------------------------------------

# 3. Project Folder Structure

    MiniGFS/
    │
    ├── master.py
    ├── client.py
    ├── chunk_server.py
    ├── metadata.json
    └── chunk_storage/

------------------------------------------------------------------------

# 4. Requirements

Make sure the following are installed:

-   Python 3.8 or later
-   VS Code or any Python IDE

Check Python version:

    python --version

------------------------------------------------------------------------

# 5. Running the System

The system must be started in the correct order.

## Step 1 -- Start Master Server

Open a terminal and run:

    python master.py

Expected output:

    Master server running on port 8000

Leave this terminal running.

------------------------------------------------------------------------

## Step 2 -- Start Chunk Servers

Open **five separate terminals** and run:

Terminal 1

    python chunk_server.py 8001

Terminal 2

    python chunk_server.py 8002

Terminal 3

    python chunk_server.py 8003

Terminal 4

    python chunk_server.py 8004

Terminal 5

    python chunk_server.py 8005

Each terminal should display:

    Chunk server running on port XXXX

------------------------------------------------------------------------

## Step 3 -- Start the Client

Open another terminal and run:

    python client.py

------------------------------------------------------------------------

# 6. Available Commands

Once the client starts, you can use the following commands.

### Create File

    CREATE test.txt

Creates a new file in the distributed system.

------------------------------------------------------------------------

### Write Data

    WRITE test.txt Hello Distributed Systems

Writes data to the file.

------------------------------------------------------------------------

### Read File

    READ test.txt

The client will retrieve chunks from chunk servers and reconstruct the
file.

------------------------------------------------------------------------

### Upload File

    UPLOAD data.txt

Uploads a file from the local directory into the distributed system.

------------------------------------------------------------------------

# 7. How the System Works

1.  Client sends a request to the master server.
2.  Master server splits files into **64-byte chunks**.
3.  Chunks are distributed across chunk servers.
4.  Metadata is stored in **metadata.json**.
5.  Chunk replicas are stored on multiple servers for fault tolerance.
6.  During read operations, the client retrieves chunks and reconstructs
    the file.

------------------------------------------------------------------------

# 8. Fault Tolerance

Each chunk is replicated across multiple chunk servers.

If one server fails, another replica can still provide the data.

------------------------------------------------------------------------

# 9. Stopping the System

To stop the system:

Press:

    CTRL + C

in each terminal.

------------------------------------------------------------------------

# 10. Future Improvements

Possible improvements include:

-   Load balancing between chunk servers
-   Dynamic server scaling
-   Web interface for file management
-   Distributed metadata storage

------------------------------------------------------------------------

# Author

Distributed File Storage System Implementation in Python.
