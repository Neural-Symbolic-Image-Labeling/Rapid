import math,re,copy,json,time

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
    
def get_result_list(target,result_list,total_list,variable1,variable2):
    new_result_list=[]
    number=[]
    character=[]
    for image in result_list:
        for clauses in image:
            a=re.split(r'[¬|(|,|)]',clauses)
            if len(a)==5:
                if a[3] not in number:
                    number.append(a[3])
            elif a[0]!="overlap" and a[0]!="num" and a[0]!="area":
                if a[2] not in number:
                    number.append(a[2])
            elif a[0]=="overlap":
                if a[2] not in number:
                    number.append(a[2])
                if a[1] not in number:
                    number.append(a[1])
            else:
                if a[1] not in number:
                    number.append(a[1])
    number.sort(key=get_int)
    for i in range(len(number)):
        if i<13:
            character.append(chr(i+65))
        elif 13<=i<23:
            character.append(chr(i+65+1))
        else:
            character.append(chr(i+65+2))
    for image in result_list:
        result=[]
        for clauses in image:
            a=re.split(r'[¬|(|,|)]',clauses)
            if len(a)==5:
                position=number.index(a[3])
                a[3]=character[position]
                clause="¬"+a[1]+"("+a[2]+","+a[3]+")"+a[4]
                result.append(clause)
            elif a[0]!="overlap" and a[0]!='num'and a[0]!='area' and a[0]!='color':
                position=number.index(a[2])
                a[2]=character[position]
                clause=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                result.append(clause)
            elif a[0]=="overlap":
                position1=number.index(a[1])
                position2=number.index(a[2])
                a[1]=character[position1]
                a[2]=character[position2]
                clause=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                result.append(clause)
            elif a[0]=="color":
                position=number.index(a[1])
                a[1]=character[position]
                clause=a[0]+"("+a[1]+","+a[2]+")"+a[3]
                result.append(clause)
            else:
                position=number.index(a[1])
                a[1]=character[position]
                clause=a[0]+"("+a[1]+","+"N"+")"+a[3]
                result.append(clause)
                mini,maxi=threshold(target,clauses,total_list,variable1,variable2)
                if mini!=0:
                    threshold_clause="N>"+str(mini)
                else:
                    threshold_clause="N<"+str(maxi)
                result.append(threshold_clause)
        new_result_list.append(result)
    return new_result_list
    
def get_total_list1(input_list):
    total_object=[]
    total_list=[]
    object_detection=[]
    segmentation=[]
    for image_num in range(len(input_list)):
        for objects_num in range(len(input_list[image_num]['object_detect']['object'])):
            name=input_list[image_num]['object_detect']['object'][str(objects_num)]['name']
            if name not in total_object:
                total_object.append(name)
                object_detection.append(name)
        for objects_num in range(len(input_list[image_num]['panoptic_segmentation'])):
            name=input_list[image_num]['panoptic_segmentation'][str(objects_num)]['name']
            if name not in total_object:
                total_object.append(name)
                segmentation.append(name)
    for image_num in range(len(input_list)):
        image_list=[]
        string=input_list[image_num]['type']+"(image"+str(input_list[image_num]['imageId'])+")"
        image_list.append(string)
        position_list=[]
        position_list1=[]
        name_list=[]
        for objects_num in range(len(input_list[image_num]['object_detect']['object'])):
            name=input_list[image_num]['object_detect']['object'][str(objects_num)]['name']
            position=total_object.index(name)
            if position not in position_list:
                position_list.append(position)
                name_list.append(name)
        for objects_num in range(len(input_list[image_num]['panoptic_segmentation'])):
            name=input_list[image_num]['panoptic_segmentation'][str(objects_num)]['name']
            position=total_object.index(name)
            if position not in position_list1:
                position_list1.append(position)
        object_numbers=[0 for i in range(len(position_list))]
        for objects_num in range(len(input_list[image_num]['object_detect']['object'])):
            name=input_list[image_num]['object_detect']['object'][str(objects_num)]['name']
            position=total_object.index(name)
            object_numbers[position_list.index(position)]+=1
        for index,objects in enumerate(position_list):
            has=total_object[objects]+"(image"+str(input_list[image_num]['imageId'])+","+str(objects)+")"
            num="num"+"("+str(objects)+","+str(object_numbers[index])+")"
            image_list.append(has)
            image_list.append(num)
        for index,objects in enumerate(position_list1):
            has=total_object[objects]+"(image"+str(input_list[image_num]['imageId'])+","+str(objects)+")"
            area="area"+"("+str(objects)+","+str(input_list[image_num]['panoptic_segmentation'][str(index)]['area'])+")"
            image_list.append(has)
            image_list.append(area)
        for index,objects in enumerate(total_object):
            if (index not in position_list) and (index not in position_list1):
                not_has="¬"+objects+"(image"+str(input_list[image_num]['imageId'])+","+str(index)+")"
                image_list.append(not_has)
        for objects_num in range(len(input_list[image_num]['object_detect']['overlap'])):
            object1_name=input_list[image_num]['object_detect']['object'][str(input_list[image_num]['object_detect']['overlap'][str(objects_num)]["idA"])]['name']
            object2_name=input_list[image_num]['object_detect']['object'][str(input_list[image_num]['object_detect']['overlap'][str(objects_num)]["idB"])]['name']
            position1=total_object.index(object1_name)
            position2=total_object.index(object2_name)
            if position1<position2:
                overlap="overlap("+str(position1)+","+str(position2)+")"
            else:
                overlap="overlap("+str(position2)+","+str(position1)+")"
            if overlap not in image_list:
                image_list.append(overlap)
        total_list.append(image_list)
    return total_list,object_detection,segmentation

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
            a=re.split(r'[¬|(|,|)]',predicate)
            if len(a)==5:
                if predicate not in new_image:
                    new_image.append(predicate)
            elif a[0]!="overlap" and a[0]!='num'and a[0]!='area' and a[0]!='color':
                still_has.append(a[2])
                if predicate not in new_image:
                    new_image.append(predicate)
            elif a[0]=="num" or a[0]=="area":
                if a[1] in still_has and predicate not in new_image:
                    new_image.append(predicate)
            elif a[0]=="overlap":
                if a[1] in still_has and a[2] in still_has and predicate not in new_image:
                    new_image.append(predicate)
        result_list.append(new_image)
    return result_list

