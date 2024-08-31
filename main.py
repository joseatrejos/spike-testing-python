import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests, os, json, random, string, time
from dotenv import load_dotenv

load_dotenv()

# Define the API endpoint
API_URL = os.getenv("API_URL")

# Shared counter and lock for thread-safe incrementing
api_call_count = 0
counter_lock = threading.Lock()

# Function to make the API call
def make_api_call():
    global api_call_count

    base_data = {
    }
    
    headers = {
        "Authorization": f"""Bearer {os.getenv("AUTH_TOKEN")}""",
        "Content-Type": "application/json"
    }

    try:
        response = requests.request("POST", API_URL, headers=headers, data=json.dumps(data_copy))
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