import praw
import time

reddit = praw.Reddit(
    client_id = "<CLIENT ID HERE>",
    client_secret = "<CLIENT SECRET HERE>",
    user_agent = "<USER AGENT HERE>",
    )


subreddit = reddit.subreddit("<SUBREDDIT NAME HERE>")

userlist = open("userlist.txt", "a+")
counter = 1

def redditorage(user):
    x = (int(time.time()) - user.created_utc)/31536000 #Approximately 1 year's time in unix
    return x

###
print("*"*80)
print("\n", " "*22, "REDDIT AGE FILTER SCRIPT", "\n", " "*25, "MADE BY KILOBRAVO3", "\n", " "*30, "WELCOME", "\n")
print("*"*80)
###

print("\nREAD BEFORE PROCEEDING!",
    "\n\n* As the userlist.txt file becomes larger and larger, it may take longer and \nlonger for the script to run the entire code.",
    "\n\n* Set the scan limit carefully. Even if your userlist.txt file is empty \ninitially, adding new usernames will make it a big chunk of text and will cause \nlatter scans take much more time than normal.\n"
    )
print("*"*80, "\n")

reqage = int(input("Please set the age limit in months for filtering. Accounts younger than the \nspecified months will be added to userlist.txt --> "))
scanlimit = int(input("\nPlease set a limit for the number of scanned submissions in total --> "))

print("\nRunning the script now... This may take a while, depending on the size of \nuserlist.txt\n")

for submission in subreddit.new(limit=scanlimit):

#Submission Owner Check
    try:    #Using this because deleted submissions may cause AttributeError
        print("*"*50, "\n")
        print("Submission Title: ", submission.title, "(SUBMISSION COUNTER:", counter, "OUT OF", scanlimit, ")")
        print("Submission Author:", submission.author)
        print(" ")
        author = str(submission.author)
        age = redditorage(submission.author)
        MeetsReq = age < reqage/12   #Requirement is the account being younger than specified months(/12 for year value)
        userlist.seek(0)
        InList = author in userlist.read()
        print("MeetsReq =", MeetsReq, "- The account was created", int(age*12), "month(s) ago!")
        print("InList =", InList)
        if MeetsReq:
            if InList:
                print(author, "is already added to the list")
                print("SKIP!", "\n")
            else:
                print("Adding the author to the list...")
                userlist.write("User: " + author + " --- Age In Months: " + str(int(age*12)) + "\n")
                print("DONE!", "\n")
        else:
            print("The user doesn't meet the requirements - The account is created", int(age*12), "month(s) ago!")
            print("SKIP!", "\n")
        counter += 1
    except AttributeError:
        print("The submission is either deleted or removed...")
        print("SKIP!", "\n")
        counter +=1
        
#Comment Owner Check
    comments = list(submission.comments)
    for comment in comments:
        try:    #Using this because deleted submissions may cause AttributeError
            print("*"*50, "\n")
            print("Comment Body:", comment.body)
            print("Comment Author:", comment.author)
            print(" ")
            comauthor = str(comment.author)
            age = redditorage(comment.author)
            MeetsReq = age < reqage/12    #Requirement is being younger than specified months(/12 for year value)
            userlist.seek(0)
            InList = comauthor in userlist.read()
            print("MeetsReq =", MeetsReq, "- The account was created", int(age*12), "month(s) ago!")
            print("InList =", InList)
            if MeetsReq:
                if InList:
                    print(comauthor, "is already added to the list")
                    print("SKIP!", "\n")
                else:
                    print("Adding the author to the list...")
                    userlist.write("User: " + comauthor + " --- Age In Months: " + str(int(age*12)) + "\n")
                    print("DONE!", "\n")
            else:
                print("The user doesn't meet the requirements - The account is created", int(age*12), "month(s) ago!")
                print("SKIP!", "\n")
        except AttributeError:
            print("The submission is either deleted or removed...")
            print("SKIP!", "\n")

userlist.close()

###
print("*"*80)
print("\n", " "*22, "REDDIT AGE FILTER SCRIPT", "\n", " "*25, "MADE BY KILOBRAVO3", "\n", " "*30, "GOODBYE", "\n")
print("*"*80)
###
