import datetime

import requests


def get_top_dataengineering_posts(limit=10):
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
                i = 1
                for post in top_posts:
                    print(f"#{i}")
                    # print(f"Score: {post['data']['score']}")
                    print(f"By: {post['data']['author']}")
                    print(f"Timestamp: {datetime.datetime.fromtimestamp(post['data']['created_utc'])} ")
                    print("Content:")
                    print(post['data']['title'])
                    print(post['data']['selftext'])
                    print("--------------------------------------------------")
                    i += 1
            else:
                print("No post data found.")
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    get_top_dataengineering_posts()
