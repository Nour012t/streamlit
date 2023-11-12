import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from datetime import date, timedelta

df = pd.read_csv("users.csv")
data = pd.read_csv('bundles.csv')

def create_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="demo"
    )
    return conn



df["registration_date"] = pd.to_datetime(df["registration_date"])
df["subscription_date"] = pd.to_datetime(df["subscription_date"])

def get_registered_users_by_period(period):
    return df.groupby(pd.Grouper(key="registration_date", freq=period)).size()

def get_subscribed_users_by_period(period):
    return df[df["subscribed"] == 1].groupby(pd.Grouper(key="subscription_date", freq=period)).size()

def main1():
    st.title("User Registration ,Subscription and Bundle Subscriptions Dashboard")

    # Sidebar options
    period = st.selectbox("Select Period", ["D", "W", "M", "Y"])

    # Data for registered users
    registered_data = get_registered_users_by_period(period)

    # Data for subscribed users
    subscribed_data = get_subscribed_users_by_period(period)
    
    
    # Plotting the data
    fig, ax = plt.subplots()
    ax.plot(registered_data.index, registered_data.values, label="Registered Users")
    ax.plot(subscribed_data.index, subscribed_data.values, label="Subscribed Users")

    ax.legend()

    # Setting x-axis label based on the selected period
    if period == "D":
        ax.set_xlabel("Day")
    elif period == "W":
        ax.set_xlabel("Week")
    elif period == "M":
        ax.set_xlabel("Month")
    elif period == "Y":
        ax.set_xlabel("Year")

    # Setting y-axis label
    ax.set_ylabel("Number of Users")

    # Display the plot
    st.pyplot(fig)



data['creation_date'] = pd.to_datetime(data['creation_date'])
def get_created_users_by_period(period):
    return data.groupby(pd.Grouper(key="creation_date", freq=period)).size()
def main2():

    # Sidebar options
    period = st.selectbox("Select Period", ["d", "w", "m", "y"])
     # Data for created users
    created_data = get_created_users_by_period(period)
    fig, ax = plt.subplots()

    ax.plot(created_data.index, created_data.values, label="created Users")
    ax.legend()
    if period == "Day":
        ax.set_xlabel("Day")
    elif period == "Week":
        ax.set_xlabel("Week")
    elif period == "Month":
        ax.set_xlabel("Month")
    elif period == "Year":
        ax.set_xlabel("Year")

    # Setting y-axis label
    ax.set_ylabel("Number of Users")

    # Display the plot
    st.pyplot(fig)
    


# Function to establish a database connection


# Function to fetch all users and their completed courses
def fetch_users_and_completed_courses():
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT
        users.user_id,
        COUNT(user_completed_courses.course_id) AS num_completed_courses,
        MAX(user_completed_courses.completion_date) AS last_completion_date,
        MAX(user_completed_courses.course_degree) AS last_completion_degree
    FROM users
    LEFT JOIN user_completed_courses ON users.user_id = user_completed_courses.user_id
    GROUP BY users.user_id
    """
    
    cursor.execute(query)
    users_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return users_data

# Streamlit app
def main3():
    st.title("10k AI Initiative Dashboard")

    # Fetch user data
    users_data = fetch_users_and_completed_courses()


    if users_data:
     user_ids = [user['user_id'] for user in users_data]
    num_completed_courses = [user['num_completed_courses'] for user in users_data]

    # Create a Matplotlib plot
    plt.figure(figsize=(10, 8))
    plt.bar(user_ids, num_completed_courses)
    plt.xlabel("User ID")
    plt.ylabel("Completed Courses")
    plt.title("Completed Courses by User")

    # Display the Matplotlib plot in Streamlit
    st.pyplot(plt.gcf())
    st.set_option('deprecation.showPyplotGlobalUse', False) 
    st.subheader("Users and Their Completed Courses")

    df = pd.DataFrame(users_data)

        
    st.dataframe(df)




        





# Function to fetch user data
def fetch_user_data():
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        users.user_id,
        COUNT(DISTINCT user_courses.course_id) AS num_learning_courses,
        SUM(CASE WHEN user_completed_courses.completion_date >= %s THEN 1 ELSE 0 END) AS num_completed_courses_week,
        SUM(CASE WHEN user_completed_courses.completion_date >= %s THEN 1 ELSE 0 END) AS num_completed_courses_month,
        SUM(CASE WHEN user_completed_courses.completion_date >= %s THEN 1 ELSE 0 END) AS num_completed_courses_year
    FROM users
    LEFT JOIN user_courses ON users.user_id = user_courses.user_id
    LEFT JOIN user_completed_courses ON users.user_id = user_completed_courses.user_id
    GROUP BY users.user_id
    """
    
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    year_start = today.replace(day=1, month=1)
    
    cursor.execute(query, (week_start, month_start, year_start))
    user_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return user_data

