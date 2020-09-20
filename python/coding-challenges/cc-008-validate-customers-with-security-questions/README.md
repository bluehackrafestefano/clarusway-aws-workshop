# Coding Challenge - 008 : Validate Customers with Security Questions

The purpose of this coding challenge is to write a program that asks security questions to the customer to check if he is a valid user that exists in the database.

## Learning Outcomes

At the end of this coding challenge, students will be able to;

- Analyze a problem, identify, and apply programming knowledge for appropriate solution.

- Implement conditional statements effectively to solve a problem.

- Demonstrate their knowledge of algorithmic design principles by solving the problem effectively.

## Problem Statement

Companies use security questions to check if a customer is valid and exists in their database before executing any operations requested by the customer (telecommunication companies, banks, etc.).

In this coding challenge, you are going to create a security questions program to assist the customer representative with questions which should be answered by the customer.

Customer should be checked for **customer's name**, **customer's username**, and **customer's birthday**.

The database is given in python lists. The matching name, surname, and birthday combinations are in the same indexes of the lists. So if the customer's name is in the first index of the name list, his surname and birthday are also going to be in the first indexes of the surname and birthday lists.

You should start by asking for customers' names, then continue with customer's surname and birthday respectively.

Each time you get the information from the customer, you should check if that information is valid or matches with existing records.

If the input is not valid or the combination that is provided does not match, the program should give an appropriate message and terminate without asking rest of the questions.

If all the information is valid and matches the pattern, the program should give an appropriate validation message.

A sample database can be designed as the following:

```python
# users database - a particular index corresponds to a specific user
names = ["James", "John", "Emma"]
surnames = ["Oliver", "Smith", "Brown"]
birth_days = [15, 22, 8]
birth_months = [3, 6, 12]
birth_years = [1984, 1994, 2001]
```

- Example for user inputs and respective outputs.

```text
Please enter your name: Jack

You are not a customer!


Please enter your name: James

Please enter your surname: Smith

You are not a customer!


Please enter your name: James

Please enter your surname: Oliver

Please enter your birthday (MM/DD/YYYY): 3/15/1984

You have entered an incorrect value!


Please enter your name: James

Please enter your surname: Oliver

Please enter your birthday (MM/DD/YYYY): 03.15/1984

You have entered an incorrect value!


Please enter your name: James

Please enter your surname: Oliver

Please enter your birthday (MM/DD/YYYY): 03/15/1984

You are a customer!
```
