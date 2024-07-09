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
            a=re.split(r'[(|,|)]',clauses)
            if a[1]==sub:
                a[1]="X"
                if len(a)==3:
                    result=a[0]+"("+a[1]+")"+a[2]
                else:
                    result=a[0]+"("+a[1]+","+a[2]+")"+a[3]
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
            a=re.split(r'[(|,|)]',clauses)
            if a[0]!="overlap" and a[0]!="num" and a[0]!="area":
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
            a=re.split(r'[(|,|)]',clauses)
            if a[0]!="overlap" and a[0]!='num'and a[0]!='area':
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
    for image_num in range(len(input_list)):
        for objects_num in range(len(input_list[image_num]['object_detect']['object'])):
            name=input_list[image_num]['object_detect']['object'][str(objects_num)]['name']
            if name not in total_object:
                total_object.append(name)
        for objects_num in range(len(input_list[image_num]['panoptic_segmentation'])):
            name=input_list[image_num]['panoptic_segmentation'][str(objects_num)]['name']
            if name not in total_object:
                total_object.append(name)
    for image_num in range(len(input_list)):
        image_list=[]
        string=input_list[image_num]['type']+"(image"+str(input_list[image_num]['imageId'])+")"
        image_list.append(string)
        position_list=[]
        position_list1=[]
        for objects_num in range(len(input_list[image_num]['object_detect']['object'])):
            name=input_list[image_num]['object_detect']['object'][str(objects_num)]['name']
            position=total_object.index(name)
            if position not in position_list:
                position_list.append(position)
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
    return total_list

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
                    a=re.split(r'[(|,|)]',clauses)
                    if a[0]!='overlap' and a[0]!='num' and a[0]!='area' and len(a)==4:
                        object_in_rule.append(a[0])
                        object_character.append(a[2])
                        for predicate in image:
                            b=re.split(r'[(|,|)]',predicate)
                            if b[0]==a[0]:
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
        for rule in rules:
            if rule!=0 and rule!=1:
                position=[]
                for pos,predicate in enumerate(rule):
                    a=re.split(r'[(|,|)]',predicate)
                    if len(a)==1:
                        if len(re.split(r'[<]',predicate))==1:
                            d=str(object_list.index(a[0]))
                            rule[pos]=a[0]+'('+'X'+','+d+')'+''
                        else:
                            position.append(pos)
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
    for label in delete:
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
                        a=re.split(r'[(|,|)]',possible_clause[clause_number])
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
                            a=re.split(r'[(|,|)]',predicate)
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
                            a=re.split(r'[(|,|)]',del_predicate)
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
                            a=re.split(r'[(|,|)]',predicate)
                            print(a[0])
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
                                a=re.split(r'[(|,|)]',predicate)
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
                            a=re.split(r'[(|,|)]',predicate)
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
        new_total_list=get_new_total_list1(result_list,total_list1)
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
            a=re.split(r'[(|,|)]',clauses)
            if a[0]!='overlap' and a[0]!="num" and a[0]!='area' and len(a)==4:
                n+='This image has '+a[0]
                objects.append(a[0])
                characters.append(a[2])
            elif a[0]=="overlap":
                index1=characters.index(a[1])
                index2=characters.index(a[2])
                n+=objects[index1]+' is overlapping with '+objects[index2]
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

def FOIL(input_list,deleted,locked):
    global_variable1=10
    global_variable2=30
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
        result_list=foil(target_list,target,total_list,global_variable1,global_variable2,deleted,locked)
        if result_list==None:
            dict_math[target]=[['none']]
            dict_nl[target]=[['none']]
        else:
            math_format=get_result_list(target,result_list,total_list,global_variable1,global_variable2)
            natural_language=NL(math_format,target,result_list)
            dict_math[target]=math_format
            dict_nl[target]=natural_language
    return dict_math,dict_nl,object_list
    #end=time.time()
    #print(end-start)

