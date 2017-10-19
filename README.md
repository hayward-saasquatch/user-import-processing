# user-processing
Script for processing user imports 

## Referral Code Calculation
`calculateCodes.py`: used to add in unique codes for users

### Usage
`python3 calculateCodes.py -i testData.csv`
  
#### Options:
- `-i`,`--inputFile`: Which input file to use. Required.
- `-o`,`--outputFile`: Which output file to use. Optional.
  
## Merge in referral code and shareLinks
`mergeLinks.py`: used to merge referral code and shareLinks from `input2.csv` into existing list of user info `input1.csv` 

### Usage
`python3 example.py -i input1.csv input2.csv -o output1.csv`

#### Options:
- `-i`,`--inputFile`: Which input file to use. Required. Accepts list of two input files.
- `-o`,`--outputFile`: Which output file to use. Optional.
