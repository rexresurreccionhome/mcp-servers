# Overfitting and Underfitting in ML

## Overfitting

**Overfitting** occurs when a machine learning model learns the training data too well, including its noise and random fluctuations. The model becomes too complex and performs excellently on training data but poorly on new, unseen data.

**Key characteristics:**
- High accuracy on training data
- Low accuracy on test/validation data
- Model memorizes rather than generalizes
- Often caused by too many features or overly complex models

**Example:** A model that memorizes every detail of training examples, including outliers and errors, instead of learning the underlying patterns.

## Underfitting

**Underfitting** occurs when a machine learning model is too simple to capture the underlying patterns in the data. The model performs poorly on both training and test data.

**Key characteristics:**
- Low accuracy on training data
- Low accuracy on test/validation data
- Model is too simple or lacks sufficient features
- Fails to capture important relationships in the data

**Example:** Using a linear model to fit data that has a complex, non-linear relationship.

## When Do These Events Occur?

### During Training

**Underfitting** typically occurs **early in training** or with insufficient model capacity:
- At the beginning of training when the model hasn't learned enough
- When using a model that's too simple for the problem
- When training stops too early (early stopping set too aggressively)
- When important features are missing from the dataset

**Overfitting** typically occurs **later in training**:
- After many training iterations/epochs when the model starts memorizing
- When training continues for too long without proper regularization
- When the model becomes too focused on training data specifics
- More common with small datasets where the model can memorize all examples

### Detecting During the ML Workflow

**Training Phase:**
- Monitor training and validation loss curves
- Underfitting: Both losses remain high and don't improve much
- Overfitting: Training loss decreases but validation loss starts increasing

**Validation Phase:**
- Compare performance metrics between training and validation sets
- Large gap indicates overfitting
- Poor performance on both indicates underfitting

**Testing Phase:**
- Final check on held-out test data
- Confirms whether the model generalizes well or suffers from overfitting

## Finding the Balance

The goal is to find the **sweet spot** between overfitting and underfitting:
- A model that generalizes well to new data
- Performs reasonably on both training and test data
- Captures important patterns without memorizing noise

**Common solutions:**
- **For overfitting:** Use regularization, reduce model complexity, collect more data, or use cross-validation
- **For underfitting:** Add more features, increase model complexity, or train longer