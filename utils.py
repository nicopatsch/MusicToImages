import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

pitchDict = {
  "C": 0,
  "D": 2,
  "E": 4,
  "F": 5,
  "G": 7,
  "A": 9,
  "B": 11
}

accDict = {
    "#": 1,
    "b": -1,
    "n": 0
}

class Note:
    fA4 = 440
    a = 1.059463094359
    def __init__(self, pitch, octave, acc):
        self.pitch = pitch
        self.octave = octave
        self.acc = acc
        n = pitchDict[pitch]+accDict[acc] + octave*12 - (pitchDict['A'] + 4*12)
        #print(pitchDict[pitch]+accDict[acc] + octave*12)
        #Print(pitchDict['A'] + 4*12)
        #print(n)
        self.freq = self.fA4 * pow(self.a, n)


def printSimMatrices(freqArray, title, fig, plotIndex, maxIndex, halfWindow=0):
    
    nbNotes = len(freqArray)
    simMatrix = np.zeros((nbNotes, nbNotes))
    simMatrix1 = np.zeros((nbNotes, nbNotes))
    simMatrix3 = np.zeros((nbNotes, nbNotes))
    simMatrix5 = np.zeros((nbNotes, nbNotes))
    
    halfWindow=5
    for i in range(halfWindow, nbNotes-halfWindow):
        for j in range(halfWindow, nbNotes-halfWindow):
            for w in range(-halfWindow, halfWindow):
                simMatrix[i][j]+=abs(freqArray[i+w]-freqArray[j+w])
                if(w<=1): simMatrix1[i][j]+=simMatrix[i][j]
                if(w<=3): simMatrix3[i][j]+=simMatrix[i][j]
                if(w<=5): simMatrix5[i][j]+=simMatrix[i][j]

    simMatrix = np.add(np.multiply(simMatrix, -1./np.amax(simMatrix)), 1)
    simMatrix1 = np.add(np.multiply(simMatrix1, -1./np.amax(simMatrix1)), 1)
    simMatrix3 = np.add(np.multiply(simMatrix3, -1./np.amax(simMatrix3)), 1)
    simMatrix5 = np.add(np.multiply(simMatrix5, -1./np.amax(simMatrix5)), 1)

    # Similarity matrix
    plt.subplot(maxIndex, 4, 4*(plotIndex-1) + 1)
    imLeft = plt.imshow(simMatrix);
    plt.colorbar(imLeft,fraction=0.046, pad=0.04)
    plt.title(title + ' - Similarity matrix (halfWindow = '+str(halfWindow)+' )')

    plt.subplot(maxIndex, 4, 4*(plotIndex-1) + 2)
    imRight = plt.imshow(simMatrix1);
    plt.colorbar(imRight,fraction=0.046, pad=0.04)
    plt.title(title + ' - Similarity matrix (halfWindow = 1')
    
    plt.subplot(maxIndex, 4, 4*(plotIndex-1) + 3)
    imLeft = plt.imshow(simMatrix3);
    plt.colorbar(imLeft,fraction=0.046, pad=0.04)
    plt.title(title + ' - Similarity matrix (halfWindow = 3')

    plt.subplot(maxIndex, 4, 4*(plotIndex-1) + 4)
    imRight = plt.imshow(simMatrix5);
    plt.colorbar(imRight,fraction=0.046, pad=0.04)
    plt.title(title + ' - Similarity matrix (halfWindow = 5')



