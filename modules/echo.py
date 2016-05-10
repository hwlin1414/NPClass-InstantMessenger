def main(lines):
    return ('server', lines)
    
def server(attr, args):
    return ('pr', ' '.join(attr))

def pr(lines, args):
    print lines
