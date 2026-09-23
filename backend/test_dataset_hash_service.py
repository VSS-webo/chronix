print("JAI SHRIRAM")

from app.services.dataset_service import (
    calculate_sha256,
    get_dataset_metadata,
)


with open("test.csv", "rb") as file:
    data = file.read()


file_hash = calculate_sha256(data)

metadata = get_dataset_metadata(data)


print("SHA-256:")
print(file_hash)

print("\nMetadata:")
print(metadata)