def camelize(string):
    string1 = string.split('-')
    newstr = []
    for i in string1:
        if i == string1[0]:
            newstr.append(i)
            continue
        newstr.append(i[0].upper() + i[1:])

    newstr = ''.join(newstr)
    return newstr


print(camelize('background-color'))
print(camelize("list-style-image"))
print(camelize("-webkit-transition"))