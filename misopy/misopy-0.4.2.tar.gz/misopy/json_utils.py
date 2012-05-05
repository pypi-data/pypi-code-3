import os
import simplejson

def json_serialize(obj, filename):
    f = open(filename, 'w')
    simplejson.dump(obj, f, indent=1)	
    f.close()

def json_load_file(filename):
    if os.path.isdir(filename):
	raise Exception, "%s is a directory -- expected a JSON filename." %(filename)
    f = open(filename)
    obj = simplejson.load(f)
    return obj
