import random
from datetime import datetime, timedelta

import random
from datetime import datetime, timedelta

def generate_random_timestamps(start_date, end_date, num_timestamps):
    timestamps = []
    days_to_generate = set()

    start_gym = datetime(2023, 1, 1)
    end_gym = datetime(2025, 1, 12)

    # Define time slots weight for between 16:00 and 21:00
    popular_hours = list(range(16, 22)) 
    off_peak_hours = list(range(9, 16)) + list(range(22, 24)) 

    while len(timestamps) < num_timestamps:
        # Randomly decide a day to add attendance within the date range
        random_day_offset = random.randint(0, (end_gym - start_gym).days) 
        random_day = start_gym + timedelta(days=random_day_offset)
        random_date_str = random_day.strftime("%Y-%m-%d")

        if random_date_str not in days_to_generate and start_date <= random_date_str <= end_date:
            days_to_generate.add(random_date_str)

            # Randomly decide if the user will have one or two attendances on this day
            num_attendances = random.randint(1, 2)

            for _ in range(num_attendances):
                # Random time between 9:00 AM and 11:00 PM, with more weight on 16:00 to 21:00
                if random.random() < 0.8:  # 70% chance for the popular time slots (16:00-21:00)
                    random_hour = random.choice(popular_hours)
                else:
                    random_hour = random.choice(off_peak_hours)

                random_minute = random.randint(0, 59)
                attendance_time = random_day.replace(hour=random_hour, minute=random_minute, second=0)
                timestamps.append(attendance_time.strftime("%Y-%m-%d %H:%M:%S"))

    return timestamps


# Example user data with some presences from 2023 to 2025
user_data = {
    "1a143bce": {
        "firstName": "Stefania",
        "lastName": "Dumitru",
        "paidMembership": True,
        "attendances":  generate_random_timestamps("2024-01-01", "2025-01-12", 217)
    },
    "331ec827": {
        "firstName": "Donald",
        "lastName": "Trump",
        "paidMembership": False,
        "attendances": generate_random_timestamps("2024-10-01","2024-10-31", 5)
    },
    "eae482ce": {
        "firstName": "Charlie",
        "lastName": "Brown",
        "paidMembership": True,
        "attendances": generate_random_timestamps("2024-03-07", "2024-08-01", 100)
    },
    "f7g8h9i0": {
        "firstName": "Alice",
        "lastName": "Wonderland",
        "paidMembership": True,
        "attendances": generate_random_timestamps("2024-02-01", "2025-01-12", 215)
    },
    "5d6e7f8a": {
        "firstName": "Bob",
        "lastName": "Marley",
        "paidMembership": True,
        "attendances": generate_random_timestamps("2024-03-15", "2024-07-01", 50)
    },
    "9h0j1k2l": {
        "firstName": "Clara",
        "lastName": "Oswald",
        "paidMembership": True,
        "attendances": generate_random_timestamps("2024-04-10", "2024-08-01", 89)
    },
    "3m4n5o6p": {
        "firstName": "David",
        "lastName": "Tennant",
        "paidMembership": False,
        "attendances": generate_random_timestamps("2024-05-01", "2024-05-31", 0) 
    },
    "7q8r9s0t": {
        "firstName": "Eleanor",
        "lastName": "Rigby",
        "paidMembership": True,
        "attendances": generate_random_timestamps("2024-01-01", "2025-01-12", 250)
    },
    "1u2v3w4x": {
        "firstName": "Frank",
        "lastName": "Sinatra",
        "paidMembership": True,
        "attendances": generate_random_timestamps("2024-07-03", "2024-08-31", 17)
    },
    "5y6z7a8b": {
        "firstName": "Grace",
        "lastName": "Hopper",
        "paidMembership": True,
        "attendances": generate_random_timestamps("2024-08-15", "2024-12-01", 71)
    },
    "0c1d2e3f": {
        "firstName": "Henry",
        "lastName": "Ford",
        "paidMembership": False,
        "attendances": generate_random_timestamps("2023-09-01", "2023-09-31", 0) 
    },
    "4g5h6i7j": {
        "firstName": "Irene",
        "lastName": "Adler",
        "paidMembership": True,
        "attendances": generate_random_timestamps("2024-10-10", "2025-01-12", 50)
    },
    "8k9l0m1n": {
        "firstName": "Jack",
        "lastName": "Sparrow",
        "paidMembership": True,
        "attendances": generate_random_timestamps("2024-02-01", "2024-12-01", 167)
    },
    "2o3p4q5r": {
        "firstName": "Karen",
        "lastName": "Gillan",
        "paidMembership": True,
        "attendances": generate_random_timestamps("2024-01-01", "2025-01-12", 170)
    },
    "6s7t8u9v": {
        "firstName": "Luna",
        "lastName": "Lovegood",
        "paidMembership": True,
        "attendances": generate_random_timestamps("2024-01-15", "2024-03-01", 40)
    }
}