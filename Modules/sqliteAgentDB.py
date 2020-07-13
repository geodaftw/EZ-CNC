#!/usr/bin/python3

import sqlite3
import os
import random
import string

# Agent Variable
AGENT1 = "agent1"
WRONGID = "abcd1234"
RIGHTID = "a1b2c3d4"


def RandomAgentID(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

def CreateDB():
    print()
    if os.path.exists("ezcnc.db") is True:
        print("Yup, its here!")
        print("Creating a 'AGENT' table if not exists..")
        conn = sqlite3.connect('ezcnc.db')
        c = conn.cursor()
        c.execute('''
                CREATE TABLE IF NOT EXISTS AGENT
             (AGENTID STRING PRIMARY KEY     ,
             NAME           TEXT    NOT NULL,
             PORT            INT     NOT NULL
             )''')

        print("Table 'AGENT' created successfully")
    else:
        print("Nope, not here")
        # Create the database
        #conn = sqlite3.connect('ezcnc.db')
        #print("ezcnc.db has been created")
    conn.close()

def AddAgent():
    # Currently works, need to add a Port section and verification
    conn = sqlite3.connect('ezcnc.db')
    c = conn.cursor()
    randomAgentID = RandomAgentID(8)
    print("Generating random Agent ID: " + randomAgentID)
    agentName = input("Please give the Agent a NAME:\n")
    print("Agents Name will be: " + agentName)
    
    try:
        addPort = int(input("Please give a Port number between 1 and 65535:\n"))
        if 1 <= addPort <= 65535:
            print("Good, thats a valid number")
            print("Adding the following to the database:\n" + \
                    "Agent Name:    " + agentName + "\n" + \
                    "Agent ID:      " + randomAgentID + "\n" + \
                    "Port:          " + str(addPort) + "\n")
            c.execute("INSERT INTO agent (agentid, name, port) VALUES (?,?,?)",(randomAgentID, agentName, addPort))
            conn.commit()
            print("Successfully Added: " + str(agentName))
            c.execute("SELECT * FROM agent WHERE (agentid=? AND name=?)",(randomAgentID, agentName))
            entry = c.fetchall()
            print("Here's the added agent: " + str(entry))
            conn.close()
        else:
            raise ValueError('The number must be in the range of 1 and 65535')
    except ValueError:
        print("Thats not a number or in range! Try again")

def AllDatabaseEntries():
    conn = sqlite3.connect('ezcnc.db')
    c = conn.cursor()
    c.execute("Select * from Agent")
    entry = c.fetchall()
    print("All entries")
    print(*entry, sep="\n")
    conn.close()

def DeleteAllEntries():
    conn = sqlite3.connect('ezcnc.db')
    c = conn.cursor()
    c.execute("DELETE FROM agent")
    print("Deleting all entries..")
    print(c.rowcount)
    print("We have deleted " + str(c.rowcount) + " records from AGENT table")
    conn.commit()
    c.execute("Select * FROM agent")
    entry = c.fetchall()
    print("All entries")
    print(*entry, sep="\n")
    conn.close()


def ChangeAgentName():
    conn = sqlite3.connect('ezcnc.db')
    c = conn.cursor()
    c.execute("SELECT name,agentid FROM agent")
    entry = c.fetchall()
    agentList = []
    print("Agent List is: " + str(entry))
    # THIS APPEND TO LIST WORKS
    for row in entry:
        agentList.append(row[0]) # Need to figure out how to get primary key from this
    # Print list in new line
    print(*agentList, sep = "\n") 
    change = input("Please change the agents name\n")
    if change in agentList:
        print("Yes, that is a valid agent name")
        update = input("What do you want it updated to?\n")
        # run a "select * from agent where name=change
        c.execute("SELECT agentid FROM agent WHERE (name=?)",(change,))
        entry = c.fetchall()
        if len(entry) > 1:
            print("There's 2 or more")
            duplicateList = []
            for row in entry:
                #print(row[0])
                duplicateList.append(row[0])
            print(*duplicateList, sep = "\n")
            
            duplicateUpdate = input("Which Primary Key from " + change + " ?\n")
            
            if duplicateUpdate in duplicateList:
                print("Yes, that's valid")
                verify = input("Do you want to update " + change + "(" + duplicateUpdate + ") to " + update + "?\nType 'yes' or 'no'\n")
                if verify == 'yes':
                    print("OKAY! Updating")
                    c.execute("UPDATE agent SET name='" + update + "' WHERE (agentid=?)", (duplicateUpdate,)) # Note the single ' around update
                    conn.commit()
                    print("Complete, here's all the entries now")
                    c.execute("SELECT * FROM agent")
                    entry = c.fetchall()
                    print(*entry, sep="\n")
                    conn.close()
                else:
                    print("NOPE, WONT DO IT")
                    conn.close()
            else:
                print("NOT VALID")
                conn.close()
        else:
            print("There's only 1")
            verify = input("Do you want to update " + change + " to " + update + "?\nType 'yes' or 'no'\n")
            if verify == 'yes':
                print("OKAY! Updating")
                c.execute("SELECT agentid FROM agent WHERE (name=?)",(change,))
                entry = c.fetchone()
                entryClean = str(entry[0])
                print(entryClean)
                c.execute("UPDATE agent SET name= " + "'" + update + "'" + " WHERE (agentid=?)", (entryClean,))
                conn.commit()
                print("Complete, here's all the entries now")
                c.execute("SELECT * FROM agent")
                entry = c.fetchall()
                print(*entry, sep="\n")
                conn.close()
            else:
                print("NOPE, WONT DO IT")
                conn.close()
    else:
        print("That is an invalid agent name")
        conn.close()

    ### WORKING ON THIS

def CheckAgent():
    print()
    conn = sqlite3.connect('ezcnc.db')
    c = conn.cursor()
    print("Table 'AGENT' created successfully")
    
    print("Let's print all entries..")
    c.execute("Select * from agent")
    rows = c.fetchall()
    print(rows)
    
    print("Checking if entry exists in 'AGENT'")

    c.execute("SELECT * FROM agent WHERE (name=? AND agentid=?)",(AGENT1, RIGHTID))
    entry = c.fetchone()
    #print("Entry is: " + str(entry))
    
    if entry is None:
        print("No entry found")
        print("Adding entry..")
        c.execute("INSERT INTO agent (name, port, agentid) VALUES (?,?,?)",(AGENT1, '8080', RIGHTID))
        conn.commit()
        print("Successfully added")
        print("Let's retrieve..")
        c.execute("SELECT * FROM agent WHERE (name=? AND port=?)",(AGENT1, '8080'))
        entry = c.fetchone()
        print(entry)
    
    else:
        print("Entry found")
        print("Entry is..")
        c.execute("SELECT * FROM agent WHERE (name=? AND port=?)", (AGENT1, '8080'))
        entry = c.fetchone()
        print(str(entry))
        print("Attemping wrong id..")
        c.execute("SELECT * FROM agent WHERE (name=? AND agentid=?)", (AGENT1, WRONGID))
        entry = c.fetchone()
        print("WRONG ID: " + str(entry))

    conn.close()


#CreateDB()
#CheckAgent()
