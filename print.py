Feenix_Template = open("/home/daniel/Desktop/Web-Template/Feenix/Feenix.txt").read()
ide = input("input a number: ")
desc = input("input a number: ")
ip = input("input a number: ")
prefix = input("input a number: ")


xml_Feenix_Template = Feenix_Template.format(ide = ide, desc = desc, ip = ip, prefix = prefix)
print(xml_Feenix_Template)