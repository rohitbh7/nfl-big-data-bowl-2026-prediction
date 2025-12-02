import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor

## Functions Used in Feature Engineering
def angle_diff(a, b):
        diff = (a - b + 180) % 360 - 180
        return abs(diff)

def summarize_last10(group):
    group_cols = ['game_id', 'play_id', 'nfl_id']
    roll = group[['x', 'y', 's', 'a', 'dir']].rolling(window=10, min_periods=1)
    
    # Compute stats
    summary = pd.DataFrame({
        'x_mean': roll['x'].mean(),
        'x_std': roll['x'].std(),
        'x_first': group['x'].shift(9).fillna(group['x'].iloc[0]),   # first of last 10 frames
        'x_last': group['x'],
        'x_min': roll['x'].min(),
        'x_max': roll['x'].max(),

        'y_mean': roll['y'].mean(),
        'y_std': roll['y'].std(),
        'y_first': group['y'].shift(9).fillna(group['y'].iloc[0]),
        'y_last': group['y'],
        'y_min': roll['y'].min(),
        'y_max': roll['y'].max(),

        'speed_mean': roll['s'].mean(),
        'speed_std': roll['s'].std(),

        'accel_mean': roll['a'].mean(),
        'accel_std': roll['a'].std(),

        'dir_mean': roll['dir'].mean(),
        'dir_std': roll['dir'].std(),
        'dir_first': group['dir'].shift(9).fillna(group['dir'].iloc[0]),
        'dir_last': group['dir'],
    })

    # Add identifying columns back
    summary[group_cols + ['frame_id']] = group[group_cols + ['frame_id']].values

    # Return only the last frame of this group
    return summary.iloc[[-1]]

def compute_closest_defender(group):
    # Separate targeted receiver & defenders
    tgt = group[group["player_role"] == "Targeted Receiver"]
    defs = group[group["player_role"] == "Defensive Coverage"]
    
    # If no defender or no target, return group unchanged
    if len(tgt) == 0 or len(defs) == 0:
        return group
    
    tgt_x, tgt_y = float(tgt["x"]), float(tgt["y"])
    
    # Compute distances
    defs = defs.assign(
        dist = np.sqrt((defs["x"] - tgt_x)**2 + (defs["y"] - tgt_y)**2)
    )
    
    # Identify closest defender
    closest_def = defs.loc[defs["dist"].idxmin()]
    
    # Assign dx/dy to target receiver only
    group.loc[group["player_role"] == "Targeted Receiver", "dx_to_closest_defender"] = \
        tgt_x - closest_def["x"]
    group.loc[group["player_role"] == "Targeted Receiver", "dy_to_closest_defender"] = \
        tgt_y - closest_def["y"]

    return group

