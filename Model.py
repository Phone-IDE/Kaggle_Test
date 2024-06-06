from peewee import CharField, ForeignKeyField, TextField, Model, SqliteDatabase

# Create SQLite database
db = SqliteDatabase('project_info.db')


class BaseModel(Model):
    class Meta:
        database = db


class Project(BaseModel):
    name = CharField()  # This will store 项目名称
    intro = TextField(null=True)


class Breadcrumb(BaseModel):
    text = CharField()
    project = ForeignKeyField(Project, backref='breadcrumbs')


class Detail(BaseModel):
    project_number = CharField()
    project_name = CharField()
    project_type = CharField()
    project_category = CharField()
    key_support_field = CharField()
    affiliated_school = CharField()
    implementation_time = CharField()
    subject_category = CharField()
    major_category = CharField()
    establishment_time = CharField()
    project = ForeignKeyField(Project, backref='details')


class Member(BaseModel):
    name = CharField()
    grade = CharField(null=True)
    student_id = CharField()
    department = CharField(null=True)
    major = CharField(null=True)
    phone = CharField(null=True)
    email = CharField(null=True)
    is_leader = CharField()
    project = ForeignKeyField(Project, backref='members')


class Teacher(BaseModel):
    name = CharField()
    unit = CharField(null=True)
    professional_title = CharField()
    teacher_type = CharField()
    project = ForeignKeyField(Project, backref='teachers')


if not Project.table_exists():
    db.create_tables([Project, Breadcrumb, Detail, Member, Teacher])









