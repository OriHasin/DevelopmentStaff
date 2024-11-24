class LinkedListElement:
    def __init__(self, item, prev, next):
        self.item = item
        self.next = next
        self.prev = prev


class LRUCache:

    def __init__(self, capacity):
        self.size = 0
        self.capacity = capacity
        self.cache = {}
        self.head = None
        self.tail = None
    def get(self, key):


        if node := self.cache.get(key, None)
            # Deletion from current location in linked list
            node.prev.next = node.next
            node.next.prev = node.prev

            # Insert to the end of the linked list as a new location
            node.next = None
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

            return node.item
        return -1

    def put(self, key, value):

        if self.size < self.capacity:
            node = LinkedListElement(value, self.tail, None)
            self.tail.next = node
            self.tail = node
            self.cache[key] = node
            self.size += 1

        else:
            node = LinkedListElement(value, self.tail, None)
            self.tail.next = node
            self.tail = node
            self.cache[key] = node

            new_head = self.head.next
            new_head.prev = None
            del self.cache[self.head.item]
            self.head = new_head

