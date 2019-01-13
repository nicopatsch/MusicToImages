import xml.etree.ElementTree as ET
import numpy as np
import utils as u
from matplotlib.ticker import NullFormatter

import sys
import matplotlib.pyplot as plt

# The Firebird, Stravinsky
#pieceName = "Stravinsky-Firebird_Finale"
#pieceName = "Queen-Bohemian_Rhapsody"
#pieceName = "Queen-Bohemian_Rhapsody_Voice"
#pieceName = "La_La_Land-City_Of_Stars"
#pieceName = "Queen-I_want_to_break_free"
#pieceName = "Lady_Gaga-Bad_Romance"
#pieceName = "Lady_Gaga-Poker_Face"
#pieceName = "Amazing_Grace"
#pieceName = "Super_Mario_Bros.-Main_Theme"
#pieceName = "Get_Lucky-Daft_Punk"

if(len(sys.argv)>0):
	pieceName = sys.argv[1]
else:
	print("You need to give the name of the piece as an argument to this function. \nFor that, type the file name in the terminal, followed by a space and then the name of the song file (without xml extension)")

tree = ET.parse("MusicXML parts/" + pieceName + '.xml')
root = tree.getroot()

# Print info on different parts
title = pieceName.replace("_", " ")
title = title.replace("-", " - ")
print("\n### " + title + " ###\n")
partList = root.findall("./part-list/score-part")
nbParts = 0
print("List of parts in this song : ")
for part in partList:
    nbParts+=1
    print("  "+part.tag, part.attrib, part.find('./part-name').text)

sys.argv[0]


fig = plt.figure(figsize=(20,5*nbParts))
fig.suptitle(title, fontsize=16)


print("\nProcessing " + str(nbParts) + " part·s:")
for partID in range(1,nbParts+1):
    print("  Part "+str(partID)+"...", end='')
    freqArray = u.getFreqArray(root, pieceName, "P"+str(partID))
    #u.printSimMatrices(freqArray, partList[partID-1].find("./part-name").text, fig, partID, nbParts, 5)
    u.printSimMatrixAndSimple(freqArray, partList[partID-1].find("./part-name").text, fig, partID, nbParts)
    print(" Done!")

figPath = "./PNG/" + pieceName + ".png"
plt.savefig(figPath)
print("\nYou can find the result at " + figPath)



