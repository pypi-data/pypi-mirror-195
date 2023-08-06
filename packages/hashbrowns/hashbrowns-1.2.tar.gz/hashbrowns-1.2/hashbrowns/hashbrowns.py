try:
  import random
  import os
  import sys
  import string
  import hashlib
  import platform
  import time, datetime
except ImportError:
  print("Error: Missing module(s) please install the following module(s): random, time, hashlib, string")


# Classes
class functions:
  def clearconsole():
    if platform == "linux" or platform == "linux2":
      os.system("clear")
    else:
      os.system("cls")
    return str("")

  def checkfile(file, print=None):
    if os.path.isfile(file) == False:
      returnList = ("File not found", "Or is not a file")
    if os.path.isfile(file) == True:
      with open(file, "r") as File:
        lines = File.readlines()
        size = ("Size:", os.path.getsize(file))
        lastedited = ("Last-Opened:", os.path.getmtime(file))
        linenum = ("Line-Number:", len(lines))
        creationTime = ("Created:", os.path.getctime(file))
        returnList = (size, lastedited, linenum, creationTime)
      if print!=None:
        print(returnList)
      else:
        return returnList

  def mutilate(file):
    with open(file, "r+") as Fout:
      for line in Fout:
        lineList = list(line)
        randoms = list(string.printable)
        
      for i in lineList:
        newList = lineList + randoms
        random.shuffle(newList)
 
      newLine = ''.join(random.choice(newList) for i in range(len(lineList)))
      Fout.truncate(0)
      Fout.write(newLine)

  def getinfo():
    # DISCLAMER: This is not for malicious use, this is for development only.
    OS = ("Operating-System: ", sys.platform)
    currentTime = ("Time: ", datetime.now().time())
    currentDate = ("Date: ", datetime.now().date())
    currentProccess = ("Current-Process: ", os.getpid())
    encoding = ("Encoding: ", sys.getfilesystemencoding())
    returnList = (OS, currentDate, currentTime, currentProccess, encoding)
    return returnList
  
  def wipefile(file):
    with open(file, "w") as Fout:
      Fout.truncate(0)
      Fout.close()
    return str("")


class hash():
  def hash(target, print=None):
    sha256 = hashlib.sha256()
    xO = random.randint(10, 200)
    targetConvert = list(target)
    for i in range(xO):
      random.shuffle(targetConvert)

    targetShuffled = ''.join(targetConvert)
    sha256.update(targetShuffled.encode())

    if print != None:
      print(sha256.hexdigest())
    else:
      return sha256.hexdigest()

  def hashfile(file):
    BUF_SIZE = os.path.getsize(file)

    sha256 = hashlib.sha256()

    with open(file, 'rb') as f:
      while True:
        data = f.read(BUF_SIZE)

        if not data:
          break

    sha256.update(data)

    return sha256.hexdigest()

  def comparehash(hashA, hashB):
    if hashA is hashB:
      return True
    else:
      return False


