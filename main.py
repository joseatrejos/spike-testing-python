import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests, os, json, random, string, time

# Define the API endpoint
API_URL = "https://eozlhp8axyofy9k.m.pipedream.net"

# Shared counter and lock for thread-safe incrementing
api_call_count = 0
counter_lock = threading.Lock()

# Function to make the API call
def make_api_call():
    global api_call_count

    base_data = {
        "folio_unico": "1",
        "marca": "Honda",
        "modelo": "string",
        "color": "string",
        "tipo_vehiculo": 3,
        "no_placa_frontal": "string",
        "no_placa_trasera": "string",
        "vpn": "001",
        "ip_carril": "1.1.1.1",
        "tag_carril": "00I",
        "imagenes": [
            {
                "tipo_imagen": 1,
                "id_dispositivo": "1",
                "fecha_hora": "2024-08-09T10:15:30",
                "tipo_dispositivo": "string",
                "folio_unico_img": "4",
                "url_img": "https://i.pinimg.com/564x/26/5e/a6/265ea61bd4c914c6c99deee75e8f2c92.jpg"
            },
            {
                "tipo_imagen": 2,
                "id_dispositivo": "1",
                "fecha_hora": "2024-08-09T10:15:30",
                "tipo_dispositivo": "string",
                "folio_unico_img": "5",
                "url_img": "https://i.pinimg.com/564x/6e/0d/86/6e0d86e3bb85bd7674b47f7244f2f6eb.jpg"
            },
            {
                "tipo_imagen": 3,
                "id_dispositivo": "3",
                "fecha_hora": "2024-08-09T10:15:30",
                "tipo_dispositivo": "string",
                "folio_unico_img": "6",
                "url_img": "https://i.pinimg.com/564x/fa/4f/ea/fa4fea5285aeaf3f425a663413749b46.jpg"
            }
        ],
        "fecha_hora_deteccion": "2024-08-09T10:15:30",
        "lista_negra": {
                "deteccion_frontal": "",
                "deteccion_trasera": "",
                "deteccion_rostro": ""
        }
    }
    random_folio = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    data_copy = json.loads(json.dumps(base_data))
    data_copy["folio_unico"] = random_folio
    data_copy["imagenes"][0]["folio_unico_img"] = random_folio
    data_copy["imagenes"][1]["folio_unico_img"] = random_folio + '1'
    data_copy["imagenes"][2]["folio_unico_img"] = random_folio + '2'
    
    url = "https://coveli-sa.software-demo.com/api/seleccion/"

    headers = {
        'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1NzQ1MjMyLCJpYXQiOjE3MjUxNDA0MzIsImp0aSI6IjhjZjUwNmRjZjQ3NDQwY2I5ZjRkYTc4N2UwYzIwYmQxIiwidXNlcl9pZCI6MTJ9.N0_3ql-PZnVKsSFT6XODE3xZpfYAgNy8-5tymc4sXmE',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(data_copy))
        # Increment the counter safely
        with counter_lock:
            global api_call_count
            api_call_count += 1

        # Process the response here
        print(f"Response: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error: {e}")

# Function that runs in each thread
def worker_function():
    # Get the number of workers that the thread pool can handle (os.cpu_count())
    max_workers = os.cpu_count()
    # Use ThreadPoolExecutor to create a pool of workers
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(make_api_call) for _ in range(max_workers)]
        
        # Wait for all futures to complete
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Worker error: {e}")

# Main function
def main():
    # Get the maximum number of threads your CPU can handle and subtract one
    max_threads = os.cpu_count()
    #print(max_threads)

    # List to hold the threads
    threads = []
    
    # Create threads
    for _ in range(max_threads):
        thread = threading.Thread(target=worker_function)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Print the total number of API calls made
    print(f"Total API calls made: {api_call_count}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Execution completed in {time.time() - start_time} seconds")