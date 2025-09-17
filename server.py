from flask import Flask, request, jsonify
from flask_cors import CORS

import joblib      


app = Flask(__name__)
CORS(app)

# Load saved models and data
df = joblib.load("tweets_df.pkl")
vectorizer = joblib.load("vectorizer.pkl")
model = joblib.load("logistic_regression.pkl")

@app.route("/search")
def search():
    term = request.args.get("term", "")
    if term == "":
        return jsonify({"error": "no term"}), 400

    # filter tweets
    matches = df[df['cleaned_text'].str.contains(term, case=False, na=False)]

    if matches.shape[0] == 0:
        return jsonify({"counts": {}, "tweets": []})

    # predict
    X = vectorizer.transform(matches['cleaned_text']).toarray()
    preds = model.predict(X)
    matches = matches.copy()
    matches['label'] = preds
    matches['label'] = matches['label'].map({0: "Negative", 1: "Positive"})

    counts = matches['label'].value_counts().to_dict()
    tweets = matches[['text', 'label']].head(10).to_dict(orient="records")

    return jsonify({"counts": counts, "tweets": tweets})

if __name__ == "__main__":
    app.run(debug=True)