def threshold(target,clause,total_list,variable1,variable2):
    a1=re.split(r'[(|,|)]',clause)
    if a1[0]=='num':
        positive_list=[]
        negative_list=[]
        positive_greater=negative_greater=0
        for image in total_list:
            for clauses in image:
                a=re.split(r'[(|,|)]',clauses)
                if a[0]=='num' and a[1]==a1[1]:
                    if image[0]==target:
                        positive_list.append(int(a[2]))
                    else:
                        negative_list.append(int(a[2]))
        for number in positive_list:
            if number>variable1:
                positive_greater+=1
        for number in negative_list:
            if number>variable1:
                negative_greater+=1
        if positive_greater>2/3*len(positive_list) and negative_greater<=1/3*len(negative_list):
            return variable1,10000
        elif positive_greater<=1/3*len(positive_list) and negative_greater>2/3*len(negative_list):
            return 0,variable1
        else:
            return False
    if a1[0]=='area':
        positive_list=[]
        negative_list=[]
        positive_greater=negative_greater=0
        for image in total_list:
            for clauses in image:
                a=re.split(r'[(|,|)]',clauses)
                if a[0]=='area' and a[1]==a1[1]:
                    if image[0]==target:
                        positive_list.append(float(a[2]))
                    else:
                        negative_list.append(float(a[2]))
        for number in positive_list:
            if number>variable2:
                positive_greater+=1
        for number in negative_list:
            if number>variable2:
                negative_greater+=1
        if positive_greater>2/3*len(positive_list) and negative_greater<=1/3*len(negative_list):
            return variable2,10000
        elif positive_greater<=1/3*len(positive_list) and negative_greater>2/3*len(negative_list):
            return 0,variable2
        else:
            return False

def still_has(possible_clause,foil_gain_list):
    has=False
    for clause_num,clauses in enumerate(possible_clause):
        a=re.split(r'[(|,|)]',clauses)
        if a[1]=='X' and foil_gain_list[clause_num]!=-99:
            has=True
            break
    return has

def still_has_num(result):
    has=0
    for clause_num,clauses in enumerate(result):
        a=re.split(r'[(|,|)]',clauses)
        if a[1]=='X':
            has+=1
    return has

