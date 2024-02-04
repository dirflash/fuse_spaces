# Description: This script, using asyncio, creates Webex spaces for each pair of SEs for the Fuse date discussion
# This script is a part of the Fuse project and is not intended for use outside of the project.
# Author: Aaron Davis
# Company: Cisco
# Creation Date: 2024-02-04
# Modified Date: 2024-02-04


import asyncio
from time import perf_counter, sleep
from typing import List

from pymongo.errors import ConnectionFailure

from utils import async_webex_actions as wa
from utils import preferences as p

TEST_MODE = True

fuse_date = "1/19/2024"


async def webex_activities(fuse_date, SE1_name, SE2_name, SE_emails):
    # Create a Webex App room for each pair
    room_id = await wa.make_space(fuse_date, SE1_name, SE2_name)
    # Add SE1 and SE2 to the room
    await wa.add_ses_to_room(SE_emails, room_id)
    # Send intro message to the room
    await wa.send_intro_message(room_id)
    # Send follow-up message to the room
    await wa.send_follow_up_message(room_id)


async def run_webex_activities(partner_pairs, se_name_dict):
    tasks = []
    pairs = 0
    for x in partner_pairs:
        print(f"  Setup for pair {pairs + 1} of {len(partner_pairs)}")
        print(f"   SE1: {x[0]}, SE2: {x[1]}")
        SE1_name = se_name_dict.get(x[0], "Unknown")
        SE2_name = se_name_dict.get(x[1], "Unknown")
        SE_emails = [f"{x[0]}@cisco.com", f"{x[1]}@cisco.com"]
        print(f"   Pair email addresses: {SE_emails}")
        tasks.append(webex_activities(fuse_date, SE1_name, SE2_name, SE_emails))
        pairs += 1
    await asyncio.gather(*tasks)


async def main():
    start_timer = perf_counter()
    # Fetch all matches at once
    for _ in range(5):
        try:
            all_matches = list(
                p.cwa_matches.find(
                    {"assignments": {"$exists": True}},
                    {"_id": 0, "SE": 1, "assignments": 1},
                )
            )
            break
        except ConnectionFailure as e:
            print(
                f"*** Failed to fetch matches. Sleeping for {pow(2, _)} seconds and trying again."
            )
            sleep(pow(2, _))
            print(e)

    # Filter matches in memory
    matches = [match for match in all_matches if fuse_date in match["assignments"]]

    del all_matches

    # room_matches = set()
    seed_value = set()

    for match in matches:
        room_match = {match["SE"]: match["assignments"][fuse_date]}
        # room_matches.add(frozenset(room_match.items()))

        for key, value in room_match.items():
            if key not in seed_value:
                seed_value.add(value)

    del key, value, room_match
    partner_pairs = []

    for _ in seed_value:
        # Find partner in memory
        partner = next((match for match in matches if match["SE"] == _), None)

        if partner is not None:
            partner_pairs.append([_, partner["assignments"][fuse_date]])

    del matches, match, partner, seed_value
    print("*** Partner pairs ***")
    print(partner_pairs)
    print(f" Number of pairs: {len(partner_pairs)}")

    # Gather all unique SE values
    all_se = {se for pair in partner_pairs for se in pair}

    # Query all SE values at once
    for _ in range(5):
        try:
            all_se_names = p.se_info.find(
                {"se": {"$in": list(all_se)}}, {"_id": 0, "se": 1, "se_name": 1}
            )
            break
        except ConnectionFailure as e:
            print(
                f"*** Failed to fetch SE names. Sleeping for {pow(2, _)} seconds and trying again."
            )
            sleep(pow(2, _))
            print(e)

    # Map se to se_name for quick access
    se_name_dict = {doc["se"]: doc["se_name"] for doc in all_se_names}

    del all_se, all_se_names
    SE_emails: List[str] = []

    print("\nStarting Webex activities...")

    if not TEST_MODE:
        await run_webex_activities(partner_pairs, se_name_dict)
    else:
        print("\n*** Test mode ***")
        SE1_name = p.SE1_name
        SE1_email = p.SE1_email
        SE2_name = p.SE2_name
        SE2_email = p.SE2_email
        SE_emails = [SE1_email, SE2_email]
        print(f" Pair email addresses: {SE_emails}")
        await webex_activities(fuse_date, SE1_name, SE2_name, SE_emails)

    end_timer = perf_counter()
    print(f"Total time: {end_timer - start_timer:.2f} seconds")


asyncio.run(main())
