import sys, argparse, csv, re

#parse input arguments -o, output, -i, input
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inputFile', help='which input file to use', nargs='+',required=True)
parser.add_argument('-o','--outputFile', help='which output file to use')
args = parser.parse_args()

ifilePath = []
readers = []

if args.inputFile:

    for item in args.inputFile:
        ifilePath.append(item)
        readers.append(csv.reader(open(item, newline='')))
if args.outputFile: ofilePath = args.outputFile
else:
    ofilePath = ifilePath[0].split(".csv")
    ofilePath = ofilePath[0] + "_output.csv"

#open output file to write to
ofile  = open(ofilePath, 'w', newline='')
writer = csv.writer(ofile)

print("ifilePath: ", ifilePath)

print("ofilePath: ", ofilePath)

#open input file
ifile  = open("Referral-SaaS_List.csv", newline='')
reader = csv.reader(ifile)

#open input file 2
ifile2  = open("USER_REPORT_Bambora_20171011-20171018.csv", newline='')
reader2 = csv.reader(ifile2)

#open output file to write to
ofile  = open("Bambora_output.csv", 'w', newline='')
writer = csv.writer(ofile)

#initialize list of taken codes
codeList = []

#initialize column locations of specific variables
accountIdColumn = None
accountIdColumn2 = None
userIdColumn = None
userIdColumn2 = None
codeColumn = None
emailShareLink = None
facebookShareLink = None
linkedinShareLink = None
shareLink = None
twitterShareLink = None


#initialize list for first row headers
firstRow = []

#loop through each row (in this case stop at the end of the first row)
for row in readers[0]:
    # do something here with `row`

    firstRow = row

    #loop through cells in the first row to see where required fields are
    for index, cell in enumerate(row):

        #print("Cell: ", cell)

        if cell == "MID": accountIdColumn = index
        if cell == "user name": userIdColumn = index

    #only loop through the first row (not hacky at all)
    break

for row in readers[1]:
    # do something here with `row`

    print(row)
    #firstRow = row

    #loop through cells in the first row to see where required fields are, and append the sharelink and code titles to the first row of the output file
    for index, cell in enumerate(row):

        print("Cell: ", cell)

        if cell == "accountId": accountIdColumn2 = index
        if cell == "id": userIdColumn2 = index
        if cell == "referralCode":
            codeColumn = index
            firstRow.append(cell)
        if cell == "emailShareLink":
            emailShareLink = index
            firstRow.append(cell)
        if cell == "facebookShareLink":
            facebookShareLink = index
            firstRow.append(cell)
        if cell == "linkedinShareLink":
            linkedinShareLink = index
            firstRow.append(cell)
        if cell == "shareLink":
            shareLink = index
            firstRow.append(cell)
        if cell == "twitterShareLink":
            twitterShareLink = index
            firstRow.append(cell)

    #only loop through the first row (not hacky at all)
    break

#read in the second input file to a list as you can only interate through the actual file once
readers1Values = []
for row in readers[1]:
    readers1Values.append(row)


#function to lookup where in the second file the user listed in the first file is
def lookupParticipant(lookupAccount, lookupUser):
    count = 0

    #list of new values to tack on
    valueList = []

    for row in readers1Values:
        count+=1
        #if the account and user IDs match
        if lookupAccount == row[accountIdColumn2] and lookupUser == row[userIdColumn2]:
            #rerturn the row in sheet 2 that houses the participant info

            valueList = [row[codeColumn], row[shareLink], row[emailShareLink], row[facebookShareLink], row[linkedinShareLink], row[twitterShareLink]]

            print("valueList: ", valueList)

            #return the sharelinks for the specific user
            return valueList

#create a new row for the output file
def createRow(row, rowValues):
    makeRow = row

    print(makeRow)

    #loop through all the values to be added to the new row
    for value in rowValues:
        print(value)
        makeRow.append(value)

    return makeRow

def main():

    #write the header row to the output file
    writer.writerow(firstRow)

    #loop through each row in the input file
    for row in readers[0]:

        print(row)

        rowValues = None

        #returns a list of sharelink values for the specific user
        rowValues = lookupParticipant(row[accountIdColumn],row[userIdColumn])

        if rowValues:
            print("rowValues: ", rowValues)

            #combines the existing row with the new sharelinks
            outputRow = createRow(row,rowValues)

            #The row, once the new code has been added in
            print("Row: ", outputRow)

            #write the new row to the output file
            writer.writerow(outputRow)

if __name__ == '__main__':
  main()
