# -*- coding: utf-8 -*-
import os
from os import path
import csv
import collections
import operator
import math
from operator import itemgetter
import time
import sys
from collections import defaultdict
start = time.time()
def search_collocations(folder, pos1, pos2):
    colocdict = []
    for filename in os.listdir(folder):
        if filename.endswith('.parsed'):
            # print('File loaded')
            file_path = path.relpath(folder + '/' + filename)
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                wordreader = csv.reader(csvfile, delimiter='	')
                workspace = []
                for row in wordreader:
                    if row:
                        workspace.append(row)
                    else:
                        # iterator(row, workspace, 2, pos, adjectives, listcount, 0)
                        for row in workspace:
                            if row[4] == pos1:
                                for difrow in workspace:
                                    if row[6] == difrow[0]:
                                        if difrow[4] == pos2:
                                            templist = row[2] + ' ' + difrow[2]
                                            colocdict.append(templist)
                        del workspace[:]
    csvfile = 'data_coloc.csv'
    with open(csvfile, "w", encoding='UTF-8') as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in colocdict:
            writer.writerow([val])
    #colocdict = ListToFreqDict(colocdict)
    #colocdict = [ "%s %s" % x for x in colocdict ]
    return colocdict
def ListToFreqDict(wordlist):
	wordfreq = [wordlist.count(p) for p in wordlist]
	freqmetric = [x  for x in wordfreq]
	perem = zip(wordlist,freqmetric)
	perem = list(perem)
	return perem
def fastcounter():
    data = [line.strip().split(';') for line in open('data.csv', 'r', encoding='utf8').readlines()]
    wordfreq = {}
    for a in data:
        for word in a:
            if word in wordfreq:
                wordfreq[word]+=1
            else:
                wordfreq[word]=1
    for c1 in data:
        counter = 0
        for c2 in data:
            if c2[0] == c1[0] and c2[1] == c1[1]:
                counter += 1
        c1.append(counter)
    err = 0
    file = open('result.csv', 'w', encoding='utf8')
    for colloc in data:
            try:
                file.write('%s %s;%d;%d;%d \n' % (colloc[0], colloc[1], wordfreq[colloc[0]], wordfreq[colloc[1]], colloc[2]))
            except:
                err += 1
            print(err)
def count_all(dict):
    print('starting counting shit...')
    newdict = []
    secondict = []
    for key in dict:
        counter = 0
        iteree = key.split()[0]
        for key in dict:
            if iteree == key.split()[0]:
                counter +=1
        newdict.append(iteree+' '+str(counter))
    newdict = list(set(newdict))
    dict = list(set(dict))
    for key in dict:
        for iteree in newdict:
            if iteree.split()[0] == key.split()[0]:
                key = key+' '+iteree.split()[1]
                secondict.append(key)
    print('yay!starting counting another frequency')
    thirdict = []
    fourthdict = []
    for key in dict:
        counter = 0
        iteree = key.split()[1]
        for key in dict:
            if iteree == key.split()[1]:
                counter += 1
        thirdict.append(iteree + ' ' + str(counter))
    thirdict = list(set(thirdict))
    dict = list(set(dict))
    for key in secondict:
        for iteree in thirdict:
            if iteree.split()[0] == key.split()[1]:
                key = key + ' ' + iteree.split()[1]
                fourthdict.append(key)
    print('ready b0ss')
    csvfile = 'data.csv'
    with open(csvfile, "w", encoding='UTF-8') as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in fourthdict:
            writer.writerow([val])
    return fourthdict
