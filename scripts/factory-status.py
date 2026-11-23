#!/usr/bin/env python3
"""Read a feature issue's child issue states and the repository's open PRs."""
import argparse
import json
import re
import subprocess
import sys


def gh(*args):
    result = subprocess.run(['gh', *args], text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or 'gh command failed')
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description='Show GitHub feature and child issue status')
    parser.add_argument('issue', type=int, help='parent feature issue number')
    args = parser.parse_args()
    if args.issue <= 0:
        parser.error('issue number must be positive')
    try:
        parent = gh('issue', 'view', str(args.issue), '--json', 'number,title,state,body,url')
        body = parent.get('body') or ''
        section = re.search(r'^## 子Issueと進捗\s*$([\s\S]*?)(?=^##\s|\Z)', body, re.M)
        if not section:
            raise RuntimeError('親Issueに「## 子Issueと進捗」がありません')
        children = list(dict.fromkeys(re.findall(r'^\s*- \[[ xX]\] #([1-9][0-9]*)\b', section.group(1), re.M)))
        if not children:
            raise RuntimeError('子Issueがありません。各行を「- [ ] #番号」で記載してください')
        if str(args.issue) in children:
            raise RuntimeError('親Issue自身が子Issueに含まれています')
        issues = [gh('issue', 'view', number, '--json', 'number,title,state,url') for number in children]
        prs = gh('pr', 'list', '--state', 'open', '--limit', '100', '--json', 'number,title,headRefName,url')
    except (OSError, RuntimeError, ValueError) as error:
        print(f'確認できません: {error}', file=sys.stderr)
        return 1
    print(f"親 #{parent['number']} [{parent['state']}] {parent['title']} {parent['url']}")
    for issue in issues:
        print(f"  子 #{issue['number']} [{issue['state']}] {issue['title']} {issue['url']}")
    print('Open PR（最大100件。競合とIssueとの対応は個別に確認）:')
    for pr in prs:
        print(f"  #{pr['number']} {pr['headRefName']} {pr['title']} {pr['url']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
