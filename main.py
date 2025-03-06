from restaurantTables import restaurant_tables2

'''
A Restaruant Class holding an instance variable that contains a specified table layout, and a dictionary of the Table ID
and Table Capacities seperated:

Specified table layout:  Defined outside of the class, it contains timeslots which are used to identify availability 
                         under each table
Table Information:    Seperates the Table ID and Table Capacity into a dictionary

Contains five functions: 
    1. A function which seperates the table Id and capacity value sfrom the header
    2. A function which lists all current free tables in a given timeslot
    3. A function which recieves a given party count and timeslot, returning a single table that is free
    4. A function which recieves a givern party count and timeslot, returning all tables that are free
    5. A function which recieves a given party count and timeslot, identifying all possible table pairs which can be combined 
       to fit the party count

 
'''

class Restaurant:
    # Initializes instance variables: Table layout and Table Information
    def __init__(self, tables):
        self.tables = tables # Locks the value in place preventing accidental change; Allows for its use anywhere in Class
        self.table_information = self.table_info() 

    # Seperates the Table ID and Table Capacity into a dictionary
    #  - This will allow for easier data access and manipulation
    def table_info(self):

        table_information = {} 
        
        # Iterate through every value in the first row (skipping the first timeslot indicator)
        # Track the index and value associated with the index 
        for i, table in enumerate(self.tables[0][1:]):  

            # Split current table value by "(" 
            # - Creates list we can work with to assign seperate Table ID and Table Capacity values to dictionary
            table_values = table.split("(")
            table_ID = table_values[0]
            table_Capacity = int(table_values[1][:-1]) # Removes extra parenthesis and converts to int

            # Uses column index (i) as key to store information in the dictionary
            table_information[i] = {"ID": table_ID, "Capacity":  table_Capacity}

        return table_information # Returns complete dictionary of Table ID's and Capacities
    


    '''
    Level 1:
    Lists all current free table in a given timeslot

    Parameters:
    timeslot - An indicater to which row is going to be checked for availability

    Returns all free tables IDs 
    '''
    def all_free_tables(self, timeslot):

        free_tables = [] # Tables that are available

        # Iterate through given row (timeslot); Ignore the timeslot value itslef
        # Keep track of column index and its value 
        for i, table in enumerate(self.tables[timeslot][1:]):

            # If the current table status is available, append it to the free tables tracker
            if table == 'o':
                free_tables.append(self.table_information[i]["ID"])
            
        # If no free tables found, return "Sorry" message
        if free_tables == []:
            return "Sorry, no tables could be found at this time."
        
        # Otherwise return all free tables
        else:
            return f'Tables available: {", ".join(free_tables)}' # Joins the array into a list



    '''
    Level 2:
    Find a single available table given party count and timeslot. 
    Capacity must be >= to the party count AND it must be free

    Parameters:
    timeslot - An indicater to which row is checked for availability
    capacity - The minimum amount of people a table must fit

    Returns a single table ID that fits the required amount of people
    '''
    def table_for_party(self, timeslot, capacity):

        # Iterates through given row (timeslot), ignores timeslot value
        # Keeps track of column index and the value assigned to the index
        for i, table in enumerate(self.tables[timeslot][1:]):

            # If table is available and if table >= party count 
            # Return table ID 
            if table == 'o':
                if self.table_information[i]["Capacity"] >= capacity:
                    return f'Your table for {capacity} is: {self.table_information[i]["ID"]}'
                
        #If not table is found, return after the loop
        return "Sorry, no tables could be found at this time."




    '''
    Level 3:
    Find all available tables given a party count and timeslot

    Parameters:
    timeslot - An indicator to which row is checked for availability
    capacity - The minimum amount of people a table must fit

    Return ALL table ID's found which match the criteria 
    '''
    def all_single_tables_for_party(self, timeslot, capacity):

        free_tables = [] # All available tables which meet the criteria

        # Iterate through the given row (timeslot), ignore the timeslot value itself
        # Keep track of colum index and the value assigned to it
        for i, table in enumerate(self.tables[timeslot][1:]):

            # If table is available and if table >= party count 
            # Append the table ID to the free table tracker
            if table == 'o':
                if self.table_information[i]["Capacity"] >= capacity:
                    free_tables.append(self.table_information[i]["ID"])
        
        # If no free tables found, return "Sorry" message
        if free_tables == []:
            return "Sorry, no tables could be found at this time."
        
        # Otherwise return all free tables
        else:
            return f'Tables available for party of {capacity}: {", ".join(free_tables)}'




    '''
    Level 4:
    Find all free tables for a given party count and timeslot. If a table is available but does not fit the
    required party count, check to see if the table adjacent to it is free and could be combined to fit the 
    party.

    Parameters:
    timeslot - An indicator to which row is checked for availability
    capacity - The minimum amount of people a table must fit

    Return ALL available tables, and table combinations, that would fit the party
    '''
    def all_tables_for_party(self, timeslot, capacity):

        free_tables = []

        # Iterate through the given row (timeslot), ignore the timeslot value itself
        # Keep track of colum index and the value assigned to it
        for i, table in enumerate(self.tables[timeslot][1:]):

            # Check table availability at given index
            if table == 'o':

                # If table capacity >= party count: Add it to the free tables tracker
                if self.table_information[i]["Capacity"] >= capacity:
                    free_tables.append(self.table_information[i]["ID"])

                # Else if table capacity < party count: 
                #   Check the availability of the table adjacent to it 
                #   Check if sum of both capacities >= party count
                #   If true add the combined ID's to the free tables tracker
                elif (
                    i + 1 < len(self.tables[timeslot]) - 1 # While debugging I ran into an IndexError, this prevents the error
                    and self.tables[timeslot][i+2] == 'o' 
                    and self.table_information[i]["Capacity"] + self.table_information[i+1]["Capacity"] >= capacity
                ):
                    free_tables.append(f'{self.table_information[i]["ID"]} with {self.table_information[i+1]["ID"]}')

        # If no tables available, print "Sorry" message
        if free_tables == []:
            return "Sorry, no tables could be found at this time."
        
        # Otherwise return free_tables 
        else:
            return f'Tables available for party of {capacity}: {", ".join(free_tables)}'
                