def search_anything(folder, seedarray, pos):
    adjectives = []
    listcount = 0
    for filename in os.listdir(folder)[:3000]:
        if filename.endswith('.parsed'):
            #print('File loaded')
            file_path = path.relpath(folder + '/' + filename)
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                wordreader = csv.reader(csvfile, delimiter='	')
                workspace = []
                for row in wordreader:
                    if row:
                        workspace.append(row)
                    else:
                        #iterator(row, workspace, 2, pos, adjectives, listcount, 0)
                        for row in workspace:
                            if row[2] in seedarray:
                                for difrow in workspace:
                                    if row[6] == difrow[0]:
                                        if difrow[4] == pos:
                                            adjectives.append(difrow[2])
                                            listcount +=1
                                            print('Adjective FOUND!!!')
                                        else:
                                            for difrow1 in workspace:
                                                if difrow[6] == difrow1[0]:
                                                    if difrow1[4] == pos:
                                                        adjectives.append(difrow1[2])
                                                        listcount += 1
                                                        print('Adjective FOUND FARTHER AWAY')
                                                    else:
                                                        for difrow2 in workspace:
                                                            if difrow1[6] == difrow2[0]:
                                                                if difrow1[4] == pos:
                                                                    adjectives.append(difrow2[2])
                                                                    listcount += 1
                                                                    print('Adjective FOUND!!!SHIIIIEET THAT FAR?')
                        del workspace[:]
    print(adjectives)
    return adjectives
# def iterator(row, workspace, depth, pos, adjectives, listcount, counter):
#     print(counter)
#     counter=counter
#     for row in workspace:
#         if row[2] in seedarray:
#             for difrow in workspace:
#                 if row[6] == difrow[0]:
#                     if difrow[4] == pos:
#                         adjectives.append(difrow[2])
#                         listcount += 1
#                         print(difrow[2])
#                         print('Adjective FOUND!!!')
#                     else:
#                         while counter < depth:
#                             counter +=1
#                             iterator(difrow, workspace, depth, pos, adjectives, listcount, counter)
def sortFreqDict(freqdict):
	aux = sorted(freqdict,key=(lambda item: item[1]), reverse=True)
	#aux = sorted(aux,key=lambda item: item[0])
	return aux
def countall(folder,seedarray):
    counter = 0
    for filename in os.listdir(folder)[:3000]:
        if filename.endswith('.parsed'):
            # print('File loaded')
            file_path = path.relpath(folder + '/' + filename)
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                wordreader = csv.reader(csvfile, delimiter='	')
                for row in wordreader:
                    if row:
                        for i in seedarray:
                            if row[2] in seedarray:
                                counter +=1
    print(counter)
    return counter
def countarray(folder, seedarray):
    valuelist = []
    for i in seedarray:
        counter = 0
        for filename in os.listdir(folder)[:3000]:
            if filename.endswith('.parsed'):
                # print('File loaded')
                file_path = path.relpath(folder + '/' + filename)
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    wordreader = csv.reader(csvfile, delimiter='	')
                    for row in wordreader:
                        if row:
                            if row[2] == i:
                                print(counter)
                                counter +=1
        valuelist.append(counter)
    finaldict = dict(zip(seedarray,valuelist))
    print(finaldict)
    return finaldict
def countallcorpus(folder, pos):
    counter = 0
    for filename in os.listdir(folder)[:3000]:
        if filename.endswith('.parsed'):
            # print('File loaded')
            file_path = path.relpath(folder + '/' + filename)
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                wordreader = csv.reader(csvfile, delimiter='	')
                for row in wordreader:
                    if row:
                        if row[4] == pos:
                            counter += 1
    return counter
seedarray = ['обслуживание','официант','швейцар','метрдотель','сервис','счет','официантка','мальчик','девушка','девочка']
seedadjective =['довольный','ленивый','приветливый','вежливый','отвратительный','фантастический','виноватый','неплохой', 'нормальный','достойный','доброжелательный']
#lsit = search_anything('sentiment_parsed',seedarray, 'A')
#cfreqdict = dict((ListToFreqDict(lsit)))
#carray = list(cfreqdict.keys())
#print(cfreqdict)
#cnfreqdict = countarray('sentiment_parsed',carray)
#print(cnfreqdict)
#print('LOOKABOVE')
#nall = countall('sentiment_parsed', seedadjective)
# отсюда вычесть частоту
def extract_dict(path):
    with open(path, mode='r', encoding='UTF-8') as infile:
        wordreader = csv.reader(infile, delimiter=';')
        mydict = {rows[0]+' '+rows[1]: rows[2]+' '+rows[3]+' '+rows[4] for rows in wordreader}
    return mydict
