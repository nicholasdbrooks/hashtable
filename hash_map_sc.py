# Name: Nicholas Brooks
# OSU Email: brooksni@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap Implementation
# Due Date: 06/03/2022
# Description: Implement a HashMap class with Separate Chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map.
        If the given key already exists, its value is replaced with the new value
        If the key doesn't exist, a new key/value pair is added
        """
        # determine the hash, index
        hash = self._hash_function(key)
        bucket = hash % self._capacity

        # see if the key pair is in the hashmap
        node = self._buckets[bucket].contains(key)
        if node:
            node.value = value
        else:
            self._buckets[bucket].insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        # initialize counter
        counter = 0

        # iterate through buckets
        for i in range(0, self._capacity):
            if self._buckets[i].length() == 0:
                counter += 1

        return counter

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        return self._size/self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map
        Does not change capacity
        """
        # clear the buckets
        for i in range(0, self._capacity):
            self._buckets[i] = LinkedList()

        # resize
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash table
        All existing key value pairs are rehashed
        """
        # ensure that the capacity is at least 1
        if new_capacity < 1:
            return

        # initialize new hashmap
        newmap = DynamicArray()
        for i in range(0, new_capacity):
            newmap.append(LinkedList())

        # rehash all table links
        for i in range(0, self._capacity):
            for element in self._buckets[i]:
                hash = self._hash_function(element.key)
                bucket = hash % new_capacity
                newmap[bucket].insert(element.key, element.value)

        self._capacity = new_capacity
        self._buckets = newmap

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key
        """
        # calculate hash/index
        hash = self._hash_function(key)
        bucket = hash % self._capacity

        # iterate through bucket to see if key is there
        for element in self._buckets[bucket]:
            if element.key == key:
                return element.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns true if the key is in the hash map
        Returns false otherwise
        """
        # calculate hash/index
        hash = self._hash_function(key)
        bucket = hash % self._capacity

        # iterate through bucket to see if key is there
        for element in self._buckets[bucket]:
            if element.key == key:
                return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map
        If the key is not in the hash map, nothing happens
        """
        # calculate the hash/index
        hash = self._hash_function(key)
        bucket = hash % self._capacity

        # iterate through bucket to see if key is there
        for element in self._buckets[bucket]:
            if element.key == key:
                self._buckets[bucket].remove(key)
                self._size -= 1
                return

    def get_keys(self) -> DynamicArray:
        """
        Returns a Dynamic Array of all keys in the hashmap
        """
        # initialize da
        key_array = DynamicArray()

        # iterate through buckets
        for i in range(0, self._capacity):
            for element in self._buckets[i]:
                key_array.append(element.key)

        return key_array

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns a tuple of a da with the most common element(s)
    and the number of times they occur
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length() // 3, hash_function_1)

    for i in range(0, da.length()):
        if map.contains_key(da[i]):
            count = map.get(da[i])
            map.put(da[i], count + 1)
        else:
            map.put(da[i], 1)

    # initialize counter, da
    ret_array = DynamicArray()
    curmax = 0
    key_array = map.get_keys()
    for i in range(0, key_array.length()):
        element = key_array[i]
        if map.get(element) == curmax:
            curmax = map.get(element)
            ret_array.append(element)
        elif map.get(element) > curmax:
            curmax = map.get(element)
            ret_array = DynamicArray()
            ret_array.append(element)

    return (ret_array, curmax)



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

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
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

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
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

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
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
