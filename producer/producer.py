import asyncio
import os
import requests

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient


EVENT_HUB_CONNECTION_STR = str(os.environ["EVENT_HUB_CONNECTION_STR"])
EVENT_HUB_NAME = str(os.environ["EVENT_HUB_NAME"])


async def get_top_data_engineering_posts(limit=10):
    # Define the URL for the Reddit API endpoint
    url = f"https://www.reddit.com/r/dataengineering/top.json?limit={limit}"

    try:
        # Send a GET request to the Reddit API
        response = requests.get(url, headers={"User-Agent": "YourAppName/1.0"})

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and display the top posts
            if "data" in data and "children" in data["data"]:
                top_posts = data["data"]["children"]
                """
                for post in top_posts:
                    print(f"#{i}")
                    # print(f"Score: {post['data']['score']}")
                    print(f"By: {post['data']['author']}")
                    print(f"Timestamp: {datetime.datetime.fromtimestamp(post['data']['created_utc'])} ")
                    print("Content:")
                    print(post['data']['title'])
                    print(post['data']['selftext'])
                    print("--------------------------------------------------")
                """
                return top_posts
            else:
                print("No post data found.")
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")


async def produce():
    # Get the top 10 posts from the data engineering subreddit
    top_10_posts = await get_top_data_engineering_posts(10)

    # Create a producer client to send messages to the event hub.
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
    )

    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(str(top_10_posts)))

        # Send the batch of events to the event hub.
        print("Sending batch to event hub...")
        await producer.send_batch(event_data_batch)


if __name__ == "__main__":
    asyncio.run(produce())
    while True:
        pass
