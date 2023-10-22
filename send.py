from azure.eventhub import EventHubProducerClient, EventData
import requests


EVENT_HUB_CONNECTION_STR = "Endpoint=sb://evhns-dev-we-tpiuolab-ms-01.servicebus.windows.net/;SharedAccessKeyName=SendAndListen;SharedAccessKey=U42zDy9DYLcUy2jb1VspmZ32Ik2/eaQxW+AEhISz53c="
EVENT_HUB_NAME = "evh-api-dev-we-tpiuolab-ms-01"


def get_top_data_engineering_posts(limit=10):
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
            if 'data' in data and 'children' in data['data']:
                top_posts = data['data']['children']
                '''
                for post in top_posts:
                    print(f"#{i}")
                    # print(f"Score: {post['data']['score']}")
                    print(f"By: {post['data']['author']}")
                    print(f"Timestamp: {datetime.datetime.fromtimestamp(post['data']['created_utc'])} ")
                    print("Content:")
                    print(post['data']['title'])
                    print(post['data']['selftext'])
                    print("--------------------------------------------------")
                '''
                return top_posts
            else:
                print("No post data found.")
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    

def send():
    # Get the top 10 posts from the data engineering subreddit
    top_10_posts = get_top_data_engineering_posts(10)

    # Create a producer client to send messages to the event hub.
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
    )

    # Create a batch.
    event_data_batch = producer.create_batch()

    # Add events to the batch.
    event_data_batch.add(EventData(str(top_10_posts)))

    # Send the batch of events to the event hub.
    with producer:
        producer.send_batch(event_data_batch)

    # Close the producer.
    producer.close()


if __name__ == "__main__":
    send()
    print("Done sending data.")
