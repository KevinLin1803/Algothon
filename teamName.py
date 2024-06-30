
import numpy as np

##### TODO #########################################
### RENAME THIS FILE TO YOUR TEAM NAME #############
### IMPLEMENT 'getMyPosition' FUNCTION #############
### TO RUN, RUN 'eval.py' ##########################

nInst = 50
currentPos = np.zeros(nInst)

# Function that finds a pair with the greatest correlation(covariance closest to 1) 
def getPair(prchistory):
    price_cov = np.cov(prchistory, rowvar=False)

    stock_a = 0
    stock_b = 0
    # Probs wanna change this
    curr = 9999999

    for i in range(0,50):
        a = price_cov[i, : ]
        for i2 in range(0,50):
            if (abs(price_cov[i][i2] < curr) and i != i2) :
                stock_a = i
                stock_b = i2
                curr = abs(price_cov[i][i2] < curr)

    return (stock_a, stock_b)

def getMyPosition(prcSoFar):
    global currentPos
    (nins, nt) = prcSoFar.shape
    if (nt < 2):
        return np.zeros(nins)
    lastRet = np.log(prcSoFar[:, -1] / prcSoFar[:, -2])
    lNorm = np.sqrt(lastRet.dot(lastRet))
    lastRet /= lNorm
    rpos = np.array([int(x) for x in 5000 * lastRet / prcSoFar[:, -1]])
    currentPos = np.array([int(x) for x in currentPos+rpos])
    print(getPair(prcSoFar))
    return currentPos

