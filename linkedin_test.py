from linkedin_api import Linkedin

# Authenticate using any Linkedin account credentials
api = Linkedin('viveksharma.mtcse19@pec.edu.in', 'vivek@pec')

# GET a profile
profile = api.get_profile('manish-r-sharma-8596b554')

for key, value in profile.items():
    print("{0:>20} ......... {1}".format(key, value))
# GET a profiles contact info
# contact_info = api.get_profile_contact_info('billy-g')
# print(contact_info)
print("edun\n\n")
if profile.get('education'):
        for edu in profile.get('education'):
            for key, value in edu.items():
                print("{0:>20} ......... {1}".format(key, value))
            print("\n\n")

print("\nlatest experience\n\n")
if profile.get('experience'):
    for key, value in profile['experience'][0].items():
        print("{0:>20} ......... {1}".format(key, value))
    print("\n\n")
