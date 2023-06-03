import re
def get_total_listt1(dict_list):
    total_list=[]
    for image_num in range(len(dict_list)):
        image_list=[]
        # string=dict_list[image_num]['type']+"(image"+str(dict_list[image_num]['imageId'])+")"
        # image_list.append(string)
        for name in dict_list[image_num]['object_detect']:
            if dict_list[image_num]['object_detect'][name]!="0":
                has=name+"(image"+str(dict_list[image_num]['imageId'])+","+dict_list[image_num]['object_detect'][name]+")"
                image_list.append(has)
            else:
                for new_image_num in range(len(dict_list)):
                    if dict_list[new_image_num]['object_detect'][name]!="0":
                        not_has="¬"+name+"(image"+str(dict_list[image_num]['imageId'])+","+dict_list[new_image_num]['object_detect'][name]+")"
                        image_list.append(not_has)
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
                for position,clauses in enumerate(rule):
                    a=re.split(r'[¬(|,|)]',clauses)
                    if len(a)==5:
                        for predicate in image:
                            b=re.split(r'[¬|(|,|)]',predicate)
                            if b[1]==a[1] and b[3]==a[3]:
                                satisfy_list[position]="True"
                                break
                    else:
                        for predicate in image:
                            b=re.split(r'[(|,|)]',predicate)
                            if b[0]==a[0] and b[2]==a[2]:
                                satisfy_list[position]="True"
                                break
                if "False" not in satisfy_list:
                    satisfy[rule_num]="True"
            for i in satisfy:
                if i == "True":
                    satisfy_clause_num += 1
            if satisfy_clause_num != 0:
                satisfy_clause_num_list.append(satisfy_clause_num)
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
                rule_length=len(rule)
                for position,clauses in enumerate(rule):
                    a=re.split(r'[¬|(|,|)]',clauses)
                    satisfy_number = 0
                    if len(a)==5:
                        for predicate in image:
                            b=re.split(r'[¬|(|,|)]',predicate)
                            if b[1]==a[1] and b[3]==a[3]:
                                satisfy_number+=1
                                break
                    else:
                        for predicate in image:
                            b=re.split(r'[(|,|)]',predicate)
                            if b[0]==a[0] and b[2]==a[2]:
                                satisfy_number+=1
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
    return labels,al
