class Car:
    def __init__(self, link, text, year, engine_size, mileage, price):
        self.link = link
        self.text = text
        self.year = year
        self.engine_size = engine_size
        self.mileage = mileage
        self.price = price

class MaxHeap:
    def __init__(self, parameter):
        self.heap = []
        self.parameter = parameter

    def _left_child(self, index):
        return 2 * index + 1
    
    def _right_child(self, index):
        return 2*index + 2
    
    def _parent(self,index):
        return (index - 1) // 2
    
    def _swap(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def insert(self, value):
        self.heap.append(value)
        current = len(self.heap) - 1

        while current > 0 and (self.parameter(self.heap[current]) > self.parameter(self.heap[self._parent(current)])):
            self._swap(current, self._parent(current))
            current = self._parent(current)

    def remove(self):
        if len(self.heap) == 0:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        max_value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sink_down(0)

        return max_value
    
    def _sink_down(self, index):
        max_index = index
        while True:
            left_index = self._left_child(index)
            right_index = self._right_child(index)

            # if (left_index < len(self.heap)) and (self.parameter(self.heap[left_index]) > self.parameter(self.heap[max_index])):
            #     max_index = left_index

            # if (right_index < len(self.heap)) and (self.parameter(self.heap[right_index]) > self.parameter(self.heap[max_index])):
            #     max_index = right_index

            # if max_index != index:
            #     print("stuck")
            #     self._swap(index, max_index)
            #     index = max_index
            if left_index < len(self.heap) and self.parameter(self.heap[left_index]) > self.parameter(self.heap[max_index]):
                max_index = left_index

            # Compare with right child
            if right_index < len(self.heap) and self.parameter(self.heap[right_index]) > self.parameter(self.heap[max_index]):
                max_index = right_index

            # If no swap needed, break
            if max_index == index:
                break

            self._swap(index, max_index)
            index = max_index


                
class MinHeap:
    def __init__(self, parameter):
        self.heap = []
        self.parameter = parameter

    def _left_child(self, index):
        return 2 * index + 1
    
    def _right_child(self, index):
        return 2*index + 2
    
    def _parent(self,index):
        return (index - 1) // 2
    
    def _swap(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def insert(self, value):
        self.heap.append(value)
        current = len(self.heap) - 1

        while current > 0 and (self.parameter(self.heap[current]) < self.parameter(self.heap[self._parent(current)])):
            self._swap(current, self._parent(current))
            current = self._parent(current)

    def remove(self):
        if len(self.heap) == 0:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        max_value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sink_down(0)

        return max_value
    
    def _sink_down(self, index):
        max_index = index
        while True:
            left_index = self._left_child(index)
            right_index = self._right_child(index)

            if (left_index < len(self.heap)) and (self.parameter(self.heap[left_index]) < self.parameter(self.heap[max_index])):
                max_index = left_index

            if (right_index < len(self.heap)) and (self.parameter(self.heap[right_index]) < self.parameter(self.heap[max_index])):
                max_index = right_index

            if max_index != index:
                self._swap(index, max_index)
                index = max_index        
