def main(lines):
    return ('server', lines)
    
def server(attr):
    return ('pr', ' '.join(attr))

def pr(lines):
    print lines
