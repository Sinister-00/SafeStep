
import numpy as np
import pandas as pd

# Import the CSV file into a DataFrame
df = pd.read_csv('./data.csv')

# Display the DataFrame
# print(df)

inputs = []
outputs = []

for file in subject_files:
    df= pd.read_csv(os.path.join(subject_path, file))
    x = np.array(df.drop(['Output'], axis = 1))
    y = np.array(df['Output'])
    group_size = 50
    num_groups = len(df) // group_size
    for i in range(num_groups):
        inp = x[i * group_size : (i + 1) * group_size]
        unique_values, counts = np.unique(y[i * group_size : (i + 1) * group_size], return_counts=True)
        majority_element = unique_values[np.argmax(counts)]
        inputs.append(inp)
        outputs.append(majority_element)
return np.array(inputs), np.array(outputs)


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Combine inputs and outputs into a single DataFrame
df_combined = pd.DataFrame({'Inputs': np.vstack(inputs), 'Outputs': outputs})

# Reshape the inputs to (50167, 50, 9)
df_combined['Inputs'] = np.vstack(inputs).reshape(-1, 50, 9)

# Split the combined DataFrame into train and test sets
train_df, test_df = train_test_split(df_combined, test_size=0.2, random_state=42)

# Split the train and test sets into input and output DataFrames
train_x_df = pd.DataFrame(np.vstack(train_df['Inputs'].values))
train_y_df = pd.DataFrame(train_df['Outputs'])
test_x_df = pd.DataFrame(np.vstack(test_df['Inputs'].values))
test_y_df = pd.DataFrame(test_df['Outputs'])

# Save the train and test sets to separate CSV files
train_x_df.to_csv('train_x.csv', index=False)
train_y_df.to_csv('train_y.csv', index=False)
test_x_df.to_csv('test_x.csv', index=False)
test_y_df.to_csv('test_y.csv', index=False)