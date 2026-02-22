import pickle
import random
import time

scorefile = open("scorefile.bin", "rb+")
old_H_score = pickle.load(scorefile)

#Maps
maps = open("Maps II.bin", "rb")

france = pickle.load(maps)
kursk = pickle.load(maps)
ardennes = pickle.load(maps)
stalingrad = pickle.load(maps)
vietnam = pickle.load(maps)
place_dict = [ardennes, stalingrad, france, vietnam, kursk]
#Maps


#Units
unitfile = open("Units II.bin", "rb")

unit_health = pickle.load(unitfile)
unit_h = pickle.load(unitfile)
units = pickle.load(unitfile)

#Units

place = random.choice(place_dict)

abonus = 0; bbonus = 0

dashline = "-------------------------------\n"
d_dashline = "================================"
line = "-------------------------------"

# Functions ----------------------------------------------
def rank_sys(scor):
    r_name = ""
    r = ""

    if scor < 100:
        r_name = "2nd  Lt "
        r = " * "
    elif scor < 150:
        r_name = " 1st  Lt "
        r = "** "
    elif scor < 250:
        r_name = "Captain "
        r = "***"
    elif scor < 500:
        r_name = " Major  "
        r = "-  "
    elif scor < 1000:
        r_name = "Colonel "
        r = "-- "
    elif scor < 2500:
        r_name = "Maj Gen "
        r = "|  "
    elif scor < 4000:
        r_name = "Lt. Gen "
        r = "|| "
    elif scor < 10000:
        r_name = " General  "
        r = "|||"
    else:
        r_name = "  Marshall  "
        r = "X"
    return r_name, r


def input_units(a, n):
    entry = a.upper().split()
    for i in entry:
        if i not in units:
            print("Incorrect Entry")
    if len(entry) != n:
        print("Enter", n, "units only")
    team = [units[key] for key in entry]
    return team


def homescreen():
    print("\n=========================================\n"
          "========== Battle Genius ==========\n"
          "=============================")

    user_input = input("\n\n"
                       "H ------- Check High Score\n"
                       "P ------ Check Player List\n"
                       "Z ------ Play Game (Guest)\n"
                       "X ------ Play Game (Login)\n"
                       "N --------- Create Account\n"
                       "Q ------------------- Quit\n\n")
    return user_input


def unit_hp(x, place):
    total = unit_health[x] + place[x]
    return total


def check_id(pid):
    database = open("Player Database.bin", "rb+")
    database.seek(0)
    try:
        while True:
            player = pickle.load(database)
            if player[0] == pid:
                    return False

    except EOFError:
        return True

    finally:
        database.close()

def update_score(pid, bonus):
    database = open("Player Database.bin", "rb")
    database.seek(0)
    players = []
    while True:
        try:
            player = pickle.load(database)
            players.append(player)
        except EOFError:
            break
    database.close()

    for a in players:
        if a[0] == pid:
            print("ID: ", pid)
            time.sleep(0.5)
            print("Name: ", a[2])
            print("Score [PREVIOUS]: ", a[4])
            time.sleep(0.5)
            a[4] += bonus
            print("Score [UPDATED]: ", a[4])

            database = open("Player Database.bin", "wb")
            for p in players:
                pickle.dump(p, database)
            database.close()


def save_score(Player_name, Player_score):
    scorefile = open("scorefile.bin", "wb")
    new_h_score = [Player_name, Player_score]
    pickle.dump(new_h_score, scorefile)
    scorefile.close()


def verify_account(id, pw):
    database = open("Player Database.bin", "rb")
    database.seek(0)
    try:
        while True:
            player = pickle.load(database)
            if player[0] == id:
                if player[1] == pw:
                    time.sleep(1)
                    return player[2], 0
                else:
                    return "Wrong Password", 1
    except EOFError:
        return "ID Not Found", 2

    finally:
        database.close()

# Functions ----------------------------------------------


# Game ---------------------------------------------------


user_input = homescreen()

