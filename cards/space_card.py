def space_card(intro_message_1, intro_message_2):
    card = [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [
                    {
                        "type": "ImageSet",
                        "images": [
                            {
                                "type": "Image",
                                "url": "https://user-images.githubusercontent.com/10964629/225653491-e3c2920c-419d-45ab-ba9f-b0add6138e33.png",  # noqa E501
                                "height": "100px",
                                "width": "400px",
                                "size": "Medium",
                            }
                        ],
                    },
                    {
                        "type": "TextBlock",
                        "text": "Fuse Session Room",
                        "horizontalAlignment": "Center",
                        "fontType": "Monospace",
                        "size": "Large",
                        "weight": "Bolder",
                    },
                    {
                        "type": "TextBlock",
                        "text": intro_message_1,
                        "wrap": True,
                        "fontType": "Monospace",
                        "horizontalAlignment": "Center",
                        "color": "Default",
                        "weight": "Bolder",
                    },
                    {
                        "type": "TextBlock",
                        "text": intro_message_2,
                        "wrap": True,
                        "fontType": "Monospace",
                        "color": "Default",
                        "weight": "Bolder",
                    },
                ],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.3",
            },
        }
    ]
    return card
