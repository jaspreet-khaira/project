import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("=" * 50)
print(" AI-BASED DISEASE PREDICTION SYSTEM")
print("=" * 50)

data = pd.read_csv("disease_dataset.csv")

print("\nDataset loaded successfully!")
print("Dataset shape:", data.shape)

X = data.drop("disease", axis=1)
y = data["disease"]

symptoms = list(X.columns)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("\nModel training completed!")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel evaluation")
print("-" * 30)

print(f"Test accuracy: {accuracy:.2%}")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

joblib.dump(model, "disease_model.pkl")
joblib.dump(symptoms, "symptoms.pkl")

print("\nTrained model saved successfully!")
print("\nAvailable symptoms:")

for index, symptom in enumerate(symptoms, start=1):
    print(f"{index}. {symptom.replace('_', ' ').title()}")
    print("\nEnter the symptoms you currently have.")
    print("Enter symptom numbers separated by commas.")
    print("Example: 1,2,3")
    print("Enter 0 if none of these symptoms apply.")

while True:

    user_input = input("\nYour choice: ").strip()

    try:
        choices = [
            int(value.strip())
            for value in user_input.split(",")
        ]

        if not choices:
            raise ValueError

        if any(
            number < 0 or number > len(symptoms)
            for number in choices
        ):
            print("Invalid choice. Please try again.")
            continue

        if len(choices) != len(set(choices)):
            print("Duplicate choices found. Please try again.")
            continue

        break

    except ValueError:
        print(
            "Invalid input. Enter symptom numbers "
            "separated by commas."
        )

input_values = [
    1 if index + 1 in choices else 0
    for index in range(len(symptoms))
]

input_data = pd.DataFrame(
    [input_values],
    columns=symptoms
)

predicted_category = model.predict(input_data)[0]

print("\n" + "=" * 50)
print(" PREDICTION RESULT")
print("=" * 50)

print("Predicted category:", predicted_category)

print(
    "\nThis result is an educational model prediction, "
    "not a medical diagnosis."
)

print(
    "If you are concerned about your symptoms, "
    "consult a qualified healthcare professional."
)

print("=" * 50)