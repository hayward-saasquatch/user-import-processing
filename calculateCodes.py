import sys, argparse, csv, re

#compile the regex expresion used to parse out special characters
noSpecialReg = re.compile(r"[^A-Za-z0-9]")

#parse input arguments -o, output, -i, input
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inputFile', help='which input file to use', required=True)
parser.add_argument('-o','--outputFile', help='which output file to use')
args = parser.parse_args()

if args.inputFile: ifilePath = args.inputFile
if args.outputFile: ofilePath = args.outputFile
else: 
    ofilePath = ifilePath.split(".csv")
    ofilePath = ofilePath[0] + "_output.csv"

#open input file
ifile  = open(ifilePath, newline='')
reader = csv.reader(ifile)

#open output file to write to
ofile  = open(ofilePath, 'w', newline='')
writer = csv.writer(ofile)

#initialize list of taken codes
codeList = []

#initialize column locations of specific variables
inputFirstNameColumn = None
inputLastNameColumn = None
inputEmailColumn = None
inputCodeColumn = None

#initialize list for first row headers
firstRow = []

#loop through each row (in this case stop at the end of the first row)
for row in reader:
    # do something here with `row`
    
    firstRow = row
    
    #loop through cells in the first row to see where required fields are
    for index, cell in enumerate(row):
        
        print("Cell: ", cell)
    
        if cell == "firstName": inputFirstNameColumn = index
        if cell == "lastName": inputLastNameColumn = index
        if cell == "email": inputEmailColumn = index
        if cell == "code": inputCodeColumn = index
    
    #only loop through the first row (not hacky at all)
    break
            
def makeCode(row):
    
    #try looking up the firstName value in the row, if not found leave it empty
    try:
        firstName = noSpecialReg.sub("", row[inputFirstNameColumn])
        #firstName = row[inputFirstNameColumn].replace(/[^A-Za-z0-9]/g, '')
    except:
        firstName = ""
    
    #set the name to all upper-case    
    firstName = firstName.upper()
    #print("FirstName: ", firstName)
    
    #try looking up the lastName value in the row, if not found leave it empty
    try:
        lastName = noSpecialReg.sub("", row[inputLastNameColumn])
        #lastName = values_values[i][input_lastName_column].replace(/[^A-Za-z0-9]/g, '')
    except:
        lastName = ""
    
    #set the name to all upper-case
    lastName = lastName.upper()
    #print("LastName: ", lastName)
    
    name = ""
    name = firstName + lastName
    
    #truncate the name to 16 characters in length
    code = name[0:16]
    
    #if there was no first or last name we will try using the first part of the email address
    if code == "":
        try:
            email = row[inputEmailColumn].split("@")
            email = email[0].upper()
            
        except:
            email = ""
        
        code = email
    
    #check if the code we just generated is unique
    code = makeUnique(code)
    
    #add the code into the code field in the row
    row[inputCodeColumn] = code
    
    #return the row back into the main function to be written to the output file
    return row

def makeUnique(initialCode):
    
    #start with the name-based code that we need to test the uniqueness of
    tempCode = str(initialCode)

    count = 0
    
    isUnique = False

    #loop while we dont know that the code is unique
    while isUnique == False:
        
        #lets assume the code is unique to start each full comparison test
        isUnique = True
            
        #append a number to the end of the code if the code is already taken (and thus the counter has been incremented)
        if count != 0:
    
            tempCode = str(initialCode) + str(count)

        #loop through each of the codes already generated, and check to be unique in codeList
        for code in codeList:
            
            #if the current code matches another code
            if tempCode == code:
                
                #set the code as not unique, increment the counter, this will bring the loop back to try again with a higher number appended
                isUnique = False
                count = count +1
    
    #once we know the code is unique append it to the list of unique codes (codeList) and return it
    codeList.append(tempCode)
    return tempCode

def main():

    #write the header row to the output file
    writer.writerow(firstRow)
    
    #loop through each row in the input file
    for row in reader:
        
        #The row, once the new code has been added in
        row = makeCode(row)
        print("Row: ", row)
        
        #write the new row to the output file
        writer.writerow(row)

if __name__ == '__main__':
  main()