if user_input.upper() == "Z":
    time.sleep(0.5)
    pln = input("\nPlayer I |\nEnter Name: ")
    time.sleep(1)

    pln2 = input("\nPlayer II |\nEnter Name: ")
    time.sleep(1)


    print("\n\nGame Type:\nBlitz [ 3 Units / Player ] ---------- B")
    time.sleep(0.5)
    print("Operation [ 5 Units / Player ] ------ O")
    time.sleep(0.5)
    print("Campaign [ 8 Units / Player ] ------- C")
    time.sleep(0.5)
    print("Total War [ 12 Units / Player ] ----- T")
    print("=======================================")
    typ = input()

    if typ.upper() == "B":
        n = 3
    elif typ.upper() == "O":
        n = 5
    elif typ.upper() == "C":
        n = 8
    elif typ.upper() == "T":
        n = 12
    else:
        print("Invalid Input")

    print('\nSalute', pln.upper(), "&", pln2.upper(), "\nWelcome To The Game")
    print(d_dashline)

    time.sleep(1)

    print("\nHere is the list of available unit types:\n")
    time.sleep(2)
    print("Key | Health | Unit")
    print(line)
    for k in units:
        print(k, "  |  ", unit_h[k], "  |  ", units[k])
        time.sleep(0.5)
    print(dashline)

    time.sleep(2)

    print("Map :", place["place"])

    time.sleep(2)

    print("\n", pln.upper(), "|")
    time.sleep(1)
    print("Create Your Army |\nType keys of", n, " units: ")
    inpa = input()
    print(d_dashline)
    time.sleep(2)

    print("\n", pln2.upper(), "|")
    time.sleep(1)
    print("Create Your Army |\nType keys of", n, " units: ")
    inpb = input()
    print(d_dashline)
    time.sleep(2)

    ateam = input_units(inpa, n)
    bteam = input_units(inpb, n)

    print("\n---- | Battle Round Initiated | ----\n")
    time.sleep(1)
    print("Each Player Chooses A Unit ---------")

    while n != 0:
        print("\n", pln, "|", abonus)
        time.sleep(1)
        print("Your Units:", ' | '.join(ateam))
        print(line)
        x = input()
        if units[x.upper()] not in ateam:
            print("This unit was not selected")
            pass
        else:
            used_unita = units[x.upper()]
            ateam.remove(used_unita)
            # Calculating The Final Unit HP ----------
            atotal_hp = unit_hp(used_unita, place)
            print(used_unita, "HP : ", atotal_hp)
            time.sleep(0.5)
            print(d_dashline)
            time.sleep(3)

            print("\n\n", pln2, "|", bbonus)
            time.sleep(1)
            print("Your Units:", ' | '.join(bteam))
            print(line)
            x = input()
            if units[x.upper()] not in bteam:
                print("This unit was not selected")
                pass
            else:
                used_unitb = units[x.upper()]
                bteam.remove(used_unitb)
                # Calculating The Final Unit HP ----------
                btotal_hp = unit_hp(used_unitb, place)
                print(used_unitb, "HP : ", btotal_hp)
                time.sleep(0.5)
                print(d_dashline)
                time.sleep(3)

                if atotal_hp > btotal_hp:
                    diff = atotal_hp - btotal_hp
                    print("\n",pln, "Wins By", diff, "Points!")
                    abonus += diff
                    n -= 1
                    print("-------------------------------------\n")

                if btotal_hp > atotal_hp:
                    diff = btotal_hp - atotal_hp
                    print("\n",pln2, "Wins By\n", diff, "Points!")
                    bbonus += diff
                    n -= 1
                    print("-------------------------------------\n")

                if btotal_hp == atotal_hp:
                    print("======== Stalemate ========")
                    n -= 1
    else:
        print("\n\n---- | Battle Round Ends | ----\n")
        time.sleep(1)
        print("Player Name: ", pln)
        time.sleep(0.5)
        print("Total Score : ", abonus)
        print(dashline)
        time.sleep(1.5)
        print("Player Name: ", pln2)
        time.sleep(0.5)
        print("Total Score : ", bbonus)
        print(dashline)
        time.sleep(1.5)

        if abonus > bbonus:
            print(d_dashline)
            time.sleep(0.2)
            print(pln, "Wins!")
            time.sleep(0.2)
            print(d_dashline)
            time.sleep(1)


            if abonus > old_H_score[1]:
                scorefile.close()
                input("\nPress Enter ----------- Save Your Score")
                save_score(pln, abonus)

        if abonus < bbonus:
            print(d_dashline)
            time.sleep(0.2)
            print(pln2, "Wins!")
            time.sleep(0.2)
            print(d_dashline)
            time.sleep(1)


            if bbonus > old_H_score[1]:
                scorefile.close()
                input("\nPress Enter ----------- Save Your Score")
                save_score(pln2, bbonus)

        if abonus == bbonus:
            print("--------- Draw ---------")

        print("\nPrevious High Score: ", old_H_score[1], "by", old_H_score[0])


    m = input("\nX ----------- Quit: ")
    if m.upper() == "X":
        pass


