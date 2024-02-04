from time import sleep

import aiohttp

from cards import space_card
from utils import preferences as p

webex_create_room_url = "https://webexapis.com/v1/rooms"
webex_memberships_url = "https://webexapis.com/v1/memberships"
webex_messages_url = "https://webexapis.com/v1/messages"

headers = {
    "Authorization": p.fusebot_help_bearer,
    "Content-Type": "application/json",
}


async def make_space(fuse_date, SE1_name, SE2_name):
    room_name = (
        f"Fuse Session ({fuse_date}) - Intro space for {SE1_name} and {SE2_name}"
    )
    room_body = {
        "title": room_name,
        "isLocked": False,
        "description": f"Fuse Session - Intro space for {SE1_name} and {SE2_name}",
    }

    async with aiohttp.ClientSession() as session:
        for _ in range(5):
            try:
                async with session.post(
                    webex_create_room_url, headers=headers, json=room_body
                ) as resp:
                    response = await resp.json()
                    print(response)
                    if resp.status == 200:
                        room_id = response["id"]
                        print(f"   Room created: {room_name}")
                        print(f"    Room ID: {room_id}")
                        return room_id
            except Exception as e:
                print(f"   *** Room creation failed: {resp.status}")
                print(f"   *** Sleeping for {pow(2, _)} seconds and trying again.")
                sleep(pow(2, _))
                print(e)


async def add_ses_to_room(SE_emails, wa_room):
    async with aiohttp.ClientSession() as session:
        for x, email in enumerate(SE_emails):
            membership_body = {
                "roomId": wa_room,
                "personEmail": email,
            }
            for _ in range(5):
                try:
                    async with session.post(
                        webex_memberships_url, headers=headers, json=membership_body
                    ) as resp:
                        if resp.status == 200:
                            print(f"    SE{x + 1} added to room.")
                            break
                except Exception as e:
                    print(f"    *** SE{x + 1} ({email}) failed to add to room.")
                    print(f"    *** Sleeping for {pow(2, _)} seconds and trying again.")
                    sleep(pow(2, _))
                    print(e)


async def send_intro_message(wa_room):
    intro_card = space_card.space_card(p.intro_message_1, p.intro_message_2)
    intro_message_body = {
        "roomId": wa_room,
        "markdown": p.intro_message_1,
        "attachments": intro_card,
    }

    async with aiohttp.ClientSession() as session:
        for _ in range(5):
            try:
                async with session.post(
                    webex_messages_url, headers=headers, json=intro_message_body
                ) as resp:
                    response = await resp.json()
                    if resp.status == 200:
                        print(f"    Intro message sent ({resp.status})")
                        print(f"     Message ID: {response['id']}")
                        break
            except Exception as e:
                print(f"    *** Intro message failed ({resp.status})")
                print(f"    *** Sleeping for {pow(2, _)} seconds and trying again.")
                sleep(pow(2, _))
                print(e)


async def send_follow_up_message(wa_room):
    async with aiohttp.ClientSession() as session:
        for _ in range(5):
            try:
                async with session.post(
                    webex_messages_url,
                    headers=headers,
                    json={"roomId": wa_room, "markdown": p.follow_up_message},
                ) as resp:
                    response = await resp.json()
                    if resp.status == 200:
                        print(f"    Follow-up message sent ({resp.status})")
                        print(f"     Message ID: {response['id']}")
                        print("   Setup complete.")
                        break
            except Exception as e:
                print(f"  *** Follow-up message failed ({resp.status})")
                print(f"  *** Sleeping for {pow(2, _)} seconds and trying again.")
                sleep(pow(2, _))
                print(e)


async def get_room_details(room_id):
    webex_room_details_url = f"https://webexapis.com/v1/rooms/{room_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(webex_room_details_url, headers=headers) as resp:
            wa_room_details = await resp.json()
            return wa_room_details
