from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

if not os.path.exists("static"):
    os.makedirs("static")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['file']

        if not file:
            return "No file uploaded"

        df = pd.read_csv(file)
        total = len(df)

        # ===== SIMULATED ANOMALY DETECTION =====
        df['prediction'] = np.random.choice([0, 1], size=len(df), p=[0.95, 0.05])

        anomalies_df = df[df['prediction'] == 1]
        anomalies = len(anomalies_df)

        # ===== ANOMALY TYPES =====
        anomaly_types = [
            'Region Anomaly',
            'Unusual Activity',
            'Login Spike',
            'Access Pattern Change',
            'Privilege Escalation'
        ]

        if anomalies > 0:
            anomalies_df['anomaly_type'] = np.random.choice(anomaly_types, size=len(anomalies_df))
            anomaly_counts = anomalies_df['anomaly_type'].value_counts().to_dict()
        else:
            anomaly_counts = {}

        # ===== GRAPH FIXED =====
        plt.figure(figsize=(8,5))

        if anomaly_counts:
            labels = list(anomaly_counts.keys())
            values = list(anomaly_counts.values())

            plt.bar(labels, values)

            # FIX LABEL ROTATION
            plt.xticks(rotation=25, ha='right')

            # ADD VALUES ON TOP
            for i, v in enumerate(values):
                plt.text(i, v + 2, str(v), ha='center')

        else:
            plt.text(0.5, 0.5, "No anomalies detected", ha='center')

        plt.title("Anomaly Type Distribution")
        plt.tight_layout()   # VERY IMPORTANT FIX

        graph_path = "static/graph.png"
        plt.savefig(graph_path)
        plt.close()

        return render_template(
            'result.html',
            total=total,
            anomalies=anomalies,
            anomaly_counts=anomaly_counts,
            graph=graph_path
        )

    except Exception as e:
        return f"Error occurred: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)