if user_input.upper() == "N":
    time.sleep(1)
    pname = input("Account Name: ")

    Unique_id = True
    while Unique_id == True:
        pid = input("Unique 3-letter ID: ")
        if check_id(pid) == False:
            Unique_id = True
            time.sleep(1)
            print("ID | Already In use")
        else:
            Unique_id = False
            time.sleep(1)
            print("ID | Accepted")


    p_score = 0
    time.sleep(1)

    pw = input("Create Password: ")

    rank, sign = rank_sys(p_score)
    time.sleep(1)

    print("\nAccount Creation Successful\n")
    print("| ID: ", pid)
    time.sleep(0.5)
    print("| Name: ", pname)
    time.sleep(0.5)
    print("| Rank: ", rank)

    N_player = [pid, pw, pname, rank, p_score]
    database = open("Player Database.bin", "ab+")
    pickle.dump(N_player, database)
    database.close()
    time.sleep(1)

    user_input = homescreen()


if user_input.upper() == "Q":
    pass

if user_input.upper() == "P":
    database = open("Player Database.bin", "rb")

    print("      Rank        |  ID   | Score |    Name    \n")
    try:
        while True:
            PL = (pickle.load(database))
            player_sc = PL[4]
            r_name, r_s = rank_sys(player_sc)
            print(r_s, r_name, r_s, " | ", PL[0], " | ", PL[4], " | ", PL[2])
            time.sleep(0.5)

    except EOFError:
        print()

    finally:
        m = input("\nX ----------- Quit: ")
        if m.upper() == "X":
            pass


if user_input.upper() == "H":
    time.sleep(1)
    print("Previous High Score: ", old_H_score[1], "by", old_H_score[0])

    m = input("\n\nX ----------- Quit")
    if m.upper() == "X":
        pass
    user_input = homescreen()


