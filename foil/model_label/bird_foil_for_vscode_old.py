import math,re,copy,json,time,random

#This function is to calculate the information gain to make sure the best literal can be added into the final output
def foil_gain(pre_p,pre_n,now_p,now_n):
    if (pre_p==0 or now_p==0):
        return -99                        #There are some cases that the numerator may be 0. Set to -99 for not affecting the normal comparision among the multiple gains
    gain=now_p*(math.log2(now_p/(now_n+now_p))-math.log2(pre_p/(pre_p+pre_n)))        #now_p:new positive, pre_n: previous negative
    return gain
'''print(foil_gain(3,3,3,2))'''

#This function can help change the input into the right format (two dimentional input, the number of first dimentional list is the number of images)
'''possible_clause=get_possile_clause(total_list)'''
'''def add_image(image_list):
    total_list=[]
    total_list.append(image_list)
    return total_list'''
#print(add_image(['people','has(person)']))
    
#This function is to get parameter(s), for example:only when you have "person" or "guitar", you can have overlap(person,guitar)
def get_parameter_list(result):
    parameter_list=[]
    for clause in result:
        a=re.split(r'[(|,|)]',clause)
        if a[0]!="overlap" and a[0]!="num" and a[0]!='area':
            parameter_list.append(a[2])
        '''for parameter_number,parameter in enumerate(a):
            if (parameter_number!=0 and parameter_number!=len(a)-1):     #The format is ["has(x,person)"],want to get "person"
                parameter_list.append(parameter)'''
    return parameter_list

'''This function is to get positive and negative list according to the target(such as "guitarist") and see if the image classified as "guitarist" has the clause,
if yes, it is positive, otherwise negative'''
def pos_neg_list(target,total_list):
    positive_list=[]
    negative_list=[]
    for image_number,image in enumerate(total_list):
        for i,clause in enumerate(image):
            if i==0:
                if clause==target:
                    positive_list.append(image_number)
                else:
                    negative_list.append(image_number)
    return positive_list,negative_list

"""This function is to get new possible list, such as we have a clause :has("person"), then next time we delete all the definition which does not has this clause.
return is a three dimentional list, for the second dimension, it is one-to-one correspond to the result_list (ie, [[has("person")],[has("guitar")]], then the inner
dimension has the correspond images which has the clause in the result_list"""
def get_new_total_list(result_list,total_list):
    del_number_hd=[]
    new_total=copy.deepcopy(total_list)
    for i in range(len(result_list)):
        if i!=len(result_list)-1:
            for image_number,image in enumerate(total_list):
                del_result=True
                for clause in result_list[i]:
                    if (clause not in image):        #remember the position of image that does not has special clause
                        del_result=False
                        break
                if del_result==True:
                    del_number_hd.append(image_number)
        else:
            for image_number,image in enumerate(total_list):
                for clause in result_list[i]:
                    if (clause not in image):
                        del_number_hd.append(image_number)
                        break
    del_number=list(set(del_number_hd))         #del_number has no duplicate
    del_number.sort()
    for i in range(len(del_number)):
        del new_total[del_number[len(del_number)-1-i]]               #the position is in positive sequence, first delete the back one
    return new_total   #two dimentional list, get the result which not has the positive that satisfy right side
    
def get_new_total_list1(result_list,total_list):        #use for outer loop
    del_number_hd=[]
    new_total=copy.deepcopy(total_list)           #use deepcopy for not changing the total_list
    for clauses_list in result_list:
        for image_number,image in enumerate(total_list):
            del_result=True
            for clause in clauses_list:
                if (clause not in image):        #remember the position of image that does not has special clause
                    del_result=False
                    break
            if del_result==True:
                del_number_hd.append(image_number)
    del_number=list(set(del_number_hd))         #del_number has no duplicate
    del_number.sort()
    for i in range(len(del_number)):
        del new_total[del_number[len(del_number)-1-i]]               #the position is in positive sequence, first delete the back one
    return new_total   #two dimentional list, get the result which not has the positive that satisfy right side

def get_possible_clause1(counting,total_list,result_list):
    if counting==0:
        new_total=get_new_total_list1(result_list,total_list)
        clause_total=[]
        for image in new_total:
            for i,clause in enumerate(image):
                if i!=0 and (clause not in clause_total):        # The first position of each image is classification, so clauses start from the second position
                    clause_total.append(clause)
    else:
        new_total=get_new_total_list(result_list,total_list)
        clause_total=[]
        for image in new_total:
            for i,clause in enumerate(image):
                if i!=0 and (clause not in result_list[len(result_list)-1]) and (clause not in clause_total):        # The first position of each image is classification, so clauses start from the second position
                    clause_total.append(clause)
    return clause_total
    
