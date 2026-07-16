import sqlite3

DB = "ridex.db"


def connect():
    return sqlite3.connect(DB)



def add_captain(name, phone, car, plate, password):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO captains
    (name, phone, car, plate, password)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        name,
        phone,
        car,
        plate,
        password
    ))

    conn.commit()
    conn.close()



def get_captain(phone):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM captains WHERE phone=?",
        (phone,)
    )

    row = cur.fetchone()

    conn.close()

    return row



def add_passenger(name, phone, password):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO passengers
    (name, phone, password)
    VALUES (?, ?, ?)
    """,
    (
        name,
        phone,
        password
    ))

    conn.commit()
    conn.close()



def get_passenger(phone):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM passengers WHERE phone=?",
        (phone,)
    )

    row = cur.fetchone()

    conn.close()

    return row

def add_ride(passenger_phone, from_location, to_location):

    conn = connect()

    cur = conn.cursor()

    cur.execute("""
    INSERT INTO rides
    (passenger_phone, from_location, to_location, status)
    VALUES (?, ?, ?, ?)
    """,
    (
        passenger_phone,
        from_location,
        to_location,
        "waiting"
    ))

    conn.commit()

    conn.close()

def get_waiting_rides():

    conn = connect()

    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM rides
    WHERE status='waiting'
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def accept_ride(ride_id, captain_phone):

    conn = connect()

    cur = conn.cursor()

    cur.execute("""
    UPDATE rides
    SET status='accepted',
        captain_phone=?
    WHERE id=?
    """,
    (
        captain_phone,
        ride_id
    ))

    conn.commit()

    conn.close()

def update_ride_status(ride_id, status):

    conn = connect()

    cur = conn.cursor()

    cur.execute("""
    UPDATE rides
    SET status=?
    WHERE id=?
    """,
    (
        status,
        ride_id
    ))

    conn.commit()

    conn.close()


def finish_ride_payment(ride_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT price, captain_phone
    FROM rides
    WHERE id=?
    """,(ride_id,))

    ride = cur.fetchone()

    if not ride:
        conn.close()
        return

    price = ride[0]
    captain_phone = ride[1]

    commission = price * 0.10

    cur.execute("""
    UPDATE rides
    SET commission=?
    WHERE id=?
    """,(commission, ride_id))


    cur.execute("""
    UPDATE captains
    SET wallet = wallet - ?
    WHERE phone=?
    """,(commission, captain_phone))


    conn.commit()
    conn.close()



def save_start_location(ride_id, lat, lng):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE rides
    SET start_lat=?,
        start_lng=?,
        started_at=CURRENT_TIMESTAMP
    WHERE id=?
    """,
    (lat,lng,ride_id))

    conn.commit()
    conn.close()



def save_end_location(ride_id, lat, lng):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE rides
    SET end_lat=?,
        end_lng=?,
        finished_at=CURRENT_TIMESTAMP
    WHERE id=?
    """,
    (lat,lng,ride_id))

    conn.commit()
    conn.close()

