import time

import requests
from bs4 import BeautifulSoup

from Model import Teacher, Project, Breadcrumb, Detail, Member


def insert_data(html_data):
   # print(html_data)
    soup = BeautifulSoup(html_data, 'lxml')

    try:
        # Extract breadcrumb navigation
        breadcrumbs = [li.get_text(strip=True) for li in soup.select('ul.breadcrumb li')]

        # Extract project details
        project_details = {}
        for group in soup.select('.form-group-line'):
            label = group.select_one('.c-label-title label')
            value = group.select_one('.c-detail-item')
            if label and value:
                project_details[label.get_text(strip=True)] = value.get_text(strip=True)

        # Extract project members
        members = []
        member_table = soup.select_one('table.c-table-members')
        if member_table:
            for row in member_table.select('tbody tr'):

                member_info = [td.get_text(strip=True) for td in row.find_all('td')]

                members.append(member_info)

        # Extract project teachers
        teachers = []
        teacher_tables = soup.select('table.c-table-members')
        if len(teacher_tables) > 1:
            teacher_table = teacher_tables[1]
            for row in teacher_table.select('tbody tr'):
                teacher_info = [td.get_text(strip=True) for td in row.find_all('td')]
                teachers.append(teacher_info)

        # Extract project introduction
        project_intro = ''
        project_intro_element = soup.select_one('table.infotable tr:nth-last-child(1) td:nth-child(2)')
        if project_intro_element:
            project_intro = project_intro_element.get_text(strip=True)

        # Extract project name
        project_name = project_details.get('项目名称', 'Unknown Project')  # Default to 'Unknown Project' if not found

        # Store data into SQLite database
        if True:
            # Create Project record
            project = Project.create(name=project_name, intro=project_intro)

            # Store Breadcrumb
            for crumb in breadcrumbs:
                Breadcrumb.create(text=crumb, project=project)

            # Store Details
            Detail.create(
                project_number=project_details.get('项目编号', ''),
                project_name=project_name,
                project_type=project_details.get('项目类型', ''),
                project_category=project_details.get('项目类别', ''),
                key_support_field=project_details.get('重点支持领域', ''),
                affiliated_school=project_details.get('所属学校', ''),
                implementation_time=project_details.get('项目实施时间', ''),
                subject_category=project_details.get('所属学科门类', ''),
                major_category=project_details.get('所属专业大类', ''),
                establishment_time=project_details.get('立项时间', ''),
                project=project
            )

            # Store Members
            for member in members:
                Member.create(
                    name=member[0] if len(member) > 1 else "",
                    grade=member[1] if len(member) > 2 else "",
                    student_id=member[2] if len(member) > 3 else "",
                    department=member[3] if len(member) > 4 else "",
                    major=member[4] if len(member) > 5 else "",
                    phone=member[5] if len(member) > 6 else "",
                    email=member[6] if len(member) > 7 else "",
                    is_leader=member[7] if len(member) > 8 else "",
                    project=project
                )

            # Store Teachers
            for teacher in teachers:
                Teacher.create(
                    name=teacher[1] if len(teacher) > 1 else "",
                    unit=teacher[2] if len(teacher) > 2 else "",
                    professional_title=teacher[3] if len(teacher) > 3 else "",
                    teacher_type=teacher[4] if len(teacher) > 4 else "",
                    project=project
                )

    except Exception as e:
        print(e)
        pass



for item in range(669541, 769541):
    print(item)
    #http://gjcxcy.bjtu.edu.cn/NewLXItemListForStudentDetail.aspx?ItemNo=1069541&IsLXItem=1
    base_url = f"http://gjcxcy.bjtu.edu.cn/NewLXItemListForStudentDetail.aspx?ItemNo={item}&IsLXItem=1"
    response = requests.get(base_url,headers={'User-Agent':'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'})
    insert_data(response.text)
    time.sleep(5)







