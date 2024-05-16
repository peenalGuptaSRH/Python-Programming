#Class for Disk Stacking with maximum height in descending order
class StackDisks: 
    #Constructor of the class to initialize the instance variable with the sorted disks in descendng order
    def __init__(self, disks):
        #Sorting in descending order
        self.disks = sorted(disks, key=lambda disk: (-disk[0], -disk[1], -disk[2]))

    #Method to check if the disk can be placed on top of another disk
    def checkToInsertOnTopOrBottom(self, bottom, top):
        return bottom[0] > top[0] and bottom[1] > top[1] and bottom[2] > top[2]

    def findStackOfMaxHeight(self):
        #Array of heights
        heights = [disk[2] for disk in self.disks]
        #sequence of disks
        sequences = [None] * len(self.disks)
        max_height_index = 0
        for i in range(1, len(self.disks)):
            for j in range(0, i):
                if self.checkToInsertOnTopOrBottom(self.disks[j], self.disks[i]):
                    if heights[i] < heights[j] + self.disks[i][2]:
                        heights[i] = heights[j] + self.disks[i][2]
                        sequences[i] = j
                        if heights[i] > heights[max_height_index]:
                            max_height_index = i

        return self.createDiskSequence(sequences, max_height_index)

    def createDiskSequence(self, sequences, current_index):
        sequence = []
        while current_index is not None:
            sequence.append(self.disks[current_index])
            current_index = sequences[current_index]
        return list(reversed(sequence))

# Sample usage
if __name__ == "__main__":
    #input for the disks to be sorted
    disks = [[2, 1, 2], [3, 2, 3], [2, 2, 8], [2, 3, 4], [1, 3, 1], [4, 4, 5]]
    # disks = [[3, 2, 3], [2, 2, 8], [2, 3, 4], [8, 6, 2], [5, 4, 3], [1, 3, 1], [4, 4, 5]]
    # disks = [[1, 1, 2],[2, 3, 4],[5, 5, 5],[2, 1, 5]]

    
    # gets the sorted disks
    sorted_disk_stack = StackDisks(disks)
    
    #gets the stack with maximum height
    finalStackwithMaxHeight = sorted_disk_stack.findStackOfMaxHeight()
    print(finalStackwithMaxHeight)

# O(n^2) is the time complexity, where n is the number of disks. This is due to the possibility that we will update the maximum height stack by comparing each disk with every other disk.

# Space Complexity: O(n), where n is the number of disks, for storing the disk heights and sequences.

