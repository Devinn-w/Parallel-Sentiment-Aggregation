# Parallel-Sentiment-Aggregation-for-Mastodon-NDJSON-Data-using-mpi4py

This project implements a **parallel sentiment aggregation pipeline** for large-scale Mastodon NDJSON datasets using Python's [`mpi4py`](https://mpi4py.readthedocs.io/) library.  
It distributes the processing of huge social media datasets across multiple cores or nodes, allowing efficient extraction and aggregation of **sentiment scores by hour and by user**.  
This project was originally developed as part of a cloud and cluster computing assignment, using real-world data (144 GB Mastodon dataset).

---

##  Features

-  **Parallel data processing** with MPI (Message Passing Interface)  
-  Handles **NDJSON** (Newline Delimited JSON) files efficiently  
-  Extracts **timestamp**, **user info**, and **sentiment scores** from each post  
-  Aggregates sentiment scores **per hour** and **per user**  
-  Scales well for benchmarking with different core/node configurations

---

## Tech Stack

| Component | Description |
|-----------|-------------|
| **Language** | Python 3 |
| **Parallelism** | [mpi4py](https://mpi4py.readthedocs.io/) |
| **Data Format** | NDJSON |
| **Libraries** | `mpi4py`, `json`, `datetime`, `collections` |

---


## How It Works

1. **MPI Initialization**  
   The script uses `mpi4py` to divide the input file into equal byte-sized chunks based on the number of processes.

2. **Parallel Chunk Processing**  
   Each MPI process reads its assigned file segment, parses each NDJSON line, and extracts:
   - ISO timestamp → converted to hour key  
   - User ID and username  
   - Sentiment score (float)

3. **Local Aggregation**  
   Each process maintains two dictionaries:
   - `hourly_stats`: sentiment totals grouped by hour  
   - `user_stats`: sentiment totals grouped by user

4. **Gather & Merge**  
   All local dictionaries are gathered at the **root process (rank 0)**, merged, and globally aggregated.

5. **Top-K Sentiment Analysis**  
   The script identifies:
   - Top 5 happiest and saddest **hours**
   - Top 5 happiest and saddest **users**

---

##  How to Run

### 1️ Install Dependencies

```bash
pip install mpi4py
