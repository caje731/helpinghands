test_cases = int(raw_input())
for t in range(test_cases):
	size = int(raw_input())
	the_list = [int(i) for i in raw_input().split()]
	
	# aux array to store frequencies
	buckets = [0]*(max(the_list)+1)
	
	# Count frequency of each element
	for i in the_list:
		buckets[i] = buckets[i]+1
	
	the_list = []
	# Since we need non-increasing order, start from the back	
	for i in range(size,-1, -1):
		if buckets[i] > 0:
			the_list.extend([i]*buckets[i])
	
	print ' '.join([str(i) for i in the_list])