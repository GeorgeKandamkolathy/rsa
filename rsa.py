import random
import math
import decimal
import base64
import json

class key:
    def __init__(self, modulus, exponent, length = 0):
        self.modulus = modulus
        self.exponent = exponent
        self.length = length


def createPrime():
    while True:
        x = random.getrandbits(1024) 
        if (x - 1) % 6 == 0 or (x + 1) % 6 == 0:
            break   
    
    k = 10
    for i in range(k):
        prime = millerTest(x)
        if prime == False:
            return (createPrime())
        i += 1
    return x


def millerTest(x):
    n = (x - 1)
    prime = True
    z = 0
    while n % 2 == 0:
        n //= 2
        z += 1 
    n = int(n)

    a = random.randint(1000,10000)

    test = pow(a,n,x)

    if test == (x - 1):
        prime = True
    
    elif test != 1:

        iterator = 1
        while iterator in range(z + 1):
            test = pow(a,n*(2**iterator),x)
            if test == (x - 1):
               return(True)
            iterator += 1
        prime = False

    else:
        prime = True

    return prime



def lcm(a, b):
    return a * b // math.gcd(a,b) 

def privExpo(e,lamdaN):
    exp = -1
    d = pow(e,exp,lamdaN)
    return(int(d))

def createKeys():
    
    p = createPrime()   
    q = createPrime()    

    while p == q:
        q = createPrime()

    n = p*q

    lamdaN = int(lcm(p-1,q-1))

    e = 65537

    while lamdaN % e == 0:
        p = createPrime()
        q = createPrime()
        lamdaN = lcm(p-1,q-1)

    d = privExpo(e, lamdaN)

    if d == 'Error':
        print('Exponent Error')
    
    public = key(n, e)
    private = key(n, d)

    return(public, private)


def encode(input, filename = 'encrypted',keyname = 'private'):
    public, private = createKeys()
    input = bytes(input,encoding = 'UTF-8')
    private.length = len(input)
    input = int.from_bytes(input,byteorder = 'big')
    f = open(filename + '.txt', 'w')
    f. write(str(pow(int(input),public.exponent, public.modulus)))
    f.close()
    f = open(keyname + '.pem', 'w')
    f. write(json.dumps({"exponent": private.exponent, "modulus": int(private.modulus), "length": int(private.length)}))
    f.close()

def decode(filename = 'encrypted.txt', keyname = 'private.pem'):
    f = open(filename, 'r')
    input = f.read()
    f.close()
    f = open(keyname, 'r')
    private = json.loads(f.read())
    output = pow(int(input),int(private['exponent']), int(private['modulus']))
    output = output.to_bytes(private['length'],'big')
    return(output.decode('utf-8'))       