def printSimMatrixAndSimple(freqArray, title, fig, plotIndex, maxIndex):
    
    nbNotes = len(freqArray)
    simMatrix = np.zeros((nbNotes, nbNotes))
    simpleSimMatrix8 = np.zeros((nbNotes, nbNotes))
    simpleSimMatrix9 = np.zeros((nbNotes, nbNotes))
    simpleSimMatrix95 = np.zeros((nbNotes, nbNotes))
    
    for i in range(0, nbNotes):
        for j in range(0, nbNotes):
            simMatrix[i][j]+=abs(freqArray[i]-freqArray[j])

    simMatrix = np.multiply(simMatrix, -1./np.amax(simMatrix))
    simMatrix = np.add(simMatrix, 1)

    for i in range(0, nbNotes):
       for j in range(0, nbNotes):
           if(simMatrix[i][j] >= 0.8): simpleSimMatrix8[i][j] = simMatrix[i][j]
           else: simpleSimMatrix8[i][j] = 0.8
                
           if(simMatrix[i][j] >= 0.9): simpleSimMatrix9[i][j] = simMatrix[i][j]
           else: simpleSimMatrix9[i][j] = 0.9
                
           if(simMatrix[i][j] >= 0.95): simpleSimMatrix95[i][j] = simMatrix[i][j]
           else: simpleSimMatrix95[i][j] = 0.95

    # Similarity matrix
    plt.subplot(maxIndex, 4, 4*(plotIndex-1) + 1)
    imLeft = plt.imshow(simMatrix);
    plt.colorbar(imLeft,fraction=0.046, pad=0.04)
    plt.title(title + ' - Similarity matrix')

    # Simplified similarity matrix 0.8
    plt.subplot(maxIndex, 4, 4*(plotIndex-1) + 2)
    imRight = plt.imshow(simpleSimMatrix8);
    plt.colorbar(imRight,fraction=0.046, pad=0.04)
    plt.title(title + ' - Similarity matrix 0.8')
    
     # Simplified similarity matrix 0.9
    plt.subplot(maxIndex, 4, 4*(plotIndex-1) + 3)
    imLeft = plt.imshow(simpleSimMatrix9);
    plt.colorbar(imLeft,fraction=0.046, pad=0.04)
    plt.title(title + ' - Similarity matrix 0.9')

    # Simplified similarity matrix 0.95
    plt.subplot(maxIndex, 4, 4*(plotIndex-1) + 4)
    imRight = plt.imshow(simpleSimMatrix95);
    plt.colorbar(imRight,fraction=0.046, pad=0.04)
    plt.title(title + ' - Similarity matrix 0.95')

def getFreqString(root, pieceName, partID, printString=0):
    return getFreqArrayAndString(root, pieceName, partID, printString)[1]

def getFreqArray(root, pieceName, partID, printString=0):
    return getFreqArrayAndString(root, pieceName, partID, printString)[0]

def getFreqArrayAndString(root, pieceName, partID, printString=0):

    # Select prefered part
    part = root.find("./part[@id='"+partID+"']")
    if(part==None):
        print("Part with id: "+partID+" not found")
    partName = root.find("./part-list/score-part[@id='"+partID+"']/part-name").text
    # Get number of measures in part
    measuresXML = part.findall("./measure")
    if(measuresXML == None):
        nbOfMeasures = 0
    else:
        nbOfMeasures = len(measuresXML)

    xmlMeasures = part.findall("./measure")
    
    
    # create array of nbOfNotes elements
    freqArray = np.array([])
    freqString = partName + "\n"
    for currentMeasure in xmlMeasures:
        notes = currentMeasure.findall('./note')
        newMeasure = []
        for note in notes:
            if(len(note.findall('./rest'))):
                #print("0")
                newMeasure = np.append(newMeasure, 0.)
                freqString += "0"
            else:
                pitchStepXML = note.find('./pitch/step')
                if(pitchStepXML != None):
                    pitchStep = pitchStepXML.text
                else:
                    pitchStep = "A"

                pitchOctaveXML = note.find('./pitch/octave')
                if(pitchOctaveXML != None):
                    pitchOctave = pitchOctaveXML.text
                else:
                    pitchOctave = "7 "
                freq = Note(pitchStep, int(pitchOctave), 'n').freq
                #print(freq)
                newMeasure = np.append(newMeasure, float(freq))
                
                freqString += str(round(freq, 2))+" "
        freqString+=" "
        freqArray = np.append(freqArray, newMeasure)
    
    if(printString):
        print(freqString)
    
    return [freqArray, freqString]