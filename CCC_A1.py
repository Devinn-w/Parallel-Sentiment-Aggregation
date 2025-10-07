from mpi4py import MPI
import json
import os
from collections import defaultdict
from datetime import datetime

def process_chunk(file_path, start, end, rank):
    hourly_stats = defaultdict(float)
    user_stats = defaultdict(float)

    with open(file_path, 'r', encoding='utf-8') as f:
        f.seek(start)
        if start != 0:
            f.readline()  

        while f.tell() < end:
            line = f.readline()
            if not line:
                break

        result = parse_and_extract_sentiment(line)
        if result:
                hour_key, user_key, sentiment = result
                update_stats(hour_key, user_key, sentiment, hourly_stats, user_stats)


    return hourly_stats, user_stats

def parse_and_extract_sentiment(line):
    try:
        data = json.loads(line).get('doc', {})
        created = data.get('createdAt')
        sentiment = data.get('sentiment', 0)
        account = data.get('account', {})
        uid = account.get('id')
        uname = account.get('username')

        if not (created and uid and uname):
            return None

        hour_key = datetime.fromisoformat(created.rstrip('Z')).strftime('%Y-%m-%dT%H')
        user_key = f"{uname} ({uid})"

        return hour_key, user_key, sentiment
    except (json.JSONDecodeError, KeyError, ValueError):
        return None


def update_stats(hour_key, user_key, sentiment, hourly_stats, user_stats):
    hourly_stats[hour_key] += sentiment
    user_stats[user_key] += sentiment

def get_chunk_range(file_path, rank, size):
    file_size = os.path.getsize(file_path)
    chunk_size = file_size // size
    start = rank * chunk_size
    end = (rank + 1) * chunk_size if rank != size - 1 else file_size
    return start, end


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()


    file_path = 'mastodon-144g.ndjson'
    start, end = get_chunk_range(file_path, rank, size)


    local_hourly, local_user = process_chunk(file_path, start, end, rank)

    all_hourly = comm.gather(local_hourly, root=0)
    all_users = comm.gather(local_user, root=0)

    if rank == 0:
        global_hourly = defaultdict(float)
        for h_dict in all_hourly:
            for hour, score in h_dict.items():
                global_hourly[hour] += score

        global_users = defaultdict(float)
        for u_dict in all_users:
            for user, score in u_dict.items():
                global_users[user] += score

        
        happiest_hours = sorted(global_hourly.items(), key=lambda x: -x[1])[:5]
        saddest_hours = sorted(global_hourly.items(), key=lambda x: x[1])[:5]
        happiest_users = sorted(global_users.items(), key=lambda x: -x[1])[:5]
        saddest_users = sorted(global_users.items(), key=lambda x: x[1])[:5]

        
        print("Happiest Hours:", happiest_hours)
        print("Saddest Hours:", saddest_hours)
        print("Happiest Users:", happiest_users)
        print("Saddest Users:", saddest_users)

if __name__ == "__main__":
    main()