import os
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


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
# sheet = client.open('top50').sheet1

projList = client.open("Project List")
parameters = projList.get_worksheet(0)


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
            # Write the folders to the Google Sheet
            folder_data = [{"Projects": folder} for folder in result]

            # Convert the data to a DataFrame
            df = pd.DataFrame(folder_data)

            # Write the DataFrame to the Google Sheet
            set_with_dataframe(parameters, df)

            print("Folders have been written to the Google Sheet.")
        else:
            print("No folders contain desc.json.")
