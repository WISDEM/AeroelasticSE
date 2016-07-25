# Must be specified for each DLC
path_to_input_file = "/Users/michelleburns/Desktop/FST_VT_IECrunner_input.txt"

variables = []
with open(path_to_input_file) as runner_file:
	for line in runner_file.readlines():
		x = line.rsplit(" = ",1)[-1]
		variables.append(x)

print variables[1]
test_var = float(variables[1])



