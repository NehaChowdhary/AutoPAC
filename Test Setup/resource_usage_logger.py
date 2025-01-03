import asyncio
import docker
from datetime import datetime

async def get_container_stats(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    stats = container.stats(stream=False)
    return stats

async def log_container_stats(container_id, log_file_prefix):
    try:
        while True:
            stats = await get_container_stats(container_id)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cpu_percent = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100
            memory_usage = stats['memory_stats']['usage'] / (1024 * 1024) # To MB

            log_file = f"{log_file_prefix}_{datetime.now().strftime('%Y%m%d')}.log"

            with open(log_file, 'a') as f:
                f.write(f"{timestamp} - CPU: {cpu_percent:.2f}% | Memory: {memory_usage:.2f} MB\n")

            await asyncio.sleep(5)  # Log every 5 seconds 
    except KeyboardInterrupt:
        print(f"Monitoring for container {container_id} stopped.")

async def main():
    client_container_name = "PrivateGPT-client"  
    server_container_name = "PrivateGPT-server"  

    client_log_file_prefix = "privategpt_log_files/privategpt_client_log_files/privategpt_client_resource.log"  
    server_log_file_prefix = "privategpt_log_files/privategpt_server_log_files/privategpt_server_resource.log" 

    tasks = [
        log_container_stats(client_container_name, client_log_file_prefix),
        log_container_stats(server_container_name, server_log_file_prefix)
    ]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())