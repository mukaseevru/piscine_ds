import sys


def call_center():
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com', 'john@snow.is',
               'bill_gates@live.com', 'mark@facebook.com', 'elon@paypal.com', 'jessica@gmail.com']
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']
    return list(set(clients) - set(recipients))


def potential_clients():
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com', 'john@snow.is',
               'bill_gates@live.com', 'mark@facebook.com', 'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru', 'pinkman@yo.org', 'jessica@gmail.com',
                    'elon@paypal.com', 'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    return list(set(participants) - set(clients))


def loyalty_program():
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com', 'john@snow.is',
               'bill_gates@live.com', 'mark@facebook.com', 'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru', 'pinkman@yo.org', 'jessica@gmail.com',
                    'elon@paypal.com', 'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    return list(set(clients) - set(participants))


def marketing(line):
    if line == 'call_center':
        print(call_center())
    elif line == 'potential_clients':
        print(potential_clients())
    elif line == 'loyalty_program':
        print(loyalty_program())
    else:
        raise Exception('Use call_center/potential_clients/loyalty_program only')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        marketing(sys.argv[1])
    elif len(sys.argv) > 2:
        raise Exception('Error. Try python3 marketing.py call_center')
