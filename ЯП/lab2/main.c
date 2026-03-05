#include <stdlib.h>
#include <stdio.h>
#include <string.h>



typedef enum {
    RUSSIA,
    USA,
    UK,
    CHINA,
    JAPAN,
    OTHER
} Country;

typedef struct {
    int id;
    char* name;
    int age;
    char gender;
    int course;
    char* group;
    char* phone;
    char* email;
    Country country;
} Student;

typedef struct {
    char fac;
    int course;
    int num;
    Student** students;
} Group;

Student* createStudent(char* name, int age, char gender, int course,
                       char* group, char* phone, char* email, Country country) {
    Student* unit = (Student*)malloc(sizeof(Student));
    unit->name = name;
    unit->age = age;
    unit->gender = gender;
    unit->course = course;
    unit->group = group;
    unit->phone = phone;
    unit->email = email;
    unit->country = country;
    return unit;
}

char* groupToStr(Group* group) {
    char* result = (char*)malloc(20 * sizeof(char));
    sprintf(result, "%c3%d%d", group->fac, group->course, group->num);
    return result;
}

Group* createGroup(char fac, int course, int num, int size) {
    
    Group* group = (Group*)malloc(sizeof(Group));
    group -> fac = fac;
    group -> course = course;
    group -> num = num;

    group -> students = (Student**)malloc(size * sizeof(Student*));

     if (!group) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    for (int i = 0; i < size; i++) {
        group->students[i] = createStudent("Student", 18, 'M', course, groupToStr(group), "89123456789", "student@gmail.com", RUSSIA);
    }
    return group;
}


void printStudent(Student* student) {
    printf("name: %s\n", student->name);
    printf("age: %d\n", student->age);
    printf("gender: %c\n", student->gender);
    printf("course: %d\n", student->course);
    printf("group: %s\n", student->group);
    printf("phone: %s\n", student->phone);
    printf("email: %s\n", student->email);
    switch (student->country) {
        case RUSSIA:
            printf("country: Russia\n");
            break;
        case USA:
            printf("country: USA\n");
            break;
        case UK:
            printf("country: UK\n");
            break;
        case CHINA:
            printf("country: China\n");
            break;
        case JAPAN:
            printf("country: Japan\n");
            break;
        case OTHER:
            printf("country: Other\n");
            break;
    }
}



void serializeStudent(const Student* student, const char* filename) {
    if (!student || !filename) {
        fprintf(stderr, "Invalid arguments for serialization\n");
        return;
    }
 
    FILE* file = fopen(filename, "wb");
    if (!file) {
        fprintf(stderr, "Failed to open file for writing\n");
        return;
    }
 
    fwrite(student, sizeof(Student), 1, file);
    fclose(file);
}
 
Student* deserializeStudent(const char* filename) {
    if (!filename) {
        fprintf(stderr, "Invalid filename for deserialization\n");
        return NULL;
    }
 
    FILE* file = fopen(filename, "rb");
    if (!file) {
        fprintf(stderr, "Failed to open file for reading\n");
        return NULL;
    }
 
    Student* student = (Student*)malloc(sizeof(Student));
    if (!student) {
        fprintf(stderr, "Memory allocation failed\n");
        fclose(file);
        return NULL;
    }
 
    fread(student, sizeof(Student), 1, file);
    fclose(file);
 
    return student;
}

int main(){
    Group* group = createGroup('P', 2, 15, 3);
    char* groupStr = groupToStr(group);
    printf("%s\n", groupStr);
    free(groupStr);

    Student* student = group->students[0];
    printStudent(student);

    serializeStudent(student, "student.bin");
    free(student);

    Student* loadedStudent = deserializeStudent("student.bin");
    if (loadedStudent) {
        printStudent(loadedStudent);
        free(loadedStudent);
    }
    return 0;
}


