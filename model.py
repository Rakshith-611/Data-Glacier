from sklearn.datasets import load_linnerud
from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle


dataset = load_linnerud()

# Create DataFrames for the features and targets
# Interchanging data and target because it is easier to know personal phisiological data
X = pd.DataFrame(dataset.target, columns=dataset.target_names)
y = pd.DataFrame(dataset.data, columns=dataset.feature_names)

regressor = LinearRegression()

regressor.fit(X,y)

pickle.dump(regressor, open('model.pkl', 'wb'))

model = pickle.load(open('model.pkl','rb'))
print(model.predict([[160, 30, 60]]))
