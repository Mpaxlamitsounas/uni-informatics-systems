
def removeDuplicates(list):
    
    current = 0
    while True:  
        # Cannot use range(len(list)) because list length changes
        if current == len(list):
            break
        
        # If element appears again later in list
        if list[current] in list[current+1::]:
            # Delete current element, eventually only 1 unique will be left
            del list[current]
            # Shift current because deleting elements moves indexes of elements
            current -= 1
        
        current += 1
    
    return list
        
def sortList(list):
    #return list.sort()
    #Υποθέτω δεν ζητούσατε το παραπάνω
    
    # Selection sort
    for start, item in enumerate(list):
        # Initialises min with start of working list
        # Working list == sublist to the right of all previously found minima
        min = item
        min_index = start

        # Finds minimum item in working list
        for cur_index, cur_item in enumerate(list[start::], start):
            if cur_item < min:
                min, min_index = cur_item, cur_index
        
        # Swaps found minimum with start of working list
        (list[min_index], list[start]) = (list[start], list[min_index])
        
    return list
        
a_list = [11, 17, 8, 3, 4, 4, 18, 23, 19, 16, 17, 1, 22, 19, 4, 5, 21, 12, 11, 6, 11, 6, 1, 7, 24]
print(a_list)
removeDuplicates(a_list)
print(a_list)
sortList(a_list)
print(a_list)