# Streamlit app
def main4():
    st.title("User Courses Dashboard")

    # Fetch user data
    user_data = fetch_user_data()

    if user_data:
        st.subheader("User Course Data")

        # Convert the data to a DataFrame
        df = pd.DataFrame(user_data)

        
        st.dataframe(df)

    else:
        st.write("No user data available.")
    





db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="demo"
)

def get_user_info(user_id):
    query = "SELECT level,age,gender,study_degree FROM users WHERE user_id = %s"
    result = execute_query(query, (user_id,))
    return result


# Add other helper functions for retrieving data

def execute_query(query, params=None):
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    

    return result

def main5():
    st.title("User Dashboard")
    user_id = st.text_input("Enter User ID...")
    if st.button("Search"):
        st.subheader("User info")

        # Convert the data to a DataFrame
        df = pd.DataFrame(get_user_info(user_id))
        
        st.dataframe(df)


# Function to fetch the count of capstones evaluated for today, this week, and this month for each admin
def fetch_capstone_evaluation_history(time_frame):
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if time_frame == "Today":
        query = """
        SELECT admin_id, COUNT(*) as num_evaluations
        FROM capstone_evaluation_history
        WHERE DATE(evaluation_date) = CURDATE()
        GROUP BY admin_id
        """
    elif time_frame == "This Week":
        query = """
        SELECT admin_id, COUNT(*) as num_evaluations
        FROM capstone_evaluation_history
        WHERE YEARWEEK(evaluation_date) = YEARWEEK(NOW())
        GROUP BY admin_id
        """
    elif time_frame == "This Month":
        query = """
        SELECT admin_id, COUNT(*) as num_evaluations
        FROM capstone_evaluation_history
        WHERE MONTH(evaluation_date) = MONTH(NOW()) AND YEAR(evaluation_date) = YEAR(NOW())
        GROUP BY admin_id
        """
    
    cursor.execute(query)
    evaluations_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return evaluations_data

# Streamlit app
def main6():
    st.title("Admin Capstone Evaluations Dashboard")

    # Choose a time frame
    time_frame = st.selectbox("Select Time Frame", ["Today", "This Week", "This Month"])

    if time_frame:
        evaluations_data = fetch_capstone_evaluation_history(time_frame)

        if evaluations_data:
            st.subheader(f"Capstone Evaluations for {time_frame}")

            # Create a table data list
            table_data = []
            for evaluation in evaluations_data:
                table_data.append({
                    "Admins": evaluation['admin_id'],
                    "Number of Evaluations": evaluation['num_evaluations']
                })

            # Display the table
            st.table(table_data)

        else:
            st.write("No capstone evaluations found for the selected time frame.")


  

# Function to fetch each user's capstone and its evaluation history
def fetch_user_capstones(user_id):
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT
        capstones.lesson_id,
        capstone_evaluation_history.eval_history_id,
        capstone_evaluation_history.evaluation_date,
        capstone_evaluation_history.degree
    FROM capstones
    LEFT JOIN capstone_evaluation_history ON capstones.lesson_id = capstone_evaluation_history.lesson_id
    WHERE capstones.user_id = %s
    """
    
    cursor.execute(query, (user_id,))
    capstones_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return capstones_data

# Streamlit app
def main7():
    st.title("User Capstones and Evaluation History Dashboard")

    # Input user ID
    user_id = st.text_input("Enter User ID")

    if user_id:
        st.subheader("User's Capstones and Evaluation History")

        # Fetch and display user's capstones and evaluation history
        capstones = fetch_user_capstones(user_id)
        if capstones:
            for capstone_data in capstones:
                st.write(f"**Evaluation History ID:** {capstone_data['eval_history_id']}")
                st.write(f"**Evaluation Date:** {capstone_data['evaluation_date']}")
                st.write(f"**degree:** {capstone_data['degree']}")
                st.write("------")
                

                break        
        else:
            st.write("No capstone data found for this user.")





   

# Function to fetch all coupons and the number of actual users who used them
def fetch_coupons_and_users_count():
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT
        copons.coupon_id,
        copons.copon_code,
        copons.users
    FROM copons
    LEFT JOIN users ON copons.coupon_id = copons.coupon_id
    GROUP BY copons.coupon_id, copons.copon_code
    """
    
    cursor.execute(query)
    coupons_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return coupons_data

