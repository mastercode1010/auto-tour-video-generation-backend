import os

def client_image_path(instance, filename, side_key):
    # Determine the file extension; assuming PNG as per requirements
    ext = 'png'
    client_id = instance.client_id if hasattr(instance, 'client_id') else 'unknown'
    image_type = ['front_1', 'front_2', 'left', 'right'][side_key-1]
    filename = f"{client_id}_{image_type}.{ext}"
    return os.path.join('clients', str(client_id), filename)
