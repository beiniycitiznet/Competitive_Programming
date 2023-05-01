import heapq
import os

chunkSize = 2 * 1024 * 1024

def read_chunk(file):
    res=[]
    for line in file.readlines(chunkSize):
        res.append(int(line.strip()))
    return res

def merge_sorted_chunks(sorted_files, output_file):
    sorted_chunks = []
    for file in sorted_files:
        sorted_chunks.append(open(file, 'r'))

    heap = []
    for i in range(len(sorted_chunks)):
        number = int(sorted_chunks[i].readline().strip())
        heap.append((number, i))
    heapq.heapify(heap)

    while heap:
        smallest_number, smallest_file_index = heapq.heappop(heap)
        output_file.write(str(smallest_number) + '\n')

        next_line = sorted_chunks[smallest_file_index].readline().strip()
        if next_line:
            next_number = int(next_line)
            next_file_index = smallest_file_index
            heapq.heappush(heap, (next_number, next_file_index))

    for file in sorted_chunks:
        file.close()

# Main function to sort the numbers from a file
def sort_numbers(input_file, output_file):
    # Read and sort each chunk of data
    sorted_files = []
    while True:
        chunk = read_chunk(input_file)
        if not chunk:
            break
        chunk.sort()
        sorted_file = 'sorted_chunk_%d.txt' % len(sorted_files)
        with open(sorted_file, 'w') as f:
            f.writelines('%d\n' % number for number in chunk)
        sorted_files.append(sorted_file)

    # Merge the sorted chunks into a single output file
    merge_sorted_chunks(sorted_files, output_file)

    # Delete the sorted chunk files
    for file in sorted_files:
        os.remove(file)
