# aiopagination
### About
`aiopagination` is a library written using the aiogram library to help you create pagination using inline buttons

**Info:** A sample to use
```python
from aiogram import executor
from aiogram import types

from aiopagination.test.data.loader import dp
from aiopagination.widgets.aiokeyboards import base_cd, pagination_cd

from aiopagination.widgets.aiopagination import Pagination




sample_list = [
    (1, "Apple", 'red'),
    (2, "Cucumber", "green"),
    (3, "Melon", "yellow"),
    (4, "Cherry", "red"),
    (5, "Watermelon", "green"),
    (6, "Banana", "yellow"),
    (7, "Carrot", "orange"),
    (8, "Kiwi", "green"),
    (9, "Malina", "red"),
    (10, "Apelsin", "yellow"),
    (11, "Lemon", "yellow"),
    (12, "Grape", "black"),
    (13, "Carrot", "red"),
    (14, "Potato", "yellow"),
    (15, "Potato", "yellow"),
    (16, "Banana", "yellow"),
    (17, "Carrot", "orange"),
    (18, "Kiwi", "green"),
    (19, "Malina", "red"),
    (20, "Apelsin", "yellow"),
    (21, "Lemon", "yellow"),
    (22, "Grape", "black"),
    (23, "Carrot", "red"),
    (24, "Potato", "yellow")
]







# start
@dp.message_handler(commands=["start"])
async def bot_start(message: types.Message):
    pagination = Pagination(sample_list)
    await pagination.start_message(message=message)




# select item and send to user
@dp.callback_query_handler(base_cd.filter())
async def get_item_id(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    item_id = callback_data.get("item_id")
    pag = Pagination(sample_list)
    get_data = await pag.select_item(item_id=int(item_id))

    await call.message.answer(get_data[1], parse_mode="HTML")





# pagination keyboards
@dp.callback_query_handler(pagination_cd.filter())
async def show_pagination(call: types.CallbackQuery, callback_data: dict):
    start = int(callback_data.get("start"))
    end = int(callback_data.get("end"))
    max_pages = int(callback_data.get("max_pages"))
    action = callback_data.get("action")

    pagination = Pagination(items=sample_list)
    if action == "prev":
        await pagination.prev(call=call, start=start, end=end, max_pages=max_pages)
    elif action == "next":
        await pagination.next(call=call, start=start, end=end, max_pages=max_pages)
    else:
        await call.answer(cache_time=1)
        await call.message.edit_reply_markup()
        await call.message.edit_text("Menga matn yuboring")





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
```