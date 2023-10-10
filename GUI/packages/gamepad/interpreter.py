from packages.models.input import Data
import config

def interpret(gamepad):
	
	#takes a gamepad object
	#return an inputData class corresponding to the controller input 
	
	
	
	for entry in config.top_data.val_names:
		
		x = convert(gamepad.read_value(config.map_dict[entry]))
		#if(entry == "UP"):
		#	print(x)
		config.top_data.assign(entry, x)
		#print all values of top data for debug
		#config.top_data.printclass()
		
# interprets mapping for second controller
def interpret2(gamepad2):
	
	
	for entry in config.arm_inputs.val_names:
		
		x = convert(gamepad2.read_value(config.map2_dict[entry]))
		config.arm_inputs.assign(entry, x)
	
	


def generate_dictionaries(filename):
	#gamepad_dict
	#for each line in map.txt
	#create a dictionary entry: 'VAL_NAME : BUTTON_NAME'
	
	filepath = "packages/gamepad/" + filename
	
	# create gamepad2's dict if gamepad's dict is already created
	# we only want to generate gamepad2's dict if gamepad's dict is already created
	if config.gamepad2_flag and config.map_dict != None:
		if config.map2_dict != None:
			return
		dictionary2 = {}
		file = open(filepath, 'r')
		for line in file:
			line = line.rstrip('\n')
			split = line.split("=")
			dictionary2[split[0].strip()] = split[1].strip()
		file.close()
		config.map2_dict = dictionary2
		return
		

	if config.map_dict != None:
		return 

	dictionary = {}

	file = open(filepath, 'r')
	
	for line in file:
		line = line.rstrip('\n')
		split = line.split("=")
		dictionary[split[0].strip()] = split[1].strip()

	#rint(dictionary)
	file.close()

	config.map_dict =  dictionary

def convert(input):
	if input is None:
		return 0
	elif input is True:
		return 1
	elif input is False:
		return 0
	else:
		return input
