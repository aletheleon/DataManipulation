"""
Georgia Institute of Technology - CS2316
HW01 - Python Basics

Replace 'pass' with the code for each function.
Test your code outside of each function. When ready to submit to GradeScope,
remove all the function calls and any print statements.
"""


def split_bill(num_people, tip_percent, pizza_cost, tax_percent):
    return round(((pizza_cost * (1 + tax_percent)) * (1 + tip_percent))
                 / num_people, 2)


def contains(a_list, value):
    found = False
    count = 0
    for element in a_list:
        count += 1
        if element == value:
            found = True
            break
    return found, count


def score(a_tuple):
    return (6 * a_tuple[0] + a_tuple[1] + 2 * a_tuple[2] + 3 * a_tuple[3]
            + 2 * a_tuple[4])


def winner(a_dict):
    teams = list(a_dict.keys())
    if score(a_dict.get(teams[0])) > score(a_dict.get(teams[1])):
        return teams[0]
    else:
        return teams[1]


def average_exams(super_grades):
    exam_names = super_grades[0][1:4]
    super_grades.remove(super_grades[0])
    exam1 = round(sum([int(exam[1]) for exam in super_grades])
                  / len(super_grades), 2)
    exam2 = round(sum([int(exam[2]) for exam in super_grades])
                  / len(super_grades), 2)
    exam3 = round(sum([int(exam[3]) for exam in super_grades])
                  / len(super_grades), 2)
    return dict([(exam_names[0], exam1), (exam_names[1], exam2),
                 (exam_names[2], exam3)])


def calc_final_grades(super_grades):
    grade_dict = {}
    for student in super_grades[1:]:
        student_grade = 0
        for grade in student[1:]:
            student_grade += (int(grade))
        student_grade *= .25
        if student_grade >= 90.0:
            student_grade = 'A'
        elif student_grade >= 80:
            student_grade = 'B'
        elif student_grade >= 70:
            student_grade = 'C'
        elif student_grade >= 60:
            student_grade = 'D'
        else:
            student_grade = 'F'
        grade_dict[student[0]] = student_grade
    return grade_dict


def date_cruncher(original_dates):
    dates_output = []
    month_dict = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
    for date in original_dates:
        month = date.split()[0][:3].lower()
        month = month_dict[month]
        day = ""
        day_string = date.split()[1]
        for char in day_string:
            if char.isdigit():
                day += char
        if len(day) < 2:
            day = '0' + day
        year = date.split()[2]
        dates_output.append(month + "-" + day + "-" + year)
    return dates_output
