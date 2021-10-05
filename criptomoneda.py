'''
Titulo: Criptomoneda con Python
Autor: franciscofl12
'''

#Importaciones del proyecto
import hashlib
import datetime
import json
import pprint
from time import time

#Clase Bloque
class Block:
    
    #Constructor por defecto
    def __init__(self, timeStamp, trans, previousBlock = ''):
        self.timeStam = timeStamp
        self.trans = trans
        self.previousBlock = previousBlock
        self.difficultyIncrement = 0
        self.hash = self.calculateHash(trans,timeStamp,self.difficultyIncrement)

    #Función para cacular el Hash
    def calculateHash(self, data, timeStamp,difficultyIncrement):
        data = (str(data) + str(timeStamp) + str(difficultyIncrement)).encode()
        hash = hashlib.sha256(data).hexdigest()
        return hash

    #Función para el minado de los bloques
    def mineBlock(self,difficulty):
        #La dificultad será afectada según los 0 que queramos que empiece el Hash.
        difficultyCheck = "0" * difficulty
        while self.hash[:difficulty] != difficultyCheck:
            self.hash = self.calculateHash(self.trans, self.timeStam, self.difficultyIncrement)
            self.difficultyIncrement +=1


#Clase Blockchain
class Blockchain:

    #Contructor por defecto
    def __init__(self):
        self.chain = [self.GenesisBlock()]
        self.difficulty = 5
        self.pendingTransaction = []
        self.reward = 10

#Acceso para acceder al Bloque 0 en BTC
    def GenesisBlock(self):
        genesisBlock = Block(str(datetime.datetime.now()), "First Block ever created.")
        return genesisBlock

    #Función para obtener el último bloque creado
    def getLastBlock(self):
        return self.chain[len(self.chain)-1]

    #Función para obtener el minero del bloque
    def minePendingTrans(self, minerRewardAddress):
        newBlock = Block(str(datetime.datetime.now()), self.pendingTransaction)
        newBlock.mineBlock(self.difficulty)
        newBlock.previousBlock = self.getLastBlock().hash

        print(f"Hash del bloque previo: {newBlock.previousBlock}")

        testChain = []
        for trans in newBlock.trans:
            temp = json.dumps(trans.__dict__ , indent=5, separators=(',',':'))
            testChain.append(temp)
        pprint.pprint(testChain)

        self.chain.append(newBlock)
        print(f"Hash del bloque actual: {newBlock.hash}")

        rewardTrans = Transaction("Sistema" , minerRewardAddress, self.reward)
        self.pendingTransaction.append(rewardTrans)
        self.pendingTransaction = []

    #Validación de la cadena de bloques
    def isChainValid(self):

        for x in range(1, len(self.chain)):
            currentBlock = self.chain[x]
            previousBlock = self.chain[x-1]

            if (currentBlock.previousBlock != previousBlock.hash):
                print("La cadena no es válida.")

        print("La cadena es válida.")

    #Creación de nueva transacción
    def createTrans(self, transaction):
        self.pendingTransaction.append(transaction)

    #Obtener el balance de una wallet
    def getBalance(self, walletAddress):
        balance = 0
        for block in self.chain:
            if block.previousBlock == "":
                continue
            for transaction in block.trans:
                if transaction.fromWallet == walletAddress:
                    balance -+ transaction.amount
                if transaction.toWallet == walletAddress:
                    balance += transaction.amount
        return balance
    
#Clase Transación
class Transaction:

    #Constructor por defecto
    def __init__(self, fromWallet,toWallet,amount):
        self.fromWallet = fromWallet
        self.toWallet = toWallet
        self.amount = amount



#Comprobación de funcionalidad de la criptomoneda.

criptomoneda = Blockchain()

criptomoneda.createTrans(Transaction("A","B", 0.01))
criptomoneda.createTrans(Transaction("C","H", 0.05))
criptomoneda.createTrans(Transaction("D","U", 200))

#Vamos a calcular cuanto tiempo tarda en minar una transacción
tiempo_inicio = time()
criptomoneda.minePendingTrans("TestMiner")
tiempo_final = time()
print(f"TestMiner tardó {tiempo_final-tiempo_inicio} segundos.")

criptomoneda.createTrans(Transaction("S","B", 0.01))
criptomoneda.createTrans(Transaction("X","R", 0.05))
criptomoneda.createTrans(Transaction("T","X", 200))

#Vamos a calcular cuanto tiempo tarda en minar una transacción
tiempo_inicio = time()
criptomoneda.minePendingTrans("TestMiner 2")
tiempo_final = time()
print(f"TestMiner 2 tardó {tiempo_final-tiempo_inicio} segundos.")

#Comprobación de los wallets para ver sin han obtenido sus rewards
print(f"TestMiner tiene " + str(criptomoneda.getBalance("TestMiner")) + " criptomonedas en su Wallet")
print(f"TestMiner 2 tiene " + str(criptomoneda.getBalance("TestMiner 2")) + " criptomonedas en su Wallet")

#Hash de los bloques de la cadena
for x in range(len(criptomoneda.chain)):
    print(f"Hash del Bloque {x}: {criptomoneda.chain[x].hash}")

#Validación de cadena
print(criptomoneda.isChainValid())