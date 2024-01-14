import asyncio

from azure.eventhub.aio import EventHubConsumerClient

EVENT_HUB_CONNECTION_STR = "Endpoint=sb://evhns-dev-hr-tpiuo-ms-01.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=WOVOO4BrzTTqxF9K+AlYbpOEFgqffjVU9+AEhA0MxUc="
EVENT_HUB_NAME = "evh-redditapi-dev-we-tpiuolab-ms-01"


async def on_event(partition_context, event):
    # Print the event data.
    print(event.body_as_str(encoding="UTF-8"), partition_context.partition_id)

    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)


async def consume():
    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string(
        EVENT_HUB_CONNECTION_STR,
        consumer_group="$Default",
        eventhub_name=EVENT_HUB_NAME,
    )
    async with client:
        # Call the receive method. Read from the beginning of the
        # partition (starting_position: "-1")
        await client.receive(on_event=on_event, starting_position="-1")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Run the main method.
    loop.run_until_complete(consume())
