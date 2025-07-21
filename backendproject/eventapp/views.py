from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import os, time
from concurrent.futures import ThreadPoolExecutor


DATA_DIR = "events"
MAX_RESULTS = 10  

def parse_line(line):
    keys = ["serialno", "version", "account_id", "instance_id",
            "srcaddr", "dstaddr", "srcport", "dstport", "protocol",
            "packets", "bytes", "starttime", "endtime", "action", "log_status"]
    return dict(zip(keys, line.strip().split()))

def process_file(fname, query, start, end):
    results = []
    with open(os.path.join(DATA_DIR, fname)) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 15:
                continue
            event = parse_line(line)
            if start <= int(event["starttime"]) <= end:
                if '=' in query:
                    key, val = query.split("=")
                    if event.get(key) == val:
                        results.append({"event": event, "file": fname})
                elif query in line:
                    results.append({"event": event, "file": fname})

            if len(results) >= MAX_RESULTS:
                break
    return results

class SearchView(APIView):
    def get(self, request):
        query = request.GET.get("query", "")

        try:
            start = int(request.GET.get("start", 0) or 0)
        except ValueError:
            start = 0
        try:
            end = int(request.GET.get("end", 9999999999) or 9999999999)
        except ValueError:
            end = 9999999999

        t0 = time.time()
        files = [f for f in os.listdir(DATA_DIR) if f.startswith("x")]
        results = []

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_file, fname, query, start, end) for fname in files]
            for future in futures:
                for r in future.result():
                    results.append(r)
                    if len(results) >= MAX_RESULTS:
                        break
                if len(results) >= MAX_RESULTS:
                    break

        return Response({
            "results": results,
            "search_time": round(time.time() - t0, 2),
            "note": f"Showing top {MAX_RESULTS} results only"
        })


