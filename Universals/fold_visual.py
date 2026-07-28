#!/usr/bin/env python3
"""
fold_visual.py - The 90-degree Crease Visualization

Core intuition of the Puno Calculus: the ReLU function |x| is the
elementary fold. Every neural network is a composition of these folds.

Exports data for dashboard rendering (no matplotlib dependency).
"""

import json
import math
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_fold_data():
    x = np.linspace(-3, 3, 500)
    y = np.abs(x)

    left_x = np.linspace(-3, 0, 100)
    left_y = -left_x
    right_x = np.linspace(0, 3, 100)
    right_y = right_x

    crease_points = []
    for i in range(1, len(x)):
        if i % 5 == 0:
            crease_points.append({
                'x': round(float(x[i]), 4),
                'y': round(float(y[i]), 4),
            })

    derivative_pos = [1.0] * 250
    derivative_neg = [-1.0] * 250

    return {
        'relu': crease_points,
        'left_ray': [{'x': round(float(left_x[i]), 4), 'y': round(float(left_y[i]), 4)}
                      for i in range(0, len(left_x), 3)],
        'right_ray': [{'x': round(float(right_x[i]), 4), 'y': round(float(right_y[i]), 4)}
                       for i in range(0, len(right_x), 3)],
        'derivative': {
            'x': [round(float(v), 4) for v in x[::5]],
            'y': [round(float(v), 4) for v in (derivative_pos + derivative_neg)[::5]],
        },
        'description': {
            'title': 'The 90-Degree Crease: Elementary Fold',
            'subtitle': 'f(x) = |x| — every ReLU network is a composition of these folds',
            'key_insight': 'The crease at x=0 is where the derivative is undefined. '
                           'In the Puno Calculus, this singularity is the fundamental object.',
            'rays': {
                'left': 'slope -1 (folded-back region)',
                'right': 'slope +1 (unfolded region)',
            },
        },
    }


def generate_multi_fold_data():
    folds = []
    offsets = [-2, 0, 1.5]
    for offset in offsets:
        x = np.linspace(-4, 4, 200)
        y = np.abs(x - offset)
        fold = [{'x': round(float(x[i]), 4), 'y': round(float(y[i]), 4)}
                for i in range(0, len(x), 4)]
        folds.append({
            'offset': offset,
            'label': f'|x - ({offset})|',
            'points': fold,
            'crease_x': offset,
        })

    composed_x = np.linspace(-4, 4, 200)
    composed_y = np.maximum.reduce([np.abs(composed_x - o) for o in offsets])
    composed = [{'x': round(float(composed_x[i]), 4), 'y': round(float(composed_y[i]), 4)}
                 for i in range(0, len(composed_x), 4)]

    return {
        'individual_folds': folds,
        'composed': composed,
        'description': {
            'title': 'Composition of Folds',
            'subtitle': 'max(|x+2|, |x|, |x-1.5|) — three creases compose into a complex boundary',
            'insight': 'Each ReLU adds one fold. A network with L hidden layers creates '
                       'up to 2^L distinct linear regions.',
        },
    }


def run():
    print('=' * 60)
    print('FOLD VISUALIZATION: The 90-Degree Crease')
    print('=' * 60)

    fold_data = generate_fold_data()
    multi_data = generate_multi_fold_data()

    export = {
        'single_fold': fold_data,
        'multi_fold': multi_data,
    }

    out_path = os.path.join(BASE_DIR, 'fold_visual_data.json')
    with open(out_path, 'w') as f:
        json.dump(export, f, indent=2)
    print(f'[EXPORTED] {out_path}')

    print(f'\nSingle fold: 500 points of |x|')
    print(f'Multi-fold: {len(multi_data["individual_folds"])} individual + 1 composed')
    print(f'\nFold visualization data generated.')


if __name__ == '__main__':
    run()