# Streamlit app
def main8():
    st.title("Coupons and Users Usage Dashboard")

    # Fetch and display all coupons and the number of users who used them
    coupons_data = fetch_coupons_and_users_count()

    if coupons_data:
        st.subheader("Coupons and Users Usage")
        

        # Convert the data to a DataFrame
        df = pd.DataFrame(coupons_data)

        
        st.dataframe(df)
    else:
        st.write("No coupon data available.")





# Function to fetch the number of users grouped by age and study degree
def fetch_users_by_age_and_degree():
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT
        users.age,
        users.study_degree,
        COUNT(users.user_id) AS user_count
    FROM users
    GROUP BY users.age, users.study_degree
    """
    
    cursor.execute(query)
    user_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return user_data
def create_bar_plot(user_data):
    age_degrees = [(f"Age: {user['age']}\nDegree: {user['study_degree']}", user['user_count']) for user in user_data]
    age_degree_labels, user_counts = zip(*age_degrees)

    plt.figure(figsize=(10, 6))
    plt.bar(age_degree_labels, user_counts)
    plt.xlabel("Age and Study Degree")
    plt.ylabel("User Count")
    plt.title("User Distribution by Age and Study Degree")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

# Main function to run the app
def main9():
    user_data = fetch_users_by_age_and_degree()

    if user_data:
        st.title("User Distribution by Age and Study Degree")
        create_bar_plot(user_data)

    # Fetch and display the number of users grouped by age and study degree
    user_data = fetch_users_by_age_and_degree()

    if user_data:
       st.subheader("User Distribution by Age and Study Degree")

        # Convert the data to a DataFrame
       df = pd.DataFrame(user_data)

        
       st.dataframe(df)
    else:
        print("No user data available.")





# Function to fetch all users and their employment grant status
def fetch_users_and_employment_grant_status():
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT users.user_id, users_employment_grant.status
    FROM users
    LEFT JOIN users_employment_grant ON users.user_id = users_employment_grant.user_id
    """
    
    cursor.execute(query)
    user_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return user_data

# Function to fetch a summary of employment grant statuses
def fetch_employment_grant_summary():
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT status, COUNT(*) AS user_count
    FROM users_employment_grant
    GROUP BY status
    """
    
    cursor.execute(query)
    summary_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return summary_data

# Streamlit app
def main10():
    st.title("User Employment Grant Dashboard")

    # Fetch user data
    user_data = fetch_users_and_employment_grant_status()

    if user_data:
        st.subheader("Users and Their Employment Grant Status")

        # Convert the data to a DataFrame
        df = pd.DataFrame(user_data)

        
        st.dataframe(df)
      
    else:
        st.write("No user data available.")

    # Fetch and display a summary of employment grant statuses
    employment_grant_summary = fetch_employment_grant_summary()
    
    if employment_grant_summary:
        st.subheader("Employment Grant Status Summary")


        # Convert the data to a DataFrame
        df = pd.DataFrame(employment_grant_summary)

        
        st.dataframe(df)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from datetime import date, timedelta

# Sample data for 10 objects



def main():
    # Display the object dashboard

    # Sidebar options
    st.sidebar.title("Select Dashboard")
    selected_dashboard = st.sidebar.selectbox("Choose Dashboard", ["User Registration","created users by period","10k AI Initiative Dashboard", "User Courses","User Dashboard", "Admin Capstone Evaluations", "User Capstones", "Coupons and Users Usage", "User Distribution by Age and Study Degree", "User Employment Grant"])

    # Run the selected dashboard
    if selected_dashboard == "User Registration":
        main1()
    elif selected_dashboard =="created users by period":
        main2()    
    elif selected_dashboard =="10k AI Initiative Dashboard":
        main3() 
    elif selected_dashboard == "User Courses":
        main4()
    elif selected_dashboard == "User Dashboard":
        main5()
    elif selected_dashboard == "Admin Capstone Evaluations":
        main6()
    elif selected_dashboard == "User Capstones":
        main7()
    elif selected_dashboard == "Coupons and Users Usage":
        main8()
    elif selected_dashboard == "User Distribution by Age and Study Degree":
        main9()
    elif selected_dashboard == "User Employment Grant":
        main10()

if __name__ == "__main__":
    main()



