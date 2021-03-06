import heapq


class OpenListHeap(object):
    """ A custom heap I made to serve as an open list. This was created because the heapq heaps are a bit cumbersome.
    """
    def __init__(self):
        self.internal_heap = []
        self.entry_count = 0

    def push(self, item, first_param, second_param):

        heapq.heappush(self.internal_heap, (first_param, second_param, self.entry_count, item))
        self.entry_count += 1  # Add some uniqueness to items in the heap to avoid comparison between nodes..

    def pop(self):
        return heapq.heappop(self.internal_heap)[3]

    def heapify(self):
        heapq.heapify(self.internal_heap)
