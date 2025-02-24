#!/usr/bin/env python

import argparse
import re
import subprocess
import sys

from natsort import natsorted


class RadonConfig:
    def __init__(self):
        self.metric_config = {
            'complexity'  : {'error': 15,          'warn': 10},
            'difficulty'  : {'error': 8,           'warn': 6},
            'effort'      : {'error': 300,         'warn': 200},
            # 'length_ratio': {'error': (0.66, 1.5), 'warn': (0.75, 1.3)},
            'time'        : {'error': 60,          'warn': 45},
            'volume'      : {'error': 1000,        'warn': 800},
        }

    def update_from_args(self, args):
        for metric in self.metric_config:
            if hasattr(args, f'error_{metric}'):
                self.metric_config[metric]['error'] = getattr(args, f'error_{metric}')

            if hasattr(args, f'warn_{metric}'):
                self.metric_config[metric]['warn'] = getattr(args, f'warn_{metric}')


def parse_radon_output(output: str) -> dict[str, dict[str, float]]:
    pattern = re.compile(
        r'^(.+\.py):\s*'
        r'h1:\s(\d+)\s*?'
        r'h2:\s(\d+)\s*?'
        r'N1:\s(\d+)\s*?'
        r'N2:\s(\d+)\s*?'
        r'vocabulary:\s(\d+)\s*?'
        r'length:\s(\d+)\s*'
        r'calculated_length:\s(\d+\.\d+)\s*'
        r'volume:\s([\d.]+)\s*'
        r'difficulty:\s([\d.]+)\s*'
        r'effort:\s([\d.]+)\s*'
        r'time:\s([\d.]+)\s*'
        r'bugs:\s([\d.]+)\s*',
        re.MULTILINE
    )

    results = {}
    for match in pattern.finditer(output):
        groups = match.groups()
        results[groups[0]] = {
            'calculated_length' : float(groups[7]),
            'bugs'              : float(groups[12]),
            'difficulty'        : float(groups[9]),
            'effort'            : float(groups[10]),
            'length'            : int(groups[6]),
            'length_ratio'      : (int(groups[6]) / float(groups[7])) if float(groups[7]) else .0,
            'time'              : float(groups[11]),
            'volume'            : float(groups[8])}
    return results


def check_metrics(
    file_metrics: dict[str, float],
    config      : RadonConfig,

) -> tuple[list[str], list[str]]:

    errors = []
    warnings = []

    for metric, values in config.metric_config.items():

        value = file_metrics.get(metric)
        if value is None:
            continue

        if isinstance(values['error'], list | tuple):  # Range check

            lower, upper = values['error']
            if not (lower <= value <= upper):
                errors.append(f'{metric} {value:.2f} outside {lower:.2f}..{upper:.2f}')

            lower, upper = values['warn']
            if not (lower <= value <= upper):
                warnings.append(f'{metric} {value:.2f} outside {lower:.2f}..{upper:.2f}')

            continue

        if value >= values['error']:
            errors.append(f"{metric} {value:.2f} >= {values['error']:.2f}")

        elif value >= values['warn']:
            warnings.append(f"{metric} {value:.2f} >= {values['warn']:.2f}")

    return warnings, errors


def main():
    parser = argparse.ArgumentParser(description='Radon pre-commit hook with configurable metrics')
    parser.add_argument('files', nargs='*', help='List of files to check')

    parser.add_argument('--warn-difficulty', type=float, default=8.0)
    parser.add_argument('--warn-effort', type=float, default=300.0)
    parser.add_argument('--warn-time', type=float, default=60.0)
    parser.add_argument('--warn-volume', type=float, default=1000.0)
    parser.add_argument('--warn-complexity', type=int, default=10)
    # parser.add_argument('--warn-length-ratio', type=float, nargs=2, default=[0.75, 1.3])

    parser.add_argument('--error-difficulty', type=float, default=10.0)
    parser.add_argument('--error-effort', type=float, default=600.0)
    parser.add_argument('--error-time', type=float, default=120.0)
    parser.add_argument('--error-volume', type=float, default=1500.0)
    parser.add_argument('--error-complexity', type=int, default=15)
    # parser.add_argument('--error-length-ratio', type=float, nargs=2, default=[0.66, 1.5])

    args = parser.parse_args()
    try:
        result = subprocess.run(
            ['radon', 'hal'] + (list(natsorted(args.files)) or ['.']),
            text  = True,
            check = True,
            capture_output = True)

    except subprocess.CalledProcessError as e:
        print(f'Radon execution failed: {e.stderr}')
        return 1

    config = RadonConfig()
    config.update_from_args(args)
    metrics = parse_radon_output(result.stdout)

    total_errors = total_warnings = 0
    for file, file_metrics in metrics.items():
        file_warnings, file_errors = check_metrics(file_metrics, config)

        if file_errors or file_warnings:
            print(f'\n{file}:')

            for warn in file_warnings:
                print(f'  [+] WARNING: {warn}')
                total_warnings += 1

            for err in file_errors:
                print(f'  [!] ERROR: {err}')
                total_errors += 1

    if total_errors or total_warnings:
        print(f'\n{total_errors} errors, {total_warnings} warnings')
        if total_errors > 0:
            return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
