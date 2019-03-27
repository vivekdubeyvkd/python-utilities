
# create a new empty file named abc.txt
f = open("abc.txt", "x")

# Open the file "abc.txt" and append the content to file, "a" will also create "abc.txt" file if this file does not exist
f = open("abc.txt", "a")
f.write("Now the file has one more line!") 

# Open the file "abc.txt" and overwrite the content of entire file, "w" will also create "abc.txt" file if this file does not exist
f = open("abc.txt", "w")
f.write("Woops! I have deleted the content!")
