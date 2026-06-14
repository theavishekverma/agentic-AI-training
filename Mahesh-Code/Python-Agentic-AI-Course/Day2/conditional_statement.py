# Shortlist candidiates for a job based on their experience and skills
# Experience is  > 5 years
# Skills should include Python and SQL
# prerance location is Pune or Bangalore

'''
#If syntax
if <condition>:  # When this contion is true then the block of code will be executed
    <action>

if <continue>:
    <action>
elif <continue>:  # When the above condition is false and this condition is true then the block of code will be executed
    <action>
elif <continue>:  # When the above condition is false and this condition is true then the block of code will be executed
    <action>
else:
    <action>  # When all the above conditions are false then the block of code will be executed

'''

experience = int(input("Enter years of experience: "))
skills = input("Enter skills (comma separated): ").split(",") # This will split the input string into a list of skills
location = input("Enter preferred location: ") # This will split the input string into a list of locations
country=input("Enter your country: ") # This will split the input string into a list of countries

preferred_countries=["India","USA","UK"] # This is a list of preferred countries


print(f"Experience: {experience} years")
print(f"Skills: {skills}")
print(f"Preferred Location: {location}")

'''
if experience > 5:
    print("Satisfied : Candidate has more than 5 years of experience.")
else:
    print("Non Satisfied : Candidate does not have more than 5 years of experience.")    


if ( "python" in skills or "java" in skills ) and "sql" in skills:
    print("Satisfied : Candidate has both Python or Java and SQL skills.")
else:
    print("Non Satisfied : Candidate does not have both Python or Java and SQL skills.")    


if "pune" == location or "bangalore" == location:
    print("Satisfied : Candidate has preferred location as Pune or Bangalore.")
else:
    print("Non Satisfied : Candidate does not have preferred location as Pune or Bangalore.")    

if country not in preferred_countries:
    print("Non Satisfied : Candidate does not have a preferred country.")
else:
    print("Satisfied : Candidate has a preferred country.")    

'''

if experience > 5 and ( "python" in skills or "java" in skills ) \
    and "sql" in skills and ( "pune" == location or "bangalore" == location) \
      and country in preferred_countries:
    print("Candidate is shortlisted for the job.")
else:    
    print("Candidate is not shortlisted for the job.")

    