"""Flag event fixtures outside an explicit age window."""
import argparse,csv,io,json,math,re
from collections import Counter
from datetime import date,datetime
from pathlib import Path

def analyze(data):
    now=datetime.fromisoformat(data['as_of'].replace('Z','+00:00'));old=[];future=[]
    for row in data['events']:
        age=(now-datetime.fromisoformat(row['ts'].replace('Z','+00:00'))).total_seconds()
        if age>data['max_age_seconds']:old.append(row['id'])
        if age<0:future.append(row['id'])
    return {'too_old':sorted(old),'future':sorted(future)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path,help='UTF-8 JSON input file')
    parser.add_argument('--explain',action='store_true',help='Send the local report to the configured chat gateway')
    args=parser.parse_args()
    report=analyze(json.loads(args.input.read_text(encoding='utf-8')))
    if args.explain:
        from gateway_client import explain
        print(explain(report))
    else:print(json.dumps(report,ensure_ascii=False,indent=2))
