import json


def write_report(stats, output_path):
    data = stats.to_dict()
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)