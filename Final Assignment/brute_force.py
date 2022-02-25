def bf_get_match(x, y, k):
    """
    Finds all common length-k substrings of x and y
    with brute force on both strings.
    Input:
    - x, y: strings
    - k: int, length of substring
    Output:
    - A list of tuples (i, j) where x[i:i+k] = y[j:j+k]
    """
    
    common_substrings = []
    m = len(x)
    n = len(y)
    for i in range(m - k + 1):
        for j in range(n - k + 1):
            #Iterate through all possible substrings to get all common substrings of x and y
            if x[i:i+k] == y[j:j+k]:
                common_substrings.append((i, j))
    
    #return the list of common substrings
    return common_substrings