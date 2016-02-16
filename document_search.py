#! /usr/bin/env python
import argparse

kPow = 2

def isEndDelimeter(c):
    return c == '.' or c == '?' or c == '!' or c == ':'


def main(filepath, s):
    with open(filepath, 'r') as fd:
        t = fd.read()
        t = t.replace('\n', ' ')

    if len(t) < len(s):
        return

    s = s.lower()
    len_s = len(s)
    
    #Compute hash of search string and beginning window of text
    lastEndIndex = -1
    h_s = 0
    h_t = 0
    for i in range(len_s):
        h_s *= kPow
        h_s += ord(s[i].lower())
        h_t *= kPow
        h_t += ord(t[i].lower())

    #Case we have a match right in the first window, now we perform a str cmp
    found = h_s == h_t and s == t[i - len_s + 1 : i + 1].lower()

    for i in range(len_s, len(t)):
        #Update rolling hash in window
        h_t -= (ord(t[i - len_s].lower())) * kPow**(len_s - 1)
        h_t *= kPow
        h_t += ord(t[i].lower())

        #Case we have a match in the current window, now we perform a str cmp
        if h_s == h_t and s == t[i - len_s + 1 : i + 1].lower():
            found = True

        #Found end of a sentence, so print out if we found a match anywhere within
        if isEndDelimeter(t[i]):
            if found:
                print '* ' + t[lastEndIndex + 1 : i + 1].strip()
                found = False
            lastEndIndex = i


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search a document for text.')
    parser.add_argument('filepath', help='Path to the document to search in.')
    parser.add_argument('word', help='Word to search for in document')
    args = parser.parse_args()
    main(args.filepath, args.word)

