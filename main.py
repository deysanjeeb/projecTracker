import os


def find_folders_with_desc_json(directory):
    folders_with_desc = []

    # Iterate through items in the directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # Check if it's a folder and contains desc.json
        if os.path.isdir(item_path) and "desc.json" in os.listdir(item_path):
            folders_with_desc.append(item)

    return folders_with_desc


if __name__ == "__main__":
    directory = input("Enter the workspace path: ").strip()

    if not os.path.isdir(directory):
        print("Invalid directory path.")
    else:
        result = find_folders_with_desc_json(directory)

        if result:
            print("Folders containing desc.json:")
            for folder in result:
                print(f"- {folder}")
        else:
            print("No folders contain desc.json.")
