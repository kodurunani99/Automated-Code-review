import ast
import subprocess
import tempfile
import os

def analyze_code(code_string):
    """Analyzes a code string using various tools and returns a list of issues."""
    try:
        # Write code to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(code_string)
            temp_file_path = temp_file.name

        # Static code analysis
        pylint_process = subprocess.Popen(['pylint', '--output-format=text', temp_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pylint_stdout, pylint_stderr = pylint_process.communicate()
        issues = pylint_stdout.split('\n')

        flake8_process = subprocess.Popen(['flake8', temp_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        flake8_stdout, flake8_stderr = flake8_process.communicate()
        issues.extend(flake8_stdout.split('\n'))

        # Remove the temporary file
        os.remove(temp_file_path)

        return issues

    except Exception as e:
        return [f"Error during analysis: {e}"]




def parse_pylint_output(output):
    """Parses the output of pylint and extracts issues."""
    issues = []
    lines = output.split('\n')
    for line in lines:
        if line.startswith('C') or line.startswith('W') or line.startswith('E'):
            issues.append(line)
    return issues


def provide_feedback(issues):
    """Formats and presents the issues in a user-friendly manner."""
    if not issues:
        print("No issues found.")
    for issue in issues:
        print(issue)






def main():
    """Reads Python code from a file and displays feedback."""
    try:
        file_path = input("Enter the path to the Python file to review: ")
        with open(file_path, 'r') as file:
            code_to_review = file.read()
        issues = analyze_code(code_to_review)
        if not issues:
            print("No issues found.")
        else:
            provide_feedback(issues)
    except FileNotFoundError:
        print("File not found. Please enter a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
