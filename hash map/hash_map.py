# Course: CS261 - Data Structures
# Assignment: 5
# Student: Ryan Farol
# Description: Class below shows a hash table which has methods to put, get, remove, check, clear, empty buckets, resize,
# find factor load, and get keys.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """clears all the contents of the hash map"""
        for contents in range(self.capacity):
            self.buckets.pop() # removes element from the end of the array until the whole list is iterated
        empty_hash = LinkedList() # initialize empty LL
        for contents in range(self.capacity): # add empty linked list to current hash map
            self.buckets.append(empty_hash)
        self.size = 0

    def get(self, key: str) -> object:
        """returns the value associated with the given key"""
        hash = self.hash_function(key) # initialize key
        index = hash % self.capacity # calculate index dividing hash and DA size (taken from lecture)
        if self.buckets.get_at_index(index).contains(key) == None: # checks if the index is empty and returns None
            return None
        else:
            return self.buckets.get_at_index(index).contains(key).value # if index is not empty, returns the value

    def put(self, key: str, value: object) -> None:
        """updates the key/value pair in the hash map. If key already exists, it's associated value is replaced with the
        new value. If key is not found, the key/value pair will be added"""
        hash = self.hash_function(key) # initialize key
        index = hash % self.capacity # calculate index dividing hash and DA size (taken from lecture)
        if self.buckets.get_at_index(index).contains(key) == None: # if key does not exist, insert key/pair value
            self.buckets.get_at_index(index).insert(key, value)
            self.size += 1 # increment size
        else:
            self.buckets.get_at_index(index).contains(key).value = value # if key exists, value is replaced

    def remove(self, key: str) -> None:
        """removes the key given and its associated value from the hash map. If key is not in hash map, function does
        nothing"""
        hash = self.hash_function(key) # initialize key
        index = hash % self.capacity # calculate index dividing hash and DA size (taken from lecture)
        if self.buckets.get_at_index(index).contains(key) == None: # if key doesn't exist, return None
            return None
        else:
            self.buckets.get_at_index(index).remove(key) # if key exists, remove key and value associated with it
            self.size -= 1 # decrement size by 1

    def contains_key(self, key: str) -> bool:
        """returns True if the given key is in the hash map. If not in hash map, return False"""
        if self.size == 0: # checks if hash map is empty and returns false if Empty
            return False
        for i in range(self.buckets.length()): # iterates through the buckets
            search = self.buckets.get_at_index(i) # checks each index
            if search.contains(key) != None: # once key is found, return True
                return True
        return False

    def empty_buckets(self) -> int:
        """returns the number of empty buckets in the hash table"""
        empty_counter = 0 # initialize counter for empty buckets
        for i in range(self.buckets.length()): # iterate through buckets
            search = self.buckets.get_at_index(i)
            if search.length() == 0: # if length is 0, then empty bucket has been found
                empty_counter += 1 # increment counter for every empty bucket found
        return empty_counter

    def table_load(self) -> float:
        """returns the current hash table load factor"""
        load = self.size / self.capacity # load factor is the number of elements divided by the number of buckets
        return load

    def resize_table(self, new_capacity: int) -> None:
        """function changes the capacity of the internal hash table. All existing key/value pairs must remain in the new
        hash map and all hash table links must be rehashed. If new capacity is less than 1, then function should do
        nothing"""
        if new_capacity < 1: # if capacity is less than 1, return function
            return
        new_DA = DynamicArray() # initialize new dynamic array
        temp_LL = LinkedList() # create a temporary linked list to store current key/value pairs
        for i in range(self.capacity): # iterate through the buckets
            search = self.buckets.get_at_index(i) # check each index
            if search.length() > 0: # check if bucket is NOT empty
                for bucket in search: # take the key/value pairs, and put it in the temporary linked list
                    temp_LL.insert(bucket.key, bucket.value)
        self.size = 0 # set size back to 0
        self.capacity = new_capacity # set new capacity
        self.buckets = new_DA # set new dynamic array
        for i in range(new_capacity): # iterate through the list and add buckets/linkedlists
            new_DA.append(LinkedList())
        for bucket in temp_LL: # take key/value pair and put it in new buckets within new dynamic array
            self.put(bucket.key, bucket.value)



    def get_keys(self) -> DynamicArray:
        """returns a Dynamic Array that contains all keys stored in your hash map"""
        key_DA = DynamicArray() # initialize new dynamic array
        for i in range(self.buckets.length()): # iterate through the buckets
            for j in self.buckets.get_at_index(i): # nested loop and iterate through each key
                key_DA.append(j.key) # add keys into new dynamic array
        return key_DA


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

