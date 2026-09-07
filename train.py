import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


df = pd.read_csv("spam_dataset.csv")

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])

model.fit(df["text"], df["label"])

joblib.dump(model, "model.joblib")

print("Model trained and saved as model.joblib")
