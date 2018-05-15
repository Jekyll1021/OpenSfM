import json
import sys, os

if __name__ == "__main__":
	print "attempting to add gps to images"

	dataset_path = sys.argv[1]

	json_path = os.path.join(dataset_path, "ride.json")
	if os.path.exists(json_path):
		print "found ride.json, adding gps to images"

		if dataset_path[-1] == "/":
			dataset_path = dataset_path[:-1]

		# get all the files
		images = []
		imbase = os.path.join(dataset_path, "images")
        for im in os.listdir(imbase):
			imlow = im.lower()
			if ("jpg" in imlow) or ("png" in imlow) or ("jpeg" in imlow):
				images.append(im)
		images = sorted(images)

		with open(json_path) as data_file:
			data = json.load(data_file)

		if len(images) > 30*len(data['locations']) or len(images) < 29*len(data['locations']):
			print "length of gps insufficient, exit"
			exit(0)
		else:
			lst = []
			for i in range(len(images)):
				if i % 30 == 0:
					lst.append(data['locations'][int(i / 30)])
				elif i < (len(data['locations'])-1)*30+1):
					dct = {}
					dct['accuracy'] = 10.0
					dct['speed'] = 0.0
					front = data['locations'][int(i // 30)]
					back = data['locations'][int(i // 30) + 1]
					delta_course = (back['course'] - front['course'])/30
					delta_latitude = (back['latitude'] - front['latitude'])/30
					delta_longitude = (back['longitude'] - front['longitude'])/30
					delta_timestamp = (back['timestamp'] - front['timestamp'])/30
					dct['course'] = delta_course * (i%30) + front['course']
					dct['latitude'] = delta_latitude * (i%30) + front['latitude']
					dct['longitude'] = delta_longitude * (i%30) + front['longitude']
					dct['timestamp'] = int(delta_timestamp * (i%30) + front['timestamp'])
					lst.append(dct)
				else:
					dct = {}
					dct['accuracy'] = 10.0
					dct['speed'] = 0.0
					front = data['locations'][-2]
					back = data['locations'][-1]
					delta_course = (back['course'] - front['course'])/30
					delta_latitude = (back['latitude'] - front['latitude'])/30
					delta_longitude = (back['longitude'] - front['longitude'])/30
					delta_timestamp = (back['timestamp'] - front['timestamp'])/30
					dct['course'] = delta_course * (i%30) + front['course']
					dct['latitude'] = delta_latitude * (i%30) + front['latitude']
					dct['longitude'] = delta_longitude * (i%30) + front['longitude']
					dct['timestamp'] = int(delta_timestamp * (i%30) + front['timestamp'])
					lst.append(dct)
				data['locations'] = lst
				with open(json_path, 'w') as fp:
    				json.dump(data, fp)
    else:
		print "json not found"

	print "exit"
	print