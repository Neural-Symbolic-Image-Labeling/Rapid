import math,re,copy,json,time
def get_total_list1(input_list):
    #list=[load_dict1]
    total_list=[]
    for image_num in range(len(input_list)):
        image_list=[]
        string=input_list[image_num]['type']+"(image"+str(input_list[image_num]['imageId'])+")"
        image_list.append(string)
        for name in input_list[image_num]['object_detect']:
            a=copy.deepcopy(name)
            new_name=re.split(r'[_]',a)
            #if name!='has_wing_color':
            if a=='has_size' or a=='has_shape' or a=='has_head_pattern' or a=='has_bill_color' or a=='has_leg_color' or a=='has_primary_color' or a=='has_belly_color' or a=='has_under_tail_color' or a=='has_nape_color' or a=='has_forehead_color' or a=='has_eye_color' or a=='has_throat__color' or a=='has_breast_color' or a=='has_underparts_color':
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

def tfidf(total_list):
    num_image=len(total_list)
    result_list=[]
    for image in total_list:
        for predicate_pos,predicate in enumerate(image):
            word_total_num=0
            for images in total_list:
                if predicate in images:
                    word_total_num+=1
            idf=math.log(num_image/(1+word_total_num))
            result=idf
            if predicate not in result_list and 3>result>0.001:
                result_list.append(predicate)
    return result_list

def idf(input_list):
    total_list1=get_total_list1(input_list)
    total_list=get_total_list(total_list1)
    return tfidf(total_list)