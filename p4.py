s = input("Enter your paragraph: ")
print("Your paragraph:", s)

# Number of words
words = s.split()
count = len(words)
print("Number of words:", count)

# Unique words
unique_words = set(words)
print("Number of unique words:", len(unique_words))
print("Unique words:", unique_words)

# Longest word
longest_word = max(words, key=len)
print("Longest word:", longest_word)

# Shortest word
shortest_word = min(words, key=len)
print("Shortest word:", shortest_word)

# Sorting alphabetically
sorted_word = sorted(words)
print("Sorted words:", sorted_word)

# Find word 'hi'
print("Position of 'hi':", s.find("hi"))

# Duplicate words
duplicate = []
for word in words:
    if words.count(word) > 1 and word not in duplicate:
        duplicate.append(word)

print("Duplicated words:", duplicate)