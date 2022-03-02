import re


file = open("844ksample.txt", "r")
lines = file.readlines()
f = open("result.txt", "w")
f.close()

for line in lines:
    # if re.match("nan", line):
    #     continue
    if re.match("(.*),(.*)", line):
        matches = re.search("(.*),(.*)", line)
        # print(matches)
        straatnummer = matches.group(1)
        gemeente = matches.group(2)
        # f = open("gemeente.txt", "a")
        # f.write(str(gemeente.strip())+"\n")
        # f.close()
        print(gemeente)


        if re.match("(^(.*) ([0-9]{3,5}-[0-9]{4}))",gemeente):
            splitted = re.search("(^(.*) ([0-9]{3,5}-[0-9]{4}))", gemeente)
            city = splitted.group(2)
            postalcode = splitted.group(3)
            print(gemeente + ": "+ "(gemeente: "+ city + ")")
            f = open("result.txt", "a")
            f.write(str(gemeente.strip() + ": "+ "(gemeente: "+ city + " postcode: "+postalcode+")\n"))
            f.close()

        # specifiek voor Nederland
        elif re.match("(^([0-9]{4} [A-Z]{2}) (.*))", gemeente):
            splitted = re.search("(^([0-9]{4} [A-Z]{2}) (.*))", gemeente)
            city = splitted.group(3)
            postalcode = splitted.group(2)
            print(gemeente + ": "+ "(gemeente: "+ city + ")")
            f = open("result.txt", "a")
            f.write(str(gemeente.strip() + ": "+ "(gemeente: "+ city.strip() + "; postcode: "+postalcode.strip()+")\n"))
            f.close()

        # US, Belgie, Duitsland format 1
        elif re.match("((^[0-9]{4,5}) (.*))", gemeente):
            splitted = re.search("((^[0-9]{4,5}) (.*))", gemeente)
            city = splitted.group(3)
            postalcode = splitted.group(2)
            print(gemeente + ": "+ "(gemeente: "+ city + ")")
            f = open("result.txt", "a")
            f.write(str(gemeente.strip() + ": "+ "(gemeente: "+ city.strip() + "; postcode: "+postalcode.strip()+")\n"))
            f.close()

        # US, Belgie, Duitsland format 2
        elif re.match("(^(.*) [0-9]{4,5})", gemeente):
            splitted = re.search("(^(.*) ([0-9]{4,5}))", gemeente)
            # print(splitted)
            # print(splitted.groups())
            city = splitted.group(2)
            postalcode = splitted.group(3)
            print(gemeente + ": "+ "(gemeente: "+ city + ")")
            f = open("result.txt", "a")
            f.write(str(gemeente.strip() + ": "+ "(gemeente: "+ city.strip() + "; postcode: "+postalcode.strip()+")\n"))
            f.close()