from itertools import islice
from string import ascii_lowercase
from random import choice, randint, seed

# top level domains
TLDS = ('com net org mil edu de biz de ch at ru de tv com'
    'st br fr de nl dk ar jp eu it es com us ca pl').split()
    
def gen_name(length):
    """Generate a random name with the given number of characters."""
    seed()
    return ''.join(choice(ascii_lowercase) for _ in xrange(length))

def address_generator():
    """Generate fake e-mail addresses."""
    seed()
    while True:
        user = gen_name(randint(3,10))
        host = gen_name(randint(4,20))
        yield '%s@%s.%s' % (user, host, choice(TLDS))
        
def fake_addresses(count=20, sep=', '):
    return sep.join(islice(address_generator(), count))