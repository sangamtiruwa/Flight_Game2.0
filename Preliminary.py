import random
import mysql.connector
from geopy.distance import great_circle

# Connect to the database
connection = mysql.connector.connect(
    host='127.0.1.1',
    port=3306,
    database='flight_game',
    user='root',
    password='3790',
    autocommit=True
)

print("Welcome to Flight Game!\n")

# Function to get airport information
def get_airport(icao):
    sql = "SELECT iso_country, ident, name, type, latitude_deg, longitude_deg FROM airport WHERE ident = %s;"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    cursor.close()
    return result

# Define a function to calculate CO2 consumption for a mission
def calculate_co2_distance(distance_km):
    return distance_km * 100  # Assuming 100 liters of CO2 for every 10 km

# Define a function to start the game
def start_game():
    player_name = input("Enter your name: ")
    print(f"Welcome, {player_name}!")

    player_co2 = 50000  # Initialize player's CO2

    while True:
        print("\nOptions:")
        print("1. Start a mission")
        print("2. Settings")
        print("3. Information")
        print("4. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            mission_start = input("Enter the departure airport (ICAO code): ")
            mission_end = input("Enter the destination airport (ICAO code): ")

            start_airport = get_airport(mission_start)
            end_airport = get_airport(mission_end)

            if start_airport and end_airport:
                # Calculate the distance between two airports using geopy
                start_coords = (start_airport['latitude_deg'], start_airport['longitude_deg'])
                end_coords = (end_airport['latitude_deg'], end_airport['longitude_deg'])
                distance_km = great_circle(start_coords, end_coords).kilometers

                co2_consumed = calculate_co2_distance(distance_km)
                player_co2 -= co2_consumed  # Deduct CO2 for the mission
                print(f"Mission completed! CO2 consumed: {co2_consumed} liters")
                print(f"Your remaining CO2: {player_co2} liters")
                if player_co2 > 0 :
                    print("Oops, you emiited a lot of co2.")
                elif player_co2 < 0:
                    print("You won the game. Thank you for saving the environment.")


            else:
                print("Invalid airports. Try again.")

        elif choice == "2":
            show_settings()

        elif choice == "3":
            show_information()

        elif choice == "4":
            print(f"Thank you, {player_name}!")
            break

        else:
            print("Invalid choice. Please select a valid option.")

# Define a function to show game information
def show_information():
    while True:
        print("\nGame Information:")
        print("1. Game Rules")
        print("2. Game Story")
        print("3. Credits")
        print("4. Back to Main Menu")

        info_choice = input("Enter your information choice: ")

        if info_choice == "1":
            print("\nGame Rules:")
            print("-- Your goal is to complete missions and reduce your CO2 consumption.")
            print("-- CO2 consumption is calculated based on the distance of your missions.")
            print("-- The less CO2 you consume, the better you're doing for the environment.")
        elif info_choice == "2":
            print("\nGame Story:")
            print("You are an eco-conscious pilot who takes on missions to help protect the environment.")
            print("Travel to different airports, complete tasks, and reduce your carbon footprint.")
        elif info_choice == "3":
            print("\nCredits:")
            print("Developed by: Bikesh, Subash, Sangam, Abhi")
            print("Game Design: NepTech Project")
            print("Graphics: NepTech Project")
        elif info_choice == "4":
            return  # Back to Main Menu
        else:
            print("Invalid choice. Please select a valid option.")

# Define a function to show settings
def show_settings():
    print("\nSettings Menu:")
    print("1. Sound Settings")
    print("2. Display Settings")
    print("3. Back to Main Menu")

    settings_choice = input("Enter your settings choice: ")

    if settings_choice == "1":
        print("\nSound Settings:")
        print("Volume: 80%")
    elif settings_choice == "2":
        print("\nDisplay Settings:")
        print("Resolution: 1920x1080")
    elif settings_choice == "3":
        return  # Back to Main Menu
    else:
        print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    print("Welcome to the Flight Game!")
    start_game()