import os
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import subprocess
from dotenv import load_dotenv


load_dotenv()
workspace = os.environ.get("WORKSPACE_PATH")


def get_github_url(repo_path):
    """
    Retrieve the GitHub URL for a given repository path.

    Args:
        repo_path (str): Path to the repository

    Returns:
        str: GitHub URL or None if not found
    """
    try:
        # Change to the repository directory
        original_dir = os.getcwd()
        os.chdir(repo_path)

        # Get the remote URL
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
        )

        # Change back to the original directory
        os.chdir(original_dir)

        # Clean up the URL
        url = result.stdout.strip()

        # Convert SSH URLs to HTTPS URLs if needed
        if url.startswith("git@"):
            # Convert git@github.com:username/repo.git to https://github.com/username/repo.git
            url = url.replace(":", "/").replace("git@", "https://").replace(".git", "")

        return url if url else None

    except Exception as e:
        print(f"Error retrieving GitHub URL for {repo_path}: {e}")
        return None


def find_folders_with_desc_json(directory):
    """
    Find folders containing desc.json and their GitHub URLs.

    Args:
        directory (str): Path to search for folders

    Returns:
        list: List of dictionaries with folder and GitHub URL
    """
    folders_with_details = []

    # Iterate through items in the directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # Check if it's a folder and contains desc.json
        if os.path.isdir(item_path) and "desc.json" in os.listdir(item_path):
            # Try to get GitHub URL
            github_url = get_github_url(item_path)

            folders_with_details.append(
                {"Projects": item, "GitHub URL": github_url or "URL Not Found"}
            )

    return folders_with_details


if __name__ == "__main__":
    # Use the credentials file you downloaded from the Google Cloud Console
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "secrets/credentials.json", scope
    )

    # Authenticate with Google
    client = gspread.authorize(creds)
    projList = client.open("Project List")
    parameters = projList.get_worksheet(0)

    # Get directory path from user input
    directory = workspace

    if not os.path.isdir(directory):
        print("Invalid directory path.")
    else:
        # Find folders with desc.json and their GitHub URLs
        result = find_folders_with_desc_json(directory)

        if result:
            print("Folders containing desc.json:")
            for item in result:
                print(f"- {item['Projects']}: {item['GitHub URL']}")

            # Convert the data to a DataFrame
            df = pd.DataFrame(result)

            # Write the DataFrame to the Google Sheet
            # Clear existing content first
            parameters.clear()

            # Write headers and data
            set_with_dataframe(parameters, df)

            print("Folders and GitHub URLs have been written to the Google Sheet.")
        else:
            print("No folders contain desc.json.")