def rank_the_result(result_list):
    result=sorted(result_list,key=lambda i:len(i))
    return result

def get_total_list(total_list1):
    total_list=[]
    for image in total_list1:
        list=[]
        sub=re.split(r'[(|,|)]',image[0])[1]     #"campus(image1)",get "image1"
        for clauses in image:
            a=re.split(r'[¬|(|,|)]',clauses)
            if a[1]==sub:
                a[1]="X"
                if len(a)==3:
                    result=a[0]+"("+a[1]+")"+a[2]
                else:
                    result=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                list.append(result)
            elif a[2]==sub:
                a[2]="X"
                result="¬"+a[1]+"("+a[2]+","+a[3]+")"+a[4]
                list.append(result)
            else:
                result=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                list.append(result)
        total_list.append(list)
    return total_list

def get_int(elem):
    return int(elem)
    
def get_total_list1(input_list):
    #list=[load_dict1]
    total_list=[]
    for image_num in range(len(input_list)):
        image_list=[]
        string=input_list[image_num]['type']+"(image"+str(input_list[image_num]['imageId'])+")"
        image_list.append(string)
        for name in input_list[image_num]['object_detect']:
            if input_list[image_num]['object_detect'][name]!="0":
                has=name+"(image"+str(input_list[image_num]['imageId'])+","+input_list[image_num]['object_detect'][name]+")"
                image_list.append(has)
            else:
                for new_image_num in range(len(input_list)):
                    if input_list[new_image_num]['object_detect'][name]!="0":
                        not_has="¬"+name+"(image"+str(input_list[image_num]['imageId'])+","+input_list[new_image_num]['object_detect'][name]+")"
                        image_list.append(not_has)
        total_list.append(image_list)
    return total_list

def tfidf(target,total_list):
    pos_total_num=0
    pos_num=0
    num_image=len(total_list)
    for image in total_list:
         if image[0]==target:
             pos_total_num+=(len(image)-1)
             pos_num+=1
    neg_num=num_image-pos_num
    result_list=[]
    for image in total_list:
        if image[0]==target:
            for predicate_pos,predicate in enumerate(image):
                if predicate_pos!=0:
                    word_pos_total_num=0
                    word_total_num=0
                    for images in total_list:
                        if images[0]==target and (predicate in images):
                            word_pos_total_num+=1
                        if predicate in images:
                            word_total_num+=1
                    tf=word_pos_total_num/pos_total_num
                    idf=math.log(num_image/(1+word_total_num))
                    #idf=math.log(1+(word_pos_total_num/pos_num)*(0.01+(word_total_num-word_pos_total_num)/neg_num))
                    result=idf
                    #limit1=math.log((1+num_image/(1+pos_num))/2)
                    #limit2=math.log((num_image/2+num_image/(1+pos_num))/2)
                    if predicate not in result_list and 3>result>0.001:
                        result_list.append(predicate)
                        #result_list.append(result)
    #print(result_list)
    return result_list

def tfidf_test(target,total_list):
    pos_total_num=0
    num_image=len(total_list)
    for image in total_list:
         if image[0]==target:
             pos_total_num+=(len(image)-1)
    result_list=[]
    for image in total_list:
        if image[0]==target:
            #print(image)
            for predicate_pos,predicate in enumerate(image):
                if predicate_pos!=0:
                    word_pos_total_num=0
                    word_total_num=0
                    for images in total_list:
                        if images[0]==target and (predicate in images):
                            word_pos_total_num+=1
                        if predicate in images:
                            word_total_num+=1
                    tf=word_pos_total_num/pos_total_num
                    idf=math.log(num_image/(1+word_total_num))
                    #print(predicate,word_total_num,num_image)
                    result=tf*idf
                    if predicate not in result_list:
                        #result_list.append(tf)
                        #result_list.append(idf)
                        result_list.append(predicate)
                        result_list.append(result)
    return result_list

def change_total(total_list):
    result_list=[]
    for image in total_list:
        new=[]
        tfidf_list=tfidf(image[0],total_list)
        for predicate in image:
            if predicate in tfidf_list:
                new.append(predicate)
        still_has=[]
        new_image=[]
        new_image.append(image[0])
        for predicate in new:
            if predicate not in new_image:
                new_image.append(predicate)
        result_list.append(new_image)
    return result_list                              

def get_object_list(total_list):
    object_list=[]
    for image in total_list:
        for clauses in image:
            a=re.split(r'[¬(|,|)]',clauses)
            if a[0]!='overlap' and a[0]!='num' and a[0]!='area' and len(a)==4 and (a[0] not in object_list):
                object_list.append(a[0])
    return object_list

