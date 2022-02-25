class HashTableNode:
    def __init__(self, value, index):
        self.value = value
        self.indexes = [index]
        
    def __repr__(self):
        return f"{self.value} => {self.indexes}"
        
    def indexing(self, index):
        """
        Append the index to the indexes for a substring with the same value as the node's value
        Input
        -----
        - int: The index to be inserted
        """
        self.indexes.append(index)
        
        
class HashTableRH:
    def __init__(self, q=9973, d = 10, string = None, k = 3):
        #q is a prime number to avoid potential collisions.
        #9973 is the biggest prime before 10000.
        #Based on the google search, the average length of English Word is 4.5 characters.
        #To be safe, I choose the k-value something smaller than 4.5.
        #As the length of the k-substring value should be less than the input.
        #Therefore, I choose k = 3.
        self.q = q #Table Size
        self.d = d #Base used for ASCII Conversion
        self.hash_table = [None for _ in range(q)] #Empty Hash Table with size of q
        self.len_x = 0 #length of x
        self.len_y = 0 #length of y
        self.collisions = 0 #number of collisions
        self.plagiarism_rate = 0 #plagiarism rate
        if string:
            self.hash_table_insert(string, k)
    def lower_no_special(self, string): 
        """
        Make the input all lower cases and without special characters.  

        Inputs
        --------
        string: str

        Outputs
        --------
        str
        string without upper cases and special characters 

        """ 
        string = string.lower().replace("!", "").replace("?", "").replace(".", "").replace(",", "").replace(";", "")\
        .replace("*", "").replace("(", "").replace(")", "").replace('$', "").replace(' ','').replace("-", "")\
        .replace("\n",'').replace("\ufeff",'').replace('\'','').replace("%", "").replace("[", "").replace("]", "")\
        .replace("+", "").replace("=", "").replace("/", "").replace("\"", "").replace("\'", "")

        return string
    
    def hash_function_1(self, key):
        """
        With the division hash function, returns the hash value

        Inputs
        --------
        key: int
            The key needs to be hashed
        Outputs
        --------
        int
            hash value

        """
        return key % self.q
    
    def hash_function_2(self, key):
        """
        With the division hash function, returns the hash value

        Inputs
        --------
        key: int
            The key needs to be hashed
        Outputs
        --------
        int
            hash value

        """
        return key + 1 % (self.q - 1)          
    
    def double_hashing(self, key, i):
        """
        Puts two hashing function together to perform double_hashing

        Inputs
        --------
        key: int
            The key needs to be hashed
        i: int
            Current interation of collision resolution

        Outputs
        --------
        int
            new hash value
        """
        return (self.hash_function_1(key) + i * self.hash_function_2(key)) % self.q
    
    def ascii_convertor(self, string):
        """
        Since Hash function uses integer, change all the characters in ASCII number.

        Inputs
        --------
        string: str

        Outputs
        --------
        ascii_code:int
            converted ASCII code

        """
        ascii_code = 0
        for i in range(len(string)):
            ascii_code += ord(string[i])*self.d**(len(string) - i - 1)
        return ascii_code
    
    def hash_table_insert(self, x, k):
        """
        With a string x, this function helps to insert k-length substrings of x into the hash table
        Input
        -----
        x: str, string needs to be inserted
        Output
        ------
        hash_table: hash table with all the substrings
        """
        m = len(x)
        if m >= k:
            self.len_x = m
            i = 0

            #Get the first substring of x
            substring = x[:k]

            #Get hash value and do double hasing
            h = self.double_hashing(self.ascii_convertor(substring), 0)
            #Store a node with the string at hash table index h
            self.hash_table[h] = HashTableNode(substring, i)
            j = k
            while j < m:
                #Next substring removing the first character and get the next character
                substring = substring[1:] + x[j]
                i += 1

                #Get hash value for newly built substring with rolling hashing
                h = ((h*self.d + self.ascii_convertor(x[j]))%self.q - self.ascii_convertor(x[j - k])*((self.d**k)%self.q))%self.q

                #Insert the substring into the hash table
                self.insert(h, substring, i)
                j += 1
            return self.hash_table
        
        #Raise an error when the input is too small
        raise ValueError('The word you are testing,x, is too short. Try longer word or greater k.')
    
    def hash_table_search(self, y, k):
        """
        This function searches all the possible k-length substrings of input y in the hash table and return matches found
        Input
        -----
        y: str, the string needs to be searched
        
        Output
        ------
        array: list of all the tuples that has matches
        """
        n = len(y)
        if n >= k:
            self.len_y = n
            matches = 0
            i = 0
            
            #Open an emptry array
            array = []
            
            #Get the first substring of x
            substring = y[:k]
            #Get hash value and do double hasing
            h_y = self.double_hashing(self.ascii_convertor(substring), 0)
            #Search the table
            results = self.search(h_y, substring, i)
            if results:
                #If there's a match, count it and store it in the array
                matches += 1
                for result in results:
                    array.append(result)
            j = k
            while j < n:
                #Next substring removing the first character and get the next character
                substring = substring[1:] + y[j]
                i += 1
                #Get hash value for newly built substring with rolling hashing
                h_y = ((h_y*self.d + self.ascii_convertor(y[j]))%self.q - self.ascii_convertor(y[j - k])*((self.d**k)%self.q))%self.q
                #Search the table
                results = self.search(h_y, substring, i)
                if results:
                    #If there's a match, count it and store it in the array
                    matches += 1
                    for result in results:
                        array.append(result)
                j += 1
            print("Found", matches, "matches")
            
            #Calculate the plagiarism rate
            self.plagiarism_rate = (2*matches)/(self.len_x - k + 1 + self.len_y - k + 1)*100
            return array
        
        #Raise an error when the input is too small
        raise ValueError('The word you are testing,y, is too short. Try longer word or greater k.')
        
    def insert(self, key, value, index):
        """
        This function inserts key in the table which will resolve the collisions
        Input
        -----
        key: int, key value to be inserted
        value: Substring value that key holds
        index: Position of the substring
        
        Output
        ------
        None
        """
        j = 0
        while j < self.q:
            #Double Hashing to find hash value with the key to resolve collision
            dh = self.double_hashing(key, j)
            if self.hash_table[dh] is None:
                #Get the empty position and insert it there
                self.hash_table[dh] = HashTableNode(value, index)
                return
            if self.hash_table[dh].value == value:
                #Assign the index
                self.hash_table[dh].indexing(index)
                return
            if j == 0:
                #Count the collisions
                self.collisions += 1
            j += 1
    
    def search(self, key, value, index):
        """
        Looks up the key by searching the table
        Input
        -----
        key: int, key value to be inserted
        value: Substring value that key holds
        index: Position of the substring
        
        Output
        ------
        bool: boolean value. False if there's no match
        list: list, the list includes the positions of match
        """
        i = 0
        while i < self.q:
            #Use double hashing to find a key in the hash table
            h_y = self.double_hashing(key, i)
            if self.hash_table[h_y] is None:
                #Empty table means no key.
                return False
            if self.hash_table[h_y].value == value:
                #If there's a match, put them in array and return it
                return [(i, index) for i in self.hash_table[h_y].indexes]
            i += 1
        return False