if user_input.upper() == "X":
    time.sleep(1)
    print("---------- New Game Created ----------")

    time.sleep(1)
    while True:
        pid1 = input("\nPlayer I |\nEnter ID: ")
        time.sleep(1)
        pw1 = input("Enter Password : ")
        time.sleep(0.5)
        Player1, fact = verify_account(pid1, pw1)
        if fact == 0:
            print("\nAccount Confirmed")
            break
        elif fact == 1:
            print("\nInvalid Password")
        elif fact == 2:
            print("\nAccount | Not Found")
        else:
            print("\nError Unknown")

    time.sleep(1)

    while True:
        pid2 = input("\nPlayer II |\nEnter ID: ")
        time.sleep(1)
        pw2 = input("Enter Password : ")
        time.sleep(0.5)
        Player2, fact2 = verify_account(pid2, pw2)
        if fact2 == 0:
            print("\nAccount Confirmed")
            break
        elif fact2 == 1:
            print("\nInvalid Password")
        elif fact2 == 2:
            print("\nAccount | Not Found")
        else:
            print("\nError Unknown")

    print("\n\nGame Type:\nBlitz [ 3 Units / Player ] ---------- B")
    time.sleep(0.5)
    print("Operation [ 5 Units / Player ] ------ O")
    time.sleep(0.5)
    print("Campaign [ 8 Units / Player ] ------- C")
    time.sleep(0.5)
    print("Total War [ 12 Units / Player ] ----- T")
    print("=======================================")
    typ = input()

    if typ.upper() == "B":
        n = 3
    elif typ.upper() == "O":
        n = 5
    elif typ.upper() == "C":
        n = 8
    elif typ.upper() == "T":
        n = 12
    else:
        print("Invalid Input")

    print('\nSalute', Player1.upper(), "&", Player2.upper(), "\nWelcome To The Game")
    print(d_dashline)

    time.sleep(2)

    print("\nHere is the list of available unit types:\n")
    time.sleep(2)
    print("Key | Health | Unit")
    print(line)
    for k in units:
        print(k, "  |  ", unit_h[k], "  |  ", units[k])
        time.sleep(0.5)
    print(dashline)

    time.sleep(2)

    print("Map :", place["place"])

    time.sleep(2)

    print("\n", Player1.upper(), "|")
    time.sleep(1)
    print("Create Your Army |\nType keys of", n, " units: ")
    print(d_dashline)
    inpa = input()
    print(dashline)
    time.sleep(2)

    print("\n", Player2.upper(), "|")
    time.sleep(1)
    print("Create Your Army |\nType keys of", n, " units: ")
    print(d_dashline)
    inpb = input()
    print(dashline)
    time.sleep(2)

    ateam = input_units(inpa, n)
    bteam = input_units(inpb, n)

    print("\n---- | Battle Round Initiated | ----\n")
    time.sleep(1)
    print("Each Player Chooses A Unit ---------")

    while n != 0:
        print("\n", Player1, "|", abonus)
        time.sleep(1)
        print("Your Units:", ' | '.join(ateam))
        print(line)
        x = input()
        if units[x.upper()] not in ateam:
            print("This unit was not selected")
            pass
        else:
            used_unita = units[x.upper()]
            ateam.remove(used_unita)
            # Calculating The Final Unit HP ----------
            atotal_hp = unit_hp(used_unita, place)
            print(used_unita, "HP : ", atotal_hp)
            time.sleep(0.5)
            print(d_dashline)
            time.sleep(3)

            print("\n\n", Player2, "|", bbonus)
            time.sleep(1)
            print("Your Units:", ' | '.join(bteam))
            print(line)
            x = input()
            if units[x.upper()] not in bteam:
                print("This unit was not selected")
                pass
            else:
                used_unitb = units[x.upper()]
                bteam.remove(used_unitb)
                # Calculating The Final Unit HP ----------
                btotal_hp = unit_hp(used_unitb, place)
                print(used_unitb, "HP : ", btotal_hp)
                time.sleep(0.5)
                print(d_dashline)
                time.sleep(3)

                if atotal_hp > btotal_hp:
                    diff = atotal_hp - btotal_hp
                    print("\n",Player1, "Wins By", diff, "Points!")
                    abonus += diff
                    n -= 1
                    print("-------------------------------------\n")

                if btotal_hp > atotal_hp:
                    diff = btotal_hp - atotal_hp
                    print("\n",Player2, "Wins By\n", diff, "Points!")
                    bbonus += diff
                    n -= 1
                    print("-------------------------------------\n")

                if btotal_hp == atotal_hp:
                    print("======== Stalemate ========")
                    n -= 1
    else:
        print("\n\n---- | Battle Round Ends | ----\n")
        time.sleep(1)
        print("Player Name: ", Player1)
        time.sleep(0.5)
        print("Total Score : ", abonus)
        print(dashline)
        time.sleep(1.5)
        print("Player Name: ", Player2)
        time.sleep(0.5)
        print("Total Score : ", bbonus)
        print(dashline)
        time.sleep(1.5)

        if abonus > bbonus:
            print(d_dashline)
            time.sleep(0.2)
            print(Player1, "Wins!")
            time.sleep(0.2)
            print(d_dashline)

            if abonus > old_H_score[1]:
                scorefile.close()
                input("\nPress Enter ----------- Save High Score")
                save_score(Player1, abonus)

        if abonus < bbonus:
            print(d_dashline)
            time.sleep(0.2)
            print(Player2, "Wins!")
            time.sleep(0.2)
            print(d_dashline)

            if bbonus > old_H_score[1]:
                scorefile.close()
                input("\nPress Enter ----------- Save High Score")
                save_score(Player2, bbonus)
        
        if abonus == bbonus:
            print("--------- Draw ---------")

        print("\nPrevious High Score: ", old_H_score[1], "by", old_H_score[0], "\n")

        print(Player1, " |")
        time.sleep(1)
        u = input("Enter S ----------- Update Profile: ")
        if u.upper() == "S":
            print("\n")
            update_score(pid1, abonus)

        print()
        print(Player2, " |")
        time.sleep(1)
        u = input("Enter S ----------- Update Profile: ")
        if u.upper() == "S":
            print("\n")
            update_score(pid2, bbonus)

    m = input("\nX ----------- Quit: ")
    if m.upper() == "X":
        pass