def locking(target,total_list,lock):
    new_total_list=copy.deepcopy(total_list)
    c=re.split(r'[(|,|)]',target)
    delete_list=[]
    final_list=[]
    for rule in lock[c[0]]:
        if rule[2]==1:
            for i,image in enumerate(new_total_list):
                satisfy_list=["False" for i in range(len(rule[0]))]
                for position,clauses in enumerate(rule[0]):
                    a=re.split(r'[¬(|,|)]',clauses)
                    if a[0]!='overlap' and a[0]!='num' and a[0]!='area' and len(a)==4:
                        for predicate in image:
                            b=re.split(r'[¬(|,|)]',predicate)
                            if b[0]==a[0] and b[2]==a[2]:
                                satisfy_list[position]="True"
                                break
                    elif len(a)==5:
                        for predicate in image:
                            b=re.split(r'[¬(|,|)]',predicate)
                            if b[1]==a[1] and b[3]==a[3]:
                                satisfy_list[position]="True"
                                break
                if "False" not in satisfy_list:
                    delete_list.append(i)
    for i,image in enumerate(new_total_list):
        if i not in delete_list:
            final_list.append(image)
    return final_list

def foil(target_list,target,total_list,deleted,locked):
    delete=copy.deepcopy(deleted)
    lock=copy.deepcopy(locked)
    if delete=={}:
        for targets in target_list:
            get_targets=re.split(r'[(|,|)]',targets)
            delete[get_targets[0]]=[[[],[],0]]
    if lock=={}:
        for targets in target_list:
            get_targets=re.split(r'[(|,|)]',targets)
            lock[get_targets[0]]=[[[],[],0]]
    for label in delete:
        if delete[label]==[]:
            delete[label]==[[[],[],0]]
    for label in delete:
        if lock[label]==[]:
            lock[label]==[[[],[],0]]
