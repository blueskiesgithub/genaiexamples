import unittest
import threading
import argparse

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
        self.cache = {}

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
            self.cache[data] = new_node

    def remove(self, data):
        if not isinstance(data, str):
            raise TypeError("Data must be a string")

        with self.lock:
            if self.head is None:
                raise ValueError("Cannot delete from an empty list")

            current = self.cache.get(data)
            if current is None:
                raise ValueError("Data not found in the list")

            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
            if current == self.head:
                self.head = current.next
            if current == self.tail:
                self.tail = current.prev
            
            self.size -= 1
            del self.cache[data]

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

class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.ll = LinkedList(max_size=TestLinkedList.max_size)

    def test_append_and_size(self):
        for i in range(TestLinkedList.data_quantity):
            self.ll.append(f"{TestLinkedList.data_type} {i}")
        self.assertEqual(self.ll.size, TestLinkedList.data_quantity, f"Size should be {TestLinkedList.data_quantity} after appending")

    def test_cache_consistency(self):
        self.ll.append("Test Data")
        self.assertIn("Test Data", self.ll.cache, "Cache should contain 'Test Data' after appending")
        self.ll.remove("Test Data")
        self.assertNotIn("Test Data", self.ll.cache, "Cache should not contain 'Test Data' after removal")

    def test_remove(self):
        self.ll.append("Remove Me")
        self.ll.remove("Remove Me")
        self.assertEqual(self.ll.size, 0, "Size should be 0 after removing the only item")

    def test_remove_nonexistent(self):
        with self.assertRaises(ValueError, msg="Removing a nonexistent item should raise ValueError"):
            self.ll.remove("Nonexistent")

    def test_append_over_max_size(self):
        for i in range(TestLinkedList.data_quantity):
            self.ll.append(f"{TestLinkedList.data_type} {i}")
        with self.assertRaises(OverflowError, msg="Appending beyond max size should raise OverflowError"):
            self.ll.append("Overflow")

    def test_thread_safety(self):
        def append_items():
            for i in range(TestLinkedList.data_quantity // 2):
                self.ll.append(f"Thread {TestLinkedList.data_type} {i}")

        thread1 = threading.Thread(target=append_items)
        thread2 = threading.Thread(target=append_items)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        self.assertEqual(self.ll.size, TestLinkedList.data_quantity, "Size should be correct after concurrent appends")

    def test_data_integrity(self):
        for i in range(TestLinkedList.data_quantity):
            self.ll.append(f"{TestLinkedList.data_type} {i}")
        for i in range(TestLinkedList.data_quantity // 2):
            self.ll.remove(f"{TestLinkedList.data_type} {i}")
        self.assertEqual(self.ll.size, TestLinkedList.data_quantity // 2, "Size should be correct after removing half the items")

    def test_reverse_print(self):
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.ll.append("First")
        self.ll.append("Second")
        self.ll.print_list_reverse()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "Second First", "Reverse print should output 'Second First'")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Test LinkedList with custom parameters")
    parser.add_argument('--quantity', type=int, default=10000, help='Number of data items to use in tests')
    parser.add_argument('--data_type', type=str, default='str', help='Type of data to use in tests: str, int, float, or char')
    parser.add_argument('--max_size', type=int, default=10000, help='Maximum size of the linked list')
    args, unknown = parser.parse_known_args()

    # Validate data_type against allowed types
    valid_types = {'str', 'int', 'float', 'char'}
    if args.data_type not in valid_types:
        parser.error(f"Invalid data_type '{args.data_type}'. Must be one of {valid_types}.")

    return args

if __name__ == "__main__":
    args = parse_arguments()
    TestLinkedList.data_quantity = args.quantity
    TestLinkedList.data_type = args.data_type
    TestLinkedList.max_size = args.max_size

    # Run the test suite with increased verbosity
    unittest.main(verbosity=2, argv=['first-arg-is-ignored'])