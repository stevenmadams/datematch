import csv

def load_csv(filename):
    data = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def main():
    # Load data from CSV files
    men_data = load_csv('men.csv')
    women_data = load_csv('women.csv')

    # Create dictionaries to store matches
    men_matches = {man['man_number']: [] for man in men_data}
    women_matches = {woman['woman_number']: [] for woman in women_data}

    # Helper function to find a person by number
    def find_person(person_number, data):
        for person in data:
            if person['person_number'] == person_number:
                return person
        return None

    while True:
        person_type = input("\nEnter 'M' to input matches for a man or 'W' for a woman (or 'done' to finish): ").strip().upper()
        if person_type == 'DONE':
            break
        if person_type not in ('M', 'W'):
            print("Invalid input, please enter 'M' or 'W'.")
            continue

        person_number = input("Enter their number: ").strip()
        if person_type == 'M':
            person = next((man for man in men_data if man['man_number'] == person_number), None)
            if not person:
                print("Invalid man number, please try again.")
                continue
            matches_input = input(f"For whom did {person['man_name']} (man #{person_number}) say YES? (Enter numbers separated by space): ")
            men_matches[person_number] = matches_input.strip().split()
        elif person_type == 'W':
            person = next((woman for woman in women_data if woman['woman_number'] == person_number), None)
            if not person:
                print("Invalid woman number, please try again.")
                continue
            matches_input = input(f"For whom did {person['woman_name']} (woman #{person_number}) say YES? (Enter numbers separated by space): ")
            women_matches[person_number] = matches_input.strip().split()

    # Find mutual matches
    mutual_matches = []
    for man_number, woman_numbers in men_matches.items():
        for woman_number in woman_numbers:
            if woman_number in women_matches and man_number in women_matches[woman_number]:
                mutual_matches.append((man_number, woman_number))

    # Organize mutual matches by men and women
    men_to_women_matches = {man['man_number']: [] for man in men_data}
    women_to_men_matches = {woman['woman_number']: [] for woman in women_data}

    for man_number, woman_number in mutual_matches:
        men_to_women_matches[man_number].append(woman_number)
        women_to_men_matches[woman_number].append(man_number)

    # Print mutual matches for men
    for man in men_data:
        man_number = man['man_number']
        man_name = man['man_name']
        if men_to_women_matches[man_number]:
            print(f"\nCongrats {man_name} (man #{man_number}), you matched with:")
            for woman_number in men_to_women_matches[man_number]:
                woman_name = next(woman['woman_name'] for woman in women_data if woman['woman_number'] == woman_number)
                woman_phone = next(woman['woman_phone'] for woman in women_data if woman['woman_number'] == woman_number)
                print(f"{woman_name} ({woman_phone})")
        else:
            print(f"\nSorry {man_name} (man #{man_number}), no matches this time!")

    # Print mutual matches for women
    for woman in women_data:
        woman_number = woman['woman_number']
        woman_name = woman['woman_name']
        if women_to_men_matches[woman_number]:
            print(f"\nCongrats {woman_name} (woman #{woman_number}), you matched with:")
            for man_number in women_to_men_matches[woman_number]:
                man_name = next(man['man_name'] for man in men_data if man['man_number'] == man_number)
                man_phone = next(man['man_phone'] for man in men_data if man['man_number'] == man_number)
                print(f"{man_name} ({man_phone})")
        else:
            print(f"\nSorry {woman_name} (woman #{woman_number}), no matches this time!")

if __name__ == "__main__":
    main()