# Feature Engineering Function
def feature_engineer(test, test_input):
    # Get relevant prethrow data
    relevant_prethrow = test_input[['game_id','play_id','nfl_id','frame_id','x','y','s','a','o','dir','ball_land_x','ball_land_y','player_position','player_role']]
    
    # Calculate distance to landing point
    relevant_prethrow['distance_to_land'] = np.sqrt((relevant_prethrow['ball_land_x'] - relevant_prethrow['x'])**2 + (relevant_prethrow['ball_land_y'] - relevant_prethrow['y'])**2)
    
    # Calculate angle to landing point
    dx = relevant_prethrow['x'] - relevant_prethrow['ball_land_x']
    dy = relevant_prethrow['y'] - relevant_prethrow['ball_land_y']
    angles = np.degrees(np.arctan2(dy, dx))
    angles = (angles + 90) % 360
    relevant_prethrow['angle_to_land'] = angles
    
    # Calculate movement and orientation angle differences
    relevant_prethrow['movement_angle_difference'] = relevant_prethrow.apply(
        lambda row: angle_diff(row['angle_to_land'], row['dir']), axis=1
    )

    relevant_prethrow['orientation_angle_difference'] = relevant_prethrow.apply(
        lambda row: angle_diff(row['angle_to_land'], row['o']), axis=1
    )

    # Summarize last 10 frames for each player in each play
    prethrow = relevant_prethrow.sort_values(['game_id', 'play_id', 'nfl_id', 'frame_id'])
    group_cols = ['game_id', 'play_id', 'nfl_id']
    prethrow = prethrow.groupby(group_cols, group_keys=False).apply(summarize_last10).reset_index(drop=True)

    # Get only the last frame for each player in each play
    lastframe = relevant_prethrow.loc[
        lambda df: df.groupby(['game_id', 'play_id', 'nfl_id'])['frame_id'].idxmax()
    ]
    lastframe = pd.merge(
        lastframe,
        prethrow,
        how = "left",
        on = ['game_id','play_id','nfl_id']
    )
    lastframe = lastframe.drop(columns=['frame_id_x','frame_id_y'])

    # Calculate distance to closest sideline
    lastframe["distance_to_closest_sideline"] = np.where(
        lastframe["y"] <= 53.3 - lastframe["y"],
        -lastframe["y"],
        53.3 - lastframe["y"]
    )

    # Calculate dx/dy to closest opponent
    df = lastframe.copy()
    target_info = df[df["player_role"] == "Targeted Receiver"][["game_id","play_id","x","y","nfl_id"]]
    target_info = target_info.rename(columns={"x":"tgt_x", "y":"tgt_y", "nfl_id":"tgt_nfl_id"})
    df = df.merge(target_info, on=["game_id","play_id"], how="left")
    df.loc[df["player_role"] == "Defensive Coverage", "dx_to_target"] = \
        df["x"] - df["tgt_x"]
    df.loc[df["player_role"] == "Defensive Coverage", "dy_to_target"] = \
        df["y"] - df["tgt_y"]
    df = df.groupby(["game_id","play_id"], group_keys=False).apply(compute_closest_defender)
    df["dx_to_closest_opponent"] = df["dx_to_target"].combine_first(df["dx_to_closest_defender"])
    df["dy_to_closest_opponent"] = df["dy_to_target"].combine_first(df["dy_to_closest_defender"])
    lastframe = pd.merge(
        lastframe,
        df[['game_id','play_id','nfl_id','dx_to_closest_opponent','dy_to_closest_opponent']],
        on = ['game_id','play_id','nfl_id']
    )

    # Merge with postthrow data to get target_x and target_y
    data = pd.merge(
        lastframe,
        test.rename(columns={'x': 'target_x', 'y': 'target_y'}),
        how = "inner",
        on = ['game_id','play_id','nfl_id']
    )
    return data

# Model and Predict Function
def knn_model_and_predict(modeling_data, predicting_data):
    # One-hot encode Training player_role
    modeling_data = pd.get_dummies(modeling_data, columns=['player_role'], prefix='role')

    # Prepare Training features and target
    X = modeling_data[['x','y','frame_id','distance_to_closest_sideline','ball_land_x','ball_land_y','dir','dir_mean','movement_angle_difference','s']]
    y = modeling_data[['target_x','target_y']]
    # Model Training Data
    
    # Input correct Model
    scaler = StandardScaler()
    X_s = scaler.fit_transform(X)
    knn = KNeighborsRegressor(n_neighbors=3, weights='distance', p=1)
    knn.fit(X_s, y)

    # Prepare Test features
    predicting_data = pd.get_dummies(predicting_data, columns=['player_role'], prefix='role')
    X_pred = predicting_data[['x','y','frame_id','distance_to_closest_sideline','ball_land_x','ball_land_y','dir','dir_mean','movement_angle_difference','s']]
    X_pred_s = scaler.transform(X_pred)
    # Predict on Test data
    y_pred = knn.predict(X_pred_s)

    # Assign predictions to predicting_data
    predicting_data['target_x'] = y_pred[:, 0]
    predicting_data['target_y'] = y_pred[:, 1]

    # Prepare output DataFrame
    output_df = pd.DataFrame({
        "id": (
            predicting_data['game_id'].astype(str) + "_" +
            predicting_data['play_id'].astype(str) + "_" +
            predicting_data['nfl_id'].astype(str) + "_" +
            predicting_data['frame_id'].astype(str)
        ),
        "x": predicting_data['target_x'],
        "y": predicting_data['target_y']
    })

    return output_df


# Predict on Test Data
def predict(test, test_input):
    # Get Training Data
    weeks = []
    for i in range(1, 19):
        df = pd.read_csv(f"train/input_2023_w{i:02d}.csv")
        weeks.append(df)

    prethrow = pd.concat(weeks, ignore_index=True)
    weeks = []
    for i in range(1, 19):
        df = pd.read_csv(f"train/output_2023_w{i:02d}.csv")
        weeks.append(df)
    postthrow = pd.concat(weeks, ignore_index=True)
    # Feature Engineering on Training Data
    data = feature_engineer(postthrow, prethrow)
    pred = feature_engineer(test, test_input)
    predictions = knn_model_and_predict(data, pred)
    return predictions
     


output = predict(pd.read_csv("test.csv"), pd.read_csv("test_input.csv"))
print(output)