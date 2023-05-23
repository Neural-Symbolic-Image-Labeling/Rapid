import re
def get_total_listt1(input_list):
    total_object=["OC","OD","HCup","HDisc","VCup","VDisc"]
    total_object1=["ACDR","HCDR","VCDR"]
    total_list=[]
    for image_num in range(len(input_list)):
        image_list=[]
        # string=input_list[image_num]['type']+"(image"+str(input_list[image_num]['imageId'])+")"
        # image_list.append(string)
        position_list1=[0,1,2]
        for index,objects in enumerate(position_list1):
            has=total_object1[objects]+"(image"+str(input_list[image_num]['imageId'])+","+str(objects)+")"
            area1=float(input_list[image_num]['object_detect']['space'][total_object[objects*2]])
            area2=float(input_list[image_num]['object_detect']['space'][total_object[objects*2+1]])
            area="area"+"("+str(objects)+","+str(area1/area2)+")"
            image_list.append(has)
            image_list.append(area)
        total_list.append(image_list)
    return total_list

def get_total_listt(total_list1):
    total_list=[]
    for image in total_list1:
        list=[]
        for clauses in image:
            a=re.split(r'[(|,|)]',clauses)
            if a[0]!='overlap' and a[0]!='num' and a[0]!='area':
                sub=a[1]
                break
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

def labeling(total_list,rules):
    labels=[]
    possible_labels=[]
    for possible_label in rules.keys():
        possible_labels.append(possible_label)
    for image in total_list:
        label_list=[]
        find=False
        satisfy_clause_num_list=[]
        for possible_label in possible_labels:
            rule_list=rules[possible_label]
            satisfy=["False" for i in range(len(rule_list))]
            satisfy_clause_num = 0
            for rule_num,rule in enumerate(rule_list):
                satisfy_list=["False" for i in range(len(rule))]
                object_in_rule=[]
                object_character=[]
                for position,clauses in enumerate(rule):
                    a=re.split(r'[¬|(|,|)]',clauses)
                    if len(a)==5:
                        for predicate in image:
                            b=re.split(r'[¬|(|,|)]',predicate)
                            if b[1]==a[1]:
                                satisfy_list[position]="True"
                                break
                    elif a[0]!='overlap' and a[0]!='num' and a[0]!='area' and len(a)==4:
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
                            #print(b)
                            if b[0]!='overlap' and b[0]!='num' and b[0]!='area':
                                object_in_image.append(b[0])
                                object_number.append(b[2])
                            if b[0]==a[0]:
                                object1_in_image=object_in_image[object_number.index(b[1])]
                                c=re.split(r'[(|,|)]',rule[position+1])
                                '''mini=float(c[0])
                                maxi=float(c[2])
                                if object1_in_image==object1_in_rule and mini<=float(b[2])<=maxi:
                                    satisfy_list[position]="True"
                                    break'''
                                '''if len(c)!=1:
                                    maxi=float(c[1])
                                    if object1_in_image==object1_in_rule and float(b[2])<=maxi:
                                        satisfy_list[position]="True"
                                        satisfy_list[position+1]="True"
                                        break
                                else:
                                    c=re.split(r'[>]',rule[position+1])
                                    mini=float(c[1])
                                    if object1_in_image==object1_in_rule and mini<float(b[2]):
                                        satisfy_list[position]="True"
                                        satisfy_list[position+1]="True"
                                        #print(1)
                                        break'''
                                maxi=float(c[3])
                                mini=float(c[2])
                                if object1_in_image==object1_in_rule and mini<=float(b[2])<=maxi:
                                    satisfy_list[position]="True"
                                    satisfy_list[position+1]="True"
                                    break
                #print(satisfy_list)
                if "False" not in satisfy_list:
                    satisfy[rule_num]="True"
            for i in satisfy:
                if i == "True":
                    satisfy_clause_num += 1
            if satisfy_clause_num != 0:
                satisfy_clause_num_list.append(satisfy_clause_num)
            #print(satisfy)
            if "True" in satisfy:
                label_list.append(possible_label)
                find=True
        if find==False:
            label_list.append("None")
        if len(label_list) > 1:
            label_list=[label_list[satisfy_clause_num_list.index(max(satisfy_clause_num_list))]]
        labels.append(label_list)
    return labels

def AL(total_list,rules):
    result=[]
    possible_labels=[]
    for possible_label in rules.keys():
        possible_labels.append(possible_label)
    for image in total_list:
        image_ratio=[]
        for possible_label in possible_labels:
            rule_list=rules[possible_label]
            ratio_list=[]
            for rule_num,rule in enumerate(rule_list):
                object_in_rule=[]
                object_character=[]
                rule_length=len(rule)
                satisfy_number = 0
                for position,clauses in enumerate(rule):
                    a=re.split(r'[¬|(|,|)]',clauses)
                    if len(a)==5:
                        for predicate in image:
                            b=re.split(r'[¬|(|,|)]',predicate)
                            if b[1]==a[1]:
                                satisfy_number+=1
                                break
                    elif a[0]!='overlap' and a[0]!='num' and a[0]!='area' and len(a)==4:
                        object_in_rule.append(a[0])
                        object_character.append(a[2])
                        for predicate in image:
                            b=re.split(r'[(|,|)]',predicate)
                            if b[0]==a[0]:
                                satisfy_number+=1
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
                                    satisfy_number+=1
                                    break
                    elif a[0]=='num' or a[0]=='area':
                        object_in_image=[]
                        object_number=[]
                        object1_in_rule=object_in_rule[object_character.index(a[1])]
                        for predicate in image:
                            b=re.split(r'[(|,|)]',predicate)
                            #print(b)
                            if b[0]!='overlap' and b[0]!='num' and b[0]!='area':
                                object_in_image.append(b[0])
                                object_number.append(b[2])
                            if b[0]==a[0]:
                                object1_in_image=object_in_image[object_number.index(b[1])]
                                c=re.split(r'[(|,|)]',rule[position+1])
                                maxi=float(c[3])
                                mini=float(c[2])
                                if object1_in_image==object1_in_rule and mini<=float(b[2])<=maxi:
                                    satisfy_number+=2
                                    break
                ratio=satisfy_number/rule_length
                ratio_list.append(ratio)
            image_ratio.append(max(ratio_list))
        result.append(image_ratio)
    return result

def label(dict_list,rules):
    total_list1=get_total_listt1(dict_list)
    total_list=get_total_listt(total_list1)
    al=AL(total_list,rules)
    labels=labeling(total_list,rules)
    # print(labels)
    return labels,al
