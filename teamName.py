
import numpy as np

##### TODO #########################################
### RENAME THIS FILE TO YOUR TEAM NAME #############
### IMPLEMENT 'getMyPosition' FUNCTION #############
### TO RUN, RUN 'eval.py' ##########################

nInst = 50
currentPos = np.zeros(nInst)

# Using Pair-Trade (covariance + z-scores)
def getHighCovPairs(prcSoFar):
    # Calculate the covariance matrix
    cov_matrix = np.cov(prcSoFar)
    
    # Create a list of pairs and their covariance values
    # cov_pairs = [covariance_value, instrument1, instrument2]
    cov_pairs = []
    for i in range(nInst):
        for j in range(i + 1, nInst):
            cov_pairs.append((cov_matrix[i, j], i, j))
    
    # Sort pairs by covariance in descending order
    cov_pairs.sort(reverse=True, key=lambda x: x[0])
    
    # Select the top pairs
    selected_pairs = []                                 # Keep track of added pairs
    selected = set()
    for cov, i, j in cov_pairs:
        if i not in selected and j not in selected:
            selected_pairs.append((i, j))
            selected.add(i)
            selected.add(j)
        if len(selected_pairs) == nInst // 2:
            break

    return selected_pairs


def getMyPosition(prcSoFar):

    (nins, nt) = prcSoFar.shape
    # Ensure there are enough time spread
    if (nt < 2):
        return np.zeros(nins)
    
    # Get pair instruments
    pairs = getHighCovPairs(prcSoFar)

    for idx, (i, j) in enumerate(pairs):
        # Calculate spread
        spread = prcSoFar[i, :] - prcSoFar[j, :]
        mean_spread = np.mean(spread)
        std_spread = np.std(spread)

        # Get Z score
        if std_spread > 0:
            z_score = (spread[-1] - mean_spread)/std_spread
        else:
            z_score = 0

        # Base position
        base_position = 10

        # Trading Signal
        if z_score > 4:                     # 4 std above, very limited trading since z_score is unlikely to go this high
            # Short i, Long j
            currentPos[i] -= base_position
            currentPos[j] += base_position

        elif z_score < -4:                  # 4 std below
            # Long i, Short j
            currentPos[i] += base_position
            currentPos[j] -= base_position

    return currentPos