class key():
  def keypair():
    threshold = random.randint(6, 14)
    buff = random.randint(300, 10000)
    length = random.randint(50, 350)
    iterable = 0
    tiny = random.uniform(0.001, 0.999)
    alphabet = string.ascii_letters + string.digits
    publicBase = '.'.join(random.choice(alphabet) for i in range(buff))
    privateBase = '.'.join(random.choice(alphabet) for i in range(buff))

    time.sleep(tiny)

    publicList = publicBase.split('.')
    privateList = privateBase.split('.')

    while iterable != threshold:
      x = privateList + publicList
      y = publicList + privateList
      for iteam in x, y:
        random.shuffle(x)
        random.shuffle(y)
      iterable += 1

    time.sleep(tiny)

    publicKey = ''.join(random.choice(x) for iterable in range(length))
    privateKey = ''.join(random.choice(y) for iterable in range(length))

    return publicKey, privateKey

  def solokey():
    threshold = random.randint(7, 12)
    primBuff = random.randint(500, 1000)
    secBuff = random.randint(500, 1000)
    length = random.randint(50, 350)
    iterable = 0
    tiny = random.uniform(0.001, 0.999)
    alphabet = string.ascii_letters + string.digits
    primaryBase = '.'.join(random.choice(alphabet) for i in range(primBuff))
    secondaryBase = '.'.join(random.choice(alphabet) for i in range(secBuff))

    time.sleep(tiny)

    primaryList = secondaryBase.split('.')
    secondaryList = primaryBase.split('.')

    while iterable != threshold:
      foo = primaryList + secondaryList
      bar = secondaryList + primaryList
      foobar = bar + foo
      for iteam in range(length):
        random.shuffle(foo)
        random.shuffle(bar)
        random.shuffle(foobar)
      iterable += 1

    time.sleep(tiny)

    soloKey = ''.join(random.choice(foobar) for iterable in range(length))

    return soloKey

  def secure(key):
    keyLength = len(key)
    keyList = list(key)
    olprime = random.randint(3, 8)
    buff = random.randint(200, 1000)
    alphabet = string.ascii_letters + string.digits + string.digits
    randomkey = list(random.choice(alphabet) for i in range(buff))

    for z in range(olprime):
      random.shuffle(keyList)
      random.shuffle(keyList)
      bar = keyList + randomkey
      for i in bar:
        random.shuffle(bar)

    newkey = ''.join(random.choice(bar) for i in range(keyLength))

    newList = list(newkey)

    for y in range(olprime):
      random.shuffle(randomkey)
      random.shuffle(randomkey)

    for x in range(olprime):
      random.shuffle(newList)
      random.shuffle(newList)
      foo = randomkey + newList
      for i in foo:
        random.shuffle(foo)

    returnKey = ''.join(random.choice(foo) for i in range(keyLength))

    return returnKey
  
  def validatekey(key, print=None):
    lowerAlphabet = list(string.ascii_lowercase)
    higherAlphabet = list(string.ascii_uppercase)
    allNumbers = list(string.digits)
    keyList = list(key)
    returnItem = list()
    lowercount = 0
    uppercount = 0
    digitcount = 0

    for i in keyList:
      if i in lowerAlphabet:
        lowercount += 1
      if i in higherAlphabet:
        uppercount += 1
      if i in allNumbers:
        digitcount += 1
    
    if int(uppercount + lowercount + digitcount) >= 40:
      returnItem.append("Strong Key")
    elif int(uppercount + lowercount + digitcount) >= 30:
      returnItem.append("Medium Key")
    elif int(uppercount + lowercount + digitcount) >= 20:
      returnItem.append("Weak Key")
    else:
      returnItem.append("Unsafe Key!")
    
    if print != None:
      print(returnItem)
    else:
      return returnItem


class encryption():
  def standard(file, message):
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    fernet = Fernet(key)

    with open(file, 'rb') as Fin:
      original = Fin.read()
      Fin.close()

    encrypted = fernet.encrypt(original)

    with open(file, 'wb') as Fout:
      Fout.write(encrypted)
      Fout.close()

    return key

  def double(file, message):
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    fernet = Fernet(key)

    with open(file, 'rb') as Fin:
      original = Fin.read()
      Fin.close()

    encrypted = fernet.encrypt(original)
    doubled = fernet.encrypt(encrypted)

    with open(file, 'wb') as Fout:
      Fout.write(doubled)
      Fout.close()

    return key


class decryption():
  def standard(file, key):
    from cryptography.fernet import Fernet
    fernet = Fernet(key)

    with open(file, 'rb') as Fin:
      encrypted = Fin.read()
      Fin.close()

    decrypted = fernet.decrypt(encrypted)

    with open(file, 'wb') as Fout:
      Fout.write(decrypted)
      Fout.close()

  def double(file, key):
    from cryptography.fernet import Fernet
    fernet = Fernet(key)

    with open(file, 'rb') as Fin:
      encrypted = Fin.read()
      Fin.close()

    decrypted = fernet.decrypt(encrypted)
    doubled = fernet.decrypt(decrypted)

    with open(file, 'wb') as Fout:
      Fout.write(doubled)
      Fout.close()

