import os
import json
 


 
dirs =  os.path.join(os.path.split(os.path.realpath(__file__))[0], 'json')
if not os.path.exists(dirs):
    os.makedirs(dirs)
with open(os.path.join(dirs, 'collection' + '.json'),'w', encoding='utf-8') as json_file:
    json.dump([1,2,3], json_file, ensure_ascii=False, indent=4)
 