def get_object_list(total_list):
    object_list=[]
    for image in total_list:
        for clauses in image:
            a=re.split(r'[(|,|)]',clauses)
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
                object_in_rule=[]
                object_character=[]
                for position,clauses in enumerate(rule[0]):
                    a=re.split(r'[¬|(|,|)]',clauses)
                    if a[0]!='overlap' and a[0]!='num' and a[0]!='area' and len(a)==4:
                        object_in_rule.append(a[0])
                        object_character.append(a[2])
                        for predicate in image:
                            b=re.split(r'[(|,|)]',predicate)
                            if b[0]==a[0]:
                                satisfy_list[position]="True"
                                break
                    elif len(a)==5:
                        for predicate in image:
                            b=re.split(r'[¬|(|,|)]',predicate)
                            if b[1]==a[1]:
                                satisfy_list[position]="True"
                                break
                    elif a[0]=='overlap':
                        object_in_image=[]
                        object_number=[]
                        object1_in_rule=object_in_rule[object_character.index(a[1])]
                        object2_in_rule=object_in_rule[object_character.index(a[2])]
                        for predicate in image:
                            b=re.split(r'[(|,|)]',predicate)
                            if b[0]!='overlap' and b[0]!='num' and b[0]!='area':
                                object_in_image.append(b[0])
                                object_number.append(b[2])
                            if b[0]==a[0]:
                                object1_in_image=object_in_image[object_number.index(b[1])]
                                object2_in_image=object_in_image[object_number.index(b[2])]
                                if object1_in_image==object1_in_rule and object2_in_image==object2_in_rule:
                                    satisfy_list[position]="True"
                                    break
                    elif a[0]=='num' or a[0]=='area':
                        object_in_image=[]
                        object_number=[]
                        object1_in_rule=object_in_rule[object_character.index(a[1])]
                        for predicate in image:
                            b=re.split(r'[(|,|)]',predicate)
                            if b[0]!='overlap' and b[0]!='num' and b[0]!='area':
                                object_in_image.append(b[0])
                                object_number.append(b[2])
                            if b[0]==a[0]:
                                object1_in_image=object_in_image[object_number.index(b[1])]
                                c=re.split(r'[<]',rule[position+1])
                                if len(c)!=1:
                                    maxi=float(c[1])
                                    if object1_in_image==object1_in_rule and float(b[2])<=maxi:
                                        satisfy_list[position]="True"
                                        break
                                else:
                                    c=re.split(r'[>]',rule[position+1])
                                    mini=float(c[1])
                                    if object1_in_image==object1_in_rule and mini<float(b[2]):
                                        satisfy_list[position]="True"
                                        break
                if "False" not in satisfy_list:
                    delete_list.append(i)
    for i,image in enumerate(new_total_list):
        if i not in delete_list:
            final_list.append(image)
    return final_list

def cha_to_num(target,total_list,lists):
    object_list=get_object_list(total_list)
    c=re.split(r'[(|,|)]',target)
    for rules in lists[c[0]]:
        print(rules)
        for rule in rules:
            if rule!=0 and rule!=1:
                position=[]
                for pos,predicate in enumerate(rule):
                    print(rule)
                    print(predicate)
                    a=re.split(r'[¬|(|,|)]',predicate)
                    if len(a)==1:
                        if len(re.split(r'[<]',predicate))==1:
                            d=str(object_list.index(a[0]))
                            rule[pos]=a[0]+'('+'X'+','+d+')'+''
                        else:
                            position.append(pos)
                    elif len(a)==2:
                        d=str(object_list.index(a[0]))
                        rule[pos]=a[0]+a[1]+'('+'X'+','+d+')'+''
                    elif a[0]=='overlap':
                        a[1]=str(object_list.index(a[1]))
                        a[2]=str(object_list.index(a[2]))
                        rule[pos]=a[0]+'('+a[1]+','+a[2]+')'+a[3]
                    elif a[0]=='num' or a[0]=='area':
                        a[1]=str(object_list.index(a[1]))
                        rule[pos]=a[0]+'('+a[1]+','+a[2]+')'+a[3]
                for i in range(len(position)):
                    del rule[position[len(position)-1-i]]
    return lists


