import requests
import msal

# Initialize the MSAL confidential client
app = msal.ConfidentialClientApplication(
    "<your-app-id>",  # Replace with your app id
    authority="https://login.microsoftonline.com/<your-tenant-id>",  # Replace with your tenant id
    client_credential="<your-client-secret>",  # Replace with your client secret
)

# Get access token
result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

if "access_token" in result:
    # Make a GET request to the OneDrive API endpoint
    headers = {
        'Authorization': 'Bearer ' + result['access_token']
    }
    response = requests.get('https://graph.microsoft.com/v1.0/me/drive/root/children', headers=headers)

    # Print the names of the files in OneDrive
    for file in response.json()['value']:
        print(file['name'])
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug