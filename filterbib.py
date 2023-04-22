import re

def getcites(texfile, verbose=False):
    cites = []
    print("Parsing:",texfile+'.tex')
    with open(texfile+'.tex','r',encoding="utf8") as f:
        text = f.read()
        for line in text.split('\n'):
            lin = line.strip()
            newline = ''
            prevchar = '\n'
            for c in lin:
                if c=='%':
                    if prevchar!='\\':
                        break
                prevchar = c
                newline = newline + c
            if len(newline)>7:
                # print(newline)
                cite = re.findall('cite\{(.+?)\}',newline)
                for cit in cite:
                    cis = cit.split(',')
                    for ci in cis:
                        if ci.strip().lower() not in cites:
                            cites.append(ci.strip().lower())
    print(texfile+'.tex Citations:',len(cites))
    if verbose:
        for cite in cites:
                print(' ',len(texfile+'.tex Citations:'),cite)
    return cites

def filtercites(bibfiles, cites, verbose=False):
    bibs = {}
    repstrs = {}
    for bibfile in bibfiles:
        bibs[bibfile] = {}
        with open(bibfile+'.bib', 'r', encoding='utf8') as f:
            text = f.read()
            stringreplacements = re.findall('(@[Ss][Tt][Rr][Ii][Nn][Gg].*)\n',text)
            repstrs[bibfile] = []
            for strrep in stringreplacements:
                strrep = '@string'+strrep[len('@string'):]
                idx = strrep.find('%')
                if idx>=0 and idx<len(strrep):
                    strrep = strrep[:idx].strip()
                idx = strrep.find('(')
                if idx>=0 and idx<len(strrep):
                    strrep = strrep[:idx] + '{' + strrep[idx+1:-1] + '}'
                repstrs[bibfile].append(strrep)
            bibcites = re.findall('@[a-zA-Z]+?\s*?\{\s*?.+?\s*?,\s*?\n',text)
            newtext = text
            for bib in bibcites:
                bibcite = re.findall('@[a-zA-Z]+?\s*?\{\s*?(.+?)\s*?,\s*?\n',bib)
                if bibcite[0].lower() not in cites:
                    continue
                start,end = newtext.split(bib)
                countopen = 0
                countclose = 0
                for i,c in enumerate(end):
                    if c=='{':
                        countopen += 1
                    elif c=='}':
                        countclose += 1
                        if countopen<countclose:
                            tracker = True
                            for bibi in bibs.keys():
                                if bibi==bibfile:
                                    continue
                                if bibcite[0] in bibs[bibi].keys():
                                    tracker = False
                                    print('[',texfile+'.tex',']','Not extracting from',bibfile+'.bib',':',bibcite[0],'already in',bibi+'.bib')
                            if tracker:
                                bibs[bibfile][bibcite[0]] = bib+end[:i+1]
                            break
                            
        print(bibfile+'.bib citation found:',len(bibs[bibfile].keys()))
        if verbose:
            for cite in list(bibs[bibfile].keys()):
                print(' ',len(bibfile+'.bib citation found:'),cite)
    return bibs,repstrs

import sys
import os
if __name__=='__main__':
    texfiles = []
    bibfiles = []
    merge_bib = ''
    print (sys.argv)
    i = 0
    while i<len(sys.argv):
        arg = sys.argv[i]
        if arg.endswith('.bib'):
            if os.path.isfile(arg):
                bibfiles.append(arg[:-4])
            else:
                print('Cannot find bib file:',arg)
        elif arg.endswith('.tex'):
            if os.path.isfile(arg):
                texfiles.append(arg[:-4])
            else:
                print('Cannot find tex file:',arg)
        elif arg in ['-m','--merge-tex']:
            i+=1
            if i<len(sys.argv):
                if sys.argv[i].endswith('.bib'):
                    merge_bib = sys.argv[i]
                else:
                    merge_bib = sys.argv[i]+'.bib'
            else:
                merge_bib = 'texmerged_filter.bib'
            if os.path.isfile(merge_bib):
                a = input("File exists: '"+merge_bib+"'! Overwrite? [Y/n] : ")
                if a.lower()!='y':
                    print("Aborting!")
                    exit(0)
        i+=1
    if len(bibfiles)>0 and len(texfiles)>0:
        print('Tex files:', texfiles)
        print('Bib files:', bibfiles)
        if len(merge_bib)>4:
            print('\n===================')
            allcites = []
            for texfile in texfiles:
                cites = getcites(texfile)
                allcites = list(set(allcites+cites))
            print('[ Merged tex ] Citations:', len(allcites))
            print('-------------------')
            bibs,repstrs = filtercites(bibfiles, allcites)
            print('[ Merged tex ] Output: '+merge_bib)
            with open(merge_bib, 'w', encoding='utf8') as f:
                maxlen = max([len('%%%%%%%% '+texfile+'.tex %%%%%%%%') for texfile in texfiles])
                f.write(('%'*maxlen)+'\n')
                for texfile in texfiles:
                    f.write('%%%%%%%% '+texfile+'.tex '+(' '*(maxlen-len('%%%%%%%% '+texfile+'.tex %%%%%%%%')))+'%%%%%%%%\n')
                f.write(('%'*maxlen)+'\n')
                for bibkey,bibvalue in bibs.items():
                    f.write('\n\n%%%%%%%% '+bibkey+'.bib %%%%%%%%\n\n')
                    f.write(('\n'.join(list(set(repstrs[bibkey]))))+'\n\n')
                    f.write('\n\n'.join(list(bibvalue.values())))
                    f.write('\n\n%%%%%%%% '+bibkey+'.bib %%%%%%%%\n\n')
            print('===================\n')
        else:
            for texfile in texfiles:
                print('\n===================')
                cites = getcites(texfile)
                print('-------------------')
                bibs,repstrs = filtercites(bibfiles, cites)
                print('[ '+texfile+'.tex ] Output: '+texfile+'_filter.bib')
                with open(texfile+'_filter.bib', 'w', encoding='utf8') as f:
                    f.write(('%'*len('%%%%%%%% '+texfile+'.tex %%%%%%%%'))+'\n')
                    f.write('%%%%%%%% '+texfile+'.tex %%%%%%%%\n')
                    f.write(('%'*len('%%%%%%%% '+texfile+'.tex %%%%%%%%'))+'\n')
                    for bibkey,bibvalue in bibs.items():
                        f.write('\n\n%%%%%%%% '+bibkey+'.bib %%%%%%%%\n\n')
                        f.write(('\n'.join(list(set(repstrs[bibkey]))))+'\n\n')
                        f.write('\n\n'.join(list(bibvalue.values())))
                        f.write('\n\n%%%%%%%% '+bibkey+'.bib %%%%%%%%\n\n')
                print('===================\n')
    else:
        if len(bibfiles)<1:
            print("No Input tex files")
        if len(texfiles)<1:
            print("No Input bib files")
        print("Usage:")
        print("$ python filterbib.py <texfile_1.tex> ... <texfile_n.tex> <bibfile_1.bib> ... <bibfile_n.tex>")
        print("     [ -m/--merge-tex <texmerged_filter.bib> ]")
        