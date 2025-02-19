import argparse

import pickle

from pathlib import Path

file = (
    Path.home()
    / "Desktop"
    / "Projects"
    / "PyDAB"
    / "my_contacts.data"
)

try:
    file.touch(exist_ok=True)
    f = open(file, 'rb')
    # if f.read()==b'':
    if not len(f.read()):
        empty_dict = {}
        empty_dict_bytes = pickle.dumps(empty_dict)
        with open(file, 'wb') as data_file:
            data_file.write(empty_dict_bytes)
    f.close()
except FileExistsError:
    pass


def pickle_contact_dict(file, contact_dict):
    with open(file, 'wb') as f:
        pickle.dump(contact_dict, f)


def unpickle_contact_dict(file):
    try:
        if file.exists():
            with open(file, 'rb') as f:
                contact_dict = pickle.load(f)
                # print(contact_dict)
                return contact_dict
        else:
            return {}
    except EOFError:
        pass


class AddressBook:
    """A class representing an address book."""
    def __init__(self, name, email, phone, category):
        self.name = name
        self.email = email
        self.phone = phone
        self.category = category

    def __repr__(self):
        pass

def add_contact(name, email, phone, category):
    """Add new contact to addressbook.

    If the pickle file exists, unpickle, add new contact, and pickle.
    if file doesn't exist,
    """
    contact_name = AddressBook(name, email, phone, category)
    contact_dict = unpickle_contact_dict(file)
    contact_dict[contact_name.name] = [contact_name.email,
                                       contact_name.phone,
                                       contact_name.category]
    print(f"{name} added successfully.")
    pickle_contact_dict(file, contact_dict)


def delete_contact(name):
    """Remove contact from addressbook.

    If the pickle file exists, unpickle, find contact by key (i.e name),
    delete data, pickle remaining contact dictionary.
    """
    contact_dict = unpickle_contact_dict(file)
    if name in contact_dict.copy().keys():
        del contact_dict[name]
        print(f"{name} deleted successfully")
    pickle_contact_dict(file, contact_dict)
    return None


def find_contact(name):
    contact_dict = unpickle_contact_dict(file)
    try:
        contact = contact_dict[name]
        full_name = name
        email, phone, category = contact
        print(f"""
        Contact Name: {full_name}
        Phone: {phone}
        Email: {email}
        Category: {category}""")
    except KeyError:
        print(f"{name} not found")
        pass
    return None


def modify_contact(name, new_name, phone, email, category):
    try:
        contact_dict = unpickle_contact_dict(file)
        del contact_dict[name]
        pickle_contact_dict(file, contact_dict)
        add_contact(new_name, phone, email, category)
    except Exception as e:
        print(f"Exception {e} occured")
        pass
    return None


def show_contacts():
    contact_dict = unpickle_contact_dict(file)
    for key in contact_dict.keys():
        contact = contact_dict[key]
        full_name = key
        email, phone, category = contact
        output = f"""
        Contact Name: {full_name}
        Phone: {phone}
        Email: {email}
        Category: {category}
        -------------------------------------------------------"""
        print(output)
    return None


def count_contacts():
    contact_dict = unpickle_contact_dict(file)
    number_of_contacts = len(contact_dict)
    print(f"The AddressBook contains {number_of_contacts} items")


# TODO
# - Add optional argument 'path' to enable user specify where
# - to save pickled contacts and set default to home directory

# - Create CLI module and customize parsers and arguments

# - Init a new github repository for a 'persistent address book' python
# - program. PyPAB

# - Document functions and class properly

# - Package program and publish on pip


# ----------CLI--------- #
parser = argparse.ArgumentParser(prog="Address Book")

sub_parsers = parser.add_subparsers(
    title="Subparser of commands",
    dest='subcommands',
)

# Add contact
add_contact_parser = sub_parsers.add_parser('add_contact')
add_contact_parser.add_argument('name')
add_contact_parser.add_argument('email')
add_contact_parser.add_argument('phone')
add_contact_parser.add_argument('category')  # add choices to category

# Remove contact
remove_contact_parser = sub_parsers.add_parser('delete_contact')
remove_contact_parser.add_argument('name')

# Find contact
find_contact_parser = sub_parsers.add_parser('find_contact')  # enable finding contact without typing the full name
find_contact_parser.add_argument('name')

# Modify contact
modify_contact_parser = sub_parsers.add_parser('modify_contact')
modify_contact_parser.add_argument('name')
modify_contact_parser.add_argument('new_name')
modify_contact_parser.add_argument('email')
modify_contact_parser.add_argument('phone')
modify_contact_parser.add_argument('category')

# Show all contact
show_all_parser = sub_parsers.add_parser('show_contacts')
# show_all_parser.add_argument('name')


# Count contacts
modify_contact_parser = sub_parsers.add_parser('count_contacts')
# modify_contact_parser.add_argument('name')


args = parser.parse_args()

# Handle sub-commands
if args.subcommands == 'add_contact':
    add_contact(args.name, args.email, args.phone, args.category)
    show_contacts()
    print("The command is 'add_contact'")

elif args.subcommands == 'delete_contact':
    delete_contact(args.name)
    show_contacts()

elif args.subcommands == 'find_contact':
    find_contact(args.name)

elif args.subcommands == 'modify_contact':
    modify_contact(
        args.name,
        args.new_name,
        args.phone,
        args.email,
        args.category,
    )
    show_contacts()

elif args.subcommands == 'show_contacts':
    show_contacts()

elif args.subcommands == 'count_contacts':
    count_contacts()
