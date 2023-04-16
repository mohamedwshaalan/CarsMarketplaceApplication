import mysql.connector
import re
import os
from prettytable import PrettyTable
# Register a user
# Add a new user sale for an ad
# INSERT INTO app_user VALUES (userEmail, userName, gender, birthDate);

# View existing reviews of a given ad
# SELECT review FROM sale WHERE Ad_ID = "";

# View aggregated rating of a seller / owner
# SELECT Avg(Rating) FROM sale S INNER JOIN ad A ON S.Ad_ID = A.ID INNER JOIN ad_owner AO 
#	ON AO.Phone_Number = A.Owner_Phone_Number and AO.Full_Name = A.Owner_Name WHERE AO.Phone_Number = "" AND AO.Full_Name = "";

# Show all the ads for a given car make, body type and year in a specific location / area, along with the average price the number of listings for each model
# SELECT Car_Model, Count(*) as Listings ,AVG(Price) AS AvgModelPrice FROM ad WHERE Car_Brand="MG" AND Car_Year="2021" AND 	Location="Heliopolis" AND Car_Model GROUP BY Car_Model;

# Show all the used cars in a certain location in a given price range, with a given set of features
# SELECT ad.* FROM ad INNER JOIN extra_features ON ad.ID = extra_features.Ad_ID WHERE ad.Location = 'Heliopolis' AND ad.Price >= '0' AND ad.Price <= '50000000' AND extra_features.Extra_Feature IN ('Air Conditioning') GROUP BY ad.ID HAVING COUNT(DISTINCT extra_features.Extra_Feature) = 1;

# Show the top 5 areas in cairo by amount of inventory and average price a given make / model
#  	SELECT a.Location, AVG(a.Price) AS average_price, COUNT(*) AS inventory_count FROM ad a WHERE a.Car_Brand = 'MG' AND a.Car_Model = '6' GROUP BY a.Location ORDER BY COUNT(*) DESC;

# Show the top 5 sellers by the amount of listings they have, along with their avg price per year
# 	SELECT Owner_Name, Owner_Phone_Number, Car_Year, Count(*), AVG(Price) FROM ad  GROUP BY 1, 2, 3  ORDER BY Count(*) DESC; 

# Show all the properties listed by a specific owner (given their first and last name and / or phone no) 
# SELECT * FROM ad WHERE Owner_Phone_Number='' AND Owner_Name='';

# Show the top 5 make / models cars by the amount of inventory and their average price for a given year range
# SELECT ad.Car_Brand, ad.Car_Model, COUNT(*) AS inventory_count, AVG(ad.Price) AS average_price FROM ad INNER JOIN cars ON ad.Car_Brand = cars.Car_Brand 
#        AND ad.Car_Model = cars.Car_Model 
#        AND ad.Car_Year = cars.Car_Year 
#WHERE 
#    ad.Car_Year BETWEEN start_year AND end_year
#GROUP BY 
#    ad.Car_Brand, 
#    ad.Car_Model 
#ORDER BY 
#    inventory_count DESC, 
#    average_price DESC 

def sqlResulttoPrettyTable(sqlResult):
    table = PrettyTable()
    for i in range(len(sqlResult[0])):
        table.add_column(sqlResult[0][i], [row[i] for row in sqlResult[1:]])
    return table
    
def emailCheck(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, email) and len(email) <= 350:
        return True
    else:
        return False

def usernameCheck(username):
    if(len(username) <= 100):
        return True
    else :
        return False

def sqlDateCheck(date):
    pattern = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    if re.match(pattern, date):
        return True
    else:
        return False
def isDigit(string):
    if string.isdigit():
        return True
    else:
        return False