if(__name__) == "__main__":
    a = [{'imageId': 1, 'type': 'motorcyclist', 'object_detect': {'object': {'0': {'coordinate': [172.38043212890625, 463.5223083496094, 646.1954956054688, 876.8612060546875], 'name': 'motorcycle', 'prob': 0.9991017580032349}, '1': {'coordinate': [326.3105163574219, 401.5079345703125, 389.7975158691406, 534.412353515625], 'name': 'person', 'prob': 0.9831495881080627}, '2': {'coordinate': [316.0980529785156, 444.77581787109375, 517.108154296875, 869.2247924804688], 'name': 'person', 'prob': 0.999517560005188}}, 'overlap': {'0': {'idA': 0, 'idB': 1, 'area': 4500.596262840554}, '1': {'idA': 0, 'idB': 2, 'area': 81550.29744025413}, '2': {'idA': 1, 'idB': 2, 'area': 5690.754694696516}}}, 'panoptic_segmentation': {'0': {'name': 'dirt', 'area': 332065}, '1': {'name': 'tree', 'area': 246561}}}, {'imageId': 2, 'type': 'motorcyclist', 'object_detect': {'object': {'0': {'coordinate': [250.38198852539062, 202.0446014404297, 473.5886535644531, 404.47027587890625], 'name': 'person', 'prob': 0.998936116695404}, '1': {'coordinate': [246.21017456054688, 290.8921813964844, 594.0880126953125, 514.2434692382812], 'name': 'motorcycle', 'prob': 0.9955138564109802}}, 'overlap': {'0': {'idA': 0, 'idB': 1, 'area': 25351.387690912932}}}, 'panoptic_segmentation': {'0': {'name': 'sky', 'area': 897040}}}, {'imageId': 3, 'type': 'motorcyclist', 'object_detect': {'object': {'0': {'coordinate': [181.60577392578125, 98.55532836914062, 341.1982116699219, 342.7300720214844], 'name': 'motorcycle', 'prob': 0.9989396929740906}, '1': {'coordinate': [186.05340576171875, 35.008670806884766, 305.5902099609375, 257.2304992675781], 'name': 'person', 'prob': 0.9962771534919739}}, 'overlap': {'0': {'idA': 0, 'idB': 1, 'area': 18967.522834964097}}}, 'panoptic_segmentation': {'0': {'name': 'grass', 'area': 114042}, '1': {'name': 'sky', 'area': 822405}}}, {'imageId': 4, 'type': 'kayaker', 'object_detect': {'object': {'0': {'coordinate': [211.9514923095703, 34.998226165771484, 649.7227783203125, 407.5581970214844], 'name': 'person', 'prob': 0.8881155848503113}, '1': {'coordinate': [356.4825744628906, 171.91932678222656, 786.2911987304688, 616.6943969726562], 'name': 'surfboard', 'prob': 0.9843191504478455}}, 'overlap': {'0': {'idA': 0, 'idB': 1, 'area': 69098.79034569254}}}, 'panoptic_segmentation': {'0': {'name': 'sea', 'area': 765699}}}, {'imageId': 5, 'type': 'kayaker', 'object_detect': {'object': {'0': {'coordinate': [587.2943115234375, 218.22201538085938, 696.8468017578125, 323.75701904296875], 'name': 'backpack', 'prob': 0.8853073716163635}, '1': {'coordinate': [817.72021484375, 77.15763854980469, 1040.55126953125, 402.1435852050781], 'name': 'person', 'prob': 0.9958968162536621}, '2': {'coordinate': [331.6114501953125, 135.56521606445312, 706.2305908203125, 471.2941589355469], 'name': 'person', 'prob': 0.9912133812904358}, '3': {'coordinate': [86.55447387695312, 236.21971130371094, 313.99334716796875, 477.8141174316406], 'name': 'person', 'prob': 0.9970971345901489}, '4': {'coordinate': [21.259765625, 316.4083557128906, 1122.1640625, 566.6729125976562], 'name': 'boat', 'prob': 0.7601139545440674}, '5': {'coordinate': [688.85205078125, 179.29611206054688, 873.27587890625, 410.3681640625], 'name': 'person', 'prob': 0.9830501675605774}}, 'overlap': {'0': {'idA': 0, 'idB': 2, 'area': 11561.622458077967}, '1': {'idA': 0, 'idB': 4, 'area': 805.0643677040935}, '2': {'idA': 0, 'idB': 5, 'area': 843.7260735891759}, '3': {'idA': 1, 'idB': 4, 'area': 19104.471611618996}, '4': {'idA': 1, 'idB': 5, 'area': 12380.439355194569}, '5': {'idA': 2, 'idB': 4, 'area': 58023.18649828434}, '6': {'idA': 2, 'idB': 5, 'area': 4015.6949076242745}, '7': {'idA': 3, 'idB': 4, 'area': 36709.94458799064}, '8': {'idA': 4, 'idB': 5, 'area': 17328.4275457263}}}, 'panoptic_segmentation': {'0': {'name': 'river', 'area': 836745}}}, {'imageId': 6, 'type': 'kayaker', 'object_detect': {'object': {'0': {'coordinate': [113.31305694580078, 170.2941131591797, 250.60275268554688, 307.49090576171875], 'name': 'person', 'prob': 0.9991798996925354}, '1': {'coordinate': [279.1169738769531, 167.58309936523438, 441.423095703125, 308.5831604003906], 'name': 'person', 'prob': 0.9981287121772766}, '2': {'coordinate': [41.08842086791992, 276.51422119140625, 540.712158203125, 341.5938720703125], 'name': 'boat', 'prob': 0.8609580397605896}}, 'overlap': {'0': {'idA': 0, 'idB': 2, 'area': 4252.779599684291}, '1': {'idA': 1, 'idB': 2, 'area': 5204.985154089518}}}, 'panoptic_segmentation': {'0': {'name': 'building', 'area': 20609}, '1': {'name': 'sea', 'area': 680111}, '2': {'name': 'sky', 'area': 42627}, '3': {'name': 'tree', 'area': 127541}}}, {'imageId': 7, 'type': 'kayaker', 'object_detect': {'object': {'0': {'coordinate': [432.0762634277344, 217.7318115234375, 630.9228515625, 370.0716247558594], 'name': 'person', 'prob': 0.9960535764694214}, '1': {'coordinate': [630.3074340820312, 214.74513244628906, 778.9440307617188, 398.73828125], 'name': 'person', 'prob': 0.9979649782180786}, '2': {'coordinate': [348.95697021484375, 314.06787109375, 1104.1219482421875, 419.23175048828125], 'name': 'boat', 'prob': 0.9847426414489746}}, 'overlap': {'0': {'idA': 0, 'idB': 1, 'area': 93.75258403457701}, '1': {'idA': 0, 'idB': 2, 'area': 11136.155338450335}, '2': {'idA': 1, 'idB': 2, 'area': 12585.121605098248}}}, 'panoptic_segmentation': {'0': {'name': 'water', 'area': 1040331}}}, {'imageId': 8, 'type': 'cyclist', 'object_detect': {'object': {'0': {'coordinate': [529.9525146484375, 0.3171815276145935, 599.99365234375, 135.58584594726562], 'name': 'person', 'prob': 0.999180018901825}, '1': {'coordinate': [243.288818359375, 11.666788101196289, 343.69970703125, 218.69947814941406], 'name': 'person', 'prob': 0.9776523113250732}, '2': {'coordinate': [236.084228515625, 98.103271484375, 343.3620910644531, 293.0020751953125], 'name': 'bicycle', 'prob': 0.987236499786377}}, 'overlap': {'0': {'idA': 1, 'idB': 2, 'area': 12068.457076788414}}}, 'panoptic_segmentation': {'0': {'name': 'dirt', 'area': 1010592}, '1': {'name': 'pavement', 'area': 73876}}}, {'imageId': 9, 'type': 'cyclist', 'object_detect': {'object': {'0': {'coordinate': [227.0825653076172, 224.40069580078125, 254.7158660888672, 269.39093017578125], 'name': 'bottle', 'prob': 0.9649207592010498}, '1': {'coordinate': [116.64045715332031, 158.34596252441406, 344.81365966796875, 328.873046875], 'name': 'bicycle', 'prob': 0.9963006973266602}, '2': {'coordinate': [174.7021942138672, 49.9415283203125, 327.0368347167969, 297.37786865234375], 'name': 'person', 'prob': 0.9994283318519592}}, 'overlap': {'0': {'idA': 0, 'idB': 1, 'area': 1243.228678703308}, '1': {'idA': 0, 'idB': 2, 'area': 1243.228678703308}, '2': {'idA': 1, 'idB': 2, 'area': 21179.375438435236}}}, 'panoptic_segmentation': {'0': {'name': 'grass', 'area': 321553}, '1': {'name': 'mountain', 'area': 14870}, '2': {'name': 'road', 'area': 50365}, '3': {'name': 'sky', 'area': 376226}}}, {'imageId': 10, 'type': 'cyclist', 'object_detect': {'object': {'0': {'coordinate': [6.980194091796875, 120.4715576171875, 290.66717529296875, 288.1678771972656], 'name': 'bicycle', 'prob': 0.9976310729980469}, '1': {'coordinate': [73.84797668457031, 24.88779640197754, 249.5963134765625, 235.88009643554688], 'name': 'person', 'prob': 0.9990437626838684}}, 'overlap': {'0': {'idA': 0, 'idB': 1, 'area': 20282.858748920728}}}, 'panoptic_segmentation': {'0': {'name': 'tree', 'area': 459467}, '1': {'name': 'road', 'area': 121046}, '2': {'name': 'grass', 'area': 91530}}}, {'imageId': 11, 'type': 'cyclist', 'object_detect': {'object': {'0': {'coordinate': [79.06304931640625, 19.793981552124023, 360.1679992675781, 661.292236328125], 'name': 'person', 'prob': 0.999744713306427}, '1': {'coordinate': [172.9658966064453, 364.18292236328125, 358.2413635253906, 761.213134765625], 'name': 'bicycle', 'prob': 0.9180211424827576}, '2': {'coordinate': [171.35415649414062, 422.8121337890625, 358.6399230957031, 761.0824584960938], 'name': 'bicycle', 'prob': 0.9464877247810364}}, 'overlap': {'0': {'idA': 0, 'idB': 1, 'area': 55047.066870803945}, '1': {'idA': 0, 'idB': 2, 'area': 44663.92882324755}, '2': {'idA': 1, 'idB': 2, 'area': 62673.19235491846}}}, 'panoptic_segmentation': {'0': {'name': 'pavement', 'area': 778804}}}, {'imageId': 12, 'type': 'bicycle', 'object_detect': {'object': {'0': {'coordinate': [200.5008087158203, 98.33873748779297, 353.92327880859375, 192.1331329345703], 'name': 'bicycle', 'prob': 0.9996660947799683}, '1': {'coordinate': [121.38050842285156, 190.1082763671875, 484.2373962402344, 321.1734313964844], 'name': 'car', 'prob': 0.9982798099517822}}, 'overlap': {'0': {'idA': 0, 'idB': 1, 'area': 310.65849615144543}}}, 'panoptic_segmentation': {}}, {'imageId': 13, 'type': 'bicycle', 'object_detect': {'object': {}, 'overlap': {}}, 'panoptic_segmentation': {}}, {'imageId': 14, 'type': 'boat', 'object_detect': {'object': {'0': {'coordinate': [212.34703063964844, 71.08491516113281, 726.1903686523438, 364.2701110839844], 'name': 'boat', 'prob': 0.9979360103607178}}, 'overlap': {}}, 'panoptic_segmentation': {'0': {'name': 'sea', 'area': 475734}, '1': {'name': 'sky', 'area': 260884}, '2': {'name': 'mountain', 'area': 63992}}}, {'imageId': 15, 'type': 'boat', 'object_detect': {'object': {'0': {'coordinate': [106.67562866210938, 121.25042724609375, 1520.6524658203125, 905.9356079101562], 'name': 'boat', 'prob': 0.9672080278396606}}, 'overlap': {}}, 'panoptic_segmentation': {}}, {'imageId': 16, 'type': 'motorcycle', 'object_detect': {'object': {'0': {'coordinate': [24.37698745727539, 134.77603149414062, 316.7694396972656, 333.7647399902344], 'name': 'motorcycle', 'prob': 0.9995155334472656}}, 'overlap': {}}, 'panoptic_segmentation': {'0': {'name': 'road', 'area': 167319}, '1': {'name': 'mountain', 'area': 22654}, '2': {'name': 'sky', 'area': 457665}, '3': {'name': 'grass', 'area': 52777}}}, {'imageId': 17, 'type': 'motorcycle', 'object_detect': {'object': {'0': {'coordinate': [88.11807250976562, 82.64065551757812, 554.759765625, 374.8077392578125], 'name': 'motorcycle', 'prob': 0.9996050000190735}}, 'overlap': {}}, 'panoptic_segmentation': {}}]
    b = [{'imageId': 1, 'type': 'motorcyclist', 'object_detect': {'object': {'0': {'coordinate': [172.38043212890625, 463.5223083496094, 646.1954956054688, 876.8612060546875], 'name': 'motorcycle', 'prob': 0.9991017580032349}, '1': {'coordinate': [326.3105163574219, 401.5079345703125, 389.7975158691406, 534.412353515625], 'name': 'person', 'prob': 0.9831495881080627}, '2': {'coordinate': [316.0980529785156, 444.77581787109375, 517.108154296875, 869.2247924804688], 'name': 'person', 'prob': 0.999517560005188}}, 'overlap': {'0': {'idA': 0, 'idB': 1, 'area': 4500.596262840554}, '1': {'idA': 0, 'idB': 2, 'area': 81550.29744025413}, '2': {'idA': 1, 'idB': 2, 'area': 5690.754694696516}}}, 'panoptic_segmentation': {'0': {'name': 'dirt', 'area': 332065}, '1': {'name': 'tree', 'area': 246561}}},]
    d = {'motorcyclist': [[['motorcycle', 'person'], [], 0]], 'kayaker': [[['boat', 'person'], [], 0], [['surfboard(X,B)'], [], 0]], 'cyclist': [[['bicycle', 'person'], [], 0]], 'bicycle': [[[], [], 0]], 'boat': [[[], [], 0]], 'motorcycle': [[[], [], 0]]}
#
    l = {'motorcyclist': [[['motorcycle', 'person'], [], 0]], 'kayaker': [[['boat', 'person'], [], 0], [['surfboard(X,B)'], [], 0]], 'cyclist': [[['bicycle', 'person'], [], 0]], 'bicycle': [[[], [], 0]], 'boat': [[[], [], 0]], 'motorcycle': [[[], [], 0]]}
#
    print(FOIL(b, {}, {})[0])