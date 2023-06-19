import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py database.csv sequence.txt")

    # Read database file into a variable
    people = []

    database_file = open(sys.argv[1])
    reader = csv.DictReader(database_file)
    for row in reader:
        person = {}
        for sequence in row:
            person[sequence] = row[sequence]
        people.append(person)

    # Read DNA sequence file into a variable
    dna_sequence_file = open(sys.argv[2])
    dnasequence = dna_sequence_file.read()

    # Find longest match of each STR in DNA sequence
    longest_matches = {}
    str_list = []

    database_file.seek(0)

    str_reader = csv.reader(database_file)

    for row in str_reader:
        for sequence in row[1:]:
            str_list.append(sequence)
        break

    longest_matches["name"] = "0"

    for sequence in str_list:
        longest_matches[f"{sequence}"] = str(longest_match(dnasequence, sequence))

    # Close files
    database_file.close()
    dna_sequence_file.close()

    # Check database for matching profiles
    match = False

    for person in people:
        personname = person["name"]
        longest_matches["name"] = personname
        if longest_matches == person:
            print(personname)
            match = True

    if match == False:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
