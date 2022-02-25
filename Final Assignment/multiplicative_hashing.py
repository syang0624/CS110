import math
class MultiHashing:
    def __init__(self, q=9973, c = (5**0.5 - 1)/2, d=26, string = None, k = 3):
        self.q = q #Table Size
        self.d = d #Base of ASCII
        self.c = c #Constant for Multiplicative Hashing
        self.len_x = 0
        self.len_y = 0
        #Create a hash table
        self.hash_table = [[] for _ in range(q)]
        self.collisions = 0 #Number of Collisions
        self.plagiarism_rate = 0 #Plagiarism Rate
        
        if string:
            #If there is a string, insert it to the hash table
            self.hash_table_insert(string, k)
    
    def hash_function(self, key):
        """
        Get the hash value of key with the multiplicative hash function
        Input
        -----
        key: int, the key value needs to be hashed
        
        Output
        ------
            A hash value of the key
        """
        return math.floor(self.q*((key*self.c)-math.floor(key*self.c)))
    
    def set_q(self, large):
        """
        Generate the larger power of 2
        Input
        -----
        large: int, the number I have to get next largest power of 2
        
        Output
        ------
            The next largest power of two
        """
        return 2**math.ceil(math.log(large, 2))
    
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
            h = self.hash_function(self.ascii_convertor(substring))
            #Store a node with the string at hash table index h
            self.hash_table[h].append(HashTableNode(substring, i))
            j = k
            while j < m:
                #Next substring removing the first character and get the next character
                substring = substring[1:] + x[j]
                i += 1

                #Get hash value for newly built substring with rolling hashing
                h = self.hash_function(self.ascii_convertor(substring))

                #Insert the substring into the hash table
                if len(self.hash_table[h]) > 0:
                    self.collisions += 1
                self.hash_table[h].append(HashTableNode(substring, i))
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
            h_y = self.hash_function(self.ascii_convertor(substring))
            #Search the table
            results = self.search(h_y, substring, i)
            if results:
                #If there's a match, count it and store it in the array
                matches += 1
                for result in results:
                    array.append(result)
            j = k
            while j < n:
                #Obtain the substring from the previous substring by removing the first character and adding the next one
                substring = substring[1:] + y[j]
                i += 1
                #Compute h_y for the new substring with the hashing function (without rolling hashing)
                h_y = self.hash_function(self.ascii_convertor(substring))
                #Call self.search to search the table for the substring (and account for possible collisions)
                results = self.search(h_y, substring, i)
                if results:
                    #If we find a match, we increase the number of matches and add the results to the array.
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
        if self.hash_table[key] is None:
            #Empty table means no key.
            return False
        array = []
        for i in self.hash_table[key]:
            if i.value == value:
                #If there's a match, put them in array and return it
                array.append((i.indexes[0], index))
        return array

def multi_get_match(x, y, k):
    """
    Find common substrings of inputs withOUT rolling hashing.
    Input
    -----
    x, y: str, input strings
    k: int, length of substring
    
    Output
    ------
        A list of tuples with matches
    """
    
    #Get a hash table with size of k
    table = MultiHashing(k = k)
    
    #Eliminates the special characters and lower the cases
    x, y = table.lower_no_special(x), table.lower_no_special(y)
    
    #Insert the substrings of x into the table
    table.hash_table_insert(x, k)
    
    #Get the lists of common sub strings from hash table
    common_substrings = table.hash_table_search(y, k)
    
    print("Collisions:", table.collisions)
    print("{:0.2f}% plagiarism detected\n".format(table.plagiarism_rate))
    
    return common_substrings

def multi_get_match_test(x, y, k):
    """
    Basically the same function like above but not printing collisions or plagiarism percentage.
    So it can be used for assert.
    """
    #Get a hash table with size of k
    table = MultiHashing(k = k)
    
    #Eliminates the special characters and lower the cases
    x, y = table.lower_no_special(x), table.lower_no_special(y)
    
    #Insert the substrings of x into the table
    table.hash_table_insert(x, k)
    
    #Get the lists of common sub strings from hash table
    common_substrings = table.hash_table_search(y, k)
    
    return common_substrings