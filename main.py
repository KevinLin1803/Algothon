
import numpy as np

##### TODO #########################################
### RENAME THIS FILE TO YOUR TEAM NAME #############
### IMPLEMENT 'getMyPosition' FUNCTION #############
### TO RUN, RUN 'eval.py' ##########################

nInst = 50
currentPos = np.zeros(nInst)
pricePos = np.zeros(nInst)

# Using Pair-Trade (covariance + z-scores)
def getHighCovPairs(prcSoFar):
    # Calculate the covariance matrix
    cov_matrix = np.cov(prcSoFar)
    
    # Create a list of pairs and their covariance values
    # cov_pairs = [covariance_value, instrument1, instrument2]
    cov_pairs = []
    for i in range(nInst):
        for j in range(i + 1, nInst):
            i_stdev = np.std(prcSoFar[i])
            j_stdev = np.std(prcSoFar[j])
            cov_pairs.append(((cov_matrix[i, j]/(i_stdev * j_stdev)), i, j))
    
    # Sort pairs by covariance in ascending order
    # cov_pairs.sort(reverse=True, key=lambda x: x[0] )
    cov_pairs.sort(key=lambda x: abs(x[0] - 1))
    
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
    
    return selected_pairs[:5]

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
        base_position = 100

        #initial position
        if (currentPos[i] == 0 and currentPos[j] == 0):
            # Trading Signal
            if z_score > 3:                     # 3 std above, very limited trading since z_score is unlikely to go this high
                # Short i, Long j
                currentPos[i] -= base_position
                currentPos[j] += base_position
                pricePos[i] = prcSoFar[i, -1]
                pricePos[j] = prcSoFar[j, -1]

            elif z_score < -3:                  # 3 std below
                # Long i, Short j
                currentPos[i] += base_position
                currentPos[j] -= base_position
                pricePos[i] = prcSoFar[i, -1]
                pricePos[j] = prcSoFar[j, -1]
            
            continue

        if (currentPos[i] > 0):
            long = i
            short = j
        else:
            long = j
            short = i
        
        current_spread = prcSoFar[long, -1] - prcSoFar[short, -1]
        initial_spread = pricePos[long] - pricePos[short]

        if (current_spread > initial_spread):
            currentPos[long] = 0
            currentPos[short] = 0
        else:
            currentPos[long] *= 2
            currentPos[short] *= 2

    return currentPos