mydb = mysql.connector.connect(
 host="db4free.net" ,
 user="mohamedshaalan",
 password="dbpassword",
 database= "olxproject"
)
mycursor = mydb.cursor()
print("Welcome to the OLX Database Project")
print("Choose one of the following options: ")
print("1) Register a new user and login")
print("2) Login")
print("3) Exit")
choice = input("Enter your choice: ")
os.system('cls')
if choice == "1":
    print("Enter username:")
    username = input()
    os.system('cls')
    while usernameCheck(username) == False:
        print("Invalid username, please enter a valid username")
        print("Enter username:")
        username = input()
        os.system('cls')
    print("Enter email:")
    email = input()
    os.system('cls')
    while emailCheck(email) == False:
        print("Invalid email, please enter a valid email")
        print("Enter email:")
        email = input()
        os.system('cls')
    sql = f"""
    SELECT Email FROM app_user WHERE Email = '{email}';
    """
    mycursor.execute(sql)
    result = mycursor.fetchall()
    while len(result) != 0:
        print("Email already exists, please enter a different email.")
        print("Enter email:")
        email = input()
        os.system('cls')
        sql = f"""
        SELECT Email FROM app_user WHERE Email = '{email}';
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
    print("Enter birth date:")
    birthdate = input()
    os.system('cls')
    while sqlDateCheck(birthdate) == False:
        print("Invalid birth date, please enter a valid birth date")
        print("Enter birth date:")
        birthdate = input()
        os.system('cls')
    print("Enter gender:")
    gender= 'X'
    gender = input()
    os.system('cls')
    while gender != 'M' and gender != 'F':
        print("Invalid gender input, please enter M or F")
        print("Enter gender:")
        gender = input()
        os.system('cls')
    sql = """
    INSERT INTO app_user VALUES ('%s', '%s', '%s', '%s');
    """ % (email,username,gender,birthdate)
    
    mycursor.execute(sql)
    mydb.commit()
    print("User registered successfully!")
    print("Login Successful!")
    currentEmail = email
elif choice == "2":
    print("Enter email:")
    email = input()
    os.system('cls')
    sql = f"""
    SELECT Email FROM app_user WHERE Email = '{email}';
    """
    mycursor.execute(sql)
    result = mycursor.fetchall()
    while len(result) == 0:
        print("Email does not exist, please enter a valid email.")
        print("Enter email:")
        email = input()
        os.system('cls')
        sql = f"""
        SELECT Email FROM app_user WHERE Email = '{email}';
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
    print("Login Successful!")
    currentEmail = email
elif choice == "3":
    print("Exiting program...")
    exit()