def word_search(word, mydict,porog):
    dictionary={}
    flag = 'adjectives'
    for coloc in mydict.keys():
        coloc = coloc.split()
        if word == coloc[1] and int(mydict[' '.join(coloc)].split(' ')[2]) >=porog:
            flag = 'adjectives'
            dictionary[coloc[0]] = loglike_count_adjective(mydict[' '.join(coloc)])
        if word ==coloc[0] and int(mydict[' '.join(coloc)].split(' ')[2]) >=porog:
            flag = 'aspects'
            dictionary[coloc[1]] = loglike_count_aspect(mydict[' '.join(coloc)])
    top10 = dict(sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)[:10])
    if flag == 'aspects':
        file1 = open('envs/final_result_aspects_LLH.csv', 'a', encoding='utf8')
        err=0
        try:
            file1.write(
                '%s;%s\n' % (word, ','.join(top10.keys()) ))
        except:
            err += 1
        list_of_words = top10.keys()
        return list_of_words
    if flag == 'adjectives':
        file1 = open('envs/final_result_adjectives_LLH.csv', 'a', encoding='utf8')
        err = 0
        try:
            file1.write(
                '%s;%s\n' % (word, ','.join(top10.keys())))
        except:
            err += 1
        list_of_words = top10.keys()
        return list_of_words
def init(list,mydict,porog):
    unique_check = []
    stack = []
    stack.append(list)
    #while True:
    for list1 in stack:
        print('iteration...')
        for word in list1:
            if word not in unique_check:
                tostack = word_search(word,mydict,porog)
                stack.append(tostack)
                unique_check.append(word)
            else:
                print('blank')
        # for list2 in stack_adjectives:
        #     if itercount >= 8:
        #         break
        #     z = {}
        #     print(itercount)
        #     for word in list2:
        #         tostack = word_search(word, mydict, porog)
        #         z.update(tostack)
        #         unique_check.append(word)
        #     top10 = dict(sorted(z.items(), key=operator.itemgetter(1), reverse=True)[:10])
        #     stack_aspects.append(top10)
        #     print(top10)
        #     file2 = open('final_result_aspects_LLH_test.csv', 'a', encoding='utf8')
        #     err = 0
        #     try:
        #         file2.write(
        #                 '%s;%s\n' % (itercount, ','.join(top10.keys())))
        #     except:
        #         err += 1
def loglike_count_adjective(value):
    value = value.split(' ')
    a = int(value[2]) # частота встречаемости сида с этим прилагательным
    b = int(value[1]) - int(value[2]) # частота встречаемости сида со всеми другими прилагательными
    c = int(value[0]) # количество
    d = 193524 - int(value[0]) # количество пригалательных
    E1 = c * (a + b) / (c + d)
    E2 = d * (a + b) / (c + d)
    if b == 0:
        checker = 0
    else:
        checker = (b * math.log(b / E2))
    G2 = 2 * ((a * math.log(a / E1)) + checker)
    return G2
def freq_count_all(value):
    value1 = value.split(' ')
    toreturn = value1[2]
    return(toreturn)
def pmi_count(value):
    value = value.split(' ')
    a = int(value[2] )/193524
    b = int(value[1])/193524
    c = int(value[0])/193524
    return(math.log(a/float(b*c)),2)
def loglike_count_aspect(value):
    value = value.split(' ')
    a = int(value[2]) # частота встречаемости сида с этим прилагательным
    b = int(value[0]) - int(value[2]) # частота встречаемости сида со всеми другими прилагательными
    c = int(value[1]) # количество
    d = 193524 - int(value[1]) # количество пригалательных
    E1 = c * (a + b) / (c + d)
    E2 = d * (a + b) / (c + d)
    if b == 0:
        checker = 0
    else:
        checker = (b * math.log(b / E2))
    G2 = 2 * ((a * math.log(a / E1)) + checker)
    return G2
