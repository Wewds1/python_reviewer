# no 18 hands on as per python basic


## EASY VARIABLES

name = 'Allen'
age = 25
is_employed = False


name = age

TAX_RATE = 0.08
price = 49.99

total_tax = price * TAX_RATE


# print(f"Name: {name}")
# print("Total Tax", total_tax)


## Medium Variables

a = [1,2,3]
b = a

b.append(4)

print("List a:", a)

# errors = warnings = passed = 0


#  both will have 0 since its bascially the same id() and using that they will have the same value


# Hard Variables


errors = warnings = passed = []

errors.append("Error 1")

print("Errors:", errors)
print("Warnings:", warnings)
print("Passed:", passed)

# They are the same Objects

# for the fix, it needs to be in seperate list so they will not have the same id() and will not be the same object

errors = []
warnings = []
passed = []

errors.append("Error 1")

print("Errors Fixed:", errors)
print("Warnings Fixed:", warnings)
print("Passed Fixed:", passed)


x = 10
y = x
x += 5
print(x, y)


a = [10]
b = a
a += [5]
print(a, b)