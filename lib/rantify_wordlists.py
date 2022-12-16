import os

def recurse_wordlists(path):
    result = {}
    for item in os.listdir(path):
        absitem = "{0}/{1}".format(path, item)
        if os.path.isdir(absitem):
            result[item] = recurse_wordlists(absitem)
        elif item[-4:] == ".txt":
            print("reading {0}".format(absitem))
            with open(absitem, encoding="utf8") as file:
                result[item[:-4]] = [line.strip() for line in file]
    
    return result

wordlists = recurse_wordlists("/lib/wordlist")

def render_rant_file(outpath):
    outfile = open(outpath, "w", encoding="utf8")
    outfile.write("<%module = (::)>\n")
    
    def render_list(input):
        return "(: {0} )".format("; ".join(["\"{0}\"".format(inline) for inline in input]))
    
    def recurse_dict(indict, prekey=None):
        for key in indict:
            if prekey:
                fullkey = "{0}/{1}".format(prekey, key)
            else:
                fullkey = key
            
            if type(indict[key]) is list:
                print("rendering wordlist {0}".format(fullkey))
                outfile.write("<module/{0} = {1}>\n".format(fullkey, render_list(indict[key])))
            elif type(indict[key]) is dict:
                outfile.write("<module/{0} = (::)>\n".format(fullkey))
                recurse_dict(indict[key], fullkey)
    
    recurse_dict(wordlists)

    outfile.write("<module>")
    outfile.close()

render_rant_file("/app/rant/wordlist.rant")