#loglike_array(cnfreqdict, cfreqdict, carray)
#mydict = extract_dict('cleanresults.csv')
#wordlist = ['обслуживание','официант','швейцар','сервис','счет','официантка','мальчик','девушка','девочка']
#init(wordlist,mydict)
def cleanup(file,name,quantity):
    with open(file, mode='r', encoding='UTF-8') as infile:
        wordreader = csv.reader(infile, delimiter=';')
        mydict = {rows[0]:rows[1] for rows in wordreader}
        cleandict = {k: v for k, v in mydict.items() if len(v.split(',')) >= quantity  }
        writer = csv.writer(open('envs/clean_result_'+name+'.csv', 'w', encoding='UTF-8'), delimiter=';')
        for key, value in cleandict.items():
            writer.writerow([key, value])
#mydict = extract_dict('cleanresults.csv')
#wordlist = ['обслуживание','официант','сервис','счет','официантка','мальчик','девушка','девочка']
# #init(wordlist,mydict,3)
# cleanup('envs/final_result_adjectives_LLH.csv','adjectives_LLH',3)
# cleanup('envs/final_result_aspects_LLH.csv','aspects_LLH',3)
def polarity (file, seed, corpus):
    mydict = {}
    with open(file, mode='r', encoding='UTF-8') as infile:
        wordreader = csv.reader(infile, delimiter=';')
        mydict = {rows[0]: rows[1] for rows in wordreader}
def polarity_append(folder, seed_good, seed_bad, file):
    with open(file, mode='r', encoding='UTF-8') as infile:
        wordreader = csv.reader(infile, delimiter=';')
        aspect = {rows[0]: rows[1] for rows in wordreader}
    newdict = aspect
    for filename in os.listdir(folder):
        if filename.endswith('.parsed'):
            print(filename)
            file_path = path.relpath(folder + '/' + filename)
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                wordreader = csv.reader(csvfile, delimiter='	')
                workspace = []
                for row in wordreader:
                    if row:
                        workspace.append(row)
                    else:
                        for row in workspace:
                            for aspect1 in aspect.keys():
                                if row[2] == aspect1:
                                    for difrow in workspace:
                                        if row[6] == difrow[0]:
                                            if difrow[2] in aspect[aspect1].split(','):
                                                print(difrow[2])
                                                for difdifrow in workspace:
                                                    if row[6] == difdifrow[0] and difdifrow[2] in seed_good:
                                                        print(difdifrow[2]+'OOOOOOOOOOHYEAH')
                                                        newdict[aspect1] = aspect[aspect1].replace(difrow[2],
                                                                                                difrow[2] + '+')
                                                    if row[6] == difdifrow[0] and difdifrow[2] in seed_bad:
                                                        print(difdifrow[2])
                                                        newdict[aspect1] = aspect[aspect1].replace(difrow[2],
                                                                                                difrow[2] + '---')
                                                    if row[6] == difdifrow [0] and difdifrow[2] =='	и	':
                                                        for difdifdifrow in workspace:
                                                            if difdifrow[6] ==difdifdifrow[0] and difdifdifrow[2] in seed_good:
                                                                print(difdifdifrow[2])
                                                                newdict[aspect1] = aspect[aspect1].replace(difrow[2],
                                                                                                difrow[2] + '+')
                                                            if difdifrow[6] == difdifdifrow[0] and difdifdifrow[2] in seed_bad:
                                                                print(difdifdifrow[2])
                                                                newdict[aspect1] = aspect[aspect1].replace(difrow[2],
                                                                                                difrow[2] + '---')
                                                    if row[6] == difdifrow[0] and difdifrow[2] == '	но	':
                                                        for difdifdifrow in workspace:
                                                            if difdifrow[6] == difdifdifrow[0] and difdifdifrow[2] in seed_good:
                                                                print(difdifdifrow[2])
                                                                newdict[aspect1] = aspect[aspect1].replace(difrow[2],
                                                                                                difrow[2] + '---')
                                                            if difdifrow[6] == difdifdifrow[0] and difdifdifrow[2] in seed_bad:
                                                                print(difdifdifrow[2])
                                                                newdict[aspect1] = aspect[aspect1].replace(difrow[2],
                                                                                                difrow[2] + '+')
                                                    del(workspace[:])
    writer = csv.writer(open('envs/withpolarity.csv', 'w', encoding='UTF-8'), delimiter=';')
    for key, value in newdict.items():
        writer.writerow([key, value])