def foil(target_list,target,total_list,variable1,variable2,deleted,locked):         #target should be a string, such as "guitarist"
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
    for label in lock:
        if lock[label]==[]:
            lock[label]==[[[],[],0]]
    result_list=[]     #two dimentional list
    object_list=get_object_list(total_list)
    delete=cha_to_num(target,total_list,delete)
    lock=cha_to_num(target,total_list,lock)
    new_total_list=locking(target,total_list,lock)
    total_list1=copy.deepcopy(new_total_list)
    positive_list,negative_list=pos_neg_list(target,new_total_list)   #get the initial_positive_list,to help find out the result that can satisfy all the positives
    c=re.split(r'[(|,|)]',target)
    initial_neg_length = len(negative_list)
    initial_pos_length = len(positive_list)
    i=0   #make sure that all the result in the result list has been proved that fulfill our requirements(can satisfy all the positives and reject all the negatives)
    #start=time.time()
    while (len(positive_list)> 0.4*initial_pos_length):
        counting=0
        while (len(negative_list)> 0.4*initial_neg_length):
            if len(result_list)==i:                #the result_list is empty at initial state
                result=[]
            else:
                result=result_list[i]
            pre_p=len(positive_list)
            pre_n=len(negative_list)
            foil_gain_list=[]
            possible_clause=get_possible_clause1(counting,total_list1,result_list)
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
            #print(foil_gain_list)    
            while correct_clause == False:
                for clause_number,clause_gain in enumerate(foil_gain_list):
                    if max(foil_gain_list)==-99:
                        return None
                    if clause_gain==max(foil_gain_list):
                        a=re.split(r'[¬|(|,|)]',possible_clause[clause_number])
                        if a[0]=="overlap":
                            if (a[1] in parameter_list) and (a[2] in parameter_list) and still_has_num(result)>=2:
                                new_result=copy.deepcopy(result)    #The following is to first add it to result, if it is a special case 
                                new_result.append(possible_clause[clause_number])       # such that only one positive has the clause and no negative has it, it may has the best gain.
                                result_list.append(new_result)
                                correct_clause=True
                                break
                            else:
                                foil_gain_list[clause_number]=-99
                                break
                        elif a[0]=="num" or a[0]=='area':
                            if a[1] in parameter_list and threshold(target,possible_clause[clause_number],total_list1,variable1,variable2)!=False and still_has_num(result)>=3:
                                new_result=copy.deepcopy(result)
                                new_result.append(possible_clause[clause_number])
                                result_list.append(new_result)
                                correct_clause=True
                                break
                            else:
                                foil_gain_list[clause_number]=-99
                                break 
                        else:
                            new_result=copy.deepcopy(result)
                            new_result.append(possible_clause[clause_number])
                            result_list.append(new_result)
                            correct_clause=True
                            break
            if counting!=0:          #Each time, because we add the updated version at the end of the list, so delete the old version
                del result_list[i]
            #print("This is result_list",result_list)
            #print(new_total_list)
            new_total_list=get_new_total_list(result_list,total_list1)
            #print(new_total_list[0])
            positive_list,negative_list=pos_neg_list(target,new_total_list)   # can use for next iteration when the answer is not perfect
            #print("This is ",positive_list)
            counting+=1           #just for the special case that at first the list is empty and we cannot delete the new added one. (Or we can say that we cannot delete the old empty version)
        for rule in delete[c[0]]:
            if rule[2]==0:
                #print(result_list[i])
                if len(result_list[i])==len(rule[0]):
                    result_in=True
                    for predicate in rule[0]:
                        if predicate not in result_list[i]:
                            a=re.split(r'[¬|(|,|)]',predicate)
                            if a[0]!='num' and a[0]!='area':
                                result_in=False
                                break
                            else:
                                result_ins=False
                                for element in result_list[i]:
                                    b=re.split(r'[(|,|)]',element)
                                    if b[0]==a[0] and b[1]==a[1]:
                                        result_ins=True
                                        break
                                if result_ins==False:
                                    result_in=False
                                    break
                    if result_in==True:
                        for del_predicate in rule[1]:
                            a=re.split(r'[¬|(|,|)]',del_predicate)
                            if a[0]!='num' and a[0]!='area':
                                result_list[i].remove(del_predicate)
                            else:
                                for ele_pos,element in enumerate(result_list[i]):
                                    b=re.split(r'[(|,|)]',element)
                                    if b[0]==a[0] and b[1]==a[1]:
                                        del_position=ele_pos
                                del result_list[i][del_position]                        
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
                            a=re.split(r'[¬|(|,|)]',predicate)
                            #print(a[0])
                            if a[0]!='num' and a[0]!='area':
                                result_in=False
                                break
                            else:
                                result_ins=False
                                for element in result_list[i]:
                                    b=re.split(r'[(|,|)]',element)
                                    if b[0]==a[0] and b[1]==a[1]:
                                        result_ins=True
                                        break
                                if result_ins==False:
                                    result_in=False
                                    break
                    if result_in==True:
                        results_in=True
                        for predicate in result_list[i]:
                            if predicate not in rule[0]:
                                a=re.split(r'[¬|(|,|)]',predicate)
                                if a[0]!='num' and a[0]!='area':
                                    results_in=False
                                    break
                                else:
                                    result_ins=False
                                    for element in rule[0]:
                                        b=re.split(r'[(|,|)]',element)
                                        if b[0]==a[0] and b[1]==a[1]:
                                            result_ins=True
                                            break
                                    if result_ins==False:
                                        results_in=False
                                        break
                        if results_in==True:
                            result_list[i]=rule[0]
            elif len(rule[0])==len(rule[1]) and rule[2]==0:
                if len(result_list[i])<len(rule[0]):
                    result_in=True
                    for predicate in result_list[i]:
                        if predicate not in rule[0]:
                            a=re.split(r'[¬|(|,|)]',predicate)
                            if a[0]!='num' and a[0]!='area':
                                result_in=False
                                break
                            else:
                                result_ins=False
                                for element in result_list[i]:
                                    b=re.split(r'[(|,|)]',element)
                                    if b[0]==a[0] and b[1]==a[1]:
                                        result_ins=True
                                        break
                                if result_ins==False:
                                    result_in=False
                                    break
                    if result_in==True:
                        result_list[i]=rule[0]
        new_total_list=get_new_total_list1(result_list,total_list1)
        #print(new_total_list)
        positive_list,negative_list=pos_neg_list(target,new_total_list)
        i+=1
    '''delete_position=[]
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
        del result_list[delete_position[len(delete_position)-1-t]]'''
    for rule in lock[c[0]]:
        if (len(rule[0])==len(rule[1]) and rule[0]!=[] and rule[2]==1) or (rule[0]==[] and rule[2]==1):
            result_list.insert(0,rule[1])
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
                n+='This image does not has '+a[1]
            elif a[0]!='overlap' and a[0]!="num" and a[0]!='area' and a[0]!='color' and len(a)==4:
                n+='This image has '+a[0]
                objects.append(a[0])
                characters.append(a[2])
            elif a[0]=="overlap":
                index1=characters.index(a[1])
                index2=characters.index(a[2])
                n+=objects[index1]+' is overlapping with '+objects[index2]
            elif a[0]=="color":
                index1=characters.index(a[1])
                n+='The color of '+objects[index1]+' is '+a[2]
            elif a[0]=='num':
                index=characters.index(a[1])
                object_name=objects[index]
                b=re.split(r'[<]',results[i+1])
                if len(b)!=1:
                    object_name= plural(object_name)
                    max=b[1]
                    n+='The number of '+object_name+" is less than "+max
                else:
                    b=re.split(r'[>]',results[i+1])
                    object_name= plural(object_name)
                    min=b[1]
                    n+='The number of '+object_name+" is greater than "+min
            elif a[0]=='area':
                index=characters.index(a[1])
                object_name=objects[index]
                b=re.split(r'[<]',results[i+1])
                if len(b)!=1:
                    max=b[1]
                    n+='The area of '+object_name+"is less than "+max
                else:
                    b=re.split(r'[>]',results[i+1])
                    min=b[1]
                    n+='The area of '+object_name+" is greater than "+min
            elif len(a)==1:
                b=re.split(r'[<]',clauses)
                if len(b)!=1:
                    object_name= plural(object_name)
                    max=b[1]
                    n+='The number is less than '+max
                else:
                    b=re.split(r'[>]',clauses)
                    object_name= plural(object_name)
                    min=b[1]
                    n+='The number is greater than '+min
            result_list.append(n)
        result.append(result_list)
    return result

def neg_FOIL(input_list,deleted,locked):
    global_variable1=10
    global_variable2=30
    dict_math={}
    dict_nl={}
    start=time.time()
    total_list1,object_detection,segmentation=get_total_list1(input_list)
    print(object_detection)
    print(segmentation)
    total_list=get_total_list(total_list1)
    #total_list_new=get_total_list(total_list1)
    #total_list=change_total(total_list_new)
    object_list=get_object_list(total_list)
    target_list=[]
    for images in total_list:
        if images[0] not in target_list:
            target_list.append(images[0])
    for target in target_list:
        result_list=foil(target_list,target,total_list,global_variable1,global_variable2,deleted,locked)
        if result_list==None:
            dict_math[target]=[['none']]
            dict_nl[target]=[['none']]
        else:
            math_format=get_result_list(target,result_list,total_list,global_variable1,global_variable2)
            natural_language=NL(math_format,target,result_list)
            dict_math[target]=math_format
            dict_nl[target]=natural_language
    end=time.time()
    print(end-start)
    return dict_math,dict_nl,object_detection,segmentation
    #end=time.time()
    #print(end-start)
