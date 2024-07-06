import hashlib

def generate_secret_key(activation_key, domain_name):
    combined_string = activation_key + domain_name
    hash_object = hashlib.sha256(combined_string.encode())
    secret_key = hash_object.hexdigest()
    return secret_key

# Example usage
activation_key = "B"
domain_name = "A"
secret_key = generate_secret_key(activation_key, domain_name)
print(f"Secret Key: {secret_key}")