quit = False
while quit == False:
    print("Welcome " + currentEmail + "!")
    print("Choose one of the following options: ")
    print("1) Add a new user sale for an ad")
    print("2) View existing reviews of a given ad")
    print("3) View aggregated rating of a seller / owner")
    print("4) Show all the ads for a given car make, body type and year in a specific location / area, along with the average price the number of listings for each model")
    print("5) Show all the used cars in a certain location in a given price range, with a given set of features")
    print("6) Show the top 5 areas in cairo by amount of inventory and average price a given make / model")
    print("7) Show the top 5 sellers by the amount of listings they have, along with their avg price per year")
    print("8) Show all the cars listed by a specific owner (given their first and last name and / or phone no)")
    print("9) Show the top 5 make / models cars by the amount of inventory and their average price for a given year range")
    print("10) Exit")
    choice = input("Enter your choice: ")
    os.system('cls')
    if choice == "1":
        print("Enter ad id:")
        ad_id = input()
        os.system('cls')
        sql = f"""
        SELECT ID FROM ad WHERE ID = '{ad_id}';
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        # check if a sale already exists for this ad and if it even exists
        while len(result) == 0:
            print("Ad does not exist, please enter a valid ad id.")
            print("Enter ad id:")
            ad_id = input()
            os.system('cls')
            sql = f"""
            SELECT ID FROM ad WHERE ID = '{ad_id}';
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()
        sql = f"""
        SELECT * FROM sale WHERE Ad_ID = '{ad_id}';
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        while len(result) != 0:
            print("A sale already exists for this ad, please enter a different ad id.")
            print("Enter ad id:")
            ad_id = input()
            os.system('cls')
            sql = f"""
            SELECT ID FROM ad WHERE ID = '{ad_id}';
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()
            sql = f"""
            SELECT * FROM sale WHERE Ad_ID = '{ad_id}';
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()
        print("Enter purchase price:")
        price = input()
        os.system('cls')
        #check price is digit
        while isDigit(price) == False:
            print("Invalid price, please enter a valid price")
            print("Enter purchase price:")
            price = input()
            os.system('cls')
        print("Enter review:")
        review = input()
        os.system('cls')
        # check review less than 1000 chars
        while len(review) > 1000:
            print("Invalid review, please enter a valid review")
            print("Enter review:")
            review = input()
            os.system('cls')
        print("Enter rating:") # 1 to 5
        rating = input()
        os.system('cls')
        while isDigit(rating) == False or int(rating) < 1 or int(rating) > 5:
            print("Invalid rating, please enter a valid rating")
            print("Enter rating:")
            rating = input()
            os.system('cls')
        sql = f"""
        INSERT INTO sale VALUES ('%s', '%s', '%s', '%s', '%s');
        """ % (ad_id,review,price,rating,currentEmail)
        mycursor.execute(sql)
        mydb.commit()
        print("Sale added successfully!")
        print("Would you like to exit the program? (Y/N)")
        choice = input()
        os.system('cls')
        if choice == "Y" or choice == "y":
            quit = True 
    elif choice == "2":
        print("Enter ad id:")
        ad_id = input()
        os.system('cls')
        sql = f"""
        SELECT Ad_ID FROM sale WHERE Ad_ID = '{ad_id}';
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        # check if there exists a review for this ad
        while len(result) == 0:
            print("Ad does not have a sale, please enter a valid ad id.")
            print("Enter ad id:")
            ad_id = input()
            os.system('cls')
            sql = f"""
            SELECT ID FROM ad WHERE ID = '{ad_id}';
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()
        # show the review
        sql = f"""
        SELECT review FROM sale WHERE Ad_ID = '{ad_id}';
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        print("Review: " + result[0][0])
        print("Would you like to exit the program? (Y/N)")
        choice = input()
        os.system('cls')
        if choice == "Y" or choice == "y":
            quit = True
    elif choice == "3":
        print("Enter seller name:")
        seller_name = input()
        os.system('cls')
        print("Enter seller phone number:")
        seller_phone = input()
        os.system('cls')
        sql= f"""
        SELECT * FROM ad_owner WHERE Full_Name = '{seller_name}' AND Phone_Number = '{seller_phone}';
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        while len(result) == 0:
            print("Seller does not exist, please enter a valid seller name and phone number.")
            print("Enter seller name:")
            seller_name = input()
            os.system('cls')
            print("Enter seller phone number:")
            seller_phone = input()
            os.system('cls')
            sql= f"""
            SELECT * FROM ad_owner WHERE Full_Name = '{seller_name}' AND Phone_Number = '{seller_phone}';
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()
        sql = f"""
        	SELECT Avg(Rating) FROM sale S INNER JOIN ad A ON S.Ad_ID = A.ID INNER JOIN ad_owner AO 
	        ON AO.Phone_Number = A.Owner_Phone_Number and AO.Full_Name = A.Owner_Name WHERE AO.Phone_Number = '{seller_phone}' AND AO.Full_Name = '{seller_name}'
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        if result[0][0] == None:
            print("Seller has no sales")
        else:
            print("Aggregated Seller Rating: " + str(result[0][0]))
        print("Would you like to exit the program? (Y/N)")
        choice = input()
        os.system('cls')
        if choice == "Y" or choice == "y":
            quit = True
    elif choice == "4":
        print("Enter Car Brand:")
        car_brand = input()
        os.system('cls')
        print("Enter Car Year:")
        car_year = input()
        os.system('cls')
        print("Enter Car Location:")
        location = input()
        os.system('cls')
        # check if car exists
        sql = f"""  
        SELECT * FROM ad WHERE Car_Brand = '{car_brand}' AND Car_Year = '{car_year}' AND Location = '{location}';
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        while len(result) == 0:
            print("Request does not exist, please enter a valid car brand, year and location.")
            print("Enter Car Brand:")
            car_brand = input()
            os.system('cls')
            print("Enter Car Year:")
            car_year = input()
            os.system('cls')
            print("Enter Car Location:")
            location = input()
            os.system('cls')
            sql = f"""  
            SELECT * FROM ad WHERE Car_Brand = '{car_brand}' AND Car_Year = '{car_year}' AND Location = '{location}';
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()
        sql = f"""
        	SELECT Car_Model, Count(*) as Listings ,AVG(Price) AS AvgModelPrice FROM ad WHERE Car_Brand='{car_brand}' AND Car_Year='{car_year}' AND 
            	Location='{location}' GROUP BY Car_Model;
            """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Car Model", "Listings", "Avg Model Price"]
        for r in result:
            table.add_row(r)
        print(table)
        print("Would you like to exit the program? (Y/N)")
        choice = input()
        os.system('cls')
        if choice == "Y" or choice == "y":
            quit = True
    elif choice == "5":
        print("Enter Location:")
        location = input()
        os.system('cls')
        sql = f"""
        SELECT Location FROM ad WHERE Location = '{location}';
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        while len(result) == 0:
            print("Location does not exist, please enter a valid location.")
            print("Enter Location:")
            location = input()
            os.system('cls')
            sql = f"""
            SELECT Location FROM ad WHERE Location = '{location}';
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()
        print("Enter Minimum Price:")
        min_price = input()
        os.system('cls')
        while not min_price.isdigit():
            print("Minimum price must be a number.")
            print("Enter Minimum Price:")
            min_price = input()
            os.system('cls')
        print("Enter Maximum Price:")
        max_price = input()
        os.system('cls')
        while not max_price.isdigit():
            print("Maximum price must be a number.")
            print("Enter Maximum Price:")
            max_price = input()
            os.system('cls')
        features = []
        print("Enter Features (Enter 0 to stop):")
        feature = input()
        os.system('cls')
        while feature != "0":
            features.append(feature)
            print("Enter Features (Enter 0 to stop):")
            feature = input()
            os.system('cls')
        featurelist = ""
        for f in features:
            featurelist += "'" + f + "',"
        featurelist = featurelist[:-1]

        sql = f"""
        SELECT
            ad.ID,
            ad.Car_Brand,
            ad.Car_Model,
            ad.Car_Year,
            ad.Color,
            ad.Maximum_Kilometers,
            ad.Minimum_Kilometers,
            ad.Car_Condition,
            ad.Car_Transmission_Type,
            ad.Fuel_Type,
            ad.Location,
            ad.Price_Type,
            ad.Price
            FROM
                ad
                INNER JOIN extra_features ON ad.ID = extra_features.Ad_ID
            WHERE
                ad.Location = '{location}' AND
                ad.Price >= '{min_price}' AND ad.Price <= '{max_price}' AND
                extra_features.Extra_Feature IN ({featurelist})
            GROUP BY
                ad.ID
            HAVING
                COUNT(DISTINCT extra_features.Extra_Feature) = {len(features)};
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        if len(result) == 0:
            print("No cars found with the given parameters.")
        else:
            table = PrettyTable()
            table.field_names = ["ID", "Brand", "Model", "Year", "Color", "Min Kilos", "Max Kilos", "Condition", "Transmission", "Fuel Type", "Location", "Price Type", "Price"]
            for r in result:
                table.add_row(r)
            print(table)
        print("Would you like to exit the program? (Y/N)")  
        choice = input()
        os.system('cls')
        if choice == "Y" or choice == "y":
            quit = True
    elif choice == "6":
        print("Enter Car Brand:")
        car_brand = input()
        os.system('cls')
        print("Enter Car Model:")
        car_model = input()
        os.system('cls')
        # check if car exists
        sql = f"""
        SELECT * FROM cars WHERE Car_Brand = '{car_brand}' AND Car_Model = '{car_model}';
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        while len(result) == 0:
            print("Car does not exist, please enter a valid car brand and model.")
            print("Enter Car Brand:")
            car_brand = input()
            os.system('cls')
            print("Enter Car Model:")
            car_model = input()
            os.system('cls')
            sql = f"""
            SELECT * FROM cars WHERE Car_Brand = '{car_brand}' AND Car_Model = '{car_model}';
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()
        sql = f"""
        	SELECT a.Location, AVG(a.Price) AS average_price, COUNT(*) AS inventory_count FROM ad a
            WHERE a.Car_Brand = '{car_brand}' AND a.Car_Model = '{car_model}' GROUP BY a.Location ORDER BY  inventory_count DESC, 
            average_price DESC LIMIT 5;
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Location", "Average Price", "Inventory Count"]
        for r in result:
            table.add_row(r)
        print(table)
        print("Would you like to exit the program? (Y/N)")
        choice = input()
        os.system('cls')
        if choice == "Y" or choice == "y":
            quit = True
    elif choice == "7":
        sql = """
        	SELECT Owner_Name, Owner_Phone_Number, Car_Year, Count(*), AVG(Price)
            FROM ad 
            GROUP BY 1, 2, 3 
            ORDER BY Count(*) DESC LIMIT 5;
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Owner Name", "Owner Phone Number", "Car Year", "Count", "Average Price"]
        for r in result:
            table.add_row(r)
        print(table)
        print("Would you like to exit the program? (Y/N)")
        choice = input()
        os.system('cls')
        if choice == "Y" or choice == "y":
            quit = True
    elif choice == "8":
        print("Enter seller name:")
        seller_name = input()
        os.system('cls')
        print("Enter seller phone number:")
        seller_phone = input()
        os.system('cls')
        sql= f"""
        SELECT * FROM ad_owner WHERE Full_Name = '{seller_name}' AND Phone_Number = '{seller_phone}';
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        while len(result) == 0:
            print("Seller does not exist, please enter a valid seller name and phone number.")
            print("Enter seller name:")
            seller_name = input()
            os.system('cls')
            print("Enter seller phone number:")
            seller_phone = input()
            os.system('cls')
            sql= f"""
            SELECT * FROM ad_owner WHERE Full_Name = '{seller_name}' AND Phone_Number = '{seller_phone}';
            """
            mycursor.execute(sql)
            result = mycursor.fetchall()
        sql = f"""
            SELECT * FROM ad WHERE Owner_Phone_Number='{seller_phone}' AND Owner_Name='{seller_name}' ;
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        table = PrettyTable()
        table.field_names = ["ID", "Car Brand", "Car Model", "Car Year", "Color", "Minimum Kilometers", "Maximum Kilometers", "Car Condition", "Car Transmission Type", "Fuel Type", "Location", "Price Type", "Price"]
        for r in result:
            table.add_row(r)
        print(table)
        print("Would you like to exit the program? (Y/N)")
        choice = input()
        os.system('cls')
        if choice == "Y" or choice == "y":
            quit = True
    elif choice == "9":
        print("Enter minimum year:")
        start_year = input()
        os.system('cls')
        while not start_year.isdigit():
            print("Please enter a valid year.")
            print("Enter minimum year:")
            start_year = input()
            os.system('cls')
        print("Enter maximum year:")
        end_year = input()
        os.system('cls')
        while not end_year.isdigit():
            print("Please enter a valid year.")
            print("Enter maximum year:")
            end_year = input()
            os.system('cls')
        sql= f"""
        SELECT 
            ad.Car_Brand, 
            ad.Car_Model, 
            COUNT(*) AS inventory_count, 
            AVG(ad.Price) AS average_price
        FROM 
            ad 
        WHERE 
            ad.Car_Year BETWEEN {start_year} AND {end_year}
        GROUP BY 
            ad.Car_Brand, 
            ad.Car_Model 
        ORDER BY 
            inventory_count DESC, 
            average_price DESC 
            LIMIT 5;
        """
        mycursor.execute(sql)
        result = mycursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Car Brand", "Car Model", "Inventory Count", "Average Price"]
        for r in result:
            table.add_row(r)
        print(table)
        print("Would you like to exit the program? (Y/N)")
        choice = input()
        os.system('cls')
        if choice == "Y" or choice == "y":
            quit = True
    elif choice == "10":
        exit()


