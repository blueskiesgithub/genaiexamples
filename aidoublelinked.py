import threading

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class LinkedList:
    def __init__(self, max_size=None):
        self.head = None
        self.tail = None
        self.size = 0
        self.max_size = max_size
        self.lock = threading.Lock()
        self.cache = {}  # Cache to store node references for quick access

    def append(self, data):
        if not isinstance(data, str):
            raise TypeError("Data must be a string")
        if len(data) > 1000:
            raise ValueError("Data size exceeds maximum limit")
        
        with self.lock:
            if self.max_size is not None and self.size >= self.max_size:
                raise OverflowError("Linked list is full")
            
            new_node = Node(data)
            
            if self.head is None:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node
            
            self.size += 1
            self.cache[data] = new_node  # Add node to cache

    def remove(self, data):
        if not isinstance(data, str):
            raise TypeError("Data must be a string")

        with self.lock:
            if self.head is None:
                raise ValueError("Cannot delete from an empty list")

            # Use cache to quickly find the node
            current = self.cache.get(data)
            if current is None:
                raise ValueError("Data not found in the list")

            # Adjust pointers to remove the node
            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
            if current == self.head:
                self.head = current.next
            if current == self.tail:
                self.tail = current.prev
            
            self.size -= 1
            del self.cache[data]  # Remove node from cache

    def print_list(self):
        with self.lock:
            current = self.head
            while current:
                print(current.data, end=" ")
                current = current.next
            print()

    def print_list_reverse(self):
        with self.lock:
            current = self.tail
            while current:
                print(current.data, end=" ")
                current = current.prev
            print()

# Example usage
ll = LinkedList(max_size=1000)
ll.append("Data 1")
ll.append("Data 2")
ll.print_list()  # Output: Data 1 Data 2
ll.print_list_reverse()  # Output: Data 2 Data 1
ll.remove("Data 1")
ll.print_list()  # Output: Data 2