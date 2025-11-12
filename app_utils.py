# generate a metadata key (remove also all special characters)
def generate_key(name: str) -> str:
    import re

    # Convert to lowercase
    key = name.lower()
    # Replace spaces with underscores
    key = key.replace(" ", "_")
    # Remove special characters
    key = re.sub(r'\W+', '', key)
    return key