
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
    # cor_pairs = [cor, instrument1, instrument2]
    cor_pairs = []
    for i in range(nInst):
        for j in range(i + 1, nInst):
            std_i = np.std(prcSoFar[i])
            std_j = np.std(prcSoFar[j])
            cor = cov_matrix[i, j] / (std_i * std_j)
            cor_pairs.append((cor, i, j))

    # Sort pairs by correlation in descending order
    cor_pairs.sort(reverse=True, key=lambda x: x[0])
    
    # Select the top pairs
    selected_pairs = []                                 # Keep track of added pairs
    selected = set()
    for cov, i, j in cor_pairs:
        if i not in selected and j not in selected:
            selected_pairs.append((i, j))
            selected.add(i)
            selected.add(j)
        if len(selected_pairs) == nInst // 2:
            break

    return selected_pairs[:10]


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

        # Martingale Strategy
        if currentPos[i] != 0 and currentPos[j] != 0:
            old_spread = abs(pricePos[i] - pricePos[j])
            current_spread = abs(prcSoFar[i, -1] - prcSoFar[j, -1])

            # Check spread movement
            if current_spread > old_spread:
                # Close positions
                # if currentPos[i] > 0:
                #     currentPos[i] -= currentPos[i]
                # else:
                #     currentPos[i] += currentPos[i]
                
                # if currentPos[j] > 0:
                #     currentPos[j] -= currentPos[j]
                # else:
                #     currentPos[j] += currentPos[j]
                currentPos[i] = 0
                currentPos[j] = 0
                
            else:
                # Double down on losses
                currentPos[i] *= 2
                currentPos[j] *= 2

            # Update price positions
            pricePos[i] = prcSoFar[i, -1]
            pricePos[j] = prcSoFar[j, -1]        

        # Initial buy
        else:
            # Get Z score
            if std_spread > 0:
                z_score = (spread[-1] - mean_spread)/std_spread
            else:
                z_score = 0

            # Base position
            base_position = 10

            # Trading Signal
            if z_score > 1:
                # Short i, Long j
                currentPos[i] -= base_position
                currentPos[j] += base_position

            elif z_score < -1:
                # Long i, Short j
                currentPos[i] += base_position
                currentPos[j] -= base_position
            
            # Update price positions
            pricePos[i] = prcSoFar[i, -1]
            pricePos[j] = prcSoFar[j, -1]

    return currentPos
