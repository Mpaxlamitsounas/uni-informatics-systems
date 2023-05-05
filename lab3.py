from pymongo import MongoClient

connection = MongoClient()
collection = connection['InfoSys']['Students']

print("---")
# 1
collection.insert_one({'name'        : 'John Koulouras',
                       'email'       : 'ioanniskoulouras.unipi@gmail.com',
                       'yearOfBirth' : 2002, 
                       'gender'      : 'male'})
results = collection.find({'name' : 'John Koulouras'}, {'_id': False})
print(results[0])

print("---")
# 2
results = collection.find({'yearOfBirth' : {'$gte' : 1996}})
for i in range(collection.count_documents({})):
    try:
        print(results[i])
    except:
        break
   
print("---") 
# 3
results = collection.find_one({'yearOfBirth' : {'$gte' : 1996}})
print(results)

print("---")
# 4
results = collection.count_documents({'gender' : 'female', 'yearOfBirth' : {'$lt' : 1996}})
print(results)

print("---")