#target should be a string, such as "guitarist"
    result_list=[]     #two dimentional list
    object_list=get_object_list(total_list)
    new_total_list=locking(target,total_list,lock)
    new_total_list=copy.deepcopy(total_list)
    positive_list,negative_list=pos_neg_list(target,new_total_list)   #get the initial_positive_list,to help find out the result that can satisfy all the positives
    c = re.split(r"[(|,|)]", target)
    i=0   #make sure that all the result in the result list has been proved that fulfill our requirements(can satisfy all the positives and reject all the negatives)
    while (len(positive_list)!=0):
        counting=0
        while (len(negative_list)!=0):
            if len(result_list)==i:                #the result_list is empty at initial state
                result=[]
            else:
                result=result_list[i]
            pre_p=len(positive_list)
            pre_n=len(negative_list)
            foil_gain_list=[]
            possible_clause=get_possible_clause1(counting,total_list,result_list)
            for new_clause in possible_clause:           #calculate the new possible clause foil_gain
                now_p=now_n=0
                for image_number,image in enumerate(new_total_list):
                    for clause in image:
                        if clause==new_clause:
                            for positive_image_number in positive_list:
                                if image_number==positive_image_number:
                                    now_p+=1  
                            for negative_image_number in negative_list:
                                if image_number==negative_image_number:
                                    now_n+=1
                foil_gain_list.append(foil_gain(pre_p,pre_n,now_p,now_n))
            correct_clause=False              #first set false, if the correct one is found, jump out of the iteration
            parameter_list=get_parameter_list(result)
            #print(possible_clause)
            # print(foil_gain_list)
            if foil_gain_list==[]:
                return None
            while correct_clause == False:
                # print(f'Foil Gain List: {foil_gain_list}')
                for clause_number,clause_gain in enumerate(foil_gain_list):
                    if max(foil_gain_list)==-99:
                        return None
                    if clause_gain==max(foil_gain_list):
                        # print(f'Clause Number: {clause_number}')
                        if possible_clause[clause_number] not in result:
                            new_result=copy.deepcopy(result)
                            new_result.append(possible_clause[clause_number])
                            #print(new_result)
                            result_list.append(new_result)
                            correct_clause=True
                            break
                        else:
                            foil_gain_list[clause_number]=-99
                            break
            if counting!=0:          #Each time, because we add the updated version at the end of the list, so delete the old version
                del result_list[i]
            #print("This is result_list",result_list)
            new_total_list=get_new_total_list(result_list,total_list)
            #print(new_total_list)
            positive_list,negative_list=pos_neg_list(target,new_total_list)   # can use for next iteration when the answer is not perfect
            #print(negative_list)
            counting+=1           #just for the special case that at first the list is empty and we cannot delete the new added one. (Or we can say that we cannot delete the old empty version)
        for rule in delete[c[0]]:
            if rule[2]==0:
                #print(result_list[i])
                if len(result_list[i])==len(rule[0]):
                    result_in=True
                    for predicate in rule[0]:
                        if predicate not in result_list[i]:
                            a=re.split(r'[(|,|)]',predicate)
                            if a[0]!='num' and a[0]!='area':
                                result_in=False
                                break
                    if result_in==True:
                        for del_predicate in rule[1]:
                            a=re.split(r'[(|,|)]',del_predicate)
                            if a[0]!='num' and a[0]!='area':
                                result_list[i].remove(del_predicate)               
        for rule in lock[c[0]]:
            if len(rule[0])!=len(rule[1]):
                pre_assign=[]
                for predicate in rule[0]:
                    if predicate not in rule[1]:
                        pre_assign.append(predicate)
                if len(pre_assign)<=len(result_list[i])<len(rule[0]):
                    result_in=True
                    for predicate in pre_assign:
                        if predicate not in result_list[i]:
                            a=re.split(r'[(|,|)]',predicate)
                            #print(a[0])
                            if a[0]!='num' and a[0]!='area':
                                result_in=False
                                break
                    if result_in==True:
                        results_in=True
                        for predicate in result_list[i]:
                            if predicate not in rule[0]:
                                a=re.split(r'[(|,|)]',predicate)
                                if a[0]!='num' and a[0]!='area':
                                    results_in=False
                                    break
                        if results_in==True:
                            result_list[i]=rule[0]
            elif len(rule[0])==len(rule[1]) and rule[2]==0:
                if len(result_list[i])<len(rule[0]):
                    result_in=True
                    for predicate in result_list[i]:
                        if predicate not in rule[0]:
                            a=re.split(r'[(|,|)]',predicate)
                            if a[0]!='num' and a[0]!='area':
                                result_in=False
                                break
                    if result_in==True:
                        result_list[i]=rule[0]
        delete_position=[]
        for rule in delete[c[0]]:
            if len(rule[0])==len(rule[1]) and rule[0]!=[] and rule[2]==1:
                for t,rules in enumerate(result_list):
                    result_in=True
                    for pred in rules:
                        a=re.split(r'[(|,|)]',pred)
                        if a[0]!='num' and a[0]!='area':
                            if pred not in rule[0]:
                                result_in=False
                                break
                        else:
                            result_ins=False
                            for predicate in rule[0]:
                                b=re.split(r'[(|,|)]',predicate)
                                if b[0]==a[0] and b[1]==a[1]:
                                    result_ins=True
                            if result_ins==False:
                                result_in=False
                                break
                    if result_in==True:
                        delete_position.append(t)
        for t in range(len(delete_position)):
            del result_list[delete_position[len(delete_position)-1-t]]
        new_total_list=get_new_total_list1(result_list,total_list)
        #print(new_total_list)
        positive_list,negative_list=pos_neg_list(target,new_total_list)
        i+=1
    for rule in lock[c[0]]:
        if len(rule[0])==len(rule[1]) and rule[0]!=[] and rule[2]==1:
            result_list.insert(0,rule[0])
    return result_list

def plural(word):
    special_list=['person','grass']
    plural_list=['people','grass']
    if word in special_list:
        return plural_list[special_list.index(word)]
    elif word.endswith('y'):
        return word[:-1]+"ies"
    elif word[-1] in 'sx' or word[-2:] in ['sh','ch']:
        return word+'es'
    elif word.endswith('an'):
        return word[:-2]+'en'
    else:
        return word+'s'
    
def NL(result_list,target,total_list):
    result=[]
    for results in result_list:
        result_list=[]
        objects=[]
        characters=[]
        for i,clauses in enumerate(results):
            n=''
            a=re.split(r'[¬|(|,|)]',clauses)
            if len(a)==5:
                n+='This bird does not has '+a[1]+a[3]
            else:
                n+="This bird has "+a[0]+a[2]
            result_list.append(n)
        result.append(result_list)
    return result

def FOIL(input_list,deleted,locked):
    #start=time.time()
    dict_math={}
    dict_nl={}
    total_list1=get_total_list1(input_list)
    total_list=get_total_list(total_list1)
    object_list=get_object_list(total_list)
    target_list=[]
    for images in total_list:
        if images[0] not in target_list:
            target_list.append(images[0])
    for target in target_list:
        result_list=foil(target_list,target,total_list,deleted,locked)
        if result_list==None:
            dict_math[target]=[['none']]
            dict_nl[target]=[['none']]
        else:
            math_format=result_list
            natural_language=NL(math_format,target,result_list)
            dict_math[target]=math_format
            dict_nl[target]=natural_language
    return dict_math,dict_nl,object_list
    #end=time.time()
    #print(end-start)
