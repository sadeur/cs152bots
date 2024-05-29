import pandas as pd
import time, csv
from perspective import check_hate_speech

hatemoji_df = pd.read_csv('../data/hatemojicheck.csv')
perspective_results = 'perspective_results.csv'

def evaluate_perspective_model(data):
    results = {}
    correct, true_pos, true_neg, false_pos, false_neg = [], [], [], [], []
    total = len(data)
    errors = []
    for index, row in data.iterrows():
        try:
            pred_hate_speech = check_hate_speech(row.text)
            if pred_hate_speech == row.label_gold:
                correct.append(row.text)
            if pred_hate_speech and row.label_gold:  # we predicted hate speech and it is
                true_pos.append(row.text)
            if not pred_hate_speech and not row.label_gold:  # we predicted not hate speech and it's not
                true_neg.append(row.text)
            if pred_hate_speech and not row.label_gold:  # we predicted hate speech but it's not
                false_pos.append(row.text)
            if not pred_hate_speech and row.label_gold:  # we predicted not hate speech but it is
                false_neg.append(row.text)
        except:
            errors.append(row.text)
            total -= 1
        if index % 50 == 0:  # avoid perspective quota limits (60 requests per minute)
            print(index)
            time.sleep(60)
    results["accuracy"] = len(correct) / total
    results["precision"] = len(true_pos) / (len(true_pos) + len(false_pos))
    results["recall"] = len(true_pos) / (len(true_pos) + len(false_neg))
    results["prevalence"] = len(false_neg) / total
    results["true_positives"] = len(true_pos), true_pos
    results["true_negatives"] = len(true_neg), true_neg
    results["false_positives"] = len(false_pos), false_pos
    results["false_negatives"] = len(false_neg), false_neg
    results["errors"] = errors
    return results

# random_rows = hatemoji_df.sample(50)  # for testing
data = evaluate_perspective_model(hatemoji_df)

# save results to csv
with open(perspective_results, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data.keys())
    writer.writeheader()
    writer.writerow(data)