'''
Creates a check-in, chatbox-like, experience for the user. Allowing them to choose what function 
they would like to preform.

Parameters:
restauraunt - Indicates the table layout

Returns the answer to whichever option the user chooses
'''
def check_in(restaurant):

    # Loops the program until the user specifies they wish to exit
    while True:

        # Provides the user with a set of actions
        print("\nWelcome to the restaurant! What action would you like to perform?")
        print("1: List free tables")
        print("2: Find one available table")
        print("3: Find all available tables")
        print("4: Find adjacent tables")
        print("5: Exit")

        # Recieves a user input for what they would like to do
        # Error would occur if input was not an int, try-except would fix this
        try:    
            choice = int(input("Enter: "))
        except ValueError:
            print("Invalid input, please try again.")
            continue
        
        # Stops execution of program
        if choice == 5:
            print("Goodbye!")
            break  
        
        # Prompts the user to input a timeslot for their table and their party count
        # try-except necessary for invalid input
        try:
            timeslot = int(input("\n\n1   2   3   4   5   6\nChoose a timeslot: "))
            party_count = int(input("Enter the amount of people in group: "))
        except ValueError:
            print("Invalid input, please try again.")
            continue

        # Calls the functions corresponding to what the user chose to do
        if choice == 1:
            print(restaurant.all_free_tables(timeslot))

        elif choice == 2:
            table = restaurant.table_for_party(timeslot, party_count)
            print(table)

        elif choice == 3:
            tables = restaurant.all_single_tables_for_party(timeslot, party_count)
            print(tables )

        elif choice == 4:
            tables = restaurant.all_tables_for_party(timeslot, party_count)
            print(tables)

        else:
            print("Choice not found, please try again.")

# Initializes the restaraunt
restaurant = Restaurant(restaurant_tables2)
check_in(restaurant)


