"""GRI institutional assurance research prototype. Python 3.10+; standard library only."""
import argparse
import json
import math
from pathlib import Path

FEATURES = ('privilege_count','unapproved_tool_calls','unpatched_critical','unexpected_egress','missing_attestations')

def fit(records):
    if len(records) < 3:
        raise ValueError('At least three baseline records required')
    stats = {}
    for feature in FEATURES:
        values = [float(r[feature]) for r in records]
        mean = sum(values)/len(values)
        std = math.sqrt(sum((v-mean)**2 for v in values)/len(values))
        stats[feature] = {'mean':mean,'std':max(std,0.5)}
    return stats

def evaluate(record, baseline):
    findings = []
    for field in FEATURES:
        if field not in record or not isinstance(record[field], (int,float)) or isinstance(record[field],bool) or record[field]<0:
            raise ValueError(f'Invalid or missing nonnegative numeric field: {field}')
    if record.get('production') and not record.get('human_approval'):
        findings.append('Production deployment lacks recorded human approval')
    if record['unapproved_tool_calls'] > 0:
        findings.append('Unapproved tool invocation detected')
    if record['unpatched_critical'] > 0:
        findings.append('Unpatched critical component reported; verify applicability')
    if record['missing_attestations'] > 0:
        findings.append('Required assurance evidence missing')
    if record['unexpected_egress'] > 0:
        findings.append('Unexpected network egress reported')
    scores = {k:max(0,(record[k]-baseline[k]['mean'])/baseline[k]['std']) for k in FEATURES}
    anomaly = max(scores.values())
    return {'decision':'BLOCK' if findings else 'REVIEW' if anomaly>=3 else 'PASS',
            'anomaly_score':round(anomaly,3), 'findings':findings,
            'feature_scores':{k:round(v,3) for k,v in scores.items()},
            'disclaimer':'Research screening only; not a security certification or proof of compromise.'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--baseline',required=True)
    parser.add_argument('--input',required=True)
    args=parser.parse_args()
    baseline_records=json.loads(Path(args.baseline).read_text())
    record=json.loads(Path(args.input).read_text())
    result=evaluate(record,fit(baseline_records))
    print(json.dumps(result,indent=2))
    return 2 if result['decision']=='BLOCK' else 1 if result['decision']=='REVIEW' else 0

if __name__=='__main__':
    raise SystemExit(main())