def filter_aspectseed(seed,folder,file):
    with open(file, mode='r', encoding='UTF-8') as infile:
        wordreader = csv.reader(infile, delimiter=';')
        aspect = {rows[0]: rows[1] for rows in wordreader}
    checkdict =extract_dict(folder)
    freqdict = {}
    for aspects1 in aspect.keys():
        counter = 0
        for aspects in checkdict.keys():
            if aspects.split(' ')[1] == aspects1 and aspects.split(' ')[0] in seed:
                counter += int(checkdict[aspects].split(' ')[2])
        freqdict[aspects1]=counter
    writer = csv.writer(open('envs/aspect_stats.csv', 'w', encoding='UTF-8'), delimiter=';')
    for key, value in freqdict.items():
        writer.writerow([key, value])
def cleanup_aspect(cleanaspects,filteraspects):
    with open(cleanaspects, mode='r', encoding='UTF-8') as infile:
        wordreader = csv.reader(infile, delimiter=';')
        aspect = {rows[0]: rows[1] for rows in wordreader}
    with open(filteraspects, mode='r', encoding='UTF-8') as infile:
        wordreader = csv.reader(infile, delimiter=';')
        aspect2 = {rows[0]: rows[1] for rows in wordreader}
    outdict = {}
    for aspects in aspect.keys():
        if int(aspect2[aspects]) >= 5:
            outdict[aspects] = aspect[aspects]
    writer = csv.writer(open('envs/clean_freq/adj-aspects.csv', 'w', encoding='UTF-8'), delimiter=';')
    for key, value in outdict.items():
        writer.writerow([key, value])
seed_good = ['хороший','отличный']
seed_bad = ['плохой', 'ужасный']
seed_good.extend(seed_bad)
#print(seed_good)
def lukashevich(lukashevich,mycorpus):
    with open(lukashevich, mode='r', encoding='UTF-8') as infile:
        wordreader = csv.reader(infile, delimiter='	')
        lukash = {rows[0]: rows[1] for rows in wordreader}
    with open(mycorpus, mode='r', encoding='UTF-8') as infile2:
        wordreader = csv.reader(infile2, delimiter=';')
        mycorpusdic = {rows[0]: rows[1] for rows in wordreader}
    polnolist = []
    for i in lukash.keys():
        print(i.lower())
        if i.lower() in mycorpusdic.keys() and float(lukash[i])>0.3:
            polnolist.append(i)
    return(polnolist)
def polnotacount(finalresult, polnolist):
    with open(finalresult, mode='r', encoding='UTF-8') as infile:
        wordreader = csv.reader(infile, delimiter=';')
        mydict = {rows[0]:rows[1] for rows in wordreader}
    counter = 0
    nowordslist = []
    for i in polnolist:
        for k in mydict.values():
            if i.lower() in k.split(','):
                counter +=1
            else:
                nowordslist.append(i.lower())
    print(counter)
    print(counter/int(len(polnolist)))
    print(', '.join(list(set(nowordslist))))
#filter_aspectseed(seed_good,'cleanresults.csv','clean_result_adjectives_freq.csv')
#cleanup_aspect('clean_result_adjectives_freq.csv','envs/aspect_stats.csv')
biba = lukashevich('lukashevich.txt','data.csv')
print(biba)
polnotacount('envs/clean_LLH/adj-aspects.csv',biba)
