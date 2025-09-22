##--------File Read & Write Challenge---------------##


#create input.txt with sample content
sample_text = """Python is a versatile programming language.
It is widely used for web development, data analysis, and automation among many other uses.
Many developers enjoy working with Python because of its simplicity.
The Python community is large and supportive.
Learning Python can open many opportunities in the tech industry."""

# Create and write to input.txt
with open('input.txt', 'w') as input_file:
    input_file.write(sample_text)

print("input.txt created successfully with 5 lines of text!")

# Read, process, and write to output.txt
    # Read the contents of input.txt
with open('input.txt', 'r') as input_file:
    content = input_file.read()
    
    # Count the number of words
words = content.split()
word_count = len(words)
#alternative shorthand ---> word_count = len(content.split())
    
    # Convert all text to uppercase
uppercaseText = content.upper()
    
    # Write processed text and word count to output.txt
with open('output.txt', 'w') as output_file:
    output_file.write(uppercaseText)
    output_file.write(f"\n\nTOTAL WORD COUNT: {word_count}")
    
    # Print success message
print(f"Success! output.txt has been created with {word_count} words\n\n")



##----Error Handling Lab task--------------##
filename = input("Enter filename to read: ")

try:
    with open(filename, 'r') as file:
        content = file.read()
    print(f"\nFile content:\n{content}")
    
except FileNotFoundError:
    print(f"Error: File '{filename}' not found!")
except PermissionError:
    print(f"Error: No permission to read '{filename}'!")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    


