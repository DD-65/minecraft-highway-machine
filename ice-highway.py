import random
import subprocess, platform
commands=[]
# standard-bau-blöcke
global buildingblock, lightingblock
buildingblock = "quartz_block"
lightingblock = "glowstone"
def settings():
    global buildingblock, lightingblock
    wahl = str(input("Sollen Standardeinstellungen verwendet werden? (Y/N):"))
    if wahl=="N" or wahl=="n":
        eingabebau = str(input("Baublock? BlockID, leer lassen für Standard:"))
        if eingabebau != "" and eingabebau != " ":
            buildingblock = eingabebau
        eingabelicht = str(input("Beleuchtungsblock? BlockID, leer für Standard:"))
        if eingabelicht != "" and eingabelicht != " ":
            lightingblock = eingabelicht
    
    
    else:
        pass

# INITIALISIEREN
def initialisierung():
    global xstart, ystart, zstart, xziel, yziel, zziel, punkt1, punkt2
    settings()
    punkt1=str(input("Startkoordinaten im Format XXX YYY ZZZ (ACHTUNG: Richtige y-Koordinate!!!!):"))
    koords=punkt1.split(sep=" ")
    try:
        # konvertieren der eingegebenen Koordinaten zu int
        xstart=int(koords[0])
        ystart=int(koords[1])
        zstart=int(koords[2])
    except ValueError:
        # keine/ungültige Koordinaten
        print("Koordinaten ungültig.")
        initialisierung()
    punkt2=str(input("Zielkoordinaten im Format XXX YYY ZZZ; - für gleiche Koordinaten:"))
    koords2=punkt2.split(sep=" ")
    try:
        # konvertieren der eingegebenen ZielKoordinaten zu int
        if koords2[0]=="-":
            xziel=xstart
        else:
            xziel=int(koords2[0])
        if koords2[1]=="-":
            yziel=ystart
        else:
            yziel=int(koords2[1])
        if koords2[2]=="-":
            zziel=zstart
        else:
            zziel=int(koords2[2])
    except ValueError:
        # keine/ungültige Koordinaten
        print("Koordinaten ungültig.")
        initialisierung()

if __name__=="__main__":
    initialisierung()

#richtung
xrichtung,zrichtung= (False, False)
if xstart==xziel and zstart !=zziel:
    xrichtung=True
elif zstart==zziel and xstart!=xziel:
    zrichtung=True
elif zstart!=zziel and xstart!=xziel or ystart!=yziel:
    print("Koordinaten ungültig, nur gerade Highways möglich.")
    initialisierung()

#COMMANDS
#PLATZ FREIMACHEN
if xrichtung == True:
    von = "{} {} {}".format(xstart + 2, ystart + 3, zstart)
    bis = "{} {} {}".format(xziel - 2, yziel, zziel)
    command="/fill {von} {bis} air".format(**locals())
    commands.append(command)
else:
    von = "{} {} {}".format(xstart, ystart + 3, zstart + 2)
    bis = "{} {} {}".format(xziel, yziel, zziel - 2)
    command="/fill {von} {bis} air".format(**locals())
    commands.append(command)

#EIS
von=punkt1
bis=punkt2
command="/fill {von} {bis} blue_ice".format(**locals())
commands.append(command)

#QUARZ-WÄNDE
if xrichtung==True:
    #erste wand
    von = "{} {} {}".format(xstart + 2, ystart + 2, zstart)
    bis = "{} {} {}".format(xziel + 2, yziel, zziel)
    command="/fill {von} {bis} {buildingblock}".format(**locals())
    commands.append(command)
    #zweite wand
    von = "{} {} {}".format(xstart - 2, ystart + 2, zstart)
    bis = "{} {} {}".format(xziel - 2, yziel, zziel)
    command="/fill {von} {bis} {buildingblock}".format(**locals())
    commands.append(command)
else:
    #erste wand
    von = "{} {} {}".format(xstart, ystart + 2, zstart + 2)
    bis = "{} {} {}".format(xziel, yziel, zziel + 2)
    command="/fill {von} {bis} {buildingblock}".format(**locals())
    commands.append(command)
    #zweite wand
    von = "{} {} {}".format(xstart, ystart + 2, zstart - 2)
    bis = "{} {} {}".format(xziel, yziel, zziel - 2)
    command="/fill {von} {bis} {buildingblock}".format(**locals())
    commands.append(command)

#DECKE
#quarz
if xrichtung==True:
    von = "{} {} {}".format(xstart + 1, ystart + 3, zstart)
    bis = "{} {} {}".format(xziel - 1, yziel + 3, zziel)
else:
    von = "{} {} {}".format(xstart, ystart + 3, zstart - 1)
    bis = "{} {} {}".format(xziel, yziel + 3, zziel + 1)
command="/fill {von} {bis} {buildingblock}".format(**locals())
commands.append(command)
#glowstone
von = "{} {} {}".format(xstart, ystart + 3, zstart)
bis = "{} {} {}".format(xziel, yziel + 3, zziel)
command="/fill {von} {bis} {lightingblock}".format(**locals())
commands.append(command)

##ALLES IN EINEN COMMAND
grosser_command="""/summon falling_block ~ ~2 ~ {Time:1,BlockState:{Name:"command_block"},TileEntityData:{auto:1,Command:"%s}"}""" % (commands[0])
letzter_command=""",Passengers:[{id:"armor_stand",Health:0,Passengers:[{id:"falling_block",Time:1,BlockState:{Name:"command_block"},TileEntityData:{auto:1,Command:"fill ~ ~%s ~ ~ ~ ~ air"}}""" % (-(len(commands)+1))
counter=1

def zwischencommand(befehl):
    text=""",Passengers:[{id:"armor_stand",Health:0,Passengers:[{id:"falling_block",Time:1,BlockState:{Name:"command_block"},TileEntityData:{auto:1,Command:"%s"}""" % (befehl)
    return text

if len(commands)>1:
    for command in commands:
        text=zwischencommand(command)
        grosser_command=grosser_command+text
    grosser_command=grosser_command+letzter_command
else:
    grosser_command=grosser_command+letzter_command

for i in range(0, len(commands)*2):
    grosser_command=grosser_command+"]}"
grosser_command+="]}]}"

system = platform.system()

if system == 'Darwin':  # MacOS
    subprocess.run("pbcopy", text=True, input=text, check=True)
elif system == 'Linux':  # Linux
    subprocess.run("xclip", input=text, check=True)
elif system == 'Windows':  # Windows
    subprocess.run("clip", input=text, check=True)
else:
    raise OSError(f"Unsupported operating system: {system}")
"""
summon falling_block ~ ~2 ~ {Time:1,BlockState:{Name:"command_block"},TileEntityData:{auto:1,Command:"say 1"}
,Passengers:[{id:"armor_stand",Health:0
,Passengers:[{id:"falling_block",Time:1,BlockState:{Name:"command_block"},TileEntityData:{auto:1,Command:"say 2"}
,Passengers:[{id:"armor_stand",Health:0
,Passengers:[{id:"falling_block",Time:1,BlockState:{Name:"command_block"},TileEntityData:{auto:1,Command:"say 3"}
,Passengers:[{id:"armor_stand",Health:0
,Passengers:[{id:"falling_block",Time:1,BlockState:{Name:"command_block"},TileEntityData:{auto:1,Command:"fill ~ ~-3 ~ ~ ~ ~ air"}}]}]}]}]}]}]}
"""