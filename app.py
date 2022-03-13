import streamlit as st
import datetime
import requests
import json
import pandas as pd
import time


page = st.sidebar.selectbox('chose your page', ['users', 'checkin', 'checkout'])

if page == 'users':
    st.title('ユーザー登録画面')
    with st.form(key='user'):
        username: str = st.text_input('ユーザー名', max_chars=12)
        data = {
            'username': username
        }
        submit_button = st.form_submit_button(label='ユーザー登録')

    if submit_button:
        url = 'http://127.0.0.1:8000/users'
        res = requests.post(
            url,
            data=json.dumps(data)
        )
        if res.status_code == 200:
            st.success("ユーザー登録完了")
        st.json(res.json())


elif page == 'checkin':
    st.title('checkin画面')

    #ユーザー一覧取得
    url_users = 'http://127.0.0.1:8000/users'
    res = requests.get(url_users)
    users = res.json()

    #ユーザー名をキー、IDをバリュー
    users_name = {}
    for user in users:
        users_name[user['username']] = user['user_id']

    with st.form(key='checkin'):
        url_check = 'http://127.0.0.1:8000/checkin'
        url_users_delete = 'http://127.0.0.1:8000/users_delete'
        username: str = st.selectbox('名前', list(users_name.keys()))
        submit_button_users_delete = st.form_submit_button(label='ユーザー削除')
        submit_button_checkin = st.form_submit_button(label='checkin実行')
        submit_button_checkout = st.form_submit_button(label='checkout実行')


# users delete
    if submit_button_users_delete:
        data_users_delete = {'username': username}
        res = requests.post(
            url_users_delete,
            data=json.dumps(data_users_delete)
        )
        if res.status_code == 200:
            st.success(f"{username}の削除完了しました")
        st.json(res.json())

# checkin
    if submit_button_checkin:
        data_checkin = {'user_id': users_name[username],'status': 'checkin'}
        res = requests.post(
            url_check,
            data=json.dumps(data_checkin)
        )
        if res.status_code == 200:
            st.success(f"{username}のcheckin完了しました")
        #st.json(res.json())

        url_check_query = 'http://127.0.0.1:8000/checkin/'
        res = requests.get(f"{url_check_query}?user_id={users_name[username]}")
        records = res.json()
        df_records = pd.DataFrame(records)
        st.table(df_records)
# checkout
    if submit_button_checkout:
        data_checkout = {'user_id': users_name[username],'status': 'checkout'}
        res = requests.post(
            url_check,
            data=json.dumps(data_checkout)
        )
        if res.status_code == 200:
            st.success(f"{username}のcheckout完了しました。")
        #st.json(res.json())

        url_check_query = 'http://127.0.0.1:8000/checkin/'
        res = requests.get(f"{url_check_query}?user_id={users_name[username]}")
        records = res.json()
        df_records = pd.DataFrame(records)
        st.table(df_records)


elif page == 'bookings':
    st.title('会議室予約画面')


    #ユーザー一覧取得
    url_users = 'http://127.0.0.1:8000/users'
    res = requests.get(url_users)
    users = res.json()


    #ユーザー名をキー、IDをバリュー
    users_name = {}
    for user in users:
        users_name[user['username']] = user['user_id']

    #会議室一覧取得
    url_rooms = 'http://127.0.0.1:8000/rooms'
    res = requests.get(url_rooms)
    rooms = res.json()
    rooms_name = {}
    for room in rooms:
        rooms_name[room['room_name']] = {
            'room_id': room['room_id'],
            'capacity': room['capacity']
        }

    st.write('### 会議室一覧')
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ['会議室名', '定員', '会議室ID']
    st.table(df_rooms)

    url_bookings = 'http://127.0.0.1:8000/bookings'
    res = requests.get(url_bookings)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)

    users_id = {}
    for user in users:
        users_id[user['user_id']] = user['username']

    rooms_id = {}
    for room in rooms:
        rooms_id[room['room_id']] = {
            'room_name': room['room_name'],
            'capacity': room['capacity'],
        }

    # IDを各値に変更
    to_username = lambda x: users_id[x]
    to_room_name = lambda x: rooms_id[x]['room_name']
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime('%Y/%m/%d %H:%M')
    #特定の列に適用
    df_bookings['user_id'] = df_bookings['user_id'].map(to_username)
    df_bookings['room_id'] = df_bookings['room_id'].map(to_room_name)
    df_bookings['start_datetime'] = df_bookings['start_datetime'].map(to_datetime)
    df_bookings['end_datetime'] = df_bookings['end_datetime'].map(to_datetime)

    df_bookings = df_bookings.rename(columns={
        'user_id': '予約者名',
        'room_id': '会議室名',
        'booked_num': '予約人数',
        'start_datetime': '開始時間',
        'end_datetime': '終了時間',
        'booking_id': '予約番号'
    })

    st.write('###　予約一覧')
    st.table(df_bookings)

    with st.form(key='booking'):
        #booking_id: int = random.randint(0, 10)
        username: str = st.selectbox('予約者名', list(users_name.keys()))
        room_name: str = st.selectbox('会議室名', list(rooms_name.keys()))
        booked_num: int = st.number_input('予約人数', step=1, min_value=1)
        date = st.date_input('日付を入力', min_value=datetime.date.today())
        start_time = st.time_input('開始時刻: ', value=datetime.time(hour=9, minute=0))
        end_time = st.time_input('終了時刻: ', value=datetime.time(hour=20, minute=0))
        submit_button = st.form_submit_button(label='予約登録')

    if submit_button:
        user_id: int = users_name[username]
        room_id: int = rooms_name[room_name]['room_id']
        capacity: int = rooms_name[room_name]['capacity']

        data = {
            'user_id': user_id,
            'room_id': room_id,
            'booked_num': booked_num,
            'start_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute
            ).isoformat(),

            'end_datetime': datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute
            ).isoformat()
        }

        #定員以下の予約場合

        if booked_num <= capacity:
            url = 'http://127.0.0.1:8000/bookings'
            res = requests.post(
                url,
                data=json.dumps(data)
            )
            if res.status_code == 200:
                st.success('予約完了しました')
            st.json(res.json())

        else:
            st.error(f'{room_name}の定員は{capacity}名です')



