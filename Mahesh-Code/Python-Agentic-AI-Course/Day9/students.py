import json
import os

def load_students(filename):
    with open(filename,'r') as file:
        students = json.load(file)
    return students


if __name__ == "__main__":
    filepath = os.path.join(os.getcwd(),"Day9","students.json")
    students = load_students(filepath)
    stud_list = []
    for student in students:
           status="Pass"
           if student["marks"]["Maths"] < 40 or student["marks"]["Science"] < 40 or student["marks"]["English"] < 40:
                status="Fail"

           percentage = (student["marks"]["Maths"] + student["marks"]["Science"] + student["marks"]["English"])/3
        
           stud = {
                "name": student["name"],
                "result": status,
                "percentage": percentage
           }          
           stud_list.append(stud)

#store stud_list in a json file
with open(os.path.join(os.getcwd(),"Day9","students_result.json"),'w') as file:      
     json.dump(stud_list,file,indent=4)