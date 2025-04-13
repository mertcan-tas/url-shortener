import sys
from django.core.management.utils import get_random_secret_key

def main():
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python generate_env.py <env-copy-file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    
    try:
        # Try to read the input .env copy file
        with open(input_file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        # If the file is not found, print an error and exit
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    # Generate a new Django SECRET_KEY with the "django-insecure-" prefix
    secret_key = "django-insecure-" + get_random_secret_key()

    # Loop through each line in the file
    for line in lines:
        # If the line is for SECRET_KEY, replace it with the newly generated one
        if line.startswith("SECRET_KEY="):
            print(f'SECRET_KEY="{secret_key}"')
        else:
            # Otherwise, print the line as-is (stripping trailing newlines)
            print(line.strip())

# Call the main function when the script is executed
if __name__ == "__main__":
    main()