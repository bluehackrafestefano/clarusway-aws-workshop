sayi = input("Please enter a number between 0-3999: ")

if sayi.isdigit() and int(sayi)>0 and int(sayi)<4000:

    say=int(sayi)

    roman=''

    M = say//1000
    if M != 0 :
        say = (say - (M * 1000))
        roman+=M*'M'

    D = say//500
    if D != 0 :
        say = (say - (D * 500))
        roman+=D*'D'

    C = say//100
    if C != 0 :
        say = (say - (C * 100))
        roman+= C*'C'

    L = say//50
    if L != 0 :
        say = (say - (L * 50))
        roman+=L*'L'

    X = say//10
    if X != 0 :
        say = (say - (X * 10))
        roman+= X*'X'

    I = say
    if I != 0:
        roman+= say*'I'

# now lets deal with exceptions:
    roman1=roman.replace('DCCCC', 'CM') # this is for 900
    roman2=roman1.replace('CCCC', 'CD') # this is for 400
    roman3=roman2.replace('LXXXX', 'XC') # this is for 90
    roman4=roman3.replace('XXXX', 'XL') # this is for 40
    roman5=roman4.replace('IIIIIIIII', 'IX') # this is for 9
    roman6=roman5.replace('IIIIIIII', 'VIII') # this is for 8, this is an additional exception
    roman7=roman6.replace('IIII', 'IV') # this is for 4
    
    print(f'Your number is --{roman7}-- in roman numerals.')
    
else:
    print("Not Valid! Please enter a number between 1 and 3999 inclusively.")