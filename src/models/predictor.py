import json
import math
from pathlib import Path
from src.config import MODEL_PATH


def load_model_pipeline(model_path: Path = MODEL_PATH):
    """
    Loads the trained churn prediction model pipeline JSON.
    Returns (model_dict, is_online).
    """
    if model_path.exists():
        try:
            with open(model_path, "r", encoding="utf-8") as f:
                model_data = json.load(f)
            return model_data, True
        except Exception:
            return None, False
    return None, False


def sigmoid(z: float) -> float:
    """Stable sigmoid function bounded to avoid overflow."""
    bounded_z = max(-35.0, min(35.0, z))
    return 1.0 / (1.0 + math.exp(-bounded_z))


def predict_churn(values: dict, model_data: dict) -> tuple[float, list[dict]]:
    """
    Preprocess and score an individual customer profile using the trained model weights and scaling.
    Feature order strictly matches model.json:
      - CreditScore
      - Age
      - Tenure
      - Balance
      - NumOfProducts
      - HasCrCard
      - IsActiveMember
      - EstimatedSalary
      - Geography=France
      - Geography=Germany
      - Geography=Spain
      - Gender=Female

    Returns:
      (churn_probability, feature_contributions)
    """
    numeric_keys = [
        "CreditScore",
        "Age",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary",
    ]
    raw = [float(values[k]) for k in numeric_keys]
    raw += [float(values["Geography"] == c) for c in ("France", "Germany", "Spain")]
    raw += [float(values["Gender"] == "Female")]

    means = model_data["means"]
    scales = model_data["scales"]
    weights = model_data["weights"]
    features = model_data["features"]
    bias = model_data["bias"]

    scaled = [(x - m) / s for x, m, s in zip(raw, means, scales)]
    contributions = [w * s for w, s in zip(weights, scaled)]
    logit = bias + sum(contributions)
    prob = sigmoid(logit)

    # Sort contributing factors by magnitude
    factors = []
    display_names = {
        "CreditScore": "Credit Score",
        "Age": "Age",
        "Tenure": "Tenure",
        "Balance": "Account Balance",
        "NumOfProducts": "Number of Products",
        "HasCrCard": "Has Credit Card",
        "IsActiveMember": "Active Membership",
        "EstimatedSalary": "Estimated Salary",
        "Geography=France": "Country (France)",
        "Geography=Germany": "Country (Germany)",
        "Geography=Spain": "Country (Spain)",
        "Gender=Female": "Gender (Female)",
    }

    selected_country = values.get("Geography")

    for feat, contrib, raw_val in zip(features, contributions, raw):
        # If this is a geography one-hot dummy, only display the customer's actual country
        if feat.startswith("Geography="):
            country_name = feat.split("=")[1]
            if country_name != selected_country:
                continue
            feat_label = f"Region ({country_name})"
        else:
            feat_label = display_names.get(feat, feat)

        # Contribution > 0 pushes toward churn, < 0 pushes toward retention
        factors.append({
            "feature": feat,
            "label": feat_label,
            "contribution": contrib,
            "impact": "Increases Risk" if contrib > 0.05 else ("Lowers Risk" if contrib < -0.05 else "Neutral"),
        })

    factors.sort(key=lambda x: abs(x["contribution"]), reverse=True)
    return prob, factors
