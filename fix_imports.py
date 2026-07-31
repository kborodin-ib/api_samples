import os
import re

def update_pb2_imports(directory):
    pattern = re.compile(r'^(import\s+)(\w+_pb2)(\s+as\s+\w+__pb2)', re.MULTILINE)

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                
                with open(filepath, 'r', encoding='utf-8') as file:
                    original_content = file.read()

                # Replace matched import statements
                updated_content = pattern.sub(r'\1ibapi.protobuf.\2\3', original_content)

                # Only write back if something changed
                if updated_content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(updated_content)
                    print(f"Updated: {filepath}")
                else:
                    print(f"No changes in: {filepath}")

# Example usage
if __name__ == '__main__':
    directory_to_search = '.'  # Replace with your target directory
    update_pb2_imports(directory_to_search)
