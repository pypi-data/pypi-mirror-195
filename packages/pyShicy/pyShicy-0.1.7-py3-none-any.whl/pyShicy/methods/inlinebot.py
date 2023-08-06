from fipper.enums import ParseMode
from fipper.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)

from ..config import Var


class InlineBot(Var):
    async def inline_pmpermit(self, ids):
        pm_results = [
            (
                InlineQueryResultArticle(
                    title='PmPermit Shicy Ubot!',
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text='• Approve •',
                                    callback_data=f'terima_{ids}',
                                ),
                                InlineKeyboardButton(
                                    text='• Disapprove •',
                                    callback_data=f'tolak_{ids}',
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    text='• Close •',
                                    callback_data=f'close',
                                ),
                            ]
                        ]
                    ),
                    input_message_content=InputTextMessageContent(self.PERMIT_MSG),
                )
            )
        ]
        
        return pm_results
    
    async def inline_music(self, video_id, users):
        play_string = """
**🎶 Lagu Ditemukan**

≽ **Judul Lagu Woy:** {video_id}....
≽ **Requested by:** {name}
≽ **User ID:** {users_id}
≽ **Powered by:** [ShicyUbot](https://github.com/sip-userbot/ShicyUbot)
"""
        thumbnail = f'https://youtu.be/{video_id[28:]}'
        music_results = [
            (
                InlineQueryResultPhoto(
                    photo_url=thumbnail,
                    title='Music Shicy Ubot!',
                    description="inline Music ShicyUbot.",
                    caption=play_string.format(video_id=video_id[9:-12], name=users.first_name, users_id=users.id),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text='• Music •',
                                    callback_data=f'music_{video_id[28:]}',
                                ),
                                InlineKeyboardButton(
                                    text='• Video •',
                                    callback_data=f'video_{video_id[28:]}',
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    text='• Close •',
                                    callback_data=f'close',
                                ),
                            ]
                        ]
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                )
            )
        ]
        
        return music_results
