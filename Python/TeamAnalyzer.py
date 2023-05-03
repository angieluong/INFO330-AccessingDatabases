import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# Connect to the SQLite database
conn = sqlite3.connect('../pokemon.sqlite')

# Create a cursor object
c = conn.cursor()

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:    
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    else:
        strong_against =[]
        weak_against = []
        print("Analyzing", i)
        c.execute("SELECT * FROM pokemon WHERE pokedex_number = ?", (arg,))
        pokemon_info = c.fetchone()
        # Finds and sets the pokemon id value
        pokemon_name = pokemon_info[2]

        # Finds and sets the types for the given pokemon
        c.execute("SELECT * FROM pokemon_types_view WHERE name = ?", (pokemon_name,))
        pokemon_type_info = c.fetchone()

        type_1 = pokemon_type_info[1]
        type_2 = pokemon_type_info[2]

        # Finds and sets a tuple consisting of the table values of the matching types
        c.execute("SELECT * FROM pokemon_types_battle_view WHERE type1name = ? AND type2name = ?", (type_1, type_2))
        pokemon_against_values = c.fetchone()

        # Loops through all against_x columns and determines whether a given pokemon is strong or weak
        # Appends x of the against_x column name to their respective list (strong_against or weak_against)
        for i in range(2, len(pokemon_against_values)):
            if pokemon_against_values[i] < 1:
                strong_against.append(c.description[i][0].split("_")[1])
            elif pokemon_against_values[i] > 1:
                weak_against.append(c.description[i][0].split("_")[1])

            
        print(pokemon_name, "(" + type_1, type_2 + ") is strong against", strong_against, "but weak against", weak_against)

        
    # Analyze the pokemon whose pokedex_number is in "arg"

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")