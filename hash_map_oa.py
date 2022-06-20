# Name: Nicholas Brooks
# OSU Email: brooksni@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap Implementation
# Due Date: 06/03/2022
# Description: Implement a HashMap with Open Addressing


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

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
        Updates the key/value pair in the hash map
        If the key already exists, the value is replaced
        If no key exists, the key/value pair must be added
        """
        # determine the hash, index
        hash = self._hash_function(key)
        index = hash % self._capacity
        j = 1

        # check to see if the key is in the map
        if self.contains_key(key):
            for i in range(0, self._capacity):
                element = self._buckets[i]
                if element is not None and element.key == key:
                    self._buckets[i].value = value
                    return
        else:
            if self.table_load() >= 0.5:
                self.resize_table(self._capacity * 2)
                index = hash % self._capacity
            tracker = self._buckets[index]
            newindex = index
            while tracker is not None and not tracker.is_tombstone:
                newindex = (index + (j * j)) % self._capacity
                j += 1
                tracker = self._buckets[newindex]
            self._buckets[newindex] = HashEntry(key, value)
            self._size += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table
        All key/value pairs must remain in the new hash map (rehashed)
        If the new capacity is less than 1 or less than the number of elements, nothing happens
        """
        # check to see if the new capacity is valid
        if new_capacity < 1 or new_capacity < self._size:
            return

        # initialize new hashmap
        newmap = HashMap(new_capacity, self._hash_function)

        counter = self._capacity

        for i in range(0, counter):
            element = self._buckets[i]
            if element is not None:
                newmap.put(element.key, element.value)

        self._size = newmap._size
        self._buckets = newmap._buckets
        self._capacity = newmap._capacity

    def get(self, key: str) -> object:
        """
        Returns the value associated w/ the given key
        If key doesn't exist, return none
        """
        # check if the key is in the hash map
        if self.contains_key(key) is None:
            return None
        else:
            for i in range(0, self._capacity):
                element = self._buckets[i]
                if element:
                    if element.key == key:
                        if element.is_tombstone:
                            continue
                        else:
                            return element.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns true if the key is in the table, false otherwise
        """
        for i in range(0, self._capacity):
            element = self._buckets[i]
            if element:
                if element.key == key:
                    if element.is_tombstone:
                        continue
                    else:
                        return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its value from the hash map
        If the key is not in the hash map, nothing happens
        """
        # check to see if the key exists
        if self.contains_key(key) is None:
            return

        for i in range(0, self._capacity):
            element = self._buckets[i]
            if element is not None:
                if element.key == key:
                    if not element.is_tombstone:
                        element.is_tombstone = True
                        self._size -= 1
                    return

    def clear(self) -> None:
        """
        Clears the hash map
        Capacity is not changed
        """
        # initialize new hashmap object
        clearedmap = HashMap(self._capacity, self._hash_function)

        # reassign variables
        self._buckets = clearedmap._buckets
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        returns a dynamic array of all keys
        """
        # initialize da
        key_array = DynamicArray()

        # iterate through buckets
        for i in range(0, self._capacity):
            element = self._buckets[i]
            if element is not None and not element.is_tombstone:
                key_array.append(element.key)

        return key_array


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print(m.get_size())
    for i in range(150):
        m.remove('str' + str(i))
        print(m.get_size())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')
        m.put('some key', 'some value')

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
