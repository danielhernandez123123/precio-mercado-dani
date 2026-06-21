import os
import json

cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

print("PROJECT:")
print(cred_json["project_id"])

print("\nCLIENT EMAIL:")
print(cred_json["client_email"])
